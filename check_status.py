from qiskit_ibm_runtime import QiskitRuntimeService
import os
import json

# SECURITY: never hardcode credentials. Read the IBM Quantum token from the environment.
# A previously hardcoded token here was exposed publicly and must be revoked/rotated.
TOKEN = os.environ.get("IBM_QUANTUM_TOKEN", "")
if not TOKEN:
    raise SystemExit("Set the IBM_QUANTUM_TOKEN environment variable before running this script.")
JOB_ID = "d9dkj6ineu4c739nddrg"
RESULT_FILE = "/home/ubuntu/chrono-testbeds/results/CHRONO-1-result.json"

try:
    service = QiskitRuntimeService(channel='ibm_quantum_platform', token=TOKEN)
    job = service.job(JOB_ID)
    status = job.status()
    queue_info = job.queue_info()
    print(f"JOB_STATUS: {status}")
    if queue_info:
        print(f"QUEUE_POSITION: {queue_info.position}")

    if os.path.exists(RESULT_FILE):
        print("RESULT_FILE_EXISTS: TRUE")
    else:
        print("RESULT_FILE_EXISTS: FALSE")

except Exception as e:
    print(f"ERROR: {str(e)}")
