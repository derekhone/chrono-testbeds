"""
CHRONO-1 — pre-lock mock tests (no hardware, no network).

Validates the physics engine, the witness logic, the ProofRecord provenance
chain, and its tamper-evidence, using synthetic ideal counts.
"""
from __future__ import annotations

import math
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import chrono
import temporal_witness as tw
import proofrecord as pr


def _ideal_counts(correlator_value: float, shots: int = 100000):
    """Build 2-bit counts with a given <Q_early Q_late> correlator and balanced
    marginals. p(same) - p(diff) = C  =>  p(same) = (1+C)/2.
    Keys are 'c[1]c[0]' == 'late early'.
    """
    p_same = (1.0 + correlator_value) / 2.0
    n_same = int(round(p_same * shots))
    n_diff = shots - n_same
    return {
        "00": n_same // 2, "11": n_same - n_same // 2,   # same outcome
        "01": n_diff // 2, "10": n_diff - n_diff // 2,   # differing outcome
    }


def test_ideal_correlators():
    for target in (0.5, -0.5, 1.0, 0.0):
        c = chrono.correlator_from_counts(_ideal_counts(target))
        assert abs(c - target) < 0.02, (target, c)


def test_ideal_K3_is_1_5():
    counts = [_ideal_counts(chrono.IDEAL_C12), _ideal_counts(chrono.IDEAL_C23),
              _ideal_counts(chrono.IDEAL_C13)]
    K3, corr = chrono.compute_K3(counts)
    assert abs(K3 - 1.5) < 0.02, (K3, corr)


def test_theta_is_60_degrees():
    assert abs(chrono.THETA - math.pi / 3) < 1e-12
    assert abs(chrono.IDEAL_C12 - 0.5) < 1e-9
    assert abs(chrono.IDEAL_C13 + 0.5) < 1e-9


def test_witness_flags_violation():
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(-0.5)]
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, 100000)
    w = tw.build_witness(K3, corr, 100000, sigma)
    assert w["violation"] is True
    assert w["significant_violation_3sigma"] is True
    assert w["device_independent"] is False
    assert w["certified_randomness"] is False
    assert w["loopholes_open"]["non_invasive_measurability"] is True


def test_witness_no_violation_when_macrorealist():
    # K3 = 1.0 exactly (e.g. C12=C23=0.5, C13=0.0) -> no violation
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(0.0)]
    K3, corr = chrono.compute_K3(counts)
    assert abs(K3 - 1.0) < 0.02
    sigma = chrono.shot_noise_sigma_K3(corr, 100000)
    w = tw.build_witness(K3, corr, 100000, sigma)
    assert w["violation"] is False


def test_proofrecord_roundtrip():
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(-0.5)]
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, 2000)
    w = tw.build_witness(K3, corr, 2000, sigma)
    cal = {"backend": "mock", "readout_error": 0.01}
    rec = pr.build_proofrecord(counts, "job_mock", "ibm_fez", "open-instance",
                               cal, w, "chrono-1-primary", "2026-07-18T00:00:00Z")
    assert pr.verify_record_hash(rec)
    assert pr.verify_chrono_nonce(rec, counts, cal, w)


def test_tamper_witness_breaks_nonce():
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(-0.5)]
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, 2000)
    w = tw.build_witness(K3, corr, 2000, sigma)
    cal = {"backend": "mock"}
    rec = pr.build_proofrecord(counts, "job_mock", "ibm_fez", "open-instance",
                               cal, w, "chrono-1-primary", "2026-07-18T00:00:00Z")
    forged = dict(w)
    forged["K3"] = 1.2  # alter the claimed statistic
    assert not pr.verify_chrono_nonce(rec, counts, cal, forged)


def test_tamper_counts_breaks_nonce():
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(-0.5)]
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, 2000)
    w = tw.build_witness(K3, corr, 2000, sigma)
    cal = {"backend": "mock"}
    rec = pr.build_proofrecord(counts, "job_mock", "ibm_fez", "open-instance",
                               cal, w, "chrono-1-primary", "2026-07-18T00:00:00Z")
    forged_counts = [dict(counts[0]), counts[1], counts[2]]
    forged_counts[0]["00"] = forged_counts[0].get("00", 0) + 5000
    assert not pr.verify_chrono_nonce(rec, forged_counts, cal, w)


def test_record_hash_detects_field_edit():
    counts = [_ideal_counts(0.5), _ideal_counts(0.5), _ideal_counts(-0.5)]
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, 2000)
    w = tw.build_witness(K3, corr, 2000, sigma)
    cal = {"backend": "mock"}
    rec = pr.build_proofrecord(counts, "job_mock", "ibm_fez", "open-instance",
                               cal, w, "chrono-1-primary", "2026-07-18T00:00:00Z")
    rec["backend"] = "ibm_marrakesh"  # edit a covered field
    assert not pr.verify_record_hash(rec)


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    for fn in fns:
        fn()
        print(f"PASS {fn.__name__}")
        passed += 1
    print(f"\n{passed}/{len(fns)} tests passed")
