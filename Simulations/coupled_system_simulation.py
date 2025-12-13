#!/usr/bin/env python3
"""
COUPLED SYSTEM SIMULATION - FINAL VERSION
Coherence Telephone - Framework #6

This simulation implements topology-selective coupling where nodes
with the SAME Chern number couple through a shared coherence channel,
while nodes with DIFFERENT Chern numbers remain uncoupled.

John Bollinger | December 2025

THE KEY PHYSICS:
    θ = 2πC (axion angle from Chern number)
    Same C → Same θ → Same coherence channel → COUPLED
    Different C → Different θ → Different channel → UNCOUPLED

⚠️ DISCLAIMER: Theoretical demonstration. Coupling constants illustrative.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from dataclasses import dataclass
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')


@dataclass
class Params:
    """Simulation parameters."""
    Nt: int = 1500
    dt: float = 0.01
    m: float = 0.5           # Mass term
    g: float = 1.0           # Coupling strength
    gamma: float = 0.05      # Damping
    omega: float = 2.0       # Modulation frequency
    amp: float = 1.0         # Modulation amplitude
    noise: float = 0.02      # Noise level


class CoherenceChannel:
    """
    A coherence field channel associated with a specific Chern number.
    
    All nodes with the same Chern number couple to this shared channel.
    The channel state is driven by E·B modulation at any connected node.
    """
    
    def __init__(self, chern: int, params: Params):
        self.C = chern
        self.theta = 2 * np.pi * chern
        self.p = params
        
        # Channel state
        self.Phi = 0.0
        self.dPhi = 0.0
        
        # History
        self.history = []
    
    def drive(self, EB: float):
        """Drive the channel with E·B modulation."""
        # Source term: 2g·θ·(E·B)
        source = 2 * self.p.g * self.theta * EB
        
        # Noise
        noise = self.p.noise * np.random.randn()
        
        # Damped harmonic oscillator
        d2Phi = -self.p.m**2 * self.Phi - self.p.gamma * self.dPhi + source + noise
        
        self.dPhi += d2Phi * self.p.dt
        self.Phi += self.dPhi * self.p.dt
        
        self.history.append(self.Phi)
    
    def idle(self):
        """Evolve channel without driving (free evolution + noise)."""
        noise = self.p.noise * np.random.randn()
        d2Phi = -self.p.m**2 * self.Phi - self.p.gamma * self.dPhi + noise
        
        self.dPhi += d2Phi * self.p.dt
        self.Phi += self.dPhi * self.p.dt
        
        self.history.append(self.Phi)


class Node:
    """
    A quantum node with a specific Chern number.
    
    The node's coherence state is determined by its channel (set by C).
    Nodes with the same C share the same channel and thus correlate.
    """
    
    def __init__(self, name: str, chern: int, channel: CoherenceChannel):
        self.name = name
        self.C = chern
        self.channel = channel
        self.history = []
        
        # Local measurement includes channel state + local noise
        self.local_noise_level = 0.1
    
    def measure(self):
        """Measure local coherence (channel state + local noise)."""
        local_noise = self.local_noise_level * np.random.randn()
        measurement = self.channel.Phi + local_noise
        self.history.append(measurement)
        return measurement


class TopologySelectiveSimulation:
    """
    Main simulation demonstrating topology-selective coupling.
    
    Nodes with matching Chern numbers couple through shared channels.
    Nodes with different Chern numbers are effectively independent.
    """
    
    def __init__(self, params: Params = None):
        self.p = params or Params()
        self.channels: Dict[int, CoherenceChannel] = {}
        self.nodes: List[Node] = []
        self.time = []
        self.EB_signal = []
        self.sender_idx = 0
    
    def add_node(self, name: str, chern: int) -> Node:
        """Add a node. Creates channel if needed."""
        if chern not in self.channels:
            self.channels[chern] = CoherenceChannel(chern, self.p)
        
        node = Node(name, chern, self.channels[chern])
        self.nodes.append(node)
        return node
    
    def run(self, sender_idx: int = 0):
        """Run simulation with E·B modulation at sender."""
        self.sender_idx = sender_idx
        sender = self.nodes[sender_idx]
        
        print("=" * 65)
        print("TOPOLOGY-SELECTIVE COHERENCE SIMULATION")
        print("=" * 65)
        print(f"Sender: {sender.name} (C = {sender.C})")
        print("-" * 65)
        
        for node in self.nodes:
            status = "← SENDER" if node == sender else ""
            match = "MATCHED" if node.C == sender.C and node != sender else ""
            if node.C != sender.C:
                match = "MISMATCHED"
            print(f"  {node.name}: C = {node.C}  {match} {status}")
        
        print("-" * 65)
        print(f"Channels active: {sorted(self.channels.keys())}")
        print("=" * 65)
        
        for n in range(self.p.Nt):
            t = n * self.p.dt
            self.time.append(t)
            
            # E·B modulation signal
            EB = self.p.amp * np.sin(2 * np.pi * self.p.omega * t)
            self.EB_signal.append(EB)
            
            # Drive sender's channel, idle others
            for C, channel in self.channels.items():
                if C == sender.C:
                    channel.drive(EB)
                else:
                    channel.idle()
            
            # All nodes measure their channel
            for node in self.nodes:
                node.measure()
            
            if n % 300 == 0:
                print(f"  t = {t:.1f}")
        
        # Convert to arrays
        self.time = np.array(self.time)
        self.EB_signal = np.array(self.EB_signal)
        for node in self.nodes:
            node.history = np.array(node.history)
        for channel in self.channels.values():
            channel.history = np.array(channel.history)
        
        print("=" * 65)
        print("COMPLETE")
        print("=" * 65)
    
    def correlation(self, n1: Node, n2: Node) -> float:
        """Compute correlation between two nodes."""
        h1 = n1.history - np.mean(n1.history)
        h2 = n2.history - np.mean(n2.history)
        norm = np.sqrt(np.sum(h1**2) * np.sum(h2**2))
        return np.sum(h1 * h2) / norm if norm > 1e-10 else 0.0
    
    def analyze(self) -> Dict:
        """Analyze results."""
        sender = self.nodes[self.sender_idx]
        
        print("\n" + "=" * 65)
        print("RESULTS")
        print("=" * 65)
        
        results = {'matched': [], 'mismatched': []}
        
        for node in self.nodes:
            if node == sender:
                continue
            
            corr = self.correlation(sender, node)
            matched = node.C == sender.C
            
            status = "MATCHED" if matched else "MISMATCHED"
            print(f"  {sender.name} ↔ {node.name}: {corr:+.4f}  ({status})")
            
            if matched:
                results['matched'].append(corr)
            else:
                results['mismatched'].append(corr)
        
        avg_matched = np.mean(results['matched']) if results['matched'] else 0
        avg_mismatched = np.mean(results['mismatched']) if results['mismatched'] else 0
        
        print("-" * 65)
        print(f"  Average MATCHED:    {avg_matched:+.4f}")
        print(f"  Average MISMATCHED: {avg_mismatched:+.4f}")
        
        if abs(avg_mismatched) > 0.01:
            ratio = abs(avg_matched / avg_mismatched)
            print(f"  SELECTIVITY RATIO:  {ratio:.1f}×")
        else:
            print(f"  SELECTIVITY RATIO:  >>10× (mismatched ≈ 0)")
        
        print("=" * 65)
        
        results['avg_matched'] = avg_matched
        results['avg_mismatched'] = avg_mismatched
        
        return results


def create_visualizations(sim: TopologySelectiveSimulation, 
                          output_dir: str = '/home/claude/sim_outputs'):
    """Generate all visualizations."""
    
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    sender = sim.nodes[sim.sender_idx]
    
    # =========================================================================
    # FIGURE 1: Main simulation results
    # =========================================================================
    
    fig = plt.figure(figsize=(16, 10))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)
    
    # Colors for Chern numbers
    cmap = {1: '#E74C3C', 2: '#E67E22', 3: '#27AE60', 4: '#3498DB', 5: '#9B59B6'}
    
    # --- E·B Signal ---
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(sim.time, sim.EB_signal, 'k-', lw=1.5, alpha=0.7)
    ax1.set_xlabel('Time', fontsize=11)
    ax1.set_ylabel('E·B', fontsize=11)
    ax1.set_title('E·B Modulation\n(Applied to Sender)', fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # --- Node Time Series ---
    ax2 = fig.add_subplot(gs[0, 1:])
    
    for node in sim.nodes:
        color = cmap.get(node.C, 'gray')
        style = '-' if node.C == sender.C else '--'
        lw = 2 if node == sender else 1.5
        alpha = 1.0 if node.C == sender.C else 0.6
        
        label = f"{node.name} (C={node.C})"
        if node == sender:
            label += " ← SENDER"
        elif node.C == sender.C:
            label += " [MATCHED]"
        else:
            label += " [mismatched]"
        
        ax2.plot(sim.time, node.history, color=color, ls=style, 
                 lw=lw, alpha=alpha, label=label)
    
    ax2.set_xlabel('Time', fontsize=11)
    ax2.set_ylabel('Φ_C (measured)', fontsize=11)
    ax2.set_title('Coherence at Each Node', fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    
    # --- Scatter: Matched ---
    ax3 = fig.add_subplot(gs[1, 0])
    matched_nodes = [n for n in sim.nodes if n.C == sender.C and n != sender]
    
    if matched_nodes:
        m = matched_nodes[0]
        corr = sim.correlation(sender, m)
        ax3.scatter(sender.history, m.history, alpha=0.2, s=8, 
                    c=cmap.get(m.C, 'green'))
        ax3.set_xlabel(f'Φ ({sender.name})', fontsize=11)
        ax3.set_ylabel(f'Φ ({m.name})', fontsize=11)
        ax3.set_title(f'MATCHED (C={sender.C}↔C={m.C})\nCorrelation: {corr:.3f}', 
                      fontweight='bold', color='green')
    ax3.grid(True, alpha=0.3)
    
    # --- Scatter: Mismatched ---
    ax4 = fig.add_subplot(gs[1, 1])
    mismatched_nodes = [n for n in sim.nodes if n.C != sender.C]
    
    if mismatched_nodes:
        m = mismatched_nodes[0]
        corr = sim.correlation(sender, m)
        ax4.scatter(sender.history, m.history, alpha=0.2, s=8,
                    c=cmap.get(m.C, 'red'))
        ax4.set_xlabel(f'Φ ({sender.name})', fontsize=11)
        ax4.set_ylabel(f'Φ ({m.name})', fontsize=11)
        ax4.set_title(f'MISMATCHED (C={sender.C}↔C={m.C})\nCorrelation: {corr:.3f}',
                      fontweight='bold', color='red')
    ax4.grid(True, alpha=0.3)
    
    # --- Bar Chart ---
    ax5 = fig.add_subplot(gs[1, 2])
    
    labels, correlations, colors = [], [], []
    for node in sim.nodes:
        if node == sender:
            continue
        corr = sim.correlation(sender, node)
        labels.append(f'{node.name}\n(C={node.C})')
        correlations.append(corr)
        colors.append('green' if node.C == sender.C else 'red')
    
    bars = ax5.bar(labels, correlations, color=colors, alpha=0.7, edgecolor='black')
    ax5.axhline(0, color='black', lw=0.5)
    ax5.set_ylabel('Correlation with Sender', fontsize=11)
    ax5.set_title('Topology Selectivity', fontweight='bold')
    ax5.set_ylim(-0.3, 1.1)
    ax5.grid(True, alpha=0.3, axis='y')
    
    for bar, val in zip(bars, correlations):
        h = bar.get_height()
        ax5.annotate(f'{val:.2f}', xy=(bar.get_x() + bar.get_width()/2, h),
                     xytext=(0, 3), textcoords='offset points',
                     ha='center', fontweight='bold', fontsize=11)
    
    fig.suptitle('COHERENCE TELEPHONE: Topology-Selective Coupling\n'
                 f'Sender C={sender.C} → Only nodes with C={sender.C} receive signal',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    path1 = f'{output_dir}/topology_selective_simulation.png'
    plt.savefig(path1, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"\nSaved: {path1}")
    plt.close()
    
    # =========================================================================
    # FIGURE 2: Channel separation diagram
    # =========================================================================
    
    fig2, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Channel time series
    ax = axes[0]
    for C, channel in sorted(sim.channels.items()):
        color = cmap.get(C, 'gray')
        lw = 2.5 if C == sender.C else 1.5
        ls = '-' if C == sender.C else '--'
        label = f'Channel C={C}'
        if C == sender.C:
            label += ' (DRIVEN)'
        else:
            label += ' (idle)'
        ax.plot(sim.time, channel.history, color=color, lw=lw, ls=ls,
                label=label, alpha=0.8)
    
    ax.set_xlabel('Time', fontsize=11)
    ax.set_ylabel('Channel State Φ', fontsize=11)
    ax.set_title('Coherence Field Channels\n(Separated by Chern Number)', fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Correlation matrix
    ax = axes[1]
    n = len(sim.nodes)
    corr_matrix = np.zeros((n, n))
    
    for i, n1 in enumerate(sim.nodes):
        for j, n2 in enumerate(sim.nodes):
            corr_matrix[i, j] = sim.correlation(n1, n2)
    
    im = ax.imshow(corr_matrix, cmap='RdYlGn', vmin=-1, vmax=1)
    
    labels = [f'{n.name}\n(C={n.C})' for n in sim.nodes]
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels, fontsize=9)
    ax.set_yticklabels(labels, fontsize=9)
    
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f'{corr_matrix[i,j]:.2f}', ha='center', va='center',
                    fontsize=10, fontweight='bold')
    
    ax.set_title('Correlation Matrix\n(Green = correlated, Red = uncorrelated)', 
                 fontweight='bold')
    plt.colorbar(im, ax=ax, label='Correlation')
    
    fig2.suptitle('TOPOLOGY AS ADDRESSING: Same Chern Number = Same Channel',
                  fontsize=13, fontweight='bold', y=1.02)
    
    plt.tight_layout()
    path2 = f'{output_dir}/channel_separation.png'
    plt.savefig(path2, dpi=150, bbox_inches='tight', facecolor='white')
    print(f"Saved: {path2}")
    plt.close()
    
    return [path1, path2]


def main():
    """Main execution."""
    
    print("\n" + "=" * 70)
    print("  COHERENCE TELEPHONE - TOPOLOGY-SELECTIVE COUPLING SIMULATION")
    print("  Path 1 Lagrangian Implementation")
    print("  John Bollinger | December 2025")
    print("=" * 70)
    
    # Simulation parameters
    params = Params(
        Nt=1500,
        dt=0.01,
        m=0.5,
        g=1.0,
        gamma=0.05,
        omega=2.0,
        noise=0.02,
    )
    
    # Create simulation with multiple nodes
    sim = TopologySelectiveSimulation(params)
    
    # Add nodes: Sender (C=3), Matched receiver (C=3), Mismatched controls (C=2, C=1)
    sim.add_node('Sender', 3)
    sim.add_node('Receiver_A', 3)   # Same C as sender → MATCHED
    sim.add_node('Control_B', 2)   # Different C → MISMATCHED  
    sim.add_node('Control_C', 1)   # Different C → MISMATCHED
    
    # Run
    sim.run(sender_idx=0)
    
    # Analyze
    results = sim.analyze()
    
    # Visualize
    paths = create_visualizations(sim)
    
    # Summary
    print("\n" + "=" * 70)
    print("  SUMMARY")
    print("=" * 70)
    print("\n  KEY FINDING:")
    print(f"    • MATCHED topology (same C):     {results['avg_matched']:+.4f} correlation")
    print(f"    • MISMATCHED topology (diff C):  {results['avg_mismatched']:+.4f} correlation")
    print("\n  INTERPRETATION:")
    print("    Nodes with the SAME Chern number couple through the SAME")
    print("    coherence field channel. E·B modulation at the sender drives")
    print("    this shared channel, creating correlated dynamics at matched")
    print("    receivers. Mismatched nodes remain uncoupled (noise only).")
    print("\n  OUTPUT FILES:")
    for p in paths:
        print(f"    • {p}")
    print("=" * 70)
    
    return sim, results


if __name__ == "__main__":
    sim, results = main()
