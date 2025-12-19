# Coherence Telephone
### Suppose the vacuum has been listening the whole time. We just learned its frequency.

**"What if quantum 'spookiness' isn’t a bug — it’s the signature of a deeper substrate?"**

The Coherence Telephone is a testable proposal: topologically protected qubits (Chern ≥ 3) coupled via axion electrodynamics can transmit information instantly across arbitrary distance by modulating the shared coherence field — not the qubit state.

One experiment decides everything: **Earth–Moon latency test.**
* Signal arrives in **<1.28 seconds** → The field is real.
* Signal arrives at **≥1.28 seconds** → Hypothesis falsified.

All hardware exists today. All math is public. All code runs on a laptop.

**Your move.**

— *John Bollinger (@AlbusLux1)*
*December 2025*

---

## 📂 Project Documentation

Click the sections below to access the files.

<details>
<summary><h3>📄 Section 1: Core Whitepapers & Physics (Start Here)</h3></summary>
<br>
These documents outline the technical and architectural foundations. They represent the "physics" of the system.

* **[📄 Read: Technical Whitepaper v2](docs/whitepapers/TECHNICAL_WHITEPAPER_v2.md)**
    * *The primary technical overview of the system.*
* **[📄 Read: Axion Electrodynamics Whitepaper](docs/whitepapers/AXION_ELECTRODYNAMICS_WHITEPAPER.md)**
    * *Deep dive into the coupling mechanism.*
* **[📄 Read: Advanced Foundations](docs/Math/Advanced_Foundations.md)**
    * *Mathematical derivations and core theory.*
* **[📄 Read: Equations of Motion](docs/Math/EQUATIONS_OF_MOTION.md)**
    * *The governing equations for the coherence field.*
* **[📄 Read: Functional Form](docs/Math/FUNCTIONAL_FORM.md)**
    * *Details on the functional form of the interaction.*
* **[📄 Read: Coupling Constant](docs/Math/COUPLING_CONSTANT.md)**
    * *Analysis of the coupling constants.*
* **[📄 Read: Mismatch Sweep Analysis](docs/whitepapers/MISMATCH_SWEEP_ANALYSIS.md)**
</details>

<details>
<summary><h3>🧠 Section 2: Philosophy & Deep Vision</h3></summary>
<br>
Understanding the "Why" and the nature of the coherence field.

* **[📄 Read: The Coherence Field](docs/Philosophy/THE_COHERENCE_FIELD_AS_QUANTUM_SUBSTRATE.md)**
    * *Why the universe isn't weird: The Coherence Field as a substrate.*
* **[📄 Read: Alternative Formulation EM Potential](docs/Philosophy/Alternative_Formulation_EM_Potential.md)**
    * *Alternative perspectives on the electromagnetic potential.*
* **[📄 Read: The Principle of Temporal Integrity](docs/Philosophy/PRINCIPLE_TEMPORAL_INTEGRITY.md)**
    * *Safeguards against causality violations.*
</details>

<details>
<summary><h3>🛠️ Section 3: Hardware & Protocols</h3></summary>
<br>
The blueprints, grocery lists, and testing protocols required to build the device.

* **[📄 View: Grocery List ($38M Prototype)](Hardware/grocery_list_38M.txt)**
    * *Complete Bill of Materials.*
* **[📄 Read: Earth-Moon Test Protocol](Hardware/earth_moon_test_protocol.txt)**
    * *Step-by-step guide for the critical latency test.*
* **[📄 Read: Phase 1 Tabletop Protocol](Hardware/PROTOCOL_Phase1_Tabletop.md)**
    * *Instructions for the initial lab-bench prototype.*
* **[🖼️ View: System Architecture Diagram](assets/Technical_System_Architecture_EB.png)**
* **[🖼️ View: Concept Diagram](assets/ct_concept_diagram.png)**
</details>

<details>
<summary><h3>💻 Section 4: Simulations & Code</h3></summary>
<br>
Python simulations to validate the theory and test signal integrity.

* **[📄 Read: Simulation Readme](Simulations/SIMULATION_README.md)**
    * *Guide to running the simulations.*
* **[🐍 Run: Earth-Moon Enhanced Final](Simulations/earth_moon_enhanced_final.py)**
    * *The latest simulation logic for the Earth-Moon test.*
* **[🐍 Run: Potential Coherence Sim v2.1](Simulations/em_potential_coherence_simulation_v2_1.py)**
* **[📄 Read: Simulation Results Summary](Simulations/EM_Simulation_Results_Summary.md)**
</details>

<details>
<summary><h3>🚀 Section 5: Roadmap & Future</h3></summary>
<br>
Where we are going and how we get there.

* **[📄 Read: Project Roadmap](ROADMAP.md)**
* **[🖼️ View: Timeline Roadmap](assets/timeline_roadmap.png)**
* **[📄 Read: Predictions on Signal Strength](Simulations/PREDICTIONS_SIGNAL_STRENGTH.md)**
</details>

---
![Coherence-Telephone-EM-Modulation](https://github.com/user-attachments/assets/44b4cd70-7400-4eea-a90b-afc158ab9b21)


## ⚡ Quick Start

To run the primary simulation:

```bash
# Clone the repository
git clone [https://github.com/Albuslux1/Coherence-Telephone.git](https://github.com/Albuslux1/Coherence-Telephone.git)

# Navigate to the simulation folder
cd Coherence-Telephone/Simulations

# Install dependencies
pip install -r requirements.txt

# Run the Earth-Moon Test Simulation
python earth_moon_enhanced_final.py
