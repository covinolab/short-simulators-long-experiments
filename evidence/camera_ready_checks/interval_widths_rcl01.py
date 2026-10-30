"""Posterior interval widths for f_D from the saved audit draws (camera-ready Appendix F).

Runs on rcl01, where the 500 per-setting result files of the horizon-audit cohort live
(read-only data). Each file holds 20 rows (10 continuous windows, ``which == 0``, and 10 reset
clips, ``which == 1``) with ``draws`` of shape (20, 1000, 10) in log10. f_D is formed inside each
joint draw from the three count coordinates, so the interval widths are those of the paper's
own summary. Bootstrap: numpy default_rng(1), 2,000 resamples over settings, percentile 2.5/97.5.
"""
import glob
import time

import numpy as np

D = ("/media/rcl_fias/RCL_FIAS_A/MARS_Data_Bank/Projects/RCL_Agent_Projects/srm-and-sbi-dimer-alp"
     "/Data_Bank/Posit/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit")
main = np.load(D + "/SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit.npz", allow_pickle=True)
files = sorted(glob.glob(D + "/cohort/result_*.npz"))
idx_file = {int(f.split("_")[-1].split(".")[0]): f for f in files}
print("main cohort", str(main["cohort_id"]), "| result files", len(files))

ci = [0, 1, 2]
t0 = time.time()
w90_c, w50_c, w90_r, w50_r = [], [], [], []
for k, ti in enumerate(main["trajectory_indices"]):
    f = idx_file.get(int(ti))
    if f is None:
        continue
    d = np.load(f, allow_pickle=True)
    assert np.allclose(d["theta_log10"], main["theta_log10"][k])
    draws = 10.0 ** np.asarray(d["draws"])[..., ci]
    fd = (draws[..., 1] + draws[..., 2]) / draws.sum(-1)
    q = np.percentile(fd, [5, 25, 75, 95], axis=-1)
    w90, w50 = q[3] - q[0], q[2] - q[1]
    wh = np.asarray(d["which"]); ps = np.asarray(d["position"])
    c = wh == 0; r = wh == 1
    a = np.full(10, np.nan); b = np.full(10, np.nan)
    for p_, x, y in zip(ps[c], w90[c], w50[c]):
        a[int(p_)] = x; b[int(p_)] = y
    w90_c.append(a); w50_c.append(b); w90_r.append(w90[r].mean()); w50_r.append(w50[r].mean())
w90_c, w50_c, w90_r, w50_r = map(np.array, (w90_c, w50_c, w90_r, w50_r))
print(f"settings used {len(w90_r)}; {time.time() - t0:.0f} s")
print("f_D 90% width (pp), continuous by window 1..10, mean over settings:", np.round(np.nanmean(w90_c, 0) * 100, 3))
print("f_D 90% width (pp), reset mean over settings and clips: {:.4f}".format(np.nanmean(w90_r) * 100))
print("f_D 50% width (pp), continuous by window 1..10:", np.round(np.nanmean(w50_c, 0) * 100, 3))
print("f_D 50% width (pp), reset mean: {:.4f}".format(np.nanmean(w50_r) * 100))

rng = np.random.default_rng(1)
N_BOOT = 2000
def boot(x):
    x = x[np.isfinite(x)]
    bs = np.array([rng.choice(x, len(x)).mean() for _ in range(N_BOOT)])
    return x.mean() * 100, np.percentile(bs, 2.5) * 100, np.percentile(bs, 97.5) * 100
print(f"bootstrap: default_rng(1), {N_BOOT} resamples over settings, 95% percentile interval")
for lab, x in (("90% cont w1", w90_c[:, 0]), ("90% cont w10", w90_c[:, 9]), ("90% reset", w90_r),
               ("50% cont w1", w50_c[:, 0]), ("50% cont w10", w50_c[:, 9]), ("50% reset", w50_r),
               ("90% paired change w10 - w1", w90_c[:, 9] - w90_c[:, 0]),
               ("50% paired change w10 - w1", w50_c[:, 9] - w50_c[:, 0])):
    m, lo, hi = boot(x)
    print("  %-28s mean %7.3f pp [%7.3f, %7.3f]" % (lab, m, lo, hi))
