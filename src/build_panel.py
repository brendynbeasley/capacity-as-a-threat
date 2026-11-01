"""Build the industry tables used by the capacity and entry tests.

Reads four public sources and writes tidy CSVs to data/derived/:

    Census Quarterly Survey of Plant Capacity Utilization (QPC), 2008-2024 quarterly tables
        -> qpc_quarterly.csv  (industry group, year, quarter, full-production utilization rate)
    Census 2017 Economic Census, manufacturing concentration and basic statistics
        -> ec2017_naics6.csv  (6-digit NAICS: shipments, firms, plants, CR4, HHI, assets)
    Census Business Dynamics Statistics (BDS), 2023 release, NAICS 4-digit by firm age
        -> bds_naics4.csv     (plant openings by new firms and by existing firms, 1978-2023)
    Federal Reserve G.17 capacity utilization by industry (used only for a long-run check)
        -> g17_annual.csv

Missing raw files are downloaded into data/raw/. The QPC tables, the Economic Census zips
and the G.17 file are small and committed; the BDS files (about 21 MB) are fetched.

Usage:
    python src/build_panel.py
"""

import re
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"

QPC_YEARS = range(2008, 2025)   # 2025 onward uses a redesigned set of industry groups
QPC_BASE = "https://www2.census.gov/programs-surveys/qpc/tables/"
BDS_BASE = "https://www2.census.gov/programs-surveys/bds/tables/time-series/2023/"
BDS_FILES = ["bds2023_vcn4.csv", "bds2023_vcn4_fa.csv"]
G17_URL = "https://www.federalreserve.gov/releases/g17/ipdisk/utl_sa.txt"
UA = {"User-Agent": "Mozilla/5.0 (research; capacity and entry study)"}


def fetch(url, dest):
    """Download url to dest unless it is already there (write to a temp name first)."""
    if dest.exists():
        return
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"  downloading {url}")
    req = urllib.request.Request(url, headers=UA)
    tmp = dest.with_suffix(dest.suffix + ".part")
    with urllib.request.urlopen(req, timeout=300) as r, open(tmp, "wb") as f:
        f.write(r.read())
    tmp.rename(dest)


def list_dir(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", "ignore")
    return re.findall(r'href="([^"?/][^"]*\.xlsx?)"', html)


def fetch_qpc():
    qdir = RAW / "qpc"
    have = {p.name[:4] for p in qdir.glob("*.xls*")} if qdir.exists() else set()
    for y in QPC_YEARS:
        if str(y) in have:
            continue
        for sub in ("", "qpc-quarterly-tables/"):
            try:
                names = list_dir(f"{QPC_BASE}{y}/{sub}")
            except Exception:
                names = []
            for n in names:
                if "old" not in n:
                    fetch(f"{QPC_BASE}{y}/{sub}{n}", qdir / n)


def expand_code(code):
    """Turn a QPC code list such as '3111,7,8', '31193-9' or '3321,2,4-6' into NAICS prefixes."""
    parts = code.split(",")
    first = parts[0]
    out = []
    if "-" in first:
        base, hi = first.split("-")
        out += [base[: len(base) - len(hi)] + str(d).zfill(len(hi)) for d in range(int(base[-len(hi):]), int(hi) + 1)]
    else:
        base = first
        out.append(base)
    for p in parts[1:]:
        if "-" in p:
            lo, hi = p.split("-")
            out += [base[: len(base) - len(lo)] + str(d).zfill(len(lo)) for d in range(int(lo), int(hi) + 1)]
        else:
            out.append(base[: len(base) - len(p)] + p)
    return out


def parse_qpc():
    rows = []
    files = sorted((RAW / "qpc").glob("*.xls*"))
    for f in files:
        m = re.match(r"(\d{4})[_-].*q(\d)\.xlsx?$", f.name)
        y, q = int(m.group(1)), int(m.group(2))
        if y not in QPC_YEARS:
            continue
        engine = "xlrd" if f.suffix == ".xls" else "openpyxl"
        book = pd.ExcelFile(f, engine=engine)
        sheet = [s for s in book.sheet_names
                 if s.lower().startswith("table 1") or "full" in s.lower() or s.lower() == "utilization rates"][0]
        d = pd.read_excel(f, sheet_name=sheet, header=None, dtype=object, engine=engine)
        for i in range(12):
            vals = [str(v).strip().lower() for v in d.iloc[i].tolist()]
            if any(v.startswith("utilization rate") for v in vals):
                hdr = i
                col = [j for j, v in enumerate(vals) if v.startswith("utilization rate")][0]
                break
        for i in range(hdr + 1, len(d)):
            code, desc = d.iat[i, 0], d.iat[i, 1]
            if pd.isna(code) or pd.isna(desc):
                continue
            code = re.sub(r"\s+", "", str(code))
            if not re.match(r"^3[1-3]\d\d", code):   # manufacturing industry groups only
                continue
            rows.append(dict(year=y, quarter=q, qpc_code=code,
                             description=re.sub(r"\s+", " ", str(desc)).strip(),
                             util=pd.to_numeric(d.iat[i, col], errors="coerce"),
                             util_se=pd.to_numeric(d.iat[i, col + 1], errors="coerce")))
    df = pd.DataFrame(rows)
    print(f"QPC: {len(files)} quarterly files, {len(df)} industry-quarter rows, "
          f"{df.qpc_code.nunique()} distinct code strings")
    return df


def read_ec(zip_path):
    df = pd.read_csv(zip_path, sep="|", dtype=str, compression="zip")
    df.columns = [c.lstrip("#") for c in df.columns]
    return df


def parse_ec2017():
    conc = read_ec(RAW / "census" / "EC1700SIZECONCEN.zip")
    conc = conc[(conc.GEOTYPE == "01") & (conc.SECTOR == "31") & (conc.NAICS2017.str.len() == 6)].copy()
    num = lambda s: pd.to_numeric(s, errors="coerce")
    # Census writes 0 in the value column when a figure is withheld (flag "D"); treat those as missing
    conc.loc[conc.VAL_PCT_F == "D", "VAL_PCT"] = None
    conc.loc[conc.HHI_F == "D", "HHI"] = None
    wide = conc.pivot_table(index=["NAICS2017", "NAICS2017_TTL"], columns="CONCENFI",
                            values="VAL_PCT", aggfunc="first").reset_index()
    hhi = conc[conc.CONCENFI == "650"].set_index("NAICS2017").HHI
    out = pd.DataFrame({"naics6": wide.NAICS2017, "label": wide.NAICS2017_TTL,
                        "cr4": num(wide["604"]), "cr8": num(wide["608"])})
    out["hhi"] = num(out.naics6.map(hhi))
    basic = read_ec(RAW / "census" / "EC1731BASIC.zip")
    basic = basic[(basic.GEOTYPE == "01") & (basic.NAICS2017.str.len() == 6)]
    keep = {"NAICS2017": "naics6", "FIRM": "firms", "ESTAB": "plants", "RCPTOT": "shipments",
            "VALADD": "value_added", "ASTEND": "assets_end", "CEXTOT": "capex", "EMP": "employees"}
    basic = basic[list(keep)].rename(columns=keep)
    for c in list(keep.values())[1:]:
        basic[c] = num(basic[c])
    out = basic.merge(out, on="naics6", how="left")
    print(f"Economic Census 2017: {len(out)} six-digit manufacturing industries, "
          f"{out.cr4.notna().sum()} with a published CR4, {out.hhi.notna().sum()} with a published HHI, "
          f"{out.assets_end.notna().sum()} with assets")
    return out


def parse_bds():
    for n in BDS_FILES:
        fetch(BDS_BASE + n, RAW / "bds" / n)
    tot = pd.read_csv(RAW / "bds" / "bds2023_vcn4.csv", dtype={"vcnaics4": str}, na_values=["X", "D", "S", "N"])
    fa = pd.read_csv(RAW / "bds" / "bds2023_vcn4_fa.csv", dtype={"vcnaics4": str}, na_values=["X", "D", "S", "N"])
    tot = tot[tot.vcnaics4.str[:2].isin(["31", "32", "33"])]
    fa = fa[fa.vcnaics4.str[:2].isin(["31", "32", "33"])]
    fa["new_firm"] = fa.fage.str.startswith("a)")
    ent = fa.groupby(["year", "vcnaics4", "new_firm"]).estabs_entry.sum(min_count=1).unstack()
    ent.columns = ["entry_existing" if not c else "entry_new" for c in ent.columns]
    jobs = fa.groupby(["year", "vcnaics4", "new_firm"]).job_creation_births.sum(min_count=1).unstack()
    jobs.columns = ["birth_jobs_existing" if not c else "birth_jobs_new" for c in jobs.columns]
    out = tot[["year", "vcnaics4", "firms", "estabs", "denom", "emp", "estabs_entry", "estabs_exit",
               "job_creation_births", "net_job_creation_rate"]].merge(ent.reset_index(), on=["year", "vcnaics4"], how="left")
    out = out.merge(jobs.reset_index(), on=["year", "vcnaics4"], how="left")
    # BDS "denom" is the employment denominator (average of this year's and last year's employment)
    out = out.rename(columns={"vcnaics4": "naics4", "estabs_entry": "entry_all", "denom": "emp_denom"})
    gap = (out.entry_all - out.entry_new - out.entry_existing).abs().max()
    print(f"BDS: {len(out)} NAICS4-year rows for {out.naics4.nunique()} manufacturing industries, "
          f"{out.year.min()}-{out.year.max()}; largest gap between total and firm-age entry counts = {gap}")
    return out


def parse_g17():
    fetch(G17_URL, RAW / "g17" / "utl_sa.txt")
    rows = []
    for line in open(RAW / "g17" / "utl_sa.txt", encoding="latin-1"):
        parts = line.split()
        if len(parts) >= 3 and parts[0].startswith('"') and parts[1].isdigit():
            vals = pd.to_numeric(pd.Series(parts[2:]), errors="coerce")
            rows.append(dict(series=parts[0].strip('"'), year=int(parts[1]), util=vals.mean(), months=vals.notna().sum()))
    g = pd.DataFrame(rows)
    g = g[g.months == 12]
    print(f"G.17: {g.series.nunique()} utilization series, {g.year.min()}-{g.year.max()}")
    return g


def main():
    DERIVED.mkdir(parents=True, exist_ok=True)
    fetch_qpc()
    qpc = parse_qpc()
    qpc["prefixes"] = qpc.qpc_code.map(lambda c: ";".join(expand_code(c)))
    qpc.to_csv(DERIVED / "qpc_quarterly.csv", index=False)
    ec = parse_ec2017()
    ec.to_csv(DERIVED / "ec2017_naics6.csv", index=False)
    bds = parse_bds()
    bds.to_csv(DERIVED / "bds_naics4.csv", index=False)
    g17 = parse_g17()
    g17.to_csv(DERIVED / "g17_annual.csv", index=False)
    print("wrote data/derived/qpc_quarterly.csv, ec2017_naics6.csv, bds_naics4.csv, g17_annual.csv")


if __name__ == "__main__":
    main()
