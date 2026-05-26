# EDUOS – Operating System Simulation Project

---

## Project Title
**EDUOS – Operating System Simulation (C & Python Hybrid System)**

## Module Code
CS 2104 – Operating Systems

## Student Information
- **Name:** Shadreck Nkhope  
- **Registration Number:** [YOUR REG NUMBER HERE]

---

# Overview

EDUOS is a simplified operating system simulation project developed for CS & IT coursework.  
It demonstrates core operating system concepts including:

- Process Management (PCB simulation)
- Thread Management
- Inter-Process Communication (IPC)
- CPU Scheduling Algorithms (FCFS, SJF, Priority, Round Robin)
- Python-based Scheduling Analysis and Visualization

The project consists of:

- **C Core System** → Low-level OS simulation
- **Python Scheduler** → Analysis + visualization layer

---

# Project Structure

EDUos/
│
├── c_core/
│ ├── main_sim.c # Main OS simulator entry point
│ ├── process_manager.c # Process creation & lifecycle (PCB)
│ ├── thread_manager.c # Thread pool simulation
│ ├── ipc_module.c # IPC (message passing simulation)
│ ├── scheduler.c # CPU scheduling algorithms
│ ├── include/
│ │ └── eduos.h # Shared structures & definitions
│ └── eduos.exe # Compiled output
│
├── python_scheduler/
│ ├── scheduler_sim.py # Scheduling simulator
│ ├── sample_processes.csv # Input workload data
│ ├── pcb_snapshot.json # Exported process states
│ ├── requirements.txt # Python dependencies
│ └── pycache/
│
├── docs/
│ └── screenshots/ # Execution screenshots
│
├── README.md
└── .gitignore


---

# Prerequisites

## C Core Requirements

- GCC compiler (MinGW / MSYS2 / WSL recommended)
- pthread support
- Windows users: MSYS2 UCRT64 recommended

### Check GCC:
```bash
gcc --version

Python Requirements
Python 3.8+
pip package manager
Install dependencies:
pip install -r requirements.txt
Build Instructions
Step 1: Clone Repository
git clone https://github.com/your-username/eduos.git
cd EDUos
Step 2: Build C Core
gcc -Wall -Wextra -pthread -std=c11 \
main_sim.c process_manager.c thread_manager.c ipc_module.c scheduler.c \
-o eduos
Run:
./eduos

Windows:

eduos.exe
Step 3: Run Python Scheduler
cd python_scheduler
pip install -r requirements.txt
python scheduler_sim.py
Features Implemented
✔ Process Management
PCB creation and lifecycle tracking
Process state transitions (READY → RUNNING → TERMINATED)
✔ Thread Management
Thread pool simulation
Concurrent execution model
✔ IPC System
Message queue simulation
Inter-process communication handling
✔ CPU Scheduling
FCFS
SJF
Priority Scheduling (with aging)
Round Robin
✔ Python Analysis
Gantt chart visualization
Performance metrics (WT, TAT, RT)
CSV → JSON pipeline
Screenshots (Evidence)
c_core execution
    ![C Execution](docs/screenshots/c_execution.png)
python_scheduler output
    ![Python Output](docs/screenshots/python_scheduler.png)
gantt chart
    ![Gantt Chart](docs/screenshots/gantt_chart.png)


Final Output
0 errors from 0 contexts

✔ Clean compilation using:

gcc -Wall -Wextra -pthread -std=c11
Challenges & Solutions
1. Multiple main() Conflict
Problem: Multiple entry points in different C files
Fix: Compiled only main_sim.c for main system
2. Windows Valgrind Limitation
Problem: Valgrind not available on Windows
Fix: Used MSYS2/WSL or documented limitation
3. Thread Synchronization Issues
Problem: Race conditions in scheduling
Fix: Added mutex-based fixed version
4. IPC Failures
Problem: Pipe/message errors
Fix: Added proper error handling and validation
5. Build System Issues
Problem: Wildcard compilation caused linking errors
Fix: Explicit source file compilation
References
Silberschatz, Galvin & Gagne – Operating System Concepts
Stallings – Operating Systems: Internals and Design Principles
GCC Documentation: https://gcc.gnu.org/onlinedocs/
POSIX Threads: https://man7.org/linux/
Python Docs: https://docs.python.org/3/
MSYS2 Documentation: https://www.msys2.org/
351 CS 2104 Lecture Notes