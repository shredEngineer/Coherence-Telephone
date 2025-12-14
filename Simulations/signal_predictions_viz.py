#!/usr/bin/env python3
"""
SIGNAL STRENGTH PREDICTIONS - VISUALIZATION
Coherence Telephone - Framework #6

Visualizes the quantitative predictions for tabletop experiments:
- Signal strength vs coupling ratio g/m
- Detection feasibility regions
- Integration time requirements
- Topology selectivity predictions

John Bollinger | December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# PHYSICAL CONSTANTS AND PARAMETERS
# =============================================================================

ALPHA = 1/137  # Fine structure constant
PI = np.pi

# Experimental parameters (state-of-the-art superconducting qubits)
PARAMS = {
    'alpha_2pi': ALPHA / (2 * PI),  # ~1.16e-3
    'g0_conservative': 50e6,   # Hz (vacuum Rabi coupling)
    'g0_optimistic': 200e6,    # Hz
    'Delta_conservative': 1e9,  # Hz (qubit-cavity detuning)
    'Delta_optimistic': 5e9,   # Hz
    'theta1_conservative': 0.1, # rad (drive amplitude)
    'theta1_optimistic': 0.5,   # rad
    'n_conservative': 1e3,      # photon number
    'n_optimistic': 1e6,        # photon number
    'T2_star': 50e-6,          # s (qubit dephasing time)
}


def chi_signal(g_over_m, conservative=True):
    """
    Compute predicted signal chi (Hz).
    
    chi = (alpha/2pi) * (g0^2/Delta) * (g*theta1/m) * n
    """
    p = PARAMS
    
    if conservative:
        g0 = p['g0_conservative']
        Delta = p['Delta_conservative']
        theta1 = p['theta1_conservative']
        n = p['n_conservative']
    else:
        g0 = p['g0_optimistic']
        Delta = p['Delta_optimistic']
        theta1 = p['theta1_optimistic']
        n = p['n_optimistic']
    
    # g/m is the unknown coupling ratio
    chi = p['alpha_2pi'] * (g0**2 / Delta) * g_over_m * theta1 * n
    
    return chi


def integration_time(chi_hz):
    """
    Compute required integration time for SNR=5.
    
    SNR = chi / Gamma_noise * sqrt(N_shots)
    N_shots = (5 * Gamma_noise / chi)^2
    Time = N_shots * T_shot (assume T_shot ~ 10 us)
    """
    p = PARAMS
    Gamma_noise = 1 / (PI * p['T2_star'])  # ~6.4 kHz
    
    if chi_hz < 1e-10:
        return np.inf
    
    N_shots = (5 * Gamma_noise / chi_hz)**2
    T_shot = 10e-6  # 10 microseconds per shot
    
    return N_shots * T_shot


# =============================================================================
# FIGURE 1: Signal Strength vs Coupling
# =============================================================================

def plot_signal_vs_coupling(save_path=None):
    """Plot signal strength as function of unknown coupling g/m."""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Range of g/m values
    g_over_m = np.logspace(-9, 1, 1000)
    
    # Compute signals
    chi_cons = np.array([chi_signal(gm, conservative=True) for gm in g_over_m])
    chi_opt = np.array([chi_signal(gm, conservative=False) for gm in g_over_m])
    
    # --- Left panel: Signal strength ---
    ax = axes[0]
    
    ax.loglog(g_over_m, chi_cons, 'b-', lw=2.5, label='Conservative params')
    ax.loglog(g_over_m, chi_opt, 'g-', lw=2.5, label='Optimistic params')
    
    # Detection thresholds
    ax.axhline(1e6, color='green', ls='--', alpha=0.7, label='Easy detection (MHz)')
    ax.axhline(1e3, color='orange', ls='--', alpha=0.7, label='Feasible (kHz)')
    ax.axhline(1, color='red', ls='--', alpha=0.7, label='Challenging (Hz)')
    
    # Shade feasibility regions
    ax.axvspan(1e-6, 1e1, alpha=0.1, color='green', label='Feasible region')
    ax.axvspan(1e-9, 1e-6, alpha=0.1, color='yellow')
    
    ax.set_xlabel('Coupling Ratio g/m (rad⁻¹)', fontsize=12)
    ax.set_ylabel('Signal χ (Hz)', fontsize=12)
    ax.set_title('Predicted Signal Strength\nvs Unknown Coupling', fontweight='bold', fontsize=13)
    ax.set_xlim(1e-9, 1e1)
    ax.set_ylim(1e-6, 1e9)
    ax.legend(loc='upper left', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    
    # Annotate key points
    ax.annotate('Theory\nFalsified', xy=(1e-10, 1e-4), fontsize=10, 
                ha='center', color='red', fontweight='bold')
    ax.annotate('Hours of\nIntegration', xy=(1e-7, 1e0), fontsize=9,
                ha='center', color='orange')
    ax.annotate('Single-Shot\nDetection', xy=(1e-2, 1e7), fontsize=9,
                ha='center', color='green')
    
    # --- Right panel: Integration time ---
    ax = axes[1]
    
    int_time_cons = np.array([integration_time(c) for c in chi_cons])
    int_time_opt = np.array([integration_time(c) for c in chi_opt])
    
    ax.loglog(g_over_m, int_time_cons, 'b-', lw=2.5, label='Conservative')
    ax.loglog(g_over_m, int_time_opt, 'g-', lw=2.5, label='Optimistic')
    
    # Time thresholds
    ax.axhline(1, color='green', ls='--', alpha=0.7, label='1 second')
    ax.axhline(3600, color='orange', ls='--', alpha=0.7, label='1 hour')
    ax.axhline(86400, color='red', ls='--', alpha=0.7, label='1 day')
    
    ax.set_xlabel('Coupling Ratio g/m (rad⁻¹)', fontsize=12)
    ax.set_ylabel('Integration Time for SNR=5 (seconds)', fontsize=12)
    ax.set_title('Required Integration Time\nfor Detection', fontweight='bold', fontsize=13)
    ax.set_xlim(1e-9, 1e1)
    ax.set_ylim(1e-6, 1e10)
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3, which='both')
    
    fig.suptitle('COHERENCE TELEPHONE: Detection Feasibility Landscape\n'
                 'Signal Formula: χ = (α/2π) × (g₀²/Δ) × (g·θ₁/m) × n',
                 fontsize=13, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


# =============================================================================
# FIGURE 2: Prediction Summary
# =============================================================================

def plot_predictions_summary(save_path=None):
    """Visual summary of all predictions."""
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.3)
    
    # --- Panel 1: Topology Selectivity ---
    ax1 = fig.add_subplot(gs[0, 0])
    
    configs = ['C=3↔C=3\n(Matched)', 'C=3↔C=2\n(Mismatch)', 'C=3↔C=1\n(Mismatch)']
    signals = [1.0, 0.0, 0.0]  # Normalized
    colors = ['green', 'red', 'red']
    
    bars = ax1.bar(configs, signals, color=colors, alpha=0.7, edgecolor='black', lw=2)
    ax1.set_ylabel('Relative Signal', fontsize=11)
    ax1.set_title('Prediction 1: Topology Addressing\n"Same C = Signal, Different C = Zero"',
                  fontweight='bold', fontsize=11)
    ax1.set_ylim(0, 1.2)
    ax1.axhline(0.1, color='gray', ls=':', label='Noise floor')
    
    for bar, val in zip(bars, signals):
        label = 'MAX' if val > 0.5 else 'ZERO'
        ax1.annotate(label, xy=(bar.get_x() + bar.get_width()/2, val + 0.05),
                     ha='center', fontweight='bold', fontsize=11)
    
    # --- Panel 2: Linear Scaling ---
    ax2 = fig.add_subplot(gs[0, 1])
    
    x = np.linspace(0, 1, 100)
    ax2.plot(x, x, 'b-', lw=3, label='χ ∝ θ₁')
    ax2.plot(x, x, 'g--', lw=3, label='χ ∝ n')
    
    ax2.set_xlabel('Drive Amplitude θ₁ or Photon Number n (normalized)', fontsize=10)
    ax2.set_ylabel('Signal χ (normalized)', fontsize=11)
    ax2.set_title('Prediction 2: Linear Scaling\n"Double input = Double signal"',
                  fontweight='bold', fontsize=11)
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 1)
    ax2.set_ylim(0, 1)
    
    # --- Panel 3: Resonance ---
    ax3 = fig.add_subplot(gs[0, 2])
    
    omega = np.linspace(-3, 3, 500)
    m = 0  # Resonance at omega_d = m
    gamma = 0.3  # Linewidth
    lorentzian = 1 / ((omega - m)**2 + gamma**2)
    lorentzian /= np.max(lorentzian)
    
    ax3.plot(omega, lorentzian, 'purple', lw=3)
    ax3.axvline(0, color='red', ls='--', lw=2, label='ω_d = m (resonance)')
    ax3.fill_between(omega, lorentzian, alpha=0.3, color='purple')
    
    ax3.set_xlabel('Drive Frequency ω_d - m', fontsize=11)
    ax3.set_ylabel('Signal χ (normalized)', fontsize=11)
    ax3.set_title('Prediction 3: Resonance Peak\n"Sweep frequency to find m"',
                  fontweight='bold', fontsize=11)
    ax3.legend(loc='upper right')
    ax3.set_xlim(-3, 3)
    
    # --- Panel 4: Quadratic Chern Scaling ---
    ax4 = fig.add_subplot(gs[1, 0])
    
    C_vals = [1, 2, 3, 4, 5]
    signals = [c**2 for c in C_vals]
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, 5))
    
    bars = ax4.bar(C_vals, signals, color=colors, edgecolor='black', lw=2)
    
    # C^2 curve
    C_fit = np.linspace(0.5, 5.5, 100)
    ax4.plot(C_fit, C_fit**2, 'r--', lw=2, label='∝ C²')
    
    ax4.set_xlabel('Chern Number C', fontsize=11)
    ax4.set_ylabel('Signal Strength (relative)', fontsize=11)
    ax4.set_title('Prediction 5: Quadratic Scaling\n"Signal ∝ C²"',
                  fontweight='bold', fontsize=11)
    ax4.legend()
    
    for bar, c, s in zip(bars, C_vals, signals):
        ax4.annotate(f'{s}×', xy=(bar.get_x() + bar.get_width()/2, s + 0.5),
                     ha='center', fontweight='bold', fontsize=10)
    
    # --- Panel 5: Detection Regimes ---
    ax5 = fig.add_subplot(gs[1, 1])
    
    regimes = ['g/m > 10⁻³', '10⁻³ to 10⁻⁶', '< 10⁻⁶', '< 10⁻⁹']
    times = [0.001, 1, 3600, np.nan]  # seconds
    labels = ['Single Shot\n(trivial)', 'Seconds\n(feasible)', 'Hours\n(challenging)', 'FALSIFIED']
    colors = ['green', 'lightgreen', 'orange', 'red']
    
    y_pos = np.arange(len(regimes))
    bars = ax5.barh(y_pos, [1, 1, 1, 1], color=colors, alpha=0.7, edgecolor='black', lw=2)
    
    ax5.set_yticks(y_pos)
    ax5.set_yticklabels(regimes)
    ax5.set_xlim(0, 1.5)
    ax5.set_xlabel('')
    ax5.set_title('Detection Feasibility by Coupling\n"Where is the threshold?"',
                  fontweight='bold', fontsize=11)
    
    for i, (bar, label) in enumerate(zip(bars, labels)):
        ax5.annotate(label, xy=(0.5, i), ha='center', va='center',
                     fontweight='bold', fontsize=11,
                     color='white' if i == 3 else 'black')
    
    ax5.set_xticks([])
    
    # --- Panel 6: Experimental Protocol ---
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')
    
    protocol_text = """
    EXPERIMENTAL PROTOCOL
    ━━━━━━━━━━━━━━━━━━━━━
    
    Phase 1: EXISTENCE
    • Match topologies (C_A = C_B = 3)
    • Apply E·B modulation
    • Detect χ > 5σ
    
    Phase 2: SELECTIVITY
    • Compare matched vs mismatched
    • Confirm selectivity > 10×
    
    Phase 3: EXTRACT g/m
    • Sweep drive frequency ω_d
    • Find resonance peak
    • Measure amplitude
    
    Phase 4: VERIFY SCALING
    • χ ∝ θ₁ (linear)
    • χ ∝ n (linear)
    • χ ∝ C² (quadratic)
    
    ━━━━━━━━━━━━━━━━━━━━━
    SUCCESS = Theory confirmed
    FAILURE = Theory falsified
    """
    
    ax6.text(0.05, 0.95, protocol_text, transform=ax6.transAxes,
             fontsize=10, fontfamily='monospace', va='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', 
                       edgecolor='black', alpha=0.9))
    
    fig.suptitle('QUANTITATIVE PREDICTIONS FOR TABLETOP EXPERIMENT\n'
                 'Signal: χ = (α/2π) × (g₀²/Δ) × (g·θ₁/m) × n',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


# =============================================================================
# FIGURE 3: Parameter Space Map
# =============================================================================

def plot_parameter_space(save_path=None):
    """2D map of signal strength in parameter space."""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create 2D grid: g/m vs photon number
    g_over_m = np.logspace(-9, 0, 200)
    n_photons = np.logspace(0, 9, 200)
    
    G, N = np.meshgrid(g_over_m, n_photons)
    
    # Compute signal (conservative parameters, but varying n)
    p = PARAMS
    chi = p['alpha_2pi'] * (p['g0_conservative']**2 / p['Delta_conservative']) * \
          G * p['theta1_conservative'] * N
    
    # Plot as contour
    levels = np.logspace(-6, 9, 16)
    
    cmap = LinearSegmentedColormap.from_list('signal', 
        ['darkred', 'red', 'orange', 'yellow', 'lightgreen', 'green', 'darkgreen'])
    
    cs = ax.contourf(G, N, chi, levels=levels, cmap=cmap, norm=plt.matplotlib.colors.LogNorm())
    
    # Contour lines for key thresholds
    ax.contour(G, N, chi, levels=[1], colors='red', linewidths=3, linestyles='-')
    ax.contour(G, N, chi, levels=[1e3], colors='orange', linewidths=3, linestyles='-')
    ax.contour(G, N, chi, levels=[1e6], colors='green', linewidths=3, linestyles='-')
    
    # Labels
    ax.text(1e-7, 1e8, 'χ = 1 Hz', color='red', fontsize=12, fontweight='bold',
            rotation=45)
    ax.text(1e-5, 1e7, 'χ = 1 kHz', color='orange', fontsize=12, fontweight='bold',
            rotation=45)
    ax.text(1e-3, 1e6, 'χ = 1 MHz', color='green', fontsize=12, fontweight='bold',
            rotation=45)
    
    # Mark feasibility boundary
    ax.axvline(1e-6, color='white', ls='--', lw=2, alpha=0.8)
    ax.text(1.2e-6, 1e1, 'Feasibility\nBoundary', color='white', fontsize=11,
            fontweight='bold', va='bottom')
    
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Coupling Ratio g/m (rad⁻¹)', fontsize=13)
    ax.set_ylabel('Photon Number n', fontsize=13)
    ax.set_title('SIGNAL STRENGTH PARAMETER SPACE\n'
                 'Contours show χ in Hz (red=1Hz, orange=1kHz, green=1MHz)',
                 fontweight='bold', fontsize=14)
    
    cbar = plt.colorbar(cs, ax=ax, label='Signal χ (Hz)')
    cbar.ax.set_ylabel('Signal χ (Hz)', fontsize=12)
    
    # Annotate regions
    ax.annotate('EASY\nDETECTION', xy=(1e-1, 1e6), fontsize=14, fontweight='bold',
                color='white', ha='center')
    ax.annotate('FEASIBLE\nWITH EFFORT', xy=(1e-5, 1e4), fontsize=12, fontweight='bold',
                color='black', ha='center')
    ax.annotate('THEORY\nFALSIFIED', xy=(1e-8, 1e2), fontsize=12, fontweight='bold',
                color='white', ha='center')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("  SIGNAL STRENGTH PREDICTIONS - VISUALIZATION")
    print("  Coherence Telephone Framework #6")
    print("=" * 70)
    
    import os
    os.makedirs('/home/claude/sim_outputs', exist_ok=True)
    
    # Generate all figures
    print("\n[1/3] Signal vs Coupling...")
    plot_signal_vs_coupling('/home/claude/sim_outputs/signal_vs_coupling.png')
    
    print("[2/3] Predictions Summary...")
    plot_predictions_summary('/home/claude/sim_outputs/predictions_summary.png')
    
    print("[3/3] Parameter Space Map...")
    plot_parameter_space('/home/claude/sim_outputs/parameter_space.png')
    
    # Print numerical summary
    print("\n" + "=" * 70)
    print("  NUMERICAL PREDICTIONS")
    print("=" * 70)
    
    test_values = [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8]
    
    print(f"\n{'g/m (rad⁻¹)':<15} {'χ_cons (Hz)':<15} {'χ_opt (Hz)':<15} {'Int. Time':<15}")
    print("-" * 60)
    
    for gm in test_values:
        chi_c = chi_signal(gm, conservative=True)
        chi_o = chi_signal(gm, conservative=False)
        t_int = integration_time(chi_c)
        
        # Format time
        if t_int < 1:
            t_str = f"{t_int*1e6:.1f} μs"
        elif t_int < 60:
            t_str = f"{t_int:.1f} s"
        elif t_int < 3600:
            t_str = f"{t_int/60:.1f} min"
        elif t_int < 86400:
            t_str = f"{t_int/3600:.1f} hr"
        else:
            t_str = f"{t_int/86400:.1f} days"
        
        print(f"{gm:<15.0e} {chi_c:<15.2e} {chi_o:<15.2e} {t_str:<15}")
    
    print("\n" + "=" * 70)
    print("  OUTPUT FILES")
    print("=" * 70)
    print("  • signal_vs_coupling.png")
    print("  • predictions_summary.png")
    print("  • parameter_space.png")
    print("=" * 70)


if __name__ == "__main__":
    main()
