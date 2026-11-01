"""Extension: Lieberman's (1987) counter-test. Do incumbents build ahead of entrants?

If incumbents add capacity strategically to pre-empt entry, they should open new plants at
lower levels of utilization than newcomers do, so their openings should respond less to how
tight capacity is, above all in concentrated industries where pre-emption pays. If both build
only when capacity runs short, the two should respond alike. Lieberman found the second in 38
chemical products, 1952-1982. This reruns the comparison for US manufacturing, 2010-2023, with
plant openings by existing firms and by new firms from the Census Business Dynamics Statistics.

Reads results/panel_markets.csv (written by src/idle_capacity.py) and results/g17_panel.csv.

Usage:
    python src/who_builds.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "results"
BINS = 10   # bins of residual utilization for the figure


def poisson(formula, data, offset, cluster):
    """Poisson pseudo-maximum likelihood with an exposure offset and clustered errors."""
    m = smf.glm(formula, data, family=sm.families.Poisson(), offset=np.log(data[offset]))
    return m.fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(data[cluster])[0]})


def rows_from(res, model, spec, keep):
    ci = res.conf_int()
    out = []
    for v in keep:
        out.append(dict(model=model, spec=spec, term=v, coef=res.params[v], se=res.bse[v], ci_low=ci.loc[v, 0],
                        ci_high=ci.loc[v, 1], p=res.pvalues[v], n=int(res.nobs)))
    return out


def stack(p, count_new, count_old, exposure_new, exposure_old):
    """Long format: one row per market-year-builder type, for testing equal responses."""
    a = p.assign(count=p[count_new], exposure=p[exposure_new], existing=0)
    b = p.assign(count=p[count_old], exposure=p[exposure_old], existing=1)
    s = pd.concat([a, b], ignore_index=True)
    s["util_x_existing"] = s.util_lag * s.existing
    s["growth_x_existing"] = s.emp_growth_lag * s.existing
    s["util_x_high"] = s.util_lag * s.high_cr4
    s["util_x_existing_x_high"] = s.util_lag * s.existing * s.high_cr4
    s["mt"] = s.market.astype(str) + "_" + s.existing.astype(str)
    s["yt"] = s.year.astype(str) + "_" + s.existing.astype(str)
    return s[s.exposure > 0]


def main():
    p = pd.read_csv(OUT / "panel_markets.csv")
    print(f"loaded panel: {len(p)} market-years, {p.market.nunique()} markets, {p.year.min()}-{p.year.max()}")
    rows = []
    fe = " + C(market) + C(year)"
    for count, label in [("entry_new", "new firms' plants"), ("entry_existing", "existing firms' plants")]:
        res = poisson(f"{count} ~ util_lag + emp_growth_lag" + fe, p, "estab_denom", "market")
        rows += rows_from(res, "Poisson, plant openings", label, ["util_lag", "emp_growth_lag"])
    for count, label in [("birth_jobs_new", "jobs at new firms' plants"),
                         ("birth_jobs_existing", "jobs at existing firms' new plants")]:
        res = poisson(f"{count} ~ util_lag + emp_growth_lag" + fe, p, "emp_denom", "market")
        rows += rows_from(res, "Poisson, jobs at new plants", label, ["util_lag", "emp_growth_lag"])

    pre = p[p.year <= 2019]
    for count, label in [("entry_new", "new firms' plants, 2010-2019"), ("entry_existing", "existing firms' plants, 2010-2019")]:
        res = poisson(f"{count} ~ util_lag + emp_growth_lag" + fe, pre, "estab_denom", "market")
        rows += rows_from(res, "Poisson, plant openings", label, ["util_lag"])
    one = p.dropna(subset=["util_lag1"])
    for count, label in [("entry_new", "new firms' plants, one-year lag"), ("entry_existing", "existing firms' plants, one-year lag")]:
        res = poisson(f"{count} ~ util_lag1 + emp_growth_lag" + fe, one, "estab_denom", "market")
        rows += rows_from(res, "Poisson, plant openings", label, ["util_lag1"])

    s = stack(p, "entry_new", "entry_existing", "estab_denom", "estab_denom")
    res = poisson("count ~ util_lag + util_x_existing + emp_growth_lag + growth_x_existing + C(mt) + C(yt)",
                  s, "exposure", "market")
    rows += rows_from(res, "Poisson, stacked plants", "existing minus new", ["util_lag", "util_x_existing"])
    res = poisson("count ~ util_lag + util_x_existing + util_x_high + util_x_existing_x_high + emp_growth_lag"
                  " + growth_x_existing + C(mt) + C(yt)", s, "exposure", "market")
    rows += rows_from(res, "Poisson, stacked plants", "by concentration",
                      ["util_lag", "util_x_existing", "util_x_high", "util_x_existing_x_high"])
    sj = stack(p, "birth_jobs_new", "birth_jobs_existing", "emp_denom", "emp_denom")
    res = poisson("count ~ util_lag + util_x_existing + emp_growth_lag + growth_x_existing + C(mt) + C(yt)",
                  sj, "exposure", "market")
    rows += rows_from(res, "Poisson, stacked jobs", "existing minus new", ["util_lag", "util_x_existing"])

    # Share of new plants opened by existing firms (OLS, market and year effects, clustered by market)
    p["existing_share"] = p.entry_existing / (p.entry_existing + p.entry_new) * 100
    q = p.dropna(subset=["existing_share"]).assign(util_x_high=lambda d: d.util_lag * d.high_cr4)
    res = smf.ols("existing_share ~ util_lag + util_x_high + emp_growth_lag" + fe, q).fit(
        cov_type="cluster", cov_kwds={"groups": pd.factorize(q.market)[0]})
    rows += rows_from(res, "OLS, existing firms' share of openings", "by concentration", ["util_lag", "util_x_high"])

    g = pd.read_csv(OUT / "g17_panel.csv")
    gs = stack(g.assign(market=g.series, high_cr4=0), "entry_new", "entry_existing", "estab_denom", "estab_denom")
    res = poisson("count ~ util_lag + util_x_existing + emp_growth_lag + growth_x_existing + C(mt) + C(yt)",
                  gs, "exposure", "market")
    rows += rows_from(res, "Poisson, stacked plants, G.17 1982-2023", "existing minus new",
                      ["util_lag", "util_x_existing"])
    out = pd.DataFrame(rows)
    out.round(6).to_csv(OUT / "who_builds_regressions.csv", index=False)
    print(out[["model", "spec", "term", "coef", "se", "p", "n"]].round(4).to_string(index=False))

    # Who builds, by market: average shares over 2010-2023
    agg = p.groupby("market").agg(label=("label", "first"), cr4=("cr4", "first"), mean_util=("util_lag", "mean"),
                                  new_plants=("entry_new", "sum"), existing_plants=("entry_existing", "sum"),
                                  jobs_new=("birth_jobs_new", "sum"), jobs_existing=("birth_jobs_existing", "sum"),
                                  shipments_bn=("shipments_bn", "first"))
    agg["existing_share_plants"] = agg.existing_plants / (agg.existing_plants + agg.new_plants) * 100
    agg["existing_share_jobs"] = agg.jobs_existing / (agg.jobs_existing + agg.jobs_new) * 100
    agg["jobs_per_new_firm_plant"] = agg.jobs_new / agg.new_plants
    agg["jobs_per_existing_firm_plant"] = agg.jobs_existing / agg.existing_plants
    agg.sort_values("existing_share_jobs", ascending=False).round(2).to_csv(OUT / "who_builds_markets.csv")
    tot = p[["entry_new", "entry_existing", "birth_jobs_new", "birth_jobs_existing"]].sum()
    hi = p[p.high_cr4 == 1][["entry_new", "entry_existing", "birth_jobs_new", "birth_jobs_existing"]].sum()
    summary = pd.DataFrame({"all markets": tot, "markets with CR4 >= 50%": hi}).T
    summary["existing_share_plants"] = summary.entry_existing / (summary.entry_existing + summary.entry_new) * 100
    summary["existing_share_jobs"] = summary.birth_jobs_existing / (summary.birth_jobs_existing + summary.birth_jobs_new) * 100
    summary["jobs_per_new_firm_plant"] = summary.birth_jobs_new / summary.entry_new
    summary["jobs_per_existing_firm_plant"] = summary.birth_jobs_existing / summary.entry_existing
    summary["markets"] = [p.market.nunique(), p[p.high_cr4 == 1].market.nunique()]
    summary.round(2).to_csv(OUT / "who_builds_summary.csv")
    print(summary.round(2).to_string())

    # Figure: residual entry rates against residual utilization (market and year effects removed)
    d = p.copy()
    for c in ["util_lag", "new_rate", "existing_rate"]:
        d[c + "_r"] = smf.ols(f"{c} ~ C(market) + C(year)", d).fit().resid
    d["bin"] = pd.qcut(d.util_lag_r, BINS, labels=False)
    b = d.groupby("bin")[["util_lag_r", "new_rate_r", "existing_rate_r"]].mean()
    b.round(4).to_csv(OUT / "who_builds_binned.csv")
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.axhline(0, color="#bbbbbb", lw=0.8)
    ax.plot(b.util_lag_r, b.new_rate_r, "o-", color="#4a7bb7", label="Plants opened by new firms")
    ax.plot(b.util_lag_r, b.existing_rate_r, "s-", color="#c8553d", label="New plants opened by existing firms")
    ax.set_xlabel("Utilization two years earlier, points above or below the industry's usual level")
    ax.set_ylabel("Openings per 100 plants, above or below usual")
    ax.set_title("Newcomers barely react to idle capacity; incumbents build after slack years")
    ax.legend(frameon=False, fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / "openings_vs_utilization.png", dpi=150)
    plt.close(fig)
    print("wrote results/who_builds_regressions.csv, who_builds_markets.csv, who_builds_summary.csv, "
          "who_builds_binned.csv, openings_vs_utilization.png")


if __name__ == "__main__":
    main()
