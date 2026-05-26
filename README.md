# EDUOS – Operating System Simulation Project

---

## Project Title
**EDUOS – Operating System Simulation (C & Python)**

## Module Code
351 CS 2104 

## Student Information
- **Name:** Shadreck Nkhope  
- **Registration Number:** 25311351019

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
│ ├── main_sim.c 
│ ├── process_manager.c 
│ ├── thread_manager.c 
│ ├── ipc_module.c
│ ├── scheduler.c
│ ├── include/
│ │ └── eduos.h 
│ └── eduos.exe
│
├── python_scheduler/
│ ├── scheduler_sim.py 
│ ├── sample_processes.csv 
│ ├── pcb_snapshot.json
│ ├── requirements.txt 
│ └── pycache/
│
├── docs/
│ └── screenshots/ 
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



