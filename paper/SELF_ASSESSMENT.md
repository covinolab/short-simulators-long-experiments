# Camera-ready self-assessment

**Assessment date:** October 30, 2026  
**Manuscript:** [Short Simulators, Long Experiments](main.pdf), camera-ready version; 21 pages, with the scientific body ending on page 5

The scientific and editorial revision is ready for submission. Comparison with the agreed enhancement plan and all three reviews shows that the manuscript addresses the principal requests for clarification, presentation, and supporting evidence. Requests for additional experiments remain unfulfilled and are explicitly retained as limitations. The [release repository](https://github.com/covinolab/short-simulators-long-experiments) was published on October 30, 2026; this assessment has been updated to record completion of that step.

| Reviewer request | What the current paper provides | Assessment |
| --- | --- | --- |
| Explain why training uses short clips | The Introduction explains the cost of building a large simulation corpus and why longer experimental recordings are scientifically useful. | Addressed |
| Clarify what is actually compared | The Introduction and Section 3 state that every estimator input is 2 seconds; initialization and inherited history distinguish the arms. | Addressed |
| Introduce microscopy and MET for a broader audience | Section 2 introduces MET, the ligand conditions, and the recordings. Appendix E explains detection, tracking, and the biological context with citations. | Addressed |
| Standardize Figure 1 typography | Figure 1 uses consistent heading and label sizes, with clearly distinguished audit arms. | Addressed |
| Illustrate the experimental results and inference limitations | Figure 4 shows the condition comparison, the selected sensitivity calculation, and the inferred experimental time courses. Its caption distinguishes these from corrected measurements. | Addressed |
| Frame the lesson beyond “long horizons” | The Introduction identifies deployment mismatch in states and histories, despite an unchanged simulator and input duration. | Addressed |
| Distinguish support escape from other inherited history | Appendix B shows degradation among settings that remain within the count box. Appendix C explains why this does not identify the responsible mechanism. | Addressed within the study’s scope |
| Make the thin composition stratum explicit | Section 4.2 and Appendix A report its two settings and withhold a verdict. | Addressed |
| Release code and supporting materials | The public repository provides reproduction commands, provenance, evidence, and explicit exclusions. The full audit analysis and posterior interval-width calculations require per-setting files available from the authors on request. | Addressed within the stated reproduction scope |

The readability criticism has been substantially addressed. Compared with the submitted version, the motivation is clearer, the Results and Discussion connect their statements more naturally, and the appendices explain their purpose before presenting technical details. The appendices remain dense, but their definitions and qualifications serve the scientific argument. No further rewrite is warranted by this assessment.

Two research extensions remain outside this revision:

- **Mechanism-separating ablations:** Appendix C states that neither intervention was run. Candidate explanations are presented without claiming to establish their causes. One accepting reviewer explicitly regarded these ablations as unnecessary for the principal conclusion.
- **A second simulator or estimator:** the study evaluates one deployed workflow. Its numerical effects and parameter-specific conclusions remain conditional on that scope; generality beyond it has not been demonstrated.

These are retained limitations, not completed reviewer requests. The manuscript-side enhancement plan is fulfilled within the agreed scope of using existing data. The release repository is public, and the submitted and camera-ready states have been committed in the separate local paper repository. The OpenReview upload remains the lead author's step; it does not require reopening the scientific revision.
