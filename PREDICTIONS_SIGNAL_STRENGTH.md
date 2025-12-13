# Quantitative Signal Strength Predictions

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

> This document derives **quantitative, falsifiable predictions** for tabletop experiments. It turns theory into engineering specifications.

---

## 1. The Minimal Model Lagrangian

Our starting point is the gauge-invariant Lagrangian where the coherence field Φ_C modulates the axion term:

$$\mathcal{L} = \underbrace{-\frac{1}{4\mu_0}F_{\mu\nu}F^{\mu\nu}}_{\text{Maxwell}} + \underbrace{\frac{\alpha}{2\pi} \left[2\pi\mathcal{C} + \delta\theta(t)\right] (\mathbf{E} \cdot \mathbf{B})}_{\text{Topological Axion Coupling}} + \underbrace{\frac{1}{2}\dot{\Phi}_C^2 - \frac{1}{2}m^2\Phi_C^2}_{\text{Free Coherence Field}}$$

From our previous derivation ([COUPLING_CONSTANT.md](COUPLING_CONSTANT.md)):

$$g = \alpha \cdot \mathcal{C} = \frac{\mathcal{C}}{137}$$

---

## 2. Experimental Assumptions

For a realistic tabletop test, we assume:

| Label | Assumption | Justification |
|:------|:-----------|:--------------|
| **A1** | Small signal | Modulation δθ(t) ≪ background 2π𝒞 |
| **A2** | Resonant cavity | Single dominant microwave mode at ω_c |
| **A3** | Coherent drive | δθ(t) = θ₁ cos(ω_d t) |
| **A4** | On-resonance | Drive frequency ω_d ≈ m (coherence field mass) |
| **A5** | Dispersive readout | Topological qubit frequency shifts with local Φ_C |

---

## 3. The Measurable Signal: Qubit Frequency Shift

The interaction causes a **dispersive shift** χ on the detector qubit. This is the measurable signal.

### 3.1 Effective Hamiltonian

Under the rotating wave approximation (RWA):

$$H_{\text{eff}}/\hbar = \omega_c a^\dagger a + \frac{\omega_q}{2}\sigma_z + \chi(t) \, a^\dagger a \, \sigma_z$$

Where χ(t) is the **time-dependent dispersive coupling** induced by the coherence field.

### 3.2 Coherence Field Response

The driven coherence field acts as a transducer. Solving the equation of motion:

$$\ddot{\Phi}_C + m^2\Phi_C = g \cdot \delta\theta(t)$$

Gives the steady-state amplitude (on resonance):

$$\Phi_C^{\text{ss}} \approx \frac{g \theta_1}{m}$$

### 3.3 Final Signal Formula

The qubit frequency shift is:

$$\boxed{\chi(t) \approx \frac{\alpha}{2\pi} \cdot \frac{g_0^2}{\Delta} \cdot \frac{g \theta_1}{m} \cdot n \cdot \cos(\omega_d t)}$$

**Parameter definitions:**

| Symbol | Meaning | Typical Range |
|:-------|:--------|:--------------|
| α/2π | Fundamental axion coupling | 1.16 × 10⁻³ |
| g₀ | Vacuum Rabi coupling (qubit-cavity) | 50–200 MHz |
| Δ | Qubit-cavity detuning (ω_q - ω_c) | 1–5 GHz |
| g | δθ-to-Φ_C coupling = α𝒞 | 0.007–0.037 |
| θ₁ | Axion angle modulation amplitude | 0.1–0.5 rad |
| m | Coherence field effective mass | **Unknown** (search target) |
| n | Pump cavity photon number | 10³–10⁶ |

---

## 4. Numerical Estimates

### 4.1 Parameter Table

| Parameter | Symbol | Conservative | Optimistic | Unit |
|:----------|:------:|:------------:|:----------:|:-----|
| Fine structure coupling | α/2π | 1.16 × 10⁻³ | 1.16 × 10⁻³ | — |
| Vacuum Rabi coupling | g₀/2π | 50 | 200 | MHz |
| Qubit-cavity detuning | Δ/2π | 1 | 5 | GHz |
| Drive amplitude | θ₁ | 0.1 | 0.5 | rad |
| Photon number | n | 10³ | 10⁶ | — |
| **Unknown coupling ratio** | g/m | **10⁻³** | **1** | rad⁻¹ |

### 4.2 Predicted Signal Strength

| Scenario | χ/2π | Detectability |
|:---------|:----:|:--------------|
| **Conservative** | **≈ 0.6 Hz** | Hours of integration |
| **Moderate** | **≈ 1 kHz** | ~40 shots (< 1 second) |
| **Optimistic** | **≈ 1.5 MHz** | Single-shot detection |

**Key insight:** The signal spans **6 orders of magnitude** based primarily on the unknown coupling g/m. This is the central parameter the experiment must measure.

---

## 5. Signal-to-Noise Analysis

### 5.1 SNR Formula

For qubit frequency shift measurement limited by dephasing time T₂*:

$$\text{SNR} \approx \frac{\chi}{\Gamma_{\text{noise}}} \cdot \sqrt{N_{\text{shots}}}$$

Where:
- Γ_noise ≈ 1/(πT₂*) is the qubit linewidth
- N_shots is the number of repeated measurements

### 5.2 State-of-the-Art Parameters

| Parameter | Value | Source |
|:----------|:------|:-------|
| T₂* (transmon qubit) | 50 μs | Current technology |
| Γ_noise/2π | 6.4 kHz | Derived |
| Single-shot SNR floor | ~10⁻⁴ | Quantum limit |

### 5.3 Detection Requirements

| Signal χ/2π | Required Shots | Integration Time |
|:------------|:--------------:|:-----------------|
| 1 MHz | 1 | **Single shot** |
| 10 kHz | ~1 | < 1 ms |
| 1 kHz | ~40 | < 1 second |
| 100 Hz | ~4,000 | ~minutes |
| 1 Hz | ~40,000,000 | **~hours** |

**Feasibility threshold:** The experiment is feasible if g/m > 10⁻⁶ rad⁻¹

---

## 6. Specific Falsifiable Predictions

### Prediction 1: Topology Addressing

**Statement:** The signal χ will be **maximal** when Chern numbers match (𝒞_A = 𝒞_B) and **vanish** for mismatched topology.

| Configuration | Expected Signal |
|:--------------|:----------------|
| 𝒞_A = 3, 𝒞_B = 3 | **Maximum** |
| 𝒞_A = 3, 𝒞_B = 2 | **Zero** (noise only) |
| 𝒞_A = 3, 𝒞_B = 1 | **Zero** (noise only) |

**Test:** Measure χ for matched vs mismatched topologies. Selectivity ratio should exceed 10×.

### Prediction 2: Linear Scaling

**Statement:** The signal χ scales **linearly** with:
- Drive amplitude θ₁
- Pump photon number n

$$\chi \propto \theta_1 \cdot n$$

**Test:** Vary θ₁ and n independently, verify linear relationship.

### Prediction 3: Resonance Peak

**Statement:** The signal shows a sharp **Lorentzian resonance** when drive frequency ω_d equals coherence field mass m.

$$\chi(\omega_d) \propto \frac{1}{(\omega_d - m)^2 + \gamma^2}$$

**Test:** Sweep ω_d, measure χ. Peak location determines m.

### Prediction 4: Chern Number Quantization

**Statement:** The background (unmodulated) dispersive shift has a **quantized component** proportional to 𝒞.

$$\chi_{\text{background}} = \chi_0 \cdot \mathcal{C}$$

**Test:** Measure background shift for 𝒞 = 1, 2, 3, 4. Verify integer ratios.

### Prediction 5: Quadratic Coupling Scaling

**Statement:** Signal strength scales as 𝒞² (from our derived g = α𝒞 and effective coupling 4πα𝒞²).

| Chern Number | Relative Signal |
|:------------:|:---------------:|
| 𝒞 = 1 | 1× |
| 𝒞 = 2 | 4× |
| 𝒞 = 3 | 9× |
| 𝒞 = 4 | 16× |

**Test:** Measure signal at different 𝒞 values. Verify quadratic scaling.

---

## 7. Experimental Protocol

### Phase 1: Existence Test

**Goal:** Detect any signal above noise floor

1. Prepare matched topology systems (𝒞_A = 𝒞_B = 3)
2. Apply E·B modulation at sender
3. Measure qubit frequency shift at receiver
4. Integrate until SNR > 5 or hit integration limit

**Success criterion:** χ > 5σ above noise

### Phase 2: Topology Selectivity

**Goal:** Confirm addressing mechanism

1. Measure χ for 𝒞_A = 𝒞_B (matched)
2. Measure χ for 𝒞_A ≠ 𝒞_B (mismatched)
3. Compute selectivity ratio

**Success criterion:** Selectivity > 10×

### Phase 3: Parameter Extraction

**Goal:** Measure unknown coupling g/m

1. Sweep drive frequency ω_d
2. Find resonance peak
3. Extract m from peak location
4. Extract g from peak amplitude

**Success criterion:** Determine g/m to within factor of 2

### Phase 4: Scaling Verification

**Goal:** Confirm theoretical predictions

1. Vary θ₁, verify linear scaling
2. Vary n, verify linear scaling
3. Vary 𝒞, verify quadratic scaling

**Success criterion:** Scaling exponents within ±0.2 of predicted values

---

## 8. Kill Conditions

The theory is **falsified** if:

1. **No signal detected** after integration to g/m < 10⁻⁹ rad⁻¹
2. **No topology selectivity** — matched and mismatched show same signal
3. **Non-linear scaling** — χ vs θ₁ or n deviates from linear
4. **No resonance** — χ independent of drive frequency ω_d

---

## 9. Connection to Earth-Moon Test

If tabletop tests succeed, the ultimate test is **faster-than-light correlation**:

| Parameter | Value |
|:----------|:------|
| Earth-Moon distance | 384,400 km |
| Light travel time | 1.28 seconds |
| Required timing precision | < 100 ms |

**Kill shot:** Measure correlation latency. If > 1.28 s, coherence field propagates at c (standard physics). If < 1.28 s, **nonlocal correlation confirmed**.

---

## 10. Summary

### The Signal Formula

$$\chi(t) \approx \frac{\alpha}{2\pi} \cdot \frac{g_0^2}{\Delta} \cdot \frac{g \theta_1}{m} \cdot n \cdot \cos(\omega_d t)$$

### Key Unknowns

| Unknown | Method to Determine |
|:--------|:--------------------|
| m (coherence field mass) | Resonance sweep |
| g/m (coupling ratio) | Signal amplitude measurement |

### Feasibility

| g/m Range | Signal | Detection |
|:----------|:-------|:----------|
| > 10⁻³ | MHz | Trivial |
| 10⁻³ – 10⁻⁶ | Hz–kHz | Feasible |
| < 10⁻⁶ | Sub-Hz | Challenging |
| < 10⁻⁹ | — | Theory falsified |

---

## References

1. Qi, X.-L., Hughes, T. L., & Zhang, S.-C. (2008). Topological field theory of time-reversal invariant insulators. *PRB* 78, 195424.

2. Essin, A. M., Moore, J. E., & Vanderbilt, D. (2009). Magnetoelectric polarizability and axion electrodynamics. *PRL* 102, 146805.

3. Blais, A., et al. (2021). Circuit quantum electrodynamics. *Rev. Mod. Phys.* 93, 025005.

4. Wu, L., et al. (2016). Quantized Faraday and Kerr rotation. *Science* 354, 1124.

---

*"The formula tells you what to build. The predictions tell you what to measure. The kill conditions tell you when to stop."*

— John Bollinger, December 2025
