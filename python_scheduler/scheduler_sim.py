from collections import deque
import argparse
import csv
import json
import random

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

        self.remaining_time = burst_time

def sort_by_fcfs(processes):
    return sorted(processes, key=lambda p: (p.arrival_time, p.pid))

def fcfs(processes):
    processes = sort_by_fcfs(processes)

    time = 0
    schedule = []

    for p in processes:
        if time < p.arrival_time:
            time = p.arrival_time  # CPU idle handled

        start = time
        end = start + p.burst_time

        schedule.append([p.pid, start, end])
        time = end

    return schedule

def sjf(processes):
    processes = processes[:]
    time = 0
    schedule = []
    completed = []

    while len(completed) < len(processes):

        available = [p for p in processes if p.arrival_time <= time and p not in completed]

        if not available:
            time += 1
            continue

        # shortest job first + FCFS tie-break
        available.sort(key=lambda p: (p.burst_time, p.arrival_time, p.pid))

        p = available[0]

        start = time
        end = time + p.burst_time

        schedule.append([p.pid, start, end])

        time = end
        completed.append(p)

    return schedule

def priority_scheduling(processes):
    processes = processes[:]
    time = 0
    schedule = []
    completed = []

    ageing_counter = 0

    while len(completed) < len(processes):

        available = [p for p in processes if p.arrival_time <= time and p not in completed]

        if not available:
            time += 1
            continue

        # AGEING: every 3 time units increase priority (reduce number = higher priority)
        if ageing_counter == 3:
            for p in available:
                if p.priority > 0:
                    p.priority -= 1
            ageing_counter = 0

        available.sort(key=lambda p: (p.priority, p.arrival_time, p.pid))

        p = available[0]

        start = time
        end = time + p.burst_time

        schedule.append([p.pid, start, end])

        time = end
        completed.append(p)

        ageing_counter += 1

    return schedule


def round_robin(processes, quantum):
    processes = sorted(processes, key=lambda p: p.arrival_time)

    time = 0
    queue = deque()
    schedule = []

    remaining = {p.pid: p.burst_time for p in processes}
    arrived = []

    while len(arrived) < len(processes) or queue:

        # add newly arrived processes
        for p in processes:
            if p.arrival_time <= time and p not in arrived:
                queue.append(p)
                arrived.append(p)

        if not queue:
            time += 1
            continue

        p = queue.popleft()

        exec_time = min(quantum, remaining[p.pid])

        start = time
        time += exec_time
        end = time

        schedule.append([p.pid, start, end])

        remaining[p.pid] -= exec_time

        if remaining[p.pid] > 0:
            queue.append(p)

    return schedule

def create_process(pid, arrival, burst, priority):
    return {
        "pid": pid,
        "arrival": arrival,
        "burst": burst,
        "priority": priority
    }

def generate_random_processes(n, seed=None):
    if seed is not None:
        random.seed(seed)

    processes = []

    for i in range(n):
        pid = f"P{i+1}"
        arrival = random.randint(0, 10)
        burst = random.randint(1, 10)
        priority = random.randint(1, 5)

        processes.append(create_process(pid, arrival, burst, priority))

    return processes

def load_from_csv(filename):
    processes = []

    with open(filename, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            processes.append(create_process(
                row["pid"],
                int(row["arrival"]),
                int(row["burst"]),
                int(row["priority"])
            ))

    return processes

def load_from_pcb_snapshot(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    processes = []

    for p in data:
        processes.append(create_process(
            p["pid"],
            p["arrival"],
            p["burst"],
            p["priority"]
        ))

    return processes

def parse_arguments():
    parser = argparse.ArgumentParser(description="CPU Scheduling Simulator")

    parser.add_argument("--random", type=int, help="Generate N random processes")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--file", type=str, help="Load processes from CSV file")
    parser.add_argument("--pcb", type=str, help="Load PCB snapshot JSON")

    return parser.parse_args()

if __name__ == "__main__":

    args = parse_arguments()

    processes = []

    # =========================
    # INPUT SOURCE HANDLING
    # =========================

    if args.random:
        processes = generate_random_processes(args.random, args.seed)

    elif args.file:
        processes = load_from_csv(args.file)

    elif args.pcb:
        processes = load_from_pcb_snapshot(args.pcb)

    else:
        print("No input provided. Use --random, --file, or --pcb")
        exit()

    # =========================
    # SHOW INPUT DATA
    # =========================

    print("\n=== INPUT PROCESSES ===")
    for p in processes:
        print(p)

    # (we will connect to schedulers in 3.3)