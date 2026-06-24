## Ranked issue list

### 1. Explainability claim is too broad: mostly traceability/documentation, not model explainability

**Reviewer quote**

> “The paper claims to improve explainability; however, the mechanisms presented are mainly related to traceability and documentation of the pipeline generation process. The explainability of the resulting models themselves is neither addressed nor experimentally evaluated. Consequently, the use of the term "explainable" appears insufficiently justified.”

Also related:

> “Explanations are a bit poor and confusing (specially in the experimental results)”

**Present in FGCS?**
**Yes, partially.** FGCS is better than ADBIS because it defines P3 as tracing and explaining the sequence of decisions leading to model selection, and explains that logs, artefacts, and natural-language explanations support inspection. However, the same ambiguity remains if “explainable” is read as **model interpretability** rather than **process explainability**.

**Improve ADBIS**

* Replace broad “explainable AutoML” language with “process-level explainability”, “pipeline-generation traceability”, or “decision-rationale explanation”
* Add a short paragraph explicitly saying that AGE-ML does **not** currently explain model predictions
* Add one example explanation in the paper or appendix and point to where the full examples are stored
* In the experiments, evaluate explanations at least minimally, e.g. by checking whether generated explanations correctly report steps, candidates, errors, fixes, and constraints

**Improve FGCS**

* Add a precise taxonomy: **model explainability**, **pipeline explainability**, **search-process explainability**, **provenance/traceability**
* State that AGE-ML targets the latter three, not intrinsic/post-hoc model explanation
* Add a small explanation-quality evaluation, even manual/rubric-based, to substantiate the claim
* Optionally add SHAP/LIME/permutation importance as future integration, not as a current contribution

**Severity / effort**: **Critical / Medium**
High acceptance risk because Reviewer 4 explicitly rejects partly on this point; moderate effort if handled by reframing plus a lightweight rubric

---

### 2. Data-centric claim is not matched by data-quality evaluation

**Reviewer quote**

> “The evaluation relies primarily on traditional predictive performance metrics. Given the data-centric nature of the proposed approach, I would have expected a more data-oriented evaluation, including metrics related to data quality, improvements to the dataset, error detection, data cleaning effectiveness, or bias reduction. This is somewhat paradoxical, as the paper advocates a data-centric perspective, yet this aspect is largely absent from the evaluation, where datasets are already provided as inputs. As a result, it remains unclear how AGE-ML concretely contributes to improving data quality.”

**Present in FGCS?**
**Yes.** FGCS is more explicit that data-centric AI involves preprocessing, data quality, feature engineering, and domain constraints, but the empirical section still mostly reports predictive performance, runtime, token cost, and pipeline execution outcomes. It does not yet demonstrate data-quality improvement as such.

**Improve ADBIS**

* Reframe the contribution as **data-centric pipeline construction**, not direct dataset improvement
* Add a limitation: AGE-ML currently selects/executes data-preparation operations; it does not perform a full data-cleaning audit
* Add at least one data-centric metric if possible: number/type of preprocessing decisions triggered by dataset predicates, missing-value handling, categorical encoding correctness, imbalance mitigation, bias-sensitive feature constraints
* For Adult, report that categorical handling and SMOTE/rebalancing are part of the selected pipeline, but avoid presenting this as “data quality improvement” unless measured

**Improve FGCS**

* Add a subsection “Data-centric evaluation”
* Add experiments on corrupted/noisy datasets: missing values, label noise, categorical-feature issues, imbalance, outliers
* Measure before/after effects of data-centric steps, not only final score
* Include bias/fairness only if the specification actually encodes bias-related rules; otherwise list as future work

**Severity / effort**: **Critical / High**
Conceptually severe; more expensive because a convincing answer requires additional experiments or a careful narrowing of claims

---

### 3. Reproducibility vs LLM non-determinism is underdeveloped

**Reviewer quote**

> “W1. LLMs are known to be not deterministic. How do you manage that? (especially in terms of reproducibility)”

Also:

> “The reproducibility aspect is not enough emphasized in the paper. It would be nice to have feedback / an experiment on how the pipelines are more transparent and/or more reproducible compared to existing systems.”

And:

> “the accumulation of agents and LLMs introduces uncertainty and non-determinism at many steps.”

**Present in FGCS?**
**Partially.** FGCS acknowledges stochasticity, logging, deterministic checks, budgets, and MLflow artefact tracking; it also notes repeated executions may lead to different pipelines. But it lacks a reproducibility protocol or experiment.

**Improve ADBIS**

* Add a concise “Reproducibility under stochastic generation” paragraph
* Distinguish:

  * **execution reproducibility**: logged code, splits, hyperparameters, metrics, artefacts
  * **search reproducibility**: weaker, due to LLM stochasticity and sampled pipelines
  * **result reproducibility**: empirical, should be assessed over repeated runs
* Add exact controls: fixed random seeds, fixed train/test splits, logged prompts, logged model version, temperature/top-p, generated code snapshots

**Improve FGCS**

* Add a repeated-run experiment: same dataset/specification, N repeated executions, report variance in selected pipelines and scores
* Report reproducibility levels:

  * same generated code rerun
  * same pipeline plan rerun
  * full AGE-ML rerun
* Store and cite prompt/model/config versions in the artefact schema

**Severity / effort**: **Critical / Medium**
Strong payoff because three reviewers touch transparency/reproducibility directly; moderate effort if first addressed analytically, higher if adding experiments

---

### 4. Budget-effect ablation is missing

**Reviewer quote**

> “Experiments should be provided on the effect of the budget (how the number of generated pipelines helps? How the number of executed pipelines help?)”

Related Reviewer 2 quote:

> “The effectiveness of the search space exploration is heavily dependent on the LLM's ability to generate valid code; in some tests (e.g., HAR and MNIST 784), the system failed to explore the full budget because the models could not consistently produce valid pipelines.”

**Present in FGCS?**
**Yes.** FGCS uses a fixed budget and reports actual executed pipelines, but does not include a budget sensitivity study.

**Improve ADBIS**

* Add a small ablation plot/table for 2–3 datasets: budget ∈ {5, 10, 20, 30}
* Report:

  * planned pipelines
  * valid generated scripts
  * executed pipelines
  * best score
  * wall-clock time
  * token cost
* If no space, at least add a paragraph explaining why budget sensitivity is future work

**Improve FGCS**

* Add full budget ablation across representative datasets
* Separate:

  * pipeline budget
  * generation-attempt budget
  * worker budget
  * time budget
* Report diminishing returns and failure modes

**Severity / effort**: **High / Medium**
Concrete, reviewer-requested, and empirically central to AutoML claims

---

### 5. Table columns and runtime/cost interpretation are unclear

**Reviewer quote**

> “The meaning and interpretation of the different columns in tables 2 and 3 is not clearly explained.”

Also:

> “The claim about the balanced distribution between LLM inference and ML training is not clearly explained. Where exactly does it come from?”

And Reviewer 2:

> “In multiple datasets (e.g., Adult and California Housing), LLM inference accounted for more than 70% of the total execution time, indicating potential inefficiencies in prompt design or the agentic loop.”

**Present in FGCS?**
**Partially.** FGCS has more discussion and time-breakdown figures, but the definitions of “Actual Time”, “Equivalent Time”, “LLM Inference Time”, “ML Training Time”, “Actual P.”, and “Putative Cost” still need to be made operationally explicit.

**Improve ADBIS**

* Add a paragraph before Tables 2–3 defining every column
* Explain whether LLM/ML times are summed across parallel workers or wall-clock
* Explain “Actual P.” as successfully executed pipelines out of budget
* Replace vague “balanced distribution” with numeric ratios
* Avoid overclaiming: say “more balanced for Gemini 3.1 Flash Lite than Gemini 2.5 Flash in our measurements”

**Improve FGCS**

* Add formulae:

  * `Equivalent time = sum over agent/pipeline execution times`
  * `Actual time = wall-clock elapsed time`
  * `LLM share = LLM inference time / equivalent time` or whatever is true
* Add per-agent/per-stage breakdown if logs support it
* Add one figure showing ratios, not only raw time

**Severity / effort**: **High / Low**
Easy fix with high payoff because it improves experimental credibility

---

### 6. Specification language needs grammar/formal syntax

**Reviewer quote**

> “Listing 1 is fine, but a grammar should be provided”

Related:

> “Lacks some formality and precision in the explanations and claims”

**Present in FGCS?**
**Partially.** FGCS gives a formal abstract model and detailed YAML-like syntax, but it still does not provide a compact grammar/EBNF. The supplementary material is much stronger than ADBIS, but still example-driven.

**Improve ADBIS**

* Add a small grammar fragment in the specification subsection or appendix
* At minimum define the top-level schema:

  * `pipeline.steps`
  * `ordering`
  * `constraints`
  * `budgets`
* State which parts are currently supported vs intended

**Improve FGCS**

* Add an explicit EBNF or JSON Schema/YAML Schema
* Clarify semantic constraints not captured by syntax, e.g. candidate uniqueness, required fields, finite domains
* Add validation rules and error cases

**Severity / effort**: **High / Medium**
Important for precision; feasible without new experiments

---

### 7. Expert-knowledge formalization ignores multiple experts, conflicts, and priorities

**Reviewer quote**

> “The formalization of expert knowledge (in this case, data scientists' knowledge) deserves further elaboration. The paper assumes the existence of a single specification expressing the knowledge of a data scientist, but it does not discuss situations where multiple experts contribute to defining constraints. In particular, mechanisms for conflict resolution, prioritization, or the integration of contradictory knowledge are not addressed.”

**Present in FGCS?**
**Yes.** FGCS formalizes specifications and constraints, but it still assumes a single coherent specification. It does not discuss multiple experts, conflict resolution, weighted constraints, priorities, or provenance of rules.

**Improve ADBIS**

* Add a limitation paragraph: current AGE-ML assumes a single consistent specification
* Explain current behavior under inconsistency: CSP unsatisfiable, no admissible pipeline
* Add future-work mechanism:

  * rule provenance
  * priorities
  * soft constraints
  * expert-specific namespaces
  * conflict diagnosis from unsat cores

**Improve FGCS**

* Add a formal extension:

  * hard vs soft constraints
  * priority levels
  * provenance metadata
  * conflict-resolution policy
* Use Z3 unsat cores to explain contradictory constraints
* Add an example conflict: one expert requires normalization, another forbids it under a condition

**Severity / effort**: **High / Medium**
Reviewer 4 rejection point; can be handled as limitation/future work in ADBIS, deeper treatment in FGCS

---

### 8. Agent-level cost and impact are not separated

**Reviewer quote**

> “More details should be provided on the separate cost and impact of each one of the agents.”

**Present in FGCS?**
**Partially.** FGCS describes planner, executor, evaluator, and catalog roles in detail; it reports aggregate tokens/costs, but not cost/impact per agent.

**Improve ADBIS**

* Add a small table with agent responsibilities and cost sources:

  * planner: dataset-condition LLM calls, CSP solving
  * executor: code generation, validation, repair, hyperparameter execution
  * evaluator: model scoring and selection
  * catalog: logging overhead
* If logs do not support precise measurement, state that current reported costs are aggregate

**Improve FGCS**

* Instrument and report:

  * number of LLM calls per agent
  * tokens per agent
  * wall-clock per agent
  * failure/retry rate per executor
  * contribution to final pipeline success
* This also helps answer latency and budget concerns

**Severity / effort**: **Medium-High / Medium**
Useful for experimental transparency and MLOps positioning

---

### 9. High LLM latency and redundant context need mitigation strategies

**Reviewer quote**

> “The authors should discuss strategies for reducing the high inference latency and redundant conversational context mentioned in the limitations.”

Related:

> “In multiple datasets (e.g., Adult and California Housing), LLM inference accounted for more than 70% of the total execution time, indicating potential inefficiencies in prompt design or the agentic loop.”

**Present in FGCS?**
**Partially.** FGCS explicitly mentions token usage and future prompt/context optimization, but mostly at a high level.

**Improve ADBIS**

* Add concrete mitigation strategies:

  * prompt compression
  * structured outputs
  * caching dataset summaries
  * caching successful code templates
  * using deterministic validators before LLM judges
  * limiting conversational history to relevant error traces
  * smaller judge models for validation
* Tie these to the observed token/time columns

**Improve FGCS**

* Add an optimization roadmap with expected effect per strategy
* Add ablation if feasible: full history vs compressed context, LLM judge vs regex-first validation
* Report cacheability: same dataset/specification summaries reused across pipelines

**Severity / effort**: **Medium-High / Low**
Easy textual improvement; stronger if supported by measurements

---

### 10. Heuristic search beyond random/symbolic enumeration needs detail

**Reviewer quote**

> “Elaborate on how future versions might move beyond symbolic enumeration toward more efficient heuristic-based search strategies to improve exploration diversity.”

Related Reviewer 4 concern:

> “several aspects deserve further investigation and development, particularly regarding the impact on data quality, the evaluation protocol, and the integration and management of expert knowledge.”

**Present in FGCS?**
**Partially.** FGCS future work mentions smarter and more efficient search strategies, but does not specify concrete methods.

**Improve ADBIS**

* Add a short paragraph naming plausible strategies:

  * diversity-aware sampling over CSP solutions
  * Bayesian optimization over pipeline structures
  * bandit allocation across pipeline families
  * warm-start from prior experiments
  * constraint-aware evolutionary search
* Clarify that CSP remains the validity filter; heuristics only rank/sample valid pipelines

**Improve FGCS**

* Formalize planner as two-stage:

  * admissibility generation via CSP
  * utility/diversity ranking via heuristic search
* Add a design sketch or future-work algorithm
* Add expected benefits and risks

**Severity / effort**: **Medium / Low**
Mostly future-work elaboration; low effort

---

### 11. Direct editing and selective re-execution are underspecified

**Reviewer quote**

> “While the framework allows for expertise injection at the start, it currently lacks the capability for data scientists to directly edit or selectively re-execute specific components of a pipeline once the automated process has begun.”

And:

> “Provide more detail on the feasibility of the proposed "direct editing" feature, as this is a critical requirement for true data-centric AI.”

**Present in FGCS?**
**Partially.** FGCS already lists direct editing and selective re-execution as future work, but feasibility and mechanism are not detailed.

**Improve ADBIS**

* Add the current limitation explicitly
* Sketch feasible support:

  * freeze a generated script
  * edit script or specification
  * invalidate only affected runs
  * rerun selected pipeline/runs
  * preserve lineage in MLflow
* Avoid claiming current support

**Improve FGCS**

* Add an architecture extension:

  * editable artefact state
  * dependency graph between specification, generated code, runs, and metrics
  * rerun policy
  * provenance of human edits
* Discuss safety validation after manual edits

**Severity / effort**: **Medium / Low-Medium**
Important to one reviewer, manageable as future-work detail

---

### 12. Multi-agent nature is not explicit enough after the introduction

**Reviewer quote**

> “Being a multi-agent system in only mentioned in the introduction, but later it is not that explicit (eg, Figure 3 is confusing)”

**Present in FGCS?**
**Mostly no.** FGCS is much clearer: it describes three agent types plus a reactive component, singleton planner/evaluator, parallel executors, and their responsibilities. This is mainly due to pruning in the ADBIS version.

**Improve ADBIS**

* In Section 3, explicitly list agents and responsibilities
* Make Figure 3 caption say it is the **executor agent state machine**, not the whole MAS
* Add a sentence distinguishing:

  * planner agent
  * executor agents
  * evaluator agent
  * data catalog
* Ensure Figure 2/3 visual language is consistent

**Improve FGCS**

* Minor: ensure all figures consistently label agents and agent interactions
* Add a short “agent taxonomy” table if space permits

**Severity / effort**: **Medium / Low**
Low-effort clarity fix; ADBIS-specific

---

### 13. Classification/regression scope is ambiguous

**Reviewer quote**

> “At some point seems that only classification problems can be solved, but then the experiments show also regressions.”

**Present in FGCS?**
**No, mostly resolved.** FGCS explicitly states the work focuses on supervised predictive tasks where the target is present: classification when categorical, regression when numerical.

**Improve ADBIS**

* Add the same scope sentence early, ideally in architecture or experimental setup
* Ensure examples mention both classification and regression constraints
* If Listing 1 is classification-heavy, add one regression candidate or a sentence saying the excerpt is partial

**Improve FGCS**

* Minor consistency pass only

**Severity / effort**: **Medium / Low**
Simple but prevents confusion about system scope

---

### 14. Supplementary material location is unclear

**Reviewer quote**

> “Where are "supplementary materials"? does this refer to the GitHub repository? In which file/folder?”

**Present in FGCS?**
**No, or much less.** FGCS has an actual supplementary-materials document. ADBIS apparently refers to supplementary materials without making the access path explicit.

**Improve ADBIS**

* Replace vague “supplementary materials” with an explicit pointer:

  * appendix file name if submitted
  * repository path if GitHub
  * artefact DOI if available
* If ADBIS does not allow supplementary files, remove the phrase and point to repository artefacts

**Improve FGCS**

* Ensure the main paper references the supplementary file by exact title and appendix names
* Add repository paths for prompts/generated explanations if not in the supplementary PDF

**Severity / effort**: **Medium / Low**
Very easy fix; avoids reviewer irritation

---

### 15. Dataset descriptions and complexity characterization are insufficient

**Reviewer quote**

> “Dataset characteristics provided in table 1 are interesting, but they not necessarily reflect the complexity of the problem.”

Also Reviewer 3:

> “a small description of each dataset would be helpful”

**Present in FGCS?**
**Partially resolved.** FGCS already includes a paragraph for each dataset and explains domain/task characteristics. However, it still could better characterize complexity beyond counts.

**Improve ADBIS**

* Add 1–2 sentences per dataset group or move full descriptions to appendix
* Add complexity proxies:

  * class imbalance
  * categorical ratio
  * missingness
  * dimensionality/instances ratio
  * number of classes
  * baseline difficulty
* Avoid relying only on features/instances/numeric/discrete columns

**Improve FGCS**

* Add a compact “complexity indicators” table
* For classification: classes, imbalance ratio
* For regression: target skew, missingness, categorical ratio
* This also supports the data-centric evaluation concern

**Severity / effort**: **Medium / Low-Medium**
Easy to improve in text; more useful if paired with data-quality metrics

---

### 16. Compact dataset description generation is underspecified

**Reviewer quote**

> “how is the compact description of the dataset structure obtained? Is it metadata / generated by an agent / ...?”

**Present in FGCS?**
**Yes.** FGCS mentions that executor prompts use a compact dataset description, and planner dataset conditions may use dataset summaries, schema information, feature statistics, or samples. But it does not fully specify the generation procedure.

**Improve ADBIS**

* Add one sentence: dataset summaries are computed from schema/statistics/sample rows, then optionally passed to the LLM for semantic predicates
* Distinguish deterministic metadata extraction from LLM-based interpretation

**Improve FGCS**

* Add exact summary fields:

  * column names
  * inferred data types
  * missingness
  * cardinality
  * target role
  * value distributions
  * sample rows if used
* State privacy/size controls for samples
* State which agent computes it

**Severity / effort**: **Medium / Low**
Simple clarification

---

### 17. Valid-code generation is a bottleneck and should be analyzed

**Reviewer quote**

> “The effectiveness of the search space exploration is heavily dependent on the LLM's ability to generate valid code; in some tests (e.g., HAR and MNIST 784), the system failed to explore the full budget because the models could not consistently produce valid pipelines.”

**Present in FGCS?**
**Yes.** FGCS reports “Actual P.” and discusses that fewer valid pipelines hurt performance, but the failure causes are not deeply analyzed.

**Improve ADBIS**

* Add “validity/executability bottleneck” discussion
* Report failure counts:

  * semantic validation failures
  * syntax/import failures
  * runtime failures
  * exhausted retries
* Explain how retry budget interacts with valid pipeline count

**Improve FGCS**

* Add a failure taxonomy and per-dataset failure rates
* Link failures to model choice, dataset type, and prompt length
* Use examples of common generated-code errors and repairs

**Severity / effort**: **Medium-High / Medium**
Important because it affects search effectiveness and performance claims

---

### 18. Presentation and formatting problems signal rushed submission

**Reviewer quote**

> “Presentation should be improved”

> “there are clear indications of the paper being written and submitted in a rush (eg, using more space than allowed, while some figures and tables could have been easily reduced in a minute to compensate that).”

Specifics:

> “Figure 4 size should be reduced”

> “Font size in table 1 should be reduced”

> “Caption of table 1 should be underneath (like in the others).”

> “Figure 1 should have a legend with the meaning of the arrows.”

> “Machine Learning should be shortened as ML everywhere.”

> “use bold font for numbers surpassing the baselines would be helpful to read more easily the table”

> “Typos: - p13 : space after the parenthesis "( Wilt..." - same for "( California..."”

**Present in FGCS?**
**Mostly ADBIS-specific.** Some consistency issues may still exist in FGCS, but the review targets the ADBIS layout.

**Improve ADBIS**

* Resize Figure 4
* Reduce Table 1 font or simplify columns
* Move Table 1 caption below the table
* Add legend to Figure 1
* Standardize “Machine Learning” → “ML” after first definition
* Bold scores outperforming baseline
* Fix listed typos
* Check page limit and figure/table whitespace

**Improve FGCS**

* Run the same editorial consistency pass
* Check figure legends and abbreviation consistency
* Ensure tables are readable in final format

**Severity / effort**: **Medium / Very low**
Low intellectual value but high reviewer-satisfaction payoff

---

### 19. Formality and precision of claims need tightening

**Reviewer quote**

> “Lacks some formality and precision in the explanations and claims”

**Present in FGCS?**
**Partially.** FGCS is substantially more formal: it has problem statements, abstract notation, specification-language semantics, CSP encoding, and architecture details. Still, some claims remain broad: “data-centric”, “explainable”, “reproducible”, “transparent”, “competitive”.

**Improve ADBIS**

* Define each major claim operationally:

  * “data-centric” = supports declarative preprocessing/data-condition constraints
  * “transparent” = logs pipeline plans, code, hyperparameters, metrics, explanations
  * “reproducible” = artefact-level replay, not necessarily deterministic full regeneration
  * “explainable” = process-level explanation
* Avoid terms not evaluated experimentally

**Improve FGCS**

* Add a claim-to-evidence table:

  * claim
  * mechanism
  * empirical evidence
  * limitation
* This would directly reduce ambiguity

**Severity / effort**: **Medium-High / Low**
Strong payoff because it mitigates multiple conceptual critiques

---

### 20. Current evaluation protocol should be clearer and more defensible

**Reviewer quote**

> “several aspects deserve further investigation and development, particularly regarding the impact on data quality, the evaluation protocol, and the integration and management of expert knowledge.”

Related:

> “Experimental results seem promising”

but:

> “Explanations are a bit poor and confusing (specially in the experimental results)”

**Present in FGCS?**
**Partially.** FGCS has a fuller experimental design, dataset descriptions, two Gemini models, baselines, runtime/cost discussion, and limitations. Still, the protocol lacks ablations, reproducibility trials, data-centric metrics, and explanation-quality metrics.

**Improve ADBIS**

* Add a compact “What is evaluated / what is not evaluated” paragraph
* Make clear that current evaluation covers:

  * predictive performance
  * cost/time
  * successful pipeline execution
  * qualitative explanation example
* State that it does not yet cover:

  * model-level explainability
  * data-quality improvement
  * repeated-run reproducibility
  * budget sensitivity

**Improve FGCS**

* Add the missing evaluations if feasible
* Otherwise reorganize experiments into:

  * performance
  * efficiency
  * executability
  * reproducibility
  * explanation/process transparency
  * data-centric behavior
* This makes limitations explicit rather than exposed by reviewers

**Severity / effort**: **Medium-High / Medium-High**
Important, but can be partially addressed by reframing if no new experiments are possible

---

### 21. Source-code availability is positive but should be tied to reproducibility

**Reviewer quote**

> “Code is openly provided”

> “The authors make the source code publicly available through a GitHub repository, which supports reproducibility.”

**Present in FGCS?**
**Yes.** FGCS states that source code and automation scripts are publicly available.

**Improve ADBIS**

* Keep the claim
* Add exact repository path and commit/tag used for the paper
* Add reproduction instructions summary:

  * environment
  * command
  * datasets
  * expected artefacts

**Improve FGCS**

* Add archival DOI or release tag
* Ensure scripts reproduce all reported tables
* Log model/provider versions, because LLM APIs can drift

**Severity / effort**: **Medium / Low**
Positive comment, but strengthening it helps answer reproducibility critiques

---

## Cross-reviewer clusters to prioritize

1. **Conceptual claim control**
   Explainability, data-centricity, transparency, reproducibility. This is the main acceptance risk, especially due to Reviewer 4.

2. **Experimental credibility**
   Budget ablation, reproducibility runs, failure taxonomy, data-centric metrics, explanation-quality assessment.

3. **Clarity and formality**
   Grammar/schema, table definitions, agent costs, dataset-summary procedure, classification/regression scope.

4. **Presentation cleanup**
   Figures, captions, table fonts, legends, abbreviations, bold baselines, typos.

## Minimal revision strategy for ADBIS

Given ADBIS page constraints, the best compact fix is:

1. Add a **claim-scope paragraph** distinguishing process explainability from model explainability, and data-centric pipeline generation from direct data-quality improvement
2. Add a **limitations paragraph** covering LLM nondeterminism, lack of repeated-run reproducibility, no data-quality metrics, and no direct editing
3. Add a **small table of column definitions** for Tables 2–3
4. Add **one small budget/valid-pipeline ablation** or at least a failure-rate table
5. Add **grammar/schema fragment** for the YAML specification
6. Fix all presentation issues
