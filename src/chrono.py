"""
CHRONO-1 — Leggett-Garg temporal-correlation engine.

We test the three-time Leggett-Garg inequality (LGI):

        K3 = C12 + C23 - C13

on a single qubit precessing under R_y(theta) between measurement times.

    - Macrorealism (a system has a definite value at all times, and that value
      can in principle be read non-invasively) bounds:  K3 <= 1.
    - Quantum mechanics allows up to the Luders bound:  K3 = 1.5.

For a qubit with equal time steps, the two-time correlators depend only on the
elapsed rotation:  C(t_i, t_j) = cos( (j - i) * theta ).  Choosing theta = pi/3
gives C12 = C23 = cos(60 deg) = +0.5 and C13 = cos(120 deg) = -0.5, hence the
maximal quantum value K3 = 0.5 + 0.5 - (-0.5) = 1.5.

Each correlator is measured in a SEPARATE circuit (pairwise), using mid-circuit
measurement so the value at the earlier time is recorded before the system
evolves to the later time:

    C12 : measure(t1) -> R_y(theta) -> measure(t2)
    C23 : R_y(theta) -> measure(t2) -> R_y(theta) -> measure(t3)
    C13 : measure(t1) -> R_y(2*theta) -> measure(t3)

Each circuit writes two bits into a single 2-bit classical register 'c'
(c[0] = earlier measurement, c[1] = later measurement).  A dichotomic outcome
Q = +1 for bit 0 and Q = -1 for bit 1; the correlator is the shot-average of the
product of the two signed outcomes.

Novelty vs. prior RF series:
    ARK       tested the authorization *boundary*.
    WITNESS   bound provenance of a superposition-sourced nonce.
    BELLWETHER witnessed *spatial* nonclassicality (CHSH Bell violation, S>2).
    CHRONO    witnesses *temporal* nonclassicality (Leggett-Garg K3>1): the
              authorization value had no definite pre-measurement (pre-execution)
              history under the non-invasive-measurability assumption.
"""
from __future__ import annotations

import math
from typing import Dict, List, Tuple

THETA = math.pi / 3.0            # 60 degrees -> maximal LGI violation
MACROREALIST_BOUND = 1.0
LUDERS_QUANTUM_BOUND = 1.5

# Ideal (noiseless) predictions, for validation.
IDEAL_C12 = math.cos(THETA)      # +0.5
IDEAL_C23 = math.cos(THETA)      # +0.5
IDEAL_C13 = math.cos(2 * THETA)  # -0.5
IDEAL_K3 = IDEAL_C12 + IDEAL_C23 - IDEAL_C13   # 1.5

CORRELATOR_ORDER = ["C12", "C23", "C13"]


def build_circuits():
    """Return [qc_C12, qc_C23, qc_C13] as qiskit QuantumCircuits.

    Each uses 1 qubit and a single 2-bit classical register named 'c':
        c[0] = earlier-time outcome, c[1] = later-time outcome.
    """
    from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

    def _new():
        q = QuantumRegister(1, "q")
        c = ClassicalRegister(2, "c")
        return QuantumCircuit(q, c), q, c

    # C12 : measure(t1) -> R_y(theta) -> measure(t2)
    qc12, q, c = _new()
    qc12.measure(q[0], c[0])
    qc12.ry(THETA, q[0])
    qc12.measure(q[0], c[1])

    # C23 : R_y(theta) -> measure(t2) -> R_y(theta) -> measure(t3)
    qc23, q, c = _new()
    qc23.ry(THETA, q[0])
    qc23.measure(q[0], c[0])
    qc23.ry(THETA, q[0])
    qc23.measure(q[0], c[1])

    # C13 : measure(t1) -> R_y(2*theta) -> measure(t3)
    qc13, q, c = _new()
    qc13.measure(q[0], c[0])
    qc13.ry(2 * THETA, q[0])
    qc13.measure(q[0], c[1])

    return [qc12, qc23, qc13]


def _sign(bitchar: str) -> int:
    """Dichotomic map: '0' -> +1, '1' -> -1."""
    return 1 if bitchar == "0" else -1


def correlator_from_counts(counts: Dict[str, int]) -> float:
    """Shot-average of the product of the two signed outcomes.

    Counts keys are 2-character strings for register 'c' (qiskit orders them
    c[1]c[0], MSB left). The product of the two signs is order-independent.
    Whitespace/other registers are not expected; keys are stripped of spaces.
    """
    total = 0
    acc = 0.0
    for key, n in counts.items():
        k = key.replace(" ", "")
        if len(k) < 2:
            continue
        b_late, b_early = k[0], k[1]
        acc += n * _sign(b_early) * _sign(b_late)
        total += n
    if total == 0:
        return 0.0
    return acc / total


def compute_K3(counts_list: List[Dict[str, int]]) -> Tuple[float, Dict[str, float]]:
    """counts_list is [counts_C12, counts_C23, counts_C13]; returns (K3, {C..})."""
    c12 = correlator_from_counts(counts_list[0])
    c23 = correlator_from_counts(counts_list[1])
    c13 = correlator_from_counts(counts_list[2])
    K3 = c12 + c23 - c13
    return K3, {"C12": c12, "C23": c23, "C13": c13}


def shot_noise_sigma_K3(correlators: Dict[str, float], shots: int) -> float:
    """Propagated 1-sigma statistical uncertainty on K3.

    Var(C) = (1 - C^2)/N for a dichotomic mean; K3 = C12 + C23 - C13, so the
    variances add (signs do not affect variance).
    """
    var = 0.0
    for name in ("C12", "C23", "C13"):
        c = correlators.get(name, 0.0)
        var += max(0.0, (1.0 - c * c)) / max(1, shots)
    return math.sqrt(var)
