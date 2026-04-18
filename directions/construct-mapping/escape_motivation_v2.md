# Escape Motivation Measurement — Analyst Working File (v2)

Active thread. Appended chronologically. Prior work in `README.md` and `measurement_framework.md` is stale — those proposed CEMP + Pedersen/Muller/Dombrovski benchmarks, none of which cleared the bar below.

---

## The Bar

The measurement of escape motivation (or whatever the right construct is) must be:

1. **Fits the scenario** — a 988 caller on ~2-min hold, listening to music, making a continuous stay/hang-up decision. Phasic state, not trait. Moment-to-moment, not weeks-to-months.
2. **Mechanistically derived** — grounded in an actual neural/cognitive mechanism, not a phenomenological gloss on behavior.
3. **Theoretically motivated** — embedded in a recognizable theoretical framework, not ad hoc.
4. **Empirically validated in the target population** — suicidal-crisis population specifically. Validation in MDD is insufficient unless the mechanism is argued-and-shown to be population-invariant.

Non-negotiable constraints:
- No staircase framing ("A validates B validates C"). Each rung must stand alone.
- Cannot scan 988 callers. Validation comes from existing literature or from target-adjacent empirical work.
- The brain model (TRIBE) is an instrument; the *construct* is defined independently.

---

## Consternations With the Current Default (Pedersen AAC-DDM)

- **Population gap**: Validated in 18 unmedicated MDD females. Not SI, not attempters, not crisis.
- **Scenario gap**: AAC task is reward-points-vs-aversive-image trial-level conflict, not 2-min sustained hold decision.
- **Generalization assumption**: "Circuit implementing AAC is conserved across MDD/SI/SA" is plausible but not empirically shown.
- **Subcortical access**: 3/4 regions are blocked until subcortical head trained. Most diagnostic parameter (NAcc) is unavailable.
- **Framing error in repo**: Treated as "measurement instrument" when at best it's a parameter-to-region template.

The user's proposed default: fall back on Pedersen with *explicit justification* for why the mechanism translates + accept that MDD-to-crisis is a literature-grounded generalization. Acceptable but not satisfying. Want to try harder.

---

## Best-Current-Case If We Must Commit Now

Sustained reward-circuit engagement to music (NAcc/vmPFC dynamics during listening), anchored on Jenkins et al. and Young et al. work in anhedonic/depressed populations with SI or SA history. Mechanism: anhedonic hyporeactivity. Validated in target-adjacent pop. Gap: measures engagement-with-stimulus, not decision-to-stay — upstream of escape motivation, not identical to it.

---

## What I Don't Yet Know (research agenda)

Starting points to expand from:

1. **Behavioral-health vocabulary** — what do behavioral health / crisis-services researchers call this construct? "Disengagement," "drop-off," "help-seeking persistence"?
2. **Crisis hotline dropout literature** — operational research on what makes callers hang up. Is there a construct there already?
3. **Hold music in crisis lines** — practitioner debates. Anything published or in grey literature?
4. **Acute suicidal state constructs** — ASAD (Rogers/Joiner), narrative crisis model (Galynker), suicide crisis syndrome. Do these have moment-to-moment operationalizations with neural correlates?
5. **EMA / ecological momentary suicidality** — Kleiman, Nock, Millner. Phasic state measures. Do any have brain correlates?
6. **Computational psychiatry of suicide** (beyond Pedersen) — Szanto, Dombrovski, Brown. Tolerance to aversion. Drift-diffusion in SI/SA populations specifically.
7. **Music + suicidal populations** — direct experimental data beyond LDAEP. Music therapy trials with in-crisis samples, if any.
8. **Help-seeking persistence / engagement with care** — adjacent construct. How is persistence-in-treatment measured?
9. **Neural correlates of acute SI state changes** — Ballard et al. (NIMH ketamine-SI work), Just et al. (concept representation in SI). Real-time state.
10. **Brain-first** — is there a replicable neural signature of "moment of crisis decision" in target population?

---

## Research Queue (parallel launches)

Planned queries are logged below as they're fired. Results appended.

---

## Findings Pass 1 — Kimi K2.5 Thinking (5 parallel tabs, 2026-04-18)

### Q1: Crisis-hotline ops vocabulary — landed

**Bottom line**: "Escape motivation" is **not** a term used in crisis-line hold literature at all. It appears in Gilbert & Allan (1998) entrapment theory referring to escape from aversive life circumstances, not from a hold queue. The repo has been using a phrase that doesn't match how anyone in ops or academic suicidology talks about hold-state.

**Actual operational terminology** (from Lifeline Call Center Metrics doc):
- **"Call abandonment" / abandonment rate** — the KPI. SAMHSA/OES 2024: 44% of 1.8M calls abandoned before routing; 11% abandoned while waiting.
- **"Caller patience" / "caller tolerance"** — the construct. Operationalized as time-to-abandon distribution. Influenced by IVR messages, hold music, process transparency. Moment-to-moment (seconds-minutes).
- **"Short abandons"** (<5-45s) vs "long abandons"; early abandons (<6-10s) usually filtered as false (wrong numbers).

**Closest suicidology construct**: Entrapment (Gilbert & Allan 1998) — trait-like/episode-stable, NOT momentary. Measured via Entrapment Scale (16 items) or Brief Entrapment Scale (De Beurs 2020, 4 items).

**Industry/grey literature on hold music**: Near-total gap. OES 2024 recommends "calming music" citing only generic call-center literature (not crisis-specific). One study: music increases hold time ~30s, with gender-by-genre interactions. **No peer-reviewed crisis-line-specific hold music research identified.**

**Other constructs I'd asked about — status**:
- "Help-seeking persistence": NOT FOUND as operationalized construct
- "Caller persistence": NOT FOUND as academic term
- "Service abandonment": synonymous with call abandonment, no distinct meaning
- "Disengagement": NOT FOUND in crisis-line caller context
- NASMHPD reports on hold time: NOT FOUND
- Samaritans operational research on hang-ups: NOT FOUND (only volunteer studies, e.g. Pollock et al. 2012)

**Adjacent: treatment dropout literature** — wrong timescale (weeks-months). Swift & Greenberg 2012 meta-analysis: 19.7% dropout. Treatment Engagement Rating (Tetley 2011), DBCI Engagement Scale (Perski 2019). Crisis Text Line "engagement" work (Szlyk et al. 2020) is LCA of conversation patterns, not momentary.

**The gap the project is actually filling**: There is currently **no measurement instrument that captures moment-to-moment "will to persist on hold" during crisis-line waits**. The field treats abandonment as a behavioral outcome, not a psychological state to be measured in-process. This is load-bearing for how we frame the project.

### Q2: Acute/phasic suicidal state constructs — landed

Ranked candidates against the user's bar (acute design / EMA hourly+ / fMRI in SI-SA / fit for escape-from-painful-wait):

| Construct | Acute design? | EMA hourly+? | fMRI in SI/SA? | Fit for target |
|---|---|---|---|---|
| **Entrapment** (Gilbert & Allan 1998) | Retrofitted from trait | **✓ Littlewood 2019** | Indirect (insula) | **Best current option** |
| **Suicide Crisis Syndrome / NCM** (Galynker, Yaseen) | ✓ Designed for acute | ✗ | ✗ | Strong 1-mo attempt prediction, static measurement |
| **ASAD** (Rogers & Joiner 2016-2017) | ✓ Designed for acute | ✗ | ✗ | Theoretical fit, no method — retrospective "worst point" |
| **Defeat** (Gilbert & Allan 1998) | Retrofitted | ✓ Littlewood 2019 | ✗ | Antecedent of entrapment, not crisis state itself |
| **Psychache** (Shneidman 1993) | Conceptually yes | ✗ | ✗ | Purest theory ("unbearable pain → escape"), worst methods |
| **Hopelessness** (Beck) | Trait stretched | Weak concurrent | ✗ | Long-horizon risk, not momentary |
| **Burdensomeness / Belongingness** (Joiner IPT) | Intended proximal | Daily; hourly rare | Indirect (Cyberball) | Interpersonal context |

**Key critical finding from Kimi**: *"No construct has been simultaneously validated with (a) high-frequency EMA (hourly or sub-hourly), (b) specific fMRI neural correlates in SI/SA samples, and (c) prospective prediction within the 24-hour window."* Entrapment = best on EMA. SCS = best on predictive validity. Psychache = best on phenomenology.

**Load-bearing references (new to our repo)**:
- **Littlewood et al. 2019** — *The temporal relationships between defeat, entrapment and suicidal ideation: An EMA study* (J Affective Disorders 293:429-436). N=51 with suicidal histories, 6 assessments/day × 7 days, 1,852 total. Entrapment has **two-way temporal associations with SI at 3-hr intervals**; within-person variance 42-63% (genuine state-variance).
- **Kuehn et al. 2021** — Systematic review of EMA constructs from IMV model (JMIR Mental Health 8(1):e63132). Entrapment present in more EMA studies than any other IMV construct; burdensomeness 28%, belongingness 41%.
- **Galynker et al. 2017** — SCI prediction of near-term (1-month) attempts; SCS has 5 dimensions including "frantic hopelessness/entrapment" which maps closest to escape-from-waiting.
- **Bloch-Elkouby et al. 2020** — Narrative Crisis Model prospective study.
- **2026 resting-state fMRI (CAMS sample)** — vAI–SFG functional connectivity distinguishes attempters from ideators. Insula implicated in "escape motivation" phenomenology. [Verify citation next pass.]
- **ASAD citations**: Tucker et al. 2016 (JAD 189), Stanley et al. 2016 (J Psychiatric Res 79), Rogers et al. 2017 (JAD 213).

**Constructs to drop or de-prioritize** based on this: Hopelessness (wrong timescale), burdensomeness (static when measured), defeat (antecedent).

### Q3: EMA real-time SI + neural state — landed

**State variables with real EMA validation in SI/SA:**
- **Kleiman et al. 2017** (J Abnormal Psych) — SI fluctuates substantially over hours; proximal predictors = negative affect, hopelessness, burdensomeness.
- **Kleiman et al. 2025** (JAD) — real-time affective predictors; underrepresentation of high-arousal negative emotions.
- **Krall et al. 2024** — hopelessness mediates physical-pain→SI in real time across two EMA samples.
- **Wastler et al. 2025** (Early Intervention in Psychiatry) — EMA in first-episode psychosis; "**desire to escape and/or stop bad feelings" emerged as a primary momentary reason for SI**. This is the closest direct EMA measurement of "escape motivation" in target-adjacent pop.
- **Millgram & Coppersmith 2026** (Clinical Psychological Science) — momentary emotion regulation strategies predict concurrent SI intensity.
- **Spangenberg 2019 + Bayliss 2024** — capability for suicide is NOT stable, it fluctuates day-to-day (refutes classical trait view).

**Neural-state tracking of SI change:**
- **Ketamine rapid-response literature** (Zarate, Ballard, Evans, Gilbert MEG, Chen) — pre/post-ketamine neural changes correlate with SI reduction. ACC resting-state, ACC-insula connectivity, fronto-striatal loops, vs/dlPFC connectivity, left superior parietal gamma oscillations (MEG, Gilbert 2020/2022).
- **Marcel Just 2017 (Nat Hum Behav) is RETRACTED**. The 91% MVPA classification has not been independently replicated. Follow-up (Pan/Brent/Cha/Nock, post-2017) refocused on group-level conceptual alteration, not individual prediction.
- **Aupperle 2024** — vmPFC neurofeedback during episodic future thinking shows *within-session modifiability*, but not linked to imminent disengagement.
- **Auerbach 2021** (AJP) — neuroimaging effect sizes too small for individual discrimination in youth SI.

**Behavioral-computational marker of escape in SI/SA**:
- **Millner et al. 2019** (J Abnormal Psych) — "Suicidal thoughts and behaviors are associated with an **increased decision-making bias for active responses to escape aversive states**." Computational marker from RL model, NOT neural state variable. But this is the first-named operationalization of "escape motivation" as a measurable behavior in SI/SA samples.

**Bottom line from Kimi Q3 (verbatim-close):** *"No validated real-time neural state variable tracks imminent behavioral disengagement or 'desire to leave' in suicidal populations."* But the construct exists as self-report (Wastler 2025) and as computational behavioral marker (Millner 2019, Jaroszewski 2025).

### Q4: Music in SI/SA — landed

**Blind spot on a profound level. Findings:**

1. **Music therapy RCTs in SI/SA**: Major evidence base (Erkkilä, Aalbers, Gold, Bradt Cochrane) either **excludes** suicidal behavior explicitly (Erkkilä 2011 excluded "history of repeated suicidal behaviour" from n=79 depressed adults, 671 citations) or fails to stratify by SI/SA status (Aalbers 2017 Cochrane, n=421). **No large-scale RCT of music therapy with SI/SA as primary inclusion criterion exists.**
   - Exceptions (both 2024-2025, small): **Zambonini 2024** — feasibility trial (n=106) in pediatric psychiatric ED with SI/attempts/self-harm. **Tan 2025 dissertation** — MDD+SI pilot, only music+neural study in suicidal sample.
2. **Music-induced mood modulation in SI/SA**: Near-zero experimental data. **Hereld 2019** — qualitative case reports of SI patients using music for "solace," "discharge," "to pull myself out of suicidal thought." No controlled experiments.
3. **Neural response to music in SI/SA beyond Jenkins/LDAEP**: Only Tan 2025 dissertation (anterior superior insula, Heschl's, left IFG in MDD+SI). Jenkins 2018 NAcc-music finding is **MDD-generic, not SI**.
4. **Crisis-line hold music**: **COMPLETE VOID.** Zero empirical studies. 988 website just states "we'll play some hold music" without citation. No grey lit from Samaritans/CTL/Vibrant.
5. **Sad music / mood repair (Van den Tol, Garrido, Taruffi, Yoon)**: All general-pop or MDD-without-SI samples. No SI/SA extensions.
6. **Music + engagement-with-care in SI/SA**: Tan 2025 only. Jimenez-Munoz 2022 mobile-intervention review treats music as one of many media.

**Kimi's verdict (near-verbatim):** *"The literature on music listening in explicitly suicidal-crisis populations is largely a blind spot... If you are building evidence for music interventions in 988 crisis contexts, you are operating in a near-total evidence vacuum and would need primary research rather than meta-analytic synthesis."*

### Q5: Computational psychiatry of suicide beyond Pedersen — landed (major update)

**The Pedersen-analog the user has been asking about EXISTS.** Not in acute-crisis samples, but in SI/SA trait/history populations. Several labs have fit DDM/RL-DDM to escape/approach-avoidance behavior in suicidal samples.

**The "Pedersen-analogs" in target population (trait-SI/SA, not acute crisis):**

| Paper | Population (N) | Trait vs Acute | Paradigm | Model | Brain |
|---|---|---|---|---|---|
| **Millner et al. 2019** (J Abnorm Psych) | STB n=40 / HC n=47 | Trait (SI/SA history) | Escape/avoidance learning | **RL-DDM** (choice + RT) | No |
| **Jaroszewski, Millner et al. 2025** (J Psychopathol Clin Sci) | n=360 with 3-month active SI | Trait (recent SI) | Escape w/ suicide-related stimuli | **RL-DDM** | No |
| **Blacutt et al. 2025** | SI vs no-SI groups | Trait | Escape-avoidance learning | Drift-diffusion RL | No |
| **Myers et al. 2023/2024** | High-risk veterans n=132 | Trait (90-day prospective) | Go/no-go recognition | DDM | No |
| **Chesin et al. 2025** | High-risk veterans n=60 | Trait (90-day prospective) | Death/suicide IAT | DDM on IAT latencies | No |
| **Laessing, Karvelis, Kennedy, Zai, Dayan, et al. 2025** (bioRxiv preprint) | Depression ± suicidal features | Trait | Approach-avoidance conflict | **Hierarchical Bayesian comparison of RL / DDM / Active Inference** | No |

**Millner 2019 is THE key reference.** Directly titled and operationalized as **"active escape bias"** via RL-DDM in STB. STB group shows increased "go" bias via Pavlovian control; escape RTs modeled via DDM non-decision time and drift rate parameters. This is the real computational operationalization of "escape motivation" in SI/SA, replacing Pedersen as the project's anchor.

**Jaroszewski 2025** is its direct follow-up with suicide-specific stimuli — past attempters show *weaker* escape bias for suicide-related stimuli (habituation/desensitization). Important nuance for attempter-vs-ideator distinction.

**Laessing 2025 (bioRxiv)** compares multiple computational frameworks on AAC task in suicidal samples — the direct Pedersen *methodological* follow-up. [Verify preprint availability next pass.]

**Other programs:**
- **Dombrovski** (Pittsburgh): RL models in older-adult attempters. Not DDM. Key papers: 2010 reversal learning (Am J Psychiatry), 2011 delay discounting / lethal forethought (Biol Psych), 2013 JAMA Psych blunted ventral striatal RPE in attempters (fMRI), 2022 WIREs theoretical "search/simulation/choice" framework, 2024 Biol Psych value-option competition.
- **Szanto et al.** — delay discounting in older adults; 2015 JCP high-vs-low lethality (less discounting in high-lethality); 2018 JCP pathway clustering.
- **Karvelis & Diaconescu 2022** (Computational Psychiatry) — active-inference model of hopelessness + active-escape bias in suicidality.
- **Huys/Browning/Bedder** — no direct SI/SA extensions yet; Bedder 2024 on rumination is not SI-specific.
- **Distress tolerance (cold pressor, breath-hold, PASAT, BIRD) in SI/SA**: NO DDM or behavioral-economics decomposition exists. Ironside 2023 found past attempters show *higher* pain tolerance on cold pressor, but uses simple duration/rating metrics — not a latent-variable model. **This is a named gap.**

**Bottom line from Kimi Q5 (verbatim-close):** *"Computational modeling (RL-DDM, DDM) has been extended to suicidal populations beyond Pedersen's MDD sample — specifically by Millner, Blacutt, Myers/Chesin, and Laessing. However, all samples are trait-based or recent-ideation, not acute-crisis state. The acute-crisis computational modeling gap remains open."*

---

## Revised Synthesis (after all 5 Q's landed)

### What changed from the Pass-1 provisional

1. **Millner 2019 replaces Pedersen as the project's anchor.** It's the Pedersen-analog in target population, directly operationalizes "active escape bias" via RL-DDM. No need to staircase or caveat MDD-generalization — this paper fits a suicidal sample directly.

2. **The "desire to escape" construct DOES exist as a measurable variable** — confirmed independently via:
   - EMA self-report (Wastler 2025 in FEP — "desire to escape and/or stop bad feelings" = primary momentary reason for SI)
   - Behavioral-economic decomposition (Millner 2019 active escape bias, Jaroszewski 2025 follow-up)
   - Not yet as a neural state variable.

3. **"Escape motivation" IS real behavioral-health vocabulary** — user corrected my summary. It appears in functional behavior analysis (Iwata et al. 1982/1994 — escape as one of four functions of behavior), negative reinforcement models of addiction (Koob & Le Moal; Baker 2004), and the **Experiential Avoidance Model of Deliberate Self-Harm** (Chapman, Gratz & Brown 2006, Behaviour Research and Therapy). Kimi's search didn't cover this axis. **Chapman et al. 2006 is in target-adjacent population (DSH) and frames the phenomenon as escape** — likely closer fit than anything else surfaced. Needs a dedicated second-pass query.

4. **Music-in-SI/SA literature is a near-total void.** Not just that Pedersen-validates-MDD-not-SI — the entire music-effect-on-target-population evidence base is non-existent. Major music therapy RCTs explicitly exclude suicidal patients (Erkkilä 2011). Crisis-line hold music has zero empirical study. **Implication for the project: validation requires primary research, not meta-analytic synthesis.**

5. **No validated moment-to-moment neural state variable for "desire to leave" exists.** But several labs track state-level SI neurally (ketamine program — Zarate, Ballard, Evans, Gilbert MEG). The gap is *concurrent* neural + SI measurement.

### Revised candidate ranking for "measurement of escape motivation"

| Candidate | Fits scenario | Mechanistic | Theoretical | Validated in target pop | Score |
|---|---|---|---|---|---|
| **Millner 2019 active escape bias (RL-DDM)** | ✓ (stay-vs-escape under aversion) | ✓ (RL + DDM) | ✓ (RL theory of escape-from-threat) | **✓ (STB n=40, trait)** | **★★★★** |
| Jaroszewski 2025 (suicide-stimulus version) | ✓ | ✓ | ✓ | ✓ (n=360 with 3-mo SI) | ★★★★ (with nuance on attempter desensitization) |
| Laessing 2025 AAC comparative | ✓ | ✓ | ✓ | ✓ (depression + SI features) | ★★★★ (if preprint verifiable; direct Pedersen methodological follow-up) |
| Chapman 2006 Experiential Avoidance of DSH | ✓ (self-harm as escape) | ✓ | ✓ (ACT / experiential-avoidance theory) | ✓ (DSH, target-adjacent) | ★★★★ (needs verification of neural work) |
| Wastler 2025 EMA "desire to escape" | ✓ | Self-report | ~ | ✓ (FEP with SI) | ★★★ (construct validation for EMA use) |
| Entrapment (Littlewood 2019 EMA) | ~ | ~ | ✓ | ✓ (n=51 suicidal history) | ★★★ |
| SCS / NCM (Galynker) | ✓ (acute pre-attempt) | ~ | ✓ | ✓ (predictive 1-mo attempts) | ★★★ |
| Pedersen AAC-DDM (MDD only) | ✓ (on paper) | ✓ | ✓ | ✗ (MDD females, not SI) | ★★ |

**Recommendation**: The new anchor is **Millner 2019 + Jaroszewski 2025 (RL-DDM active escape bias)** for the computational operationalization, ideally combined with **Chapman 2006 experiential-avoidance theory** for the psychological framing, and **Wastler 2025 EMA measurement** for state-variable ground truth. This triad clears the user's bar much more cleanly than Pedersen did.

The remaining gap — *acute-crisis samples* — is acknowledged but unavoidable (can't scan 988 callers). Trait-SI/SA validation is the best available and is genuinely in target population.

---

## Second-Pass Research Queue — IN PROGRESS

**5 queries fired 2026-04-18 into Kimi K2.5 Thinking (tabs 1914596733-1914596745):**

1. **2P-Q1**: Construct-connection / nomological network — how do escape-motivation terms across literatures (behavioral-health/Chapman, suicidology/Millner/Pedersen, ops/caller-patience, emotion/Mobbs) relate? Is there a published synthesis paper? [streaming]
2. **2P-Q2**: Better Function-1 candidates — deep-dig Karvelis 2022, Dombrovski 2024 (turned out: CONFERENCE-ONLY, not published — demote), Vanyukov 2016, Laessing 2025, any Millner fMRI extension. [streaming]
3. **2P-Q3**: Verify+extend Function-2 audio benchmark — push harder on LDAEP, ASR/PPI, Tan 2025 published follow-ups, foreign-language SI/SA audio neuroimaging. [streaming]
4. **2P-Q4**: Sustained-decision / fatigue / persistence models in SI/SA — Muller 2021 extensions, effort-based decision-making, distress tolerance DDM. [fired late, just submitted]
5. **2P-Q5**: Millner-fMRI bridgeability — can we make our own Millner+fMRI connection? Drop-in vs proxy via Dombrovski vs open-dataset post-hoc vs primary study. [streaming]

---

## Pass-2 Findings (continuously updated)

### Paper pulls successful (3 new PDFs)

- `context/papers/karvelis2022_active_inference_suicide.pdf` — Karvelis & Diaconescu 2022, Computational Psychiatry 6(1):34-59. **Major find.**
- `context/papers/brown2020_vmpfc_suicide.pdf` — Brown, Wilson, Hallquist, Szanto, Dombrovski 2020, Neuropsychopharmacology 45:1034-1041. **Major find.**
- `context/papers/millner2018_active_escape_healthy.pdf` — Millner, Gershman, Nock & den Ouden 2018 J Cog Neurosci 30(10) (foundational paradigm paper, healthy-subject version that Millner 2019 builds on).
- `context/papers/kleiman2018_realtime_monitoring.pdf` — Kleiman & Nock 2018 real-time monitoring review.
- `context/papers/pedersen2021_aac_ddm.pdf` — already had it; now actually read it.

### Paper pulls failed (explicit demote)

- **Dombrovski 2024 "Neural Dynamics of Value-Based Option Competition in Suicidal Behavior"** — **CONFERENCE-ONLY (SOBP May 2024), not peer-reviewed.** Prior notes cited this as a published paper; it isn't. Demote from candidate list.
- **Dombrovski 2013 JAMA Psych** — paywalled, no open-access version located. Work from summaries with explicit flag.
- **Jaroszewski 2025 J Psychopathol Clin Sci** — paywalled. Work from summaries.

### KARVELIS & DIACONESCU 2022 — Function-1 theoretical anchor

**Role**: integrated active-inference computational model of STB that explains **hopelessness + Pavlovian bias + active-escape bias** jointly via the drive to maximize Bayesian model evidence.

**Mechanism**: four computational perturbations that generate all three STB markers:
1. Increased learning from aversive outcomes
2. Reduced belief decay in response to unexpected outcomes
3. Increased stress sensitivity
4. Reduced sense of stressor controllability

**Neurocircuit mapping** (their Figure 1b):
- **Locus coeruleus - norepinephrine (LC-NE)** → belief update rate (learning rate)
- **Amygdala (Amy)** + LC → aversive learning rate boost
- **Dorsolateral PFC (dPFC)** + LC → belief decay rate (cognitive flexibility)
- **Anterior cingulate cortex (ACC)** → action-state beliefs (hopelessness representation; receives from dPFC-LC)
- **Ventromedial PFC (vmPFC)** + dorsal raphe-serotonin (DRN-5-HT) → controllability inference + amygdala regulation

**Key theoretical move**: hopelessness is reconceptualized as **strong negative instrumental beliefs about state transitions**. Increased Pavlovian bias (and thus active-escape bias) emerges as a rational consequence when instrumental control has low model evidence — *"if my actions can't change outcomes, fall back on reflexive defensive policies."*

**Validation**: simulations of Avoid/Escape Go/No-Go task **replicate Millner et al. 2019's active-escape bias findings**.

**Paper type**: proof-of-concept / theoretical. No empirical fit to data. Bridges the behavioral findings (Millner) to neurocircuits (via active-inference framework) without empirical test yet.

**Why this is load-bearing for Function 1**: it's the theoretical engine that converts "active-escape bias" (a decision parameter) into claims about specific neural circuits. Applied with Pedersen's empirical-regression methodology, it tells us what TRIBE-predicted activation in LC / Amy / dPFC / ACC / vmPFC should translate to in terms of hopelessness / escape-bias parameters.

**Clean subtyping prediction**: their model distinguishes **impulsive vs planful** STB via which perturbation dominates (reduced dPFC-mediated belief decay = planful/rigid; increased Amy-LC learning from negatives = impulsive).

### BROWN ET AL. 2020 — Function-1 empirical anchor (target pop + fMRI + computational model)

**Role**: empirical evidence that the vmPFC-leg of Karvelis's circuit is actually disrupted in suicide attempters during decision-making under learning + uncertainty. Closest-available empirical validation of the Karvelis framework, in target population, with fMRI + computational model.

**Sample**: n=116 middle-aged/older adults (47-79 yrs):
- 35 suicide attempters with current ideation
- 25 ideators only
- 25 depressed controls (no ideation)
- 31 nonpsychiatric controls

**Task**: 3-armed bandit with drifting reward probabilities. 300 trials. Continuous value-updating required (not serial reversal — more cognitively demanding). fMRI during task.

**Model**: reinforcement learning model fit to behavior. Value estimates from best-fitting parameters regressed against BOLD signal (meta-analytic vmPFC ROI; striatal ROIs as comparison). PPI analysis for vmPFC-frontoparietal connectivity.

**Key findings**:
1. **vmPFC value signals reduced in attempters** vs nonpsychiatric controls (p<0.05). Effect present in attempters above-and-beyond depression or ideation. Not seen in striatum — specific to vmPFC.
2. **vmPFC-frontoparietal connectivity is normally moderated by impulsivity** (more impulsive → weaker connectivity) in nonpsychiatric controls. Effect preserved in depressed controls. **Effect abolished in attempters** (p<0.001). I.e. the normal "high-impulsivity-shows-weak-cognitive-control" signature disappears in attempters.
3. **Behavior follows**: attempters show disrupted integration of vmPFC connectivity × impulsivity × reinforcement on choice quality (p<0.001).

**Interpretation they offer**: "Reduced vmPFC-frontostriatal connectivity may result in reduced cognitive control and selection of choices based on proximal vs. distant outcomes, similar to behavior during a suicidal crisis." This is a DIRECT claim that the neural signature they found maps onto crisis-decision phenomenology.

**Why this is load-bearing for Function 1**: supplies the empirical vmPFC fingerprint that fine-tuned TRIBE should reproduce if it's really modeling target-pop physiology. Provides the target-population calibration that Karvelis's theoretical framework lacks.

**Why this is load-bearing for Function 2**: this IS the kind of benchmark we wanted — specific brain-region neural signature of attempter physiology during decision-making. Fine-tuned TRIBE should reproduce vmPFC-value-attenuation and vmPFC-frontoparietal-connectivity-disruption when predicting brain responses for target-pop-like subjects.

### PEDERSEN 2021 — Function-1 methodological scaffold (not population anchor)

**Actually read now**. Critical methodology detail (pg 6-7):

- Trial-by-trial BOLD activity in pACC, caudate, NAcc, STN extracted via LS-S approach.
- Hierarchical Bayesian DDM fit via HDDM/STAN/BRMS.
- **The exact regression structure** (this is what we want to re-apply with TRIBE output):
  - `v_t ~ log(reward_t) × caudate_t + aversiveness_t × pACC_t + dReward_t`  (drift rate)
  - `a_t ~ |reward_t - aversiveness_t| × STN_t`  (decision threshold)
  - `z_t ~ PavlovianBias_t × NAcc_t`  (starting point)
- Empirical findings: v-reward p(HC>MDD)=0.99 (strong); z-NAc p(HC>MDD)=0.971 (NAc flips bias direction); z-Pavlovian p(HC>MDD)=0.971; AUC=0.68 classification.

**Role**: Pedersen's methodological *structure* — use trial-by-trial BOLD in ROIs as regressors on DDM parameters — is what we want to apply. The population is MDD, not target pop, but the methodology is what we'd reuse. Karvelis + Brown provide the target-pop priors on which region maps to which parameter.

### Revised Single-Anchor Framing (Updated after Karvelis + Brown)

Retracting the earlier "Millner is the anchor" framing. Actual shape:

**Function 1 (Instrument: fMRI-typed input → escape-motivation score)**
- **Theoretical engine**: Karvelis & Diaconescu 2022 — active-inference framework mapping LC-NE, Amy, dPFC, ACC, vmPFC to hopelessness + Pavlovian + active-escape components.
- **Empirical neural evidence**: Brown et al. 2020 — target-pop fMRI + RL-model showing vmPFC value + connectivity disruption in attempters.
- **Methodological reuse**: Pedersen 2021's trial-by-trial BOLD-as-regressor structure — applied with TRIBE output and Karvelis's parameter-region priors.
- **Behavioral ground truth for validation**: Millner 2019 — RL-DDM active-escape bias in STB; validation samples should reproduce Millner-type behavioral effects.

This is ONE anchor expressed as a connected trio: Karvelis (theory) + Brown (empirical) + Pedersen (method), with Millner providing behavioral calibration. Not a staircase — each piece covers a specific function and they're jointly necessary.

**Function 2 (Benchmark: fine-tuned TRIBE predicts target-pop-like neural patterns)**
- **Schmaal et al. 2020** Mol Psych — 2-decade neuroimaging meta-review in SI/SA populations
- **Brown 2020** doubles as benchmark: fine-tuned TRIBE should reproduce the reduced-vmPFC-value + disrupted-connectivity pattern in predicted activations for target-pop-like subjects
- **Sastre-Buades et al. 2021** NBR — systematic review/meta-analysis of decision-making in suicidal behavior; supporting population-level context

### Key honesty flags

1. **The task-invariance assumption.** Pedersen-style methodology maps trial-by-trial BOLD *during AAC task decision phase* to DDM parameters of that task. Applying the same parameter-to-region mapping to *music-listening BOLD* assumes the mapping is task-invariant (i.e., the circuit mechanisms of value encoding in vmPFC are what the vmPFC does in general, not only during reward/bandit/AAC tasks). This is a nontrivial extrapolation. Strongest defense: Karvelis's theoretical framework IS a task-general claim about active-inference machinery, not a task-specific empirical claim. Still needs stating.

2. **All target-pop validation samples are non-acute.** Brown 2020: "attempters with current ideation" but testing was during non-crisis periods. Millner 2019: "past-year STB" including 26 past-year attempts, still non-acute-at-testing. Karvelis 2022: simulations, not empirical. There is no "acute crisis fMRI" data to anchor on.

3. **Dombrovski 2024 was not an actual paper.** Conference abstract only. Any earlier analysis that treated it as a candidate needs revision.

4. **The music axis is a genuine void.** Previous Q4 finding confirmed: Tan 2025 dissertation is the only music-neural study in SI/SA. Erkkilä 2011 (the major music therapy RCT, 671 citations) *explicitly excluded* suicidal patients. Primary research is required for direct music-in-target-pop evidence; no existing-literature rescue exists.

### Still open (next-step second-pass items)

- **Nomological network of escape-motivation terms** (2P-Q1 cooking)
- **Verify Millner+fMRI bridgeability** (2P-Q5 cooking) — is there a feasible way to get Millner-paradigm + fMRI in target pop via open datasets, or does it require new data collection?
- **Full verification of Laessing 2025 bioRxiv preprint** — if real, another strong candidate
- **Sustained-decision models** (2P-Q4 just fired) — does Muller fatigue / effort-based work extend to SI/SA?
- **Tighter audio-benchmark** (2P-Q3 cooking) — LDAEP and others, verify Q4's "blind spot" claim isn't overclaimed

### Supporting context from Kleiman 2018 (Current Opinion Psychology)

Just read. Validates the moment-to-moment framing:
- SI episodes are episodic with quick onset + short duration (typically <1 hour)
- ~1/3 of momentary SI observations differ by ≥1 SD from a few hours earlier — genuine hour-scale fluctuation
- Hour-to-hour variability in SI nearly as large as person-to-person variability
- **Affect (especially sadness) predicts time-lagged SI change; hopelessness/loneliness CORRELATE concurrently but DO NOT predict change.** Important: don't overweight hopelessness as a temporal mover.
- Fluid Vulnerability Theory (Rudd 2006) — baseline with episodic peaks — fits the real-time data.
- Law et al. 2017 RCT: repeatedly asking about SI does NOT have iatrogenic effects, validating that EMA in target pop is safe.

**Takeaway for our project**: 2-minute 988 hold is squarely within the timescale of a real SI episode. The caller is potentially *in* such an episode during the hold. What we want the music to do is push them out of the peak-SI state within that window. That's biologically plausible given the episodic dynamics Kleiman documents. The "escape motivation" construct we care about is specifically the affect + action-tendency layer during these peaks, not the trait vulnerability.

### Exploratory threads worth flagging (construct/measurement side, not training)

Not things I'm doing — things that surfaced reading these papers and seem worth noting for the record:

1. **Psychache ≈ Karvelis's "negative instrumental beliefs about state transitions"?** Shneidman: suicide is escape from unbearable psychache. Karvelis: hopelessness = strong belief that instrumental actions won't change state. These are structurally the same claim in different vocabularies. If they're equivalent, it resolves the long-standing complaint that psychache lacks mechanistic operationalization — Karvelis provides the math, Shneidman provides the phenomenological anchor.

2. **Muller 2021 fatigue dynamics ≈ Karvelis belief-decay dynamics?** Muller's RCZa/RCZp cingulate signals for accumulated effort fatigue look structurally identical to Karvelis's λ (belief decay modulated by dPFC-LC via SAPEs). Both represent "accumulated evidence that my actions aren't producing desired outcomes," just interpreted in different theoretical vocabularies (effort-fatigue vs Bayesian belief updating). If they converge, Muller's repo-integrated fatigue benchmarks could be reused as an orthogonal validation for the belief-decay leg of the Karvelis framework.

3. **"Caller patience" ≈ Karvelis w (stressor controllability)?** Operations term "caller patience" is just "how long will you wait before giving up." Karvelis predicts that patience depends on perceived controllability: if caller believes the counselor will arrive on a predictable timeline (high w), they stay; if they believe the wait is uncontrollable (low w), Pavlovian escape kicks in and they hang up. This maps the behavioral-health ops metric directly onto the Karvelis framework. Worth explicit writing-up later.

4. **LDAEP as cheap auditory-pathway sanity check.** Park 2021/2022 showed LDAEP (auditory cortex loudness-dependence) is elevated in high-suicidality MDD. If fine-tuned TRIBE doesn't reproduce this in its auditory-cortex predictions for simulated high-SI subjects, the audio pathway is likely broken *before* we even get to the escape-motivation instrument. Quick test, clear pass/fail.

5. **Audiogenic aversion framework generalization.** Millner's fork-on-slate (80-85 dB, high-freq) is pharmacologically aversive audio. 988 hold music is *mildly* aversive (aversive-by-tedium rather than aversive-by-pain). Millner's active-escape-bias findings are about decision dynamics under aversion; the construct should generalize from high-intensity noise to low-intensity stimuli, but the neural recruitment may differ. Specifically: hold music likely doesn't engage amygdala/LC as strongly as Millner's noise. This matters for which Karvelis parameters dominate — mild-aversion music probably mostly operates via m (belief decay) and w (controllability) rather than k (stress-weighted learning boost). That's actually a more tractable intervention target: shift perceived controllability with progress-of-queue transparency rather than try to flip Pavlovian escape bias via stimuli. Relevant to SAMHSA/OES 2024 "process transparency" recommendation — independent theoretical grounding for what the field has already converged on operationally.

Flagging these now so they don't get lost. Not trying to commit to any of them as research direction.

---

## 2P-Q1 Results (Construct Nomology) — landed

**Headline**: Kimi confirms **no published paper performs the comprehensive nomological network analysis we need**. "Your specific context (crisis-hotline hold scenario) is theoretically unmapped." This is a writable gap.

### Four construct clusters with relative independence

**Cluster 1 — Core Escape Mechanisms (negative reinforcement family)**: Iwata 1982/1994 escape motivation (molar functional class, external-target), Hayes 1996 experiential avoidance (requires verbal mediation, internal-target), Baker 2004 / Koob-LeMoal allostatic (homeostatic dysregulation), Millner 2019 active escape bias (computational DDM bias parameter), Guitart-Masip 2012 Pavlovian escape (automatic S-R).

Neural overlap is *partial* on PAG-amygdala-striatal circuitry but functionally dissociable. **Hierarchically nested**: Iwata (molar class) → Hayes (+verbal mediation) → Millner (computational mechanism) → Pavlovian escape (automatic component). **Not interchangeable.**

**Cluster 2 — Suicide-specific crisis (entrapment family)**: Gilbert & Allan 1998 defeat + entrapment, Shneidman 1993 psychache, Galynker SCS frantic hopelessness, Rogers & Joiner 2015-2017 ASAD.

Temporal progression: **Defeat → Entrapment → Psychache → Suicidal Crisis (ASAD/SCS)**. NOT synonyms despite cross-sectional collinearity (entrapment–psychache r > 0.60). SCS ≠ ASAD: SCS is persistent/fluctuating frantic hopelessness (doesn't require SI); ASAD is spike-like rapid escalation of conscious SI.

**Cluster 3 — Conflict and disengagement**: Pedersen 2021 AAC (ambivalence, simultaneous positive+negative valence), Mobbs 2020 defensive flight (urgent unidirectional PAG-mediated avoidance), Carver behavioral disengagement (motivational collapse — giving up, not active escape).

**Genuinely distinct.** AAC involves wanting-reward-while-fearing-punishment; escape constructs are unidirectional negative valence.

**Cluster 4 — Operations (isolated from psychological lit)**: "Caller patience / tolerance" — operationally defined as queue abandonment thresholds. **No psychological mechanism in the published literature connects it to the other clusters.** Kimi's bridge proposal: could be modeled as *temporal discounting of help-seeking* — an AAC variant where aversiveness-of-waiting is weighed against expected utility of counselor connection. But no published link to Millner / Hayes / Gilbert.

### Critical construct distinctions (things I should keep straight)

| Construct | Critical differentiator |
|---|---|
| **Escape motivation (Iwata)** | External aversive stimulus termination; behavioral topography irrelevant |
| **Experiential avoidance (Hayes)** | Internal (thoughts/emotions) target; requires verbal mediation |
| **Active escape bias (Millner)** | Computational starting-point bias in DDM; pre-decisional, not functional |
| **Pavlovian escape (Guitart-Masip)** | Automatic S-R, may conflict with instrumental goals |
| **Allostatic escape (Koob/Baker)** | Chronic recruitment during withdrawal; homeostatic dysregulation |
| **Entrapment (Gilbert)** | Motivational BLOCKING — escape motivation present but blocked |
| **Psychache (Shneidman)** | Phenomenological pain experience, mechanistically agnostic |
| **Frantic hopelessness (SCS)** | Persistent urge to escape + cognitive dysregulation + hyperarousal; no SI required |
| **ASAD (Rogers-Joiner)** | Spike-like escalation of CONSCIOUS SI + social/self-alienation + hyperarousal |
| **AAC (Pedersen)** | Ambivalence — simultaneous + and - valence; conflict-point vacillation |
| **Defensive flight (Mobbs)** | Urgent, reactive, PAG-mediated, subcortical (below conscious valuation) |
| **Behavioral disengagement (Carver)** | Motivational collapse / resignation; NOT active escape |
| **Caller patience (Lifeline)** | Pure operational metric; no psychological mechanism |

### Kimi's recommended multi-level measurement design

Independently converged on what we've been building:

1. **Computational**: Millner RL-DDM active-escape-bias parameter → decision threshold for hanging up vs holding
2. **Clinical**: Entrapment scale (Gilbert & Allan) → perceived inability to reach help
3. **Physiological**: PAG/amygdala reactivity (fMRI) OR heart rate variability (parasympathetic withdrawal) → defensive flight
4. **Operational**: Caller patience metrics (queue duration, abandonment point) → behavioral outcome

This is basically the "Function 1 + Function 2" carving but with 4 levels instead of 2, and adds physiology + operational as independent validations.

### Writable empirical hypothesis Kimi flagged

*"Active escape bias predicts queue abandonment thresholds, mediated by entrapment and moderated by psychache intensity."*

Thesis-level claim. Specifies (1) Millner param = primary predictor, (2) entrapment = mediator, (3) psychache = moderator. If we had a target-adjacent behavioral sample doing Millner's task plus self-reported entrapment+psychache plus a hold-simulation wait task, this would test.

### Demote from prior candidate list

- **Experiential Avoidance Model of DSH (Chapman 2006)**: confirmed as Cluster-1 construct, valid, but **internal-target framework with no fMRI validation in SI/SA as a specific construct** — it's a theoretical framework, not an instrument. Keep in the architecture as psychological framing but not as measurement anchor.

---

## 2P-Q2 Results (Function-1 candidate verification) — landed

**Headline**: no paper currently exists with the exact Pedersen 2021 structure (NAcc=bias, pgACC=drift, STN=threshold via joint RL-DDM-fMRI) in an SI/SA population. One viable "best available" candidate: **Ji et al. 2021**.

### Retractions from prior notes

- **Laessing, Karvelis, Kennedy, Zai, Dayan et al. 2025 bioRxiv — FABRICATED CITATION. DOES NOT EXIST.** Kimi's first-pass Q5 confabulated the citation (with specific author names). Second-pass verified: no record in bioRxiv, PubMed, or preprint servers. **Remove from candidate list in all earlier notes/summaries.** This is a reminder that Kimi will confabulate — always verify via a second route before relying on surprisingly-perfect-fit citations.
- **Dombrovski et al. 2024 Biol Psych "Neural Dynamics of Value-Based Option Competition in Suicidal Behavior" — DOES NOT EXIST as described.** Likely conflated with Hallquist et al. 2024 Science Advances (general population, not SI/SA). Confirmed demote (was already flagged).

### Verified candidates (what actually exists)

| Paper | Verified? | Sample | fMRI | Computational model | Param↔Brain mapping? | Verdict |
|---|---|---|---|---|---|---|
| **Pedersen 2021** PLOS CB | ✓ | 18 MDD female + 24 HC | ✓ | RL-DDM | **✓ (NAcc=z, pACC=v, STN=a, caudate=v)** | Methodology scaffold, wrong population |
| **Ji et al. 2021** J Psych Res 139:14-24 | ✓ | 23 SA+MDD + 30 NS-MDD + 30 HC | ✓ | 4-param Bayesian BART model | **✓ (left insula = pain avoidance / risk aversion; left dlPFC = loss sensitivity)** | **Strongest target-pop candidate** but BART not DDM, correlational not joint, insula/dlPFC not subcortical DDM regions. Sample includes **recent attempters (acute, past weeks/months)**. |
| **Dombrovski 2013** JAMA Psych | ✓ | 15 SA + 18 dep + 20 HC (late-life) | ✓ | Modified Rescorla-Wagner RL | Partial: maps model-derived *signals* (RPE, expected value) to regions — NOT parameters to regions | Late-life only, weak for instrument role |
| **Karvelis & Diaconescu 2022** Comp Psych | ✓ | Simulation only | ✗ | Active inference MDP | Theoretical only (LC↔k, Amy↔c, dPFC-LC↔m, vmPFC-DRN↔w₀) | Useful for theoretical framework + priors, NOT empirical |
| **Vanyukov et al. 2016** Psychol Med | ✓ | 13 SA + 13 non-SA MDD + 22 HC (late-life) | ✓ | No computational model — standard GLM | NO — precuneus/PCC for impulsivity, dlPFC for planned attempts | No comp model, fails criterion |
| **Millner 2019** J Abnorm Psych | ✓ | 85 STB + 44 psych controls | ✗ | RL-DDM | No neural data | Behavioral only |
| **Dombrovski & Hallquist 2022** WIREs | ✓ | Review/theoretical | — | — | — | Not empirical |

### Strategic options identified by Kimi

1. **Use Ji et al. 2021 as the target-pop instrument** — accept BART framework (not DDM), use insula↔uncertainty-aversion + dlPFC↔loss-sensitivity as proxy escape-motivation scores. Weakness: different regions than Pedersen's subcortical DDM circuit, correlational mapping not joint.
2. **Use Dombrovski 2013 for the RL+neural-signal approach** (but accept signal-mapping not parameter-mapping).
3. **Commission/use Millner 2019 behavioral paradigm with added fMRI** — task exists and validated for STB; neural version does not exist. Would require primary data collection.

Kimi's bottom line: *"The literature gap you identified is real and represents a significant methodological opportunity (or necessity for de novo data collection)."*

### Updated Function-1 shape

- **Theoretical engine**: Karvelis 2022 (unchanged).
- **Empirical neural evidence in target pop**: Brown 2020 (vmPFC value + connectivity) **AND Ji 2021 (insula + dlPFC in recent attempters with computational model)**. Ji is actually closer to what we want — acute sample + computational model + parameter-to-region mapping — but with BART rather than escape paradigm.
- **Methodology scaffold**: Pedersen 2021 (unchanged) — use BOLD-as-regressor structure.
- **Behavioral validation in target pop**: Millner 2019 (unchanged).
- **Known gap**: no paper does all three (target pop + escape paradigm + joint fMRI-DDM parameter mapping). That's the specific open question.

---

## 2P-Q3 Results (Audio benchmark verification) — landed

**Headline**: the "music-in-SI/SA is a blind spot" claim from Q4 **survives** scrutiny for direct music-neuroimaging, but **partially falsifies** for auditory electrophysiology broadly. LDAEP and ASR/PPI are well-studied in suicidality, just not with music as the stimulus.

### Verified non-blind-spots

**LDAEP in SI/SA is well-studied**:
- **Tyron, Ip, Jørgensen & Jensen (2025) *J Affective Disorders* — meta-analysis with replication in unmedicated patients.** Authoritative most-recent synthesis.
- Korean literature (Park 2015, Park & Lee 2013, Hwang 2021 *Clinical Psychopharmacology and Neuroscience*): serotonergic dysfunction via LDAEP in MDD+suicidality.
- German literature (Uhl 2012, Graßnickel 2015, Juckel).
- **Kim et al. 2021 *Sci Reports*** — explicit conclusion: "LDAEP might not be a biomarker for suicide behaviors." Mixed directionality: high LDAEP in acute SI (Hwang 2021) vs blunted in attempters (Graßnickel 2015, Cho 2023).
- **Verdict: unreliable as standalone marker** but rich literature exists. Could still serve as cheap sanity check on TRIBE's auditory cortex predictions (does fine-tuned TRIBE reproduce *any* loudness-dependent asymmetry between simulated SI and HC?).

**ASR/PPI in SI/SA**:
- **Quednow et al. 2006 *J Affective Disorders*** — "Normal PPI/ASR in suicidal depressed patients." 60 citations. PPI doesn't stratify suicide within depression.
- **Takahashi et al. 2011** review; **Storozheva 2025** systematic review.
- Verdict: PPI not a useful suicide stratifier within depression.

### Confirmed blind spots

- **EEG/MEG music in SI/SA**: only Tan 2025 (behavioral) and Jenkins 2018 (MDD, no SI stratification). No other studies found.
- **Jenkins 2018 follow-ups**: no SI-stratified reanalyses 2019-2026.
- **Hold music neuroimaging in any psychiatric population**: zero studies.
- **Multi-modal auditory biomarker panels (MMN + LDAEP + ASR + music)**: do not exist. Yin 2025 Psychoradiology meta-analysis includes LDAEP + P3 + RewP but not MMN or music.
- **MMN in SI/SA**: emerging blind spot — mentioned as biomarker but no suicide-specific validation.

### Verified papers newly surfaced (to pull next if relevant)

- **Tyron et al. 2025 JAD** — LDAEP meta-analysis
- **Tan 2025** — confirmed **published** in *J Clin Med* (pilot n=18 MDD+SI) and *PLOS Mental Health* (n=74 BMRQ + semantic differential). But neural data still in dissertation only.
- **Yin et al. 2025 *Psychoradiology*** — meta-analysis of auditory biomarkers for suicide (LDAEP + P3 + RewP)
- **Jandl et al. 2010 JAD** — P300 + EDA as suicide risk markers
- **Zhou et al. 2024 J Psych Res** — P2-P3 and N2-P3 amplitudes in MDD+suicide
- **Shukuroglou et al. 2023 J Psychopharmacology** — psilocybin + music + NAc functional connectivity in TRD. Relevant — music + reward circuit in a target-adjacent treatment-resistant sample.
- **Sun et al. 2024 Cell Reports** — music synchronization in BNST-NAc circuit in TRD via implanted electrodes. First direct neural-music-depression data. Very relevant.

### Updated Function-2 (benchmark) position

**Still primarily a blind spot for music**, but the auditory electrophysiology literature offers a cheap independent sanity-check layer:

- **LDAEP fine-tuning check**: does fine-tuned TRIBE reproduce *any* loudness-dependence difference in auditory cortex predictions between simulated SI and HC? Pass/fail on the auditory pathway independent of escape-motivation.
- **Shukuroglou 2023 + Sun 2024** offer the closest-available music-reward-circuit empirical fingerprints in target-adjacent populations.
- **Hold music neuroimaging is a total void** → if the project needs direct validation, must generate it.

---

## Critical methodological lesson from this session

**Always verify citations via a second route before propagating.** Kimi confabulated Laessing 2025 bioRxiv in its first pass with specific author names, DOI pattern, and descriptive content. The paper does not exist. I propagated it into the v2 doc as a "critical candidate" for several messages before Q2's verification pass caught it. Ji 2021 turned out to be real (verified via PubMed with Pizzagalli as author). The lesson: every time Kimi surfaces a surprisingly-perfect-fit paper, verify via PubMed / publisher direct / independent search before building arguments on it.

This is now a rule I should carry forward. Added to the `research-paper-pointers` skill (under "Red flags that the PDF you downloaded is wrong" — should extend to "Red flags that the paper doesn't exist at all").

**Also discovered**: Kimi rate-limits parallel chats. Opening ~11 tabs triggered a "You already have several chats open. Please wait to finish them." modal on tab 736 that silently blocked 2P-Q4 from ever submitting to Kimi's inference backend. No error surfaced; the tab just sat idle while I thought it was streaming. For future parallel runs, keep concurrent tabs under ~8 or accept that some will silently stall. Updating `using-kimi-for-research` skill with this gotcha.

---

## 2P-Q5 Results (Millner-fMRI bridgeability) — landed

**Headline**: Kimi evaluated six feasibility paths. Only two are live (Dombrovski Bridge + Primary Study); the rest are currently dead ends.

### Path assessment summary (Kimi's verdict)

| Path | Feasibility | Verdict |
|---|---|---|
| **1. Does it exist?** (published Millner+fMRI in SI/SA) | LOW | Does not exist. "You would be the first." |
| **2. PIT fMRI in SI/SA as substitute** | LOW | No PIT fMRI in SI/SA. Only healthy samples (Guitart-Masip 2012). |
| **3. Open-dataset post-hoc** (ABCD, UCLA CNP, ds001814 BART) | MEDIUM-LOW | Construct validity gap — monetary/risk paradigms ≠ escape. Could fit RL-DDM to ds001814 (Ji's BART data) but tests "RL dysfunction" generally, not escape-specifically. |
| **4. Dombrovski Bridge** (striatal RPE → Millner's escape bias via shared RL theory) | **MEDIUM — defensible** | **Only real drop-in option.** Dombrovski 2013 striatal RPE findings in attempters + shared corticostriatothalamic circuitry argument → theoretical grounding for Millner's behavioral parameter. Weak links: mechanistic (RPE vs starting-point), population (late-life vs veteran), task (reversal vs escape). |
| **5. Primary study** (fMRI with Millner task in SI/SA) | HIGH (resource-intensive) | Budget $150-300K, n=30-40/group, ~120 scan hrs. "If your project requires valid neural correlates of escape bias specifically, you must collect the data. No existing substitute exists." |
| **6. Meta-analysis** | LOW-MEDIUM | Premature — too few fMRI studies of escape in SI/SA (1-2 max); ALE requires ~10+. |

### Kimi's realistic recommendation

**Path 4 (Dombrovski Bridge) for initial writeup/grants, Path 5 (primary data) as ultimate validation strategy. Paths 1, 2, 6 are currently dead ends.**

This lines up with what I had been converging on but makes the costing explicit. $200K+ for a valid Millner-fMRI dataset is the eventual budget if we want the neural piece done right.

### New candidates named

- **Auerbach et al. 2021** — blunted caudate/putamen activation during reward anticipation in suicidal youth (not PIT, but target-adjacent)
- **Dombrovski 2014** — reduced RPE signals in corticostriatothalamic networks correlated with executive control deficits (more ammunition for the Dombrovski Bridge argument)
- **Esmaeil-Zadeh** — Raven/future imagination fMRI in suicide (for ALE meta-analysis, if ever attempted)

### Ji 2021 actually read (`context/papers/ji2021_motivation_decision_suicide.pdf`)

PDF pulled successfully from UCI depression institute site. Key sample details from pages 1-4:

- **Sample**: n=53 MDD (23 SA + 30 NS) + 30 HC; age 16-45, right-handed, Chinese (Changsha, Central South University).
- **All MDD recruited during ACUTE episode**, UNMEDICATED (no antidepressant or ECT in past 6mo). This is closer to acute-crisis than most comparable papers.
- **Attempt profile explicitly described as "generally carefully planned, non-impulsive and not personality-disorder driven."** Methods diverse: wrist-cutting (n=11), jumping (n=8), overdose (n=7), hanging (n=3), immolation (n=1). Some subjects attempted more than once.
- **Computational model**: 4-param Bayesian (φ, η, γ, τ) fit via hBayesDM. γ = risk-taking propensity; τ = inverse temperature (choice determinism).
- **Key parameter finding**: γ lower in SA vs NS (p<0.05 by posterior distributions shown in Fig 2d). Higher pain avoidance (TDPPS) in SA vs NS.
- **Neural findings**: 
  - Left insula: reduced activation in SA during high-risk decision phase; modulated by pain avoidance in both SA and NS
  - Left dlPFC: greater activation in SA during loss feedback (loss hypersensitivity)
- **Authors' interpretation**: "Suicide as extreme choice when value estimations are compromised and emotionally overwhelmed."

### Important scope note on Ji 2021 (flagged during user check-in)

Ji's attempter sample is narrowly defined: **planful, non-impulsive, non-BPD-driven, acute-episode unipolar depressed, unmedicated**. This is ONE subtype of 988 caller, not all of them.

Excluded by design:
- Impulsive / BPD-driven attempt profile
- Non-depressed acute-crisis callers (substance, interpersonal crisis, adjustment)
- Bipolar depressed suicidality

**Softening counterpoint**: Ji's primary contrast is **SA+MDD vs NS-MDD**, not SA vs HC. That's a stronger contrast than naive SA-vs-control because it controls for depression-general effects. The insula/dlPFC findings isolate suicidality-specific effects *within* a depressed sample. Much more usable than raw SA-vs-HC.

**Practical implication for the project**: one-brain-model-produces-one-escape-motivation-score is too simple. We likely need subtype-specific scores (planful-depressive, impulsive, non-depressed-crisis) or at minimum explicit scoping language ("this music's score is validated for the planful-depressive subtype"). Ji covers ~the plurality of 988 caller risk profile but not the full distribution.

---

## End of pass-2. Final v2 doc state ready for user review.

---

## Provisional synthesis (after Q1/Q2, pending Q3/Q4/Q5)

**What we now know about the measurement gap:**

1. "Escape motivation" is not a real operational construct — it's our internal shorthand that doesn't appear in either operations research or academic suicidology. The project doc should stop using it as if it's a name.

2. The *closest operational construct* is **caller patience / caller tolerance** (momentary behavioral state, how long someone will wait before hanging up). Already operationalized in ops research; no psychological scale.

3. The *closest psychological construct with any EMA validation in target pop* is **entrapment** (Littlewood 2019, 3-hr dynamics). Still retrofitted from trait, but has the most real data.

4. The *closest construct with predictive validity in target pop* is **Suicide Crisis Syndrome / Narrative Crisis Model** (Galynker). Designed for acute state. No EMA or fMRI yet.

5. Nothing hits all four of the user's criteria (fits scenario / mechanistic / theoretical / validated in target pop at the right timescale). **Kimi independently confirmed this gap.**

**Implication for the project**: the user's bar may not be clearable with existing literature alone. The work becomes either (a) commit to the closest-available — entrapment-like construct with explicit caveats, or (b) rebuild on a pragmatic ops construct (caller patience) with the neural model as a predictor-of-behavior rather than measurer-of-state. The earlier Option C (phenomenological target + mediator) still looks viable but needs to be re-anchored on entrapment or SCS rather than "escape motivation."

**Open for second-pass research**:
1. Verify Laessing/Karvelis 2025 suicidality DDM papers (critical if real).
2. Full read of Q3 ketamine-state-neural lit.
3. Full read of Q4 sad-music / music-therapy in SI/SA.
4. Littlewood 2019 replications? Any hourly-sub-hourly EMA in SI/SA?
5. Does the Narrative Crisis Model have any moment-to-moment measurement development in the pipeline?


