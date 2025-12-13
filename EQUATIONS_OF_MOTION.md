# Equations of Motion: Path 1 Lagrangian

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

> This document derives the equations of motion from the Minimal Gauge-Invariant Model (Path 1). These are the equations that govern the dynamics of the coherence field and its coupling to electromagnetism.

---

## The Complete Lagrangian

Starting from the Path 1 functional form:

$$\mathcal{L} = \mathcal{L}_{\text{Maxwell}} + \mathcal{L}_{\text{axion}} + \mathcal{L}_{\text{coh}} + \mathcal{L}_{\text{int}}$$

### Term by Term

**1. Maxwell (Standard Electrodynamics)**

$$\mathcal{L}_{\text{Maxwell}} = -\frac{1}{4}F_{\mu\nu}F^{\mu\nu} = \frac{1}{2}(\mathbf{E}^2 - \mathbf{B}^2)$$

**2. Axion Electrodynamics (Topological Coupling)**

$$\mathcal{L}_{\text{axion}} = \frac{\alpha}{2\pi} \theta \, (\mathbf{E} \cdot \mathbf{B})$$

Where θ = 2π𝒞 + δθ (Chern number sets the background, fluctuations carry signal).

**3. Coherence Field (Kinetic + Potential)**

$$\mathcal{L}_{\text{coh}} = \frac{1}{2}(\partial_\mu \Phi_{\mathcal{C}})(\partial^\mu \Phi_{\mathcal{C}}) - V(\Phi_{\mathcal{C}})$$

$$= \frac{1}{2}\left(\frac{\partial \Phi_{\mathcal{C}}}{\partial t}\right)^2 - \frac{1}{2}(\nabla \Phi_{\mathcal{C}})^2 - V(\Phi_{\mathcal{C}})$$

**4. Interaction (Coherence-EM Coupling)**

$$\mathcal{L}_{\text{int}} = g \, \Phi_{\mathcal{C}}^2 \, (\mathbf{E} \cdot \mathbf{B})$$

---

## Deriving the Equations of Motion

I apply the Euler-Lagrange equations to each dynamical field.

### Equation 1: Coherence Field Dynamics

Varying the action with respect to Φ_𝒞:

$$\frac{\partial \mathcal{L}}{\partial \Phi_{\mathcal{C}}} - \partial_\mu \left( \frac{\partial \mathcal{L}}{\partial (\partial_\mu \Phi_{\mathcal{C}})} \right) = 0$$

**Result — The Coherence Wave Equation:**

$$\square \Phi_{\mathcal{C}} + \frac{dV}{d\Phi_{\mathcal{C}}} = 2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B})$$

Where $\square = \partial_t^2 - \nabla^2$ is the d'Alembertian operator.

**Physical Interpretation:**

| Term | Meaning |
|:-----|:--------|
| $\square \Phi_{\mathcal{C}}$ | Wave propagation (kinetic) |
| $\frac{dV}{d\Phi_{\mathcal{C}}}$ | Self-interaction / mass term |
| $2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B})$ | **Source term** — EM field drives coherence |

This is a **Klein-Gordon equation with an E·B source**. The electromagnetic field configuration directly pumps the coherence field.

---

### Equation 2: Modified Maxwell Equations

The axion term and interaction term modify Maxwell's equations. Varying with respect to the vector potential A_μ:

**Modified Gauss's Law:**

$$\nabla \cdot \mathbf{E} = \rho - \frac{\alpha}{2\pi}(\nabla \theta) \cdot \mathbf{B} - 2g \, \Phi_{\mathcal{C}} \, (\nabla \Phi_{\mathcal{C}}) \cdot \mathbf{B}$$

**Modified Ampère-Maxwell Law:**

$$\nabla \times \mathbf{B} - \frac{\partial \mathbf{E}}{\partial t} = \mathbf{J} + \frac{\alpha}{2\pi}\left[(\partial_t \theta)\mathbf{B} + (\nabla \theta) \times \mathbf{E}\right] + 2g \, \Phi_{\mathcal{C}} \left[(\partial_t \Phi_{\mathcal{C}})\mathbf{B} + (\nabla \Phi_{\mathcal{C}}) \times \mathbf{E}\right]$$

**The Homogeneous Equations (Unchanged):**

$$\nabla \cdot \mathbf{B} = 0$$

$$\nabla \times \mathbf{E} + \frac{\partial \mathbf{B}}{\partial t} = 0$$

---

## The Coupled System

The full dynamics are governed by three coupled equations:

### Coherence Dynamics

$$\square \Phi_{\mathcal{C}} + V'(\Phi_{\mathcal{C}}) = 2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B})$$

### Modified Gauss's Law

$$\nabla \cdot \mathbf{E} = \rho + P_{\text{axion}} + P_{\text{coh}}$$

### Modified Ampère's Law

$$\nabla \times \mathbf{B} - \partial_t \mathbf{E} = \mathbf{J} + \mathbf{J}_{\text{axion}} + \mathbf{J}_{\text{coh}}$$

---

### Effective Sources

The effective charges and currents are:

**Axion contributions:**

$$P_{\text{axion}} = -\frac{\alpha}{2\pi}(\nabla \theta) \cdot \mathbf{B}$$

$$\mathbf{J}_{\text{axion}} = \frac{\alpha}{2\pi}\left[(\partial_t \theta)\mathbf{B} + (\nabla \theta) \times \mathbf{E}\right]$$

**Coherence contributions:**

$$P_{\text{coh}} = -2g \, \Phi_{\mathcal{C}} \, (\nabla \Phi_{\mathcal{C}}) \cdot \mathbf{B}$$

$$\mathbf{J}_{\text{coh}} = 2g \, \Phi_{\mathcal{C}} \left[(\partial_t \Phi_{\mathcal{C}})\mathbf{B} + (\nabla \Phi_{\mathcal{C}}) \times \mathbf{E}\right]$$

---

## Key Physical Insights

### 1. The E·B Pump

The coherence field equation has a source term proportional to **(E·B)**:

$$\square \Phi_{\mathcal{C}} = 2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B}) - V'(\Phi_{\mathcal{C}})$$

This means: **applying crossed E and B fields pumps energy into the coherence field.**

This is exactly what our simulations showed — E·B modulation is ~100× more effective than entropy-based methods because it directly targets this source term.

### 2. Back-Reaction on EM Fields

The coherence field modifies Maxwell's equations through effective currents J_coh and charges P_coh. This means:

- Changes in Φ_𝒞 create effective electromagnetic sources
- The system is **bidirectionally coupled**
- Information can flow both ways: EM → Coherence and Coherence → EM

### 3. Topology as Addressing

The background θ = 2π𝒞 sets the baseline. Two systems with the same Chern number have the same θ background, so they couple to the same mode of the coherence field.

**Same 𝒞 → Same channel → Correlated dynamics**

---

## Simplified Case: Weak Coupling Limit

For initial experiments and simulations, assume:
- Weak coherence field: Φ_𝒞 ≪ 1
- Uniform topology: ∇θ ≈ 0
- Slowly varying: ∂_t θ ≈ 0

The equations simplify to:

**Coherence (linearized):**

$$\frac{\partial^2 \Phi_{\mathcal{C}}}{\partial t^2} - c^2 \nabla^2 \Phi_{\mathcal{C}} + m^2 \Phi_{\mathcal{C}} = 2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B})$$

Where $m^2 = V''(0)$ is the effective mass from the potential.

**EM fields (nearly standard Maxwell):**

$$\nabla \cdot \mathbf{E} \approx \rho$$

$$\nabla \times \mathbf{B} - \partial_t \mathbf{E} \approx \mathbf{J}$$

This is the regime for tabletop tests: standard EM with a weakly coupled coherence mode.

---

## The Potential V(Φ_𝒞)

The choice of potential determines the coherence field's behavior:

### Option A: Mass Term Only (Simplest)

$$V(\Phi_{\mathcal{C}}) = \frac{1}{2}m^2 \Phi_{\mathcal{C}}^2$$

Gives simple harmonic oscillator behavior. Good for initial simulations.

### Option B: Symmetry-Breaking (Richer Dynamics)

$$V(\Phi_{\mathcal{C}}) = -\frac{1}{2}\mu^2 \Phi_{\mathcal{C}}^2 + \frac{1}{4}\lambda \Phi_{\mathcal{C}}^4$$

Allows for nonzero vacuum expectation value. Could explain persistent coherence states.

### Option C: Topological Pinning (Path 2 Preview)

$$V(\Phi_{\mathcal{C}}) = V_0 \left[1 - \cos\left(\frac{\Phi_{\mathcal{C}}}{f}\right)\right]$$

Natural if Φ_𝒞 is identified with the dynamical axion. Leads to quantized behavior.

For now, I use **Option A** for simulations. The experiment will tell us which potential is correct.

---

## Simulation Strategy

With these equations, I can now:

1. **Discretize** the coherence wave equation on a lattice
2. **Apply** crossed E and B fields at the "sender" node
3. **Evolve** the coupled system forward in time
4. **Measure** Φ_𝒞 at the "receiver" node
5. **Compare** topology-matched vs. mismatched configurations

The key observable is: **Does Φ_𝒞 at the receiver correlate with E·B modulation at the sender?**

If yes, and if the correlation appears faster than light-travel time between nodes, we have our signal.

---

## Summary

### The Three Equations That Govern Everything

| Equation | Governs | Key Feature |
|:---------|:--------|:------------|
| Coherence wave equation | Φ_𝒞 dynamics | E·B source term |
| Modified Gauss | Electric field | Coherence-induced charge |
| Modified Ampère | Magnetic field | Coherence-induced current |

### The Key Coupling

$$2g \, \Phi_{\mathcal{C}} \, (\mathbf{E} \cdot \mathbf{B})$$

This term appears in all the equations. It is the bridge between electromagnetism and coherence. It is why E·B modulation works.

### The Experimental Prediction

Systems with matching Chern numbers (same θ background) will show correlated coherence dynamics when one is subjected to E·B modulation.

If that correlation is nonlocal, we've found something new.

---

## Next Steps

1. Equations of motion derived (this document)
2. Implement numerical simulation of coupled system
3. Determine coupling constant g from material parameters
4. Make quantitative predictions for signal strength
5. Design tabletop test protocol

---

*"The equations are derived. The physics is clear. Now we simulate, then we build, then we test."*

— John Bollinger, December 2025
