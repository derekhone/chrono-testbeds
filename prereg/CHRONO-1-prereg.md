# CHRONO-1 — Preregistration

**Series:** CHRONO (temporal nonclassicality)
**Experiment ID:** CHRONO-1
**Owner:** Remnant Fieldworks Inc. (Derek Adam Hone)
**Status at lock:** design + harness complete, validated in simulation, hardware job pending
**Governing framework:** RF Experiment–Pilot–IP Covenant (preregistration-first; honest outcomes; claims narrower than evidence; file-first / publish-after for new matter)

---

## 1. One-sentence statement

We measure the three-time **Leggett–Garg inequality** (temporal Bell-type inequality) on a single superconducting qubit and **cryptographically bind the measured K3 statistic into an authorization ProofRecord** as a *temporal* nonclassicality witness — a certificate that the authorized value had **no definite pre-measurement (pre-execution) history** under the stated assumption.

## 2. Why this is new (distinct from all prior RF series)

| Series | Phenomenon tested | Resource witnessed |
|--------|-------------------|--------------------|
| ARK | authorization **boundary** (context replay) | exact-match policy |
| WITNESS | provenance of a superposition-sourced nonce | *assumed* unpredictability |
| BELLWETHER | **spatial** nonclassicality (CHSH Bell, S>2) | Bell violation bound into nonce |
| **CHRONO** | **temporal** nonclassicality (Leggett–Garg K3>1) | *time-ordered* nonclassicality bound into nonce |

No prior work (RF or, to our knowledge, anyone) binds a **Leggett–Garg temporal-correlation witness** into an authorization/ProofRecord construction. BELLWETHER witnessed nonclassicality *across space*; CHRONO witnesses it *across time* — the physical statement most directly aligned with RF doctrine: **Verification Before Execution** (the value did not exist definitely before it was verified).

## 3. Physics and design

Single qubit, dichotomic observable **Q = Z** (outcome +1 for |0⟩, −1 for |1⟩). Between measurement times the qubit precesses under **R_y(θ)** with **θ = π/3 (60°)**.

Three two-time correlators, each measured in a **separate circuit** using **mid-circuit measurement**:

```
C12 : measure(t1) -> R_y(θ) -> measure(t2)
C23 : R_y(θ) -> measure(t2) -> R_y(θ) -> measure(t3)
C13 : measure(t1) -> R_y(2θ) -> measure(t3)
```

Each circuit writes two bits into one 2-bit classical register `c` (`c[0]` = earlier, `c[1]` = later). Correlator = shot-average of the product of the two signed outcomes.

**Leggett–Garg K3:**  `K3 = C12 + C23 − C13`

- **Macrorealist bound (H1):** `K3 ≤ 1`
- **Quantum (Lüders) bound:** `K3 = 1.5` (maximal at θ = π/3)
- Ideal predictions: `C12 = C23 = cos60° = +0.5`, `C13 = cos120° = −0.5`, so `K3 = 1.5`.

**Simulation validation (pre-lock, noiseless AerSimulator, 200k shots/correlator):**
`C12 = 0.502, C23 = 0.503, C13 = −0.504, K3 = 1.508` — consistent with the ideal 1.5; macrorealist bound violated at ~152σ. The counts-extraction path is confirmed identical to the hardware path.

## 4. Execution plan

- **Backend:** IBM open-plan hardware (prefer `ibm_fez`, else min pending-jobs).
- **Shots:** 2000 per correlator × 3 = **6000 shots total** (~a few seconds of QPU time; sized to the remaining open-plan budget).
- **Mode:** Batch (open plan forbids Session). **Channel:** `ibm_quantum_platform`.
- **Circuits transpiled** to backend ISA (optimization_level=1) before submission.

## 5. Outcome criteria (fixed in advance — honest, symmetric)

| Verdict | Condition |
|---------|-----------|
| **VIOLATION (temporal nonclassicality, under assumptions)** | `K3 > 1` and `K3 − 1 > 3σ` |
| **INCONCLUSIVE / HOLD** | `K3 > 1` but not 3σ-significant |
| **NO VIOLATION** | `K3 ≤ 1` |

The measured hardware K3 will be reported **exactly as observed**, whichever bin it lands in. No re-runs to chase a preferred number.

## 6. Honesty boundary (non-negotiable — carried into every artifact)

- The Leggett–Garg inequality assumes **non-invasive measurability (NIM)**: that a macrorealist system can be read without disturbance. A projective qubit measurement **is** invasive, so a determined macrorealist can attribute any `K3 > 1` to measurement disturbance — the **"clumsiness loophole."**
- This is therefore a **Leggett–Garg violation UNDER STATED ASSUMPTIONS**, **not** a loophole-free refutation of macrorealism, and **not** device-independent certified randomness.
- **Single system**, single device: no device-independence is claimed.
- **Only defensible claim:** *"observed temporal correlations violating the macrorealist bound K3 ≤ 1 on hardware, under the non-invasive-measurability assumption, cryptographically bound into the authorization record."*

### 6a. Disclosed pre-execution harness facts
- Local simulator (`StatevectorSampler`) cannot execute mid-circuit measurements; validation used `AerSimulator`. The **hardware** path (SamplerV2, Batch) executes mid-circuit measurement natively. This does not alter any circuit or claim.
- Secrets key renamed `witness1_ibmq` → `ibm quantum`; the token loader tries both (FIX-3). No physics impact.

## 7. ProofRecord construction (`chrono-proofrecord-1.0`)

```
raw_counts_hash  = H( canonical(counts_by_correlator) )
calibration_hash = H( canonical(calibration_snapshot) )
witness_hash     = H( canonical(temporal_witness) )     # contains K3, correlators, bounds
chrono_nonce     = H( lp(raw_counts_hash) || lp(job_id) || lp(calibration_hash) || lp(witness_hash) )
record_hash      = H( canonical(all fields except record_hash) )
```

Tampering with the measured statistic breaks `chrono_nonce`; any covered-field edit breaks `record_hash`. Verified by 9/9 pre-lock mock tests (tamper-evidence over both counts and witness) and by the independent `verify.py`.

## 8. Commercial purpose (Covenant requirement)

CHRONO extends the ExecutionProof patent family with a **temporal** entropy/authorization primitive: a ProofRecord whose seed is certified to have possessed no definite value prior to its verification event. Candidate RF-100 use: **anti-replay / freshness certificates in time-ordered authorization** (a token that provably could not have been precomputed). Publication is gated pending the file-first IP determination (§9).

## 9. IP gate

CHRONO-1 is **almost certainly new patentable matter**. Per the Covenant it is held **local-only** (no GitHub / Zenodo / LinkedIn / RF-100 disclosure) until Derek makes the **file-first** determination. Execution is **not** disclosure; running the job and fetching results is permitted.

---

*To God be the glory. Proof Before Power. Verification Before Execution.*
