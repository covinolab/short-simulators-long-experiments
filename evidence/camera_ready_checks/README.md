# Camera-ready numerical checks

Scripts and outputs behind the statements added for the camera-ready version (2026-10-29).
Both scripts read persisted artifacts only; no simulation or inference was run.

| file | what it computes | runs on |
|---|---|---|
| `local_checks.py` / `local_checks.out` | Appendix A strata by window-10 start truth (417/81/2) and the first-frame start count (230 in [0.8, 1]; 226 strictly above 0.8); signed f_D shifts by stratum (+7.0 / −7.1 / −30.2 pp at window 10) and by initial-label subset (+5.6 / +3.5 pp at window 10; +3.4 / +1.9 pp recording means); held-out recovery error with optimized point estimates vs marginal medians (D_A 0.0227 / 0.0222 dex, κ_OFF 0.1773 / 0.1788 dex) and the primary verdicts under either tolerance (unchanged at both reporting levels); experimental per-window time course (31.4 ± 2.0, 78.2 ± 3.7; 87.0 → 70.2) | this directory (`evidence/`) |
| `interval_widths_rcl01.py` / `interval_widths_rcl01.out` | central 90% and 50% posterior interval widths for f_D from the 500 per-setting draw files of the audit cohort (90%: 15.13 → 13.61 pp continuous, 15.25 pp reset; paired change −1.53 pp [−2.12, −0.93]; 50%: 6.06 → 5.53, reset 6.10) | rcl01, read-only data bank path given in the script |

Bootstrap settings: percentile 95% intervals over settings, 2,000 resamples; `numpy.random.default_rng(20260826)`
for `local_checks.py` and `default_rng(1)` for `interval_widths_rcl01.py`, resampling in the order printed.
The intervals reproduce with the recorded seeds and execution order; other seeds give small endpoint differences. The paper quotes one decimal.

Definitions: f_D is formed inside each joint posterior draw from the three count coordinates and summarized
by the in-draw mean; the signed shift is (continuous estimate − window-start truth) minus the mean of the same
quantity over the ten reset clips of the same setting; strata use the true composition at the start of the
window named, with intervals [0, 0.2), [0.2, 0.8), [0.8, 1]; the transfer subsets use the initial composition
label formed from the drawn theta counts.
