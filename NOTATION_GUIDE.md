# Notation Guide — Coherence Telephone Framework

## Symbol Conventions

To avoid confusion between similar-looking symbols, this framework uses the following conventions:

---

## Primary Symbols

| Symbol | Name | Meaning | Units | Notes |
|:------:|:-----|:--------|:------|:------|
| **C** | Coherence field | The proposed nonlocal field mediating information transfer | dimensionless | Primary output variable |
| **𝒞** | Chern number | Topological invariant (integer) characterizing the system | dimensionless | Always an integer ≥ 0 |
| **θ** | Axion angle | θ = 2π𝒞; determines EM coupling strength | radians | Quantized in units of π |
| **Φ** | Coherence potential | Domain-specific coherence amplitude | dimensionless | Mode-dependent: Φ_𝒞 |

---

## Electromagnetic Quantities

| Symbol | Name | Meaning | Units |
|:------:|:-----|:--------|:------|
| **E** | Electric field | Vector electric field | V/m |
| **B** | Magnetic field | Vector magnetic field | Tesla (T) |
| **E·B** | EM pseudoscalar | Dot product of E and B | V·T/m |
| **F_μν** | Field tensor | Electromagnetic field strength tensor | V/m, T |
| **A_μ** | 4-potential | Electromagnetic 4-potential | V, V·s/m |

---

## Physical Constants

| Symbol | Name | Value | Units |
|:------:|:-----|:------|:------|
| **α** | Fine structure constant | ≈ 1/137 | dimensionless |
| **ℏ** | Reduced Planck constant | 1.054 × 10⁻³⁴ | J·s |
| **c** | Speed of light | 299,792,458 | m/s |
| **e** | Elementary charge | 1.602 × 10⁻¹⁹ | C |
| **h** | Planck constant | 6.626 × 10⁻³⁴ | J·s |

---

## Framework-Specific Parameters

| Symbol | Name | Meaning | Determination |
|:------:|:-----|:--------|:--------------|
| **β** | Coupling constant | Strength of E·B → C coupling | Experimental |
| **k** | Entropy scale | Normalization in C = e^(-S/k) | Context-dependent |
| **S** | Informational entropy | System disorder measure | Calculated |
| **T** | Integration time | Time window for coherence calculation | Protocol-defined |

---

## Subscript Conventions

| Notation | Meaning |
|:---------|:--------|
| **C_A, C_B** | Coherence field at Node A, Node B |
| **𝒞_A, 𝒞_B** | Chern number of system A, system B |
| **Φ_𝒞** | Coherence potential for mode with Chern number 𝒞 |
| **θ_A, θ_B** | Axion angle of system A, system B |

---

## Key Relationships

### Topology → Coupling

$$\mathcal{C} \xrightarrow{\theta = 2\pi\mathcal{C}} \theta \xrightarrow{\Delta\mathcal{L}} \text{EM coupling}$$

### Coherence Field (E·B formulation)

$$C = \exp\left(-\beta \int_0^T |\mathbf{E} \cdot \mathbf{B}|^2 \, dt\right) \cdot \Phi_{\mathcal{C}}$$

### Axion Electrodynamics Term

$$\Delta \mathcal{L} = \frac{\theta \alpha}{2\pi} (\mathbf{E} \cdot \mathbf{B})$$

### Topological Magnetoelectric Effect

$$\mathbf{P} = \frac{\theta}{2\pi} \cdot \frac{e^2}{h} \mathbf{B} \qquad \mathbf{M} = \frac{\theta}{2\pi} \cdot \frac{e^2}{h} \mathbf{E}$$

---

## Rendering Notes

### LaTeX in GitHub Markdown

- **Inline math:** `$...$` renders as inline
- **Display math:** `$$...$$` renders as block

### Unicode Symbols

- **𝒞** = U+1D49E (Mathematical Script Capital C)
- **Φ** = U+03A6 (Greek Capital Letter Phi)
- **θ** = U+03B8 (Greek Small Letter Theta)
- **α** = U+03B1 (Greek Small Letter Alpha)
- **β** = U+03B2 (Greek Small Letter Beta)

---

## Version History

| Version | Date | Changes |
|:--------|:-----|:--------|
| 1.0 | Dec 10, 2025 | Initial notation (C for both coherence and Chern) |
| 2.0 | Dec 11, 2025 | Fixed notation conflict: C = coherence, 𝒞 = Chern |
| 2.1 | Dec 12, 2025 | Added axion electrodynamics symbols (θ, E·B, F_μν) |

---

*Notation matters. Clarity enables collaboration.*
