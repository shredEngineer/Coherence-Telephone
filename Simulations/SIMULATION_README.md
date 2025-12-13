# Coupled System Simulation

**John Bollinger | December 2025**  
**Framework #6 — Coherence Telephone**

---

> This simulation implements the equations of motion derived from the Path 1 Lagrangian and demonstrates topology-selective coupling.

---

## What This Simulation Shows

The key prediction of the Coherence Telephone framework:

**Same Chern number → Same coherence channel → Correlated dynamics**  
**Different Chern number → Different channel → Uncorrelated (noise only)**

---

## Results

### Topology Selectivity

| Node | Chern Number | Correlation with Sender | Status |
|:-----|:------------:|:-----------------------:|:-------|
| Sender | C = 3 | — | TRANSMITTER |
| Receiver_A | C = 3 | **+0.999** | MATCHED |
| Control_B | C = 2 | +0.033 | mismatched |
| Control_C | C = 1 | +0.016 | mismatched |

**Selectivity ratio: 41×**

### Visualization

![Topology Selective Simulation](Visuals/topology_selective_simulation.png)

The scatter plots show the key result:
- **MATCHED (C=3↔C=3)**: Perfect diagonal line (correlation ≈ 1.0)
- **MISMATCHED (C=3↔C=2)**: Random cloud (correlation ≈ 0.03)

### Channel Separation

![Channel Separation](Visuals/channel_separation.png)

The coherence field separates into independent channels by Chern number:
- **Channel C=3**: Driven by E·B modulation (large amplitude)
- **Channels C=1, C=2**: Remain idle (noise floor only)

---

## The Physics

### Equations of Motion

From the Path 1 Lagrangian, the coherence field evolves according to:

$$\frac{\partial^2 \Phi}{\partial t^2} + \gamma \frac{\partial \Phi}{\partial t} + m^2 \Phi = 2g \cdot \theta \cdot (\mathbf{E} \cdot \mathbf{B})$$

Where:
- **θ = 2π𝒞** is the axion angle (set by Chern number)
- **g** is the coupling constant
- **E·B** is the electromagnetic modulation

### Why Topology Creates Channels

The axion angle θ = 2π𝒞 means:
- Systems with C=3 have θ = 6π
- Systems with C=2 have θ = 4π
- Systems with C=1 have θ = 2π

Each θ value couples to a **different mode** of the coherence field. This creates natural "channels" addressed by topology.

When you modulate E·B at a C=3 node, you drive the θ=6π channel. Only other C=3 nodes couple to that channel and receive the signal.

---

## Running the Simulation

### Requirements

```
numpy
matplotlib
```

### Usage

```bash
python coupled_system_simulation.py
```

### Parameters

Edit the `Params` dataclass to adjust:

| Parameter | Default | Description |
|:----------|:-------:|:------------|
| `Nt` | 1500 | Time steps |
| `dt` | 0.01 | Time step size |
| `m` | 0.5 | Effective mass |
| `g` | 1.0 | Coupling strength |
| `gamma` | 0.05 | Damping coefficient |
| `omega` | 2.0 | Modulation frequency |
| `noise` | 0.02 | Noise level |

---

## Experimental Prediction

This simulation predicts that in a real experiment:

1. Two topological qubit systems with **matching Chern numbers** will show correlated coherence dynamics under E·B modulation

2. Systems with **different Chern numbers** will remain uncorrelated

3. The selectivity ratio should be large (>>10×) for well-prepared topological states

---

## Limitations

This is a **theoretical demonstration**, not an experimental prediction calculator.

- Coupling constants are illustrative
- Real materials have additional complexity
- Noise model is simplified
- Does not include decoherence effects

**Real validation requires laboratory measurement.**

---

## Files

| File | Description |
|:-----|:------------|
| `coupled_system_simulation.py` | Main simulation code |
| `topology_selective_simulation.png` | Main results visualization |
| `channel_separation.png` | Channel isolation diagram |

---

## Next Steps

1. Determine coupling constant g from material parameters
2. Add realistic decoherence model
3. Include spatial propagation effects
4. Make quantitative predictions for specific materials (Bi₂Se₃, Bi₂Te₃)

---

*"The simulation confirms the theory. Now we build the hardware."*

— John Bollinger, December 2025
