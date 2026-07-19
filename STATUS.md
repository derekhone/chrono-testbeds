# CHRONO-1 — Status

**Experiment:** Leggett–Garg temporal-inequality (K3) witness bound into an authorization ProofRecord.
**Series:** CHRONO (temporal nonclassicality) — distinct from ARK, WITNESS, CIF (formerly UIP), BELLWETHER.

## State
- Design + harness: COMPLETE
- Mock tests: 9/9 PASS
- Simulation (AerSimulator, noiseless): K3 = 1.508 (ideal 1.5; macrorealist bound ≤ 1 violated ~152σ)
- Preregistration: LOCKED (MANIFEST.sha256)
- Hardware job: see results/SUBMITTED_JOB_ID.txt once submitted
- IP gate: LOCAL-ONLY. No GitHub / Zenodo / LinkedIn / RF-100 until Derek's file-first determination.

## Finalize when job is DONE
    cd /home/ubuntu/chrono-testbeds
    python3 src/fetch_result.py            # reads job id from results/raw/job_meta.json or SUBMITTED_JOB_ID.txt
    python3 src/verify.py

## Honesty boundary
Device-dependent, single-system TEMPORAL witness under the non-invasive-measurability assumption
(clumsiness loophole OPEN). NOT loophole-free; NOT device-independent certified randomness.
