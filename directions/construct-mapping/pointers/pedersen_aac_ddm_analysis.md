# Pedersen 2021 AAC-DDM Analysis

## Paper
Pedersen et al. (2021). "Computational phenotyping of brain-behavior dynamics underlying approach-avoidance conflict in major depressive disorder." PLOS Computational Biology, 17(5): e1008955. DOI: 10.1371/journal.pcbi.1008955

## Key Findings
- AAC task: reward (points) vs. aversion (IAPS images) offered simultaneously. Approach = gain points + see aversive image. Avoid = no points, neutral image.
- 18 MDD (unmedicated) + 24 HC females
- Hierarchical DDM fit via HDDM toolbox

## Parameter-Region Mappings
| Parameter | Region | Atlas | In TRIBE v2? |
|-----------|--------|-------|-------------|
| Drift rate (v) | Caudate | Oxford-Harvard subcortical | NO |
| Drift rate (v) | pgACC | 12mm sphere at MNI (0,40,0) — ventral/pregenual, NOT dorsal ACC | PARTIAL — maps to G_and_S_cingul-Ant or ventral cingulate, NOT the dACC parcel we tested |
| Threshold (a) | STN | FSL atlas | NO |
| Bias (z) | NAcc | Oxford-Harvard subcortical | NO |

## Clinical Findings
- MDD: reduced reward sensitivity (drift rate), p=0.99
- MDD: NAcc flips from approach-bias (HC) to avoidance-bias, p(HC>MDD)=0.971
- Model classifies MDD AUC=0.68, accuracy 69% at 6-month follow-up
- NAcc parameter predicts future depression severity (b=-1495, p=0.04)
- Reward sensitivity negatively correlated with perceived stress (b=-14.74, p=0.039)

## Verdict for Our Use
**Theoretically perfect, practically blocked.** 3 of 4 brain-mapped parameters are subcortical. We can only access pgACC (drift rate, partial contribution). The most diagnostic feature (NAcc avoidance bias in MDD) is inaccessible with cortical-only TRIBE v2.

**Salvageable components**: pgACC drift-rate modulation is cortical and testable. The behavioral model (what drives approach vs. avoidance) is sound even if we can't decode all parameters from brain signals.

**If subcortical becomes available**: This becomes the gold-standard decision framework. Monitor GitHub Issue #23.
