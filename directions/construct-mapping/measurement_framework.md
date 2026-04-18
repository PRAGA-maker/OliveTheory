# Measurement Framework: Escape Motivation

Last substantive revision 2026-04-18. Replaces the earlier CEMP (Cortical Escape Motivation Profile) framework, which is now stale — this doc represents a deeper, more honest reading of the construct-mapping space.

This is an evolving working doc, not a final architecture. Structure:

1. **Problem space** — what we're actually trying to measure and why it's hard
2. **Solution space** — the different legitimate ways to view this problem
3. **X ≈ Y equivalences** — where different literatures appear to describe the same underlying thing
4. **Papers in contention** — the frontier, ordered by relevance to our use case
5. **An opinionated take** — my read, at the end, as one option among several

---

## 1. Problem space

### What we're trying to measure

A 988 caller on ~2 minutes of hold is making a continuous stay-or-hang-up decision. We want an instrument that, given a candidate hold-music clip, tells us whether that music will shift the caller toward staying or toward hanging up. Because we cannot ethically scan callers during the hold, the instrument has to work off **TRIBE-predicted brain activation in response to the music**, not real fMRI data.

Concretely, the instrument needs to:
- Take fMRI-typed input (a predicted BOLD timecourse over some set of regions, produced by TRIBE given the music)
- Produce a scalar (or vector) score interpretable as "how strongly does this music push the listener toward escape vs. stay?"
- Be **mechanistically derived**, **theoretically motivated**, and **empirically validated in a suicidal-crisis-adjacent population** — so that we can defend the score as measuring something real, not a post-hoc fit.

### Why this is hard

Four distinct difficulties compound:

1. **"Escape motivation" is not a canonical construct.** It appears in behavioral health (Iwata's functional analysis of behavior), in ACT/experiential-avoidance literature (Chapman/Hayes), in negative-reinforcement models of addiction (Koob, Baker), and in suicidology as a theoretical shadow of Shneidman's psychache. No single literature owns it, and no published nomological network links the versions across disciplines.

2. **The 988 scenario is unmapped.** The intersection of {escape motivation, crisis-hotline hold, suicidal caller, music} has zero empirical studies. Tan 2025 is the only music-in-target-pop neural study and it's a small pilot. Hold-music neuroimaging in *any* psychiatric population is zero studies. We're operating in a literature void on the scenario axis.

3. **Most comp-psych of suicide is trait, not acute.** Dombrovski, Millner, Brown, Karvelis, Vanyukov — all study suicidality as trait (history-based) or recent-but-not-acute states. The "active crisis at time of testing" subpopulation has no computational-neural data. We can't get "what the 988 caller's brain looks like right now" from any existing dataset.

4. **Brain→parameter mapping in target pop barely exists.** Pedersen 2021 provides the methodology we want (trial-by-trial BOLD as regressor on DDM parameters) but in MDD-only. Nobody has reproduced that structure in an SI/SA sample. Ji 2021 comes closest (4-param Bayesian model + fMRI in acute depressed attempters) but uses BART not a DDM, and maps to insula/dlPFC not the subcortical DDM circuit.

### Two functions, not one

The instrument and its validation are actually two separable jobs:

- **Function 1 — the instrument itself.** A mechanism for turning TRIBE-predicted brain activation into an escape-motivation-like score.
- **Function 2 — the benchmark.** Evidence that TRIBE (possibly fine-tuned) predicts target-population-like patterns at all.

Everything below is organized around both. Papers rarely serve both; the honest story is a combination.

---

## 2. Solution space

There are several different legitimate *ways to view* the problem. I'll enumerate them, because which view you pick changes which papers matter.

### View A: Computational-parameter view
Frame escape motivation as a **set of decision-process parameters** — drift rate, starting-point bias, decision threshold, learning rate, Pavlovian bias — that differ in target population and can be inferred from brain activation patterns. Under this view, the instrument is a model that maps BOLD → parameters → behavior, and "escape motivation" means something like "active-escape bias" or "pain-avoidance parameter." Pedersen's structure. Millner's RL-DDM. Karvelis's active-inference variables.

### View B: Neural-fingerprint view
Frame escape motivation as a **characteristic brain-activation pattern** that distinguishes target-population-in-a-decision-state from controls. Under this view, the instrument just measures how similar TRIBE's predicted BOLD looks to the published attempter-fingerprint (e.g., Brown 2020's reduced vmPFC value + abolished vmPFC-frontoparietal impulsivity-connectivity, Dombrovski 2013's blunted ventral-striatal RPE, Ji 2021's reduced left insula during high-risk decisions). No explicit parameter inference — just pattern matching.

### View C: Phenomenological-construct view
Frame escape motivation as a **recognized clinical construct** (entrapment, psychache, frantic hopelessness, ASAD) with a validated self-report scale. Under this view, the brain model doesn't measure escape motivation at all — it predicts which music will reduce entrapment/psychache in a validation sample. The measurement is behavioral; the brain model is just a ranking aid.

### View D: Operational view
Frame escape motivation as **caller patience** (a Lifeline ops metric — time-to-hang-up in the queue). Under this view, the instrument is just a predictor of behavioral dropout under various music conditions. No psychological theory necessary. The brain model is optional.

### View E: Sustained-decision-dynamics view
Frame escape motivation as a **time-accumulating fatigue/disengagement signal** — Muller 2021's RCZa/RCZp fatigue dynamics, effort-based decision-making, belief decay (Karvelis λ). Under this view, what matters is not the instantaneous state but the trajectory over the 2-minute hold: does the music keep fatigue/hopelessness from accumulating?

**These views are not mutually exclusive.** A full pipeline could combine A (parameter inference) + B (fingerprint matching) + C (validation against self-report) + D (behavioral endpoint) + E (sustained-dynamics overlay). But picking a primary view shapes which papers drive the design.

---

## 3. X ≈ Y equivalences (the interesting network)

These are the places where different literatures appear to describe the same underlying construct with different vocabulary. They matter because (a) they let us triangulate evidence across literatures, (b) they tell us which "different" constructs are actually synonyms under the hood, and (c) some of these equivalences are writable as construct-validity claims in their own right.

I have verified each of these via direct text readings (Karvelis 2022, Pedersen 2021, Brown 2020, Ji 2021, Millner 2018/2019, Kleiman 2018). Some are cited in those papers; some are my synthesis.

### Equivalences about the escape *mechanism*

| Left | ≈ | Right | Basis |
|---|---|---|---|
| **Shneidman 1993 psychache** | ≈ | **Karvelis 2022 negative instrumental beliefs about state transitions** | Both = "I cannot make my pain stop through my actions." Karvelis's active-inference formalization gives the math; Shneidman gives the phenomenology. Karvelis cites Shneidman explicitly. |
| **Ji 2021 pain avoidance (TDPPS subscale)** | ≈ | **Shneidman 1993 psychache** | Ji explicitly uses the Li et al. 2014 Three-Dimensional Psychological Pain Scale, which operationalizes Shneidman. Ji's "pain-avoidance is the strongest predictor" is Shneidman with a measurable scale. |
| **Iwata 1982/1994 escape function (behavior analysis)** | ≈ | **Chapman et al. 2006 experiential avoidance of DSH (ACT)** | ≈ | **Millner 2019 active-escape bias (comp psych)** | Three different disciplines describing "behavior that functions to terminate an aversive state." Differ mainly on whether the aversive state is external (Iwata), internal (Chapman), or parameterized computationally (Millner). |
| **Guitart-Masip 2012 Pavlovian-instrumental transfer (PIT)** | ≈ | **Millner 2019 active-escape bias** | Same underlying mechanism — Pavlovian bias invading instrumental decision-making — with Millner explicitly extending PIT from appetitive to aversive-escape. Same math. |
| **Mobbs 2020 defensive flight (imminent-threat)** | ≈ (trial-level) | **Millner 2019 active escape (aversive-sound trial)** | Both recruit PAG/insula/dACC. Mobbs emphasizes reactive/subcortical; Millner uses explicit RL-DDM. Different timescales, same neural machinery. |

### Equivalences about the *decay / quit / fatigue* dynamics

| Left | ≈ | Right | Basis |
|---|---|---|---|
| **Muller 2021 unrecoverable fatigue (RCZa/MFG/insula)** | ≈ | **Karvelis 2022 belief decay λ (dPFC-LC-mediated)** | Both = "accumulated evidence that my actions aren't producing desired outcomes." Muller frames as effort fatigue; Karvelis frames as Bayesian belief updating. Same shape: an integrator that updates a decision threshold downward. |
| **Beck trait hopelessness (BHS)** | ≠ | **Kleiman 2017 EMA hopelessness** | Explicitly distinct. Kleiman's EMA data shows hopelessness correlates concurrently with SI but does NOT predict short-term change, challenging Beck's trait interpretation. Same word, different timescale constructs. |
| **Galynker SCS "frantic hopelessness"** | ≈ (temporal variant) | **Gilbert 1998 entrapment** | Q1 analysis: "Defeat → Entrapment → Psychache → Crisis (ASAD/SCS)" is a temporal progression of what may be one underlying state. High cross-sectional collinearity (r > 0.60). |

### Equivalences in *neural-circuit disruption*

| Left | ≈ | Right | Basis |
|---|---|---|---|
| **Jenkins 2018 "failure to sustain NAcc activity to preferred music" (MDD)** | ≈ | **Brown 2020 "disrupted vmPFC value signal" (attempters)** | ≈ | **Dombrovski 2013 "blunted ventral striatal RPE" (attempters)** | Three tasks (music, bandit, reversal learning), three regions (NAcc, vmPFC, ventral striatum), one underlying claim: **reward-circuit value encoding is attenuated in depressed/attempter populations**. Probably the same mechanism viewed through different measurement windows. |
| **Brown 2020 vmPFC value signal in attempters** | ≈ | **Karvelis 2022 vmPFC-controllability inference (w)** | Brown: attempter vmPFC value encoding is disrupted. Karvelis: vmPFC encodes expected outcome / controllability inference. If controllability is disrupted, Karvelis predicts stronger Pavlovian escape. Mechanism unified. |
| **Olié 2015 blunted rACC to sad faces (attempters)** | ≈ | **Karvelis 2022 ACC encoding of action-state beliefs (hopelessness)** | Both attribute ACC to action-outcome belief representations. Karvelis cites Olié directly. |

### Equivalences about the *caller's operational state*

| Left | ≈ | Right | Basis |
|---|---|---|---|
| **Lifeline "caller patience"** | ≈ | **Karvelis 2022 stressor controllability w** | Both = "how long someone will stay in an aversive situation when they believe they can't affect when relief arrives." My synthesis (not cited in either), but direct mapping: low caller patience = low w = more Pavlovian escape = hang up. |
| **SAMHSA/OES 2024 "process transparency" recommendation** | ≈ | **Karvelis 2022 w elevation via controllability inference** | OES recommends giving callers visibility into queue progress. Karvelis would predict this raises w → lowers Pavlovian escape → reduces hang-ups. Independent operational arrival at a mechanism prediction. |

### What these equivalences buy us

- **Multiple vocabulary layers for the same claim**, which lets us defend a model to audiences from different disciplines (operations, clinical, computational).
- **A testable structure**: if Karvelis's parameter-to-region mapping is right, then the reward-circuit disruption triad (Jenkins / Brown / Dombrovski) should be mathematically equivalent when re-expressed in Karvelis's parameters.
- **A reason to be suspicious of some "distinctions."** E.g., the Beck trait-hopelessness ↔ Kleiman state-hopelessness mismatch is a real confound in the older literature that newer EMA work has already partially resolved.

---

## 4. Papers in contention (the frontier)

Ordered by how directly the paper serves our specific use case (988 hold music + TRIBE-based instrument + target pop). This is **not** a ranking of paper quality or scientific importance — it's a ranking of "how much work does this paper save us for what we're trying to build."

### Tier 1 — Direct brain↔parameter↔target-pop instrument candidates

**(1) Ji et al. 2021** — J Psych Res 139:14-24
- `context/papers/ji2021_motivation_decision_suicide.pdf`
- **Why it matters**: Closest-available thing to what we need. Acute-episode, unmedicated, depressed attempters (n=23 SA + 30 NS + 30 HC). fMRI + computational model (4-param Bayesian BART) + parameter-to-region mapping (insula ↔ pain avoidance / risk aversion; dlPFC ↔ loss sensitivity). Pizzagalli on author list (McLean).
- **What it doesn't cover**: BART not DDM (different task dynamics); insula/dlPFC not Pedersen's subcortical DDM circuit (NAcc/pgACC/STN); correlational not joint estimation; sample is explicitly **"planful, non-impulsive, non-BPD"** — excludes impulsive attempter subtype and non-depressed acute-crisis.
- **How we'd use it**: as the empirical parameter-region anchor for the "pain avoidance / risk aversion / loss hypersensitivity" axis, scope-limited to the planful-depressive subtype. Valid for the modal 988 caller; not valid for all.

**(2) Brown, Wilson, Hallquist, Szanto & Dombrovski 2020** — Neuropsychopharmacology 45:1034-1041
- `context/papers/brown2020_vmpfc_suicide.pdf`
- **Why it matters**: Target-pop fMRI (n=116: 35 attempters + 25 ideators + 25 depressed + 31 HC) with RL model + PPI-based connectivity analysis. Specific findings: (a) vmPFC value signals reduced in attempters vs HC, above depression; (b) normal vmPFC-frontoparietal impulsivity-connectivity moderation is **abolished in attempters specifically** (preserved in depressed controls). Disrupted choice quality follows from the connectivity abolition.
- **What it doesn't cover**: late-life (age 47-79, mean ~62); task is 3-armed bandit, not escape. The connectivity-abolition finding is qualitatively distinct from value-signal disruption (impulsivity mechanism vs value mechanism), and "suicidal behavior" here includes both impulsive and planned attempts without stratification.
- **How we'd use it**: as the **connectivity-pattern benchmark** for Function 2. Fine-tuned TRIBE should predict vmPFC-pattern attenuation *and* frontoparietal-connectivity-impulsivity-abolition when running on simulated-attempter input.

**(3) Karvelis & Diaconescu 2022** — Computational Psychiatry 6:34-59
- `context/papers/karvelis2022_active_inference_suicide.pdf`
- **Why it matters**: Integrated active-inference framework unifying hopelessness + Pavlovian bias + active-escape bias in one generative model with four mechanistic perturbations (k, c, m, w₀) and an explicit neurocircuit mapping (LC-NE, DRN-5-HT, Amy-dPFC-ACC-vmPFC). Simulations replicate Millner 2019 behavioral findings. Theory-level integration of the most disparate constructs.
- **What it doesn't cover**: proof-of-concept only — no empirical fit to data. The parameter-to-region mapping is theoretical, not validated. No direct neural imaging. Subcortical regions (LC, DRN, Amy) are exactly where TRIBE is weakest.
- **How we'd use it**: as the theoretical engine. Gives us the *structure* of what brain-to-parameter mapping should look like; tells us which regions to regress on which parameters; predicts subtypes (impulsive vs planful). Pair with Ji/Brown for empirical grounding.

**(4) Pedersen et al. 2021** — PLOS Computational Biology 17(5):e1008955
- `context/papers/pedersen2021_aac_ddm.pdf`
- **Why it matters**: Methodology scaffold. Explicit trial-by-trial BOLD-as-regressor structure on DDM parameters: v ~ caudate×reward + pACC×aversiveness, a ~ STN×conflict, z ~ NAcc×PavlovianBias. Tells us *how* to turn brain activation time-series into decision-parameter time-series.
- **What it doesn't cover**: 18 MDD female, not SI/SA. Wrong population. Subcortical regions (NAcc, STN) are weak in TRIBE — this is a secondary blocker.
- **How we'd use it**: not as a clinical anchor, but as a methodological blueprint. The regression structure is what we'd re-apply with TRIBE output + Karvelis's target-pop parameter priors.

### Tier 2 — Behavioral validation / ground truth

**(5) Millner et al. 2019** — J Abnormal Psychology 128(2):106
- `context/papers/millner2019_active_escape.pdf`
- **Why it matters**: RL-DDM operationalization of "active escape bias" in n=85 STB veterans (including 26 with past-year attempt) + 44 psychiatric controls. Direct computational-behavioral measurement in target pop. Bias parameter uniquely predicts group status *beyond* hopelessness/depression — meaning "active escape bias" is not just a depression proxy.
- **What it doesn't cover**: No neural imaging. Aversive-sound task is single-tone (fork-on-slate), so extending to music is an assumption. Trial-level, not sustained.
- **How we'd use it**: as behavioral validation target. If our TRIBE-based instrument is well-calibrated, it should correlate with Millner-style active-escape-bias in a target-adjacent behavioral validation sample.

**(6) Jaroszewski, Millner et al. 2025** — J Psychopathol Clin Sci
- Not yet pulled (paywalled via APA PsycNet).
- **Why it matters**: Direct follow-up to Millner 2019 with **suicide-specific stimuli** (n=360 with 3-month active SI). Found past attempters show *weaker* escape bias for suicide-related stimuli (habituation/desensitization). Critical nuance for attempter-vs-ideator distinction.
- **How we'd use it**: tells us Millner-style measurement should be stimulus-general, not assume escape-bias is unidirectional across stimulus types.

**(7) Dombrovski et al. 2013** — JAMA Psychiatry 70(10):1020-1030
- Paywalled, but summary context exists across Karvelis + Q2/Q5 outputs.
- **Why it matters**: fMRI + RL in late-life attempters. Blunted ventral-striatal reward prediction error. Classic neural-fingerprint finding for attempter physiology.
- **What it doesn't cover**: maps RL *signals* (RPE, expected value) to regions, not *parameters* (learning rate, temperature). Late-life only. Reversal learning, not escape.
- **How we'd use it**: as the "Dombrovski bridge" (Kimi's recommended drop-in for theoretical grounding). The striatal-RPE finding can be argued as the neural substrate of Millner's escape bias via shared dopaminergic/RL machinery — but the argument has known weak links (phasic vs tonic signals, different populations, different tasks).

### Tier 3 — Phenomenological / clinical construct anchors

**(8) Shneidman 1993 psychache** — books + scales (Mee/Orbach TDPPS, Li 2014 TDPPS, Psychache Scale)
- Not pulled as standalone paper; well-covered in the cited works.
- **Why it matters**: the phenomenological backbone. "Suicide is escape from unbearable psychological pain." Ji 2021 measured it directly via TDPPS. Karvelis formalized it as negative instrumental beliefs. If the instrument loses sight of this, it has lost the clinical point of the exercise.
- **How we'd use it**: as the construct the instrument ultimately *measures*, articulated clinically rather than computationally. Reviewers will want to see this explicitly.

**(9) Gilbert & Allan 1998 entrapment + O'Connor IMV model**
- Well-validated clinical literature; Entrapment Scale (16-item) and Brief Entrapment Scale (De Beurs 2020, 4-item).
- **Why it matters**: most empirically validated construct on the escape axis, with real EMA data (Littlewood 2019: 6 assessments/day × 7 days, n=51 suicidal history, entrapment predicts SI at 3-hour lags).
- **How we'd use it**: as the self-report ground truth for validation studies. What Brown/Ji's brain patterns should correlate with.

**(10) Galynker SCS + Rogers/Joiner ASAD**
- **Why it matters**: two acute-state constructs with good near-term attempt prediction validity. SCS is fluctuating pre-crisis; ASAD is spike-like escalation. Neither has EMA or fMRI validation yet.
- **How we'd use it**: as the clinical framing for acute-crisis relevance. These are what the 988 caller is in the middle of.

### Tier 4 — Audio-pathway benchmarks

**(11) Tyron et al. 2025 JAD** — LDAEP meta-analysis in suicidality
- Not yet pulled.
- **Why it matters**: cheap sanity-check on the auditory pathway. Does fine-tuned TRIBE predict any loudness-dependence asymmetry in auditory cortex between simulated SI and HC? Independent of the escape-motivation instrument itself.
- **Reliability**: mixed — some studies find elevated LDAEP in acute SI, others blunted in attempters. Unreliable as standalone marker but useful as sanity check.

**(12) Shukuroglou et al. 2023 + Sun et al. 2024 Cell Reports**
- Not yet pulled.
- **Why it matters**: first two studies showing music ↔ reward-circuit coupling in treatment-resistant depression (the latter via implanted BNST-NAc electrodes). Closest-available target-adjacent music-reward neural evidence.
- **How we'd use it**: as Function-2 benchmarks — does fine-tuned TRIBE reproduce music-induced NAc/reward-circuit engagement patterns in simulated target pop?

### Tier 5 — Real-time dynamics + operational context

**(13) Kleiman 2017 J Abnorm Psych + Kleiman 2018 Current Opinion in Psychology**
- `context/papers/kleiman2018_realtime_monitoring.pdf`
- **Why it matters**: establishes that SI is genuinely hour-scale-episodic, with quick onset and typically <1 hour duration. Our 2-minute hold scenario is squarely within an SI episode. Negative affect predicts time-lagged SI change; hopelessness is a concurrent correlate but NOT a temporal mover. This is what the literature actually says about fast dynamics, and it both validates our timescale and tells us which constructs actually drive minute-scale change.

**(14) Muller et al. 2021 Neuron** — fatigue dynamics, RCZa/RCZp
- Already in the repo as the prior "ruler"; now reframed as one angle among many.
- **Why it matters**: best available model of sustained-decision dynamics over minutes. The RCZa/RCZp → MFG/insula accumulation is a candidate architecture for "fatigue/disengagement" during the hold. Equivalence to Karvelis belief decay (Section 3) is an important bridge — they may be describing the same thing.

**(15) Lifeline Call Center Metrics + SAMHSA/OES 2024** — caller patience / tolerance
- Operational context. Defines the behavioral endpoint (call abandonment) and the operational construct (caller patience). No psychological-mechanism claims but tells us what actually gets measured in practice.

### Demoted or retracted

- **Laessing et al. 2025 bioRxiv** — fabricated by Kimi, does not exist. Retracted from all prior analyses.
- **Dombrovski 2024 Biol Psych "Neural Dynamics..."** — conference abstract only (SOBP May 2024), not peer-reviewed.
- **CEMP (prior repo framework)** — too narrow and prematurely committed to one cortical-only pattern-based measure.

---

## 5. An opinionated take

This section is mine, explicitly one possible read. Treat as a recommendation to evaluate, not a committed design.

### What I think is true

1. **No single paper clears all the criteria.** This isn't a gap we can paper over — it's the literature's honest state. Kimi's three independent second-pass queries each converged on "your exact shape doesn't exist in target pop, you'd need de novo data or you have to synthesize across papers."

2. **The synthesis story is strong even without a single anchor.** Karvelis gives us the theoretical engine. Brown + Ji give us target-pop empirical fingerprints on two different but related tasks (bandit + BART). Pedersen gives us the methodology of trial-by-trial BOLD regression on decision parameters. Millner gives us the behavioral ground truth in target pop. Shneidman/Gilbert give us the clinical framing. Each paper does one specific job; no paper does all.

3. **The equivalences in Section 3 are the actual scientific contribution.** The fact that Shneidman psychache, Karvelis negative-instrumental beliefs, and Ji pain-avoidance all probably describe the same construct via different vocabularies is a *claim we can make*. The fact that Jenkins / Brown / Dombrovski all show reward-circuit attenuation in different tasks and regions suggests one underlying mechanism expressed differently. Making these equivalences explicit in a writeup is much more defensible than picking a single "anchor" and hoping reviewers don't notice the gaps.

### What I think the project should commit to (weakly)

A primary view and a defensible fallback:

- **Primary view (A + B hybrid)**: Treat escape motivation as a **parameter-set** (computational view A) that manifests as a **neural fingerprint** (view B). Specifically: Karvelis's k/c/m/w₀ framework, populated empirically with Brown's vmPFC + Ji's insula/dlPFC target-pop data, applied to TRIBE output via Pedersen's regression methodology. This is "Function 1 done by triangulation."

- **Fallback (view C + D)**: If the computational instrument proves too speculative under review, retreat to behavioral-validation-with-brain-model-as-predictor. The brain model *predicts music that correlates with entrapment-reduction / hang-up-reduction* in a validation sample, without claiming to measure escape motivation directly. This is more honest but also narrower.

- **Overlay (view E)**: Whatever else we commit to, the temporal dynamics over the 2-min hold are important. Muller fatigue or Karvelis belief-decay should be an overlay on the instantaneous parameter estimates.

### What I would not do

- **Commit to any single paper as "the anchor."** Whatever we pick, its limits will show. Better to triangulate and acknowledge the gaps than over-fit to one paper.
- **Use Pedersen as the population-calibration source.** It's good methodology in MDD; using it to calibrate parameters for SI/SA is an over-extrapolation Kimi flagged explicitly.
- **Drop the phenomenological anchors (Shneidman, Gilbert).** They're not measurement instruments but they're how reviewers will translate our computational claims into clinical meaning. Lose them and the paper reads as technocratic.
- **Promise acute-crisis validation we can't deliver.** All target-pop data is non-acute-at-testing. That's a real scope limit we should flag up-front rather than have called out in review.

### Outstanding questions for you to weigh in on

1. **How opinionated do you want the final framework?** My read above picks a primary + fallback, but the alternative is to commit to the fallback-only (view C + D) and let the brain model be purely a predictor not a measurer. That's safer but less ambitious.
2. **Is the subtype-specificity of Ji (planful-depressive only) a dealbreaker or scoping opportunity?** If we accept Ji's scope, the instrument is valid for the modal 988 caller but not all.
3. **Do we want to pursue the construct-validity writeup Kimi flagged** ("active escape bias predicts queue abandonment mediated by entrapment, moderated by psychache")? That's a standalone paper's worth of hypothesis; could be a secondary output.
4. **Is Muller 2021 fatigue or Karvelis belief-decay the temporal-dynamics overlay?** Per Section 3 they may be the same thing expressed differently. Picking one for the architecture vs treating them as interchangeable has implications for which regions we need TRIBE to predict reliably.

---

## What this framework is *not*

- A final architecture. It's a frontier analysis.
- A claim that any specific paper is "the anchor." It explicitly rejects that framing.
- Validated against data. None of this has been empirically tested in our TRIBE pipeline yet.

The earlier CEMP framework is superseded by this doc. The earlier "Muller 2021 as the ruler" decision is superseded — Muller is now one view among several, and the v5/E (sustained-dynamics) view is only one of five legitimate views of the problem.

## Load-bearing papers in `context/papers/`

- `millner2019_active_escape.pdf` — RL-DDM in STB veterans
- `millner2018_active_escape_healthy.pdf` — foundational paradigm paper (healthy subjects)
- `karvelis2022_active_inference_suicide.pdf` — theoretical framework
- `brown2020_vmpfc_suicide.pdf` — vmPFC + connectivity in attempters
- `ji2021_motivation_decision_suicide.pdf` — BART fMRI + 4-param Bayesian in acute depressed attempters
- `pedersen2021_aac_ddm.pdf` — methodology scaffold
- `kleiman2018_realtime_monitoring.pdf` — EMA dynamics overview
- `tribev2.pdf` — brain-encoding model itself

## Still to pull

- Tyron 2025 LDAEP meta-analysis
- Shukuroglou 2023 psilocybin+music+NAc TRD
- Sun 2024 Cell Reports BNST-NAc music TRD
- Dombrovski 2013 (paywalled, work from summary)
- Jaroszewski 2025 (paywalled, APA)
- Schmaal 2020 neuroimaging meta-review
- Muller 2021 Neuron
