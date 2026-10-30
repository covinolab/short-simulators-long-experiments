# Experiment temporal dynamics — SRM_AND_SBI_DIMER_ALP 2S_50FPS
Run: 2026-08-20 11:56:44 UTC

Generated from `SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment.npz`. **500 MAP estimates** = 2 conditions × 25 recordings × 10 non-overlapping 2 s windows spanning [0, 20) s. Conditions: MET-FAB, MET-INLB (stored tokens ALP, BET). Central-estimate family: **sgm**.

## What the analysis asks, and what it cannot answer alone

The Experiment stage reports one **MAP estimate per window** — the point estimate it optimizes for one (condition, cell, chunk) window. Stacking the windows along time asks whether an inferred value holds still across the recording. A parameter that is a constant property of the system should be flat; a trend is **either real dynamics or an acquisition confound**, and this analysis cannot decide which.

That limit is structural. The biology workflow holds imaging fixed, so it is blind to imaging drift; the detector workflow marginalizes the reaction-diffusion block, so it is blind to biological drift. The two read the **same recordings** — the experimental path pattern carries no workflow qualifier, so a given recording index is the same acquisition in both — which makes each the other's control. Neither attributes a cause on its own.

## The central estimate — exactly what was aggregated

A timeseries needs one vector per chunk, so the **cell** axis is aggregated; a single summary line needs one vector overall, so the **cell and chunk** axes are. Crossing that with the choice of estimator gives four, named for what they aggregate:

| name | definition | drawn as |
|---|---|---|
| `mean-window` | Mean value vector, aggregated across cells for a given chunk, of the MAP estimate vectors computed for (chunk, cell) pairs. Each parameter is averaged independently. | timeseries |
| `sgm-window` | Realized value vector, aggregated across cells for a given chunk, minimizing the summed normalized distance to the other cells' vectors at that chunk, of the MAP estimate vectors computed for (chunk, cell) pairs. | timeseries |
| `mean-trajectory` | Mean value vector, aggregated across chunks and cells, of the MAP estimate vectors computed for (chunk, cell) pairs. | horizontal line |
| `sgm-trajectory` | Realized value vector, aggregated across chunks and cells, minimizing the summed normalized distance to all other (chunk, cell) vectors. | horizontal line |

This run drew the **sgm-window** timeseries with the **sgm-trajectory** summary line. The pairing is enforced, so the curve and the line are always the same estimator.

**Distance metric** (both `sgm-*` estimates): absolute values `10**theta`, each parameter divided by its absolute prior width `10**high - 10**low` so no parameter dominates, Euclidean, **exact medoid** — the member minimizing the summed distance to every other member of the set. Selection is on **all parameters jointly**, so a selected vector is internally coherent; consequently the value it reports for one parameter is that jointly-central window's value, not that parameter's own median.

A `mean-*` estimate averages each parameter independently, so its coordinates need not have co-occurred in any recording. An `sgm-*` estimate is an actual window, so its coordinates did.

### Which windows were selected

- **MET-FAB** — `sgm-trajectory`: cell 17, chunk 6 (one realized window). `sgm-window` selected 6 distinct: 3,7,8,14,17,22 across the 10 chunks.
- **MET-INLB** — `sgm-trajectory`: cell 14, chunk 3 (one realized window). `sgm-window` selected 4 distinct: 1,8,9,14 across the 10 chunks.

`sgm-window` selecting more than one cell is expected and must be read with the curve: **a step between adjacent chunks can be a change of cell rather than a change in time.** `sgm-trajectory` is a single window and carries no such ambiguity, and it is the same quantity the standalone sample-geometric-median analysis reports over the same pooled windows, so the two agree by construction.

## Drift — measured per cell, independent of the display

For every (condition, cell, parameter) an ordinary least-squares line is fit to the stored **log10** MAP estimate against time (log10 because drift is multiplicative), giving a slope and hence fitted endpoints:

```
change_dex = slope * (t_last - t_first)
start      = 10 ** (fitted value at t_first)
end        = 10 ** (fitted value at t_last)
```

Because the fit is per cell, **none of these statistics depends on the central estimate the figures draw**: swapping a mean for a medoid changes what is displayed, not what is measured.

| name | definition |
|---|---|
| `drift-absolute` | Median across cells of `end - start`, in the parameter's own units. **Annotated on the figure.** |
| `drift-sign-consistency` | Fraction of cells whose change shares the sign of the median change. **Annotated on the figure.** |
| `drift-fold` | Median across cells of `end / start`, a multiplicative factor. |
| `drift-dex` | Median across cells of `change_dex`, in log10 units. |
| `drift-material-fraction` | Fraction of cells whose `|change_dex|` exceeds 0.3 dex (a factor of two). |
| `drift-wilcoxon-p` | Two-sided signed-rank test that the per-cell changes are centered at zero. A **detectability** statement, not a magnitude. |
| `reference-ratio` | The `*-trajectory` value divided by the reference mean, where a reference applies to that condition. |
| `reference-verdict` | Whether the `*-trajectory` value lies inside the reference band. |

| Parameter | MET-FAB: sgm-traj | MET-INLB: sgm-traj | MET-FAB: drift-absolute / fold / dex / sign / >2x / p | MET-INLB: drift-absolute / fold / dex / sign / >2x / p | reference |
|---|---|---|---|---|---|
| Initial monomer count ($C_{A}$) | 151 | 105.1 | -68.9 / 0.62x / -0.209 / 88% / 16% / 1.8e-05 | -0.643 / 1.00x / -0.002 / 52% / 84% / 2.5e-01 | — |
| Initial mobile-dimer count ($C_{B}$) | 26.38 | 100.7 | -7.53 / 0.68x / -0.165 / 64% / 52% / 7.1e-02 | -9.86 / 0.54x / -0.268 / 56% / 80% / 9.8e-01 | — |
| Initial immobile-dimer count ($C_{C}$) | 22.47 | 329.6 | -24 / 0.59x / -0.227 / 84% / 36% / 5.4e-05 | -122 / 0.58x / -0.238 / 68% / 56% / 4.2e-02 | — |
| Monomer diffusivity ($D_{A}$) | 0.1239 | 0.1329 | -0.00973 / 0.93x / -0.033 / 80% / 0% / 3.0e-02 | +0.00616 / 1.05x / +0.021 / 52% / 44% / 5.2e-01 | 0.101 [0.04–0.177] um^2/s; MET-FAB 1.2x, inside; MET-INLB 1.3x, inside |
| Rel. mobile-dimer diffusivity ($R_{B}$) | 0.4049 | 0.655 | -0.137 / 0.71x / -0.149 / 80% / 8% / 1.2e-04 | +0.0164 / 1.04x / +0.019 / 52% / 48% / 2.0e-01 | 0.604 [0.602–0.606] ratio; MET-INLB 1.1x, outside |
| Rel. immobile-dimer diffusivity ($R_{C}$) | 0.02383 | 0.003302 | +0.00312 / 1.38x / +0.140 / 80% / 12% / 4.9e-04 | +0.00185 / 1.34x / +0.127 / 64% / 64% / 5.8e-01 | — |
| Rel. dimerization rate ($R_{ON}$) | 0.08694 | 0.08485 | -0.00796 / 0.92x / -0.037 / 88% / 0% / 2.2e-05 | +0.000805 / 1.01x / +0.004 / 52% / 20% / 3.7e-01 | — |
| Dissociation rate ($\kappa_{OFF}$) | 3.104 | 3.515 | +2.07 / 2.84x / +0.454 / 80% / 64% / 1.8e-05 | +1.82 / 2.21x / +0.344 / 80% / 64% / 1.8e-03 | 1.01 [0.74–1.3] 1/s; MET-INLB 3.5x, outside |
| Immobilization rate ($\kappa_{IMMOBILITY}$) | 6.595 | 3.191 | +1.82 / 1.59x / +0.201 / 68% / 60% / 7.5e-02 | +1.15 / 1.42x / +0.153 / 64% / 64% / 1.7e-01 | — |
| Mobilization rate ($\kappa_{MOBILITY}$) | 0.1412 | 0.1861 | -0.187 / 0.62x / -0.210 / 80% / 40% / 1.0e-04 | -0.473 / 0.31x / -0.512 / 92% / 68% / 1.1e-06 | — |

**A time-aggregated summary of a drifting parameter summarizes a non-stationary process.** Where `drift-absolute` is large and `drift-sign-consistency` high, the `*-trajectory` line — and any reference comparison drawn against it — is a summary over that drift, not a measurement of a constant.

## Uncertainty figure

`<key>_temporal_posterior.png` shows, at each chunk, the **median across cells of that window's stored posterior interval** — how uncertain a typical single window's estimate is. It is an interval **width** built from the stored five-quantile record, **not a posterior density**, and it does not approximate one.

When a parameter's interval spans essentially its whole prior, the posterior is returning the prior and the point estimate is the prior's center regardless of the data.

## Pooled posterior density (time axis collapsed)

`<key>_temporal_posterior_pooled.png` is the classic histogram: every window's posterior draws, pooled within a condition, in the parameter's absolute units. This run used 64 **both-spaced** bins. With `log` spacing the bins are uniform across the prior's decades, height is a density **per decade**, and the log-uniform prior is the flat dashed line at `1 / (log10 hi - log10 lo)`. With `linear` spacing the bins are uniform in absolute units, height is a density **per unit**, and the prior is drawn as the `1 / x` curve a log-uniform density becomes under `x = 10**y` — not a flat line, which would misread the change of variable as evidence. Either way the distance between a curve and the prior is what the data added.

**How the pooling works, exactly.** The Experiment stage draws 1,000 samples from the posterior of every (recording, window) pair. For one condition that is 25 recordings x 10 windows x 1,000 draws, and all of them enter one histogram with equal weight.

**What that mixture does and does not mean.** Equal-weight pooling makes the **mixture** of the per-window posteriors. Its density answers: for a single window drawn at random from this condition, which values are consistent with it? It is **not** a joint posterior for the condition — combining independent observations under Bayes multiplies likelihoods, whereas pooling draws adds densities. The mixture is therefore as wide as the between-window spread plus the within-window uncertainty, while a genuine joint posterior over all windows would be narrower than any single one of them. Read the width as a property of the window population, never as evidence accumulated over the recording.

Because it is a population rather than an estimate, the mixture's mode and median are **not** this analysis's central estimate. That remains `sgm-trajectory`, marked as a thin vertical line: one jointly realized vector, which a per-parameter summary of pooled marginals is not. The two answer different questions and need not coincide.

| parameter | label | MET-FAB p05 | MET-FAB median | MET-FAB p95 | MET-INLB p05 | MET-INLB median | MET-INLB p95 |
|---|---|---|---|---|---|---|---|
| `count_alp` | $C_{A}$ | 30.4 | 186 | 642 | 0.475 | 73.4 | 238 |
| `count_bet` | $C_{B}$ | 1.28 | 19.6 | 162 | 0.653 | 42.1 | 334 |
| `count_chi` | $C_{C}$ | 6.08 | 46 | 227 | 94.8 | 291 | 658 |
| `diffusivity_alp` | $D_{A}$ | 0.103 | 0.135 | 0.178 | 0.0625 | 0.127 | 0.56 |
| `relative_diffusivity_bet` | $R_{B}$ | 0.238 | 0.463 | 0.988 | 0.168 | 0.623 | 1.87 |
| `relative_diffusivity_chi` | $R_{C}$ | 0.00578 | 0.0167 | 0.0377 | 0.00166 | 0.00546 | 0.0327 |
| `relative_rate_dimerization` | $R_{ON}$ | 0.0107 | 0.0924 | 0.802 | 0.00653 | 0.0931 | 1.39 |
| `rate_dissociation` | $\kappa_{OFF}$ | 0.157 | 2.77 | 15.5 | 0.2 | 1.81 | 12.3 |
| `rate_immobility` | $\kappa_{IMMOBILITY}$ | 0.515 | 5.61 | 16.7 | 0.276 | 3.8 | 13.1 |
| `rate_mobility` | $\kappa_{MOBILITY}$ | 0.0708 | 0.201 | 2.42 | 0.0896 | 0.324 | 2.18 |

Marginal quantiles of the pooled mixture, in absolute units. Per-coordinate by construction, so they carry no joint information — which is why they sit beside the `sgm-trajectory` vector rather than replacing it.

### Marginal centers versus the trajectory medoid

A vertical line on a one-dimensional histogram is read as the center of that histogram, so the figure marks a **marginal** center of the plotted mixture (`median-pooled`) and keeps `sgm-trajectory` beside it. The two answer different questions and the table below is where the gap between them can be checked parameter by parameter.

- `median-pooled` — marginal median of the pooled draws. **Equivariant**: the median in absolute units and `10 ** median(log10)` are the same number, so this value does not depend on the space it was computed in.
- `mean-pooled` — arithmetic mean in absolute units. **Not equivariant**: it differs from `geomean-pooled` by a factor that grows with the spread, so for a log-uniform prior it partly reports the choice of basis rather than the posterior. Reported because it is what "the mean of the posterior" usually names, not because it is the better summary.
- `geomean-pooled` — `10 ** mean(log10)`, the mean taken in the space the prior is uniform in.
- `sgm-trajectory` — the medoid: one jointly realized vector. Its coordinates are a real recording's values and need **not** be marginally central; a large `ratio` below means the mixture is skewed for that parameter, not that the medoid is wrong.

| parameter | condition | median-pooled | mean-pooled | geomean-pooled | sgm-trajectory | ratio traj/median |
|---|---|---|---|---|---|---|
| `count_alp` | MET-FAB | 186 | 259 | 172 | 151 | 0.81x |
| `count_alp` | MET-INLB | 73.4 | 90 | 29.3 | 105 | 1.43x |
| `count_bet` | MET-FAB | 19.6 | 38.3 | 16.2 | 26.4 | 1.35x |
| `count_bet` | MET-INLB | 42.1 | 91.2 | 27.1 | 101 | 2.39x |
| `count_chi` | MET-FAB | 46 | 69.9 | 42.3 | 22.5 | 0.49x |
| `count_chi` | MET-INLB | 291 | 323 | 275 | 330 | 1.13x |
| `diffusivity_alp` | MET-FAB | 0.135 | 0.137 | 0.135 | 0.124 | 0.92x |
| `diffusivity_alp` | MET-INLB | 0.127 | 0.193 | 0.148 | 0.133 | 1.05x |
| `relative_diffusivity_bet` | MET-FAB | 0.463 | 0.524 | 0.473 | 0.405 | 0.87x |
| `relative_diffusivity_bet` | MET-INLB | 0.623 | 0.949 | 0.595 | 0.655 | 1.05x |
| `relative_diffusivity_chi` | MET-FAB | 0.0167 | 0.0187 | 0.016 | 0.0238 | 1.43x |
| `relative_diffusivity_chi` | MET-INLB | 0.00546 | 0.0154 | 0.00582 | 0.0033 | 0.60x |
| `relative_rate_dimerization` | MET-FAB | 0.0924 | 0.219 | 0.0924 | 0.0869 | 0.94x |
| `relative_rate_dimerization` | MET-INLB | 0.0931 | 0.436 | 0.0939 | 0.0849 | 0.91x |
| `rate_dissociation` | MET-FAB | 2.77 | 4.68 | 2.22 | 3.1 | 1.12x |
| `rate_dissociation` | MET-INLB | 1.81 | 3.57 | 1.71 | 3.51 | 1.94x |
| `rate_immobility` | MET-FAB | 5.61 | 6.7 | 4.42 | 6.6 | 1.18x |
| `rate_immobility` | MET-INLB | 3.8 | 4.86 | 2.94 | 3.19 | 0.84x |
| `rate_mobility` | MET-FAB | 0.201 | 0.586 | 0.277 | 0.141 | 0.70x |
| `rate_mobility` | MET-INLB | 0.324 | 0.701 | 0.374 | 0.186 | 0.57x |

All values in the parameter's absolute units. Every entry except `sgm-trajectory` is a per-coordinate composite: its coordinates come from different draws and need never have co-occurred, so use them to describe a marginal and never as the condition's parameter vector.

## External reference values

Source: Li et al., Small 2026, 22, e07115. A reference is drawn only on the parameters it constrains and only for the conditions it applies to; drawing it elsewhere would invite a false comparison.

- **Dissociation rate** (MET-INLB only): kappa_OFF = 1/tau per FRET variant: 1/1.30=0.77, 1/0.80=1.25 1/s (tau = 1.30+/-0.05, 0.80+/-0.03 s; SD propagated as d(tau)/tau^2); band = value+/-SD; mean line = mean of the two RATES = 1.01. The study measured InlB-activated MET, so the reference compares to MET-INLB only. Li et al. 2026, Fig. 2C
- **Monomer diffusivity** (both conditions): monomer diffusion, donor-only segments: 0.109+/-0.068 (T-T), 0.093+/-0.053 (H-T) um^2/s; band = value+/-SD; mean = 0.10. Monomer diffusion is ligand-independent, so the reference applies to both conditions. Li et al. 2026, Sec. 2.3
- **Rel. mobile-dimer diffusivity** (MET-INLB only): R_B = D_dimer/D_monomer per FRET variant: 0.066/0.109=0.61 (T-T), 0.056/0.093=0.60 (H-T); mean = 0.60. Derived from the InlB-activated measurement, so it compares to MET-INLB. Li et al. 2026, Sec. 2.3

No external reference exists for: Initial monomer count, Initial mobile-dimer count, Initial immobile-dimer count, Rel. immobile-dimer diffusivity, Rel. dimerization rate, Immobilization rate, Mobilization rate. These are read on their internal evidence alone — drift, recovery, and posterior width.

## How to read a parameter

**Held-out recovery bands.** Where a recovery artifact exists for this workflow, each figure states the fraction of held-out synthetic videos whose inferred value landed inside two nested tolerances of the truth: `[0.50x, 2.00x]` and `[0.71x, 1.41x]`. These are the multiplicative ranges of the log10 half-widths ±0.3 dex and ±0.15 dex that the Evaluation stage reports — a factor of two and a factor of the square root of two — restated as the value range they permit, since that is what a reader needs in order to judge whether the parameter is usable.

Trust a parameter on experimental data when it recovers well on held-out synthetic data, **and** is stationary where the model says it should be, **and** its posterior is narrow relative to its prior. A parameter that recovers poorly carries no signal however smooth its trajectory looks, and a posterior that spans its prior is reporting the prior back. A parameter that drifts is not thereby discredited — the drift may be the acquisition's, which is what the other workflow's run measures.
