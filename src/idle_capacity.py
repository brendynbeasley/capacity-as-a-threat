"""Spence (1977) on modern data: idle capacity, concentration and entry in US manufacturing.

Two tests of the theory that incumbents hold capacity to keep entrants out.

    Test 1 (cross-section, Spence against Dixit). Do concentrated, capital-heavy industries run
        with more idle capacity? Census QPC full-production utilization, averaged over 2015-2019,
        against 2017 Economic Census concentration, capital intensity and plant size.
    Test 2 (panel). Does idle capacity keep new firms out? New-firm plant openings from the
        Census Business Dynamics Statistics, 2010-2023, against utilization two years earlier,
        with industry and year fixed effects, and a long-run version on Federal Reserve G.17
        utilization for 1982-2023.

Run src/build_panel.py first. Writes CSVs and PNGs to results/ and the analysis panel to
results/panel_markets.csv, which src/who_builds.py reads.

Usage:
    python src/idle_capacity.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
DERIVED = ROOT / "data" / "derived"
OUT = ROOT / "results"

CROSS_YEARS = range(2015, 2020)   # five pre-pandemic years around the 2017 Economic Census
PANEL_YEARS = range(2010, 2024)   # BDS years whose two-year utilization lag is in the QPC (2008-2021)
LAG = 2                           # Lieberman (1987) uses utilization two years before a plant opens
MIN_QUARTERS = 3                  # an industry-year needs at least 3 of 4 quarters of QPC data
VOL_YEARS = range(1990, 2020)     # years for the employment-volatility control
HIGH_CR4 = 50.0                   # "concentrated" = top four firms make half the shipments or more

# Federal Reserve G.17 utilization series and the NAICS codes each one covers (3- or 4-digit)
G17_MAP = {
    "G311": ["311"], "G312": ["312"], "G313": ["313"], "G314": ["314"], "G315": ["315"],
    "G316": ["316"], "G321": ["321"], "G322": ["322"], "G323": ["323"], "G324": ["324"],
    "G325": ["325"], "G326": ["326"], "G327": ["327"], "G331": ["331"], "G332": ["332"],
    "G333": ["333"], "G334": ["334"], "G335": ["335"], "G3361T3": ["3361", "3362", "3363"],
    "G3364T9": ["3364", "3365", "3366", "3369"], "G337": ["337"], "G339": ["339"],
}


class UnionFind(dict):
    def find(self, x):
        self.setdefault(x, x)
        while self[x] != x:
            self[x] = self[self[x]]
            x = self[x]
        return x

    def union(self, a, b):
        self[self.find(a)] = self.find(b)


def load():
    q = pd.read_csv(DERIVED / "qpc_quarterly.csv", dtype={"qpc_code": str})
    ec = pd.read_csv(DERIVED / "ec2017_naics6.csv", dtype={"naics6": str})
    bds = pd.read_csv(DERIVED / "bds_naics4.csv", dtype={"naics4": str})
    g17 = pd.read_csv(DERIVED / "g17_annual.csv")
    print(f"loaded {len(q)} QPC rows, {len(ec)} Census industries, {len(bds)} BDS rows, {len(g17)} G.17 rows")
    return q, ec, bds, g17


def build_units(q, ec):
    """Group 6-digit NAICS codes into consistent QPC industries and into BDS-matchable markets.

    A QPC industry joins every QPC group whose definition overlapped another over 2008-2024.
    A market joins QPC industries that share a 4-digit NAICS code, so BDS data can be attached.
    """
    codes = ec.naics6.tolist()
    q["members"] = q.prefixes.map(lambda p: tuple(c for c in codes if any(c.startswith(x) for x in p.split(";"))))
    dropped = q[q.members.map(len) == 0]
    print(f"QPC rows dropped because the code has no 2017 NAICS match: {len(dropped)} "
          f"({', '.join(sorted(dropped.qpc_code.unique()))})")
    q = q[q.members.map(len) > 0].copy()
    uf = UnionFind()
    for m in q.members.unique():
        for c in m:
            uf.union(m[0], c)
    ec["industry"] = ec.naics6.map(uf.find)
    for c in codes:
        uf.union(c, "N4_" + c[:4])
    ec["market"] = ec.naics6.map(uf.find)
    q["industry"] = q.members.map(lambda m: ec.set_index("naics6").industry[m[0]])
    size = ec.groupby("industry").size()
    labels = {}
    for ind, d in q.groupby("industry"):
        full = d[d.members.map(len) == size[ind]].sort_values(["year", "quarter"])
        latest = d[d.year == d.year.max()]
        text = full.description.iloc[-1] if len(full) else "; ".join(sorted(set(latest.description)))
        labels[ind] = text.replace(" 1/", "").replace("mfg.", "manufacturing").strip()
    ec["qlabel"] = ec.industry.map(labels)
    print(f"{len(codes)} six-digit industries form {ec.industry.nunique()} QPC industries "
          f"and {ec.market.nunique()} BDS markets")
    return q, ec


def industry_utilization(q, ec):
    """Shipment-weighted utilization of each QPC industry by quarter, then by year."""
    ship = ec.set_index("naics6").shipments
    q["weight"] = q.members.map(lambda m: ship[list(m)].sum())
    q["covered"] = q.members.map(len)
    size = ec.groupby("industry").size()
    rows = []
    for (ind, y, qq), d in q.dropna(subset=["util"]).groupby(["industry", "year", "quarter"]):
        if d.covered.sum() != size[ind]:      # reported groups must cover the whole industry
            continue
        rows.append(dict(industry=ind, year=y, quarter=qq, util=np.average(d.util, weights=d.weight)))
    uq = pd.DataFrame(rows)
    ua = uq.groupby(["industry", "year"]).util.agg(["mean", "count"]).reset_index()
    kept = ua[ua["count"] >= MIN_QUARTERS].rename(columns={"mean": "util"}).drop(columns="count")
    print(f"utilization: {len(uq)} industry-quarters, {len(kept)} industry-years with >= {MIN_QUARTERS} quarters "
          f"({len(ua) - len(kept)} dropped)")
    return kept


def weighted_mean(d, col):
    """Shipment-weighted mean of a 6-digit measure over the codes where the Census published it."""
    ok = d[col].notna()
    return np.average(d.loc[ok, col], weights=d.loc[ok, "shipments"]) if ok.any() else np.nan


def unit_traits(ec, key):
    """Concentration, capital intensity and plant size for a grouping of 6-digit industries."""
    g = ec.groupby(key)
    t = pd.DataFrame({
        "shipments_bn": g.shipments.sum() / 1e6,
        "cr4": g.apply(lambda d: weighted_mean(d, "cr4")),
        "hhi": g.apply(lambda d: weighted_mean(d, "hhi")),
        "capital_intensity": g.assets_end.sum() / g.shipments.sum(),
        "plants": g.plants.sum(),
        "ship_per_plant_m": g.shipments.sum() / g.plants.sum() / 1e3,
        "naics6_count": g.size(),
        "label": g.qlabel.apply(lambda s: "; ".join(sorted(set(s)))),
    })
    return t


def ols(formula, data, weights=None, cluster=None):
    if weights is not None:
        m = smf.wls(formula, data, weights=data[weights])
    else:
        m = smf.ols(formula, data)
    if cluster is not None:
        return m.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(data[cluster])[0]})
    return m.fit(cov_type="HC1")


def coef_rows(res, test, spec, n_clusters=None):
    rows = []
    ci = res.conf_int()
    for v in res.params.index:
        if v == "Intercept" or v.startswith("C("):
            continue
        rows.append(dict(test=test, spec=spec, term=v, coef=res.params[v], se=res.bse[v],
                         ci_low=ci.loc[v, 0], ci_high=ci.loc[v, 1], p=res.pvalues[v],
                         n=int(res.nobs), clusters=n_clusters, r2=res.rsquared))
    return rows


def lincom(res, expr, test, spec, term):
    """A linear combination of coefficients (e.g. a slope for one group) with its test."""
    tt = res.t_test(expr)
    ci = np.asarray(tt.conf_int()).ravel()
    return dict(test=test, spec=spec, term=term, coef=float(np.ravel(tt.effect)[0]), se=float(np.ravel(tt.sd)[0]),
                ci_low=ci[0], ci_high=ci[1], p=float(np.ravel(tt.pvalue)[0]), n=int(res.nobs), clusters=None,
                r2=res.rsquared)


def employment_volatility(bds, ec, key):
    """Standard deviation of annual log employment growth, 1990-2019, for each unit's 4-digit codes."""
    n4 = ec.groupby(key).naics6.apply(lambda s: sorted(set(s.str[:4])))
    out = {}
    for unit, codes in n4.items():
        e = bds[bds.naics4.isin(codes)].groupby("year").emp.sum().sort_index()
        growth = np.log(e).diff()
        out[unit] = growth[growth.index.isin(VOL_YEARS)].std() * 100
    return pd.Series(out, name="emp_volatility")


def cross_section(ua, ec, bds, rows):
    traits = unit_traits(ec, "industry")
    traits["emp_volatility"] = employment_volatility(bds, ec, "industry")
    win = ua[ua.year.isin(CROSS_YEARS)].groupby("industry").util.agg(["mean", "count"])
    cs = traits.join(win[win["count"] == len(CROSS_YEARS)]["mean"].rename("util"), how="inner")
    print(f"cross-section: {len(cs)} QPC industries with all five years 2015-2019 "
          f"({len(traits) - len(cs)} dropped for incomplete utilization data)")
    print(f"cross-section: {cs.hhi.notna().sum()} of {len(cs)} industries have a published HHI "
          f"(the HHI regression drops the rest)")
    cs["idle"] = 100 - cs.util
    cs["ln_plant_size"] = np.log(cs.ship_per_plant_m)
    cs["k_high"] = (cs.capital_intensity > cs.capital_intensity.median()).astype(int)
    cs["cr4_x_k"] = cs.cr4 * cs.capital_intensity
    cs["cr4_x_k_high"] = cs.cr4 * cs.k_high
    specs = {
        "concentration only": "util ~ cr4",
        "plus controls": "util ~ cr4 + capital_intensity + ln_plant_size + emp_volatility",
        "Spence interaction": "util ~ cr4 + k_high + cr4_x_k_high + ln_plant_size + emp_volatility",
        "Spence interaction, continuous": "util ~ cr4 + capital_intensity + cr4_x_k + ln_plant_size + emp_volatility",
        "HHI instead of CR4": "util ~ I(hhi / 100) + capital_intensity + ln_plant_size + emp_volatility",
    }
    for name, f in specs.items():
        res = ols(f, cs)
        rows += coef_rows(res, "cross-section 2015-19", name)
        if name == "Spence interaction":
            rows.append(lincom(res, "cr4 + cr4_x_k_high", "cross-section 2015-19", name, "cr4 slope, capital-heavy"))
    rows += coef_rows(ols(specs["plus controls"], cs, weights="shipments_bn"), "cross-section 2015-19",
                      "plus controls, shipment-weighted")
    later = ua[ua.year.isin(range(2021, 2025))].groupby("industry").util.mean().rename("util")
    cs2 = traits.join(later, how="inner")
    cs2["ln_plant_size"] = np.log(cs2.ship_per_plant_m)
    cs2["k_high"] = (cs2.capital_intensity > cs2.capital_intensity.median()).astype(int)
    cs2["cr4_x_k_high"] = cs2.cr4 * cs2.k_high
    rows += coef_rows(ols(specs["plus controls"], cs2), "cross-section 2021-24", "plus controls")
    res = ols(specs["Spence interaction"], cs2)
    rows += coef_rows(res, "cross-section 2021-24", "Spence interaction")
    rows.append(lincom(res, "cr4 + cr4_x_k_high", "cross-section 2021-24", "Spence interaction", "cr4 slope, capital-heavy"))
    corr = cs[["util", "cr4", "capital_intensity", "ln_plant_size", "emp_volatility"]].corr()
    corr.round(3).to_csv(OUT / "cross_section_correlations.csv")
    cs["cr4_band"] = pd.cut(cs.cr4, [0, 30, 50, 101], right=False, labels=["under 30%", "30-50%", "50% or more"])
    bands = cs.groupby(["cr4_band", "k_high"], observed=True).agg(
        industries=("util", "size"), mean_util=("util", "mean"), mean_cr4=("cr4", "mean"),
        mean_capital_intensity=("capital_intensity", "mean")).reset_index()
    bands["k_high"] = bands.k_high.map({0: "below median", 1: "above median"})
    bands.round(2).to_csv(OUT / "cross_section_bands.csv", index=False)
    cs.sort_values("util").round(3).to_csv(OUT / "cross_section_industries.csv")
    return cs


# Industries labeled on the scatter (start of the QPC label -> short name)
SCATTER_LABELS = {
    "Paperboard mills": "Paperboard mills", "Light truck": "Light trucks and SUVs",
    "Petroleum refineries": "Refineries", "Ethyl alcohol": "Ethanol", "Pulp mills": "Pulp mills",
    "Aerospace": "Aerospace", "Cement manufacturing": "Cement", "Ready-mix": "Ready-mix concrete",
    "Audio and video": "Audio and video equipment", "Leather and hide": "Leather tanning",
    "Heavy duty truck": "Heavy trucks", "Lime and gypsum": "Lime and gypsum",
    "Semiconductor": "Semiconductors", "Alumina and aluminum": "Aluminum", "Tire manufacturing": "Tires",
}


def scatter(cs):
    fig, ax = plt.subplots(figsize=(7.5, 5))
    hi = cs.k_high == 1
    for mask, color, name in [(~hi, "#4a7bb7", "Capital per dollar of shipments below the median"),
                              (hi, "#c8553d", "Capital per dollar of shipments above the median")]:
        ax.scatter(cs.cr4[mask], cs.util[mask], s=np.sqrt(cs.shipments_bn[mask]) * 6, alpha=0.6, color=color)
        ax.scatter([], [], s=40, color=color, alpha=0.6, label=name)
        b = np.polyfit(cs.cr4[mask], cs.util[mask], 1)
        xs = np.linspace(cs.cr4[mask].min(), cs.cr4[mask].max(), 50)
        ax.plot(xs, b[1] + b[0] * xs, color=color, lw=1.2)
    for _, r in cs.iterrows():
        short = [v for k, v in SCATTER_LABELS.items() if r.label.startswith(k)]
        if short:
            ax.annotate(short[0], (r.cr4, r.util), fontsize=7.5, xytext=(4, -3), textcoords="offset points")
    ax.set_ylim(44, 101)
    ax.set_xlabel("Top four firms' share of shipments, 2017 (%)")
    ax.set_ylabel("Output as % of full capacity, 2015-2019 average")
    ax.set_title("Capital-heavy concentrated industries run fuller, not emptier")
    ax.legend(fontsize=8, loc="upper left", frameon=False)
    fig.tight_layout()
    fig.savefig(OUT / "utilization_vs_concentration.png", dpi=150)
    plt.close(fig)


def add_rates(b, key):
    """Sum BDS counts to a unit and compute entry rates per 100 plants and per 100 jobs.

    Plant rates divide by the average of this year's and last year's plant counts, the BDS
    convention; job rates divide by the BDS employment denominator, which follows the same rule.
    """
    cols = ["estabs", "emp_denom", "emp", "entry_all", "entry_new", "entry_existing", "estabs_exit",
            "birth_jobs_new", "birth_jobs_existing"]
    m = b.groupby([key, "year"])[cols].sum(min_count=1).reset_index().sort_values([key, "year"])
    m["estab_denom"] = (m.estabs + m.groupby(key).estabs.shift(1)) / 2
    m["new_rate"] = m.entry_new / m.estab_denom * 100
    m["existing_rate"] = m.entry_existing / m.estab_denom * 100
    m["exit_rate"] = m.estabs_exit / m.estab_denom * 100
    m["new_job_rate"] = m.birth_jobs_new / m.emp_denom * 100
    m["existing_job_rate"] = m.birth_jobs_existing / m.emp_denom * 100
    m["emp_growth_lag"] = m.groupby(key).emp.transform(
        lambda e: (np.log(e).shift(LAG) - np.log(e).shift(LAG + 2)) / 2 * 100)
    return m


def build_panel(ua, ec, bds):
    """Market-year panel: BDS plant openings in year t against utilization in calendar year t - LAG."""
    ship = ec.set_index("industry").groupby(level=0).shipments.sum()
    ind_market = ec.drop_duplicates("industry").set_index("industry").market
    u = ua.assign(market=ua.industry.map(ind_market), w=ua.industry.map(ship))
    n_ind = ec.groupby("market").industry.nunique()
    mu = u.groupby(["market", "year"]).apply(
        lambda d: pd.Series({"util": np.average(d.util, weights=d.w), "n": d.industry.nunique()})).reset_index()
    mu = mu[mu.n == mu.market.map(n_ind)].drop(columns="n")
    n4 = ec.groupby("market").naics6.apply(lambda s: sorted(set(s.str[:4])))
    b = bds.assign(market=bds.naics4.map({c: m for m, cs in n4.items() for c in cs}))
    bm = add_rates(b, "market")
    bm["emp_growth_lag"] = bm.groupby("market").emp.transform(lambda e: (np.log(e).shift(LAG) - np.log(e).shift(LAG + 2)) / 2 * 100)
    mu["year"] = mu.year + LAG
    mu = mu.rename(columns={"util": "util_lag"})
    p = bm.merge(mu, on=["market", "year"], how="inner")
    lag1 = u.groupby(["market", "year"]).apply(lambda d: np.average(d.util, weights=d.w)).rename("util_lag1").reset_index()
    lag1["year"] = lag1.year + 1
    p = p.merge(lag1, on=["market", "year"], how="left")
    p = p[p.year.isin(PANEL_YEARS)].copy()
    traits = unit_traits(ec, "market")
    p = p.merge(traits, left_on="market", right_index=True)
    p["high_cr4"] = (p.cr4 >= HIGH_CR4).astype(int)
    p["k_high"] = (p.capital_intensity > traits.capital_intensity.median()).astype(int)
    before = len(p)
    p = p.dropna(subset=["new_rate", "existing_rate", "util_lag", "emp_growth_lag"])
    print(f"panel: {len(p)} market-years for {p.market.nunique()} markets, {p.year.min()}-{p.year.max()} "
          f"({before - len(p)} dropped for missing entry or growth data)")
    return p


def panel_tests(p, rows):
    g = p.market.nunique()
    base = "new_rate ~ util_lag + emp_growth_lag + C(market) + C(year)"
    rows += coef_rows(ols(base, p, cluster="market"), "panel new-firm entry", "baseline", g)
    rows += coef_rows(ols("new_rate ~ util_lag1 + emp_growth_lag + C(market) + C(year)", p.dropna(subset=["util_lag1"]),
                          cluster="market"), "panel new-firm entry", "one-year lag", g)
    rows += coef_rows(ols(base, p, weights="estabs", cluster="market"), "panel new-firm entry", "plant-weighted", g)
    p = p.assign(util_x_high_cr4=p.util_lag * p.high_cr4, util_x_k_high=p.util_lag * p.k_high)
    rows += coef_rows(ols("new_rate ~ util_lag + util_x_high_cr4 + emp_growth_lag + C(market) + C(year)", p,
                          cluster="market"), "panel new-firm entry", "by concentration", g)
    rows += coef_rows(ols("new_rate ~ util_lag + util_x_k_high + emp_growth_lag + C(market) + C(year)", p,
                          cluster="market"), "panel new-firm entry", "by capital intensity", g)
    rows += coef_rows(ols("new_rate ~ util_lag + emp_growth_lag + C(market) + C(year)",
                          p[p.year <= 2019], cluster="market"), "panel new-firm entry", "2010-2019 only", g)
    rows += coef_rows(ols("new_job_rate ~ util_lag + emp_growth_lag + C(market) + C(year)", p, cluster="market"),
                      "panel new-firm entry", "jobs at new firms' plants", g)
    rows += coef_rows(ols("exit_rate ~ util_lag + emp_growth_lag + C(market) + C(year)", p, cluster="market"),
                      "panel plant exits", "baseline", g)


def g17_panel(g17, bds, rows):
    """Long-run check: 22 G.17 manufacturing industries, BDS years 1982-2023."""
    recs = []
    for s, prefixes in G17_MAP.items():
        b = bds[bds.naics4.str[:len(prefixes[0])].isin(prefixes) if len(prefixes[0]) == 3
                else bds.naics4.isin(prefixes)]
        recs.append(b.assign(series=s))
    b = add_rates(pd.concat(recs), "series")
    u = g17[g17.series.isin(G17_MAP)][["series", "year", "util"]].copy()
    u["year"] = u.year + LAG
    p = b.merge(u.rename(columns={"util": "util_lag"}), on=["series", "year"])
    p = p[p.year.between(1982, 2023)].dropna()
    print(f"G.17 long-run panel: {len(p)} industry-years, {p.series.nunique()} industries, {p.year.min()}-{p.year.max()}")
    for y in ["new_rate", "existing_rate", "new_job_rate"]:
        res = ols(f"{y} ~ util_lag + emp_growth_lag + C(series) + C(year)", p, cluster="series")
        rows += coef_rows(res, f"G.17 long run {y.replace('_rate', '')}", "baseline", p.series.nunique())
    p.round(4).to_csv(OUT / "g17_panel.csv", index=False)


def main():
    OUT.mkdir(exist_ok=True)
    q, ec, bds, g17 = load()
    q, ec = build_units(q, ec)
    ua = industry_utilization(q, ec)
    labels = unit_traits(ec, "industry").label
    ua.assign(label=ua.industry.map(labels)).round(2).to_csv(OUT / "utilization_by_industry_year.csv", index=False)
    rows = []
    cs = cross_section(ua, ec, bds, rows)
    scatter(cs)
    p = build_panel(ua, ec, bds)
    panel_tests(p, rows)
    g17_panel(g17, bds, rows)
    res = pd.DataFrame(rows)
    res.round(6).to_csv(OUT / "regressions.csv", index=False)
    p.round(4).to_csv(OUT / "panel_markets.csv", index=False)
    ms = p.groupby("market").agg(label=("label", "first"), cr4=("cr4", "first"),
                                 capital_intensity=("capital_intensity", "first"), shipments_bn=("shipments_bn", "first"),
                                 mean_util_2008_21=("util_lag", "mean"), min_util=("util_lag", "min"),
                                 new_rate=("new_rate", "mean"), existing_rate=("existing_rate", "mean"),
                                 exit_rate=("exit_rate", "mean"), plants_2023=("estabs", "last"))
    ms.sort_values("mean_util_2008_21").round(2).to_csv(OUT / "market_summary.csv")
    means = pd.DataFrame({"market_years": [len(p)], "markets": [p.market.nunique()],
                          "mean_new_rate": [p.new_rate.mean()], "mean_existing_rate": [p.existing_rate.mean()],
                          "mean_exit_rate": [p.exit_rate.mean()], "mean_util_lag": [p.util_lag.mean()]})
    means.round(3).to_csv(OUT / "panel_summary.csv", index=False)
    show = res[res.term.isin(["cr4", "cr4_x_k", "cr4_x_k_high", "k_high", "I(hhi / 100)", "cr4 slope, capital-heavy", "util_lag", "util_lag1", "util_x_high_cr4", "util_x_k_high"])]
    print(show[["test", "spec", "term", "coef", "se", "p", "n"]].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
