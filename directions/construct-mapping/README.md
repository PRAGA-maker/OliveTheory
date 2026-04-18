# Construct Mapping: Escape Motivation

## Purpose

Operationally define what we're measuring when we say "escape motivation" in the 988 hold-music context, and identify the paper(s) that give us the best available instrument and validation path.

## Current state

**The single-anchor framing is retracted.** Earlier iterations tried to commit to one paper (Muller 2021 → CEMP framework, then Pedersen 2021 AAC-DDM, then briefly Millner 2019). Each attempt uncovered limits that made single-anchor framing dishonest.

The current read of the space is in `measurement_framework.md` (rewritten 2026-04-18). Structure:
1. Problem space
2. Five legitimate views of the problem (computational-parameter, neural-fingerprint, phenomenological, operational, sustained-dynamics)
3. X ≈ Y equivalences across literatures (the underlying nomological network)
4. Frontier of papers in contention (15 papers across 5 tiers)
5. An opinionated take at the end

## Critical gap confirmed by second-pass research

Kimi K2.5 Thinking, in three independent queries (nomology, Function-1 candidates, Millner-fMRI feasibility), converged on: **no published paper provides brain-activation→escape-motivation-parameter mapping in an SI/SA population.** The closest-available candidate is **Ji et al. 2021** (J Psych Res 139:14-24) — acute unmedicated depressed attempters + fMRI + 4-param Bayesian BART model + parameter-to-region mapping (insula↔pain avoidance, dlPFC↔loss sensitivity). But it's scoped to planful-depressive subtype and uses BART not a DDM.

The honest path forward is triangulation across Karvelis (theory) + Brown/Ji (target-pop neural) + Pedersen (methodology scaffold) + Millner (behavioral validation) + Shneidman/Gilbert (phenomenological framing). No single paper does all.

## Working files in this folder

- `measurement_framework.md` — **primary current doc**. Problem/solution space, frontier of papers, X≈Y equivalences, opinionated take.
- `escape_motivation_v2.md` — analyst working notebook. Chronological logs of Kimi pass-1 and pass-2 findings, paper-by-paper summaries, retractions, exploratory threads.
- `pointers/` — paper-level analyses
  - `pedersen_aac_ddm_analysis.md` — structural analysis of Pedersen's methodology
  - `muller_ruler_assessment.md` — earlier Muller-as-anchor assessment (now a secondary view)

## Load-bearing PDFs (in `context/papers/`)

- `ji2021_motivation_decision_suicide.pdf` — closest-available instrument candidate
- `brown2020_vmpfc_suicide.pdf` — target-pop vmPFC disruption, Dombrovski lab
- `karvelis2022_active_inference_suicide.pdf` — theoretical framework
- `pedersen2021_aac_ddm.pdf` — methodology scaffold
- `millner2019_active_escape.pdf` — behavioral RL-DDM ground truth
- `millner2018_active_escape_healthy.pdf` — paradigm paper
- `kleiman2018_realtime_monitoring.pdf` — EMA dynamics context
- `tribev2.pdf` — brain-encoding model

## Next steps

Per `measurement_framework.md` Section 5:
1. Decide (user) how opinionated to make the final framework — primary+fallback or fallback-only
2. Decide how to handle Ji's subtype-specificity (accept as scope limit or pursue broader)
3. Decide whether to pursue the construct-validity writeup as a standalone paper
4. Decide whether Muller fatigue or Karvelis belief-decay is the temporal-dynamics overlay

## Retractions

- **Laessing et al. 2025 bioRxiv**: fabricated by Kimi, does not exist. Remove from all prior references.
- **Dombrovski 2024 "Neural Dynamics..."**: conference abstract only (SOBP May 2024), not peer-reviewed. Demote.
- **CEMP (Cortical Escape Motivation Profile)**: superseded framework. Too narrow, prematurely committed to cortical-only pattern-matching.

## Methodological notes

Kimi's outputs must be citation-verified before being treated as load-bearing. Laessing 2025 was a hallucinated citation with specific author names and DOI pattern — it propagated through several revisions of the analysis before second-pass verification caught it. Always cross-check with PubMed or publisher-direct before building arguments on any Kimi-surfaced paper. (This rule is now encoded in `.claude/skills/research-paper-pointers.md`.)
