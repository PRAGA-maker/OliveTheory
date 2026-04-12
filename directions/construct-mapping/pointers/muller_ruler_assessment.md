# Muller 2021 as the "Ruler" for Quit Decisions

## Assessment: Promising but requires adaptation

### What Muller gives us
- Two hidden fatigue states (RF, UF) that predict when people quit
- Specific brain regions encoding each: RCZp for RF, RCZa + left MFG + right insula for UF
- A computational model: SV = R - (RF+UF) * k * E^2
- Validated: quitting probability tracks RF*effort (Z=-4.98) and UF*effort (Z=-5.17)

### Brain regions in our context (Destrieux atlas mapping)
- RCZp (MNI: 9, 5, 50) → maps to G_and_S_cingul-Mid-Post or G_and_S_cingul-Mid-Ant
  - Synthetic test rank: 57-59 (weak but nonzero)
- RCZa (MNI: -6, 20, 47) → maps to G_and_S_cingul-Ant or G_and_S_cingul-Mid-Ant
  - Synthetic test rank: 57-69 (very weak)
- Left MFG → G_front_middle — synthetic rank 45
- Right insula → S_circular_insula_ant/sup — synthetic rank 50-56

### Key limitation
Parameters (alpha, delta, theta) CANNOT be extracted from predicted fMRI alone.
They require behavioral fitting (maximum likelihood on trial-by-trial choices).
We don't have behavioral data from 988 callers.

### How to use it anyway
We don't need the parameters. We need the RELATIVE signal:
- Music A → higher RCZp activity → less recoverable fatigue → better for hold music
- Music B → lower RCZp activity → more fatigue → worse
The model tells us WHICH regions to look at. TRIBE v2 tells us what those regions
predict for a given music stimulus. The comparison is: does music A produce a
different predicted pattern in fatigue regions than music B?

### Operational definition (proposed)
"Escape-motivation proxy" = predicted activation magnitude in fatigue-encoding
regions (RCZp, RCZa, MFG, insula) + value regions (VS, SFG) during music listening.
Music that maintains higher SFG/VS activation and causes less RCZp/RCZa deactivation
is predicted to sustain longer hold times.

This is not a direct measurement of escape motivation. It's a proxy based on the
closest validated computational ruler we have.
