# Spence (1977) and Dixit (1980) on modern data: findings

## In plain English

In 1977 Michael Spence argued that established firms keep rivals out by holding more capacity than they use, a
standing threat to flood the market if anyone builds. In 1980 Avinash Dixit argued that a rational incumbent never
holds idle capacity for that purpose. This repository checks both against Census plant data for 2008 to 2024.

- **The idle capacity is not where Spence put it.** Concentrated, capital-heavy industries such as paperboard,
  pulp and paper mills, petrochemicals, tires and aluminum run their plants harder than other industries (76.5% of
  full capacity on average, against 67.5% to 71.7% elsewhere). The concentrated industries with the most slack are
  light, cyclical ones such as ships and rail cars, farm chemicals, heavy trucks and household appliances.
- **Slack does not keep newcomers out.** Within an industry, years that follow idle capacity bring about as many
  plants opened by brand-new firms as years that follow tight capacity, in concentrated industries as elsewhere.
  Tobacco ran at 57.7% of capacity and still drew new firms at more than twice the rate of the average market (4.39 per 100 plants).
- **Established firms do build after slack years, but everywhere.** Incumbents open about 1% more new plants for
  every point utilization was below normal two years earlier. The effect is not larger in concentrated industries, it
  does not go with fewer entrants, and it vanishes over 1982 to 2023. It looks like replacement and relocation of big
  plants (incumbents' new vehicle plants averaged 91 jobs, newcomers' 17) more than pre-emption.

The essay is in the [README](../README.md); methods and every test statistic are in [TECHNICAL.md](../TECHNICAL.md).

**Key to the labels below.** *Utilization* = Census QPC full-production utilization rate, % (annual mean of
quarters). *CR4* = shipment-weighted average of 2017 six-digit four-firm concentration ratios, %. *Capital per $* =
gross depreciable assets per dollar of shipments, 2017. *Capital-heavy* = above the median, 0.60. *Industry* = one
of 90 consistent QPC industries; *market* = one of 69 groupings that match 4-digit BDS codes. *New-firm openings* =
establishments opened by firms of age 0; *incumbent openings* = establishments opened by firms of age 1 or more.
Openings in BDS year t are paired with utilization in calendar year t − 2 (`util_lag`; `util_lag1` is t − 1).
*util_x_high_cr4* and *util_x_k_high* interact lagged utilization with CR4 ≥ 50% and capital-heavy markets;
*util_x_existing* is the incumbent-minus-new-firm difference in the stacked Poisson; *util_x_existing_x_high* adds
the concentrated-market difference. Coefficients in the panel are openings per 100 plants per point of utilization;
in the Poisson models, log points per point.

## Utilization by concentration and capital intensity, 2015–2019 (`cross_section_bands.csv`)

| CR4 band | Capital intensity | Industries | Mean utilization (%) | Mean CR4 (%) | Mean capital per $ shipments |
|---|---|---|---|---|---|
| under 30% | below median | 9 | 71.68 | 20.68 | 0.38 |
| under 30% | above median | 8 | 68.78 | 21.73 | 0.78 |
| 30-50% | below median | 23 | 68.06 | 37.64 | 0.45 |
| 30-50% | above median | 24 | 70.69 | 38.96 | 1.02 |
| 50% or more | below median | 13 | 67.53 | 62.12 | 0.39 |
| 50% or more | above median | 12 | 76.47 | 62.46 | 1.16 |

## Every regression (`regressions.csv`)

Controls (log plant size, employment volatility, lagged employment growth) are estimated but omitted here; they are in the CSV.

| test | spec | term | coef | se | ci_low | ci_high | p | n | clusters |
|---|---|---|---|---|---|---|---|---|---|
| cross-section 2015-19 | concentration only | cr4 | 0.1244 | 0.0725 | -0.0177 | 0.2664 | 0.0862 | 89 |  |
| cross-section 2015-19 | plus controls | cr4 | -0.0605 | 0.0765 | -0.2105 | 0.0896 | 0.4296 | 89 |  |
| cross-section 2015-19 | plus controls | capital_intensity | 1.8977 | 2.3097 | -2.6292 | 6.4246 | 0.4113 | 89 |  |
| cross-section 2015-19 | Spence interaction | cr4 | -0.2698 | 0.1074 | -0.4803 | -0.0593 | 0.0120 | 89 |  |
| cross-section 2015-19 | Spence interaction | k_high | -14.4291 | 5.5662 | -25.3387 | -3.5196 | 0.0095 | 89 |  |
| cross-section 2015-19 | Spence interaction | cr4_x_k_high | 0.3830 | 0.1213 | 0.1452 | 0.6208 | 0.0016 | 89 |  |
| cross-section 2015-19 | Spence interaction | cr4 slope, capital-heavy | 0.1132 | 0.0812 | -0.0459 | 0.2722 | 0.1632 | 89 |  |
| cross-section 2015-19 | Spence interaction, continuous | cr4 | -0.3581 | 0.1343 | -0.6214 | -0.0949 | 0.0077 | 89 |  |
| cross-section 2015-19 | Spence interaction, continuous | capital_intensity | -16.9010 | 6.5723 | -29.7825 | -4.0195 | 0.0101 | 89 |  |
| cross-section 2015-19 | Spence interaction, continuous | cr4_x_k | 0.3721 | 0.1229 | 0.1313 | 0.6129 | 0.0025 | 89 |  |
| cross-section 2015-19 | HHI instead of CR4 | I(hhi / 100) | 0.0650 | 0.2634 | -0.4512 | 0.5811 | 0.8052 | 86 |  |
| cross-section 2015-19 | HHI instead of CR4 | capital_intensity | 1.2997 | 2.4492 | -3.5007 | 6.1001 | 0.5957 | 86 |  |
| cross-section 2015-19 | plus controls, shipment-weighted | cr4 | -0.0242 | 0.0564 | -0.1347 | 0.0862 | 0.6674 | 89 |  |
| cross-section 2015-19 | plus controls, shipment-weighted | capital_intensity | 2.2286 | 2.5836 | -2.8352 | 7.2924 | 0.3884 | 89 |  |
| cross-section 2021-24 | plus controls | cr4 | 0.0017 | 0.0903 | -0.1753 | 0.1787 | 0.9850 | 90 |  |
| cross-section 2021-24 | plus controls | capital_intensity | 4.9900 | 2.3676 | 0.3496 | 9.6304 | 0.0351 | 90 |  |
| cross-section 2021-24 | Spence interaction | cr4 | -0.2178 | 0.1055 | -0.4245 | -0.0110 | 0.0390 | 90 |  |
| cross-section 2021-24 | Spence interaction | k_high | -15.3940 | 4.8324 | -24.8653 | -5.9227 | 0.0014 | 90 |  |
| cross-section 2021-24 | Spence interaction | cr4_x_k_high | 0.4199 | 0.1151 | 0.1943 | 0.6455 | 0.0003 | 90 |  |
| cross-section 2021-24 | Spence interaction | cr4 slope, capital-heavy | 0.2021 | 0.0782 | 0.0489 | 0.3553 | 0.0097 | 90 |  |
| panel new-firm entry | baseline | util_lag | 0.0143 | 0.0130 | -0.0112 | 0.0398 | 0.2716 | 944 | 69 |
| panel new-firm entry | one-year lag | util_lag1 | 0.0111 | 0.0099 | -0.0083 | 0.0306 | 0.2609 | 943 | 69 |
| panel new-firm entry | plant-weighted | util_lag | 0.0150 | 0.0113 | -0.0070 | 0.0371 | 0.1814 | 944 | 69 |
| panel new-firm entry | by concentration | util_lag | 0.0169 | 0.0140 | -0.0105 | 0.0444 | 0.2273 | 944 | 69 |
| panel new-firm entry | by concentration | util_x_high_cr4 | -0.0068 | 0.0175 | -0.0410 | 0.0275 | 0.6988 | 944 | 69 |
| panel new-firm entry | by capital intensity | util_lag | 0.0227 | 0.0182 | -0.0130 | 0.0584 | 0.2120 | 944 | 69 |
| panel new-firm entry | by capital intensity | util_x_k_high | -0.0186 | 0.0158 | -0.0496 | 0.0124 | 0.2388 | 944 | 69 |
| panel new-firm entry | 2010-2019 only | util_lag | 0.0113 | 0.0109 | -0.0101 | 0.0327 | 0.2993 | 670 | 69 |
| panel new-firm entry | jobs at new firms' plants | util_lag | -0.0025 | 0.0048 | -0.0120 | 0.0069 | 0.5972 | 944 | 69 |
| panel plant exits | baseline | util_lag | -0.0050 | 0.0079 | -0.0204 | 0.0105 | 0.5271 | 944 | 69 |
| G.17 long run new | baseline | util_lag | -0.0539 | 0.0409 | -0.1340 | 0.0263 | 0.1879 | 924 | 22 |
| G.17 long run existing | baseline | util_lag | 0.0054 | 0.0068 | -0.0080 | 0.0188 | 0.4286 | 924 | 22 |
| G.17 long run new_job | baseline | util_lag | -0.0122 | 0.0118 | -0.0353 | 0.0109 | 0.3010 | 924 | 22 |

## Incumbents against new firms (`who_builds_regressions.csv`)

| model | spec | term | coef | se | ci_low | ci_high | p | n |
|---|---|---|---|---|---|---|---|---|
| Poisson, plant openings | new firms' plants | util_lag | 0.0033 | 0.0024 | -0.0013 | 0.0080 | 0.1575 | 944 |
| Poisson, plant openings | existing firms' plants | util_lag | -0.0102 | 0.0025 | -0.0150 | -0.0053 | 0.0000 | 944 |
| Poisson, jobs at new plants | jobs at new firms' plants | util_lag | -0.0005 | 0.0033 | -0.0070 | 0.0060 | 0.8753 | 944 |
| Poisson, jobs at new plants | jobs at existing firms' new plants | util_lag | -0.0157 | 0.0041 | -0.0238 | -0.0076 | 0.0001 | 944 |
| Poisson, plant openings | new firms' plants, 2010-2019 | util_lag | 0.0024 | 0.0027 | -0.0030 | 0.0077 | 0.3848 | 670 |
| Poisson, plant openings | existing firms' plants, 2010-2019 | util_lag | -0.0101 | 0.0036 | -0.0172 | -0.0030 | 0.0055 | 670 |
| Poisson, plant openings | new firms' plants, one-year lag | util_lag1 | 0.0048 | 0.0022 | 0.0005 | 0.0092 | 0.0294 | 943 |
| Poisson, plant openings | existing firms' plants, one-year lag | util_lag1 | -0.0030 | 0.0020 | -0.0070 | 0.0010 | 0.1469 | 943 |
| Poisson, stacked plants | existing minus new | util_lag | 0.0033 | 0.0024 | -0.0013 | 0.0080 | 0.1577 | 1888 |
| Poisson, stacked plants | existing minus new | util_x_existing | -0.0135 | 0.0040 | -0.0213 | -0.0057 | 0.0007 | 1888 |
| Poisson, stacked plants | by concentration | util_lag | 0.0044 | 0.0027 | -0.0010 | 0.0098 | 0.1099 | 1888 |
| Poisson, stacked plants | by concentration | util_x_existing | -0.0148 | 0.0046 | -0.0239 | -0.0058 | 0.0013 | 1888 |
| Poisson, stacked plants | by concentration | util_x_high | -0.0061 | 0.0060 | -0.0179 | 0.0056 | 0.3067 | 1888 |
| Poisson, stacked plants | by concentration | util_x_existing_x_high | 0.0079 | 0.0063 | -0.0044 | 0.0202 | 0.2095 | 1888 |
| Poisson, stacked jobs | existing minus new | util_lag | -0.0005 | 0.0033 | -0.0070 | 0.0060 | 0.8754 | 1888 |
| Poisson, stacked jobs | existing minus new | util_x_existing | -0.0152 | 0.0050 | -0.0250 | -0.0054 | 0.0024 | 1888 |
| OLS, existing firms' share of openings | by concentration | util_lag | -0.0526 | 0.0647 | -0.1793 | 0.0742 | 0.4163 | 944 |
| OLS, existing firms' share of openings | by concentration | util_x_high | -0.2482 | 0.1620 | -0.5658 | 0.0694 | 0.1256 | 944 |
| Poisson, stacked plants, G.17 1982-2023 | existing minus new | util_lag | -0.0038 | 0.0063 | -0.0161 | 0.0085 | 0.5472 | 1848 |
| Poisson, stacked plants, G.17 1982-2023 | existing minus new | util_x_existing | 0.0046 | 0.0071 | -0.0094 | 0.0186 | 0.5183 | 1848 |

## Who builds new plants, 2010–2023 (`who_builds_summary.csv`)

| Group | entry_new | entry_existing | birth_jobs_new | birth_jobs_existing | existing_share_plants | existing_share_jobs | jobs_per_new_firm_plant | jobs_per_existing_firm_plant | markets |
|---|---|---|---|---|---|---|---|---|---|
| all markets | 160077 | 75931 | 1249195 | 1591969 | 32.17 | 56.03 | 7.8 | 20.97 | 69 |
| markets with CR4 >= 50% | 22296 | 6290 | 185605 | 203734 | 22 | 52.33 | 8.32 | 32.39 | 17 |

## Panel averages, 2010–2023 (`panel_summary.csv`)

Unweighted means over market-years; rates are openings or exits per 100 plants, utilization is two years earlier.

| market_years | markets | mean_new_rate | mean_existing_rate | mean_exit_rate | mean_util_lag |
|---|---|---|---|---|---|
| 944 | 69 | 4.389 | 1.674 | 7.303 | 67.932 |

## Figure data: residual openings by decile of residual utilization (`who_builds_binned.csv`)

| bin | util_lag_r | new_rate_r | existing_rate_r |
|---|---|---|---|
| 0 | -12.357 | -0.305 | 0.092 |
| 1 | -6.056 | -0.073 | 0.229 |
| 2 | -3.822 | 0.001 | 0.134 |
| 3 | -1.995 | -0.015 | -0.110 |
| 4 | -0.394 | -0.037 | -0.001 |
| 5 | 0.996 | 0.009 | -0.081 |
| 6 | 2.537 | 0.094 | -0.100 |
| 7 | 3.986 | 0.085 | 0.089 |
| 8 | 5.936 | 0.019 | -0.119 |
| 9 | 11.176 | 0.222 | -0.130 |

## Cross-section correlations (`cross_section_correlations.csv`)

|  | util | cr4 | capital_intensity | ln_plant_size | emp_volatility |
|---|---|---|---|---|---|
| util | 1.000 | 0.199 | 0.198 | 0.411 | -0.240 |
| cr4 | 0.199 | 1.000 | 0.194 | 0.663 | 0.021 |
| capital_intensity | 0.198 | 0.194 | 1.000 | 0.250 | -0.143 |
| ln_plant_size | 0.411 | 0.663 | 0.250 | 1.000 | -0.190 |
| emp_volatility | -0.240 | 0.021 | -0.143 | -0.190 | 1.000 |

## All 89 industries in the cross-section, sorted by utilization (`cross_section_industries.csv`)

| Industry | Utilization 2015-19 (%) | CR4 (%) | HHI | Capital per $ | Shipments per plant ($M) | Employment volatility | Shipments ($bn) |
|---|---|---|---|---|---|---|---|
| Audio and video equipment manufacturing; and manufacturing and reproducing magnetic and optical media | 47.4 | 35.3 | 385 | 0.65 | 5.2 | 7.7 | 4.8 |
| Leather and hide tanning and finishing | 48.9 | 60.0 | 1108 | 0.60 | 8.2 | 9.5 | 1.5 |
| Hosiery and sock mills; and other apparel knitting mills | 49.1 | 38.5 | 517 | 1.08 | 5.3 | 7.8 | 1.2 |
| Ready-mix concrete; concrete pipe, brick, and block; and other concrete manufacturing | 51.9 | 15.7 | 87 | 0.86 | 5.8 | 5.8 | 50.1 |
| Communications equipment manufacturing | 55.0 | 43.8 | 557 | 0.52 | 27.5 | 9.7 | 34.9 |
| Paint, coating, and adhesive manufacturing | 55.7 | 35.5 | 489 | 0.44 | 24.1 | 3.7 | 42.4 |
| Electric lighting equipment manufacturing | 56.0 | 39.6 | 391 | 0.44 | 12.9 | 4.1 | 13.9 |
| Agriculture, construction, and mining machinery manufacturing | 57.4 | 51.1 | 787 | 0.60 | 27.5 | 6.3 | 81.3 |
| Railroad rolling stock, ship, boat, and other transportation equipment manufacturing | 57.4 | 57.8 | 935 | 0.45 | 26.2 | 4.0 | 69.5 |
| Pesticide and other agricultural chemical manufacturing | 57.8 | 58.1 | 930 | 0.55 | 64.1 | 3.5 | 14.6 |
| Cut and sew apparel contractors | 58.0 | 7.8 | 39 | 0.19 | 0.7 | 6.1 | 2.1 |
| Paving, roofing, and all other petroleum and coal products manufacturing | 58.0 | 45.0 | 659 | 0.54 | 22.5 | 1.9 | 44.3 |
| Footwear manufacturing | 60.1 | 42.1 | 577 | 0.40 | 8.1 | 7.8 | 1.8 |
| Nonferrous metal (except aluminum) production and processing | 60.5 | 39.2 | 565 | 0.82 | 56.2 | 4.6 | 46.1 |
| Other textile product mills | 61.0 | 23.0 | 259 | 0.50 | 2.3 | 4.6 | 9.2 |
| All other miscellaneous manufacturing | 61.4 | 31.2 | 353 | 0.56 | 3.4 | 3.6 | 25.2 |
| Bare printed circuit board, electronic capacitor, and other electronic component manufacturing | 61.6 | 32.3 | 323 | 0.49 | 14.0 | 7.2 | 43.5 |
| Coffee and tea manufacturing | 62.6 | 50.5 | 775 | 0.36 | 19.0 | 3.3 | 13.7 |
| Navigational, measuring, electromedical, and control instruments manufacturing | 62.7 | 38.9 | 540 | 0.46 | 29.1 | 3.2 | 151.0 |
| Other chemical product and preparation manufacturing | 63.0 | 30.3 | 409 | 0.69 | 20.2 | 2.9 | 46.9 |
| Textile and fabric finishing, and fabric coating mills | 63.1 | 28.8 | 330 | 0.69 | 8.5 | 7.4 | 7.1 |
| Fabric mills | 63.2 | 32.3 | 387 | 0.95 | 15.9 | 6.3 | 13.4 |
| Cement manufacturing | 63.9 | 40.1 | 661 | 2.90 | 43.3 | 5.8 | 8.3 |
| Engine, turbine, and power transmission equipment manufacturing | 64.2 | 55.5 | 917 | 0.62 | 47.9 | 5.2 | 45.6 |
| Sugar and confectionary product, fruit and vegetable preserving and specialty food manufacturing | 64.8 | 42.5 | 638 | 0.61 | 28.4 | 1.5 | 109.2 |
| Computer and peripheral equipment manufacturing | 64.9 | 57.2 | 783 | 0.61 | 21.5 | 10.0 | 20.3 |
| Soap, cleaning compound, and toilet preparation manufacturing | 64.9 | 54.4 | 1381 | 0.49 | 36.6 | 3.2 | 82.5 |
| Heavy duty truck manufacturing | 65.1 | 71.5 | 1528 | 0.17 | 312.8 | 8.0 | 25.7 |
| Industrial gas, synthetic organic dye and pigment, and other basic inorganic chemical manufacturing | 65.4 | 37.8 | 590 | 1.62 | 36.9 | 2.9 | 47.7 |
| All other fabricated metal product manufacturing | 65.8 | 17.9 | 168 | 0.62 | 5.3 | 4.5 | 252.1 |
| Electrical equipment and component manufacturing | 65.9 | 40.1 | 637 | 0.49 | 21.0 | 4.7 | 86.4 |
| Automobile manufacturing | 65.9 | 57.5 | 1159 | 0.46 | 584.5 | 8.0 | 99.4 |
| Household appliance manufacturing | 66.4 | 68.1 | 1014 | 0.47 | 74.5 | 6.0 | 22.7 |
| Other general purpose machinery manufacturing | 67.5 | 33.3 | 420 | 0.41 | 17.2 | 4.7 | 103.9 |
| Pharmaceutical and medicine manufacturing | 67.8 | 43.0 | 644 | 0.69 | 88.6 | 3.1 | 211.2 |
| Industrial machinery manufacturing | 68.1 | 25.5 | 359 | 0.52 | 10.6 | 5.7 | 33.5 |
| Forging and stamping; cutlery, handtool, boiler, tank, shipping container, hardware, and spring and wire manufacturing | 68.2 | 35.6 | 528 | 0.64 | 13.4 | 4.1 | 91.1 |
| Clay product and refractory manufacturing | 68.5 | 32.8 | 403 | 1.19 | 7.2 | 6.2 | 8.1 |
| Ventilation, heating, air-conditioning, and commercial refrigeration equipment manufacturing | 68.6 | 32.1 | 370 | 0.38 | 25.1 | 4.6 | 43.2 |
| Lime and gypsum product manufacturing | 68.6 | 75.7 | 1581 | 1.38 | 27.7 | 6.3 | 8.0 |
| Other cut and sew apparel manufacturing | 68.7 | 40.7 | 486 | 0.25 | 2.4 | 6.1 | 1.1 |
| Animal food, bakery and tortilla manufacturing, seafood product preparation and packaging | 68.8 | 37.9 | 611 | 0.49 | 10.1 | 1.7 | 138.2 |
| Apparel accessories and other apparel manufacturing | 70.0 | 28.0 | 344 | 0.36 | 1.8 | 9.3 | 1.1 |
| All other rubber product (excluding tires) manufacturing | 70.0 | 31.4 | 386 | 0.60 | 17.3 | 4.2 | 23.5 |
| Textile furnishings mills | 70.4 | 45.1 | 818 | 0.49 | 8.2 | 5.1 | 13.6 |
| Synthetic rubber manufacturing | 70.9 | 31.3 | 433 | 0.83 | 53.7 | 4.9 | 8.3 |
| Metalworking machinery manufacturing | 70.9 | 17.8 | 147 | 0.70 | 5.1 | 5.1 | 32.3 |
| Foundries | 71.0 | 40.0 | 485 | 0.98 | 17.7 | 6.0 | 30.0 |
| Jewelry, silverware, sporting and athletic goods, and doll, toy and game manufacturing | 71.1 | 31.8 | 394 | 0.38 | 4.6 | 3.6 | 18.9 |
| Office furniture (incl. fixtures) manufacturing | 71.4 | 28.9 | 444 | 0.46 | 7.2 | 6.4 | 26.0 |
| Other furniture related product manufacturing | 71.6 | 59.4 | 1102 | 0.26 | 13.8 | 5.3 | 10.2 |
| Other food manufacturing | 71.9 | 30.5 | 328 | 0.41 | 25.4 | 3.3 | 62.5 |
| Medical equipment and supplies manufacturing | 72.3 | 32.8 | 402 | 0.48 | 8.8 | 2.4 | 88.6 |
| Other wood product manufacturing | 72.8 | 30.2 | 312 | 0.46 | 5.0 | 6.5 | 50.0 |
| Office supplies (except paper) and sign manufacturing | 73.1 | 15.4 | 147 | 0.38 | 2.5 | 3.6 | 15.7 |
| Household and institutional furniture and kitchen cabinet manufacturing | 73.2 | 32.9 | 286 | 0.37 | 3.9 | 5.9 | 38.9 |
| Plastics product manufacturing | 73.2 | 21.2 | 204 | 0.68 | 18.6 | 4.5 | 193.3 |
| Fertilizer manufacturing | 73.2 | 60.8 | n/a | 1.81 | 22.4 | 3.5 | 16.8 |
| Iron and steel mills and ferroalloy manufacturing; and steel product manufacturing from purchased steel | 73.5 | 45.0 | 720 | 0.89 | 114.8 | 4.6 | 110.3 |
| Aerospace product and parts manufacturing | 73.7 | 82.5 | 2231 | 0.42 | 140.9 | 5.2 | 249.8 |
| Plastics material and resin manufacturing | 74.0 | 29.4 | 368 | 1.14 | 78.5 | 4.9 | 88.4 |
| Snack food manufacturing | 74.5 | 57.8 | 410 | 0.36 | 58.1 | 3.3 | 38.8 |
| Printing and related support activities | 74.5 | 16.9 | 121 | 0.80 | 3.3 | 3.2 | 82.8 |
| Other leather and allied product manufacturing | 75.6 | 33.0 | 632 | 0.31 | 2.0 | 6.1 | 1.5 |
| Alumina and aluminum production and processing | 75.6 | 55.2 | 1243 | 0.68 | 78.7 | 5.5 | 35.7 |
| Other nonmetallic mineral product manufacturing | 76.0 | 46.3 | 603 | 0.89 | 7.9 | 5.1 | 25.5 |
| Men's and boy's cut and sew apparel manufacturing | 76.1 | 21.1 | 225 | 0.38 | 3.4 | 6.1 | 1.5 |
| Beverage manufacturing | 76.6 | 56.6 | 1152 | 0.74 | 11.9 | 4.4 | 107.5 |
| Commercial and service industry machinery manufacturing | 76.8 | 22.1 | 175 | 0.47 | 12.8 | 4.7 | 24.7 |
| Sawmills and wood preservation | 77.0 | 26.1 | 268 | 0.70 | 9.9 | 6.0 | 32.7 |
| Motor vehicle body and trailer manufacturing | 77.8 | 51.6 | 656 | 0.17 | 24.3 | 10.6 | 47.7 |
| Motor vehicle parts manufacturing | 77.9 | 31.3 | 414 | 0.63 | 52.4 | 7.3 | 261.3 |
| Veneer, plywood, and engineered wood product manufacturing | 78.8 | 45.2 | 698 | 0.72 | 17.1 | 8.1 | 24.5 |
| Glass and glass product manufacturing | 79.3 | 49.1 | 980 | 1.01 | 15.3 | 4.2 | 25.9 |
| Converted paper product manufacturing | 79.6 | 43.0 | 669 | 0.56 | 29.6 | 2.8 | 108.9 |
| Artificial and synthetic fibers and filaments manufacturing | 79.6 | 45.0 | 764 | 1.21 | 51.8 | 4.9 | 6.8 |
| Semiconductor and related device manufacturing | 81.3 | 43.7 | n/a | 1.95 | 63.5 | 7.2 | 51.8 |
| Fiber, yarn, and thread mills | 81.4 | 46.1 | 803 | 0.93 | 24.3 | 5.5 | 7.1 |
| Paper mills | 81.5 | 57.8 | 1048 | 1.62 | 215.0 | 2.8 | 37.8 |
| Grain and oilseed milling, dairy, and animal slaughtering and processing | 81.6 | 49.0 | 793 | 0.38 | 68.3 | 1.5 | 413.4 |
| Gum, wood chemical, cyclic crude and intermediate, and all other basic organic chemical manufacturing | 82.7 | 33.8 | 343 | 1.18 | 91.8 | 2.9 | 84.3 |
| Tire manufacturing | 85.2 | 66.5 | 1323 | 1.00 | 40.0 | 4.2 | 19.8 |
| Petroleum refineries | 87.1 | 44.9 | 708 | 0.56 | 3372.6 | 1.9 | 499.1 |
| Pulp mills | 88.0 | 74.9 | 1711 | 2.46 | 196.1 | 2.8 | 6.9 |
| Petrochemical manufacturing | 89.3 | 74.4 | n/a | 0.70 | 1261.3 | 2.9 | 54.2 |
| Women's and girl's cut and sew apparel manufacturing | 90.5 | 14.4 | 98 | 0.20 | 3.0 | 6.1 | 3.3 |
| Light truck and utility vehicle manufacturing | 91.3 | 78.5 | 2023 | 0.27 | 3252.9 | 8.0 | 198.4 |
| Ethyl alcohol manufacturing | 92.3 | 39.4 | 512 | 0.81 | 153.4 | 2.9 | 31.8 |
| Paperboard mills | 93.1 | 63.8 | 1299 | 1.65 | 209.8 | 2.8 | 32.7 |

## All 69 markets in the panel, sorted by utilization (`market_summary.csv`)

| Market | CR4 (%) | Capital per $ | Mean utilization 2008-21 (%) | New-firm openings per 100 plants | Incumbent openings per 100 plants | Exits per 100 plants | Plants 2023 |
|---|---|---|---|---|---|---|---|
| Railroad rolling stock, ship, boat, and other transportation equipment manufacturing | 57.77 | 0.45 | 52.77 | 5.76 | 2.03 | 8.90 | 2354 |
| Hosiery and sock mills; and other apparel knitting mills | 38.46 | 1.08 | 54.10 | 4.67 | 0.17 | 8.75 | 194 |
| Audio and video equipment manufacturing; and manufacturing and reproducing magnetic and optical media | 35.27 | 0.65 | 54.71 | 6.33 | 1.19 | 10.59 | 765 |
| Cement manufacturing; Ready-mix concrete; concrete pipe, brick, and block; and other concrete manufacturing | 19.18 | 1.15 | 56.12 | 1.48 | 3.86 | 4.52 | 8854 |
| Electric lighting equipment manufacturing | 39.56 | 0.44 | 57.45 | 4.78 | 1.31 | 8.29 | 943 |
| Tobacco manufacturing | 91.10 | 0.21 | 57.66 | 10.51 | 0.00 | 10.38 | 120 |
| Clay product and refractory manufacturing | 32.82 | 1.19 | 59.46 | 3.95 | 2.02 | 8.16 | 947 |
| Nonferrous metal (except aluminum) production and processing | 39.23 | 0.82 | 60.40 | 2.66 | 0.62 | 5.12 | 678 |
| Textile and fabric finishing, and fabric coating mills | 28.77 | 0.70 | 61.28 | 5.18 | 1.02 | 8.73 | 692 |
| Paint, coating, and adhesive manufacturing | 35.53 | 0.44 | 62.24 | 2.87 | 1.37 | 5.58 | 1570 |
| Lime and gypsum product manufacturing | 75.69 | 1.38 | 63.37 | 2.15 | 1.15 | 5.92 | 262 |
| Communications equipment manufacturing | 43.83 | 0.52 | 63.80 | 3.88 | 1.81 | 8.03 | 1058 |
| Soap, cleaning compound, and toilet preparation manufacturing | 54.39 | 0.49 | 63.84 | 5.52 | 1.83 | 7.22 | 2311 |
| Textile furnishings mills | 45.06 | 0.49 | 63.88 | 2.98 | 2.21 | 9.26 | 1226 |
| Household appliance manufacturing | 68.09 | 0.48 | 63.96 | 7.00 | 0.54 | 8.09 | 324 |
| Agriculture, construction, and mining machinery manufacturing | 51.07 | 0.60 | 63.97 | 3.37 | 1.88 | 6.02 | 2677 |
| Computer and peripheral equipment manufacturing | 57.21 | 0.61 | 64.02 | 5.34 | 1.64 | 9.52 | 538 |
| Ventilation, heating, air-conditioning, and commercial refrigeration equipment manufacturing | 32.11 | 0.38 | 64.49 | 3.04 | 1.39 | 5.86 | 1597 |
| Leather and hide tanning and finishing | 60.00 | 0.60 | 64.63 | 5.31 | 0.14 | 8.29 | 149 |
| Industrial machinery manufacturing | 25.50 | 0.52 | 64.84 | 3.32 | 1.71 | 6.12 | 2751 |
| Other leather and allied product manufacturing | 33.03 | 0.31 | 64.97 | 6.92 | 1.08 | 10.21 | 666 |
| Other chemical product and preparation manufacturing | 30.28 | 0.69 | 65.57 | 4.12 | 1.97 | 7.33 | 2126 |
| Footwear manufacturing | 42.10 | 0.40 | 65.90 | 7.68 | 0.68 | 10.84 | 199 |
| Printing and related support activities | 16.88 | 0.80 | 66.10 | 3.77 | 2.01 | 8.56 | 20962 |
| Other textile product mills | 22.95 | 0.50 | 66.14 | 5.58 | 2.53 | 9.21 | 3507 |
| Sugar and confectionary product, fruit and vegetable preserving and specialty food manufacturing | 42.53 | 0.61 | 66.15 | 5.71 | 1.87 | 7.14 | 3626 |
| Other wood product manufacturing | 30.24 | 0.46 | 66.23 | 5.02 | 2.63 | 8.07 | 8828 |
| All other fabricated metal product manufacturing | 17.93 | 0.62 | 66.39 | 3.34 | 1.89 | 6.28 | 45243 |
| Engine, turbine, and power transmission equipment manufacturing | 55.49 | 0.62 | 66.47 | 2.19 | 1.13 | 5.69 | 873 |
| Office furniture (incl. fixtures) manufacturing | 28.92 | 0.46 | 66.51 | 3.48 | 1.97 | 7.72 | 3455 |
| Forging and stamping; cutlery, handtool, boiler, tank, shipping container, hardware, and spring and wire manufacturing | 35.61 | 0.64 | 66.81 | 2.25 | 1.16 | 5.26 | 5748 |
| Navigational, measuring, electromedical, and control instruments manufacturing | 38.91 | 0.46 | 66.83 | 3.33 | 2.28 | 6.56 | 4690 |
| Fertilizer manufacturing; Pesticide and other agricultural chemical manufacturing | 59.52 | 1.22 | 66.87 | 4.41 | 1.72 | 6.22 | 977 |
| Metalworking machinery manufacturing | 17.85 | 0.70 | 67.08 | 2.10 | 1.56 | 5.69 | 5555 |
| Fabric mills | 32.26 | 0.95 | 67.25 | 3.45 | 0.93 | 7.44 | 709 |
| Other general purpose machinery manufacturing | 33.26 | 0.41 | 67.25 | 2.79 | 1.92 | 5.24 | 5648 |
| Sawmills and wood preservation | 26.11 | 0.70 | 67.53 | 3.93 | 2.35 | 7.52 | 2918 |
| Veneer, plywood, and engineered wood product manufacturing | 45.19 | 0.72 | 67.66 | 2.41 | 1.88 | 6.35 | 1414 |
| Electrical equipment and component manufacturing | 40.08 | 0.49 | 67.71 | 3.23 | 1.73 | 6.02 | 3812 |
| Motor vehicle body and trailer manufacturing | 51.58 | 0.17 | 67.73 | 4.30 | 2.26 | 6.55 | 2066 |
| All other miscellaneous manufacturing; Jewelry, silverware, sporting and athletic goods, and doll, toy and game manufacturing; Office supplies (except paper) and sign manufacturing | 27.25 | 0.45 | 68.25 | 7.00 | 2.49 | 9.01 | 13702 |
| Bare printed circuit board, electronic capacitor, and other electronic component manufacturing; Semiconductor and related device manufacturing | 38.49 | 1.29 | 68.62 | 3.36 | 1.63 | 6.57 | 3486 |
| Household and institutional furniture and kitchen cabinet manufacturing | 32.89 | 0.37 | 68.77 | 4.20 | 2.97 | 9.53 | 9235 |
| Plastics product manufacturing | 21.23 | 0.68 | 68.86 | 2.19 | 1.77 | 5.21 | 9256 |
| Motor vehicle parts manufacturing | 31.32 | 0.63 | 68.95 | 2.88 | 1.96 | 5.85 | 4394 |
| Pharmaceutical and medicine manufacturing | 42.99 | 0.69 | 69.09 | 6.69 | 2.56 | 7.06 | 2745 |
| Other nonmetallic mineral product manufacturing | 46.33 | 0.89 | 69.19 | 3.64 | 2.31 | 6.97 | 3165 |
| Foundries | 39.99 | 0.98 | 69.23 | 1.84 | 0.94 | 5.13 | 1297 |
| Animal food, bakery and tortilla manufacturing, seafood product preparation and packaging | 37.93 | 0.49 | 69.46 | 7.59 | 1.97 | 8.29 | 14330 |
| Coffee and tea manufacturing; Other food manufacturing; Snack food manufacturing | 43.39 | 0.39 | 70.17 | 8.38 | 2.24 | 7.45 | 4547 |
| Apparel accessories and other apparel manufacturing | 28.00 | 0.36 | 70.50 | 10.01 | 1.44 | 12.33 | 643 |
| Iron and steel mills and ferroalloy manufacturing; and steel product manufacturing from purchased steel | 45.03 | 0.89 | 71.56 | 4.13 | 0.99 | 5.83 | 1004 |
| Other furniture related product manufacturing | 59.37 | 0.26 | 71.96 | 3.70 | 1.03 | 7.96 | 676 |
| Aerospace product and parts manufacturing | 82.46 | 0.42 | 72.54 | 3.66 | 2.70 | 6.84 | 1784 |
| Medical equipment and supplies manufacturing | 32.78 | 0.48 | 73.13 | 4.02 | 2.22 | 8.36 | 8281 |
| Artificial and synthetic fibers and filaments manufacturing; Plastics material and resin manufacturing; Synthetic rubber manufacturing | 30.57 | 1.12 | 73.27 | 2.37 | 1.41 | 4.48 | 1508 |
| Cut and sew apparel contractors; Men's and boy's cut and sew apparel manufacturing; Other cut and sew apparel manufacturing; Women's and girl's cut and sew apparel manufacturing | 17.47 | 0.24 | 73.76 | 10.66 | 3.01 | 17.60 | 3395 |
| Alumina and aluminum production and processing | 55.23 | 0.68 | 74.36 | 2.76 | 0.40 | 5.44 | 412 |
| Beverage manufacturing | 56.62 | 0.74 | 74.72 | 12.45 | 2.05 | 6.33 | 11596 |
| Automobile manufacturing; Heavy duty truck manufacturing; Light truck and utility vehicle manufacturing | 71.49 | 0.32 | 75.10 | 6.50 | 1.17 | 8.46 | 324 |
| All other rubber product (excluding tires) manufacturing; Tire manufacturing | 47.46 | 0.78 | 75.29 | 2.07 | 1.63 | 5.10 | 1725 |
| Commercial and service industry machinery manufacturing | 22.08 | 0.47 | 75.35 | 3.64 | 1.97 | 7.17 | 1640 |
| Converted paper product manufacturing | 43.03 | 0.56 | 75.42 | 1.65 | 1.55 | 4.97 | 3297 |
| Fiber, yarn, and thread mills | 46.10 | 0.93 | 79.00 | 5.09 | 0.67 | 8.91 | 245 |
| Glass and glass product manufacturing | 49.05 | 1.01 | 79.27 | 3.96 | 2.19 | 8.11 | 1426 |
| Ethyl alcohol manufacturing; Gum, wood chemical, cyclic crude and intermediate, and all other basic organic chemical manufacturing; Industrial gas, synthetic organic dye and pigment, and other basic inorganic chemical manufacturing; Petrochemical manufacturing | 45.59 | 1.10 | 80.61 | 2.07 | 4.01 | 5.90 | 2528 |
| Grain and oilseed milling, dairy, and animal slaughtering and processing | 48.99 | 0.38 | 82.59 | 4.22 | 1.45 | 5.55 | 6160 |
| Paving, roofing, and all other petroleum and coal products manufacturing; Petroleum refineries | 44.90 | 0.56 | 83.57 | 1.68 | 3.34 | 5.52 | 2049 |
| Paper mills; Paperboard mills; Pulp mills | 61.84 | 1.70 | 87.33 | 1.89 | 0.55 | 4.42 | 387 |

## Who builds, by market (`who_builds_markets.csv`)

| Market | CR4 (%) | New-firm plants | Incumbent plants | Incumbent share of plants (%) | Incumbent share of new-plant jobs (%) | Jobs per new-firm plant | Jobs per incumbent plant |
|---|---|---|---|---|---|---|---|
| Cement manufacturing; Ready-mix concrete; concrete pipe, brick, and block; and other concrete manufacturing | 19.2 | 1007 | 2636 | 72.4 | 77.3 | 10.5 | 13.6 |
| Converted paper product manufacturing | 43.0 | 845 | 788 | 48.2 | 73.7 | 15.3 | 45.9 |
| Engine, turbine, and power transmission equipment manufacturing | 55.5 | 295 | 151 | 33.9 | 73.6 | 16.6 | 90.5 |
| All other rubber product (excluding tires) manufacturing; Tire manufacturing | 47.5 | 527 | 413 | 43.9 | 71.6 | 11.1 | 35.8 |
| Aerospace product and parts manufacturing | 82.5 | 878 | 652 | 42.6 | 71.3 | 17.9 | 59.9 |
| Ethyl alcohol manufacturing; Gum, wood chemical, cyclic crude and intermediate, and all other basic organic chemical manufacturing; Industrial gas, synthetic organic dye and pigment, and other basic inorganic chemical manufacturing; Petrochemical manufacturing | 45.6 | 352 | 691 | 66.2 | 71.3 | 20.3 | 25.7 |
| Lime and gypsum product manufacturing | 75.7 | 88 | 47 | 34.8 | 70.8 | 4.6 | 20.8 |
| Paving, roofing, and all other petroleum and coal products manufacturing; Petroleum refineries | 44.9 | 491 | 975 | 66.5 | 70.5 | 11.1 | 13.3 |
| Paint, coating, and adhesive manufacturing | 35.5 | 656 | 312 | 32.2 | 69.4 | 8.4 | 40.2 |
| Pharmaceutical and medicine manufacturing | 43.0 | 2128 | 818 | 27.8 | 68.0 | 13.6 | 75.1 |
| Veneer, plywood, and engineered wood product manufacturing | 45.2 | 471 | 368 | 43.9 | 67.6 | 14.3 | 38.2 |
| Navigational, measuring, electromedical, and control instruments manufacturing | 38.9 | 2295 | 1571 | 40.6 | 67.5 | 11.4 | 34.7 |
| Motor vehicle parts manufacturing | 31.3 | 1914 | 1307 | 40.6 | 66.8 | 19.2 | 56.5 |
| Plastics product manufacturing | 21.2 | 3087 | 2480 | 44.5 | 66.3 | 14.1 | 34.5 |
| Electrical equipment and component manufacturing | 40.1 | 1806 | 963 | 34.8 | 64.5 | 10.0 | 34.1 |
| Medical equipment and supplies manufacturing | 32.8 | 5498 | 2997 | 35.3 | 64.4 | 5.6 | 18.6 |
| Ventilation, heating, air-conditioning, and commercial refrigeration equipment manufacturing | 32.1 | 709 | 323 | 31.3 | 64.4 | 14.6 | 57.8 |
| Other general purpose machinery manufacturing | 33.3 | 2244 | 1544 | 40.8 | 63.2 | 9.8 | 24.5 |
| Artificial and synthetic fibers and filaments manufacturing; Plastics material and resin manufacturing; Synthetic rubber manufacturing | 30.6 | 458 | 274 | 37.4 | 62.8 | 17.4 | 49.1 |
| Agriculture, construction, and mining machinery manufacturing | 51.1 | 1327 | 735 | 35.6 | 62.1 | 10.8 | 32.0 |
| Forging and stamping; cutlery, handtool, boiler, tank, shipping container, hardware, and spring and wire manufacturing | 35.6 | 2061 | 1063 | 34.0 | 61.6 | 10.5 | 32.7 |
| Commercial and service industry machinery manufacturing | 22.1 | 933 | 497 | 34.8 | 61.2 | 8.5 | 25.1 |
| Motor vehicle body and trailer manufacturing | 51.6 | 1124 | 590 | 34.4 | 60.8 | 15.5 | 45.6 |
| Computer and peripheral equipment manufacturing | 57.2 | 675 | 202 | 23.0 | 60.0 | 7.2 | 35.9 |
| Bare printed circuit board, electronic capacitor, and other electronic component manufacturing; Semiconductor and related device manufacturing | 38.5 | 1784 | 860 | 32.5 | 58.2 | 12.3 | 35.4 |
| Soap, cleaning compound, and toilet preparation manufacturing | 54.4 | 1663 | 556 | 25.1 | 57.9 | 7.3 | 30.0 |
| Other nonmetallic mineral product manufacturing | 46.3 | 1550 | 986 | 38.9 | 57.4 | 6.7 | 14.3 |
| Printing and related support activities | 16.9 | 12710 | 6702 | 34.5 | 57.0 | 4.8 | 11.9 |
| Textile furnishings mills | 45.1 | 677 | 505 | 42.7 | 57.0 | 8.1 | 14.3 |
| Grain and oilseed milling, dairy, and animal slaughtering and processing | 49.0 | 3424 | 1174 | 25.5 | 56.7 | 11.9 | 45.5 |
| Other wood product manufacturing | 30.2 | 6186 | 3231 | 34.3 | 56.0 | 6.7 | 16.5 |
| Metalworking machinery manufacturing | 17.9 | 1835 | 1359 | 42.5 | 55.9 | 8.7 | 14.9 |
| Clay product and refractory manufacturing | 32.8 | 579 | 301 | 34.2 | 55.6 | 5.5 | 13.4 |
| Fertilizer manufacturing; Pesticide and other agricultural chemical manufacturing | 59.5 | 560 | 219 | 28.1 | 54.6 | 5.7 | 17.6 |
| Other chemical product and preparation manufacturing | 30.3 | 1268 | 606 | 32.3 | 54.5 | 8.8 | 22.1 |
| Sugar and confectionary product, fruit and vegetable preserving and specialty food manufacturing | 42.5 | 2782 | 916 | 24.8 | 54.4 | 8.5 | 31.0 |
| Glass and glass product manufacturing | 49.0 | 887 | 488 | 35.5 | 54.4 | 8.4 | 18.2 |
| All other fabricated metal product manufacturing | 17.9 | 21313 | 12089 | 36.2 | 53.5 | 7.1 | 14.3 |
| Coffee and tea manufacturing; Other food manufacturing; Snack food manufacturing | 43.4 | 4187 | 1135 | 21.3 | 53.5 | 7.9 | 33.4 |
| Communications equipment manufacturing | 43.8 | 683 | 315 | 31.6 | 52.3 | 12.9 | 30.8 |
| Railroad rolling stock, ship, boat, and other transportation equipment manufacturing | 57.8 | 1936 | 679 | 26.0 | 52.2 | 10.0 | 31.3 |
| Foundries | 40.0 | 427 | 213 | 33.3 | 51.9 | 17.7 | 38.3 |
| Sawmills and wood preservation | 26.1 | 1673 | 1007 | 37.6 | 50.7 | 8.9 | 15.3 |
| Household and institutional furniture and kitchen cabinet manufacturing | 32.9 | 5904 | 4245 | 41.8 | 49.7 | 5.5 | 7.5 |
| Automobile manufacturing; Heavy duty truck manufacturing; Light truck and utility vehicle manufacturing | 71.5 | 288 | 52 | 15.3 | 49.0 | 17.2 | 91.4 |
| Industrial machinery manufacturing | 25.5 | 1406 | 723 | 34.0 | 49.0 | 9.1 | 16.9 |
| Iron and steel mills and ferroalloy manufacturing; and steel product manufacturing from purchased steel | 45.0 | 613 | 146 | 19.2 | 47.5 | 14.4 | 54.7 |
| Office furniture (incl. fixtures) manufacturing | 28.9 | 1707 | 969 | 36.2 | 46.8 | 7.5 | 11.6 |
| Paper mills; Paperboard mills; Pulp mills | 61.8 | 111 | 33 | 22.9 | 46.4 | 31.7 | 92.3 |
| Household appliance manufacturing | 68.1 | 280 | 24 | 7.9 | 45.1 | 8.9 | 85.2 |
| Electric lighting equipment manufacturing | 39.6 | 681 | 184 | 21.3 | 42.4 | 6.8 | 18.4 |
| Fabric mills | 32.3 | 411 | 110 | 21.1 | 42.2 | 10.6 | 29.0 |
| Other leather and allied product manufacturing | 33.0 | 655 | 101 | 13.4 | 40.6 | 4.3 | 19.1 |
| Other textile product mills | 22.9 | 2977 | 1340 | 31.0 | 40.5 | 4.4 | 6.7 |
| Animal food, bakery and tortilla manufacturing, seafood product preparation and packaging | 37.9 | 13552 | 3518 | 20.6 | 40.0 | 7.3 | 18.8 |
| All other miscellaneous manufacturing; Jewelry, silverware, sporting and athletic goods, and doll, toy and game manufacturing; Office supplies (except paper) and sign manufacturing | 27.2 | 14452 | 5091 | 26.1 | 40.0 | 4.7 | 8.9 |
| Fiber, yarn, and thread mills | 46.1 | 199 | 26 | 11.6 | 35.6 | 12.6 | 53.3 |
| Nonferrous metal (except aluminum) production and processing | 39.2 | 327 | 73 | 18.2 | 35.3 | 13.6 | 33.2 |
| Beverage manufacturing | 56.6 | 12218 | 2214 | 15.3 | 34.7 | 5.6 | 16.3 |
| Alumina and aluminum production and processing | 55.2 | 187 | 28 | 13.0 | 26.8 | 28.9 | 70.5 |
| Audio and video equipment manufacturing; and manufacturing and reproducing magnetic and optical media | 35.3 | 760 | 146 | 16.1 | 26.5 | 4.8 | 9.1 |
| Other furniture related product manufacturing | 59.4 | 380 | 105 | 21.6 | 26.0 | 19.8 | 25.1 |
| Textile and fabric finishing, and fabric coating mills | 28.8 | 633 | 124 | 16.4 | 25.7 | 6.9 | 12.2 |
| Cut and sew apparel contractors; Men's and boy's cut and sew apparel manufacturing; Other cut and sew apparel manufacturing; Women's and girl's cut and sew apparel manufacturing | 17.5 | 2939 | 802 | 21.4 | 22.8 | 6.1 | 6.6 |
| Footwear manufacturing | 42.1 | 217 | 19 | 8.1 | 18.6 | 8.1 | 20.9 |
| Apparel accessories and other apparel manufacturing | 28.0 | 753 | 110 | 12.8 | 12.9 | 4.6 | 4.7 |
| Hosiery and sock mills; and other apparel knitting mills | 38.5 | 148 | 7 | 4.5 | 6.9 | 10.1 | 15.9 |
| Leather and hide tanning and finishing | 60.0 | 125 | 3 | 2.3 | 1.8 | 4.0 | 3.0 |
| Tobacco manufacturing | 91.1 | 161 | 0 | 0.0 | 0.0 | 6.5 | n/a |

Figures: [utilization_vs_concentration.png](utilization_vs_concentration.png), [openings_vs_utilization.png](openings_vs_utilization.png). The full panels are in `panel_markets.csv`, `g17_panel.csv` and `utilization_by_industry_year.csv`.
