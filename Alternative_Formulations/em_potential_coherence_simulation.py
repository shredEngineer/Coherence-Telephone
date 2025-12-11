#!/usr/bin/env python3
"""
EM 4-Potential Coherence Simulation

Exploring Dr. Wilhelm's suggestion to compute coherence C directly from
electromagnetic 4-potential A^μ time history, rather than through entropy
and phase alignment.

This simulation compares multiple functional forms and evaluates their
behavior against the entropy-based formulation.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from matplotlib.gridspec import GridSpec

# Physical constants
HBAR = 1.054571817e-34  # J·s
C_LIGHT = 2.99792458e8  # m/s
E_CHARGE = 1.602176634e-19  # C
K_B = 1.380649e-23  # J/K

class EMPotentialCoherence:
    """Compute coherence from EM 4-potential using various functionals"""
    
    def __init__(self, alpha=1.0, beta=1.0, tau=1.0):
        """
        Parameters:
        -----------
        alpha : float
            Field gradient sensitivity constant
        beta : float
            Field strength sensitivity constant
        tau : float
            Memory time window (seconds)
        """
        self.alpha = alpha
        self.beta = beta
        self.tau = tau
    
    def gradient_based(self, A_field, dx, dt):
        """
        Gradient-based coherence: C = exp(-α ∫ |∇A|² dt)
        
        Parameters:
        -----------
        A_field : ndarray, shape (time_steps, spatial_points)
            Vector potential A(x,t)
        dx : float
            Spatial step size
        dt : float
            Time step size
        
        Returns:
        --------
        C : ndarray, shape (time_steps, spatial_points)
            Coherence field C(x,t)
        """
        # Compute spatial gradient |∇A|²
        grad_A = np.gradient(A_field, dx, axis=1)
        grad_A_squared = grad_A**2
        
        # Time integration over memory window
        n_memory = int(self.tau / dt)
        C = np.zeros_like(A_field)
        
        for t in range(len(A_field)):
            t_start = max(0, t - n_memory)
            integrand = grad_A_squared[t_start:t+1]
            integral = simpson(integrand, dx=dt, axis=0)
            C[t] = np.exp(-self.alpha * integral)
        
        return C
    
    def field_strength_based(self, A_field, dx, dt):
        """
        Field strength based: C = exp(-β ∫ F_μν F^μν dt)
        
        For 1D simplification: F_μν F^μν ≈ (∂_t A)² - (∂_x A)²
        """
        # Temporal derivative
        dA_dt = np.gradient(A_field, dt, axis=0)
        
        # Spatial derivative
        dA_dx = np.gradient(A_field, dx, axis=1)
        
        # Field strength invariant (simplified 1D)
        F_invariant = dA_dt**2 - dA_dx**2
        
        # Time integration
        n_memory = int(self.tau / dt)
        C = np.zeros_like(A_field)
        
        for t in range(len(A_field)):
            t_start = max(0, t - n_memory)
            integrand = F_invariant[t_start:t+1]
            integral = simpson(integrand, dx=dt, axis=0)
            C[t] = np.exp(-self.beta * np.abs(integral))
        
        return C
    
    def phase_correlation(self, A_field, dx, dt):
        """
        Phase correlation: C = |∫ exp(iφ[A]) dt| / τ
        
        Phase from Wilson line: φ = (e/ℏ) ∫ A dx
        """
        # Compute phase from vector potential
        phase = (E_CHARGE / HBAR) * A_field * dx
        
        # Complex phase factor
        phase_factor = np.exp(1j * phase)
        
        # Time integration over memory window
        n_memory = int(self.tau / dt)
        C = np.zeros_like(A_field, dtype=float)
        
        for t in range(len(A_field)):
            t_start = max(0, t - n_memory)
            integral = simpson(phase_factor[t_start:t+1], dx=dt, axis=0)
            C[t] = np.abs(integral) / (self.tau if self.tau > 0 else dt)
        
        return C
    
    def hybrid(self, A_field, dx, dt):
        """
        Hybrid approach combining gradient and field strength
        """
        C_grad = self.gradient_based(A_field, dx, dt)
        C_field = self.field_strength_based(A_field, dx, dt)
        return np.sqrt(C_grad * C_field)  # Geometric mean


class EntropyCoherence:
    """Traditional entropy-based coherence: C = exp(-S/k) · Φ"""
    
    def __init__(self, k=1.0):
        """
        Parameters:
        -----------
        k : float
            Scale constant (J/K)
        """
        self.k = k
    
    def compute(self, A_field, T=4.0):
        """
        Compute coherence from entropy estimate
        
        Entropy estimated from field fluctuations:
        S ∝ k_B * log(σ_A²)
        
        Phase alignment Φ from field stability
        """
        # Estimate entropy from field variance
        sigma_A = np.std(A_field, axis=0)
        S = K_B * np.log(1 + sigma_A**2)
        
        # Phase alignment from temporal correlation
        autocorr = np.correlate(A_field[:, 0], A_field[:, 0], mode='full')
        Phi = np.abs(autocorr[len(autocorr)//2]) / np.max(np.abs(autocorr))
        
        # Coherence
        C = np.exp(-S / self.k) * Phi
        
        # Broadcast to full field
        C_field = np.outer(np.ones(len(A_field)), C)
        
        return C_field


def generate_em_field(scenario, x, t, params=None):
    """
    Generate EM field A(x,t) for different scenarios
    
    Parameters:
    -----------
    scenario : str
        'smooth', 'turbulent', 'modulated', or 'two_node'
    x : ndarray
        Spatial coordinates
    t : ndarray
        Time coordinates
    params : dict
        Scenario-specific parameters
    
    Returns:
    --------
    A_field : ndarray, shape (len(t), len(x))
        Vector potential A(x,t)
    """
    if params is None:
        params = {}
    
    X, T = np.meshgrid(x, t)
    
    if scenario == 'smooth':
        # Smooth sinusoidal field
        k = params.get('k', 2*np.pi)
        omega = params.get('omega', 2*np.pi)
        A0 = params.get('A0', 1.0)
        A_field = A0 * np.sin(k * X - omega * T)
    
    elif scenario == 'turbulent':
        # Multi-mode random field
        A_field = np.zeros_like(X)
        N_modes = params.get('N_modes', 10)
        
        for n in range(N_modes):
            k_n = (n + 1) * 2*np.pi / (x[-1] - x[0])
            omega_n = (n + 1) * 2*np.pi / (t[-1] - t[0])
            phi_n = np.random.uniform(0, 2*np.pi)
            A_n = np.random.uniform(0.1, 1.0)
            
            A_field += A_n * np.sin(k_n * X - omega_n * T + phi_n)
        
        A_field /= np.sqrt(N_modes)  # Normalize
    
    elif scenario == 'modulated':
        # Carrier modulated with bit pattern
        k = params.get('k', 2*np.pi)
        omega = params.get('omega', 2*np.pi)
        A0 = params.get('A0', 1.0)
        bit_pattern = params.get('bit_pattern', [1, 0, 1, 1, 0])
        bit_duration = len(t) // len(bit_pattern)
        
        carrier = A0 * np.sin(k * X - omega * T)
        
        # Modulation function
        modulation = np.zeros(len(t))
        for i, bit in enumerate(bit_pattern):
            start = i * bit_duration
            end = min((i + 1) * bit_duration, len(t))
            modulation[start:end] = 0.5 if bit == 0 else 1.0
        
        A_field = carrier * modulation[:, np.newaxis]
    
    elif scenario == 'two_node':
        # Two spatial locations, Node A modulates
        k = params.get('k', 2*np.pi)
        omega = params.get('omega', 2*np.pi)
        A0 = params.get('A0', 1.0)
        x_A = params.get('x_A', x[len(x)//4])
        x_B = params.get('x_B', x[3*len(x)//4])
        
        # Base field
        A_field = A0 * np.sin(k * X - omega * T)
        
        # Node A modulation (localized)
        bit_pattern = params.get('bit_pattern', [1, 0, 1, 1, 0])
        bit_duration = len(t) // len(bit_pattern)
        
        for i, bit in enumerate(bit_pattern):
            start = i * bit_duration
            end = min((i + 1) * bit_duration, len(t))
            
            # Gaussian localized modulation at x_A
            spatial_profile = np.exp(-((x - x_A)**2) / (2 * 0.1**2))
            modulation_factor = 0.5 if bit == 0 else 1.5
            
            A_field[start:end] *= (1 + (modulation_factor - 1) * spatial_profile)
    
    return A_field


def run_comparison_simulation():
    """Run full comparison of EM vs entropy approaches"""
    
    print("=" * 60)
    print("EM 4-Potential Coherence Simulation")
    print("Comparing Wilhelm's alternative with entropy formulation")
    print("=" * 60)
    
    # Spatial and temporal grids
    x = np.linspace(0, 1, 100)  # meters
    t = np.linspace(0, 1, 200)  # seconds
    dx = x[1] - x[0]
    dt = t[1] - t[0]
    
    # Initialize coherence calculators
    em_coherence = EMPotentialCoherence(alpha=1.0, beta=1.0, tau=0.1)
    entropy_coherence = EntropyCoherence(k=1.0)
    
    scenarios = ['smooth', 'turbulent', 'modulated']
    
    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(len(scenarios), 4, figure=fig, hspace=0.3, wspace=0.3)
    
    for row, scenario in enumerate(scenarios):
        print(f"\nSimulating scenario: {scenario.upper()}")
        
        # Generate EM field
        params = {
            'A0': 1.0,
            'k': 2*np.pi,
            'omega': 2*np.pi,
            'bit_pattern': [1, 0, 1, 1, 0, 1, 0, 0],
            'N_modes': 20
        }
        A_field = generate_em_field(scenario, x, t, params)
        
        # Compute coherence using different methods
        print("  Computing gradient-based coherence...")
        C_gradient = em_coherence.gradient_based(A_field, dx, dt)
        
        print("  Computing field-strength coherence...")
        C_field = em_coherence.field_strength_based(A_field, dx, dt)
        
        print("  Computing entropy-based coherence...")
        C_entropy = entropy_coherence.compute(A_field)
        
        # Plot A field
        ax1 = fig.add_subplot(gs[row, 0])
        im1 = ax1.imshow(A_field, aspect='auto', cmap='RdBu', 
                         extent=[x[0], x[-1], t[-1], t[0]])
        ax1.set_title(f'{scenario.capitalize()}: A(x,t)')
        ax1.set_xlabel('Position (m)')
        ax1.set_ylabel('Time (s)')
        plt.colorbar(im1, ax=ax1, label='A')
        
        # Plot EM gradient coherence
        ax2 = fig.add_subplot(gs[row, 1])
        im2 = ax2.imshow(C_gradient, aspect='auto', cmap='viridis', vmin=0, vmax=1,
                         extent=[x[0], x[-1], t[-1], t[0]])
        ax2.set_title('EM Gradient: C(x,t)')
        ax2.set_xlabel('Position (m)')
        ax2.set_ylabel('Time (s)')
        plt.colorbar(im2, ax=ax2, label='C')
        
        # Plot EM field strength coherence
        ax3 = fig.add_subplot(gs[row, 2])
        im3 = ax3.imshow(C_field, aspect='auto', cmap='viridis', vmin=0, vmax=1,
                         extent=[x[0], x[-1], t[-1], t[0]])
        ax3.set_title('EM Field Strength: C(x,t)')
        ax3.set_xlabel('Position (m)')
        ax3.set_ylabel('Time (s)')
        plt.colorbar(im3, ax=ax3, label='C')
        
        # Plot entropy-based coherence
        ax4 = fig.add_subplot(gs[row, 3])
        im4 = ax4.imshow(C_entropy, aspect='auto', cmap='viridis', vmin=0, vmax=1,
                         extent=[x[0], x[-1], t[-1], t[0]])
        ax4.set_title('Entropy Method: C(x,t)')
        ax4.set_xlabel('Position (m)')
        ax4.set_ylabel('Time (s)')
        plt.colorbar(im4, ax=ax4, label='C')
        
        # Compute statistics
        print(f"  Gradient method: mean C = {np.mean(C_gradient):.3f}, std = {np.std(C_gradient):.3f}")
        print(f"  Field strength method: mean C = {np.mean(C_field):.3f}, std = {np.std(C_field):.3f}")
        print(f"  Entropy method: mean C = {np.mean(C_entropy):.3f}, std = {np.std(C_entropy):.3f}")
    
    plt.suptitle('EM 4-Potential vs Entropy Coherence Comparison', fontsize=16, y=0.995)
    plt.savefig('/home/claude/em_coherence_comparison.png', dpi=300, bbox_inches='tight')
    print(f"\nFigure saved: em_coherence_comparison.png")
    
    return fig


def run_two_node_simulation():
    """Simulate two-node communication scenario"""
    
    print("\n" + "=" * 60)
    print("Two-Node Communication Simulation")
    print("Testing information transfer through coherence field")
    print("=" * 60)
    
    # Setup
    x = np.linspace(0, 1, 200)
    t = np.linspace(0, 2, 400)
    dx = x[1] - x[0]
    dt = t[1] - t[0]
    
    # Node positions
    x_A = x[50]   # Node A at 1/4 position
    x_B = x[150]  # Node B at 3/4 position
    
    params = {
        'x_A': x_A,
        'x_B': x_B,
        'bit_pattern': [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        'A0': 1.0
    }
    
    print(f"Node A position: {x_A:.3f} m")
    print(f"Node B position: {x_B:.3f} m")
    print(f"Separation: {x_B - x_A:.3f} m")
    print(f"Bit pattern: {params['bit_pattern']}")
    
    # Generate field with modulation
    A_field = generate_em_field('two_node', x, t, params)
    
    # Compute coherence
    em_coherence = EMPotentialCoherence(alpha=2.0, beta=1.0, tau=0.05)
    C_field = em_coherence.gradient_based(A_field, dx, dt)
    
    # Extract time series at nodes
    idx_A = np.argmin(np.abs(x - x_A))
    idx_B = np.argmin(np.abs(x - x_B))
    
    C_A = C_field[:, idx_A]
    C_B = C_field[:, idx_B]
    
    # Create figure
    fig, axes = plt.subplots(3, 2, figsize=(14, 10))
    
    # Full field visualization
    ax1 = axes[0, 0]
    im1 = ax1.imshow(A_field, aspect='auto', cmap='RdBu',
                     extent=[x[0], x[-1], t[-1], t[0]])
    ax1.axvline(x_A, color='red', linestyle='--', label='Node A')
    ax1.axvline(x_B, color='blue', linestyle='--', label='Node B')
    ax1.set_title('EM Potential A(x,t)')
    ax1.set_xlabel('Position (m)')
    ax1.set_ylabel('Time (s)')
    ax1.legend()
    plt.colorbar(im1, ax=ax1)
    
    ax2 = axes[0, 1]
    im2 = ax2.imshow(C_field, aspect='auto', cmap='viridis', vmin=0, vmax=1,
                     extent=[x[0], x[-1], t[-1], t[0]])
    ax2.axvline(x_A, color='red', linestyle='--', label='Node A')
    ax2.axvline(x_B, color='blue', linestyle='--', label='Node B')
    ax2.set_title('Coherence Field C(x,t)')
    ax2.set_xlabel('Position (m)')
    ax2.set_ylabel('Time (s)')
    ax2.legend()
    plt.colorbar(im2, ax=ax2)
    
    # Time series at nodes
    ax3 = axes[1, 0]
    ax3.plot(t, C_A, 'r-', linewidth=2, label='Node A')
    ax3.set_title('Coherence at Node A (Transmitter)')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Coherence C')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim([0, 1])
    
    ax4 = axes[1, 1]
    ax4.plot(t, C_B, 'b-', linewidth=2, label='Node B')
    ax4.set_title('Coherence at Node B (Receiver)')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Coherence C')
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim([0, 1])
    
    # Cross-correlation
    ax5 = axes[2, 0]
    correlation = np.correlate(C_A - np.mean(C_A), C_B - np.mean(C_B), mode='full')
    lags = np.arange(-len(C_A)+1, len(C_A))
    lag_time = lags * dt
    
    ax5.plot(lag_time, correlation / np.max(np.abs(correlation)))
    ax5.axvline(0, color='k', linestyle='--', alpha=0.5)
    ax5.set_title('Cross-Correlation C_A ⊗ C_B')
    ax5.set_xlabel('Lag Time (s)')
    ax5.set_ylabel('Correlation')
    ax5.grid(True, alpha=0.3)
    
    # Find peak correlation and lag
    peak_idx = np.argmax(np.abs(correlation))
    peak_lag = lag_time[peak_idx]
    peak_corr = correlation[peak_idx] / np.max(np.abs(correlation))
    
    ax5.plot(peak_lag, peak_corr, 'ro', markersize=10, label=f'Peak: τ={peak_lag:.3f}s')
    ax5.legend()
    
    # Comparison overlay
    ax6 = axes[2, 1]
    ax6.plot(t, C_A, 'r-', linewidth=2, alpha=0.7, label='Node A')
    ax6.plot(t, C_B, 'b-', linewidth=2, alpha=0.7, label='Node B')
    ax6.set_title('Direct Comparison')
    ax6.set_xlabel('Time (s)')
    ax6.set_ylabel('Coherence C')
    ax6.legend()
    ax6.grid(True, alpha=0.3)
    ax6.set_ylim([0, 1])
    
    plt.tight_layout()
    plt.savefig('/home/claude/two_node_communication.png', dpi=300, bbox_inches='tight')
    print(f"\nFigure saved: two_node_communication.png")
    
    # Analysis
    print(f"\nAnalysis:")
    print(f"  Peak correlation: {peak_corr:.3f}")
    print(f"  Signal lag: {peak_lag:.6f} s")
    print(f"  Light travel time ({x_B-x_A:.3f}m): {(x_B-x_A)/C_LIGHT:.6e} s")
    
    if np.abs(peak_lag) < (x_B - x_A) / C_LIGHT:
        print(f"  Result: SUPERLUMINAL correlation detected! (if real)")
    else:
        print(f"  Result: Correlation within light-speed constraint")
    
    return fig


if __name__ == '__main__':
    print("Starting EM 4-Potential Coherence Simulations\n")
    
    # Run comparison
    fig1 = run_comparison_simulation()
    
    # Run two-node test
    fig2 = run_two_node_simulation()
    
    print("\n" + "=" * 60)
    print("Simulation Complete")
    print("=" * 60)
    print("\nGenerated files:")
    print("  1. em_coherence_comparison.png")
    print("  2. two_node_communication.png")
    print("\nNext steps:")
    print("  - Review results")
    print("  - Compare with entropy formulation")
    print("  - Identify distinguishing predictions")
    print("  - Share with Dr. Wilhelm for feedback")
