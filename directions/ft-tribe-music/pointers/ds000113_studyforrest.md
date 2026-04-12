# ds000113 / ds000113b — Studyforrest Music of the 7Ts

## Summary
The "Music of the 7Ts" data is NOT ds000145 — it's part of the **studyforrest** project.
- **OpenNeuro**: ds000113 (main studyforrest collection)
- **Legacy openfmri**: ds000113b (7T music extension specifically)
- **Paper**: Casey 2017, Frontiers in Psychology

## Dataset Details
- 20 right-handed adults (mean age 26.6)
- 7T Siemens, 1.4mm isotropic EPI, TR=2s
- 25 music clips, 6 seconds each, 5 genres:
  - **Ambient** (Brian Eno etc.) — DIRECTLY RELEVANT
  - Country
  - Heavy Metal
  - Rock'n'Roll
  - Symphonic
- Slow event-related design (4-8s inter-trial delays)
- 8 runs per subject, 153 volumes per run
- BIDS format, event timing files included

## Access
```bash
datalad install ///openneuro/ds000113
# or
openneuro-cli download ds000113
```
Full studyforrest: https://www.studyforrest.org/access.html

## Caveats for FT
1. **Clips are only 6s** — TRIBE v2 uses 100s windows. Would need to concatenate or use shorter context.
2. **7T data** — TRIBE v2 trained on 3T. Resolution/SNR difference may cause FT issues.
3. **Only 20 subjects** — small for FT, but the paper shows 1-epoch FT works with limited data.
4. **Dataset size**: ~100-200 GB total studyforrest. Music extension subset is smaller.

## Relevance
Casey showed chromagram + melodic features → OFC/IFG/MFG encoding from this data.
If we can fine-tune TRIBE v2 on this, we might get better PFC predictions for music stimuli.
The ambient genre clips are the closest thing to hold music in any public fMRI dataset.
