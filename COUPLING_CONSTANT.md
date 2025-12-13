# Coupling Constant g: Derivation from Material Parameters

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

> This document derives the coupling constant g from first principles using established axion electrodynamics in topological materials, then provides numerical estimates for real experimental systems.

---

## The Goal

Our interaction Lagrangian contains a coupling constant g:

$$\mathcal{L}_{\text{int}} = g \cdot \Phi_{\mathcal{C}}^2 \cdot (\mathbf{E} \cdot \mathbf{B})$$

To make quantitative experimental predictions, we need to determine g from measurable material parameters.

---

## Starting Point: Axion Electrodynamics in Topological Insulators

The axion electrodynamics term in topological materials is well-established:

$$\mathcal{L}_{\text{axion}} = \frac{\alpha}{2\pi} \theta \, (\mathbf{E} \cdot \mathbf{B})$$

Where:
- **α = e²/(4πε₀ℏc) ≈ 1/137** is the fine structure constant
- **θ** is the axion angle

For topological insulators:
- **θ = π** for standard 3D TIs (Bi₂Se₃, Bi₂Te₃)
- **θ = 2π𝒞** for systems with Chern number 𝒞

---

## The Magnetoelectric Coupling Coefficient

The topological magnetoelectric effect gives measurable responses:

$$\mathbf{P} = \alpha_{ME} \, \mathbf{B}$$
$$\mathbf{M} = \alpha_{ME} \, \mathbf{E}$$

Where the magnetoelectric coupling coefficient is:

$$\alpha_{ME} = \frac{\theta}{2\pi} \cdot \frac{e^2}{h} = \frac{\theta}{2\pi} \cdot \frac{\alpha}{\pi} \cdot \frac{c}{\mu_0 c^2} = \frac{\theta \alpha}{2\pi^2} \cdot \frac{1}{c\mu_0}$$

In SI units:

$$\alpha_{ME} = \frac{\theta e^2}{4\pi^2 \hbar c}$$

For **θ = π** (standard TI):

$$\alpha_{ME} = \frac{e^2}{4\pi \hbar c} = \frac{\alpha}{2\pi}$$

**Numerical value:**

$$\alpha_{ME} \approx \frac{1}{137 \times 2\pi} \approx 1.16 \times 10^{-3}$$

This is the **quantized** magnetoelectric coupling — a topological invariant.

---

## Connecting to Our Coupling Constant g

### Dimensional Analysis

In our model, the coherence field Φ_𝒞 modulates the axion term:

$$\mathcal{L}_{\text{int}} = g \cdot \Phi_{\mathcal{C}}^2 \cdot (\mathbf{E} \cdot \mathbf{B})$$

Comparing to the standard axion term:

$$\mathcal{L}_{\text{axion}} = \frac{\alpha \theta}{2\pi} (\mathbf{E} \cdot \mathbf{B})$$

The coupling g must have dimensions such that g·Φ² is dimensionless (if E·B has dimensions of energy density).

### Natural Identification

The most natural identification is:

$$g \cdot \Phi_{\mathcal{C}}^2 \equiv \frac{\alpha \theta}{2\pi} = \alpha \mathcal{C}$$

If we normalize Φ_𝒞 such that its vacuum expectation value ⟨Φ_𝒞⟩ = 1, then:

$$\boxed{g = \alpha \mathcal{C} = \frac{e^2}{4\pi\epsilon_0 \hbar c} \cdot \mathcal{C}}$$

**For C = 3:**

$$g = 3\alpha \approx \frac{3}{137} \approx 0.022$$

---

## Material-Specific Parameters

### Bismuth Selenide (Bi₂Se₃)

| Parameter | Value | Source |
|:----------|:------|:-------|
| Band gap | 0.3 eV | ARPES measurements |
| Surface Fermi velocity | 5 × 10⁵ m/s | ARPES |
| Dielectric constant ε | ~100 | Optical measurements |
| Axion angle θ | π | Topological classification |
| Effective Chern number | 1 (surface) | Band topology |

### Bismuth Telluride (Bi₂Te₃)

| Parameter | Value | Source |
|:----------|:------|:-------|
| Band gap | 0.15 eV | ARPES measurements |
| Surface Fermi velocity | 4 × 10⁵ m/s | ARPES |
| Dielectric constant ε | ~80 | Optical measurements |
| Axion angle θ | π | Topological classification |
| Effective Chern number | 1 (surface) | Band topology |

### Higher Chern Number Systems

For quantum anomalous Hall systems or engineered topological structures:

| System | Chern Number | Coupling g |
|:-------|:------------:|:----------:|
| Standard TI surface | 1 | α ≈ 0.0073 |
| Magnetic TI | 1 | α ≈ 0.0073 |
| Multilayer QAH | 2 | 2α ≈ 0.015 |
| Engineered stack | 3 | 3α ≈ 0.022 |
| High-C system | 4 | 4α ≈ 0.029 |

---

## The Full Coupling Strength

The effective coupling in the coherence equation is:

$$\text{Source} = 2g \cdot \theta \cdot (\mathbf{E} \cdot \mathbf{B}) = 2 \cdot (\alpha \mathcal{C}) \cdot (2\pi\mathcal{C}) \cdot (\mathbf{E} \cdot \mathbf{B})$$

$$= 4\pi \alpha \mathcal{C}^2 \cdot (\mathbf{E} \cdot \mathbf{B})$$

**This scales as 𝒞² — higher Chern numbers give quadratically stronger coupling.**

| Chern Number | Coupling Factor (4πα𝒞²) | Relative Strength |
|:------------:|:-----------------------:|:-----------------:|
| 1 | 0.092 | 1× |
| 2 | 0.37 | 4× |
| 3 | 0.83 | 9× |
| 4 | 1.47 | 16× |
| 5 | 2.30 | 25× |

**This is why we specify 𝒞 ≥ 3 in the protocol** — the coupling strength increases quadratically.

---

## Converting to SI Units

For practical calculations, we need g in SI units.

### Energy Density Form

The E·B term has dimensions of energy density:

$$[\mathbf{E} \cdot \mathbf{B}] = \frac{\text{V}}{\text{m}} \cdot \text{T} = \frac{\text{J}}{\text{m}^3}$$

### Coupling in SI

$$g_{\text{SI}} = \alpha \mathcal{C} \cdot \epsilon_0 c = \frac{e^2 \mathcal{C}}{4\pi \hbar c} \cdot \epsilon_0 c$$

**Numerical value for 𝒞 = 3:**

$$g_{\text{SI}} = 3 \times \frac{1}{137} \times (8.85 \times 10^{-12}) \times (3 \times 10^8)$$

$$g_{\text{SI}} \approx 5.8 \times 10^{-5} \, \text{s/Ω}$$

---

## Experimental Verification

### Method 1: Faraday/Kerr Rotation

The magnetoelectric coupling causes Faraday rotation:

$$\theta_F = \alpha_{ME} \cdot d \cdot B$$

Where d is the sample thickness. Measuring θ_F vs B gives α_ME, which constrains g.

**Expected rotation for Bi₂Se₃:**
- At B = 1 T, d = 10 nm: θ_F ~ 1 mrad

### Method 2: Quantized Magnetoelectric Response

Apply crossed E and B fields, measure induced polarization:

$$P = \frac{\theta \alpha}{2\pi^2} \cdot B$$

For θ = π, B = 1 T:

$$P \approx 1.2 \times 10^{-11} \, \text{C/m}^2$$

### Method 3: Surface Hall Conductance

The surface carries quantized Hall conductance:

$$\sigma_{xy} = \frac{e^2}{h} \cdot \mathcal{C} = (3.87 \times 10^{-5} \, \text{S}) \cdot \mathcal{C}$$

Measuring σ_xy confirms the Chern number and thus g.

---

## Updated Simulation Parameters

With the derived coupling constant:

### Normalized Units (for simulation)

If we work in units where ℏ = c = 1 and normalize fields appropriately:

$$g_{\text{norm}} = \alpha \mathcal{C}$$

| Parameter | Value | Justification |
|:----------|:------|:--------------|
| g (𝒞=1) | 0.0073 | α |
| g (𝒞=2) | 0.015 | 2α |
| g (𝒞=3) | 0.022 | 3α |
| g (𝒞=4) | 0.029 | 4α |

### Physical Units (for experiment)

For E in V/m and B in Tesla:

$$\text{Coupling energy density} = g_{\text{SI}} \cdot (\mathbf{E} \cdot \mathbf{B})$$

**Example:** E = 10⁶ V/m, B = 1 T, 𝒞 = 3

$$\text{Energy density} \approx 5.8 \times 10^{-5} \times 10^6 \approx 58 \, \text{J/m}^3$$

---

## Summary Table

| Quantity | Symbol | Formula | Value (𝒞=3) |
|:---------|:------:|:--------|:------------|
| Fine structure constant | α | e²/(4πε₀ℏc) | 1/137 ≈ 0.0073 |
| Axion angle | θ | 2π𝒞 | 6π ≈ 18.85 |
| Base coupling | g | α𝒞 | 0.022 |
| Full coupling factor | 4πα𝒞² | — | 0.83 |
| Magnetoelectric coefficient | α_ME | θα/(2π²) | 0.0034 |

---

## Key Results

1. **The coupling constant g = α𝒞** — directly proportional to fine structure constant and Chern number

2. **The effective coupling scales as 𝒞²** — this is why higher Chern numbers dramatically improve signal strength

3. **For 𝒞 = 3: g ≈ 0.022** — this replaces the arbitrary g = 1.0 used in initial simulations

4. **The coupling is quantized** — it takes discrete values set by topology, not continuous material parameters

5. **Measurement methods exist** — Faraday rotation, magnetoelectric response, and Hall conductance all constrain g

---

## Updated Equations of Motion

With the derived coupling:

$$\square \Phi_{\mathcal{C}} + m^2 \Phi_{\mathcal{C}} = 2(\alpha \mathcal{C}) \cdot (2\pi\mathcal{C}) \cdot \Phi_{\mathcal{C}} \cdot (\mathbf{E} \cdot \mathbf{B})$$

$$\boxed{\square \Phi_{\mathcal{C}} + m^2 \Phi_{\mathcal{C}} = 4\pi\alpha\mathcal{C}^2 \cdot \Phi_{\mathcal{C}} \cdot (\mathbf{E} \cdot \mathbf{B})}$$

The 𝒞² scaling is the key prediction: **double the Chern number, quadruple the coupling.**

---

## References

1. Qi, X.-L., Hughes, T. L., & Zhang, S.-C. (2008). Topological field theory of time-reversal invariant insulators. *Physical Review B*, 78(19), 195424.

2. Essin, A. M., Moore, J. E., & Vanderbilt, D. (2009). Magnetoelectric polarizability and axion electrodynamics in crystalline insulators. *Physical Review Letters*, 102(14), 146805.

3. Wu, L., et al. (2016). Quantized Faraday and Kerr rotation and axion electrodynamics of a 3D topological insulator. *Science*, 354(6316), 1124-1127.

4. Morimoto, T., et al. (2015). Topological magnetoelectric effects in thin films of topological insulators. *Physical Review B*, 92(8), 085113.

---

*"The coupling is quantized by topology. Nature has already set the dial."*

— John Bollinger, December 2025
