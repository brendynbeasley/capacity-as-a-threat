# Technical notes

This is the technical companion to the [README](README.md). It covers the data, the rules, every test statistic and
how to reproduce the results. Every table is in [results/FINDINGS.md](results/FINDINGS.md).

## The original study

A. Michael Spence, "Entry, Capacity, Investment and Oligopolistic Pricing," *Bell Journal of Economics* 8(2),
Autumn 1977, pp. 534–544, read with Avinash Dixit, "The Role of Investment in Entry-Deterrence," *Economic Journal*
90(357), March 1980, pp. 95–106. Both are theory papers with no data. Spence's abstract states that entry is deterred
when incumbents hold enough capacity to make entry unprofitable, that this capacity need not be fully used before
entry, and that the result is higher costs and prices than limit-price models imply. Dixit's correction, as summarized
by Lieberman (1987, p. 609), is that under linear demand and costs an incumbent gains nothing by raising output after
entry, so deterring capacity is capacity that is used. The empirical benchmark is Lieberman (1987): 38 chemical
products, 839 product-years, entrants' and incumbents' plant-building thresholds statistically indistinguishable
(Tables IV and V), strategic excess capacity found in 3 products.

## Headline results

| Test | Estimate (SE) | 95% CI | N |
|---|---|---|---|
| Utilization on CR4, capital-heavy industries, 2015–19 ($`\beta+\delta`$) | 0.113 (0.081) | [−0.046, 0.272] | 89 |
| Same, 2021–24 | 0.202 (0.078) | [0.049, 0.355] | 90 |
| Utilization on CR4, light industries, 2015–19 ($`\beta`$) | −0.270 (0.107) | [−0.480, −0.059] | 89 |
| Difference, heavy minus light ($`\delta`$) | 0.383 (0.121) | [0.145, 0.621] | 89 |
| New-firm openings per 100 plants on $`U_{t-2}`$ (OLS, FE) | 0.014 (0.013) | [−0.011, 0.040] | 944 |
| New firms, Poisson | 0.0033 (0.0024) | [−0.0013, 0.0080] | 944 |
| Incumbents, Poisson | −0.0102 (0.0025) | [−0.0150, −0.0053] | 944 |
| Incumbents minus new firms, stacked Poisson | −0.0135 (0.0040) | [−0.0213, −0.0057] | 1,888 |

Spence predicts $`\beta+\delta<0`$ and a positive coefficient on lagged utilization for new-firm entry. The first
estimate has the opposite sign (significant in 2021–24, not in 2015–19), and the second is small and not significant.

## Data

- **Utilization:** US Census Bureau, Quarterly Survey of Plant Capacity Utilization, Table 1 (full production
  utilization rates), all quarterly files for 2008–2024 from `www2.census.gov/programs-surveys/qpc/tables/`
  (68 files in `data/raw/qpc/`, downloaded November 2026). 2025 onward uses a redesigned set of groups and is not used.
- **Concentration and plant traits:** 2017 Economic Census, `EC1700SIZECONCEN.zip` (CR4, CR8, HHI for 360 six-digit
  manufacturing industries) and `EC1731BASIC.zip` (shipments, plants, firms, gross depreciable assets), in
  `data/raw/census/`.
- **Openings:** Census Business Dynamics Statistics, 2023 release, `bds2023_vcn4.csv` and `bds2023_vcn4_fa.csv`
  (NAICS 4-digit, by firm age, 1978–2023). About 21 MB, fetched into `data/raw/bds/` and not committed.
- **Long-run utilization:** Federal Reserve Board G.17, `utl_sa.txt` (monthly, seasonally adjusted, 57 series), in
  `data/raw/g17/`.
- **Derived tables (committed):** `data/derived/qpc_quarterly.csv`, `ec2017_naics6.csv`, `bds_naics4.csv`,
  `g17_annual.csv`, written by `src/build_panel.py`.

## Method

Rules fixed before looking at the results:

- **Industries:** QPC code lists are expanded to 2017 six-digit NAICS codes. Groups whose definitions overlapped at
  any point in 2008–2024 are merged (union-find), giving 90 consistent industries. An industry-quarter is kept only if
  the groups reported that quarter cover the whole industry; group rates are combined with 2017 shipment weights.
  Annual utilization is the mean of quarters, with at least 3 of 4 required. Three codes with no 2017 match
  (31523, 31529, 334411) are dropped.
- **Industry traits:** CR4 and HHI are shipment-weighted averages of six-digit values, using only the codes where
  the Census published the figure. The Census withholds CR4 for one code (311930, flavoring syrups) and HHI for 72
  codes, writing 0 in their place; these are treated as missing, so 3 of the 89 cross-section industries have no HHI. Capital intensity is
  end-of-year gross depreciable assets over shipments; "capital-heavy" means above the median, 0.60. Plant size is
  shipments per plant. Demand volatility is the standard deviation of annual log employment growth in the industry's
  4-digit codes, 1990–2019 (BDS).
- **Cross-section:** 2015–2019 average utilization, industries with all five years (89):

```math
U_i = \alpha + \beta\,\text{CR4}_i + \eta H_i + \delta\,\text{CR4}_i H_i + \theta_1 \ln S_i + \theta_2 V_i + \varepsilon_i
```

  with HC1 standard errors. Repeated for 2021–2024 and with HHI.
- **Markets:** QPC industries sharing a 4-digit NAICS code are merged into 69 markets that match BDS codes.
  Plant openings in BDS year $`t`$ (the twelve months to March $`t`$) are matched to calendar-year utilization in
  $`t-2`$, Lieberman's construction lag; BDS years 2010–2023. Rates divide by the average of this year's and last
  year's plant counts; job rates use the BDS employment denominator. Demand growth is
  $`g_{m,t-2} = \tfrac{1}{2}(\ln L_{m,t-2} - \ln L_{m,t-4})`$, with $`L`$ employment.
- **Panel:** $`E_{mt} = \beta U_{m,t-2} + \gamma g_{m,t-2} + \mu_m + \lambda_t + \varepsilon_{mt}`$, standard errors
  clustered by market (69), concentrated markets defined as CR4 of 50% or more (17 markets).
- **Extension:** Poisson pseudo-maximum likelihood for counts of openings by new firms (firm age 0) and by existing
  firms, offset by the log plant denominator, market and year effects, clustered by market; stacked with
  builder-specific market and year effects to test $`\beta_{\text{inc}}=\beta_{\text{new}}`$.
- **Long run:** 22 G.17 manufacturing series mapped to BDS 3- and 4-digit codes, BDS years 1982–2023.

## Full test statistics

Cross-section, coefficient on CR4 (points of utilization per point of CR4):

| Specification | 2015–19 | 2021–24 |
|---|---|---|
| CR4 only | 0.124 (0.072), p = 0.09 | |
| With controls | −0.060 (0.077), p = 0.43 | 0.002 (0.090), p = 0.98 |
| With controls, shipment-weighted | −0.024 (0.056), p = 0.67 | |
| Interaction with continuous capital intensity | −0.358 (0.134) and 0.372 (0.123) | |
| HHI per 100 points (86 industries) | 0.065 (0.263), p = 0.81 | |

Panel, new-firm openings per 100 plants on lagged utilization (69 clusters):

| Specification | Coefficient (SE) | p |
|---|---|---|
| Baseline | 0.0143 (0.0130) | 0.27 |
| One-year lag | 0.0111 (0.0099) | 0.26 |
| Weighted by plants | 0.0150 (0.0113) | 0.18 |
| Interaction, CR4 ≥ 50% | −0.0068 (0.0175) | 0.70 |
| Interaction, capital-heavy | −0.0186 (0.0158) | 0.24 |
| 2010–2019 only | 0.0113 (0.0109) | 0.30 |
| Jobs at new firms' plants per 100 jobs | −0.0025 (0.0048) | 0.60 |
| Plant exits per 100 plants | −0.0050 (0.0079) | 0.53 |
| G.17, 1982–2023, new firms (22 clusters) | −0.0539 (0.0409) | 0.19 |
| G.17, 1982–2023, existing firms | 0.0054 (0.0068) | 0.43 |

Extension (Poisson, log points per point of utilization): incumbents' jobs at new plants −0.0157 (0.0041); stacked
jobs difference −0.0152 (0.0050), p = 0.002; 2010–2019 only, new 0.0024 (0.0027), incumbents −0.0101 (0.0036); one-year
lag, new 0.0048 (0.0022), p = 0.03, incumbents −0.0030 (0.0020); triple interaction with CR4 ≥ 50% +0.0079 (0.0063),
p = 0.21; incumbents' share of openings on utilization −0.053 (0.065), extra in concentrated markets −0.248 (0.162);
G.17 stacked difference +0.0046 (0.0071), p = 0.52.

## Reproducing the results

```bash
pip install -r requirements.txt
python src/build_panel.py      # downloads the BDS files (~21 MB) and rebuilds data/derived/
python src/idle_capacity.py    # cross-section, panel, long-run check, first figure
python src/who_builds.py       # incumbents against new firms, second figure
```

## Repository layout

| Path | What it is |
|---|---|
| `src/build_panel.py` | Parses QPC, Economic Census, BDS and G.17 files into `data/derived/` |
| `src/idle_capacity.py` | Industry grouping, cross-section and panel tests |
| `src/who_builds.py` | Lieberman's comparison of incumbents and new firms |
| `results/*.csv`, `results/*.png` | Every number and chart in the README |

## References

- Bulow, J., Geanakoplos, J. & Klemperer, P. (1985). Holding idle capacity to deter entry. *Economic Journal* 95:
  178–182.
- Dixit, A. (1980). The role of investment in entry-deterrence. *Economic Journal* 90(357): 95–106.
- Lieberman, M. B. (1987). Excess capacity as a barrier to entry: an empirical appraisal. *Journal of Industrial
  Economics* 35(4): 607–627.
- Spence, A. M. (1977). Entry, capacity, investment and oligopolistic pricing. *Bell Journal of Economics* 8(2):
  534–544.
