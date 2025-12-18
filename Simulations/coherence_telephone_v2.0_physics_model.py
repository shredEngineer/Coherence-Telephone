"""
Coherence Telephone v2.0 – Physics-First Model
Topological addressing via axion electrodynamics
December 2025 – John Bollinger (@AlbusLux1)

Key Features:
- Chern number sets axion angle θ = 2π𝒞 (topological address)
- Matching Chern = resonant coupling
- Mismatched Chern = no signal
- E·B modulation at sender drives receiver via axion term
- No separate entropy field — pure axion electrodynamics
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ============================= PARAMETERS =============================
# Topological addressing
Chern_sender = 3.0
Chern_receiver = 3.0  # Try 2.0 or 4.0 for mismatch test

theta_sender = 2 * np.pi * Chern_sender
theta_receiver = 2 * np.pi * Chern_receiver

# Address match factor (perfect = 1.0, mismatch = 0)
match_factor = np.exp(-((theta_sender - theta_receiver)/ (2*np.pi))**2 / 0.1)

# Axion coupling (α/2π factor)
alpha = 1/137
axion_coupling = (alpha / (2 * np.pi)) * match_factor

# Receiver resonance (natural frequency tied to topology)
omega_B = theta_receiver
gamma_B = 0.2  # Damping

# Message to send
message_bits = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
bit_duration = 2.0  # seconds per bit

# Time grid
t_end = len(message_bits) * bit_duration + 5
dt = 0.001
t_eval = np.linspace(0, t_end, int(t_end/dt) + 1)

# Sender E·B modulation (our control input)
def sender_EB(t):
    bit_index = int(t / bit_duration) % len(message_bits)
    return 1.0 if message_bits[bit_index] else -1.0

# ============================= DYNAMICS =============================
def dynamics(t, y):
    """Receiver coherence observable driven by sender's E·B via axion coupling"""
    Phi_B = y[0]
    
    # Sender's applied E·B (our input signal)
    EB_applied = sender_EB(t)
    
    # Axion drive term
    drive = axion_coupling * EB_applied
    
    # Driven damped oscillator for receiver
    dPhiB_dt = -gamma_B * Phi_B + drive - omega_B**2 * Phi_B
    
    return [dPhiB_dt]

# Initial state
y0 = [0.0]

print("Running Coherence Telephone v2.0 – Physics-First Model")
print(f"Sender Chern: {Chern_sender} | Receiver Chern: {Chern_receiver}")
print(f"Address match factor: {match_factor:.4f}")
print(f"Effective axion coupling: {axion_coupling:.6f}")

# Solve
sol = solve_ivp(dynamics, (0, t_end), y0, t_eval=t_eval, method='RK45')

t = sol.t
Phi_B = sol.y[0]
EB_applied = np.array([sender_EB(ti) for ti in t])

# ============================= DECODING =============================
decoded_bits = []
for i in range(len(message_bits)):
    start = int(i * bit_duration / dt)
    end = int((i + 1) * bit_duration / dt)
    segment = Phi_B[start:end]
    avg = np.mean(segment)
    decoded_bits.append(1 if avg > 0 else 0)

ber = sum(a != b for a, b in zip(message_bits, decoded_bits)) / len(message_bits)

# First significant response
baseline = np.mean(Phi_B[:500])
deviation = np.abs(Phi_B - baseline)
first_detection_idx = np.argmax(deviation > 0.2)
detection_time = t[first_detection_idx] if first_detection_idx > 0 else t_end

# ============================= RESULTS =============================
print("\n" + "="*70)
print("RESULTS")
print("="*70)
print(f"First detectable response: {detection_time:.4f} seconds")
print(f"Bit Error Rate: {ber:.1%}")
print(f"Message sent:     {message_bits}")
print(f"Message decoded:  {decoded_bits}")

match_status = "MATCHED" if Chern_sender == Chern_receiver else "MISMATCHED"
if match_status == "MATCHED" and ber == 0 and detection_time < 1.0:
    print("\nINSTANT COHERENCE COMMUNICATION CONFIRMED")
    print("  Topological addressing works.")
else:
    print("\nNo usable signal — check address match or coupling strength.")

# ============================= PLOT =============================
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), facecolor='black')
fig.suptitle(f'Coherence Telephone v2.0 – Physics-First Model\n'
             f'Topology: {match_status} | Detection: {detection_time:.3f}s | BER: {ber:.1%}',
             color='white', fontsize=16)

ax1.plot(t, EB_applied, 'cyan', lw=2)
ax1.set_ylabel('Sender E·B', color='white')
ax1.grid(alpha=0.3)

ax2.plot(t, Phi_B, 'lime', lw=2)
ax2.axhline(0, color='gray', ls='--', alpha=0.5)
ax2.axvline(detection_time, color='yellow', ls='--', label=f'Detection {detection_time:.3f}s')
ax2.set_ylabel('Receiver Coherence Φ', color='white')
ax2.set_xlabel('Time (seconds)', color='white')
ax2.legend()
ax2.grid(alpha=0.3)

for a in [ax1, ax2]:
    a.set_facecolor('black')
    for spine in a.spines.values():
        spine.set_color('white')
    a.tick_params(colors='white')

plt.tight_layout()
plt.savefig('Visuals/coherence_telephone_v2.0_result.png', dpi=300, facecolor='black')
plt.show()
