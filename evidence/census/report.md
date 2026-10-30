# Experimental versus synthetic estimates — comparison report

`SRM_AND_SBI_DIMER_ALP_2S_50FPS` · biology workflow
Run: 2026-08-21 (analysis date; artifact run stamps in §9)

---

## 1. Scope and question

This report compares, for the biology workflow at 2 s / 50 FPS, the parameter estimates obtained on
**experimental** single-particle-tracking recordings of the MET receptor against the estimator's
behavior on **synthetic** data, and reads both against independent published measurements. It answers
three questions in order:

1. **What can the estimator do when the model is true?** — validation on held-out synthetic videos
   with known ground truth (§3).
2. **Are the experimental videos inside the domain the estimator was trained on?** — the formal
   experimental-versus-synthetic comparison: embedding-space distance, scene density, and prior
   support (§4).
3. **What do the experimental estimates say, and how far can they be trusted?** — the
   population-composition and rate estimates, their robustness checks, and their consistency with
   independent experiments (§5–§7).

The report is self-contained: every number quoted here was computed from the artifacts listed in §9,
and every external value carries a public citation.

### 1.1 At a glance — the MET population, measured two ways

The recordings analyzed here are the same ones published in [1]. That study classified individual
*trajectories* by their motion, without a dynamical model; this work infers a census of *complexes*
by species, through a reaction–diffusion model fitted by simulation-based inference. Both are
population percentages of the same receptor system, resting versus activated. The columns of the
two tables are aligned by decreasing mobility — free ↔ monomers, confined ↔ mobile dimers,
immobile ↔ immobile dimers are the closest counterparts — but the units differ (trajectories
versus complexes), so the pairing is a reading aid, not an identity.

**Published trajectory classification** (fraction of trajectories; mean ± SEM over N = 60 cells;
Fab- and InlB321-bound MET [1]):

| condition | free | confined | immobile | all dimers |
|---|---|---|---|---|
| Fab/MET (resting) | 57 ± 3% | 31 ± 3% | 12 ± 1% | — |
| InlB/MET (activated) | 60 ± 1% | 17 ± 2% | 23 ± 1% | — |

**This work — model-based complex census** (fraction of complexes; mean ± SEM over n = 25 cells;
time-averaged over the 20 s recordings; full-precision values and robustness checks in §5.1):

| condition | monomers | mobile dimers | immobile dimers | all dimers |
|---|---|---|---|---|
| MET-FAB (resting) | 69 ± 2% | 13 ± 2% | 18 ± 1% | 31 ± 2% |
| MET-INLB (activated) | 22 ± 4% | 16 ± 2% | 63 ± 3% | 78 ± 4% |

Read together:

- **Resting state — the two readouts are numerically close.** 12% immobile trajectories versus
  18% immobile-dimer complexes; 88% mobile trajectories versus 82% mobile complexes. This is
  same-data mobility triangulation, not stoichiometric validation: motion class and molecular
  species have no established one-to-one mapping, and [1] shares the data lineage of this work.
- **Activation direction — the two analyses agree.** Both see the population shift toward
  immobility: the immobile share roughly doubles in [1] (12 → 23%) and more than triples here
  (18 → 63%).
- **Activation magnitude — they diverge, and the divergence is the model speaking.** This work
  places most of the activated population (63%) in the immobile-dimer state, against 23% immobile
  trajectories in [1]. That state is where the model concentrates everything slow, bright, and
  persistent (§6); the 63% is an effective model-based composition, not a molecular census.
- **The all-dimers column has no counterpart in [1]** (dash above): the study reports no dimer
  fractions. Two stoichiometric comparators exist. [2] reports protocol-specific dimer-associated
  spot fractions of 18% (resting) and 29% (after InlB321) that its authors expect to
  underestimate (sub-stoichiometric labeling) — not bounds transferable to another experiment.
  [4] (detection-corrected qPALM, endogenously tagged HEK293T) reports 5 ± 1% dimers at rest and
  63 ± 2% after InlB (68 ± 4% among ligand-colocalized spots): activation direction and activated
  magnitude (63–68% versus our model-conditional 78%) are approximately consistent, while our
  resting 31% sits above both published resting values — different cell lines, labeling
  strategies and estimands; none of these values is ground truth for another.
- **The census values are 20 s time averages.** The MET-INLB composition evolves within the
  recording (all dimers 87.0% in the first 2 s window → 70.2% in the last, §5.1); MET-FAB is flat.

### 1.2 At a glance — diffusion, dissociation, and abundance

The remaining externally anchored quantities, against the published values:

| observable (units) | published value | this work — MET-FAB | this work — MET-INLB | estimand match | reading |
|---|---|---|---|---|---|
| monomer diffusivity D_A (µm²/s) | 0.109 ± 0.068 and 0.093 ± 0.053 (mean ± SD, donor-only segments of two constructs [3]) | 0.124 | 0.133 | direct — same quantity | inside the span of the published values (the 0.040–0.177 envelope used previously is a union of the two mean ± SD ranges constructed in this project, not a published interval) |
| ensemble diffusivity (µm²/s) | Fab 0.126 ± 0.005; InlB321 0.085 ± 0.003 [1] | 0.124 (scene ~70% monomer, so ensemble ≈ D_A) | slowdown carried by the composition shift (63% immobile dimers), not by D_A | direct (MET-FAB); via decomposition (MET-INLB) | agrees; consistent |
| dissociation rate kappa_OFF (1/s) | no dissociation rate is published; [3] reports apparent (MET:InlB)₂ lifetimes of order 1 s (1.13 ± 0.06 and 0.80 ± 0.03 s), whose inversion gives a comparison scale of ~0.9–1.3 1/s DERIVED HERE | no published counterpart; drifts 0.68 → 4.89 within the recording | 1.75 (first window) → 2.20; 2.8–3.5 time-aggregated | partial — an effective termination scale, not the model's B → A + A rate; the estimate drifts with the acquisition (§5.2) | ~1.7x above the derived scale at the least-contaminated window; no constant-rate reading supported |
| total complex abundance (per scene) | not reported in [1–3] | median 267 | median 503 (1.88x, p = 0.014) | no external anchor | internal contrast only |

Published conditions: [1] live cells at 23 °C; [3] live-cell single-molecule FRET-tracking of
InlB-bound MET. All values from this work are model-conditional estimates on the S-BSST712
recordings — the domain gap of §4 applies; full discussion in §5.2 and §6.

## 2. Data and estimator

**Experimental data.** 50 recordings of MET (hepatocyte growth factor receptor) on live cells,
single-particle tracking, 20 s at 50 FPS, in two conditions of 25 cells each: **MET-FAB** (receptor
bound by a non-activating Fab fragment — the resting, non-activating condition) and **MET-INLB**
(the InlB-activated, dimerization-enriched condition); both conditions can contain mixtures of
monomers and dimers. Source: BioStudies / BioImage Archive accession `S-BSST712`, the study of
Harwardt et al. (2017) [1]; the activating ligand in that study is the truncated construct
InlB321, and acquisition began approximately three minutes after ligand addition [1], so the
first recorded window is not the initial post-ligand state. Each recording is analyzed in ten non-overlapping
2 s windows, giving 250 windows per condition; the recording (cell) is the independent replicate
unit, so all condition-level tests below are 25-versus-25.

**Synthetic data.** 10,000 held-out evaluation videos from the same simulator the estimator was
trained on (reaction–diffusion dynamics of three species — A: monomer, B: mobile dimer, C: immobile
dimer — rendered through the calibrated diffraction-limited-imaging chain). Each synthetic video
carries its own ground-truth parameter vector drawn log-uniformly from the prior box.

**Estimator.** A single amortized neural posterior estimator (masked autoregressive flow conditioned
on a 3D-CNN + temporal-attention video embedding), 10 learnable parameters, applied identically to
both data sources. Real-data windows were estimated with the unrestricted candidate pool, so point
estimates and posterior draws may leave the trained prior box; §4.3 and §5.2 quantify the
consequences.

## 3. What the synthetic side establishes

### 3.1 Per-parameter recovery (10,000 held-out videos)

| parameter | MAE (dex) | r | within [0.50x, 2.00x] | within [0.71x, 1.41x] |
|---|---|---|---|---|
| count_alp (C_A) | 0.117 | 0.967 | 88.6% | 72.8% |
| count_bet (C_B) | 0.158 | 0.938 | 83.0% | 66.3% |
| count_chi (C_C) | 0.130 | 0.960 | 87.2% | 71.0% |
| diffusivity_alp (D_A) | 0.023 | 0.993 | 100.0% | 99.4% |
| relative_diffusivity_bet (R_B) | 0.076 | 0.721 | 99.5% | 85.8% |
| relative_diffusivity_chi (R_C) | 0.116 | 0.827 | 91.7% | 73.2% |
| relative_rate_dimerization (R_ON) | 0.499 | 0.040 | 29.8% | 14.7% |
| rate_dissociation (kappa_OFF) | 0.177 | 0.899 | 82.4% | 58.3% |
| rate_immobility | 0.226 | 0.832 | 73.6% | 49.7% |
| rate_mobility | 0.156 | 0.919 | 85.8% | 63.4% |

Three structural facts qualify this table:

- **R_ON is unidentified** (r = 0.04, worse than a constant predictor; its posterior undercovers,
  0.783 against a nominal 0.90). No R_ON statement on experimental data is supportable.
- **Individual counts are accurate only above roughly 32 receptors.** The fraction recovered within
  a factor of 1.41 crosses 0.8 at the 31.6-receptor boundary for all three counts; in the
  10–31.6-receptor band a constant guess of ~18 receptors matches the estimator's accuracy. The
  degradation follows the square-root-of-n law expected for counting few emitters — an information
  limit, not a training-coverage gap (the log-uniform prior places ~60% of training below 31.6
  receptors).
- **Rate accuracy improves with scene abundance.** kappa_OFF error falls from 0.208 dex to
  0.091 dex as the dimer-limiting species count min(B, C) rises from ~1 to ~180, saturating above
  ~100. Given a video, kappa_OFF is conditionally near-independent of the counts (|r| <= 0.083),
  so this gain enters through the likelihood (more observed events), not through any prior choice.

### 3.2 Derived population composition recovers far better than its parts

Because the three counts trade off against one another in the posterior (B–C correlation −0.56
within a window), quantities derived from the **joint** count vector are recovered much better than
the counts individually:

| derived quantity | definition | MAE | p95 abs. error |
|---|---|---|---|
| total complex count | A + B + C | 0.0117 dex (factor 1.027) | — (r = 0.9995) |
| monomer fraction f_A | A / (A+B+C) | 2.8 pp | 8.3 pp |
| mobile-dimer fraction f_B | B / (A+B+C) | 5.0 pp | 15.8 pp |
| immobile-dimer fraction f_C | C / (A+B+C) | 4.3 pp | 14.5 pp |
| dimer-complex fraction f_D | (B+C) / (A+B+C) | 2.8 pp | 8.3 pp |
| receptors in dimers f_R | 2(B+C) / (A+2B+2C) | 2.2 pp | 7.1 pp |

The dimer-rich corner that matters for MET-INLB is not a weak spot: restricted to true f_D > 0.7
(n = 5,634), the MAE is 2.6 pp with bias +0.3 pp. The monomer-versus-dimer contrast is therefore a
well-identified readout; the mobile-versus-immobile subdivision (f_B vs f_C) is roughly twice as
uncertain.

### 3.3 Calibration

Marginal 90% credible intervals are conservative for the counts (empirical coverage
0.936 / 0.932 / 0.928 against nominal 0.90). Two documented exceptions: at the one-receptor floor
coverage collapses one-sidedly (0.62–0.68, all misses below the interval), and for a species holding
under 1% of a scene's complexes coverage falls to 0.633 — the dimmest species in a crowded scene is
reported with too narrow an interval.

## 4. Where the experimental data sit relative to the synthetic domain

### 4.1 Embedding-space distance (formal comparison)

Both data sources were passed through the estimator's own embedding and compared as point clouds
(500 experimental windows versus 10,000 synthetic; MMD with permutation test, and a
classifier-two-sample test whose class-imbalance baseline is 0.952):

| comparison | MMD | MMD p | C2ST accuracy | verdict |
|---|---|---|---|---|
| experimental (pooled) vs synthetic | 0.584 | 0.000999 (permutation floor) | 0.999 | **gap** |
| MET-FAB vs synthetic | 0.583 | 0.000999 | 0.999 | gap |
| MET-INLB vs synthetic | 0.749 | 0.000999 | 0.999 | gap |
| MET-FAB vs MET-INLB | 0.621 | 0.000999 | 0.978 | separable |

The experimental recordings are distinguishable from the synthetic reference: a classifier
separates them essentially perfectly. What this establishes is a **prior-predictive distribution
difference** — the synthetic reference spans the whole training prior while the experimental
windows come from one instrument and one biology — not support exclusion, structural
misspecification, or bias in any particular inferred parameter. MET-INLB lies farther from the
synthetic cloud than MET-FAB, and the two conditions are separable from each other. Absolute
estimates in §5 therefore carry an unquantified transfer risk, which is why every conclusion in
§7 is graded rather than asserted.

### 4.2 Scene abundance

The experimental scenes are denser than the synthetic training regime: the experimental median total
complex count (388.6) sits at the 93.6th percentile of the synthetic distribution (median 129.9);
46.2% of experimental windows exceed the synthetic 95th percentile, and 8.6% exceed the synthetic
maximum (818).

### 4.3 Prior support

A substantial fraction of experimental count estimates presses beyond the trained prior ceiling of
316 receptors per species: 32.8% of MET-FAB count_alp and 41.6% of MET-INLB count_chi point
estimates exceed it, and at the posterior-draw level 32.9% and 44.1% of draws respectively lie
outside the box (only 50% of MET-INLB's joint draws are fully inside). Absolute counts in that
regime are extrapolations of the flow beyond its training support. The prior binds at its
**ceiling**, not its floor.

## 5. Experimental estimates

### 5.1 Population composition (primary readout)

Fractions are computed per posterior draw from the jointly sampled (A, B, C) — preserving their
correlations — then averaged: draws → window, windows → cell, cells → condition (mean ± SEM,
n = 25 cells). Fractions close to 100% exactly by construction. A cell-level bootstrap (10,000
resamples) reproduces every normal-theory interval within 0.45 pp, and a log-ratio compositional
center moves the headline values only in the direction of a **stronger** contrast, so the arithmetic
mean is the conservative choice. A condensed at-a-glance version appears in §1.1.

**Time-averaged over the full 20 s recording:**

| condition | monomer complexes | mobile dimers | immobile dimers | all dimer complexes | receptors in dimers |
|---|---|---|---|---|---|
| MET-FAB | 68.6 ± 2.0% | 12.9 ± 1.7% | 18.4 ± 0.7% | 31.4 ± 2.0% | 46.4 ± 2.2% |
| MET-INLB | 21.8 ± 3.7% | 15.6 ± 1.7% | 62.6 ± 2.7% | 78.2 ± 3.7% | 86.2 ± 2.5% |

**First recorded window only (0–2 s of acquisition; recording began ~3 min after ligand addition [1], so this is the earliest measured, not the initial post-ligand, composition):**

| condition | monomer | mobile dimers | immobile dimers | all dimers | receptors in dimers |
|---|---|---|---|---|---|
| MET-FAB | 67.5% | 13.4% | 19.0% | 32.5% | 47.0% |
| MET-INLB | 13.0% | 15.7% | 71.4% | 87.0% | 91.8% |

**Robustness to the prior-support problem (§4.3).** Excluding every posterior draw outside the
trained count box — half of MET-INLB's draws — moves the dimer-complex fraction from 78.2% to 77.1%
(MET-FAB: 31.4% to 35.8%): the composition is a ratio, and the extrapolated mass inflates all three
counts roughly together. The harshest variant, restricting to draws inside the **full ten-parameter**
prior box, retains only 3.4% of MET-INLB's draws (123 of its 250 windows keep none) and yields
fD = 73.1%; the alternative compositional center (closed geometric mean across cells) yields 86.4%.
The honest model-conditional bracket for the MET-INLB dimer-complex fraction is therefore
**73–86%**, with 78.2% the conservative arithmetic headline. Under every variant the condition
contrast against MET-FAB (29–36%) is preserved.

**Per-cell heterogeneity.** The MET-INLB response is not uniform: the per-cell monomer fraction
spans 1.2% to 52.8%, with bimodal structure (9 of 25 cells below 10%, 6 above 40%). The condition
mean does not describe a typical cell, and per-cell values should accompany any downstream use.

**Time course.** The MET-FAB dimer fraction is flat across the recording (32.5% in the first
window, 31.7% in the last; per-cell first-versus-last Wilcoxon p = 0.52). The MET-INLB dimer
fraction declines monotonically from 87.0% to 70.2% (median per-cell Spearman rho = −0.71 against
window index; first-versus-last p = 0.0015). A photobleaching artifact — a dimer losing one of its
two fluorophores and resembling a monomer in brightness — was considered as the cause of the decline
and **fails three independent tests**: (i) magnitude — the measured per-window bleaching probability
predicts a final-window dimer fraction of roughly 7–20% if masquerade dominated, against the
observed 70.2%; (ii) control — MET-FAB shows the *stronger* measured bleaching drift (−0.518 versus
−0.446 dex on the same recordings, detector workflow) yet a flat composition; (iii) sign — a
two-label dimer remains visible longer than a single-label monomer under shared bleaching, which
predicts an apparent dimer fraction that rises, not falls. Within-window bleaching is, moreover,
part of the trained forward model. The simple bleaching artifacts tested here (magnitude, control, and
sign) therefore do not straightforwardly account for the observed recording-position dependence,
and the decline is **consistent with** post-ligand evolution of the population (dimer disassembly
and/or internalization over the 20 s). The composition should be read as a trajectory: the first
recorded window gives the earliest measured composition (fD = 87.0%, ~3 min post-ligand [1]), the
time-averaged table its 20 s summary. Full attribution among biological and acquisition
mechanisms remains open.

**Condition contrast at cell level (Mann-Whitney, 25 vs 25):**

| quantity | MET-FAB median | MET-INLB median | ratio | p |
|---|---|---|---|---|
| monomer fraction f_A | 0.697 | 0.219 | 0.31x | 2e-09 |
| immobile-dimer fraction f_C | 0.177 | 0.607 | 3.42x | 1.4e-09 |
| dimer-complex fraction f_D | 0.303 | 0.781 | 2.57x | 2e-09 |
| receptors in dimers f_R | 0.461 | 0.872 | 1.89x | 2e-09 |
| total complex count | 267 | 503 | 1.88x | 0.014 |
| mobile-dimer fraction f_B | 0.128 | 0.170 | 1.33x | 0.19 (n.s.) |
| kappa_OFF (1/s) | 4.05 | 2.61 | 0.64x | 0.21 (n.s.) |

The contrasts that reach significance are exactly the ones the synthetic validation licenses (§3.2):
the composition and the total. The mobile-dimer subdivision — the least identified derived quantity —
does not resolve, and neither does a condition difference in kappa_OFF.

### 5.2 Rate parameters

**Dissociation rate (kappa_OFF).** Measured per window (median across cells), kappa_OFF **rises
across the recording**: 0.68 → 4.89 1/s in MET-FAB (a 7.2x span) and 1.75 → 2.20 1/s in MET-INLB.
The per-cell drift is +0.454 dex (MET-FAB) and +0.344 dex (MET-INLB), 80% sign-consistent in both.
No dissociation rate is published for this system; [3] reports apparent (MET:InlB)₂ complex
lifetimes of order one second (1.13 ± 0.06 and 0.80 ± 0.03 s), and the ~1 1/s comparison scale
used here is derived by inverting them — an effective FRET-segment termination scale, not a
direct measurement of the model's B → A + A rate. The
first-window MET-FAB value (0.68) sits below that scale and the first-window MET-INLB value
(1.75) ~1.7x above it, while time-aggregated summaries (2.8–3.5 1/s) overshoot it by 2–3.5x. The rise is
consistent with progressive model misspecification: the biology workflow holds imaging fixed, so
cumulative photobleaching — molecules disappearing — is absorbed by the parameter best able to
mimic it, which is dissociation. Coherently with that reading, the kappa_OFF rise is *larger* in MET-FAB, whose
measured bleaching drift is stronger, while MET-FAB's composition stays flat — the rate drift tracks
the acquisition, the composition drift (§5.1) does not. A time-aggregated kappa_OFF on these
recordings summarizes a drifting estimate, not a constant; the early-window values are the least
contaminated, and all late-window kinetic parameters should be treated as acquisition-coupled.

**Monomer diffusivity (D_A).** 0.124 µm²/s (MET-FAB) and 0.133 µm²/s (MET-INLB) against the
published donor-only values 0.109 ± 0.068 and 0.093 ± 0.053 µm²/s [3] (mean ± SD per construct) —
inside the span of those values in both conditions, with a flat time course. This is the
workflow's cleanest externally anchored success.

## 6. Consistency with independent experiments

Two independent published measurements of the same receptor system provide direction checks
(summarized side by side with this work's values in §1.1 and §1.2; neither is unit-compatible
with a complex census, so magnitudes are not directly comparable):

- **Mobility classes** [1] (single-particle tracking, live cells, same accession as our recordings —
  values verified against the publication): relative occurrences immobile / confined / free of
  12 ± 1% / 31 ± 3% / 57 ± 3% for Fab-bound MET and 23 ± 1% / 17 ± 2% / 60 ± 1% for InlB321-bound
  MET (mean ± SEM over N = 60 cells, at 23 °C). Direction: activation roughly doubles the immobile
  share. Our immobile-dimer complex fraction rises 3.4x (18.4% → 62.6%) — same direction, larger
  magnitude, different estimand (complex census versus detection-weighted trajectory
  classification). The study reports **no receptor surface density and no monomer/dimer fractions**
  (its dimerization statements cite [2]), so it anchors mobility and diffusion only.
- **Ensemble diffusion** [1]: 0.126 ± 0.005 µm²/s for Fab-bound and 0.085 ± 0.003 µm²/s for
  InlB321-bound MET (23 °C). Our *monomer* diffusivity D_A is 0.124 µm²/s in MET-FAB — where
  monomers dominate the scene (70%), so the ensemble is monomer-like, and the agreement is direct —
  and 0.133 µm²/s in MET-INLB, where the model expresses the ensemble slowdown not as a slower
  monomer but as a composition shift toward the immobile-dimer state. The decomposition is
  consistent with the published ensemble numbers rather than in tension with them.
- **Spot stoichiometry** [2] (single-molecule intensity-distribution analysis in chemically fixed
  cells, ligand binding at 4 °C, sub-stoichiometric ligand labeling): 18% dimeric spots
  unstimulated (n = 527 spots) rising to 29% after InlB321 stimulation (n = 421). The publication
  itself states its dimer fraction "is clearly underestimated" owing to the non-stoichiometric
  labeling, so these are protocol-specific spot fractions the authors expected to underestimate —
  useful for direction, not mathematical lower bounds transferable to another experiment.
  Direction: activation increases the dimer fraction — confirmed. Magnitude: not comparable
  across protocols.
- **Detection-corrected dimer fractions** [4] (quantitative PALM of endogenously tagged
  MET-mEos4b in HEK293T, detection and labeling efficiency explicitly corrected): 5 ± 1% dimers
  at rest, 63 ± 2% after InlB (68 ± 4% among ligand-colocalized spots; 71 ± 3% after HGF).
  Direction: confirmed. Activated magnitude: 63–68% versus our model-conditional 78% —
  approximately consistent. Resting magnitude: 5 ± 1% versus our 31% — **not** in agreement;
  published resting estimates ([2], [4]) span roughly 5–18% under different cell lines, labeling
  strategies and estimands, and our resting value sits above all of them.

The **direction** of the inferred condition contrast is therefore confirmed by three published
experimental modalities ([1] mobility, [2] spot stoichiometry, [4] detection-corrected qPALM —
note all three share a laboratory lineage, and [1] shares the data itself),
and the ensemble-diffusion decomposition agrees quantitatively. Two magnitude tensions remain:
our immobile-dimer fraction (62.6% time-averaged, 71.4% first-recorded) exceeds the published
immobile trajectory share (23 ± 1%) — different estimands, but the gap is large — and our RESTING
dimer-complex fraction (31%) exceeds the published resting stoichiometric estimates (5–18%). Both
point at the immobile-dimer state as the place
where the model concentrates everything slow, bright, and persistent.
Given the embedding-level gap (§4.1) and the C-count support exceedance (§4.3), the most defensible
reading is that C functions partly as an effective state absorbing signatures (confinement,
clustering, persistent binding, unmodeled acquisition effects) that the three-species model has
nowhere else to put.

## 7. Ranked conclusions

1. **Strong.** InlB activation shifts the observable MET population from monomer-dominated toward a
   dimer-associated, low-mobility state: monomer fraction 0.31x (p = 2e-9), immobile-dimer fraction
   3.42x (p = 1.4e-9), dimer-complex fraction 0.30 → 0.78 (p = 2e-9) at cell level. The readout is
   the best-identified derived quantity (2.8 pp held-out, in-simulator point-estimate MAE — an
   in-model figure, not an experimental error bar), robust to the point-summary choice, to
   compositional-center choice, and to excluding all out-of-support posterior mass; its direction
   agrees with three published experiments [1, 2, 4] (distinct modalities, shared lab lineage).
2. **Strong (negative).** The experimental recordings are distinguishable from the synthetic
   reference (C2ST 0.999 against a 0.952 baseline; MMD permutation p at floor) — a
   prior-predictive distribution difference, not proof of support exclusion or structural
   misspecification. Absolute estimates carry an unquantified transfer risk.
3. **Moderate.** MET-FAB carries a nonzero baseline dimer-like population (~31%, first recorded
   window 32.5%) — directionally consistent with reports of preformed MET dimers, though above
   the published resting magnitudes (5 ± 1% detection-corrected qPALM [4]; 18% underestimated
   spot fraction [2]) obtained under different protocols and estimands; and total complex
   abundance is higher in MET-INLB (1.88x, p = 0.014).
4. **Moderate.** The MET-INLB composition evolves *within* the 20 s recording — the dimer-complex
   fraction falls from 87.0% to 70.2% (per-cell Spearman median −0.71, first-versus-last p = 0.0015)
   while MET-FAB stays flat (p = 0.52). The simple photobleaching artifacts tested (magnitude,
   control, and sign) do not straightforwardly account for the recording-position dependence; the
   decline is consistent with post-activation population dynamics, with biological and
   acquisition mechanisms unresolved.
5. **Model-dependent.** The allocation of the MET-INLB dimer signal predominantly to the *immobile*
   dimer state (62.6% time-averaged, 71.4% first-window) exceeds the published immobile mobility
   class [1], and the MET-INLB absolute composition carries a model-conditional bracket of 73–86%
   under defensible alternative choices (support restriction; compositional center). Describe it as
   an effective model-based composition, not a molecular census.
6. **Not supported.** A condition difference in kappa_OFF (cell-level p = 0.21); any constant-rate
   reading of kappa_OFF on these recordings (it drifts 2–7x within a recording, tracking cumulative
   photobleaching that the frozen-imaging model cannot absorb elsewhere); any statement about R_ON
   (unidentified, r = 0.04); exact absolute percentages for MET-INLB (44% of its C-count posterior
   mass lies beyond the trained support).

## 8. Limitations and outstanding validation

- **Composition coverage is unvalidated.** The 2.8 pp figure is a point-estimate error; whether the
  *posterior* of f_D covers truth at nominal rate requires joint posterior draws on the synthetic
  evaluation set (one sharded GPU evaluation run; the mechanism exists via the Experiment stage's
  posterior-draw dump).
- **The time-course attribution is open.** The simple photobleaching explanations tested
  (magnitude, control, and sign, §5.1) do not straightforwardly account for the MET-INLB
  decline's recording-position dependence; the decline is consistent with post-activation
  dynamics, but the split between dimer disassembly, internalization, and residual unmodeled
  acquisition effects is not determined by these data.
- **The prior ceiling binds.** Extending the count prior above 316 receptors per species (and
  regenerating/retraining) is required before MET-INLB absolute counts can be called calibrated;
  only 3.4% of MET-INLB's joint posterior draws fall inside the full ten-parameter trained box. The
  composition moves by at most ~5 pp under support restriction; the absolute counts are
  extrapolations.
- **Within-recording non-stationarity** (kappa_OFF drift, count drift, published-band photobleaching
  drift in the detector workflow) rules out combining a cell's ten window posteriors into a joint
  constant-parameter posterior; window-level estimates with the cell as replicate unit are the
  supportable unit of analysis.
- **The embedding gap is measured, not attributed.** The distance says the synthetic manifold does
  not contain the experimental videos; it does not say which imaging or dynamical ingredient is
  responsible.

## 9. Provenance

| artifact | content | run stamp |
|---|---|---|
| `Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Recovery/` | 10,000-video held-out recovery + posterior quantiles | 2026-08-18 |
| `Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment/` | 500 experimental windows: MAP + 1,000 joint posterior draws each | 2026-08-20 (reproduces the archived 2026-08-17 run to <=0.005 dex/window) |
| `Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Embedding_Space_Distance/` | MMD / C2ST experimental-versus-synthetic distances | 2026-08-18 |
| `Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment/temporal_dynamics/` | per-window time courses, drift statistics, pooled posteriors | 2026-08-20 |

All derived numbers in this report were recomputed from these artifacts on 2026-08-21; the
composition table was additionally verified by independent replication (exact to the printed
decimal) and by a 10,000-resample cell-level bootstrap.

## References

[1] M.-L. I. E. Harwardt, P. Young, W. M. Bleymüller, T. Meyer, C. Karathanasis, H. H. Niemann,
    M. Heilemann, M. S. Dietz, "Membrane dynamics of resting and internalin B-bound MET receptor
    tyrosine kinase studied by single-molecule tracking," *FEBS Open Bio* **7**(9):1422–1440 (2017).
    doi:10.1002/2211-5463.12285. Data: BioStudies accession S-BSST712.

[2] M. S. Dietz, D. Haße, D. M. Ferraris, A. Göhler, H. H. Niemann, M. Heilemann, "Single-molecule
    photobleaching reveals increased MET receptor dimerization upon ligand binding in intact cells,"
    *BMC Biophysics* **6**:6 (2013). doi:10.1186/2046-1682-6-6.

[3] Y. Li, M. S. Dietz, H.-D. Barth, H. H. Niemann, M. Heilemann, "Single-Molecule FRET-Tracking of
    MET Receptor Dynamics," *Small* **22**, e07115 (2026). doi:10.1002/smll.202507115.

[4] T. N. Baldering, C. Karathanasis, M.-L. I. E. Harwardt, P. Freund, M. Meurer, J. V. Rahm,
    M. Knop, M. S. Dietz, M. Heilemann, "CRISPR/Cas12a-mediated labeling of MET receptor enables
    quantitative single-molecule imaging of endogenous protein organization and dynamics,"
    *iScience* **24**(1):101895 (2021). doi:10.1016/j.isci.2020.101895.
