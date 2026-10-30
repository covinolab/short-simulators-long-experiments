"""Generate the manuscript's four figures from the persisted audit arrays.

Every number drawn here comes from files listed in ``evidence/MANIFEST.md`` -- no figure in this
paper is produced from a scratch calculation. Run from the paper directory:

    python figures/make_paper_figures.py

Writes ``figures/fig1_design.pdf``, ``fig2_result.pdf``, ``fig3_payoff.pdf`` and
``figS1_census.pdf`` (vector, for LaTeX) plus matching .png previews, and
``figures/census_transfer.md``: the simulator-to-experiment sensitivity numbers that Section 4.3,
Figure 3 and Figure S1 quote, computed here from the same persisted arrays so that they trace to
the 500-trajectory cohort rather than to an earlier hand calculation.

DESIGN NOTES (see WRITING_GUIDELINES.md section 7 and the data-visualization method):
* Colors are the reference categorical palette, slots 1 and 2, unchanged: blue = the RESET arm
  (training condition), orange = the CONTINUOUS arm (deployment condition). The mapping is fixed
  across all three figures, so a color always means the same arm. Slots 1-3 of that palette are
  documented as clearing the all-pairs colorblind gates on a light surface.
* Identity is never carried by color alone: every arm is also direct-labeled or legended, and the
  two arms differ in mark type (band vs line with markers).
* One axis per panel; no dual scales. Where quantities with different units must share a panel
  they are expressed in units of their OWN prespecified margin, which is a common base rather
  than a second axis.
* The reset arm has NO window position -- its clips are independent replicates -- so it is drawn
  as a horizontal band (mean and 95% interval), not as a line across positions. Drawing it as a
  line would imply a trend that the design cannot produce.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = Path(__file__).resolve().parent
EV = HERE.parent / "evidence" / "horizon_audit"
OUT = HERE

# ---- palette (reference categorical slots 1 and 2, light mode) -----------------------------
RESET = "#2a78d6"      # slot 1, blue  -- training condition
CONT = "#eb6834"       # slot 2, orange -- deployment condition
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#d8d7d2"
SURF = "#ffffff"

plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF,
    "font.size": 8.8, "axes.labelsize": 8.8, "axes.titlesize": 9.0,
    "xtick.labelsize": 7.8, "ytick.labelsize": 7.8, "legend.fontsize": 7.2,
    "text.color": INK, "axes.labelcolor": INK, "axes.edgecolor": GRID,
    "xtick.color": INK2, "ytick.color": INK2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.5, "grid.alpha": 0.7,
    "lines.linewidth": 1.6, "lines.markersize": 3.4,
    "legend.frameon": False, "figure.dpi": 200,
    "pdf.fonttype": 42, "ps.fonttype": 42,
})

MARGINS = {"f_D": 2.8, "rate_dissociation": 0.177, "diffusivity_alp": 0.023}


def load():
    d = np.load(EV / "SRM_AND_SBI_DIMER_ALP_2S_50FPS_Horizon_Audit.npz", allow_pickle=True)
    return {k: d[k] for k in d.files}


def boot(values, n_boot=2000, seed=20260826):
    """Bootstrap mean and 95% interval over trajectories (axis 0) -- the independent unit."""
    values = np.asarray(values, dtype=float)
    rng = np.random.default_rng(seed)
    n = values.shape[0]
    stats = np.stack([np.nanmean(values[rng.integers(0, n, n)], axis=0) for _ in range(n_boot)])
    return (np.nanmean(values, axis=0),
            np.nanpercentile(stats, 2.5, axis=0), np.nanpercentile(stats, 97.5, axis=0))


def band(ax, lo, hi, color, label):
    """The reset arm: a horizontal band, because independent clips have no window position."""
    ax.axhspan(lo, hi, color=color, alpha=0.16, lw=0, zorder=1)
    ax.axhline((lo + hi) / 2, color=color, lw=1.3, zorder=2, label=label)


# =============================================================================
# Figure 1 -- the design
# =============================================================================

def figure_design():
    fig, ax = plt.subplots(figsize=(5.5, 1.06))
    ax.set_xlim(-0.15, 12.6); ax.set_ylim(0.02, 3.02); ax.axis("off")

    def clip(x, y, w, h, color):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=color, alpha=0.28,
                               edgecolor=color, lw=0.9, joinstyle="round"))

    # --- training condition: ten independently initialized clips --------------------------
    # Label and descriptor are stacked, never side by side: side-by-side placement depends on
    # rendered text width and collided at this figure size.
    # Typography: one heading size (bold) and one label size for every other text element.
    HEAD, LAB = 7.4, 6.8
    ax.text(0, 2.91, "RESET ARM  (independent resets, training-like)", color=RESET,
            fontsize=HEAD, weight="bold", va="center")
    ax.text(0, 2.58, "ten independent 2 s clips, each started from the training initialization",
            color=INK2, fontsize=LAB, va="center")
    for i in range(10):
        x = i * 1.00
        clip(x, 2.00, 0.80, 0.40, RESET)
        ax.plot([x + 0.10], [2.20], marker="o", ms=2.8, color=RESET, zorder=3)
    ax.text(10.18, 2.20, "10 fresh starts", fontsize=LAB, color=RESET, va="center")

    # --- deployment condition: one recording, sliced ---------------------------------------
    ax.text(0, 1.57, "CONTINUOUS ARM  (one trajectory, consecutive windows)", color=CONT,
            fontsize=HEAD, weight="bold", va="center")
    ax.text(0, 1.24, "one 20 s simulation, cut into ten consecutive 2 s windows",
            color=INK2, fontsize=LAB, va="center")
    for i in range(10):
        clip(i * 1.00, 0.66, 0.94, 0.40, CONT)
    for i in range(1, 10):                       # inheritance arrows AT the window boundaries
        xb = i * 1.00
        ax.add_patch(FancyArrowPatch((xb - 0.20, 0.86), (xb + 0.14, 0.86),
                                     arrowstyle="-|>", mutation_scale=6.0,
                                     color=CONT, lw=0.9, shrinkA=0, shrinkB=0, zorder=3))
    ax.plot([0.10], [0.86], marker="o", ms=2.8, color=CONT, zorder=3)
    ax.text(10.18, 0.86, "1 fresh start,\nthen inheritance", fontsize=LAB, color=CONT,
            va="center")
    ax.text(0, 0.24, "Only the first window starts from the training initialization. Every later "
                     "one inherits composition\ndrift, spatial correlations built by the dynamics, "
                     "and photophysical history.",
            fontsize=LAB, color=INK, ha="left", va="center", linespacing=1.5)
    fig.tight_layout(pad=0.18)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig1_design.{ext}", bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# Figure 2 -- the result
# =============================================================================

def figure_result(d):
    keys = list(d["parameter_keys"])
    i_koff, i_da = keys.index("rate_dissociation"), keys.index("diffusivity_alp")
    fd_err_cont = np.abs(100 * (d["fd_cont"] - d["fd_true_start_cont"]))
    fd_err_reset = np.abs(100 * (d["fd_reset"] - d["fd_true_start_reset"]))
    pos = np.arange(1, 11)

    fig, axes = plt.subplots(1, 3, figsize=(5.5, 1.60),
                             gridspec_kw={"width_ratios": [1.18, 0.74, 1.08]})

    # ---- (a) accuracy, each quantity relative to its OWN training-condition error ---------
    # A ratio, not a margin comparison: the margin test is on the PAIRED ADDED error and lives
    # in the tables. Plotting total error against a margin line would invite the wrong read.
    ax = axes[0]
    series = [(fd_err_cont, fd_err_reset, "dimer-complex fraction", "o", CONT),
              (np.abs(d["cont_err"][:, :, i_koff]), np.abs(d["reset_err"][:, :, i_koff]),
               "unpairing rate", "s", "#b8471c"),
              (np.abs(d["cont_err"][:, :, i_da]), np.abs(d["reset_err"][:, :, i_da]),
               "diffusion coeff.", "^", "#f2a884")]
    for cont_e, reset_e, lab, mk, col in series:
        base = float(np.nanmean(reset_e))
        mean, lo, hi = boot(cont_e / base)
        ax.plot(pos, mean, marker=mk, color=col, label=lab, clip_on=False)
        ax.fill_between(pos, lo, hi, color=col, alpha=0.15, lw=0)
    ax.axhline(1.0, color=INK2, lw=1.0, ls=(0, (4, 2.5)))
    ax.set_ylim(0.78, 4.3); ax.set_xlim(1, 10)
    ax.set_xticks([1, 4, 7, 10]); ax.set_yticks([1, 2, 3])
    ax.set_ylabel("typical error\n(\u00d7 its own baseline)")
    ax.set_xlabel("window position")
    ax.set_title("(a) Error grows\nwith window position", loc="left")
    ax.legend(loc="upper left", handlelength=0.8, labelspacing=0.2, borderpad=0.1, fontsize=7.0)

    # ---- (b) direction: the horizon-specific signed shift, by true unpairing rate ---------
    ax = axes[1]
    theta = d["theta_log10"]
    edges = np.linspace(-1.0, 1.0, 4)                        # prior bounds, log10 1/s
    reset_base = np.nanmean(d["reset_err"][:, :, i_koff], axis=1)
    names = ["slow", "mid", "fast"]
    xs, shifts, los, his, labels = [], [], [], [], []
    for s in range(3):
        sel = ((theta[:, i_koff] >= edges[s]) &
               ((theta[:, i_koff] <= edges[s + 1]) if s == 2
                else (theta[:, i_koff] < edges[s + 1])))
        paired = d["cont_err"][sel, -1, i_koff] - reset_base[sel]
        mean, lo, hi = boot(paired[:, None])
        # Keep the plotting coordinate in log10 space so reciprocal changes are symmetric
        # around zero, but label every value as the reader-facing multiplicative factor.
        xs.append(s); shifts.append(mean[0])
        los.append(lo[0]); his.append(hi[0])
        labels.append(names[s])   # the ranges are given in the caption
    ax.axhline(0, color=INK2, lw=1.0)
    for x, sh, lo, hi in zip(xs, shifts, los, his):
        ax.plot([x, x], [lo, hi], color=CONT, lw=1.7, solid_capstyle="round")
        ax.plot([x], [sh], marker="o", color=CONT, clip_on=False, zorder=3)
        ax.annotate(f"×{10 ** sh:.2f}", (x, sh), textcoords="offset points", xytext=(7.5, 0),
                    ha="left", va="center", fontsize=7.6, color=INK)
    ax.set_xticks(xs); ax.set_xticklabels(labels)
    ax.tick_params(axis="x", labelsize=7.0)
    ax.set_xlim(-0.45, 2.8); ax.set_ylim(-0.43, 0.65)
    ax.set_yticks([-np.log10(2), 0, np.log10(2), np.log10(4)])
    ax.set_yticklabels(["×0.5", "×1", "×2", "×4"])
    ax.set_ylabel("window-10 shift\n(multiplicative factor)")
    ax.set_xlabel("true unpairing rate (1/s)")
    ax.set_title("(b) Rates compress\ntoward the prior", loc="left")

    # ---- (c) confidence does not follow ----------------------------------------------------
    ax = axes[2]
    cov_c, lo_c, hi_c = boot(d["fd_cov90_cont"])
    _, r_lo, r_hi = boot(d["fd_cov90_reset"])
    band(ax, float(np.nanmean(r_lo)), float(np.nanmean(r_hi)), RESET, "reset")
    ax.plot(pos, cov_c, marker="o", color=CONT, label="continuous", clip_on=False)
    ax.fill_between(pos, lo_c, hi_c, color=CONT, alpha=0.15, lw=0)
    ax.axhline(0.90, color=INK2, lw=1.0, ls=(0, (4, 2.5)))
    ax.text(9.9, 0.875, "nominal 90%", fontsize=7.2, color=INK2, ha="right", va="top")
    ax.set_ylim(0.2, 1.03); ax.set_xlim(1, 10)
    ax.set_xticks([1, 4, 7, 10])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("90% interval coverage")
    ax.set_xlabel("window position")
    ax.set_title("(c) Coverage collapses\nwithout wider intervals", loc="left")
    ax.legend(loc="lower left", handlelength=1.0, labelspacing=0.2, borderpad=0.1, fontsize=7.2)

    fig.tight_layout(pad=0.3, w_pad=1.3)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig2_result.{ext}", bbox_inches="tight")
    plt.close(fig)


# =============================================================================
# Simulator-to-experiment sensitivity numbers (Section 4.3, Figure 3, Figure S1)
# =============================================================================

CENSUS = {"resting": (31.4, 2.0), "activated": (78.2, 3.7)}   # inferred f_D (%), cell-level SE
# Median across cells of the OLS slope x nine window intervals, applied to each window's
# stored marginal-posterior median: ALP = resting MET-FAB; BET = activated MET-INLB.
EXPERIMENTAL_KOFF_RISE_LOG10 = {"resting": 0.4749941761, "activated": 0.3111711281}


def census_transfer(d):
    """The horizon artifact carried, unchanged, onto the experimental census.

    A SENSITIVITY calculation, not a correction: simulator-to-experiment transfer is
    uncalibrated. The artifact is the paired recording-level signed shift of the dimer-complex
    fraction (continuous minus reset at the same parameters), i.e. the horizon-specific bias with
    the estimator's ordinary in-distribution bias differenced out. Recordings are classed as
    resting-like or activated-like by their initial composition label (< 0.4 / > 0.7), the strata
    of the audit report's exploratory composition table. For the unpairing rate the like-for-like
    comparison with the experimental temporal-dynamics report is slope-based: that report fits an
    OLS line to log10 estimates against time and multiplies by the span, so the same operator is
    applied to the continuous arm's mean signed error; the endpoint (window 10 minus window 1) and
    recording-level variants are written alongside because the trend is concave.
    """
    keys = list(d["parameter_keys"])
    i_koff = keys.index("rate_dissociation")
    fdc, fdt = d["fd_cont"], d["fd_true_start_cont"]
    fdr, fdrt = d["fd_reset"], d["fd_true_start_reset"]
    rec_c = 100 * (fdc.mean(1) - fdt.mean(1))
    rec_r = 100 * (fdr.mean(1) - fdrt.mean(1))
    signed = rec_c - rec_r                                   # pp per recording, paired
    last = 100 * (fdc[:, -1] - fdt[:, -1]) - rec_r
    th = d["theta_log10"]
    A, B, C = (10 ** th[:, keys.index(k)] for k in ("count_alp", "count_bet", "count_chi"))
    label_fd = (B + C) / (A + B + C)
    classes = {"resting": label_fd < 0.4, "activated": label_fd > 0.7}
    out = {"n": int(signed.size)}
    m, lo, hi = boot(signed[:, None]); out["all"] = (float(m[0]), float(lo[0]), float(hi[0]))
    m, lo, hi = boot(last[:, None]); out["last_window"] = (float(m[0]), float(lo[0]), float(hi[0]))
    for cls, sel in classes.items():
        m, lo, hi = boot(signed[sel][:, None])
        out[cls] = (float(m[0]), float(lo[0]), float(hi[0]), int(sel.sum()))
    inferred = {c: CENSUS[c][0] for c in CENSUS}
    out["shifted"] = {c: inferred[c] - out[c][0] for c in CENSUS}
    out["inferred_contrast"] = inferred["activated"] - inferred["resting"]
    out["shifted_contrast"] = out["shifted"]["activated"] - out["shifted"]["resting"]
    kc, kr = d["cont_err"][:, :, i_koff], d["reset_err"][:, :, i_koff]
    mw = kc.mean(0)
    out["koff_rise"] = {"slope": float(np.polyfit(np.arange(10), mw, 1)[0] * 9),
                        "endpoint": float(mw[-1] - mw[0]),
                        "recording": float((kc.mean(1) - kr.mean(1)).mean())}
    # First-window gate: the window-1 paired |error| contrast of every primary must lie within
    # its tolerance (the runner's criterion, equivalence_verdict == "equivalent"); persisted
    # here so the Results sentence quoting it traces to the same arrays.
    gate = {}
    fd_w1 = d["fd_delta_abs"][:, 0] * (100.0 if np.abs(d["fd_delta_abs"]).max() < 1 else 1.0)
    m, lo, hi = boot(fd_w1[:, None]); gate["f_D"] = (float(m[0]), float(lo[0]), float(hi[0]), MARGINS["f_D"], "pp")
    for k in ("diffusivity_alp", "rate_dissociation"):
        v = d["delta_abs"][:, 0, keys.index(k)]; m, lo, hi = boot(v[:, None])
        gate[k] = (float(m[0]), float(lo[0]), float(hi[0]), MARGINS[k], "dex")
    out["gate"] = gate
    names = {"slope": "OLS slope x 9 windows (like-for-like with the experimental report)",
             "endpoint": "window 10 minus window 1", "recording": "recording-level paired shift"}
    gap = out["shifted_contrast"] - out["inferred_contrast"]
    lines = [
        "# Simulator-to-experiment sensitivity numbers", "",
        "Generated by `figures/make_paper_figures.py` from the persisted audit arrays (cohort "
        f"`{d['cohort_id']}`, {out['n']} matched settings). Sensitivity calculation only: transfer is "
        "uncalibrated, so shifted values are not corrected estimates.", "",
        "| quantity | value | 95% bootstrap CI over matched settings | n |", "|---|---|---|---|",
        "| recording-level signed f_D shift, continuous minus reset, all | %+.2f pp | [%+.2f, %+.2f] | %d |"
        % (*out["all"], out["n"]),
        "| same, last window only | %+.2f pp | [%+.2f, %+.2f] | %d |" % (*out["last_window"], out["n"]),
        "| same, resting-like recordings (initial label f_D < 0.4) | %+.2f pp | [%+.2f, %+.2f] | %d |"
        % out["resting"],
        "| same, activated-like recordings (initial label f_D > 0.7) | %+.2f pp | [%+.2f, %+.2f] | %d |"
        % out["activated"],
        "", "| census (dimer-complex fraction) | inferred from recordings | under direct transfer |", "|---|---|---|",
        "| resting condition | %.1f%% | %.1f%% |" % (inferred["resting"], out["shifted"]["resting"]),
        "| activated condition | %.1f%% | %.1f%% |" % (inferred["activated"], out["shifted"]["activated"]),
        "| condition contrast | %.1f pp | %.1f pp (the inferred contrast is %.1f pp smaller "
        "than the direct-transfer value) |"
        % (out["inferred_contrast"], out["shifted_contrast"], gap),
        "", "| in-simulator kappa_OFF horizon rise across a recording (continuous arm, mean signed "
        "log10 error) | log10 shift | factor | share of the experimental rise: resting MET-FAB "
        "0.475 / activated MET-INLB 0.311 (posterior-median, slope-based) |",
        "|---|---|---|---|"]
    for k, v in out["koff_rise"].items():
        lines.append("| %s | %+.3f | x%.2f | %.2f / %.2f |" % (
            names[k], v, 10 ** v, v / EXPERIMENTAL_KOFF_RISE_LOG10["resting"],
            v / EXPERIMENTAL_KOFF_RISE_LOG10["activated"]))
    lines += ["", "## First-window gate (window 1 continuous minus reset, paired |error| contrast)", "",
              "| primary | mean | 95% CI | tolerance | within tolerance |", "|---|---|---|---|---|"]
    for k, (m, lo, hi, tol, unit) in out["gate"].items():
        inside = lo > -tol and hi < tol
        extra = "" if unit == "pp" else " (factor %.3f / %.3f)" % (10 ** abs(lo), 10 ** abs(hi))
        lines.append("| %s | %+.4f %s | [%+.4f, %+.4f]%s | %g %s | %s |" % (k, m, unit, lo, hi, extra, tol, unit, "yes" if inside else "NO"))
    (OUT / "census_transfer.md").write_text("\n".join(lines) + "\n")
    return out


# =============================================================================
# Figure 3 -- the payoff
# =============================================================================

def figure_payoff(numbers):
    """The claim-verdict matrix.

    The census scatter that used to sit beside this panel was dropped: its four numbers
    (31.4%, 78.2%, the 46.8 pp contrast and the 1.5 pp shift) are all stated in the text,
    so the plot spent a quarter page repeating them. What cannot be said as compactly is the
    per-claim verdict, which is what this panel keeps.

    Verdicts are carried by the words and by a neutral rail, never by the arm colors: blue and
    orange mean "reset" and "continuous" everywhere else in this paper, and reusing them as
    status would overload them.
    """
    fig, ax = plt.subplots(figsize=(5.5, 1.42))
    gap = numbers["shifted_contrast"] - numbers["inferred_contrast"]
    rows = [("condition contrast", "survives",
             f"artifact changes {numbers['inferred_contrast']:.1f} pp by {abs(gap):.1f} pp", 0),
            ("within-recording decline", "not generated", "artifact pushes the other way", 0),
            ("monomer diffusion coefficient", "within tolerance", "at both audited levels", 0),
            ("absolute composition", "qualified", "artifact of order 2-3 pp", 1),
            ("absolute unpairing rate", "not supported",
             "horizon effect ×1.24; experiment ×3.0 / ×2.0", 2)]
    rail = {0: "#3f3f3c", 1: "#8a8983", 2: "#b9b7ae"}
    ax.set_xlim(0, 1); ax.set_ylim(-0.62, len(rows) - 0.38); ax.axis("off")
    for i, (claim, verdict, why, tone) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.add_patch(Rectangle((0.0, y - 0.40), 1.0, 0.80, facecolor="#f1f0ec",
                               alpha=0.85 if tone == 0 else 0.5, lw=0))
        ax.plot([0.010, 0.010], [y - 0.34, y + 0.34], color=rail[tone], lw=2.8,
                solid_capstyle="round")
        ax.text(0.040, y + 0.14, claim, fontsize=7.6, color=INK, va="center")
        ax.text(0.040, y - 0.18, why, fontsize=7.0, color=INK2, va="center")
        ax.text(0.992, y, verdict, fontsize=7.6, color=INK, va="center", ha="right",
                weight="bold")
    fig.tight_layout(pad=0.15)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"fig3_payoff.{ext}", bbox_inches="tight")
    plt.close(fig)


def experimental_time_course():
    """Per-window dimer-complex fraction of the experimental recordings, from the persisted
    Experiment results (evidence/census/MAP_Experiment): the in-draw mean of f_D per window,
    averaged over the 25 cells of each condition, with the cell-level standard error.
    Window 1 and window 10 reproduce the 87.0% -> 70.2% figures quoted in Section 4.3."""
    d = np.load(HERE.parent / "evidence" / "census" / "MAP_Experiment"
                / "SRM_AND_SBI_DIMER_ALP_2S_50FPS_MAP_Experiment.npz", allow_pickle=True)
    c = 10.0 ** d["posterior_samples_cloud"].astype(float)[..., :3]
    fd = ((c[..., 1] + c[..., 2]) / c.sum(-1)).mean(-1)                 # (500,) in-draw mean
    out = {}
    for k, name in ((0, "resting"), (1, "activated")):                   # kinds: ALP = MET-FAB, BET = MET-INLB
        m = d["kind_index"] == k
        cells = np.unique(d["cell"][m])
        per = np.array([[fd[m & (d["cell"] == cell) & (d["chunk"] == ch)].mean() for ch in range(10)]
                        for cell in cells])                                # (cells, 10)
        out[name] = (per.mean(0) * 100, per.std(0, ddof=1) / np.sqrt(per.shape[0]) * 100)
    return out


def figure_census(numbers):
    """Supplementary: (a) the inferred census and its value under direct transfer of the
    artifact; (b) the within-recording time course of the same quantity, which is the
    measurement the sensitivity calculation is applied to. Panel (b) shows experimental
    inferences only; the simulated effect enters as a caption statement, not as a curve."""
    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(5.5, 2.3), gridspec_kw={"width_ratios": [1.0, 1.15]})
    inferred = [CENSUS["resting"][0], CENSUS["activated"][0]]
    adjusted = [numbers["shifted"]["resting"], numbers["shifted"]["activated"]]
    err = [CENSUS["resting"][1], CENSUS["activated"][1]]
    x = np.array([0.0, 1.0])
    ax.errorbar(x - 0.09, inferred, yerr=err, fmt="o", color=CONT, capsize=2.6, lw=1.6,
                label="inferred from recordings", clip_on=False)
    ax.errorbar(x + 0.09, adjusted, yerr=err, fmt="s", color=RESET, capsize=2.6, lw=1.6,
                mfc=SURF, label="under direct transfer of\nthe in-simulator effect", clip_on=False)
    for xi, m, c in zip(x, inferred, adjusted):
        ax.annotate("", xy=(xi + 0.09, c + 1.4), xytext=(xi - 0.09, m - 1.4),
                    arrowprops=dict(arrowstyle="->", color=INK2, lw=0.9, alpha=0.75))
    xb = 1.42
    ax.annotate("", xy=(xb, inferred[1]), xytext=(xb, inferred[0]),
                arrowprops=dict(arrowstyle="<->", color=INK2, lw=1.0))
    ax.text(xb + 0.07, 54, f"{numbers['inferred_contrast']:.1f} pp inferred\n"
            f"{numbers['shifted_contrast']:.1f} pp under transfer", fontsize=7.2, color=INK,
            va="center", ha="left")
    ax.set_xticks(x); ax.set_xticklabels(["resting", "InlB-activated"])
    ax.set_ylim(0, 118); ax.set_xlim(-0.45, 2.35); ax.set_yticks([0, 25, 50, 75, 100])
    ax.set_ylabel("dimer complexes (%)")
    ax.set_title("(a) Recording-level census", loc="left")
    ax.legend(loc="upper right", handlelength=1.2, labelspacing=0.3, borderpad=0.2, fontsize=7.0)

    course = experimental_time_course()
    pos = np.arange(1, 11)
    for name, color, label in (("resting", INK2, "resting (MET-FAB)"),
                               ("activated", CONT, "InlB-activated (MET-INLB)")):
        m, e = course[name]
        ax2.plot(pos, m, marker="o", ms=3.2, color=color, lw=1.4, label=label, clip_on=False)
        ax2.fill_between(pos, m - e, m + e, color=color, alpha=0.15, lw=0)
    ax2.set_ylim(0, 118); ax2.set_xlim(1, 10); ax2.set_xticks([1, 4, 7, 10])
    ax2.set_yticks([0, 25, 50, 75, 100])
    ax2.set_xlabel("window position within the recording")
    ax2.set_title("(b) Within-recording time course", loc="left")
    ax2.legend(loc="lower left", handlelength=1.2, labelspacing=0.3, borderpad=0.2, fontsize=7.0)
    fig.tight_layout(pad=0.3, w_pad=1.2)
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"figS1_census.{ext}", bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    data = load()
    numbers = census_transfer(data)
    figure_design()
    figure_result(data)
    figure_payoff(numbers)
    figure_census(numbers)
    print("wrote:", *sorted(p.name for p in OUT.glob("fig*.pdf")))
