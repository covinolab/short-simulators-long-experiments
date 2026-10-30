# Embedding_Space_Distance diagnostics - SRM_AND_SBI_DIMER_ALP_2S_50FPS
Run: 2026-08-18 13:00:13 UTC

## Checks - 3 passed, 0 failed

| check | result | detail |
|---|---|---|
| experimental_windows_nonempty | PASS | 500 experimental windows embedded across 2 condition(s) |
| synthetic_windows_nonempty | PASS | 10000 synthetic EVAL windows embedded (10 task(s)) |
| no_nan_inf(embeddings) | PASS | clean |

## Quantitative

| metric | value | expected | meaning |
|---|---|---|---|
| PC1 max |loading| | 0.252 | - | - |
| PC1 participation ratio | 42.4 of 128 dims (a multi-dimensional combination) | - | - |
| estimator | /e/project1/chkf10/ramirezsierra1/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Estimator.npz | - | - |
| mix | natural | - | - |
| alpha | 0.05 | - | - |
| n_permutations | 1000 | - | - |
| pooled MMD (L2/cosine, secondary) | 0.585  (permutation p 0.000999) | - | - |

## Experimental-versus-synthetic embedding distance

| comparison | MMD | MMD p | C2ST acc | C2ST 95% CI | C2ST p | verdict |
|---|---|---|---|---|---|---|
| experimental (pooled) vs synthetic | 0.5843 | 0.000999 | 0.999 | [0.999, 1.000] | 2.87e-13 | gap |
| experimental MET-FAB vs synthetic | 0.5827 | 0.000999 | 0.999 | [0.999, 1.000] | 5.79e-13 | gap |
| experimental MET-INLB vs synthetic | 0.7487 | 0.000999 | 0.999 | [0.997, 1.001] | 3.88e-11 | gap |
| experimental MET-FAB vs MET-INLB | 0.621 | 0.000999 | 0.978 | [0.940, 1.016] | 8.38e-06 | gap |

*Overlap (realistic imaging) is concluded when both agree: the C2ST CI covers 0.5 (p >= 0.05) and the MMD permutation p >= 0.05. The pooled row is the primary imaging-realism result (imaging is a microscope property, not a condition); the per-condition and between-condition rows are diagnostics.*

## Group composition

| group | recordings | windows (embeddings) |
|---|---|---|
| MET-FAB | 25 | 250 |
| MET-INLB | 25 | 250 |
| synthetic EVAL | 10 task(s) | 10000 |

*Pooled experimental group composed by mix='natural'.*

## PCA variance spectrum (pooled raw embeddings)

| component | variance | cumulative |
|---|---|---|
| PC1 | 26.22% | 26.22% |
| PC2 | 14.86% | 41.08% |
| PC3 | 12.63% | 53.71% |
| PC4 | 11.29% | 65.01% |
| PC5 | 8.23% | 73.23% |
| PC6 | 7.23% | 80.46% |

*Intrinsic dimensionality of the embedding — how fast the variance concentrates; a single dominant component means a near-one-dimensional embedding.*

## PC1 vs target parameters (Spearman) - collapse driver

| parameter | key | meaning | Spearman rho | abs(rho) | p |
|---|---|---|---|---|---|
| $C_{C}$ | count_chi | abundance: initial immobile-dimer (C) count | +0.611 | 0.611 | 0.0e+00 |
| $C_{B}$ | count_bet | abundance: initial mobile-dimer (B) count | +0.567 | 0.567 | 0.0e+00 |
| $\kappa_{IMMOBILITY}$ | rate_immobility | immobilization: mobile dimer enters the immobile state (B -> C), per second | +0.169 | 0.169 | 8.2e-65 |
| $D_{A}$ | diffusivity_alp | mobility: monomer diffusion coefficient D_A (um^2/s) | +0.128 | 0.128 | 6.1e-38 |
| $\kappa_{MOBILITY}$ | rate_mobility | remobilization: immobile dimer returns to the mobile state (C -> B), per second | -0.117 | 0.117 | 4.9e-32 |
| $R_{C}$ | relative_diffusivity_chi | mobility ratio: immobile-dimer diffusivity as a fraction of D_A | -0.103 | 0.103 | 3.3e-25 |
| $C_{A}$ | count_alp | abundance: initial monomer (A) count in the simulated region | +0.076 | 0.076 | 3.7e-14 |
| $R_{B}$ | relative_diffusivity_bet | mobility ratio: mobile-dimer diffusivity as a fraction of D_A | +0.040 | 0.040 | 6.9e-05 |
| $R_{ON}$ | relative_rate_dimerization | association: monomer-monomer dimerization rate (A + A -> B) | +0.018 | 0.018 | 6.7e-02 |
| $\kappa_{OFF}$ | rate_dissociation | dissociation: mobile dimer breaks into two monomers (B -> A + A), per second | -0.013 | 0.013 | 1.9e-01 |

*Correlation of the dominant embedding axis (PC1) with each known imaging parameter of the synthetic EVAL set (meanings distilled from the parameter schema); the largest |rho| is the parameter that drives the embedding's single dominant direction.*

## What these mean

A check **PASS** means the invariant held; a **FAIL** aborts the run immediately with a located error message.

- **no_nan_inf** -- the array contains no NaN and no infinite values.

## Figures

![embedding_distance_distributions](figures/embedding_distance_distributions.png)

*Distributions of pairwise distances between video windows in the trained detector embedding, across two geometries (rows) and two panel types (columns). Columns: (a) within-group distances (each cloud to itself) show internal spread; (b) cross-group distances show how far apart groups sit. Rows: the top row is the raw embedding — the primary geometry, in the network's activation units, so its scale is arbitrary; the bottom row projects each embedding to the unit sphere, bounding the distance in [0, 2] (cosine), a check on whether the raw picture is a magnitude artifact. In either row, cross-group mass in (b) falling within the within-group range of (a) means overlap (realistic imaging); a shift to larger distances means a gap. The raw MMD is the statistic of record; the pooled MMD in the L2 geometry is a secondary diagnostic (reported below the table).*

![c2st_scores](figures/c2st_scores.png)

*Out-of-fold probability that each window is synthetic, from the C2ST classifier (every window scored by a fold that did not train on it, so the scores are honest). If experimental and synthetic are indistinguishable the classifier can only guess and all groups pile on the dotted 0.5 line; the more the synthetic scores push toward 1 and the experimental toward 0, the more separable the groups — a larger imaging gap. This is the graphical form of the C2ST accuracy (0.5 = overlap, →1 = gap).*

![inter_group_distance_matrix](figures/inter_group_distance_matrix.png)

*Mean pairwise embedding distance between and within groups: the diagonal is each group's own internal spread, the off-diagonal the distance between two groups. Read each off-diagonal cell against its row's diagonal — comparable means the groups overlap, much larger means a gap. Same arbitrary activation units as the distance distributions, so compare cells to one another, not to an absolute scale.*

![pca_scatter](figures/pca_scatter.png)

*PCA (equivalently classical MDS) of the raw embeddings — the optimal linear distance-preserving projection, deterministic unlike UMAP or t-SNE. (a) The pooled embeddings on their top two principal components, colored by group, with each axis's explained-variance fraction; when PC1 dominates, the points fall on a single curved arc (the horseshoe artifact of one-dimensional data) rather than separated blobs. (b) The distribution of each group's PC1 coordinate — the honest one-dimensional reading of where each group sits along the single real axis and how far it spreads. (c) The Shepard diagram plots projected 2-D distance against true high-dimensional distance; a linear projection can only shrink distances, so points lie on or below the identity line, and the annotated correlation states how faithfully the view preserves them. The variance-spectrum table quantifies the dimensionality; the distance-distribution and matrix figures remain the exact high-dimensional summary.*

![collapse_tracking](figures/collapse_tracking.png)

*Which imaging parameter the dominant embedding axis (PC1) encodes. (a) The absolute Spearman correlation of PC1 with each imaging parameter of the synthetic EVAL set, sorted; the tallest bar is the parameter driving the near-one-dimensional collapse. (b) PC1 against that top parameter, labeled with the signed Spearman rho. Rank correlation, so it is unaffected by the log or linear storage of the parameters.*
