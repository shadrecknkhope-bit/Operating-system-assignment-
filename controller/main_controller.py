import subprocess
import json
import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.dirname(BASE_DIR)

C_BINARY = os.path.join(
    PROJECT_ROOT,
    "c_core",
    "eduos.exe"
)

PCB_FILE = os.path.join(
    PROJECT_ROOT,
    "python_scheduler",
    "pcb_snapshot.json"
)

PYTHON_SCHEDULER = os.path.join(
    PROJECT_ROOT,
    "python_scheduler",
    "scheduler_sim.py"
)

def launch_c_simulator():

    print("\n=== STARTING C SIMULATOR ===")

    try:

        process = subprocess.Popen(
            [C_BINARY],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        return process

    except FileNotFoundError:

        print("ERROR: eduos.exe not found")

        return None
    
def monitor_c_output(process):

    print("\n=== C SIMULATOR OUTPUT ===")

    while True:

        output = process.stdout.readline()

        if output == "" and process.poll() is not None:
            break

        if output:
            print(output.strip())

def wait_for_pcb_snapshot():

    print("\nWaiting for pcb_snapshot.json...")

    while not os.path.exists(PCB_FILE):

        time.sleep(1)

    print("PCB snapshot detected.")

def load_pcb_data():

    with open(PCB_FILE, "r") as file:

        data = json.load(file)

    print("\n=== PCB DATA ===")

    print(json.dumps(data, indent=4))

    return data

def run_scheduler():

    print("\n=== RUNNING PYTHON SCHEDULER ===")

    subprocess.run([
        "py",
        PYTHON_SCHEDULER,
        "--pcb",
        PCB_FILE
    ])

def generate_report():

    report = {

        "timestamp": str(datetime.now()),

        "status": "Simulation Completed",

        "charts_location": "docs/screenshots/",

        "scheduler": [
            "FCFS",
            "SJF",
            "Priority",
            "Round Robin"
        ]
    }

    report_path = os.path.join(
        PROJECT_ROOT,
        "docs",
        "simulation_report.json"
    )

    with open(report_path, "w") as file:

        json.dump(report, file, indent=4)

    print(f"\nReport generated: {report_path}")

if __name__ == "__main__":

    print("\n========== EDUOS CONTROLLER ==========")

    process = launch_c_simulator()

    if process is not None:

        monitor_c_output(process)

    wait_for_pcb_snapshot()

    load_pcb_data()

    run_scheduler()

    generate_report()

    print("\n=== FULL SYSTEM EXECUTION COMPLETE ===")