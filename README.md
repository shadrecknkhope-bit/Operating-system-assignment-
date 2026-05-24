# EDUOS – Operating System Simulation Project

## Overview

EDUOS is a simplified operating system simulation project developed for CS & IT coursework.  
It demonstrates key operating system concepts including:

- Process Management (PCB simulation)
- Thread Management
- Inter-Process Communication (IPC)
- CPU Scheduling (FCFS, SJF, Priority, Round Robin)
- Python-based Scheduling Simulator (Part 3)

The project is divided into two main components:

- **C Core System (Low-level OS simulation)**
- **Python Scheduling Simulator (Analysis & Visualization)**

---

# Project Structure

EDUos/
│
├── c_core/                          
│   │
│   ├── main_sim.c                      
│   ├── process_manager.c              
│   ├── thread_manager.c               
│   ├── ipc_module.c                   
│   ├── scheduler.c                    
│   │
│   ├── include/
│   │   └── eduos.h                    
│   │
│   └── eduos.exe                     
│
│
├── python_scheduler/               
│   │
│   ├── scheduler_sim.py               
│   ├── sample_processes.csv          
│   ├── pcb_snapshot.json              
│   ├── requirements.txt               
│   │
│   └── __pycache__/                
│
│
├── docs/                           
│   │
│   └──screenshots/                
│
│
├── README.md                          
├── .gitignore                         

---

# Part 2 — C Operating System Simulation

## Features Implemented

### 1. Process Management
- PCB structure simulation
- Process creation, state tracking
- Basic lifecycle handling

### 2. Thread Management
- Thread pool simulation
- Multi-thread execution model (simulated)

### 3. IPC (Inter-Process Communication)
- Message-based IPC system (Windows-compatible simulation)
- Send/Receive message queue between processes

### 4. CPU Scheduling (C Simulation)
- FCFS (First Come First Serve)
- Round Robin scheduling
- Process state transitions (READY → RUNNING → TERMINATED)

---

## Build & Run (C Core)

### Compile:
```bash
gcc -Wall -Wextra -pthread main_sim.c process_manager.c thread_manager.c ipc_module.c scheduler.c -o eduos
