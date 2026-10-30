# Experiment diagnostics - SRM_AND_SBI_DIMER_ALP_2S_50FPS
Run: 2026-08-20 11:37:27 UTC

## Checks - 1 passed, 0 failed

| check | result | detail |
|---|---|---|
| estimates_nonempty | PASS | 500 MAP estimates over real videos |

## Quantitative

| metric | value | expected | meaning |
|---|---|---|---|
| conditions | 2 | - | - |
| total_estimates | 500 | - | number of (cell, chunk) windows MAP-estimated across all conditions. |
| aggregation | pooled | - | report distribution view: pooled over (cell x chunk). |
| n[MET-FAB] | 250 | - | estimates for condition MET-FAB (stored as 'ALP'). |
| n[MET-INLB] | 250 | - | estimates for condition MET-INLB (stored as 'BET'). |
| mean_log_prob | 11.2 | - | mean MAP log-density at the optimized mode (optimization diagnostic; not a calibration/quality metric). |
| posterior_samples | 1000 | - | samples per chunk used to summarize the posterior (View B). |

## Inferred theta by condition (log10 units)

| parameter | label | kind | n | median log10 | IQR log10 | median value |
|---|---|---|---|---|---|---|
| count_alp | $C_{A}$ | MET-FAB | 250 | +2.262 | 0.670 | 182.9 |
| count_alp | $C_{A}$ | MET-INLB | 250 | +1.878 | 1.400 | 75.54 |
| count_bet | $C_{B}$ | MET-FAB | 250 | +1.318 | 0.511 | 20.78 |
| count_bet | $C_{B}$ | MET-INLB | 250 | +1.663 | 1.030 | 46.04 |
| count_chi | $C_{C}$ | MET-FAB | 250 | +1.678 | 0.599 | 47.59 |
| count_chi | $C_{C}$ | MET-INLB | 250 | +2.458 | 0.322 | 287.1 |
| diffusivity_alp | $D_{A}$ | MET-FAB | 250 | -0.867 | 0.073 | 0.1358 |
| diffusivity_alp | $D_{A}$ | MET-INLB | 250 | -0.902 | 0.262 | 0.1252 |
| relative_diffusivity_bet | $R_{B}$ | MET-FAB | 250 | -0.346 | 0.249 | 0.4509 |
| relative_diffusivity_bet | $R_{B}$ | MET-INLB | 250 | -0.179 | 0.331 | 0.6629 |
| relative_diffusivity_chi | $R_{C}$ | MET-FAB | 250 | -1.782 | 0.311 | 0.01654 |
| relative_diffusivity_chi | $R_{C}$ | MET-INLB | 250 | -2.217 | 0.386 | 0.006061 |
| relative_rate_dimerization | $R_{ON}$ | MET-FAB | 250 | -1.035 | 0.048 | 0.0923 |
| relative_rate_dimerization | $R_{ON}$ | MET-INLB | 250 | -1.046 | 0.080 | 0.0899 |
| rate_dissociation | $\kappa_{OFF}$ | MET-FAB | 250 | +0.477 | 0.773 | 2.996 |
| rate_dissociation | $\kappa_{OFF}$ | MET-INLB | 250 | +0.270 | 0.778 | 1.861 |
| rate_immobility | $\kappa_{IMMOBILITY}$ | MET-FAB | 250 | +0.736 | 0.441 | 5.445 |
| rate_immobility | $\kappa_{IMMOBILITY}$ | MET-INLB | 250 | +0.538 | 0.614 | 3.454 |
| rate_mobility | $\kappa_{MOBILITY}$ | MET-FAB | 250 | -0.738 | 0.653 | 0.1828 |
| rate_mobility | $\kappa_{MOBILITY}$ | MET-INLB | 250 | -0.501 | 0.767 | 0.3153 |

*no ground truth for real data; values are the distribution of inferred MAP theta per condition (pooled over (cell x chunk)). Compare conditions to read out parameter differences.*

## What these mean

A check **PASS** means the invariant held; a **FAIL** aborts the run immediately with a located error message.

- **estimates_nonempty** -- at least one experimental chunk was MAP-estimated.

## Figures

![experiment_count_alp](figures/experiment_count_alp.png)

*count_alp ($C_{A}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_count_bet](figures/experiment_count_bet.png)

*count_bet ($C_{B}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_count_chi](figures/experiment_count_chi.png)

*count_chi ($C_{C}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_diffusivity_alp](figures/experiment_diffusivity_alp.png)

*diffusivity_alp ($D_{A}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_relative_diffusivity_bet](figures/experiment_relative_diffusivity_bet.png)

*relative_diffusivity_bet ($R_{B}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_relative_diffusivity_chi](figures/experiment_relative_diffusivity_chi.png)

*relative_diffusivity_chi ($R_{C}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_relative_rate_dimerization](figures/experiment_relative_rate_dimerization.png)

*relative_rate_dimerization ($R_{ON}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_rate_dissociation](figures/experiment_rate_dissociation.png)

*rate_dissociation ($\kappa_{OFF}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_rate_immobility](figures/experiment_rate_immobility.png)

*rate_immobility ($\kappa_{IMMOBILITY}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*

![experiment_rate_mobility](figures/experiment_rate_mobility.png)

*rate_mobility ($\kappa_{MOBILITY}$). View A (MAP): per-condition distribution of inferred MAP theta (pooled over (cell x chunk)). View B (posterior): each chunk's posterior median +/- IQR per condition (within-chunk uncertainty). A panel stamped 'not computed' marks a view the --summary option omitted.*
