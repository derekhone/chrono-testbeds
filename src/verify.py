"""
CHRONO-1 — independent verifier.

Recomputes K3 from the committed raw counts, rebuilds the temporal witness, and
re-checks the ProofRecord's record_hash and chrono_nonce against the raw
artifacts. This is the check a skeptical third party runs: nothing is trusted
except the raw counts file and the record.

Usage: python3 src/verify.py
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import chrono
import temporal_witness as tw
import proofrecord as pr

RESULTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "results"))
RAW = os.path.join(RESULTS, "raw")


def main():
    raw = json.load(open(os.path.join(RAW, "raw_counts.json")))
    counts = raw["counts_by_correlator"]
    meta = json.load(open(os.path.join(RAW, "job_meta.json")))
    cal = json.load(open(os.path.join(RAW, "calibration_snapshot.json")))
    record = json.load(open(os.path.join(RESULTS, "proofrecord.json")))

    shots = meta.get("shots_per_correlator", 2000)
    K3, corr = chrono.compute_K3(counts)
    sigma = chrono.shot_noise_sigma_K3(corr, shots)
    witness = tw.build_witness(K3, corr, shots, sigma)

    checks = {
        "recomputed_K3": K3,
        "recomputed_correlators": corr,
        "K3_matches_record": abs(K3 - record["temporal_witness"]["K3"]) < 1e-9,
        "record_hash_valid": pr.verify_record_hash(record),
        "chrono_nonce_valid": pr.verify_chrono_nonce(record, counts, cal, witness),
        "violation": witness["violation"],
        "significant_violation_3sigma": witness["significant_violation_3sigma"],
    }
    all_ok = (checks["K3_matches_record"] and checks["record_hash_valid"]
              and checks["chrono_nonce_valid"])
    print(json.dumps(checks, indent=2))
    print(f"\n[verify] OVERALL: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
