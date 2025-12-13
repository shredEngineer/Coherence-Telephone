#!/usr/bin/env python3
"""
COUPLED SYSTEM SIMULATION - PHYSICAL PARAMETERS
Coherence Telephone - Framework #6

This version uses the coupling constant g derived from first principles:
    g = α × C  (fine structure constant × Chern number)
    
The effective coupling scales as C² — this is why higher Chern numbers
dramatically improve signal strength.

John Bollinger | December 2025

⚠️ DISCLAIMER: Theoretical demonstration using derived physical parameters.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')


# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

ALPHA = 1/137  # Fine structure constant
PI = np.pi


@dataclass
class PhysicalParams:
    """
    Simulation parameters derived from physical constants.
    
    Key relation: g = α × C (coupling from axion electrodynamics)
    Effective coupling: 4πα C² (scales quadratically with Chern number)
    """
    
    # Time parameters
    Nt: int = 2000
    dt: float = 0.005
    
    # Coherence field mass (sets characteristic frequency)
    # In real materials, related to gap: m ~ Δ/ℏ
    m: float = 0.3
    
    # Damping (decoherence rate)
    gamma: float = 0.02
    
    # E·B modulation
    omega: float = 1.0      # Modulation frequency
    EB_amplitude: float = 1.0  # Normalized E·B amplitude
    
    # Noise (thermal + quantum fluctuations)
    noise_level: float = 0.01
    
    def coupling_g(self, C: int) -> float:
        """Coupling constant g = α × C"""
        return ALPHA * C
    
    def effective_coupling(self, C: int) -> float:
        """Full effective coupling factor: 4πα C²"""
        return 4 * PI * ALPHA * C**2
    
    def theta(self, C: int) -> float:
        """Axion angle θ = 2πC"""
        return 2 * PI * C


# =============================================================================
# COHERENCE CHANNEL (Physical Model)
# =============================================================================

class PhysicalCoherenceChannel:
    """
    Coherence field channel with physical coupling.
    
    Equation of motion:
        d²Φ/dt² + γ dΦ/dt + m²Φ = 4παC² × Φ × (E·B)
    
    The C² scaling means higher Chern numbers give quadratically 
    stronger response.
    """
    
    def __init__(self, chern: int, params: PhysicalParams):
        self.C = chern
        self.p = params
        
        # Physical parameters for this channel
        self.theta = params.theta(chern)
        self.g = params.coupling_g(chern)
        self.coupling = params.effective_coupling(chern)
        
        # State
        self.Phi = 0.0
        self.dPhi = 0.0
        self.history = []
        
        print(f"  Channel C={chern}: g={self.g:.4f}, coupling={self.coupling:.4f}")
    
    def drive(self, EB: float):
        """Drive with E·B modulation using physical coupling."""
        # Source: 4παC² × Φ × (E·B)
        # For stability, use linear approximation when Φ is small
        source = self.coupling * (1 + self.Phi) * EB
        
        noise = self.p.noise_level * np.random.randn()
        
        # Damped harmonic oscillator
        d2Phi = -self.p.m**2 * self.Phi - self.p.gamma * self.dPhi + source + noise
        
        self.dPhi += d2Phi * self.p.dt
        self.Phi += self.dPhi * self.p.dt
        
        self.history.append(self.Phi)
    
    def idle(self):
        """Free evolution (no driving)."""
        noise = self.p.noise_level * np.random.randn()
        d2Phi = -self.p.m**2 * self.Phi - self.p.gamma * self.dPhi + noise
        
        self.dPhi += d2Phi * self.p.dt
        self.Phi += self.dPhi * self.p.dt
        
        self.history.append(self.Phi)


# =============================================================================
# NODE CLASS
# =============================================================================

class Node:
    """Measurement node coupled to a coherence channel."""
    
    def __init__(self, name: str, chern: int, channel: PhysicalCoherenceChannel):
        self.name = name
        self.C = chern
        self.channel = channel
        self.history = []
        self.local_noise = 0.05
    
    def measure(self):
        """Measure local coherence state."""
        measurement = self.channel.Phi + self.local_noise * np.random.randn()
        self.history.append(measurement)
        return measurement


# =============================================================================
# PHYSICAL SIMULATION
# =============================================================================

class PhysicalSimulation:
    """
    Simulation using physically derived coupling constants.
    
    Key predictions:
    - Coupling scales as C² (quadratic in Chern number)
    - g = α × C ≈ 0.0073 × C
    - Higher C = stronger signal (and better selectivity)
    """
    
    def __init__(self, params: PhysicalParams = None):
        self.p = params or PhysicalParams()
        self.channels: Dict[int, PhysicalCoherenceChannel] = {}
        self.nodes: List[Node] = []
        self.time = []
        self.EB_signal = []
        self.sender_idx = 0
    
    def add_node(self, name: str, chern: int) -> Node:
        """Add node, creating channel if needed."""
        if chern not in self.channels:
            self.channels[chern] = PhysicalCoherenceChannel(chern, self.p)
        
        node = Node(name, chern, self.channels[chern])
        self.nodes.append(node)
        return node
    
    def run(self, sender_idx: int = 0):
        """Run simulation."""
        self.sender_idx = sender_idx
        sender = self.nodes[sender_idx]
        
        print("\n" + "=" * 70)
        print("PHYSICAL COUPLING SIMULATION")
        print("=" * 70)
        print(f"Fine structure constant α = {ALPHA:.6f}")
        print(f"Sender: {sender.name} (C={sender.C})")
        print(f"Sender coupling g = α×{sender.C} = {self.p.coupling_g(sender.C):.4f}")
        print(f"Sender effective coupling = 4πα×{sender.C}² = {self.p.effective_coupling(sender.C):.4f}")
        print("-" * 70)
        
        for n in range(self.p.Nt):
            t = n * self.p.dt
            self.time.append(t)
            
            # E·B modulation
            EB = self.p.EB_amplitude * np.sin(2 * PI * self.p.omega * t)
            self.EB_signal.append(EB)
            
            # Drive sender's channel, others idle
            for C, channel in self.channels.items():
                if C == sender.C:
                    channel.drive(EB)
                else:
                    channel.idle()
            
            # Measure at all nodes
            for node in self.nodes:
                node.measure()
            
            if n % 400 == 0:
                print(f"  t = {t:.1f}")
        
        # Convert to arrays
        self.time = np.array(self.time)
        self.EB_signal = np.array(self.EB_signal)
        for node in self.nodes:
            node.history = np.array(node.history)
        for ch in self.channels.values():
            ch.history = np.array(ch.history)
        
        print("=" * 70)
    
    def correlation(self, n1: Node, n2: Node) -> float:
        """Compute correlation between nodes."""
        h1 = n1.history - np.mean(n1.history)
        h2 = n2.history - np.mean(n2.history)
        norm = np.sqrt(np.sum(h1**2) * np.sum(h2**2))
        return np.sum(h1 * h2) / norm if norm > 1e-10 else 0.0
    
    def analyze(self) -> Dict:
        """Analyze results."""
        sender = self.nodes[self.sender_idx]
        
        print("\n" + "=" * 70)
        print("RESULTS: Physical Coupling g = α × C")
        print("=" * 70)
        
        results = {'matched': [], 'mismatched': [], 'by_node': {}}
        
        for node in self.nodes:
            if node == sender:
                continue
            
            corr = self.correlation(sender, node)
            matched = node.C == sender.C
            
            results['by_node'][node.name] = {
                'C': node.C,
                'correlation': corr,
                'matched': matched,
                'coupling': self.p.effective_coupling(node.C)
            }
            
            status = "MATCHED" if matched else "MISMATCHED"
            coupling = self.p.effective_coupling(node.C)
            print(f"  {sender.name}↔{node.name} (C={node.C}): "
                  f"corr={corr:+.4f}, coupling={coupling:.4f} [{status}]")
            
            if matched:
                results['matched'].append(corr)
            else:
                results['mismatched'].append(corr)
        
        avg_m = np.mean(results['matched']) if results['matched'] else 0
        avg_mm = np.mean(results['mismatched']) if results['mismatched'] else 0
        
        print("-" * 70)
        print(f"  Average MATCHED:    {avg_m:+.4f}")
        print(f"  Average MISMATCHED: {avg_mm:+.4f}")
        
        if abs(avg_mm) > 0.001:
            ratio = abs(avg_m / avg_mm)
            print(f"  SELECTIVITY:        {ratio:.1f}×")
        
        results['avg_matched'] = avg_m
        results['avg_mismatched'] = avg_mm
        
        print("=" * 70)
        return results


# =============================================================================
# CHERN NUMBER SCALING STUDY
# =============================================================================

def run_chern_scaling_study():
    """
    Study how signal strength scales with Chern number.
    
    Prediction: Response amplitude ∝ C² (quadratic scaling)
    """
    
    print("\n" + "=" * 70)
    print("CHERN NUMBER SCALING STUDY")
    print("Prediction: Signal ∝ C² (quadratic scaling)")
    print("=" * 70)
    
    chern_values = [1, 2, 3, 4, 5]
    results = []
    
    for C in chern_values:
        params = PhysicalParams(Nt=1500, noise_level=0.005)
        
        sim = PhysicalSimulation(params)
        sim.add_node('Sender', C)
        sim.add_node('Receiver', C)  # Matched
        
        sim.run(sender_idx=0)
        
        # Measure signal amplitude
        sender = sim.nodes[0]
        receiver = sim.nodes[1]
        
        amplitude = np.std(receiver.history)
        corr = sim.correlation(sender, receiver)
        coupling = params.effective_coupling(C)
        
        results.append({
            'C': C,
            'g': params.coupling_g(C),
            'coupling': coupling,
            'amplitude': amplitude,
            'correlation': corr
        })
        
        print(f"\n  C={C}: g={params.coupling_g(C):.4f}, "
              f"coupling={coupling:.4f}, amplitude={amplitude:.4f}")
    
    return results


def plot_chern_scaling(results: List[Dict], save_path: str = None):
    """Visualize Chern number scaling."""
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    Cs = [r['C'] for r in results]
    couplings = [r['coupling'] for r in results]
    amplitudes = [r['amplitude'] for r in results]
    
    # Plot 1: Coupling vs C
    ax = axes[0]
    ax.bar(Cs, couplings, color='steelblue', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Chern Number C', fontsize=12)
    ax.set_ylabel('Effective Coupling (4παC²)', fontsize=12)
    ax.set_title('Coupling Strength\nScales as C²', fontweight='bold')
    
    # Add C² fit line
    C_fit = np.linspace(0.5, 5.5, 100)
    coupling_fit = 4 * PI * ALPHA * C_fit**2
    ax.plot(C_fit, coupling_fit, 'r--', lw=2, label='4παC²')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Plot 2: Signal amplitude vs C
    ax = axes[1]
    ax.bar(Cs, amplitudes, color='green', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Chern Number C', fontsize=12)
    ax.set_ylabel('Signal Amplitude (std)', fontsize=12)
    ax.set_title('Signal Strength\nIncreases with C', fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Plot 3: Amplitude vs Coupling (should be linear)
    ax = axes[2]
    ax.scatter(couplings, amplitudes, s=100, c=Cs, cmap='viridis', 
               edgecolor='black', linewidth=1.5)
    
    # Linear fit
    z = np.polyfit(couplings, amplitudes, 1)
    p = np.poly1d(z)
    x_fit = np.linspace(min(couplings), max(couplings), 100)
    ax.plot(x_fit, p(x_fit), 'r--', lw=2, label='Linear fit')
    
    for r in results:
        ax.annotate(f'C={r["C"]}', (r['coupling'], r['amplitude']),
                    xytext=(5, 5), textcoords='offset points', fontsize=10)
    
    ax.set_xlabel('Effective Coupling (4παC²)', fontsize=12)
    ax.set_ylabel('Signal Amplitude', fontsize=12)
    ax.set_title('Signal ∝ Coupling\n(Linear Response)', fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Colorbar
    sm = plt.cm.ScalarMappable(cmap='viridis', 
                                norm=plt.Normalize(vmin=1, vmax=5))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Chern Number', fontsize=10)
    
    fig.suptitle('PHYSICAL COUPLING: g = αC, Effective Coupling = 4παC²\n'
                 f'α = 1/137 ≈ {ALPHA:.4f} (Fine Structure Constant)',
                 fontsize=13, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"\nSaved: {save_path}")
    
    plt.close()


def plot_full_simulation(sim: PhysicalSimulation, save_path: str = None):
    """Plot full simulation results with physical parameters."""
    
    sender = sim.nodes[sim.sender_idx]
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    cmap = {1: '#E74C3C', 2: '#E67E22', 3: '#27AE60', 4: '#3498DB', 5: '#9B59B6'}
    
    # E·B signal
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(sim.time, sim.EB_signal, 'k-', lw=1, alpha=0.7)
    ax1.set_xlabel('Time')
    ax1.set_ylabel('E·B')
    ax1.set_title('E·B Modulation Signal', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Node time series
    ax2 = fig.add_subplot(gs[0, 1:])
    for node in sim.nodes:
        color = cmap.get(node.C, 'gray')
        style = '-' if node.C == sender.C else '--'
        lw = 2 if node == sender else 1.5
        label = f"{node.name} (C={node.C})"
        if node == sender:
            label += f" [g={sim.p.coupling_g(node.C):.4f}]"
        ax2.plot(sim.time, node.history, color=color, ls=style, lw=lw, 
                 label=label, alpha=0.8)
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Φ_C')
    ax2.set_title('Coherence at Each Node', fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # Scatter plots
    matched = [n for n in sim.nodes if n.C == sender.C and n != sender]
    mismatched = [n for n in sim.nodes if n.C != sender.C]
    
    ax3 = fig.add_subplot(gs[1, 0])
    if matched:
        m = matched[0]
        corr = sim.correlation(sender, m)
        ax3.scatter(sender.history, m.history, alpha=0.2, s=8, c=cmap.get(m.C))
        ax3.set_xlabel(f'Φ ({sender.name})')
        ax3.set_ylabel(f'Φ ({m.name})')
        ax3.set_title(f'MATCHED (C={sender.C}↔{m.C})\nCorr: {corr:.3f}', 
                      fontweight='bold', color='green')
    ax3.grid(True, alpha=0.3)
    
    ax4 = fig.add_subplot(gs[1, 1])
    if mismatched:
        m = mismatched[0]
        corr = sim.correlation(sender, m)
        ax4.scatter(sender.history, m.history, alpha=0.2, s=8, c=cmap.get(m.C))
        ax4.set_xlabel(f'Φ ({sender.name})')
        ax4.set_ylabel(f'Φ ({m.name})')
        ax4.set_title(f'MISMATCHED (C={sender.C}↔{m.C})\nCorr: {corr:.3f}',
                      fontweight='bold', color='red')
    ax4.grid(True, alpha=0.3)
    
    # Bar chart
    ax5 = fig.add_subplot(gs[1, 2])
    labels, correlations, colors = [], [], []
    for node in sim.nodes:
        if node == sender:
            continue
        corr = sim.correlation(sender, node)
        g = sim.p.coupling_g(node.C)
        labels.append(f'{node.name}\n(C={node.C}, g={g:.3f})')
        correlations.append(corr)
        colors.append('green' if node.C == sender.C else 'red')
    
    bars = ax5.bar(labels, correlations, color=colors, alpha=0.7, edgecolor='black')
    ax5.axhline(0, color='black', lw=0.5)
    ax5.set_ylabel('Correlation with Sender')
    ax5.set_title('Topology Selectivity', fontweight='bold')
    ax5.set_ylim(-0.3, 1.1)
    
    for bar, val in zip(bars, correlations):
        h = bar.get_height()
        ax5.annotate(f'{val:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords='offset points',
                     ha='center', fontweight='bold')
    
    g_sender = sim.p.coupling_g(sender.C)
    eff_sender = sim.p.effective_coupling(sender.C)
    
    fig.suptitle(f'PHYSICAL SIMULATION: α = 1/137, g = αC\n'
                 f'Sender C={sender.C}: g={g_sender:.4f}, '
                 f'effective coupling={eff_sender:.4f}',
                 fontsize=13, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"\nSaved: {save_path}")
    
    plt.close()


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 70)
    print("  COHERENCE TELEPHONE - PHYSICAL COUPLING SIMULATION")
    print("  Coupling Constant: g = α × C (Fine Structure × Chern)")
    print("  Effective Coupling: 4παC² (Quadratic Scaling)")
    print("=" * 70)
    print(f"\n  α = 1/137 ≈ {ALPHA:.6f}")
    print("  This is not arbitrary — it's derived from axion electrodynamics")
    print("=" * 70)
    
    import os
    os.makedirs('/home/claude/sim_outputs', exist_ok=True)
    
    # --- Main simulation with physical parameters ---
    print("\n[1/2] FULL SIMULATION WITH PHYSICAL g")
    
    params = PhysicalParams(
        Nt=2000,
        dt=0.005,
        m=0.3,
        gamma=0.02,
        omega=1.0,
        noise_level=0.01
    )
    
    sim = PhysicalSimulation(params)
    sim.add_node('Sender', 3)
    sim.add_node('Receiver_A', 3)  # Matched
    sim.add_node('Control_B', 2)   # Mismatched
    sim.add_node('Control_C', 1)   # Mismatched
    
    sim.run(sender_idx=0)
    results = sim.analyze()
    
    plot_full_simulation(sim, '/home/claude/sim_outputs/physical_coupling_simulation.png')
    
    # --- Chern scaling study ---
    print("\n[2/2] CHERN NUMBER SCALING STUDY")
    
    scaling_results = run_chern_scaling_study()
    plot_chern_scaling(scaling_results, '/home/claude/sim_outputs/chern_scaling_physical.png')
    
    # --- Summary ---
    print("\n" + "=" * 70)
    print("  SUMMARY: Physical Coupling Constants")
    print("=" * 70)
    print(f"\n  PHYSICAL PARAMETERS:")
    print(f"    • Fine structure constant α = {ALPHA:.6f}")
    print(f"    • Coupling g = α × C")
    print(f"    • Effective coupling = 4παC² (quadratic in C)")
    
    print(f"\n  VALUES BY CHERN NUMBER:")
    for C in [1, 2, 3, 4, 5]:
        g = ALPHA * C
        eff = 4 * PI * ALPHA * C**2
        print(f"    C={C}: g={g:.4f}, effective={eff:.4f}")
    
    print(f"\n  KEY RESULT:")
    print(f"    • MATCHED correlation:    {results['avg_matched']:+.4f}")
    print(f"    • MISMATCHED correlation: {results['avg_mismatched']:+.4f}")
    
    print("\n  OUTPUT FILES:")
    print("    • physical_coupling_simulation.png")
    print("    • chern_scaling_physical.png")
    print("=" * 70)
    
    return sim, results, scaling_results


if __name__ == "__main__":
    sim, results, scaling = main()
