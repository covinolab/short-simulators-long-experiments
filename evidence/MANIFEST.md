# Evidence manifest

Every file in `evidence/` is a **verbatim copy**, refreshed 2026-08-26; the five census source
artifacts were added 2026-08-29. The canonical originals
are the paths in the last column; this directory exists so the paper can be reviewed without
mounting the external data reserve or hunting across repositories. Nothing here is edited by
hand -- to refresh, re-copy from the source. All 25 files were verified byte-identical
to their sources when each was added.

The census section's own provenance table names four artifacts. Three of them - the experimental
posterior, its temporal-dynamics summary, and the embedding-distance run - were added on 2026-08-29
so that every census number can be recomputed from this directory alone; the fourth, `MAP_Recovery`,
was already present under `horizon_audit/`. Diagnostic figures and job logs from those runs stay in
the archive: they are regenerable from the `.npz` and are not needed to check a number.

**Canonical code repository:** `/home/mars-fias/Documents/Projects/RCL_Agent_Projects/srm-and-sbi/srm-and-sbi-dimer-alp` at commit `2d24491` (branch `main`).
The `evidence/code/*.py` files are copies of that commit; the repository is authoritative if they
ever disagree, and the sha256 column lets you check.

**Cohort identity:** `936727a9bd6b`, lineage `0fd0220c2a38` (the parent cohort, before two
unrealizable draws were topped up -- see `horizon_audit/findings.md` section 3b). **500 completed
trajectories.** Every artifact the audit consumed carried a stamp in that lineage and had its
theta row re-checked exactly; mismatches abort the run.

| file | size | sha256 (first 16) | canonical source |
|---|---|---|---|
| `census/figures/S1_census_two_ways.png` | 139,823 B | `a64f5dcde351a528` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/figures/S1_census_two_ways.png` |
| `census/figures/S2_external_anchors.png` | 144,049 B | `cef825b9c75bfcf4` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/figures/S2_external_anchors.png` |
| `census/figures/S3_counting_parts_vs_whole.png` | 183,696 B | `da9c518eff803cc7` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/figures/S3_counting_parts_vs_whole.png` |
| `census/figures/S4_scene_abundance.png` | 65,764 B | `b5876c14f9902d67` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/figures/S4_scene_abundance.png` |
| `census/figures/S5_conclusions_ladder.png` | 219,572 B | `3d60dabfed8846a5` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/figures/S5_conclusions_ladder.png` |
| `census/progress_summary.md` | 22,637 B | `fa6f80f867d3c4db` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/progress_summary.md` |
| `census/report.md` | 31,975 B | `f8f18366fa8e9909` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Experimental_Synthetic_Comparison/report.md` |
| `census/MAP_Experiment/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment.npz` | 18,558,291 B | `a20a8b4f6c26afaa` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment.npz` |
| `census/MAP_Experiment/report.md` | 6,744 B | `0e5b9ccbb805e9b7` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment/report.md` |
| `census/MAP_Experiment/temporal_dynamics/report.md` | 17,143 B | `4a01630462178090` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment/temporal_dynamics/report.md` |
| `census/Embedding_Space_Distance/report.md` | 7,774 B | `b1622af8ac53b5df` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Embedding_Space_Distance/report.md` |
| `census/Embedding_Space_Distance/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Embedding_Space_Distance_1405186.out` | 6,562 B | `1f2f2f728a7f3dec` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Embedding_Space_Distance/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Embedding_Space_Distance_1405186.out` |
| `code/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.md` | 12,798 B | `2ecb74b5b2aa7cc4` | `/home/mars-fias/Documents/Projects/RCL_Agent_Projects/srm-and-sbi/srm-and-sbi-dimer-alp/Script_Bank/Analysis/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.md` |
| `code/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py` | 4,888 B | `19db5de3fa4bc900` | `/home/mars-fias/Documents/Projects/RCL_Agent_Projects/srm-and-sbi/srm-and-sbi-dimer-alp/Script_Bank/Analysis/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py` |
| `code/horizon_audit.py` | 20,332 B | `ff5f5787d33040ae` | `/home/mars-fias/Documents/Projects/RCL_Agent_Projects/srm-and-sbi/srm-and-sbi-dimer-alp/srm_and_sbi_dimer_alp/horizon_audit.py` |
| `code/horizon_audit_runner.py` | 91,051 B | `e747e18ef96bd1d6` | `/home/mars-fias/Documents/Projects/RCL_Agent_Projects/srm-and-sbi/srm-and-sbi-dimer-alp/srm_and_sbi_dimer_alp/horizon_audit_runner.py` |
| `horizon_audit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit.npz` | 1,518,622 B | `a7fa92e3bb71f7d6` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit.npz` |
| `horizon_audit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Recovery.npz` | 3,701,650 B | `561efe808e464cb5` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Recovery/SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Recovery.npz` |
| `horizon_audit/cohort_theta.npz` | 40,804 B | `cdd9f0a211ddc893` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/cohort_theta.npz` |
| `horizon_audit/figures/coverage_vs_position.png` | 108,230 B | `f5fb49d66757ca24` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/figures/coverage_vs_position.png` |
| `horizon_audit/figures/dynamic_state_f_D.png` | 406,062 B | `91f715b8ecfba1bc` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/figures/dynamic_state_f_D.png` |
| `horizon_audit/figures/error_vs_position.png` | 325,753 B | `96e68a1afa335b7d` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/figures/error_vs_position.png` |
| `horizon_audit/figures/flow_mass_outside_box.png` | 73,701 B | `0cf447961b78d83d` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/figures/flow_mass_outside_box.png` |
| `horizon_audit/findings.md` | 40,922 B | `cf8118c22644b212` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/findings.md` |
| `horizon_audit/report.md` | 10,441 B | `40198a3fa049f5f8` | `/media/mars-fias/MARS_Data_Reserve_0/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit/report.md` |

## Regenerating

The manuscript's figures are built from the two `.npz` files above:

```
python figures/make_paper_figures.py        # writes figures/fig{1,2,3}*.pdf
```

The audit results themselves come from the code repository, with the environment
`SRM_AND_SBI_ENVY_V0`:

```
MACHINE_PROFILE=<profile> python Script_Bank/Analysis/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py \
    --total-time-seconds 2.0 --phase selftest    # 8 check families, seconds, no data needed
MACHINE_PROFILE=<profile> python Script_Bank/Analysis/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py \
    --total-time-seconds 2.0 --phase analyze     # rewrites report.md, figures and the arrays
```

`--phase analyze` needs the per-theta result files (500 x 2, ~GB, not copied here) and the
recovery artifact that calibrates the stratified margins. `--phase selftest` needs nothing and is
the fastest way to check that the decision-critical logic behaves as documented.

**Camera-ready checks (2026-10-29):** `camera_ready_checks/` holds the two scripts and their outputs
behind the appendix statements added for the camera-ready version (interval widths, strata and subset
shifts, tolerance correspondence, experimental time course). They are derived checks, not copies of
archive files; see `camera_ready_checks/README.md`.
