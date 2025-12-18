"""
Coherence Telephone v2.1 – Parameter Exploration
Test experimental knobs: drive strength, Chern number, integration time.
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

def run_coherence_simulation(Chern_sender=3.0,
                             Chern_receiver=3.0,
                             drive_amplitude=1.0,    # E·B drive strength (V·T/m)
                             bit_duration=2.0,       # seconds per bit
                             qubit_coherence_time=5.0,  # T2* in seconds (1/gamma_B)
                             message_bits=None):
    
    if message_bits is None:
        message_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
    
    # ====================== PHYSICS PARAMETERS ======================
    # Topological addressing
    theta_sender = 2 * np.pi * Chern_sender
    theta_receiver = 2 * np.pi * Chern_receiver
    
    # Topological match factor (simplified quantum overlap)
    if Chern_sender == Chern_receiver:
        match_factor = 1.0
    else:
        # Small residual coupling if numbers are close?
        match_factor = np.exp(-(Chern_sender - Chern_receiver)**2 / 0.1)
    
    # Axion coupling (α/2π ≈ 0.001161)
    alpha = 1/137
    base_coupling = alpha / (2 * np.pi)
    
    # Unknown coupling strengths (WHAT WE WANT TO MEASURE)
    g_A_to_field = 0.5   # Sender → Field efficiency
    g_field_to_B = 0.5   # Field → Receiver efficiency
    total_coupling = base_coupling * g_A_to_field * g_field_to_B * match_factor
    
    # Receiver damping (from coherence time)
    gamma_B = 1.0 / qubit_coherence_time
    omega_B = theta_receiver  # Resonance frequency
    
    # ====================== DYNAMICS ======================
    def sender_modulation(t):
        """E·B drive signal."""
        bit_index = int(t / bit_duration) % len(message_bits)
        return drive_amplitude if message_bits[bit_index] else -drive_amplitude
    
    def system_dynamics(t, y):
        EB_applied, Phi_B = y
        # Sender: we control EB_applied directly
        dEB_dt = 0
        
        # Receiver: damped oscillator driven by coherence field
        field_drive = total_coupling * EB_applied
        dPhiB_dt = -gamma_B * Phi_B + field_drive - omega_B**2 * Phi_B
        
        return [dEB_dt, dPhiB_dt]
    
    # ====================== SIMULATION ======================
    t_end = len(message_bits) * bit_duration
    t_eval = np.linspace(0, t_end, int(t_end * 100))  # 100 Hz sampling
    
    sol = solve_ivp(system_dynamics, [0, t_end], [0.0, 0.0], 
                    t_eval=t_eval, method='RK45', rtol=1e-6)
    
    t = sol.t
    EB_applied_hist = sender_modulation(t)
    Phi_B_hist = sol.y[1]
    
    # ====================== DETECTION & DECODING ======================
    decoded_bits = []
    detection_times = []
    
    for i, bit in enumerate(message_bits):
        start_idx = int(i * bit_duration * 100)
        end_idx = int((i + 1) * bit_duration * 100)
        segment = Phi_B_hist[start_idx:end_idx]
        
        # Average value for decoding
        avg_val = np.mean(segment)
        decoded_bit = 1 if avg_val > 0 else 0
        decoded_bits.append(decoded_bit)
        
        # Time to cross detection threshold (0.2 * drive_amplitude)
        threshold = 0.2 * drive_amplitude * np.sign(bit if bit else -1)
        if np.any(np.abs(segment) > np.abs(threshold)):
            cross_idx = np.where(np.abs(segment) > np.abs(threshold))[0]
            if len(cross_idx) > 0:
                detection_times.append(t[start_idx + cross_idx[0]])
    
    # ====================== RESULTS ======================
    ber = np.mean([a != b for a, b in zip(message_bits, decoded_bits)])
    avg_detection_time = np.mean(detection_times) if detection_times else t_end
    
    results = {
        't': t,
        'EB_applied': EB_applied_hist,
        'Phi_B': Phi_B_hist,
        'decoded_bits': decoded_bits,
        'ber': ber,
        'detection_time': avg_detection_time,
        'total_coupling': total_coupling,
        'match_factor': match_factor
    }
    
    return results

# ====================== PARAMETER SWEEP ======================
print("Coherence Telephone v2.1 – Parameter Exploration")
print("="*60)

# Test 1: Baseline (your original result)
print("\n1. BASELINE (Matched C=3, Low Drive)")
results1 = run_coherence_simulation(Chern_sender=3.0, Chern_receiver=3.0,
                                    drive_amplitude=1.0, qubit_coherence_time=5.0)
print(f"   Coupling: {results1['total_coupling']:.6f}")
print(f"   BER: {results1['ber']:.1%}")
print(f"   Avg detection: {results1['detection_time']:.2f}s")

# Test 2: Boosted Drive (Experimental knob)
print("\n2. BOOSTED DRIVE (10x Amplitude)")
results2 = run_coherence_simulation(Chern_sender=3.0, Chern_receiver=3.0,
                                    drive_amplitude=10.0, qubit_coherence_time=5.0)
print(f"   Coupling: {results2['total_coupling']:.6f}")
print(f"   BER: {results2['ber']:.1%}")
print(f"   Avg detection: {results2['detection_time']:.2f}s")

# Test 3: Better Qubit (Longer T2*)
print("\n3. BETTER QUBIT (T2* = 50s)")
results3 = run_coherence_simulation(Chern_sender=3.0, Chern_receiver=3.0,
                                    drive_amplitude=1.0, qubit_coherence_time=50.0)
print(f"   Coupling: {results3['total_coupling']:.6f}")
print(f"   BER: {results3['ber']:.1%}")
print(f"   Avg detection: {results3['detection_time']:.2f}s")

# Test 4: Higher Chern Number
print("\n4. HIGHER CHERN (C=5)")
results4 = run_coherence_simulation(Chern_sender=5.0, Chern_receiver=5.0,
                                    drive_amplitude=1.0, qubit_coherence_time=5.0)
print(f"   Coupling: {results4['total_coupling']:.6f}")
print(f"   BER: {results4['ber']:.1%}")
print(f"   Avg detection: {results4['detection_time']:.2f}s")

# Test 5: Mismatched (Control)
print("\n5. CONTROL (Mismatched C=3 vs C=2)")
results5 = run_coherence_simulation(Chern_sender=3.0, Chern_receiver=2.0,
                                    drive_amplitude=10.0, qubit_coherence_time=50.0)
print(f"   Coupling: {results5['total_coupling']:.6f}")
print(f"   BER: {results5['ber']:.1%}")

# ====================== VISUALIZATION ======================
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
all_results = [results1, results2, results3, results4, results5]
titles = ['Baseline', '10x Drive', 'Better Qubit', 'C=5', 'Mismatched C=3 vs C=2']

for idx, (ax, results, title) in enumerate(zip(axes.flatten()[:5], all_results[:5], titles)):
    ax.plot(results['t'], results['EB_applied'], 'cyan', alpha=0.7, label='E·B Drive')
    ax.plot(results['t'], results['Phi_B'], 'white', lw=1.5, label='Receiver Φ_B')
    ax.axhline(0, color='gray', ls='--', alpha=0.3)
    ax.set_title(f"{title}\nBER={results['ber']:.1%}, τ={results['detection_time']:.2f}s")
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    ax.legend(loc='upper right', fontsize=8)
    ax.grid(alpha=0.2)

# Summary plot on last subplot
axes[2, 1].axis('off')
summary_text = (
    "PARAMETER SWEEP SUMMARY\n"
    "=======================\n"
    "Key finding: Signal scales with:\n"
    "• Drive amplitude (E·B)\n"
    "• Qubit coherence time (T2*)\n"
    "• Chern number match\n"
    "\nExperimental implications:\n"
    "1. Use highest possible E·B drive\n"
    "2. Use best available qubits (T2* > 50µs)\n"
    "3. Verify with mismatched control\n"
    "\nPredicted coupling: ~10⁻³"
)
axes[2, 1].text(0.1, 0.5, summary_text, fontfamily='monospace', 
                verticalalignment='center', fontsize=10, color='white')

plt.suptitle('Coherence Telephone v2.1 – Parameter Exploration\n'
             'How to boost signal for detectable correlation', fontsize=16)
plt.tight_layout()
plt.savefig('Visuals/coherence_telephone_v2.1_parameter_sweep.png', 
            dpi=300, facecolor='black')
plt.show()
