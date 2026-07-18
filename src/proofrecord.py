"""
CHRONO-1 — ProofRecord with a bound temporal (Leggett-Garg) witness.

schema_version: chrono-proofrecord-1.0

Novelty vs. BELLWETHER: the record carries a `temporal_witness` block (the
Leggett-Garg K3 statistic + violation verdict) AND a `chrono_nonce` whose
preimage includes that statistic. Tampering with the witness therefore breaks
the nonce, and the record_hash covers the whole thing. The bound quantity is a
TEMPORAL nonclassicality certificate (no definite pre-measurement value under
NIM), not a spatial one.

Provenance chain (all SHA-256, length-prefixed canonical JSON):
    raw_counts_hash   = H( canonical(counts_by_correlator) )
    calibration_hash  = H( canonical(calibration_snapshot) )
    witness_hash      = H( canonical(temporal_witness) )
    chrono_nonce      = H( lp(raw_counts_hash) || lp(job_id) ||
                          lp(calibration_hash) || lp(witness_hash) )
    record_hash       = H( canonical(all record fields except record_hash) )
"""
from __future__ import annotations

import hashlib
import json
from typing import Any, Dict

SCHEMA_VERSION = "chrono-proofrecord-1.0"


def canonical_json(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def _sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_hex(obj: Any) -> str:
    return _sha256(canonical_json(obj))


def lp(b: bytes) -> bytes:
    """Length-prefix with 8-byte big-endian length (anti boundary-collision)."""
    return len(b).to_bytes(8, "big") + b


def compute_chrono_nonce(raw_counts_hash: str, job_id: str,
                         calibration_hash: str, witness_hash: str) -> str:
    h = hashlib.sha256()
    for part in (raw_counts_hash, job_id, calibration_hash, witness_hash):
        h.update(lp(part.encode("utf-8")))
    return h.hexdigest()


def build_proofrecord(counts_by_correlator, job_id: str, backend: str,
                      provider_instance: str, calibration_snapshot: Dict,
                      temporal_witness: Dict, context_id: str,
                      timestamp_utc: str) -> Dict:
    raw_counts_hash = sha256_hex(counts_by_correlator)
    calibration_hash = sha256_hex(calibration_snapshot)
    witness_hash = sha256_hex(temporal_witness)
    chrono_nonce = compute_chrono_nonce(raw_counts_hash, job_id,
                                        calibration_hash, witness_hash)
    record = {
        "schema_version": SCHEMA_VERSION,
        "chrono_nonce": chrono_nonce,
        "temporal_witness": temporal_witness,
        "raw_counts_hash": raw_counts_hash,
        "calibration_hash": calibration_hash,
        "witness_hash": witness_hash,
        "job_id": job_id,
        "backend": backend,
        "provider_instance": provider_instance,
        "context_id": context_id,
        "timestamp_utc": timestamp_utc,
    }
    record["record_hash"] = _sha256(canonical_json(
        {k: v for k, v in record.items() if k != "record_hash"}))
    return record


def verify_record_hash(record: Dict) -> bool:
    expected = _sha256(canonical_json(
        {k: v for k, v in record.items() if k != "record_hash"}))
    return expected == record.get("record_hash")


def verify_chrono_nonce(record: Dict, counts_by_correlator,
                        calibration_snapshot, temporal_witness) -> bool:
    rc = sha256_hex(counts_by_correlator)
    cal = sha256_hex(calibration_snapshot)
    wit = sha256_hex(temporal_witness)
    if rc != record.get("raw_counts_hash"):
        return False
    if cal != record.get("calibration_hash"):
        return False
    if wit != record.get("witness_hash"):
        return False
    expect = compute_chrono_nonce(rc, record["job_id"], cal, wit)
    return expect == record.get("chrono_nonce")
