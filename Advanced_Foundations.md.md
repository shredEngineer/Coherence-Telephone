# Advanced Theoretical Foundations

## Gauge Invariance & The Coherence Field

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

## The Critical Question

Any field theory that interacts with electromagnetism must respect **gauge invariance** — the fundamental symmetry that physical observables don't change under transformations like:

$$A_\mu \rightarrow A_\mu + \partial_\mu \lambda$$

This isn't a technicality. It's what ensures the theory is physically meaningful and doesn't produce infinite or nonsensical results.

For the coherence field Φ_𝒞 coupled via axion electrodynamics, there are two rigorous paths to ensure gauge invariance.

---

## Two Theoretical Frameworks

### Framework V1: Minimal Gauge-Invariant Model (Conservative)

**Treat Φ_𝒞 as a gauge-invariant scalar that couples to the already gauge-invariant axion term.**

This is the safest, most defensible approach. We don't modify Maxwell's equations; we add the coherence field as a modulator that interacts only through the gauge-invariant object **E·B**.

#### The Coupling

The Lagrangian density has an interaction term:

$$\mathcal{L}_{\text{int}} = f(\Phi_{\mathcal{C}}) \cdot \frac{\theta \alpha}{2\pi} (\mathbf{E} \cdot \mathbf{B})$$

Where:
- **f(Φ_𝒞)** is a function of the gauge-invariant coherence field (e.g., Φ_𝒞, Φ_𝒞²)
- **E·B** is itself gauge-invariant (derived from F_μν F̃^μν)
- The entire term is therefore **manifestly gauge-invariant**

#### Physical Picture

The coherence field Φ_𝒞 **modulates the strength** of the already-established topological magnetoelectric effect:

```
Topology (Chern number 𝒞) → Sets the channel (θ = 2π𝒞)
Coherence field (Φ_𝒞)    → Carries the signal by varying the coupling
```

#### Advantages
- ✅ Absolutely secure from gauge problems
- ✅ Closely tied to known, measured physics
- ✅ Directly testable with current experimental design
- ✅ Conservative — minimizes new assumptions

#### Limitations
- The coherence field is somewhat passive
- Its dynamics are less constrained
- Doesn't explain the *origin* of Φ_𝒞

---

### Framework V2: Dynamical Axion Model (Speculative)

**Promote the axion angle θ to a dynamical field θ(x,t), and identify it with the coherence field Φ_𝒞.**

This is bolder and more fundamental. In this view, Φ_𝒞 *is* the dynamical axion field for the topological material.

#### The Coupling

The interaction term is the standard axion electrodynamics term, but now θ is dynamical:

$$\mathcal{L}_{\text{axion}} = \frac{\alpha}{4\pi} \theta(x,t) F_{\mu\nu} \tilde{F}^{\mu\nu} = \frac{\alpha}{2\pi} \theta(x,t) (\mathbf{E} \cdot \mathbf{B})$$

**Gauge invariance is guaranteed** because the topological term θFF̃ is gauge-invariant for both smooth A_μ and θ.

#### The Dynamics

For θ(x,t) to be a true dynamical field, we need a **kinetic term**:

$$\mathcal{L}_{\text{kin}} = \frac{1}{2\Lambda^2} (\partial_\mu \theta)(\partial^\mu \theta)$$

Where **Λ** is an energy scale.

A **potential term** V(θ) determines its vacuum state, which should be pinned to θ = 2π𝒞 to encode the topology:

$$V(\theta) = V_0 \left[1 - \cos\left(\theta - 2\pi\mathcal{C}\right)\right]$$

#### Physical Picture

The coherence field **is** the fluctuating part of the topological axion mode:

```
θ(x,t) = 2π𝒞 + δθ(x,t)
         ↑         ↑
    Topological   Dynamical fluctuation
    vacuum        (= coherence field Φ_𝒞)
```

Encoding information modulates this dynamical θ field at one location, and a nonlocal interaction law (our hypothesis) allows this modulation to appear elsewhere.

#### Advantages
- ✅ Deeply elegant — the field is fundamental and dynamic
- ✅ Naturally leads to wave equations and propagating modes
- ✅ Explains the *nature* of the coherence field
- ✅ Points toward a complete field theory

#### Limitations
- Highly speculative
- Requires explaining why this dynamical mode is nonlocal
- Must explain how it remains pinned to topological sector
- Needs more theoretical development before experimental predictions

---

## Complete Lagrangian (Framework V2)

For reference, the full dynamical axion Lagrangian would be:

$$\mathcal{L} = -\frac{1}{4}F_{\mu\nu}F^{\mu\nu} + \frac{1}{2\Lambda^2}(\partial_\mu\theta)(\partial^\mu\theta) - V(\theta) + \frac{\alpha}{2\pi}\theta(\mathbf{E}\cdot\mathbf{B})$$

| Term | Physical Meaning |
|:-----|:-----------------|
| -¼F_μν F^μν | Standard Maxwell electrodynamics |
| ½Λ⁻²(∂θ)² | Kinetic energy of dynamical axion |
| V(θ) | Potential pinning θ to topological vacuum |
| (α/2π)θ(E·B) | Axion-photon coupling |

---

## Experimental Strategy

### Current Tests: Use Framework V1

For the Earth-Moon latency test and near-term experiments, Framework V1 is sufficient and appropriate:

- It makes clear, falsifiable predictions
- It's manifestly gauge-invariant
- It doesn't require resolving deeper theoretical questions first

### Future Development: If V1 Succeeds, Develop V2

If experiments confirm nonlocal coupling:

1. The next major theoretical task will be to promote θ to a dynamical field
2. Determine the energy scale Λ from experimental data
3. Characterize the potential V(θ) and its topological pinning
4. Develop the full nonlocal propagator for θ fluctuations

---

## Response to Gauge Invariance Questions

When asked about gauge invariance, the complete answer is:

> "Gauge invariance is enforced by design. In our minimal model (Framework V1), the coherence field Φ_𝒞 couples exclusively through the gauge-invariant pseudoscalar E·B of the established axion electrodynamics term. In a more advanced formulation (Framework V2), Φ_𝒞 is identified with a dynamical axion field θ(x,t), where gauge invariance is inherent in the topological term θFF̃. The first formulation ensures consistency for current tests; the second points to deeper theory if the effect is real."

---

## Summary

| Framework | Type | Gauge Invariance | Use Case |
|:----------|:-----|:-----------------|:---------|
| **V1** | Minimal/Conservative | Via gauge-invariant E·B coupling | Current experiments |
| **V2** | Dynamical/Speculative | Inherent in θFF̃ topology | Future theory development |

Both frameworks are internally consistent. V1 is the experimental workhorse. V2 is the theoretical endgame.

---

## References

1. Qi, Hughes, Zhang (2008): "Topological field theory of time-reversal invariant insulators"
2. Essin, Moore, Vanderbilt (2009): "Magnetoelectric polarizability and axion electrodynamics"
3. Wilczek (1987): "Two applications of axion electrodynamics"
4. Peccei & Quinn (1977): Original axion mechanism
5. Weinberg (1978), Wilczek (1978): Axion as pseudo-Nambu-Goldstone boson

---

*"The conservative model gets us to the test. The dynamical model explains what we find."*

— John Bollinger, December 2025
