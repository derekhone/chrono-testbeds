"""
CHRONO-1 — temporal nonclassicality witness.

Turns the measured Leggett-Garg K3 statistic into a bounded, honest witness
block that is bound into the ProofRecord (see proofrecord.py).

HONESTY BOUNDARY (carried verbatim into every artifact):
  * This is a single-system TEMPORAL test. The Leggett-Garg inequality assumes
    NON-INVASIVE MEASURABILITY (NIM) — that a macrorealist system can be
    measured without disturbing it. A projective qubit measurement is invasive,
    so a determined macrorealist can attribute any observed K3 > 1 to
    measurement disturbance ("clumsiness loophole"). This is therefore a
    Leggett-Garg violation UNDER THE STATED ASSUMPTIONS, *not* a loophole-free
    refutation of macrorealism, and NOT device-independent certified randomness.
  * Defensible claim: "observed temporal correlations violating the macrorealist
    bound K3 <= 1 on hardware, under the non-invasive-measurability assumption,
    cryptographically bound into the authorization record."
"""
from __future__ import annotations

from typing import Dict

import chrono


def build_witness(K3: float, correlators: Dict[str, float], shots: int,
                  sigma: float) -> Dict:
    excess = K3 - chrono.MACROREALIST_BOUND
    n_sigma = (excess / sigma) if sigma > 0 else 0.0
    witness = {
        "witness_type": "leggett_garg_temporal_K3",
        "K3": K3,
        "correlators": correlators,
        "theta_radians": chrono.THETA,
        "macrorealist_bound": chrono.MACROREALIST_BOUND,
        "luders_quantum_bound": chrono.LUDERS_QUANTUM_BOUND,
        "ideal_K3": chrono.IDEAL_K3,
        "shots_per_correlator": shots,
        "sigma_K3": sigma,
        "excess_over_bound": excess,
        "n_sigma": n_sigma,
        "violation": bool(K3 > chrono.MACROREALIST_BOUND),
        "significant_violation_3sigma": bool(excess > 3 * sigma),
        # Explicit, non-negotiable honesty flags.
        "loopholes_open": {
            "non_invasive_measurability": True,
            "clumsiness": True,
            "single_system": True,
        },
        "device_independent": False,
        "certified_randomness": False,
        "claim": (
            "Observed temporal correlations violating the macrorealist bound "
            "K3<=1 on quantum hardware, under the non-invasive-measurability "
            "assumption. NOT a loophole-free refutation of macrorealism; NOT "
            "device-independent certified randomness."
        ),
    }
    return witness
