#!/usr/bin/env python3
"""
PHASE 1 TABLETOP PROTOCOL - VISUALIZATION
Coherence Telephone - Framework #6

Visual diagrams for the experimental protocol:
- Experimental schematic
- Sequence diagram
- Decision tree
- Timeline

John Bollinger | December 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Circle, FancyArrowPatch, Arrow
from matplotlib.patches import ConnectionPatch
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')


def plot_experimental_schematic(save_path=None):
    """Create detailed experimental schematic."""
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Colors
    C_CRYO = '#E8F4F8'
    C_SOURCE = '#FFE4E1'
    C_DETECT = '#E1FFE4'
    C_SHIELD = '#D0D0D0'
    C_COMPONENT = '#FFF8DC'
    
    # Main cryostat box
    cryo = FancyBboxPatch((0.5, 0.5), 13, 9, boxstyle="round,pad=0.1",
                           facecolor=C_CRYO, edgecolor='navy', linewidth=3)
    ax.add_patch(cryo)
    ax.text(7, 9.7, 'DILUTION REFRIGERATOR (T < 20 mK)', 
            ha='center', fontsize=14, fontweight='bold', color='navy')
    
    # Shielding barrier (center)
    shield = Rectangle((6.7, 1), 0.6, 7.5, facecolor=C_SHIELD, 
                        edgecolor='black', linewidth=2, hatch='///')
    ax.add_patch(shield)
    ax.text(7, 0.6, 'μ-METAL\nSHIELD', ha='center', fontsize=8, fontweight='bold')
    
    # Source Node A (left side)
    source_box = FancyBboxPatch((1, 1.5), 5, 7, boxstyle="round,pad=0.05",
                                 facecolor=C_SOURCE, edgecolor='red', linewidth=2)
    ax.add_patch(source_box)
    ax.text(3.5, 8.2, 'SOURCE NODE A', ha='center', fontsize=12, 
            fontweight='bold', color='darkred')
    
    # Source components
    # Topological array
    arr_s = FancyBboxPatch((1.5, 6), 4, 1.5, boxstyle="round,pad=0.02",
                            facecolor='#FFB6C1', edgecolor='darkred', linewidth=2)
    ax.add_patch(arr_s)
    ax.text(3.5, 6.75, '𝒞 = 3 ARRAY', ha='center', fontsize=11, fontweight='bold')
    ax.text(3.5, 6.3, '(Tunable Chern Insulator)', ha='center', fontsize=8)
    
    # Cavity
    cavity = FancyBboxPatch((1.5, 4), 4, 1.5, boxstyle="round,pad=0.02",
                             facecolor=C_COMPONENT, edgecolor='orange', linewidth=2)
    ax.add_patch(cavity)
    ax.text(3.5, 4.75, 'MICROWAVE CAVITY', ha='center', fontsize=10, fontweight='bold')
    ax.text(3.5, 4.3, 'ω_c/2π ~ 6-8 GHz', ha='center', fontsize=8)
    
    # E·B Drive
    drive = FancyBboxPatch((1.5, 2), 4, 1.5, boxstyle="round,pad=0.02",
                            facecolor='#FFDAB9', edgecolor='darkorange', linewidth=2)
    ax.add_patch(drive)
    ax.text(3.5, 2.75, 'E·B MODULATOR', ha='center', fontsize=10, fontweight='bold')
    ax.text(3.5, 2.3, 'δθ(t) = θ₁ cos(ω_d t)', ha='center', fontsize=9)
    
    # Detector Node B (right side)
    detect_box = FancyBboxPatch((8, 1.5), 5, 7, boxstyle="round,pad=0.05",
                                 facecolor=C_DETECT, edgecolor='green', linewidth=2)
    ax.add_patch(detect_box)
    ax.text(10.5, 8.2, 'DETECTOR NODE B', ha='center', fontsize=12,
            fontweight='bold', color='darkgreen')
    
    # Detector components
    # Topological array
    arr_d = FancyBboxPatch((8.5, 6), 4, 1.5, boxstyle="round,pad=0.02",
                            facecolor='#90EE90', edgecolor='darkgreen', linewidth=2)
    ax.add_patch(arr_d)
    ax.text(10.5, 6.75, '𝒞 = 3 ARRAY', ha='center', fontsize=11, fontweight='bold')
    ax.text(10.5, 6.3, '(Matched Topology)', ha='center', fontsize=8)
    
    # Readout qubit
    qubit = FancyBboxPatch((8.5, 4), 4, 1.5, boxstyle="round,pad=0.02",
                            facecolor=C_COMPONENT, edgecolor='purple', linewidth=2)
    ax.add_patch(qubit)
    ax.text(10.5, 4.75, 'READOUT QUBIT', ha='center', fontsize=10, fontweight='bold')
    ax.text(10.5, 4.3, 'T₂* > 50 μs', ha='center', fontsize=8)
    
    # Resonator
    reson = FancyBboxPatch((8.5, 2), 4, 1.5, boxstyle="round,pad=0.02",
                            facecolor='#E6E6FA', edgecolor='indigo', linewidth=2)
    ax.add_patch(reson)
    ax.text(10.5, 2.75, 'READOUT RESONATOR', ha='center', fontsize=10, fontweight='bold')
    ax.text(10.5, 2.3, 'QND Measurement', ha='center', fontsize=8)
    
    # Arrows between components
    arrow_style = dict(arrowstyle='->', color='black', lw=2)
    
    # Source internal arrows
    ax.annotate('', xy=(3.5, 5.5), xytext=(3.5, 6),
                arrowprops=dict(arrowstyle='->', color='darkred', lw=2))
    ax.annotate('', xy=(3.5, 3.5), xytext=(3.5, 4),
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=2))
    
    # Detector internal arrows
    ax.annotate('', xy=(10.5, 5.5), xytext=(10.5, 6),
                arrowprops=dict(arrowstyle='->', color='darkgreen', lw=2))
    ax.annotate('', xy=(10.5, 3.5), xytext=(10.5, 4),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2))
    
    # Coherence field coupling (dashed, through shield)
    ax.annotate('', xy=(8, 6.75), xytext=(6, 6.75),
                arrowprops=dict(arrowstyle='<->', color='blue', lw=3, 
                               linestyle='--', connectionstyle='arc3,rad=0'))
    ax.text(7, 7.3, 'Φ_C', fontsize=14, fontweight='bold', color='blue', ha='center')
    ax.text(7, 7.8, 'COHERENCE\nCHANNEL', fontsize=8, ha='center', color='blue')
    
    # Control & DAQ box at bottom
    daq = FancyBboxPatch((4, -0.8), 6, 1.2, boxstyle="round,pad=0.05",
                          facecolor='#F0F0F0', edgecolor='black', linewidth=2)
    ax.add_patch(daq)
    ax.text(7, -0.2, 'CONTROL & DATA ACQUISITION', ha='center', 
            fontsize=10, fontweight='bold')
    
    # Connections to DAQ
    ax.plot([3.5, 3.5, 5], [1.5, 0.8, 0.4], 'k-', lw=1.5)
    ax.plot([10.5, 10.5, 9], [1.5, 0.8, 0.4], 'k-', lw=1.5)
    
    # Legend
    legend_y = 9.3
    ax.add_patch(Rectangle((0.8, legend_y-0.3), 0.4, 0.3, facecolor=C_SOURCE, edgecolor='red'))
    ax.text(1.4, legend_y-0.15, 'Source', fontsize=9)
    ax.add_patch(Rectangle((2.5, legend_y-0.3), 0.4, 0.3, facecolor=C_DETECT, edgecolor='green'))
    ax.text(3.1, legend_y-0.15, 'Detector', fontsize=9)
    ax.add_patch(Rectangle((4.2, legend_y-0.3), 0.4, 0.3, facecolor=C_SHIELD, edgecolor='black', hatch='//'))
    ax.text(4.8, legend_y-0.15, 'Shield', fontsize=9)
    
    # Title
    fig.suptitle('PHASE 1: TABLETOP EXPERIMENTAL SETUP\n'
                 'Topology-Matched Nodes in Single Cryostat',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


def plot_sequence_diagram(save_path=None):
    """Create experimental sequence diagram."""
    
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Timeline
    ax.arrow(1, 7, 12, 0, head_width=0.15, head_length=0.2, fc='black', ec='black')
    ax.text(13.5, 7, 'Time', fontsize=11, fontweight='bold')
    
    # Phases
    phases = [
        (1.5, 'CALIBRATE', '#FFE4B5', 2),
        (4, 'MATCHED\n(𝒞=3↔𝒞=3)', '#90EE90', 2.5),
        (7, 'MISMATCHED\n(𝒞=2↔𝒞=3)', '#FFB6C1', 2.5),
        (10, 'CONTROLS', '#E6E6FA', 2.5),
    ]
    
    for x, label, color, width in phases:
        box = FancyBboxPatch((x, 6.3), width, 1.2, boxstyle="round,pad=0.05",
                              facecolor=color, edgecolor='black', linewidth=2)
        ax.add_patch(box)
        ax.text(x + width/2, 6.9, label, ha='center', va='center',
                fontsize=10, fontweight='bold')
    
    # Detailed steps
    steps_y = 5
    step_height = 4.5
    
    # Step boxes
    for i, (x, title, color, width) in enumerate(phases):
        # Vertical connector
        ax.plot([x + width/2, x + width/2], [6.3, steps_y], 'k--', lw=1)
        
    # Calibration steps
    cal_steps = ['1. Cool to <20mK', '2. Tune arrays to 𝒞=3', 
                 '3. Calibrate E·B drive', '4. Calibrate χ₀']
    for i, step in enumerate(cal_steps):
        ax.text(2.5, 4.5 - i*0.6, step, fontsize=9, ha='center')
    
    # Matched experiment steps
    match_steps = ['1. Initialize ground state', '2. Apply E·B pulse',
                   '3. Ramsey measurement', '4. Record χᵢ', 
                   '5. Repeat 10⁴-10⁶ times']
    for i, step in enumerate(match_steps):
        ax.text(5.25, 4.5 - i*0.6, step, fontsize=9, ha='center')
    
    # Mismatched steps
    mismatch_steps = ['1. Retune source to 𝒞=2', '2. Keep detector at 𝒞=3',
                      '3. SAME measurement', '4. Expected: χ → 0']
    for i, step in enumerate(mismatch_steps):
        ax.text(8.25, 4.5 - i*0.6, step, fontsize=9, ha='center')
    
    # Control steps
    control_steps = ['• RF shunting', '• Freq. detuning', 
                     '• Thermal test', '• Time reversal']
    for i, step in enumerate(control_steps):
        ax.text(11.25, 4.5 - i*0.6, step, fontsize=9, ha='center')
    
    # Expected results bar
    ax.text(7, 1.5, 'EXPECTED CROSS-CORRELATION C(0)', ha='center',
            fontsize=12, fontweight='bold')
    
    # Result bars
    bar_y = 0.8
    # Matched
    ax.add_patch(Rectangle((4, bar_y), 2, 0.5, facecolor='green', edgecolor='black'))
    ax.text(5, bar_y + 0.25, 'STRONG', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    ax.text(5, bar_y - 0.2, 'Matched', ha='center', fontsize=9)
    
    # Mismatched
    ax.add_patch(Rectangle((8, bar_y), 0.3, 0.5, facecolor='red', edgecolor='black'))
    ax.text(8.15, bar_y + 0.25, '~0', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    ax.text(8.15, bar_y - 0.2, 'Mismatched', ha='center', fontsize=9)
    
    fig.suptitle('EXPERIMENTAL SEQUENCE: Phase 1 Protocol',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


def plot_decision_tree(save_path=None):
    """Create outcome decision tree."""
    
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.axis('off')
    
    # Root node
    root = FancyBboxPatch((5, 7.5), 4, 1, boxstyle="round,pad=0.1",
                           facecolor='#E0E0E0', edgecolor='black', linewidth=2)
    ax.add_patch(root)
    ax.text(7, 8, 'RUN EXPERIMENT', ha='center', va='center',
            fontsize=12, fontweight='bold')
    
    # First branch: Matched result
    ax.plot([7, 7], [7.5, 6.5], 'k-', lw=2)
    ax.plot([7, 4], [6.5, 5.5], 'k-', lw=2)
    ax.plot([7, 10], [6.5, 5.5], 'k-', lw=2)
    
    ax.text(5, 6.7, 'Matched\nSignal?', fontsize=10, ha='center')
    
    # No matched signal
    no_match = FancyBboxPatch((2, 4.5), 4, 1, boxstyle="round,pad=0.1",
                               facecolor='#FFB6C1', edgecolor='red', linewidth=2)
    ax.add_patch(no_match)
    ax.text(4, 5, 'NO SIGNAL', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkred')
    ax.text(2, 5.3, '❌', fontsize=14)
    
    # Yes matched signal
    yes_match = FancyBboxPatch((8, 4.5), 4, 1, boxstyle="round,pad=0.1",
                                facecolor='#90EE90', edgecolor='green', linewidth=2)
    ax.add_patch(yes_match)
    ax.text(10, 5, 'SIGNAL DETECTED', ha='center', va='center',
            fontsize=11, fontweight='bold', color='darkgreen')
    ax.text(8.2, 5.3, '✓', fontsize=14, color='green')
    
    # Second branch from yes: Mismatched result
    ax.plot([10, 10], [4.5, 3.5], 'k-', lw=2)
    ax.plot([10, 7], [3.5, 2.5], 'k-', lw=2)
    ax.plot([10, 13], [3.5, 2.5], 'k-', lw=2)
    
    ax.text(11.5, 3.7, 'Mismatched\nSignal?', fontsize=10, ha='center')
    
    # Yes mismatched (BAD - classical leakage)
    yes_mismatch = FancyBboxPatch((11, 1.5), 2.5, 1, boxstyle="round,pad=0.1",
                                   facecolor='#FF6347', edgecolor='darkred', linewidth=2)
    ax.add_patch(yes_mismatch)
    ax.text(12.25, 2, 'LEAKAGE', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    
    # No mismatched (GOOD - topology works!)
    no_mismatch = FancyBboxPatch((5, 1.5), 3.5, 1, boxstyle="round,pad=0.1",
                                  facecolor='#32CD32', edgecolor='darkgreen', linewidth=2)
    ax.add_patch(no_mismatch)
    ax.text(6.75, 2, 'SUCCESS!', ha='center', va='center',
            fontsize=12, fontweight='bold', color='white')
    
    # Outcomes
    # Null result
    null_box = FancyBboxPatch((1.5, 2.5), 5, 1.2, boxstyle="round,pad=0.05",
                               facecolor='#FFF0F0', edgecolor='gray', linewidth=1)
    ax.add_patch(null_box)
    ax.text(4, 3.3, 'NULL RESULT', ha='center', fontsize=10, fontweight='bold', color='gray')
    ax.text(4, 2.85, 'g/m too weak OR mechanism wrong', ha='center', fontsize=8, color='gray')
    ax.plot([4, 4], [4.5, 3.7], 'k-', lw=2)
    
    # Leakage result
    leak_box = FancyBboxPatch((10.5, 0.2), 3, 1.2, boxstyle="round,pad=0.05",
                               facecolor='#FFF0F0', edgecolor='gray', linewidth=1)
    ax.add_patch(leak_box)
    ax.text(12, 1, 'CLASSICAL LEAKAGE', ha='center', fontsize=10, fontweight='bold', color='gray')
    ax.text(12, 0.55, 'Improve shielding or abandon', ha='center', fontsize=8, color='gray')
    ax.plot([12.25, 12.25], [1.5, 1.4], 'k-', lw=2)
    
    # Success result
    success_box = FancyBboxPatch((4.5, 0.2), 4, 1.2, boxstyle="round,pad=0.05",
                                  facecolor='#F0FFF0', edgecolor='green', linewidth=1)
    ax.add_patch(success_box)
    ax.text(6.5, 1, 'HYPOTHESIS SUPPORTED', ha='center', fontsize=10, 
            fontweight='bold', color='darkgreen')
    ax.text(6.5, 0.55, '→ Proceed to PHASE 2', ha='center', fontsize=9, color='darkgreen')
    ax.plot([6.75, 6.75], [1.5, 1.4], 'k-', lw=2)
    
    fig.suptitle('OUTCOME DECISION TREE\n'
                 'How to Interpret Results',
                 fontsize=14, fontweight='bold', y=0.98)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


def plot_protocol_summary(save_path=None):
    """Create single-page protocol summary."""
    
    fig = plt.figure(figsize=(16, 12))
    gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.25)
    
    # Panel 1: Success criteria
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    
    criteria_text = """
    SUCCESS CRITERIA
    ════════════════════════════════════════
    
    ✓ MATCHED CONDITION
      • Cross-correlation C(0) significant
      • p-value < 10⁻⁵ (≥ 4.4σ)
    
    ✓ CONTROL CONDITION  
      • Mismatched C(0) ≈ 0
      • p-value > 0.05 (consistent with null)
    
    ✓ SELECTIVITY
      • Signal ratio > 5×
      • Clear topology discrimination
    
    ✓ REPRODUCIBILITY
      • 3+ independent runs agree
    
    ════════════════════════════════════════
    ALL FOUR required for SUCCESS
    """
    
    ax1.text(0.05, 0.95, criteria_text, transform=ax1.transAxes,
             fontsize=11, fontfamily='monospace', va='top',
             bbox=dict(boxstyle='round', facecolor='#E8F8E8', 
                       edgecolor='green', linewidth=2))
    ax1.set_title('Success Criteria', fontweight='bold', fontsize=13)
    
    # Panel 2: Kill conditions
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.axis('off')
    
    kill_text = """
    KILL CONDITIONS (Theory Falsified)
    ════════════════════════════════════════
    
    ✗ CLASSICAL LEAKAGE
      • Equal signal in matched AND mismatched
      • Indicates EM crosstalk, not topology
    
    ✗ NULL RESULT
      • No signal in either condition
      • g/m < 10⁻⁹ rad⁻¹ after max integration
    
    ✗ NON-REPRODUCIBLE
      • Results vary between runs
      • Indicates systematic error
    
    ════════════════════════════════════════
    ANY ONE of these = FAILURE
    """
    
    ax2.text(0.05, 0.95, kill_text, transform=ax2.transAxes,
             fontsize=11, fontfamily='monospace', va='top',
             bbox=dict(boxstyle='round', facecolor='#FFE8E8',
                       edgecolor='red', linewidth=2))
    ax2.set_title('Kill Conditions', fontweight='bold', fontsize=13)
    
    # Panel 3: Timeline
    ax3 = fig.add_subplot(gs[1, 0])
    
    months = ['M1-3', 'M4-6', 'M7-9', 'M10-12']
    phases = ['Design &\nProcurement', 'Integration &\nCalibration', 
              'Data\nCollection', 'Analysis &\nPublication']
    colors = ['#FFE4B5', '#90EE90', '#87CEEB', '#DDA0DD']
    
    bars = ax3.barh(months, [3, 3, 3, 3], color=colors, edgecolor='black', linewidth=2)
    
    for bar, phase in zip(bars, phases):
        ax3.text(bar.get_width()/2, bar.get_y() + bar.get_height()/2,
                 phase, ha='center', va='center', fontsize=10, fontweight='bold')
    
    ax3.set_xlabel('Duration (months)', fontsize=11)
    ax3.set_title('Timeline (12 Months Total)', fontweight='bold', fontsize=13)
    ax3.set_xlim(0, 4)
    ax3.invert_yaxis()
    
    # Panel 4: Key parameters
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.axis('off')
    
    params_text = """
    KEY PARAMETERS
    ════════════════════════════════════════
    
    PHYSICAL CONSTANTS
    • α = 1/137 (fine structure)
    • g = αC ≈ 0.022 (for C=3)
    
    EXPERIMENTAL SETTINGS
    • T < 20 mK (cryostat)
    • T₂* > 50 μs (qubit coherence)
    • ω_c/2π ~ 6-8 GHz (cavity)
    • n = 10³ - 10⁶ (photon number)
    
    SIGNAL ESTIMATES
    • χ ~ 1 Hz to 1 MHz
    • Depends on unknown g/m
    • Integration: seconds to days
    
    TOPOLOGY
    • Matched: C = 3 ↔ C = 3
    • Control: C = 2 ↔ C = 3
    
    ════════════════════════════════════════
    """
    
    ax4.text(0.05, 0.95, params_text, transform=ax4.transAxes,
             fontsize=10, fontfamily='monospace', va='top',
             bbox=dict(boxstyle='round', facecolor='#F0F8FF',
                       edgecolor='navy', linewidth=2))
    ax4.set_title('Key Parameters', fontweight='bold', fontsize=13)
    
    fig.suptitle('PHASE 1 TABLETOP PROTOCOL: SUMMARY\n'
                 'Topology-Mediated Coherence Field Coupling Test',
                 fontsize=15, fontweight='bold', y=0.98)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
        print(f"Saved: {save_path}")
    
    plt.close()


def main():
    print("\n" + "=" * 60)
    print("  PHASE 1 PROTOCOL VISUALIZATIONS")
    print("=" * 60)
    
    import os
    os.makedirs('/home/claude/sim_outputs', exist_ok=True)
    
    print("\n[1/4] Experimental schematic...")
    plot_experimental_schematic('/home/claude/sim_outputs/protocol_schematic.png')
    
    print("[2/4] Sequence diagram...")
    plot_sequence_diagram('/home/claude/sim_outputs/protocol_sequence.png')
    
    print("[3/4] Decision tree...")
    plot_decision_tree('/home/claude/sim_outputs/protocol_decision_tree.png')
    
    print("[4/4] Protocol summary...")
    plot_protocol_summary('/home/claude/sim_outputs/protocol_summary.png')
    
    print("\n" + "=" * 60)
    print("  OUTPUT FILES")
    print("=" * 60)
    print("  • protocol_schematic.png")
    print("  • protocol_sequence.png")
    print("  • protocol_decision_tree.png")
    print("  • protocol_summary.png")
    print("=" * 60)


if __name__ == "__main__":
    main()
