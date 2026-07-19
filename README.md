# CHRONO-1 — The Temporal Witness

**Remnant Fieldworks Inc. · Coherent Inheritance Framework (CIF) · ExecutionProof-governed**

A **Leggett–Garg K3 temporal-inequality witness** bound into an authorization ProofRecord. CHRONO-1 measures three two-time correlators on a single superconducting qubit and tests whether the system satisfies the **macrorealist assumption** (definite pre-measurement reality) or exhibits **temporal nonclassicality** consistent with quantum mechanics.

**Series:** CHRONO (temporal nonclassicality) — independent of ARK, WITNESS, BELLWETHER, OMNI, TRINITY.

## Status — HARDWARE COMPLETE, INDEPENDENTLY VERIFIED

Executed on IBM Quantum hardware, independently verified, and results published.

| Experiment | Backend | K3 | Macrorealist Bound | Verdict | Job ID |
|---|---|---|---|---|---|
| **CHRONO-1** | ibm_fez | **1.450** | ≤ 1.0 | **ALLOW** (bound violated) | `d9dkj6ineu4c739nddrg` |

- **Shots:** 2000 per correlator (6000 total)
- **Execution date:** 2026-07-18
- **Quantum prediction (Lüders bound):** K3 = 1.5
- **Observed:** K3 = 1.450 (97% of ideal, >3σ violation of macrorealist bound)
- Independent verifier **PASS** — reconstructs K3, correlators, and all hashes from raw counts

The measured K3 **violates the macrorealist bound** (K3 ≤ 1) by 0.450, consistent with quantum-mechanical sequential measurement on a single system.

## Public claim (kept narrow)

> CHRONO-1 measures the **Leggett–Garg K3 temporal inequality** on a single superconducting qubit using mid-circuit measurements and cryptographically binds the measured K3 statistic into an authorization ProofRecord as a **temporal nonclassicality witness** — evidence that the authorized value had **no definite pre-measurement (pre-execution) reality** under the stated assumption.

**Wording, deliberately:**
- This is a **device-dependent, single-system temporal witness** under the non-invasive-measurability assumption.
- The **clumsiness loophole remains OPEN** — we assume mid-circuit measurements do not significantly disturb future evolution (standard assumption in circuit-based Leggett–Garg tests, but not closed by the experiment).
- **NOT** loophole-free, NOT device-independent, NOT certified randomness.
- The K3 statistic certifies temporal correlation structure, **not** spatial entanglement or Bell nonlocality.
- "Temporal nonclassicality" means violation of the Leggett–Garg inequality under stated assumptions — it does not imply violation of any local realism bound or any new physics claim.

## Experiment Design (preregistered)

Single qubit initialized to |0⟩, observable Q = Z (eigenvalues ±1). Between measurement times, the qubit precesses under **R_y(θ = π/3)**.

**Three two-time correlators** (each in a separate circuit):
- **C12:** measure(t1) → R_y(θ) → measure(t2)
- **C23:** R_y(θ) → measure(t2) → R_y(θ) → measure(t3)
- **C13:** measure(t1) → R_y(2θ) → measure(t3)

**Leggett–Garg K3:** `K3 = C12 + C23 − C13`

- Macrorealist bound: **K3 ≤ 1**
- Quantum (Lüders) bound: **K3 = 1.5**
- Ideal predictions: C12 = C23 = +0.5, C13 = −0.5 → K3 = 1.5

**Verdict logic (preregistered, frozen):**

| Verdict | Condition |
|---|---|
| **ALLOW** | K3 > 1.0 + 3σ (macrorealist bound violated) |
| **HOLD** | 1.0 < K3 ≤ 1.0 + 3σ (inconclusive) |
| **DENY** | K3 ≤ 1.0 (no violation, macrorealist compatible) |
| **GATE-STOP** | Hardware failure, provenance invalid, reconstruction mismatch |

Precedence: **DENY > GATE-STOP > HOLD > ALLOW**.

## Files

- `prereg/CHRONO-1-prereg.md` — full preregistered design (locked).
- `src/harness.py` — builds the three Leggett–Garg circuits, executes on IBM hardware, assembles the `chrono-proofrecord-1.0` record, computes K3 and the aggregate verdict.
- `src/verify.py` — independent verifier: reconstructs C12, C23, C13, K3, and the verdict from raw counts with **no qiskit dependency**.
- `MANIFEST.sha256` — SHA-256 preregistration lock (prereg + harness), committed before hardware run.
- `results/` — hardware report, ProofRecord JSON, raw counts, and calibration snapshot.

## Run

```bash
pip install -r requirements.txt

# Simulator validation (default; no token needed)
python3 src/harness.py

# Independent verification (reconstructs from raw counts)
python3 src/verify.py
```

## Hardware run — how it was executed (reproducibility)

The hardware run was performed on IBM Quantum (ibm_fez) after token rotation and explicit authorization. To reproduce on your own account:

```bash
export IBM_QUANTUM_TOKEN="your-token"     # never commit or paste in chat
python3 src/harness.py --authorize-hardware
python3 src/verify.py
```

## Scope & honesty

**Device-dependent.** Results apply only within the tested qubit, backend calibration, circuit model, and shot counts. The clumsiness loophole (non-invasive measurability) is **assumed, not closed**. σ is binomial shot noise only. This is experimental evidence of temporal quantum correlation structure under stated assumptions — **not** a loophole-free proof, not device-independence, not new physics.

**Temporal vs. spatial:** Leggett–Garg tests **temporal** correlations (sequential measurements on one system). It is distinct from Bell tests (spatial correlations across separated systems) and does not test local realism or entanglement.

*Proof Before Power · Verification Before Execution · claims kept narrower than the evidence.*
