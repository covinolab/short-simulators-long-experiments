# Short simulators, long experiments

Code, persisted results, and reproduction scripts for the paper

> **Short Simulators, Long Experiments: A Controlled Audit of Horizon Mismatch in Simulation-Based Inference for Live-Cell Microscopy**
> Michael Alexander Ramirez Sierra and Roberto Covino
> NeurIPS 2026 Workshop on Sim2Science: ML with Imperfect Scientific Models

The paper audits an unstated assumption of simulation-based inference for single-particle-tracking
microscopy: an estimator trained on short, independently initialized simulated clips is deployed on
consecutive windows of long experimental recordings. Inside the simulator, where the truth is known,
the audit compares the two deployment modes on 500 matched parameter settings and grades each
conclusion of an earlier experimental analysis against the measured effect.

The repository regenerates all manuscript figures and recomputes the supplied numerical checks from
persisted results. Recomputing the full audit analysis and the posterior interval-width statistics
requires the per-setting files, available from the authors on request. The video corpora and trained
estimator are not included (see *What is not included*).

## Layout

```
paper/        camera-ready LaTeX source, bibliography, NeurIPS checklist, style file, figure PDFs
figures/      make_paper_figures.py builds the four figures and census_transfer.md from evidence/
evidence/     persisted results (verbatim archive copies, sha256 in MANIFEST.md) and check scripts
  horizon_audit/        audit arrays, cohort file, 10,000-video recovery, machine report, findings
  census/               experimental inference results (MET recordings), reports, embedding-distance run
  code/                 copies of the audit kernel, engine, entry point and method companion
  camera_ready_checks/  scripts and saved outputs behind the appendix numbers (see its README)
code/         srm-and-sbi-dimer-alp at the study commit, with one helper script omitted (see PROVENANCE.md)
```

## What you can reproduce from this repository

With the minimal environment (`environment.yml`: Python, NumPy, Matplotlib):

```bash
conda env create -f environment.yml && conda activate short-simulators-long-experiments
python figures/make_paper_figures.py                      # Figures 1-4 (pdf+png) and figures/census_transfer.md
python evidence/camera_ready_checks/local_checks.py       # Appendix A/E/G numbers and Figure 4b values
```

- **Every figure** (Figures 1 to 4) is regenerated from `evidence/` by `figures/make_paper_figures.py`.
- **The supplied numerical checks** (`evidence/camera_ready_checks/local_checks.py`) recompute the Appendix
  A, E and G numbers and the Figure 4b values from `evidence/`. The remaining table and appendix numbers
  trace to `evidence/horizon_audit/report.md` (the machine report of the audit) and to
  `figures/census_transfer.md`; `evidence/horizon_audit/findings.md` is the narrative record of the analysis.
- **The paper** builds with `cd paper && tectonic main.tex` (or `pdflatex` + `bibtex`).
- **Not recomputable from this repository alone:** the audit's analysis phase
  (`SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py --phase analyze` in `code/`) and the posterior interval-width
  statistics of Appendix F (`evidence/camera_ready_checks/interval_widths_rcl01.py`) both read the 500
  per-setting result files (601 MB, posterior draws included), which are not bundled and are available
  from the authors on request. The saved outputs of both calculations are included; they document the
  calculations but do not replace the data needed to rerun them.

## What is not included, and how to obtain it

| item | status |
|---|---|
| 2 s simulated video corpora (200,000 TRAIN, 50,000 TEST, 25,000 EVAL videos; 662 GiB TRAIN+TEST) | not bundled; regenerable with `code/` on an HPC system (paper Appendix H gives the measured resources) |
| trained estimator checkpoint | not released |
| horizon-audit per-setting files (videos not kept; posteriors and truths kept, 601 MB) | available on request |
| experimental MET recordings | public, BioStudies accession S-BSST712 (Baldering et al.; see the paper's references) |

Re-running corpus generation, training, or the audit's generation and inference phases requires the
full environment in `code/srm-and-sbi-dimer-alp/env_snapshots/README.md` (ReaDDy 2.0.14, PyTorch, sbi
0.26.1) and the compute described in the paper's Appendix H.

## Notes on the numbers

- Bootstrap intervals in the paper come from `evidence/camera_ready_checks/local_checks.py` (seed
  recorded in its README). `figures/census_transfer.md` recomputes the same means with the figure
  script's own seed; its interval endpoints may differ from the paper's by up to 0.1 pp.
- The evidence directory and its manifest were assembled for the paper's submission and extended for the
  camera-ready version; `evidence/MANIFEST.md` says which files are archive copies and which are derived checks.

## Citation and license

See `CITATION.cff` for the authors and their institutions. The repository is released under the MIT
License (`LICENSE`), with the copyright notice of the source code repository preserved; the code
snapshot carries the same notice in `code/srm-and-sbi-dimer-alp/LICENSE`.
