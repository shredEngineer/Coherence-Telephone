# Experimental Protocol: Phase 1 — Tabletop Validation

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

> **Objective:** Detect topology-specific, non-classical correlation between E·B modulation and coherence-sensitive observables, under conditions that rule out conventional electromagnetic coupling.

---

## Core Hypothesis

Two topologically-matched systems (Chern number 𝒞=3) will exhibit a measurable correlation in response to E·B modulation that is **absent** when their topologies are mismatched.

**The kill shot:** Same signal for matched AND mismatched = classical leakage (theory fails).

---

## 1. Experimental Schematic

```
┌──────────────────────────────────────────────────────────────────┐
│                    SINGLE DILUTION REFRIGERATOR                   │
│                         (Base T < 20 mK)                          │
├──────────────────────────────────────────────────────────────────┤
│                                                                   │
│   ┌─────────────────┐              ┌─────────────────┐           │
│   │   SOURCE NODE   │              │  DETECTOR NODE  │           │
│   │      (A)        │   SHIELDED   │       (B)       │           │
│   │                 │   BARRIER    │                 │           │
│   │  ┌───────────┐  │      ║       │  ┌───────────┐  │           │
│   │  │  𝒞 = 3    │  │      ║       │  │  𝒞 = 3    │  │           │
│   │  │  Array    │  │      ║       │  │  Array    │  │           │
│   │  └─────┬─────┘  │      ║       │  └─────┬─────┘  │           │
│   │        │        │      ║       │        │        │           │
│   │  ┌─────▼─────┐  │      ║       │  ┌─────▼─────┐  │           │
│   │  │ Microwave │  │      ║       │  │  Readout  │  │           │
│   │  │  Cavity   │  │      ║       │  │   Qubit   │  │           │
│   │  └─────┬─────┘  │      ║       │  └─────┬─────┘  │           │
│   │        │        │      ║       │        │        │           │
│   │  ┌─────▼─────┐  │      ║       │  ┌─────▼─────┐  │           │
│   │  │E·B Drive  │  │      ║       │  │ Resonator │  │           │
│   │  │ (ω_d, θ₁) │  │      ║       │  │ (Readout) │  │           │
│   │  └───────────┘  │      ║       │  └───────────┘  │           │
│   │                 │      ║       │                 │           │
│   └────────┬────────┘      ║       └────────┬────────┘           │
│            │               ║                │                    │
│            └───────────────╫────────────────┘                    │
│                            ║                                     │
│                    ┌───────▼───────┐                             │
│                    │  CONTROL &    │                             │
│                    │    DATA       │                             │
│                    │ ACQUISITION   │                             │
│                    └───────────────┘                             │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Key Design Principle:** Both nodes in **separately shielded compartments** within the same cryostat. Millikelvin temperatures with precise isolation control.

---

## 2. Component Specifications

### 2.1 Topological Qubit Arrays (Source A & Detector B)

| Parameter | Specification | Notes |
|:----------|:--------------|:------|
| Platform | Superconducting qubit array | Google Sycamore / Quantinuum H2 techniques |
| Topology | Tunable Chern insulator | In-situ tunable to 𝒞 = 2, 3, 4 |
| Verification | Quantized Hall conductance | Confirms topological phase |
| Coherence | T₂* > 50 μs | State-of-the-art transmon |

**Critical requirement:** Arrays must be tunable in-situ between Chern numbers for control experiments.

### 2.2 Source Node A: Modulation Cavity & Drive

| Component | Specification | Purpose |
|:----------|:--------------|:--------|
| Cavity | High-Q 3D microwave, ω_c/2π ~ 6-8 GHz | Resonant enhancement |
| E·B Modulator | Orthogonal antenna/coil pair | Crossed E and B fields |
| Drive signal | Coherent tone at ω_d | δθ(t) = θ₁ cos(ω_d t) |
| Control knob | θ₁ amplitude | Primary experimental variable |

### 2.3 Detector Node B: Readout System

| Component | Specification | Purpose |
|:----------|:--------------|:--------|
| Readout qubit | High-coherence transmon (T₂* > 50 μs) | Frequency shift sensor |
| Coupling | Dispersive to 𝒞=3 array | Coherence field → qubit shift |
| Resonator | Standard readout circuit | QND measurement |
| Measurement | Ramsey interferometry | Precise frequency determination |

### 2.4 Shared Infrastructure

| System | Specification | Purpose |
|:-------|:--------------|:--------|
| Cryostat | Dilution refrigerator, T < 20 mK | Quantum coherence |
| Magnetic shield | Cryoperm + superconducting Al | Field isolation |
| RF shield | Separate enclosures per node | EM isolation |
| Control | Phase-locked μW generators | Timing precision |
| DAQ | Ultra-low-noise digitizers | Signal acquisition |

---

## 3. Experimental Sequence

### Step 1: Calibration & Characterization

```
┌─────────────────────────────────────────────────────────────┐
│  1.1  Cool system to base temperature (< 20 mK)             │
│  1.2  Tune BOTH arrays to 𝒞 = 3                             │
│  1.3  Verify topology via transport or spectroscopy         │
│  1.4  Calibrate E·B drive amplitude θ₁ (radians)            │
│  1.5  Calibrate dispersive shift χ₀ (qubit + array ground)  │
│  1.6  Measure noise floor (no drive)                        │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Primary Experiment (Matched Topology)

```
Configuration: Source 𝒞 = 3, Detector 𝒞 = 3 (MATCHED)

For shot i = 1 to N_shot:
    
    2.1  INITIALIZE
         └─ Prepare both arrays in ground state
         └─ Reset readout qubit
    
    2.2  MODULATE
         └─ Apply E·B drive δθ(t) = θ₁ cos(ω_d t) at Node A
         └─ Duration: T_pulse = 1-10 μs
    
    2.3  MEASURE
         └─ Ramsey sequence on readout qubit (Node B)
         └─ Extract frequency shift χᵢ
    
    2.4  RECORD
         └─ Store (timestamp, θ(t), χᵢ)

Accumulate N_shot = 10⁴ to 10⁶ measurements
```

### Step 3: Control Experiment (Mismatched Topology)

```
Configuration: Source 𝒞 = 2, Detector 𝒞 = 3 (MISMATCHED)

    3.1  Re-tune Source Node A to 𝒞 = 2
         └─ Detector Node B remains at 𝒞 = 3
    
    3.2  Repeat EXACTLY the same sequence as Step 2
    
    3.3  Expected result (if hypothesis correct):
         └─ Correlated shift χ(t) → ZERO (noise floor only)
```

### Step 4: Supplementary Controls

| Control | Procedure | Purpose |
|:--------|:----------|:--------|
| **4.1 RF Shunting** | Disconnect all μW lines to Node B during modulation | Rule out EM crosstalk |
| **4.2 Frequency Detuning** | Set ω_d far off any resonance | Rule out cavity coupling |
| **4.3 Thermal Test** | Replace coherent drive with heating pulse | Rule out thermal effects |
| **4.4 Time Reversal** | Swap source/detector roles | Verify symmetry |

---

## 4. Data Analysis

### 4.1 Raw Data Structure

```
Data matrix D[i, t]:
    i = shot index (1 to N_shot)
    t = time bin
    
    D[i, t] = {
        θ(t)  : Drive envelope at time t
        χᵢ(t) : Measured frequency shift
        config: Topology configuration (3-3 or 2-3)
    }
```

### 4.2 Primary Metric: Cross-Correlation

Compute cross-correlation between drive and response:

$$C(\tau) = \frac{\langle \theta(t) \cdot \chi(t+\tau) \rangle}{\sigma_\theta \sigma_\chi}$$

**Predicted outcomes:**

| Configuration | C(0) Prediction | Physical Meaning |
|:--------------|:----------------|:-----------------|
| 𝒞=3 ↔ 𝒞=3 (matched) | **Strong peak** | Topology-mediated coupling |
| 𝒞=2 ↔ 𝒞=3 (mismatched) | **Zero** (noise) | No coupling (different channel) |

### 4.3 Secondary Metrics

| Metric | Formula | Purpose |
|:-------|:--------|:--------|
| Selectivity ratio | S = C(0)_matched / σ_mismatched | Topology discrimination |
| SNR | χ_peak / σ_noise | Detection significance |
| p-value | From null hypothesis test | Statistical confidence |

---

## 5. Success Criteria

### 5.1 Binary Success Conditions

The experiment is a **SUCCESS** if **ALL** of the following are true:

| Criterion | Threshold | Meaning |
|:----------|:----------|:--------|
| **Matched signal** | p-value < 10⁻⁵ (≥ 4.4σ) | Real correlation detected |
| **Control null** | p-value > 0.05 | No signal in mismatched case |
| **Selectivity** | S > 5 | Clear topology discrimination |
| **Reproducibility** | 3+ independent runs | Not a statistical fluke |

### 5.2 Failure Modes

The experiment **FAILS** (falsifies hypothesis) if:

| Failure Mode | Observation | Interpretation |
|:-------------|:------------|:---------------|
| **Classical leakage** | Equal signal in matched AND mismatched | EM crosstalk, not topology |
| **Null result** | No signal in either condition | Coupling too weak or mechanism wrong |
| **Inconsistent** | Non-reproducible results | Systematic error |

---

## 6. Outcome Interpretation Matrix

| Matched (3-3) | Mismatched (2-3) | Interpretation | Next Step |
|:-------------:|:----------------:|:---------------|:----------|
| ✅ Strong | ❌ Zero | **HYPOTHESIS SUPPORTED** | Proceed to Phase 2 |
| ✅ Strong | ✅ Strong | **CLASSICAL LEAKAGE** | Improve shielding or abandon |
| ❌ Zero | ❌ Zero | **NULL RESULT** | Increase sensitivity or abandon |
| ❌ Zero | ✅ Strong | **ANOMALOUS** | Investigate systematic error |

---

## 7. Timeline & Resources

### 7.1 Personnel

| Role | Responsibility | FTE |
|:-----|:---------------|:----|
| PI (Theorist) | Framework, analysis, interpretation | 0.5 |
| Experimentalist | Cryogenics, qubit fabrication, measurement | 1.0 |
| Technician | Fabrication, cooldown support | 0.5 |
| Postdoc/Student | Data acquisition, analysis | 1.0 |

### 7.2 Timeline

```
Month 1-3:   DESIGN & PROCUREMENT
             └─ Finalize component specs
             └─ Procure/fabricate arrays and cavities
             └─ Prepare control software

Month 4-6:   INTEGRATION & CALIBRATION
             └─ Cooldown and system characterization
             └─ Tune arrays to target Chern numbers
             └─ Calibrate all drives and readout

Month 7-9:   DATA COLLECTION
             └─ Primary matched-topology experiment
             └─ Control experiments (mismatched, shunted, etc.)
             └─ Statistical accumulation

Month 10-12: ANALYSIS & PUBLICATION
             └─ Data analysis and interpretation
             └─ Manuscript preparation
             └─ Peer review submission
```

### 7.3 Facility Requirements

| Requirement | Specification | Potential Sites |
|:------------|:--------------|:----------------|
| Dilution refrigerator | < 20 mK base, advanced μW control | University labs, NHMFL |
| Qubit fabrication | Transmon + tunable arrays | IBM, Google, academic fabs |
| Shielding | Multi-layer magnetic + RF | Standard cryogenic practice |

---

## 8. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|:-----|:------------|:-------|:-----------|
| Insufficient isolation | Medium | High | Multiple shielding layers, separate enclosures |
| Topology not tunable | Low | Critical | Pre-characterize arrays before cooldown |
| Signal below noise | Medium | High | Optimize photon number n, integration time |
| Qubit decoherence | Low | Medium | Use state-of-the-art fabrication |
| Systematic errors | Medium | Medium | Extensive control experiments |

---

## 9. Deliverables

### 9.1 Primary Deliverable

**Dataset:** Cross-correlation C(0) for matched vs. mismatched topology configurations, with full statistical analysis.

### 9.2 Publication

**Title:** "Search for Topology-Mediated Coherence Field Coupling in a Tunable Chern Insulator Array"

**Structure:**
1. Introduction: Coherence field hypothesis and predictions
2. Theory: Signal formula χ = (α/2π)(g₀²/Δ)(gθ₁/m)n
3. Methods: This protocol
4. Results: Cross-correlation analysis
5. Discussion: Interpretation and implications
6. Conclusion: Support/refutation of hypothesis

### 9.3 If Successful → Phase 2

**Phase 2 objective:** Increase spatial separation to separate cryostats (meters apart) while maintaining millikelvin temperatures.

**Phase 3 objective:** Earth-Moon test for faster-than-light correlation (the ultimate kill shot).

---

## 10. Connection to Theoretical Framework

This protocol tests the predictions from [PREDICTIONS_SIGNAL_STRENGTH.md](PREDICTIONS_SIGNAL_STRENGTH.md):

| Prediction | Protocol Test | Success Criterion |
|:-----------|:--------------|:------------------|
| **P1: Topology addressing** | Step 2 vs Step 3 | Signal only in matched case |
| **P2: Linear scaling** | Vary θ₁ | χ ∝ θ₁ |
| **P3: Resonance** | Sweep ω_d | Peak at ω_d = m |
| **P5: C² scaling** | Vary Chern number | Signal ∝ 𝒞² |

---

## 11. Summary

### The Experiment in One Sentence

> Modulate E·B at a 𝒞=3 source, measure qubit frequency shift at a 𝒞=3 detector, and verify the signal vanishes when source is changed to 𝒞=2.

### The Success Criterion in One Sentence

> Strong correlation for matched topology (>4.4σ), zero correlation for mismatched topology (>5× selectivity).

### The Kill Condition in One Sentence

> Equal signal in both configurations = classical leakage = theory falsified.

---

## Appendix A: Parameter Quick Reference

| Parameter | Symbol | Typical Value | Units |
|:----------|:------:|:-------------:|:------|
| Fine structure constant | α | 1/137 | — |
| Vacuum Rabi coupling | g₀/2π | 50-200 | MHz |
| Qubit-cavity detuning | Δ/2π | 1-5 | GHz |
| Drive amplitude | θ₁ | 0.1-0.5 | rad |
| Photon number | n | 10³-10⁶ | — |
| Qubit dephasing time | T₂* | >50 | μs |
| Base temperature | T | <20 | mK |
| Chern number (matched) | 𝒞 | 3 | — |
| Chern number (control) | 𝒞 | 2 | — |

---

## Appendix B: Expected Signal Estimates

From [PREDICTIONS_SIGNAL_STRENGTH.md](PREDICTIONS_SIGNAL_STRENGTH.md):

| g/m (rad⁻¹) | χ (Hz) | Integration | Feasibility |
|:------------|:------:|:-----------:|:------------|
| 10⁻³ | 290 | ~120 ms | ✅ Easy |
| 10⁻⁴ | 29 | ~12 s | ✅ Feasible |
| 10⁻⁵ | 2.9 | ~20 min | ✅ Doable |
| 10⁻⁶ | 0.29 | ~1.4 days | ⚠️ Hard |
| 10⁻⁹ | — | — | ❌ Falsified |

---

*"This protocol turns equations into measurements. If it works, we've found something real. If it fails cleanly, we've learned something true."*

— John Bollinger, December 2025
