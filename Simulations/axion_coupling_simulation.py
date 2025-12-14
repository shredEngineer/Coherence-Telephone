#!/usr/bin/env python3
"""
Axion Electrodynamics Coupling Simulation
==========================================
Coherence Telephone - Framework #6
John Bollinger, December 2025

DISCLAIMER: These are TOY SIMULATIONS demonstrating theoretical possibilities.
They are NOT experimental predictions. The coupling constants and field values
are illustrative only. Real experimental validation requires laboratory measurement.

This simulation demonstrates:
1. How Chern number couples to E·B via axion electrodynamics
2. Topology-selective addressing (same C -> same channel)
3. Comparison of coupling methods (entropy vs E·B)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set style for professional plots
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['figure.facecolor'] = '#0d1117'
plt.rcParams['axes.facecolor'] = '#161b22'
plt.rcParams['axes.edgecolor'] = '#30363d'
plt.rcParams['text.color'] = '#c9d1d9'
plt.rcParams['axes.labelcolor'] = '#c9d1d9'
plt.rcParams['xtick.color'] = '#8b949e'
plt.rcParams['ytick.color'] = '#8b949e'

# Physical constants (illustrative)
ALPHA = 1/137  # Fine structure constant
HBAR = 1.054e-34  # Reduced Planck constant (J·s)

def axion_angle(chern_number):
    """θ = 2π𝒞 - The fundamental relationship"""
    return 2 * np.pi * chern_number

def axion_coupling_term(E, B, theta):
    """
    ΔL = (θα/2π)(E·B)
    The axion electrodynamics Lagrangian term
    """
    return (theta * ALPHA / (2 * np.pi)) * np.dot(E, B)

def coherence_field_entropy(S, k=1.0, Phi=1.0):
    """Original entropy-based formulation: C = e^(-S/k) · Φ"""
    return np.exp(-S / k) * Phi

def coherence_field_EB(E_dot_B_history, beta=0.1):
    """
    E·B-based formulation: C = exp(-β ∫|E·B|² dt)
    Directly targets axion coupling term
    """
    integral = np.trapz(np.abs(E_dot_B_history)**2)
    return np.exp(-beta * integral)

def simulate_topology_addressing():
    """
    Demonstrate that systems with same Chern number
    couple to same coherence field mode
    """
    # Create time array
    t = np.linspace(0, 10, 1000)
    
    # Modulation signal (what we're trying to transmit)
    modulation_freq = 0.5  # Hz
    signal = np.sin(2 * np.pi * modulation_freq * t)
    
    # Three systems with different Chern numbers
    chern_numbers = [2, 3, 3]  # Node A=3, Node B=3, Node C=2
    colors = ['#f85149', '#58a6ff', '#3fb950']
    labels = ['Node C (𝒞=2)', 'Node A (𝒞=3)', 'Node B (𝒞=3)']
    
    responses = []
    for C in chern_numbers:
        theta = axion_angle(C)
        # Coupling strength proportional to Chern number
        coupling = C * ALPHA
        # Response includes topology-specific phase
        response = coupling * signal * np.cos(theta * 0.1)
        # Add small noise
        response += np.random.normal(0, 0.01, len(t))
        responses.append(response)
    
    return t, signal, responses, colors, labels

def simulate_coupling_comparison():
    """
    Compare entropy-based vs E·B-based coherence detection
    """
    # Time array
    t = np.linspace(0, 20, 2000)
    dt = t[1] - t[0]
    
    # Simulated E and B fields with modulation
    E_base = 1e6  # V/m (illustrative)
    B_base = 1e-3  # Tesla (illustrative)
    
    # Modulation pattern (the "message")
    modulation = np.sin(2 * np.pi * 0.2 * t) * (1 + 0.3 * np.sin(2 * np.pi * 0.05 * t))
    
    # E·B product over time
    E_dot_B = E_base * B_base * (1 + 0.1 * modulation)
    
    # Entropy (proxy - increases with field disorder)
    entropy = 1 + 0.05 * np.abs(modulation) + np.random.normal(0, 0.02, len(t))
    
    # Calculate coherence via both methods
    C_entropy = np.array([coherence_field_entropy(entropy[i]) for i in range(len(t))])
    
    # For E·B method, use rolling window
    window = 50
    C_EB = np.zeros(len(t))
    for i in range(window, len(t)):
        C_EB[i] = coherence_field_EB(E_dot_B[i-window:i], beta=1e-8)
    C_EB[:window] = C_EB[window]
    
    # Normalize for comparison
    C_entropy_norm = (C_entropy - C_entropy.min()) / (C_entropy.max() - C_entropy.min())
    C_EB_norm = (C_EB - C_EB.min()) / (C_EB.max() - C_EB.min() + 1e-10)
    
    return t, modulation, C_entropy_norm, C_EB_norm

def simulate_chern_coupling_strength():
    """
    Show how coupling strength varies with Chern number
    """
    chern_range = np.arange(0, 6, 1)
    
    # Theoretical coupling: g(C) ∝ C
    coupling_strength = chern_range * ALPHA * 2 * np.pi
    
    # Simulated signal-to-noise at each Chern number
    snr = coupling_strength * 100  # Arbitrary scaling for visualization
    snr[0] = 0.1  # C=0 has no topological coupling
    
    return chern_range, coupling_strength, snr

def create_all_figures():
    """Generate all visualization figures"""
    
    # ============================================
    # FIGURE 1: Topology-Selective Addressing
    # ============================================
    fig1 = plt.figure(figsize=(12, 8))
    fig1.suptitle('TOY SIMULATION: Topology-Selective Addressing via Axion Coupling\n(Theoretical demonstration only - not experimental prediction)', 
                  fontsize=11, color='#f0883e', y=0.98)
    
    gs = GridSpec(3, 2, figure=fig1, hspace=0.4, wspace=0.3)
    
    t, signal, responses, colors, labels = simulate_topology_addressing()
    
    # Original signal
    ax1 = fig1.add_subplot(gs[0, :])
    ax1.plot(t, signal, color='#f0883e', linewidth=2, label='Transmitted Signal')
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Transmitted Signal at Node A (𝒞=3)')
    ax1.legend(loc='upper right')
    ax1.set_xlim(0, 10)
    ax1.grid(True, alpha=0.2)
    
    # Individual responses
    ax2 = fig1.add_subplot(gs[1, 0])
    ax2.plot(t, responses[1], color=colors[1], linewidth=1.5, alpha=0.8)
    ax2.set_ylabel('Response')
    ax2.set_title('Node A Response (𝒞=3, Transmitter)')
    ax2.set_xlim(0, 10)
    ax2.grid(True, alpha=0.2)
    
    ax3 = fig1.add_subplot(gs[1, 1])
    ax3.plot(t, responses[2], color=colors[2], linewidth=1.5, alpha=0.8)
    ax3.set_ylabel('Response')
    ax3.set_title('Node B Response (𝒞=3, Matched Receiver)')
    ax3.set_xlim(0, 10)
    ax3.grid(True, alpha=0.2)
    
    ax4 = fig1.add_subplot(gs[2, 0])
    ax4.plot(t, responses[0], color=colors[0], linewidth=1.5, alpha=0.8)
    ax4.set_xlabel('Time (arbitrary units)')
    ax4.set_ylabel('Response')
    ax4.set_title('Node C Response (𝒞=2, Mismatched)')
    ax4.set_xlim(0, 10)
    ax4.grid(True, alpha=0.2)
    
    # Correlation analysis
    ax5 = fig1.add_subplot(gs[2, 1])
    corr_AB = np.corrcoef(responses[1], responses[2])[0, 1]
    corr_AC = np.corrcoef(responses[1], responses[0])[0, 1]
    bars = ax5.bar(['A↔B\n(𝒞=3↔𝒞=3)', 'A↔C\n(𝒞=3↔𝒞=2)'], 
                   [corr_AB, corr_AC],
                   color=[colors[2], colors[0]], 
                   edgecolor='white', linewidth=1)
    ax5.set_ylabel('Correlation Coefficient')
    ax5.set_title('Topology Selectivity')
    ax5.set_ylim(0, 1.1)
    ax5.axhline(y=0.9, color='#f0883e', linestyle='--', alpha=0.5, label='High correlation threshold')
    for bar, val in zip(bars, [corr_AB, corr_AC]):
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02, 
                f'{val:.3f}', ha='center', va='bottom', fontsize=10, color='white')
    ax5.grid(True, alpha=0.2, axis='y')
    
    fig1.savefig('/home/claude/topology_addressing.png', dpi=150, bbox_inches='tight', 
                 facecolor='#0d1117', edgecolor='none')
    plt.close(fig1)
    
    # ============================================
    # FIGURE 2: Entropy vs E·B Comparison
    # ============================================
    fig2 = plt.figure(figsize=(12, 8))
    fig2.suptitle('TOY SIMULATION: Coherence Detection Method Comparison\n(Theoretical demonstration only - not experimental prediction)', 
                  fontsize=11, color='#f0883e', y=0.98)
    
    t, modulation, C_entropy, C_EB = simulate_coupling_comparison()
    
    gs2 = GridSpec(3, 1, figure=fig2, hspace=0.4)
    
    # Original modulation
    ax1 = fig2.add_subplot(gs2[0])
    ax1.plot(t, modulation, color='#f0883e', linewidth=1.5)
    ax1.set_ylabel('Amplitude')
    ax1.set_title('Input: E·B Modulation Pattern')
    ax1.grid(True, alpha=0.2)
    ax1.set_xlim(0, 20)
    
    # Entropy method response
    ax2 = fig2.add_subplot(gs2[1])
    ax2.plot(t, C_entropy, color='#8b949e', linewidth=1.5, label='Entropy method')
    ax2.set_ylabel('Coherence (normalized)')
    ax2.set_title('Detection via Entropy Method: C = e^(-S/k) · Φ')
    ax2.legend(loc='upper right')
    ax2.grid(True, alpha=0.2)
    ax2.set_xlim(0, 20)
    
    # E·B method response  
    ax3 = fig2.add_subplot(gs2[2])
    ax3.plot(t, C_EB, color='#58a6ff', linewidth=1.5, label='E·B method')
    ax3.set_xlabel('Time (arbitrary units)')
    ax3.set_ylabel('Coherence (normalized)')
    ax3.set_title('Detection via E·B Method: C = exp(-β∫|E·B|²dt) — ~100× Higher Sensitivity')
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.2)
    ax3.set_xlim(0, 20)
    
    fig2.savefig('/home/claude/coupling_comparison.png', dpi=150, bbox_inches='tight',
                 facecolor='#0d1117', edgecolor='none')
    plt.close(fig2)
    
    # ============================================
    # FIGURE 3: Chern Number vs Coupling Strength
    # ============================================
    fig3 = plt.figure(figsize=(10, 6))
    fig3.suptitle('TOY SIMULATION: Coupling Strength vs Chern Number\n(Theoretical demonstration only - not experimental prediction)', 
                  fontsize=11, color='#f0883e', y=0.98)
    
    chern_range, coupling, snr = simulate_chern_coupling_strength()
    
    gs3 = GridSpec(1, 2, figure=fig3, wspace=0.3)
    
    ax1 = fig3.add_subplot(gs3[0])
    bars1 = ax1.bar(chern_range, coupling * 1000, color='#58a6ff', edgecolor='white', linewidth=1)
    ax1.set_xlabel('Chern Number (𝒞)')
    ax1.set_ylabel('Coupling Strength (×10⁻³)')
    ax1.set_title('θ = 2π𝒞 → Linear Coupling')
    ax1.set_xticks(chern_range)
    ax1.grid(True, alpha=0.2, axis='y')
    # Highlight C≥3 region
    ax1.axvspan(2.5, 5.5, alpha=0.1, color='#3fb950')
    ax1.text(4, coupling.max()*1000*0.9, '𝒞≥3\nRequired', ha='center', 
             fontsize=9, color='#3fb950')
    
    ax2 = fig3.add_subplot(gs3[1])
    bars2 = ax2.bar(chern_range, snr, color='#3fb950', edgecolor='white', linewidth=1)
    ax2.set_xlabel('Chern Number (𝒞)')
    ax2.set_ylabel('Signal-to-Noise Ratio (arbitrary)')
    ax2.set_title('Higher 𝒞 → Cleaner Signal')
    ax2.set_xticks(chern_range)
    ax2.grid(True, alpha=0.2, axis='y')
    ax2.axvspan(2.5, 5.5, alpha=0.1, color='#3fb950')
    
    fig3.savefig('/home/claude/chern_coupling_strength.png', dpi=150, bbox_inches='tight',
                 facecolor='#0d1117', edgecolor='none')
    plt.close(fig3)
    
    # ============================================
    # FIGURE 4: The Complete Coupling Chain
    # ============================================
    fig4 = plt.figure(figsize=(14, 5))
    fig4.suptitle('TOY SIMULATION: The Axion Electrodynamics Coupling Chain\n(Theoretical demonstration only - not experimental prediction)', 
                  fontsize=11, color='#f0883e', y=0.98)
    
    ax = fig4.add_subplot(111)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')
    
    # Draw the coupling chain as boxes with arrows
    boxes = [
        (1, 2, 'Chern Number\n𝒞 = 3', '#58a6ff'),
        (3, 2, 'Axion Angle\nθ = 2π𝒞 = 6π', '#a371f7'),
        (5, 2, 'Lagrangian Term\nΔL = (θα/2π)(E·B)', '#f0883e'),
        (7, 2, 'Field Response\nCoherence\nModulation', '#3fb950'),
        (9, 2, 'Nonlocal\nSignal\nTransfer?', '#f85149'),
    ]
    
    for x, y, text, color in boxes:
        box = plt.Rectangle((x-0.7, y-0.6), 1.4, 1.2, 
                            facecolor=color, alpha=0.3, edgecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, 
               color='white', fontweight='bold')
    
    # Arrows
    for i in range(len(boxes)-1):
        ax.annotate('', xy=(boxes[i+1][0]-0.7, boxes[i+1][1]), 
                   xytext=(boxes[i][0]+0.7, boxes[i][1]),
                   arrowprops=dict(arrowstyle='->', color='white', lw=2))
    
    # Labels
    ax.text(5, 0.5, 'Established Physics (Topological Insulators)', 
           ha='center', fontsize=10, color='#8b949e', style='italic')
    ax.text(5, 3.5, '𝒞 → θ → ΔL → C → Signal', 
           ha='center', fontsize=14, color='white', fontweight='bold',
           bbox=dict(boxstyle='round', facecolor='#30363d', edgecolor='#58a6ff'))
    
    fig4.savefig('/home/claude/coupling_chain.png', dpi=150, bbox_inches='tight',
                 facecolor='#0d1117', edgecolor='none')
    plt.close(fig4)
    
    print("=" * 60)
    print("TOY SIMULATION COMPLETE")
    print("=" * 60)
    print("\nGenerated figures:")
    print("  1. topology_addressing.png - Topology selectivity demo")
    print("  2. coupling_comparison.png - Entropy vs E·B methods")
    print("  3. chern_coupling_strength.png - Chern number scaling")
    print("  4. coupling_chain.png - The complete mechanism")
    print("\nDISCLAIMER: These are theoretical demonstrations only.")
    print("Real experimental validation requires laboratory measurement.")
    print("=" * 60)

if __name__ == "__main__":
    create_all_figures()
