# Construct Mapping: Escape Motivation

## Purpose
Operationally define what we're measuring. "Escape motivation" isn't a canonical neuroscience term. The adjacent constructs are:
- **Entrapment** (Gilbert & Allan 1998) — perceived inability to escape aversive situation
- **Escape vs. avoidance** (Millner 2018) — RL+DDM Pavlovian bias toward active escape
- **Defensive flight** (Mobbs 2020) — vmPFC→PAG transition under threat imminence
- **Fatigue-driven quitting** (Muller 2021) — recoverable + unrecoverable fatigue → value depletion → quit

## Motivation
A 988 caller on hold is making a continuous decision: stay or hang up. This maps to multiple constructs simultaneously. We need to pick which one(s) give us measurable brain signals without over-defining.

## Critical Context
- Millner's RLDDM gives computational parameters (w_escape, drift rate) but NO brain mapping — it's behavioral only
- Mobbs gives brain regions (vmPFC, PAG) but the mapping is qualitative, not parametric
- Muller gives the most concrete brain→behavior link: frontal fatigue signals predict quitting
- Entrapment (Malhi 2022) shows PFC hypoactivation in suicide attempters — overlaps with our PFC signal concern
- ds001814 on OpenNeuro literally studies approach-avoidance conflict with aversive stimulation during fMRI

## What Does Working Look Like?
A decision document: "We measure X (operational definition), using Y (brain signal/region), validated by Z (existing paper that already built this ruler)." The ruler exists — we're not building new theory, we're picking which existing instrument to adopt.

## Next Experiments
1. **Read Muller 2021 in detail** — their fatigue model has the most direct quit-prediction utility
2. **Check ds001814** — approach-avoidance conflict fMRI. If this dataset has event-level timing + BOLD, it could validate the escape→brain mapping directly
3. **Make the call** — write a 1-page operational definition, get human sign-off
