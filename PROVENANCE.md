# Provenance

## Code

`code/srm-and-sbi-dimer-alp/` is a snapshot of the public repository
<https://github.com/srm-and-sbi/srm-and-sbi-dimer-alp> at the commit that produced the horizon
audit reported in the paper:

| item | value |
|---|---|
| commit | `2d24491a9d384d6313e4fc1c39dfb14e694e0387` (2026-08-26, "Audit the recording summary, not only the individual window") |
| package version at that commit | 0.4.20 (`pyproject.toml`) |
| later history | the repository was frozen at v0.4.23 (`d78b2f2b`, 2026-09-02); no result in the paper depends on commits after `2d24491` |
| omitted from the snapshot | `Script_Bank/HPC/SRM_AND_SBI_DIMER_ALP_Fleet_Sync.sh`, a machine-synchronization helper with no role in the reported study; every other file is byte-identical to the commit |

To verify the snapshot against the public repository:

```bash
git clone https://github.com/srm-and-sbi/srm-and-sbi-dimer-alp.git
cd srm-and-sbi-dimer-alp && git archive --format=tar --prefix=srm-and-sbi-dimer-alp/ 2d24491 | tar -x -C /tmp
diff -r /tmp/srm-and-sbi-dimer-alp <this repository>/code/srm-and-sbi-dimer-alp
# expected output: only the omitted file, "Only in /tmp/srm-and-sbi-dimer-alp/Script_Bank/HPC: SRM_AND_SBI_DIMER_ALP_Fleet_Sync.sh"
```

The audit code the paper describes is `srm_and_sbi_dimer_alp/horizon_audit.py` (kernel),
`srm_and_sbi_dimer_alp/horizon_audit_runner.py` (engine) and
`Script_Bank/Analysis/SRM_AND_SBI_DIMER_ALP_Horizon_Audit.py` with its method companion `.md`.
Copies of these four files also sit in `evidence/code/` with sha256 digests in `evidence/MANIFEST.md`.

## Results

Every persisted result under `evidence/` is a verbatim copy of an archive file; `evidence/MANIFEST.md`
records each file's canonical path and sha256 digest. The horizon-audit cohort is `936727a9bd6b`
(lineage `0fd0220c2a38`), 500 completed matched parameter settings. The 2 s estimator is the one
described in the paper's Appendix G; its checkpoint is not part of this release.

## Where the computations ran

| computation | system |
|---|---|
| 2 s corpus generation (TRAIN/TEST/EVAL) | CPU array nodes of the Goethe-NHR cluster and JUWELS |
| estimator training, 10,000-video held-out recovery | AMD MI210 GPU nodes of the Goethe-NHR cluster |
| horizon-audit generation and posterior sampling | a local workstation with one RTX 6000 Ada 48 GB GPU |
| horizon-audit analysis, figures, camera-ready checks | local workstations |

The paper's Appendix H gives the measured resources and their qualifications.
