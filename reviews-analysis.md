Below is the regenerated issue list, with your constraints applied:

* **ADBIS**: accepted, no appendix, 16 pages including references, no real room for additions; therefore actions are mostly **micro-rephrasing, deletion, clarification, or future-work promises**
* **FGCS**: place for substantive fixes: extra experiments, fuller formalisation, variability analysis, syntax/semantics, and expanded future-work framing

I keep the list sorted by **descending severity/effort payoff**, under the revised assumption that ADBIS fixes must be lightweight.

## 1. Explainability claim is too broad

**Reviewer quote**

> “The paper claims to improve explainability; however, the mechanisms presented are mainly related to traceability and documentation of the pipeline generation process. The explainability of the resulting models themselves is neither addressed nor experimentally evaluated. Consequently, the use of the term "explainable" appears insufficiently justified.” 

Also:

> “Explanations are a bit poor and confusing (specially in the experimental results)” 

**Present also in FGCS?**
**Partially.** FGCS is clearer because it frames the contribution around **decision/process traceability**, logging, artefacts, and natural-language explanations of pipeline generation. Still, the word “explainable” may be overread as **model-level explainability**, which AGE-ML does not currently provide.

**Improve ADBIS**

Rephrase claims everywhere possible from:

> explainable pipelines / explainable AutoML

to:

> process-level explainability of pipeline generation
> traceable and inspectable pipeline construction
> explanations of the design and generation rationale

Add or replace one sentence along these lines:

> In this work, explainability refers to the traceability and natural-language documentation of the pipeline-generation process, rather than to post-hoc explanation of individual model predictions, which we leave to future integrations with model-explanation tools.

**Improve FGCS**

* Add a short taxonomy:

  * model explainability;
  * pipeline-structure explainability;
  * search-process explainability;
  * provenance/traceability.
* Explicitly state AGE-ML targets the last three
* Add a lightweight explanation-quality assessment:

  * correctness of reported steps;
  * correctness of reported candidates;
  * coverage of validation/execution failures;
  * usefulness for human inspection.

**Severity / effort**: **Critical / Low for ADBIS, Medium for FGCS**
High payoff because the issue affects a core claim and can be mitigated in ADBIS by wording alone

---

## 2. Data-centric claim is not sufficiently aligned with the evaluation

**Reviewer quote**

> “The evaluation relies primarily on traditional predictive performance metrics. Given the data-centric nature of the proposed approach, I would have expected a more data-oriented evaluation, including metrics related to data quality, improvements to the dataset, error detection, data cleaning effectiveness, or bias reduction. This is somewhat paradoxical, as the paper advocates a data-centric perspective, yet this aspect is largely absent from the evaluation, where datasets are already provided as inputs. As a result, it remains unclear how AGE-ML concretely contributes to improving data quality.” 

**Present also in FGCS?**
**Yes.** FGCS explains the data-centric motivation more thoroughly, but the empirical evaluation is still mostly predictive performance, execution cost, token cost, and pipeline success.

**Improve ADBIS**

Do **not** promise new metrics in ADBIS. Rephrase the claim to avoid implying that AGE-ML directly improves datasets.

Suggested replacement idea:

> AGE-ML is data-centric in the sense that pipeline construction is conditioned on the data at hand: the selected pipeline may include data-preparation, preprocessing, feature-engineering, and rebalancing steps required by the dataset properties and by the selected estimators. Thus, the system does not only select a model family and its hyperparameters, but searches for a suitable end-to-end workflow for the current data.

Also add a limitation/future-work sentence:

> A direct evaluation of data-quality improvement, error detection, cleaning effectiveness, and bias mitigation is outside the scope of this paper and will be addressed in future work.

**Improve FGCS**

* Add a “data-centric behaviour” analysis
* At minimum, report which preprocessing/data-handling steps are selected per dataset
* Better: add controlled perturbation experiments:

  * missing values;
  * categorical features;
  * imbalance;
  * noisy labels;
  * outliers.
* Evaluate whether AGE-ML selects appropriate preprocessing for the data/model combination

**Severity / effort**: **Critical / Low for ADBIS, High for FGCS**
The reviewer’s objection is strong, but ADBIS can only narrow the claim

---

## 3. Reproducibility under LLM nondeterminism is underspecified

**Reviewer quote**

> “W1. LLMs are known to be not deterministic. How do you manage that? (especially in terms of reproducibility)” 

Also:

> “The reproducibility aspect is not enough emphasized in the paper. It would be nice to have feedback / an experiment on how the pipelines are more transparent and/or more reproducible compared to existing systems.” 

And:

> “the accumulation of agents and LLMs introduces uncertainty and non-determinism at many steps.” 

**Present also in FGCS?**
**Partially.** FGCS already discusses logging, MLflow, prompts, validation, and stochasticity. However, it does not yet include a variability analysis of generated code/pipelines.

**Improve ADBIS**

Rephrase reproducibility as **guardrailed reproducibility**, not deterministic regeneration.

Suggested sentence:

> Reproducibility is addressed at the artefact and execution level rather than by assuming deterministic LLM behaviour: AGE-ML constrains code generation through explicit prompts, fixed interfaces, automated validation, runtime testing, and complete logging of generated code, hyperparameters, metrics, and artefacts. Nevertheless, the variability of generated code and selected pipelines across repeated executions remains an important empirical question and is left to future work.

This aligns with your point: reproducibility is governed by strong guardrails around code generation, prompt engineering, and automated tests.

**Improve FGCS**

Add a variability/reproducibility experiment:

* repeat same dataset/specification/model N times;
* compare generated pipelines;
* compare generated code structure;
* compare final scores;
* compare failure/retry patterns;
* report variance and stability.

Separate:

* **artefact reproducibility**: rerun logged code;
* **execution reproducibility**: rerun logged pipeline with fixed split and hyperparameters;
* **generation reproducibility**: rerun full LLM-driven process.

**Severity / effort**: **Critical / Low for ADBIS, Medium for FGCS**

---

## 4. Budget effect is missing

**Reviewer quote**

> “Experiments should be provided on the effect of the budget (how the number of generated pipelines helps? How the number of executed pipelines help?)” 

Related:

> “The effectiveness of the search space exploration is heavily dependent on the LLM's ability to generate valid code; in some tests (e.g., HAR and MNIST 784), the system failed to explore the full budget because the models could not consistently produce valid pipelines.” 

**Present also in FGCS?**
**Yes.** FGCS reports fixed-budget experiments and actual executed pipelines, but no budget ablation.

**Improve ADBIS**

No room for new experiments. Add a future-work sentence only:

> A systematic analysis of how pipeline budget, retry budget, and execution budget affect performance, cost, and pipeline diversity is left to future work.

Possibly rephrase current “Actual P.” discussion to make clear that budget controls exploration but valid execution depends on successful generation and validation.

**Improve FGCS**

Add budget ablation:

* pipeline budget: 5, 10, 20, 30;
* generation-attempt budget: 1, 3, 5, 10;
* possibly time budget;
* metrics:

  * best score;
  * number of valid scripts;
  * number of executed pipelines;
  * runtime;
  * tokens;
  * cost.

**Severity / effort**: **High / Low for ADBIS, Medium for FGCS**

---

## 5. Valid-code generation bottleneck needs clearer framing

**Reviewer quote**

> “The effectiveness of the search space exploration is heavily dependent on the LLM's ability to generate valid code; in some tests (e.g., HAR and MNIST 784), the system failed to explore the full budget because the models could not consistently produce valid pipelines.” 

**Present also in FGCS?**
**Yes.** FGCS discusses actual executed pipelines and notes that validity/executability affects performance, but it does not deeply analyze the failure modes.

**Improve ADBIS**

Rephrase around the role of the guardrailed loop:

> The number of actually executed pipelines depends not only on the nominal exploration budget, but also on whether the LLM-generated code passes semantic validation and runtime tests within the retry budget. Thus, Actual P. should be interpreted as the effective exploration achieved after guardrailed generation and validation.

Promise deeper analysis:

> A detailed taxonomy of generation, validation, and execution failures is left to future work.

**Improve FGCS**

Add failure taxonomy:

* invalid syntax;
* missing imports;
* wrong estimator interface;
* missing hyperparameter;
* extra pipeline step;
* incompatible preprocessing;
* runtime error;
* failed semantic validation;
* exhausted retry budget.

Report per dataset/model if available.

**Severity / effort**: **High / Low for ADBIS, Medium for FGCS**

---

## 6. Table columns and runtime/cost interpretation are unclear

**Reviewer quote**

> “The meaning and interpretation of the different columns in tables 2 and 3 is not clearly explained.” 

Also:

> “The claim about the balanced distribution between LLM inference and ML training is not clearly explained. Where exactly does it come from?” 

And:

> “In multiple datasets (e.g., Adult and California Housing), LLM inference accounted for more than 70% of the total execution time, indicating potential inefficiencies in prompt design or the agentic loop.” 

**Present also in FGCS?**
**Partially.** FGCS has more detail and time-decomposition figures, but still benefits from clearer definitions.

**Improve ADBIS**

This is one of the best low-effort fixes. Add/rephrase one compact sentence near Tables 2–3:

> `Actual P.` denotes the number of pipelines successfully generated, validated, and executed within the budget; token columns report aggregate LLM usage; putative cost is estimated from token usage; lower scores are better for regression tasks using RMSE, whereas higher scores are better for classification tasks using balanced accuracy.

For the “balanced distribution” claim, either remove it or make it numeric and cautious. Better:

> Gemini 3.1 Flash Lite shows a more favourable execution profile in our runs, because it reaches the pipeline budget more consistently while producing fewer output tokens than Gemini 2.5 Flash.

**Improve FGCS**

* Define each column explicitly
* Explain wall-clock vs accumulated/equivalent time
* Add ratios for LLM inference vs ML training
* Avoid qualitative claims unless supported by ratios

**Severity / effort**: **High / Very low for ADBIS, Low for FGCS**

---

## 7. Specification grammar is missing

**Reviewer quote**

> “Listing 1 is fine, but a grammar should be provided” 

**Present also in FGCS?**
**Mostly addressed but not fully.** FGCS and supplementary material contain much fuller syntax and semantics, but still may not include a compact grammar/EBNF. The supplementary material does describe the YAML-like syntax and constraints in detail .

**Improve ADBIS**

Do **not** add grammar. Use the space-limitation argument.

Suggested sentence:

> Listing 1 reports only the core constructs needed to understand the architecture; a complete account of the syntax and formal semantics of the specification language is omitted for space reasons and delegated to an extended version of this work.

Avoid mentioning supplementary materials in ADBIS.

**Improve FGCS**

* Add full syntax and semantics
* Ideally include:

  * EBNF;
  * YAML schema;
  * semantic validation rules;
  * examples of invalid specifications;
  * mapping to CSP.

**Severity / effort**: **High / Very low for ADBIS, Medium for FGCS**

---

## 8. Expert-knowledge formalization assumes one coherent specification

**Reviewer quote**

> “The formalization of expert knowledge (in this case, data scientists' knowledge) deserves further elaboration. The paper assumes the existence of a single specification expressing the knowledge of a data scientist, but it does not discuss situations where multiple experts contribute to defining constraints. In particular, mechanisms for conflict resolution, prioritization, or the integration of contradictory knowledge are not addressed.” 

**Present also in FGCS?**
**Yes.** FGCS formalizes a single specification and does not deeply address decomposition, reuse, abstraction, priorities, or multi-expert conflict management.

**Improve ADBIS**

State the design assumption, then future work.

Suggested sentence:

> AGE-ML currently assumes that experts collaborate before execution to produce a coherent and consistent specification. Supporting independently authored, reusable, or partially conflicting specification modules would require additional language mechanisms for decomposition, abstraction, priority, and conflict handling, which we leave to future engineering work.

This avoids overpromising “conflict resolution” as a current feature.

**Improve FGCS**

Add a future-work subsection or design paragraph on:

* specification modules;
* reusable rule libraries;
* abstraction mechanisms;
* hard vs soft constraints;
* priorities;
* provenance of rules;
* conflict detection via CSP unsatisfiability;
* possible use of unsat cores for diagnostics.

**Severity / effort**: **High / Low for ADBIS, Medium for FGCS**

---

## 9. Direct editing and selective re-execution are missing

**Reviewer quote**

> “While the framework allows for expertise injection at the start, it currently lacks the capability for data scientists to directly edit or selectively re-execute specific components of a pipeline once the automated process has begun.” 

Also:

> “Provide more detail on the feasibility of the proposed "direct editing" feature, as this is a critical requirement for true data-centric AI.” 

**Present also in FGCS?**
**Partially.** FGCS already mentions direct editing and selective re-execution as future work, but feasibility can be better articulated.

**Improve ADBIS**

Make this a high-priority future-work sentence:

> A direct next step is to support human editing of generated pipeline scripts and selective re-execution of only the affected runs, while preserving provenance in the data catalog. This would make the current specification-first workflow more interactive and better aligned with iterative data-centric practice.

**Improve FGCS**

Add architecture-level detail:

* editable generated script state;
* invalidation of affected runs;
* rerun only modified pipeline;
* provenance of human edits;
* validation after manual edit;
* MLflow lineage update.

**Severity / effort**: **High / Low for ADBIS, Medium for FGCS**

---

## 10. High inference latency and redundant context require mitigation

**Reviewer quote**

> “The authors should discuss strategies for reducing the high inference latency and redundant conversational context mentioned in the limitations.” 

**Present also in FGCS?**
**Partially.** FGCS mentions token usage and future prompt/context optimization, but can be more concrete.

**Improve ADBIS**

Add one compact future-work phrase:

> Future work will also target latency and token reduction through prompt compression, reduced conversational context, caching of dataset summaries, and stronger deterministic checks before invoking LLM-based validation.

**Improve FGCS**

Expand with concrete mechanisms:

* prompt compression;
* structured outputs;
* reusable code templates;
* cache dataset summaries;
* cache validated code fragments;
* regex/static checks before LLM judge;
* shorter repair contexts;
* model specialization for generation vs validation.

**Severity / effort**: **Medium-High / Low**

---

## 11. Heuristic search beyond symbolic enumeration should be discussed

**Reviewer quote**

> “Elaborate on how future versions might move beyond symbolic enumeration toward more efficient heuristic-based search strategies to improve exploration diversity.” 

**Present also in FGCS?**
**Partially.** FGCS already mentions smarter search strategies as future work, but without much detail.

**Improve ADBIS**

One sentence in future work:

> Another direction is to retain CSP-based admissibility checking while replacing uniform/random sampling with heuristic or diversity-aware strategies for ranking and selecting valid pipelines under budget constraints.

**Improve FGCS**

Elaborate possible methods:

* diversity-aware CSP solution sampling;
* heuristic ranking;
* Bayesian optimization over pipeline families;
* multi-armed bandits;
* warm-start from prior runs;
* meta-learning over logged experiments.

**Severity / effort**: **Medium-High / Low**

---

## 12. Multi-agent framing is not explicit enough after the introduction

**Reviewer quote**

> “Being a multi-agent system in only mentioned in the introduction, but later it is not that explicit (eg, Figure 3 is confusing)” 

**Present also in FGCS?**
**Mostly no.** FGCS is already clearer about planner, executor, evaluator, and catalog roles .

**Improve ADBIS**

Given your positioning for a database venue, do **not** increase the MAS emphasis substantially. Just reduce confusion.

Minimal rephrase:

> Figure 3 describes the control loop of an executor agent, not the whole multi-agent architecture.

And keep the database/MLOps focus on:

* specification;
* constraints;
* data catalog;
* reproducibility;
* pipeline artefacts.

**Improve FGCS**

No major action. Ensure figure captions distinguish:

* overall architecture;
* executor-agent state machine;
* catalog/logging hierarchy.

**Severity / effort**: **Medium / Very low**

---

## 13. Classification/regression scope appears ambiguous

**Reviewer quote**

> “At some point seems that only classification problems can be solved, but then the experiments show also regressions.” 

**Present also in FGCS?**
**Mostly no.** FGCS states classification and regression as supervised tasks, but the broader practical claim should be sharpened.

**Improve ADBIS**

Use your actual scope: any scikit-learn-style fittable estimator can be supported.

Suggested sentence:

> Although the examples focus on classification for brevity, AGE-ML is not restricted to classifiers: in practice, any estimator following the scikit-learn fitting interface can be used as a candidate, and our experiments cover both classification and regression as common and easily interpretable use cases.

**Improve FGCS**

Make the same point more formally:

* AGE-ML supports candidate algorithms compatible with the expected generated-code interface;
* classification/regression are experimental instances;
* other estimators/tasks require suitable specification entries, metrics, and evaluation protocols.

**Severity / effort**: **Medium / Very low**

---

## 14. Supplementary materials references are problematic in ADBIS

**Reviewer quote**

> “Where are "supplementary materials"? does this refer to the GitHub repository? In which file/folder?” 

The ADBIS text currently contains:

> “The supplementary materials include examples of generated explanations.” 

and:

> “Full prompt definitions and implementation details are available on the repository7 and in the supplementary materials.” 

**Present also in FGCS?**
**No real issue.** FGCS has a real supplementary document.

**Improve ADBIS**

Remove all references to supplementary materials. Replace with repository-only references when needed.

Suggested replacements:

> Examples of generated explanations are available in the project repository.

and:

> Full prompt definitions and implementation details are available in the project repository.

Do not mention supplementary material at all.

**Improve FGCS**

Keep supplementary references, but make them exact:

* title;
* appendix/section;
* repository folder for prompts and generated artefacts.

**Severity / effort**: **Medium / Very low**

---

## 15. Dataset descriptions and complexity are insufficient

**Reviewer quote**

> “Dataset characteristics provided in table 1 are interesting, but they not necessarily reflect the complexity of the problem.” 

Also:

> “a small description of each dataset would be helpful” 

**Present also in FGCS?**
**Partially fixed.** FGCS already contains dataset descriptions. It could still add better complexity indicators.

**Improve ADBIS**

No room for real descriptions. Add one sentence:

> The datasets were selected to cover heterogeneous settings in terms of task type, dimensionality, number of instances, and feature types; a more detailed dataset-level complexity analysis is left to extended work.

If a table caption can be changed, mention that the table reports only coarse descriptors.

**Improve FGCS**

Add dataset complexity indicators:

* number of classes;
* class imbalance;
* missingness;
* categorical ratio;
* dimensionality/instance ratio;
* target skew for regression.

**Severity / effort**: **Medium / Low**

---

## 16. Compact dataset description generation is underspecified

**Reviewer quote**

> “how is the compact description of the dataset structure obtained? Is it metadata / generated by an agent / ...?” 

**Present also in FGCS?**
**Partially.** FGCS says dataset summaries, schema information, feature statistics, or samples may be used, but the precise procedure can be clearer.

**Improve ADBIS**

Add one short clarification:

> The compact dataset description is computed from deterministic metadata and summary statistics, such as column names, inferred types, cardinalities, missingness, and small samples; LLMs are only used to interpret semantic predicates when needed.

**Improve FGCS**

Specify exact fields and responsibility:

* which component computes it;
* whether samples are included;
* how many rows;
* privacy safeguards;
* which parts are deterministic vs LLM-interpreted.

**Severity / effort**: **Medium / Very low for ADBIS, Low for FGCS**

---

## 17. Agent-level cost and impact are not separated

**Reviewer quote**

> “More details should be provided on the separate cost and impact of each one of the agents.” 

**Present also in FGCS?**
**Partially.** FGCS describes agent roles but reports mostly aggregate cost/time.

**Improve ADBIS**

Given your decision, do not add anything unless a sentence can be inserted without cost:

> The reported costs are aggregate over the complete AGE-ML run; a per-agent cost attribution requires additional instrumentation and is left to future work.

**Improve FGCS**

Only collect/report this if FGCS reviewers ask, or if instrumentation is cheap. Candidate metrics:

* LLM calls per agent;
* tokens per agent;
* runtime per agent;
* validation failures per executor;
* retry counts.

**Severity / effort**: **Medium / Very low for ADBIS, Medium for FGCS but optional**

---

## 18. Formality and precision of claims need tightening

**Reviewer quote**

> “Lacks some formality and precision in the explanations and claims” 

**Present also in FGCS?**
**Partially.** FGCS is more formal, but broad claims still need care.

**Improve ADBIS**

This should be handled through wording, not new content. Avoid unqualified claims.

Rephrase:

* “ensures reproducibility” → “supports artefact-level reproducibility through logging and validation”
* “improves data quality” → “selects data-preparation steps suited to the data and estimator”
* “explainable” → “traceable and inspectable”
* “optimal pipeline” → “best pipeline found within the explored budget”
* “guarantees correctness” → “checks compliance through validation and runtime tests”

**Improve FGCS**

Add a claim/evidence/limitation table if space allows, or tighten prose throughout.

**Severity / effort**: **Medium / Very low**

---

## 19. Presentation and formatting issues

**Reviewer quote**

> “Presentation should be improved” 

Specifics:

> “Figure 4 size should be reduced”
> “Font size in table 1 should be reduced”
> “Caption of table 1 should be underneath (like in the others).”
> “Figure 1 should have a legend with the meaning of the arrows.”
> “Machine Learning should be shortened as ML everywhere.”
> “use bold font for numbers surpassing the baselines would be helpful to read more easily the table”
> “Typos: - p13 : space after the parenthesis "( Wilt..." - same for "( California..."”  

**Present also in FGCS?**
Mostly ADBIS-specific, but an editorial pass also helps FGCS.

**Improve ADBIS**

Do all formatting fixes that do not add text:

* reduce Figure 4 size
* reduce Table 1 font if needed
* move Table 1 caption underneath
* add/clarify Figure 1 legend if possible without adding much text
* replace repeated “Machine Learning” with “ML” after first definition
* bold values surpassing baselines
* fix listed typos
* remove supplementary-material references

**Improve FGCS**

Run same consistency pass.

**Severity / effort**: **Medium / Very low**

---

## 20. Evaluation protocol is promising but incomplete

**Reviewer quote**

> “Overall, the paper presents an interesting approach that may provide valuable contributions to the community. However, several aspects deserve further investigation and development, particularly regarding the impact on data quality, the evaluation protocol, and the integration and management of expert knowledge.” 

**Present also in FGCS?**
**Yes.** FGCS has a fuller experimental section but should absorb the deeper evaluation requests.

**Improve ADBIS**

Do not expand experiments. Add one calibrated sentence:

> The present evaluation focuses on predictive performance, execution feasibility, and cost under a fixed budget; future work will extend it with budget sensitivity, generation-variability analysis, and data-oriented metrics.

**Improve FGCS**

Add, in priority order:

1. generation variability/reproducibility;
2. budget sensitivity;
3. data-centric behaviour/preprocessing analysis;
4. failure taxonomy;
5. explanation-quality assessment.

**Severity / effort**: **Medium / Low for ADBIS, High for FGCS**

---

## 21. Source-code availability and reproducibility instructions

**Reviewer quote**

> “Code is openly provided” 

Also:

> “The authors make the source code publicly available through a GitHub repository, which supports reproducibility.” 

**Present also in FGCS?**
**Yes.** Both ADBIS and FGCS mention the repository.

**Improve ADBIS**

Do not add reproduction instructions to the paper. Forward readers to the repository:

> Reproduction instructions, scripts, prompts, and configuration files are provided in the project repository.

**Improve FGCS**

Same principle, but ensure the repository actually contains:

* README;
* environment file;
* run scripts;
* dataset acquisition instructions;
* prompt files;
* configuration files;
* expected output artefacts;
* paper table reproduction instructions;
* commit/tag for the paper version.

**Severity / effort**: **Medium / Very low in paper, Medium in repository**

---

## Updated minimal revision strategy for ADBIS

Given the page constraint and acceptance status, the best strategy is **not to add new material**, but to reduce reviewer-visible overclaims and ambiguity.

### Must-do wording fixes

1. **Narrow “explainability”**

   * Replace broad “explainable” with “traceable”, “inspectable”, “process-level explanation”, or “pipeline-generation rationale”
   * Add one sentence saying model-level explanation is future work

2. **Narrow “data-centric”**

   * Clarify that AGE-ML is data-centric because the pipeline is selected for the data at hand and may include preprocessing, feature handling, rebalancing, and model-dependent data preparation
   * Do not claim direct data-quality improvement unless measured

3. **Clarify reproducibility**

   * Say reproducibility is supported through guardrailed generation, prompt constraints, automated validation/runtime testing, and logged artefacts
   * Promise pipeline/code variability analysis as future work

4. **Clarify estimator/task scope**

   * Say AGE-ML can support any scikit-learn-style fittable estimator; classification/regression are used because they are common and easy to interpret

5. **Remove supplementary-material references**

   * Replace with repository references or delete

6. **Clarify tables**

   * Define `Actual P.`, token columns, putative cost, and metric direction in one compact sentence
   * Remove or weaken the “balanced distribution” claim unless numerically supported

7. **Grammar issue**

   * State that complete syntax/semantics are omitted due to space and delegated to an extended version

8. **Expert-knowledge issue**

   * State that current AGE-ML assumes a coherent collaborative specification
   * Promise future language engineering for modularity, abstraction, decomposition, reuse, and priority mechanisms

9. **Direct editing**

   * Make it a high-priority future-work item

10. **Presentation cleanup**

* Fix figures, captions, table readability, abbreviation consistency, bold baselines, and typos

### ADBIS future-work sentence bundle

A compact paragraph could cover many reviewer concerns:

> Future work will address several limitations that are orthogonal to the core architecture presented here: analysing the variability of generated pipelines and code across repeated executions; studying the effect of pipeline, retry, and time budgets; reducing latency and token usage through prompt compression, caching, and stronger deterministic validation; supporting direct human editing and selective re-execution of generated pipelines; and extending the specification language with modularity, reuse, abstraction, and priority mechanisms for large or collaboratively authored specifications.

### ADBIS claim-control sentence bundle

A compact paragraph could replace overclaiming:

> AGE-ML is data-centric in the sense that pipeline generation is conditioned on the data at hand and may include preprocessing, feature handling, rebalancing, and other data-preparation steps required by the selected estimators. Its explainability is process-level: the system records and summarizes the generation, validation, execution, and selection of pipelines, rather than explaining individual model predictions.

### What not to do in ADBIS

* Do not add appendix
* Do not add grammar
* Do not add new experiments
* Do not add per-agent cost analysis
* Do not discuss supplementary materials
* Do not overemphasize multi-agent systems beyond avoiding figure confusion
* Do not claim data-quality improvement, model explainability, or deterministic LLM reproducibility.
