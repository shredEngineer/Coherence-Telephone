Coherence Telephone – Earth–Moon FTL Test Protocol
Version 1.0 – December 2025
Author: John Bollinger (@AlbusLux1)

Objective
Determine whether topologically protected coherence coupling can transmit information faster than the speed of light.

Success criterion: Signal arrives in <1.28 seconds over 384,000 km Earth–Moon distance.
Failure criterion: Signal arrives at ≥1.28 seconds ± measurement error.

Hardware (minimum viable)
• 2 × Quantinuum H2-1 logical qubit systems (Chern ≥ 3 demonstrated)
• 1 × 10 cm sapphire whispering-gallery resonator (Q > 10¹¹)
• 1 × 10.6 THz quantum cascade laser pump
• 1 × 16-channel SNSPD array
• 2 × Bluefors LD400 dilution refrigerators
• Timing synchronization: GPS-disciplined rubidium clocks + optical fiber link
• Total estimated cost: $150 million (including lunar relay/orbiter)

Test Configuration
1. Earth Station (ground, e.g., Mauna Kea or Atacama)
   - Logical qubit A in fridge
   - Coherence injection cavity
   - Entropy modulator (piezo + THz pump)
   - GPS time reference

2. Moon Station (lunar orbiter or Chinese lunar relay satellite)
   - Logical qubit B in fridge
   - Identical coherence cavity
   - SNSPD receiver array
   - Same GPS time reference

Procedure
1. Generate Bell pair between Earth and Moon qubits (standard entanglement distribution)
2. Inject one photon from each pair into its local coherence cavity
3. Earth station modulates cavity entropy at 0.1 Hz (clear sine wave, 10-second period)
   - Bit 1: increase S by ΔS = 0.5
   - Bit 0: decrease S by ΔS = 0.5
4. Moon station continuously measures ⟨σ_x⟩ on its qubit
5. Record arrival time of first detectable coherence wiggle
6. Repeat 10,000 cycles for statistics

Data Analysis
• Calculate time-of-flight from first measurable deviation in ⟨σ_x⟩
• Statistical significance: SNR > 10 required
• Measurement resolution: <50 ps (achievable with current SNSPDs)

Expected Results
If coherence field is real and nonlocal:
   → Signal arrival time: <100 μs (limited only by electronics)
   → Theory confirmed

If coherence field is local or nonexistent:
   → Signal arrival time: 1.28 seconds ± light-travel variation
   → Theory falsified

Safety & Ethics
• No risk to lunar environment
• No weaponization potential (pure communication test)
• Full data public release regardless of outcome

This is the one test that ends the argument forever.
One afternoon. One number.

The universe answers, or it doesn’t.

Your move.

— John Bollinger
December 2025
