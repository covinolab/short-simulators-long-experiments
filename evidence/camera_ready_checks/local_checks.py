"""Camera-ready numerical checks computed from the evidence directory alone.

Run from the paper repository root:
    python evidence/camera_ready_checks/local_checks.py > evidence/camera_ready_checks/local_checks.out

Checks (all appendix statements added for the camera-ready version):
  1. f_D strata of Appendix A by the true composition at the start of window 10 (417/81/2),
     and the number of settings that start in the highest interval (first-frame composition).
  2. Signed f_D shift (continuous minus reset mean, window 10 and recording mean) by stratum
     and by initial-composition label subset (Appendix A table, Appendix E reconciliation).
  3. Held-out recovery error with optimized point estimates versus marginal posterior medians
     (Appendix G tolerance correspondence), and the primary audit verdicts under either value.
  4. Experimental per-window time course of the inferred dimer-complex fraction (Figure 4b).
Bootstrap: numpy default_rng(20260826), 2,000 resamples over settings, percentile 2.5/97.5.
"""
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EV = HERE.parent
N_BOOT = 2000
rng = np.random.default_rng(20260826)


def boot(x):
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    bs = np.array([rng.choice(x, len(x)).mean() for _ in range(N_BOOT)])
    return x.mean(), np.percentile(bs, 2.5), np.percentile(bs, 97.5), len(x)


def fmt(t, unit="pp", scale=1.0, nd=2):
    m, lo, hi, n = t
    return f"{m*scale:+.{nd}f} {unit} [{lo*scale:+.{nd}f}, {hi*scale:+.{nd}f}] (n={n})"


a = np.load(EV / "horizon_audit" / "SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit.npz", allow_pickle=True)
keys = list(a["parameter_keys"])
fd_c, fd_r = a["fd_cont"], a["fd_reset"]
ts_c, ts_r = a["fd_true_start_cont"], a["fd_true_start_reset"]
signed = (fd_c - ts_c) - np.nanmean(fd_r - ts_r, axis=1, keepdims=True)   # (500, 10), fractions
th = a["theta_log10"]
cnt = 10.0 ** th[:, :3]
label = (cnt[:, 1] + cnt[:, 2]) / cnt.sum(1)
w1, w10 = ts_c[:, 0], ts_c[:, 9]

print("== 1. Strata and start counts (true composition, strata [0,0.2), [0.2,0.8), [0.8,1]) ==")
print("window-10 start: n =", int((w10 < 0.2).sum()), int(((w10 >= 0.2) & (w10 < 0.8)).sum()), int((w10 >= 0.8).sum()))
print("first-frame start in [0.8,1]:", int((w1 >= 0.8).sum()), "| strictly above 0.8:", int((w1 > 0.8).sum()))
print("initial LABEL (theta counts) strictly above 0.8:", int((label > 0.8).sum()),
      "| rounded counts:", int(((np.round(cnt)[:, 1] + np.round(cnt)[:, 2]) / np.round(cnt).sum(1) > 0.8).sum()))

print("\n== 2. Signed f_D shift, continuous minus reset mean (pp) ==")
for name, m in [("stratum w10 [0,0.2)", w10 < 0.2), ("stratum w10 [0.2,0.8)", (w10 >= 0.2) & (w10 < 0.8)),
                ("stratum w10 [0.8,1]", w10 >= 0.8), ("label f_D < 0.4 (resting-like)", label < 0.4),
                ("label f_D > 0.7 (activated-like)", label > 0.7), ("all", np.ones(500, bool))]:
    print(f"{name:34s} window 10: {fmt(boot(signed[m, 9]), scale=100)} | recording mean: "
          f"{fmt(boot(np.nanmean(signed[m], axis=1)), scale=100)}")
print("continuous error alone at window 10 by stratum (pp, no reset baseline):",
      [round(float(np.nanmean((fd_c - ts_c)[m, 9]) * 100), 2) for m in (w10 < 0.2, (w10 >= 0.2) & (w10 < 0.8), w10 >= 0.8)])

print("\n== 3. Tolerances: optimized point estimate vs marginal median; verdict robustness ==")
r = np.load(EV / "horizon_audit" / "SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Recovery.npz", allow_pickle=True)
rkeys = list(r["parameter_keys"]) if "parameter_keys" in r.files else keys
true, inf = r["true_log10"], r["inferred_log10"]
pq = r["posterior_quantiles"]                      # (10000, 10, 5): levels 5, 25, 50, 75, 95
med = pq[:, :, 2]                                   # marginal posterior median
tol = {}
for k in ("diffusivity_alp", "rate_dissociation"):
    j = rkeys.index(k)
    mae_opt = np.abs(inf[:, j] - true[:, j]).mean(); mae_med = np.abs(med[:, j] - true[:, j]).mean()
    tol[k] = (mae_opt, mae_med)
    print(f"{k:18s} MAE optimized {mae_opt:.4f} dex (x{10**mae_opt:.3f}) | median {mae_med:.4f} dex (x{10**mae_med:.3f})")
cont_err, reset_err, delta_abs = a["cont_err"], a["reset_err"], a["delta_abs"]
for k in ("diffusivity_alp", "rate_dissociation"):
    j = keys.index(k)
    w = boot(delta_abs[:, 9, j])
    rec_c = np.abs(np.nanmean(cont_err[:, :, j], axis=1)); rec_r = np.abs(np.nanmean(reset_err[:, :, j], axis=1))
    rc = boot(rec_c - rec_r)
    for lab, t in (("window 10", w), ("recording", rc)):
        verd = {}
        for tn, tv in zip(("optimized", "median"), tol[k]):
            lo, hi = t[1], t[2]
            verd[tn] = "degraded" if lo > tv else ("equivalent" if (lo > -tv and hi < tv) else "inconclusive")
        print(f"{k:18s} {lab:10s} contrast {fmt(t, unit='dex', nd=4)}  -> {verd}")
    print(f"{'':18s} recording-level errors: reset {rec_r.mean():.3f} cont {rec_c.mean():.3f} dex")

print("\n== 4. Experimental per-window time course (in-draw mean f_D; mean and cell-level s.e.m., %) ==")
d = np.load(EV / "census" / "MAP_Experiment" / "SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment.npz", allow_pickle=True)
c = 10.0 ** d["posterior_samples_cloud"].astype(float)[..., :3]
fd = ((c[..., 1] + c[..., 2]) / c.sum(-1)).mean(-1)
for k, name in ((0, "resting (ALP = MET-FAB)"), (1, "activated (BET = MET-INLB)")):
    m = d["kind_index"] == k
    cells = np.unique(d["cell"][m])
    per = np.array([[fd[m & (d["cell"] == cell) & (d["chunk"] == ch)].mean() for ch in range(10)] for cell in cells])
    mean_w = per.mean(0) * 100; sem_w = per.std(0, ddof=1) / np.sqrt(per.shape[0]) * 100
    cellmean = per.mean(1) * 100
    print(f"{name:28s} cells {len(cells)} | condition mean {cellmean.mean():.1f} +/- {cellmean.std(ddof=1)/np.sqrt(len(cells)):.1f} "
          f"| window 1 {mean_w[0]:.1f} +/- {sem_w[0]:.1f} | window 10 {mean_w[9]:.1f} +/- {sem_w[9]:.1f}")
    print("   by window:", np.round(mean_w, 1))
