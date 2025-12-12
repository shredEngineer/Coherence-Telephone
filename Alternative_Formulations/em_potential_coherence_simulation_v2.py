#!/usr/bin/env python3
"""
EM 4-Potential Coherence Simulation v2 (Enhanced)
--------------------------------------------------
Improvements over v1:
  • Energy-like functional (avoids plane-wave saturation)
  • Bit Error Rate (BER) calculation for communication metrics
  • Coupling speed comparison (light-speed vs instant vs intermediate)
  • Noise robustness testing
  • Professional framing (no overclaiming)

Notes:
  - This is a *toy model* to compare coherence functionals and signal-processing behavior.
  - It does NOT enforce Maxwell propagation between nodes unless you enable coupling.
  - The "instant coupling" scenario is for hypothesis testing only, not a claim of reality.
"""

from __future__ import annotations

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import simpson
from pathlib import Path
from dataclasses import dataclass

C_LIGHT = 299_792_458.0  # m/s


@dataclass
class EMPotentialCoherence:
    """
    Candidate coherence functionals built from a vector potential A(x,t)
    and its time history. In practice, A is gauge-dependent; for serious
    work, prefer gauge-invariant constructs (e.g., via F_{μν}). Here we
    keep it simple and explicit.
    """
    alpha: float = 2.0
    beta: float = 1.0
    tau: float = 0.05  # memory window (s)

    def _memory_samples(self, dt: float) -> int:
        return max(1, int(self.tau / dt))

    def gradient_based(self, A_field: np.ndarray, dx: float, dt: float) -> np.ndarray:
        """
        C = exp(-alpha * ∫ |∇A|^2 dt)   (1D: ∇A -> ∂A/∂x)
        
        Note: This is NOT gauge-invariant. For proper formulation,
        use field strength tensor F_μν.
        """
        dA_dx = np.gradient(A_field, dx, axis=1)
        integrand = dA_dx ** 2
        n_mem = self._memory_samples(dt)

        C = np.zeros_like(A_field, dtype=float)
        for t in range(A_field.shape[0]):
            t0 = max(0, t - n_mem)
            integral = simpson(integrand[t0:t + 1], dx=dt, axis=0)
            C[t] = np.exp(-self.alpha * integral)
        return np.clip(C, 0.0, 1.0)

    def energy_like(self, A_field: np.ndarray, dx: float, dt: float) -> np.ndarray:
        """
        Energy-like functional that avoids the "plane-wave invariant ~ 0" trap:
          E ≈ -∂A/∂t (proxy), B ≈ ∂A/∂x (proxy)  ->  u ~ E^2 + B^2 >= 0
        C = exp(-beta * ∫ ( (∂t A)^2 + (∂x A)^2 ) dt )
        
        Note: This is NOT the actual EM energy density (which would be 
        ε₀E²/2 + B²/(2μ₀) in proper units). It's a proxy that captures 
        field dynamics while staying always-positive. For gauge-invariant 
        formulation, see field_strength_based method using F_μν.
        """
        dA_dt = np.gradient(A_field, dt, axis=0)
        dA_dx = np.gradient(A_field, dx, axis=1)
        integrand = (dA_dt ** 2) + (dA_dx ** 2)
        n_mem = self._memory_samples(dt)

        C = np.zeros_like(A_field, dtype=float)
        for t in range(A_field.shape[0]):
            t0 = max(0, t - n_mem)
            integral = simpson(integrand[t0:t + 1], dx=dt, axis=0)
            C[t] = np.exp(-self.beta * integral)
        return np.clip(C, 0.0, 1.0)

    def phase_wilson_line(self, A_field: np.ndarray, dt: float) -> np.ndarray:
        """
        Phase / Wilson-line inspired:
          φ ~ ∫ A dt  =>  C ~ |∫ exp(i φ) dt| / window
        """
        n_mem = self._memory_samples(dt)
        # Accumulated phase (toy; scalar potential omitted)
        phase = np.cumsum(A_field, axis=0) * dt
        phase_factor = np.exp(1j * phase)

        C = np.zeros_like(A_field, dtype=float)
        for t in range(A_field.shape[0]):
            t0 = max(0, t - n_mem)
            integral = simpson(phase_factor[t0:t + 1], dx=dt, axis=0)
            window = max(dt, (t - t0 + 1) * dt)
            C[t] = np.abs(integral) / window

        Cmax = np.maximum(1e-12, np.max(C, axis=0, keepdims=True))
        return np.clip(C / Cmax, 0.0, 1.0)

    def hybrid(self, A_field: np.ndarray, dx: float, dt: float) -> np.ndarray:
        """
        Hybrid = geometric mean of (gradient) and (energy-like)
        """
        Cg = self.gradient_based(A_field, dx, dt)
        Ce = self.energy_like(A_field, dx, dt)
        return np.sqrt(np.clip(Cg * Ce, 0.0, 1.0))


def entropy_coherence(A_field: np.ndarray, dx: float, dt: float, tau: float = 0.05, gamma: float = 1.0) -> np.ndarray:
    """
    Baseline: entropy-ish proxy based on local variance over a time window.
    (Kept mainly for comparison; not a "physical" entropy field.)
    """
    n_mem = max(1, int(tau / dt))
    C = np.zeros_like(A_field, dtype=float)

    for t in range(A_field.shape[0]):
        t0 = max(0, t - n_mem)
        window = A_field[t0:t + 1]
        var = np.var(window, axis=0)
        C[t] = np.exp(-gamma * var)

    Cmax = np.maximum(1e-12, np.max(C, axis=0, keepdims=True))
    return np.clip(C / Cmax, 0.0, 1.0)


def _bits_to_levels(bits: list[int]) -> np.ndarray:
    """Map {0,1} -> {-1,+1} for amplitude modulation."""
    return np.array([1 if b else -1 for b in bits], dtype=float)


def generate_em_field(mode: str, x: np.ndarray, t: np.ndarray, params: dict) -> tuple[np.ndarray, dict]:
    """
    Returns (A_field, meta) where meta may include modulation signals, etc.
    """
    X, T = np.meshgrid(x, t)
    A0 = float(params.get("A0", 1.0))
    k = float(params.get("k", 2 * np.pi * 3))
    omega = float(params.get("omega", 2 * np.pi * 5))

    rng = np.random.default_rng(int(params.get("seed", 1234)))

    if mode == "smooth":
        A = A0 * np.sin(k * X - omega * T)
        return A, {}

    if mode == "turbulent":
        A = A0 * np.sin(k * X - omega * T)
        noise = 0.4 * rng.normal(size=A.shape)
        kernel = np.ones(5) / 5
        noise = np.apply_along_axis(lambda v: np.convolve(v, kernel, mode="same"), 1, noise)
        return A + noise, {}

    if mode == "modulated":
        bits = params.get("bit_pattern", [1, 0, 1, 1, 0])
        levels = _bits_to_levels(bits)
        bit_dur = max(1, len(t) // len(bits))
        envelope = np.zeros_like(t, dtype=float)
        for i, lvl in enumerate(levels):
            envelope[i * bit_dur: min((i + 1) * bit_dur, len(t))] = lvl
        A = A0 * (1.0 + 0.25 * envelope[:, None]) * np.sin(k * X - omega * T)
        return A, {"bit_pattern": bits, "bit_duration": bit_dur, "envelope": envelope}

    if mode == "two_node":
        x_A = float(params.get("x_A", x[len(x)//4]))
        x_B = float(params.get("x_B", x[3*len(x)//4]))

        bits = params.get("bit_pattern", [1, 0, 1, 1, 0, 1, 0, 0, 1, 1])
        levels = _bits_to_levels(bits)
        bit_dur = max(1, len(t) // len(bits))

        A = A0 * np.sin(k * X - omega * T)

        envelope = np.zeros_like(t, dtype=float)
        for i, lvl in enumerate(levels):
            envelope[i * bit_dur: min((i + 1) * bit_dur, len(t))] = lvl

        sigma = float(params.get("sigma", 0.02))
        tx_profile = np.exp(-((X - x_A) ** 2) / (2 * sigma ** 2))
        A += float(params.get("tx_strength", 0.75)) * (envelope[:, None] * tx_profile)

        couple = bool(params.get("enable_coupling", True))
        if couple:
            v = float(params.get("coupling_speed", C_LIGHT))
            delay = 0.0 if not np.isfinite(v) else (abs(x_B - x_A) / v)
            delay_steps = int(round(delay / (t[1] - t[0])))

            env_delayed = np.roll(envelope, delay_steps)
            if delay_steps > 0:
                env_delayed[:delay_steps] = 0.0

            rx_profile = np.exp(-((X - x_B) ** 2) / (2 * sigma ** 2))
            A += float(params.get("rx_strength", 0.35)) * (env_delayed[:, None] * rx_profile)

        meta = {
            "x_A": x_A, "x_B": x_B,
            "bit_pattern": bits,
            "bit_duration": bit_dur,
            "envelope": envelope,
            "enable_coupling": couple,
            "coupling_speed": float(params.get("coupling_speed", C_LIGHT)),
        }
        return A, meta

    raise ValueError(f"Unknown mode: {mode}")


def decode_bits_from_trace(trace: np.ndarray, bit_pattern: list[int], bit_duration: int, 
                           trim: int = 0, noise_level: float = 0.0) -> dict:
    """
    Decode bits from a 1D trace by window-averaging and thresholding.
    
    Parameters:
    -----------
    trace : array
        1D coherence signal
    bit_pattern : list
        True bit pattern for comparison
    bit_duration : int
        Samples per bit
    trim : int
        Skip this many samples at start of each bit window (settling time)
    noise_level : float
        Add Gaussian noise to trace before decoding (for robustness testing)
    """
    # Add noise if specified
    if noise_level > 0:
        rng = np.random.default_rng(42)
        trace = trace + rng.normal(0, noise_level, trace.shape)
    
    nbits = len(bit_pattern)
    y_true = np.array(bit_pattern, dtype=int)

    feats = []
    for i in range(nbits):
        s = i * bit_duration + trim
        e = min((i + 1) * bit_duration, len(trace))
        feats.append(float(np.mean(trace[s:e])) if s < e else np.nan)

    feats = np.array(feats, dtype=float)
    valid = np.isfinite(feats)
    feats_v = feats[valid]
    y_true_v = y_true[valid]

    if np.any(y_true_v == 0) and np.any(y_true_v == 1):
        m0 = float(np.mean(feats_v[y_true_v == 0]))
        m1 = float(np.mean(feats_v[y_true_v == 1]))
        threshold = 0.5 * (m0 + m1)
    else:
        threshold = float(np.nanmedian(feats_v))

    y_pred_v = (feats_v > threshold).astype(int)
    errors = int(np.sum(y_pred_v != y_true_v))
    ber = errors / max(1, len(y_true_v))
    acc = 1.0 - ber

    y_pred = np.full_like(y_true, fill_value=-1)
    y_pred[valid] = y_pred_v

    return {
        "features": feats,
        "threshold": threshold,
        "y_true": y_true,
        "y_pred": y_pred,
        "ber": ber,
        "accuracy": acc,
        "errors": errors,
        "nbits_valid": int(len(y_true_v)),
        "noise_level": noise_level,
    }


def run_comparison(outputs: Path) -> plt.Figure:
    print("\n" + "=" * 60)
    print("Coherence Functional Comparison v2")
    print("=" * 60)

    x = np.linspace(0, 1, 200)
    t = np.linspace(0, 2, 400)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    em = EMPotentialCoherence(alpha=2.0, beta=1.0, tau=0.05)

    scenarios = [
        ("smooth", {}),
        ("turbulent", {"seed": 42}),
        ("modulated", {"bit_pattern": [1, 0, 1, 1, 0]}),
    ]

    fig, axes = plt.subplots(len(scenarios), 4, figsize=(18, 4.5 * len(scenarios)))
    if len(scenarios) == 1:
        axes = axes[None, :]

    for r, (mode, params) in enumerate(scenarios):
        A, _ = generate_em_field(mode, x, t, params)

        Cg = em.gradient_based(A, dx, dt)
        Ce = em.energy_like(A, dx, dt)
        Cent = entropy_coherence(A, dx, dt, tau=0.05, gamma=1.0)

        mats = [
            (A, "A(x,t)"),
            (Cg, "C_grad"),
            (Ce, "C_energy"),
            (Cent, "C_entropy"),
        ]

        for c, (M, title) in enumerate(mats):
            ax = axes[r, c]
            im = ax.imshow(M, aspect="auto", extent=[x[0], x[-1], t[-1], t[0]])
            ax.set_title(f"{mode}: {title}")
            ax.set_xlabel("x")
            ax.set_ylabel("t")
            plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    fig.tight_layout()
    out = outputs / "em_coherence_comparison_v2.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print(f"Saved: {out}")
    return fig


def run_coupling_speed_comparison(outputs: Path) -> plt.Figure:
    """
    Compare BER for different coupling scenarios.
    
    This demonstrates what advantage (if any) a coherence field would provide
    compared to standard light-speed propagation.
    """
    print("\n" + "=" * 60)
    print("Coupling Speed Comparison")
    print("Testing: Light-speed vs Instant vs Intermediate")
    print("=" * 60)

    x = np.linspace(0, 1, 220)
    t = np.linspace(0, 2, 500)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    x_A = x[55]
    x_B = x[165]
    separation = x_B - x_A

    base_params = {
        "x_A": float(x_A),
        "x_B": float(x_B),
        "bit_pattern": [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        "A0": 1.0,
        "sigma": 0.02,
        "tx_strength": 0.75,
        "rx_strength": 0.35,
        "enable_coupling": True,
        "seed": 1234,
    }

    speeds = [
        ("Light-speed (c)", C_LIGHT, 'blue'),
        ("Instant (toy)", np.inf, 'red'),
        ("Half light-speed", C_LIGHT/2, 'green'),
        ("Double light-speed", C_LIGHT*2, 'orange'),
    ]

    em = EMPotentialCoherence(alpha=2.0, beta=1.0, tau=0.05)
    
    results = []
    
    for name, speed, color in speeds:
        params = {**base_params, "coupling_speed": speed}
        A, meta = generate_em_field("two_node", x, t, params)
        
        C = em.hybrid(A, dx, dt)
        
        idx_B = int(np.argmin(np.abs(x - x_B)))
        C_B = C[:, idx_B]
        
        bit_dur = int(meta["bit_duration"])
        decode = decode_bits_from_trace(C_B, meta["bit_pattern"], bit_dur, 
                                       trim=max(1, bit_dur // 10))
        
        delay = 0.0 if not np.isfinite(speed) else separation / speed
        
        results.append({
            "name": name,
            "speed": speed,
            "color": color,
            "ber": decode["ber"],
            "accuracy": decode["accuracy"],
            "errors": decode["errors"],
            "delay": delay,
        })
        
        print(f"{name:20s} | Speed: {speed:12.2e} m/s | BER: {decode['ber']:.4f} | Acc: {decode['accuracy']:.4f}")

    # Create comparison plots
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # BER comparison
    ax = axes[0]
    names = [r["name"] for r in results]
    bers = [r["ber"] for r in results]
    colors = [r["color"] for r in results]
    
    bars = ax.bar(range(len(names)), bers, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=15, ha='right')
    ax.set_ylabel('Bit Error Rate (BER)')
    ax.set_title('Communication Quality vs Coupling Speed')
    ax.set_ylim([0, max(bers) * 1.2 if max(bers) > 0 else 1.0])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for i, (bar, ber) in enumerate(zip(bars, bers)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{ber:.3f}',
                ha='center', va='bottom', fontsize=9)

    # Accuracy comparison
    ax = axes[1]
    accs = [r["accuracy"] for r in results]
    
    bars = ax.bar(range(len(names)), accs, color=colors, alpha=0.7, edgecolor='black')
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=15, ha='right')
    ax.set_ylabel('Accuracy')
    ax.set_title('Bit Recovery Accuracy vs Coupling Speed')
    ax.set_ylim([0, 1.05])
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add value labels
    for bar, acc in zip(bars, accs):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{acc:.3f}',
                ha='center', va='bottom', fontsize=9)

    fig.tight_layout()
    out = outputs / "coupling_speed_comparison.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"\nSaved: {out}")
    
    light_time = separation / C_LIGHT
    print(f"\nReference: Light travel time for {separation:.3f}m = {light_time:.6e}s")
    print("\nNote: This is a toy model comparison. The 'instant' scenario demonstrates")
    print("what coherence field hypothesis predicts, not a claim it actually works.")
    
    return fig


def run_noise_robustness_test(outputs: Path) -> plt.Figure:
    """
    Test how BER degrades with increasing noise levels.
    
    This shows robustness of different coherence functionals to noise.
    """
    print("\n" + "=" * 60)
    print("Noise Robustness Test")
    print("=" * 60)

    x = np.linspace(0, 1, 220)
    t = np.linspace(0, 2, 500)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    x_A = x[55]
    x_B = x[165]

    params = {
        "x_A": float(x_A),
        "x_B": float(x_B),
        "bit_pattern": [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        "A0": 1.0,
        "sigma": 0.02,
        "tx_strength": 0.75,
        "rx_strength": 0.35,
        "enable_coupling": True,
        "coupling_speed": C_LIGHT,
        "seed": 1234,
    }

    A, meta = generate_em_field("two_node", x, t, params)
    
    em = EMPotentialCoherence(alpha=2.0, beta=1.0, tau=0.05)
    
    # Test different functionals
    functionals = [
        ("Gradient", em.gradient_based),
        ("Energy-like", em.energy_like),
        ("Hybrid", em.hybrid),
    ]
    
    noise_levels = np.linspace(0, 0.3, 10)
    
    results = {name: [] for name, _ in functionals}
    
    idx_B = int(np.argmin(np.abs(x - x_B)))
    bit_dur = int(meta["bit_duration"])
    
    for noise in noise_levels:
        for name, func in functionals:
            C = func(A, dx, dt)
            C_B = C[:, idx_B]
            
            decode = decode_bits_from_trace(C_B, meta["bit_pattern"], bit_dur,
                                           trim=max(1, bit_dur // 10),
                                           noise_level=noise)
            results[name].append(decode["ber"])

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    colors = ['blue', 'red', 'green']
    for (name, _), color in zip(functionals, colors):
        ax.plot(noise_levels, results[name], marker='o', label=name, 
                color=color, linewidth=2, markersize=6)
    
    ax.set_xlabel('Noise Level (σ)', fontsize=12)
    ax.set_ylabel('Bit Error Rate (BER)', fontsize=12)
    ax.set_title('Coherence Functional Robustness to Noise', fontsize=14)
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim([0, 1.05])
    
    fig.tight_layout()
    out = outputs / "noise_robustness_test.png"
    fig.savefig(out, dpi=300, bbox_inches='tight')
    print(f"Saved: {out}")
    
    return fig


def run_two_node_simulation(outputs: Path) -> plt.Figure:
    """Enhanced two-node simulation with BER calculation"""
    print("\n" + "=" * 60)
    print("Two-Node Communication Simulation v2")
    print("=" * 60)

    x = np.linspace(0, 1, 220)
    t = np.linspace(0, 2, 500)
    dx = x[1] - x[0]
    dt = t[1] - t[0]

    x_A = x[55]
    x_B = x[165]

    params = {
        "x_A": float(x_A),
        "x_B": float(x_B),
        "bit_pattern": [1, 0, 1, 1, 0, 1, 0, 0, 1, 1],
        "A0": 1.0,
        "sigma": 0.02,
        "tx_strength": 0.75,
        "enable_coupling": True,
        "coupling_speed": C_LIGHT,
        "rx_strength": 0.35,
        "seed": 1234,
    }

    print(f"Node A: {x_A:.3f} m | Node B: {x_B:.3f} m | Separation: {x_B - x_A:.3f} m")
    print(f"Coupling: {params['enable_coupling']} | Speed: {params['coupling_speed']:.2e} m/s")

    A, meta = generate_em_field("two_node", x, t, params)

    em = EMPotentialCoherence(alpha=2.0, beta=1.0, tau=0.05)
    C = em.hybrid(A, dx, dt)

    idx_A = int(np.argmin(np.abs(x - x_A)))
    idx_B = int(np.argmin(np.abs(x - x_B)))
    C_A = C[:, idx_A]
    C_B = C[:, idx_B]

    bit_dur = int(meta["bit_duration"])
    decode = decode_bits_from_trace(C_B, meta["bit_pattern"], bit_dur, trim=max(1, bit_dur // 10))

    corr = np.correlate(C_A - np.mean(C_A), C_B - np.mean(C_B), mode="full")
    lags = np.arange(-len(C_A) + 1, len(C_A))
    lag_time = lags * dt
    peak_idx = int(np.argmax(np.abs(corr)))
    peak_lag = float(lag_time[peak_idx])
    peak_corr = float(corr[peak_idx] / (np.max(np.abs(corr)) + 1e-12))

    fig, axes = plt.subplots(3, 2, figsize=(15, 10))

    ax = axes[0, 0]
    im = ax.imshow(A, aspect="auto", cmap="RdBu", extent=[x[0], x[-1], t[-1], t[0]])
    ax.axvline(x_A, color="red", linestyle="--", label="Node A (TX)")
    ax.axvline(x_B, color="blue", linestyle="--", label="Node B (RX)")
    ax.set_title("EM Potential A(x,t)")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("t (s)")
    ax.legend()
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[0, 1]
    im2 = ax.imshow(C, aspect="auto", cmap="viridis", vmin=0, vmax=1, extent=[x[0], x[-1], t[-1], t[0]])
    ax.axvline(x_A, color="red", linestyle="--")
    ax.axvline(x_B, color="blue", linestyle="--")
    ax.set_title("Coherence Field C(x,t) - Hybrid Functional")
    ax.set_xlabel("x (m)")
    ax.set_ylabel("t (s)")
    plt.colorbar(im2, ax=ax, fraction=0.046, pad=0.04)

    ax = axes[1, 0]
    ax.plot(t, C_A, linewidth=2, color='red')
    ax.set_title("Coherence at Node A (Transmitter)")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("C")
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)

    ax = axes[1, 1]
    ax.plot(t, C_B, linewidth=2, color='blue')
    ax.set_title(f"Coherence at Node B (Receiver)\nBER={decode['ber']:.3f}, Accuracy={decode['accuracy']:.3f}")
    ax.set_xlabel("t (s)")
    ax.set_ylabel("C")
    ax.set_ylim([0, 1])
    ax.grid(True, alpha=0.3)

    ax = axes[2, 1]
    feats = decode["features"]
    ax.plot(np.arange(len(feats)), feats, marker="o", linewidth=2, markersize=8)
    ax.axhline(decode["threshold"], linestyle="--", alpha=0.7, color='red', label='Threshold')
    ax.set_title("RX Bit-Window Features (Mean C per Bit)")
    ax.set_xlabel("Bit Index")
    ax.set_ylabel("Feature Value")
    ax.legend()
    ax.grid(True, alpha=0.3)

    ax = axes[2, 0]
    ax.plot(lag_time, corr / (np.max(np.abs(corr)) + 1e-12), linewidth=2)
    ax.axvline(0, linestyle="--", alpha=0.5, color='black')
    ax.plot(peak_lag, peak_corr, 'ro', markersize=10, label=f'Peak: {peak_lag:.4f}s')
    ax.set_title("Cross-Correlation C_A ⊗ C_B")
    ax.set_xlabel("Lag (s)")
    ax.set_ylabel("Normalized Correlation")
    ax.legend()
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    out = outputs / "two_node_communication_v2.png"
    fig.savefig(out, dpi=300, bbox_inches="tight")
    print(f"Saved: {out}")

    light_time = (x_B - x_A) / C_LIGHT
    print("\nAnalysis:")
    print(f"  Peak correlation: {peak_corr:.3f}")
    print(f"  Peak lag: {peak_lag:.6f} s")
    print(f"  Light travel time ({x_B-x_A:.3f} m): {light_time:.6e} s")
    print(f"  BER: {decode['ber']:.3f} ({decode['errors']}/{decode['nbits_valid']} errors)")
    print(f"  Accuracy: {decode['accuracy']:.3f}")
    print("\nNote: Correlation lag is NOT a speed measurement; propagation depends on coupling_speed parameter.")

    return fig


def main() -> None:
    outputs = Path("outputs")
    outputs.mkdir(exist_ok=True, parents=True)

    print("=" * 60)
    print("EM 4-Potential Coherence Simulation v2 (Enhanced)")
    print("=" * 60)
    print("\nImprovements:")
    print("  • Energy-like functional (no plane-wave saturation)")
    print("  • BER calculation for communication metrics")
    print("  • Coupling speed comparison")
    print("  • Noise robustness testing")
    print("=" * 60)
    
    run_comparison(outputs)
    run_two_node_simulation(outputs)
    run_coupling_speed_comparison(outputs)
    run_noise_robustness_test(outputs)
    
    print("\n" + "=" * 60)
    print("Simulation Complete - v2")
    print("=" * 60)
    print("\nGenerated files:")
    print("  1. em_coherence_comparison_v2.png")
    print("  2. two_node_communication_v2.png")
    print("  3. coupling_speed_comparison.png")
    print("  4. noise_robustness_test.png")
    print("\nAll outputs in: ./outputs/")


if __name__ == "__main__":
    main()
