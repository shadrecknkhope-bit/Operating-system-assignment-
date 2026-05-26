from collections import deque
import argparse
import csv
import json
import random
import matplotlib.pyplot as plt
from tabulate import tabulate
import os

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

    processes = sorted(processes, key=lambda p: (p["arrival"], p["pid"]))

    time = 0
    schedule = []

    for p in processes:

        if time < p["arrival"]:
            time = p["arrival"]

        start = time
        end = start + p["burst"]

        schedule.append([p["pid"], start, end])

        time = end

    return schedule

def sjf(processes):

    processes = processes[:]

    time = 0
    completed = []
    schedule = []

    while len(completed) < len(processes):

        available = [
            p for p in processes
            if p["arrival"] <= time and p not in completed
        ]

        if not available:
            time += 1
            continue

        available.sort(
            key=lambda p: (p["burst"], p["arrival"], p["pid"])
        )

        p = available[0]

        start = time
        end = time + p["burst"]

        schedule.append([p["pid"], start, end])

        time = end

        completed.append(p)

    return schedule

def priority_scheduling(processes):

    processes = [p.copy() for p in processes]

    time = 0
    completed = []
    schedule = []

    waiting_counter = 0

    while len(completed) < len(processes):

        available = [
            p for p in processes
            if p["arrival"] <= time and p not in completed
        ]

        if not available:
            time += 1
            continue

        # ageing every 3 time units
        if waiting_counter == 3:

            for p in available:
                if p["priority"] > 0:
                    p["priority"] -= 1

            waiting_counter = 0

        available.sort(
            key=lambda p: (p["priority"], p["arrival"], p["pid"])
        )

        p = available[0]

        start = time
        end = time + p["burst"]

        schedule.append([p["pid"], start, end])

        time = end

        completed.append(p)

        waiting_counter += 1

    return schedule


def round_robin(processes, quantum):

    processes = sorted(processes, key=lambda p: p["arrival"])

    time = 0
    queue = deque()
    schedule = []

    remaining = {
        p["pid"]: p["burst"]
        for p in processes
    }

    arrived = []

    while len(arrived) < len(processes) or queue:

        for p in processes:

            if p["arrival"] <= time and p not in arrived:
                queue.append(p)
                arrived.append(p)

        if not queue:
            time += 1
            continue

        p = queue.popleft()

        exec_time = min(quantum, remaining[p["pid"]])

        start = time
        end = time + exec_time

        schedule.append([p["pid"], start, end])

        time = end

        remaining[p["pid"]] -= exec_time

        if remaining[p["pid"]] > 0:
            queue.append(p)

    return schedule

def calculate_metrics(schedule, processes):

    metrics = {}

    for p in processes:

        pid = p["pid"]
        arrival = p["arrival"]
        burst = p["burst"]

        completion = 0
        response = -1

        total_runtime = 0

        for entry in schedule:

            if entry[0] == pid:

                start = entry[1]
                end = entry[2]

                total_runtime += (end - start)

                completion = end

                if response == -1:
                    response = start - arrival

        turnaround = completion - arrival
        waiting = turnaround - burst

        metrics[pid] = {
            "Arrival": arrival,
            "Burst": burst,
            "Completion": completion,
            "TAT": turnaround,
            "WT": waiting,
            "RT": response
        }

    return metrics

def print_metrics_table(metrics, algorithm_name):

    print(f"\n=== {algorithm_name} RESULTS ===")

    table = []

    total_wt = 0
    total_tat = 0
    total_rt = 0

    for pid, m in metrics.items():

        table.append([
            pid,
            m["Arrival"],
            m["Burst"],
            m["Completion"],
            m["TAT"],
            m["WT"],
            m["RT"]
        ])

        total_wt += m["WT"]
        total_tat += m["TAT"]
        total_rt += m["RT"]

    print(tabulate(
        table,
        headers=["PID", "AT", "BT", "CT", "TAT", "WT", "RT"],
        tablefmt="grid"
    ))

    n = len(metrics)

    if n == 0:
        print("No metrics to display.")
        return 0, 0, 0

    avg_wt = total_wt / n
    avg_tat = total_tat / n
    avg_rt = total_rt / n

    print(f"\nAverage WT : {avg_wt:.2f}")
    print(f"Average TAT: {avg_tat:.2f}")
    print(f"Average RT : {avg_rt:.2f}")

    return avg_wt, avg_tat, avg_rt

def generate_gantt_chart(schedule, algorithm_name):

    os.makedirs("docs/screenshots", exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 3))

    colors = {}

    for i, entry in enumerate(schedule):

        pid, start, end = entry

        label = pid

        if pid == "CS":

            color = "grey"

        else:

            process_group = pid.split("-")[0]

            if process_group not in colors:
                colors[process_group] = f"C{len(colors)}"

            color = colors[process_group]

        ax.barh(
            label,
            end - start,
            left=start,
            color=color,
            edgecolor="black"
        )

    ax.set_xlabel("Time")
    ax.set_ylabel("Processes / Threads")
    ax.set_title(f"{algorithm_name} Gantt Chart")

    ax.set_xticks(
        range(0, max(e[2] for e in schedule) + 1)
    )

    filename = f"docs/screenshots/{algorithm_name.lower()}_gantt.png"

    plt.savefig(filename, bbox_inches="tight")

    print(f"Gantt chart saved: {filename}")

    plt.close()

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

            print("DEBUG ROW:", row)

            processes.append({
                "pid": row["pid"],
                "arrival": int(row["arrival"]),
                "burst": int(row["burst"]),
                "priority": int(row["priority"])
            })

    print("LOADED PROCESSES:", processes)

    return processes

def load_from_pcb_snapshot(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    processes = []

    for p in data:
        processes.append(create_process(
            p["pid"],
            p.get("arrival", 0),   
            p.get("burst", 1),     
            p.get("priority", 0)   
        ))

    return processes

def parse_arguments():
    parser = argparse.ArgumentParser(description="CPU Scheduling Simulator")

    parser.add_argument("--random", type=int, help="Generate N random processes")
    parser.add_argument("--seed", type=int, help="Random seed")
    parser.add_argument("--file", type=str, help="Load processes from CSV file")
    parser.add_argument("--pcb", type=str, help="Load PCB snapshot JSON")
    parser.add_argument("--mode",choices=["process", "thread"],default="process",help="Scheduling mode")

    return parser.parse_args()

def generate_thread_processes(count, seed=None):

    import random

    if seed is not None:
        random.seed(seed)

    threads = []

    process_groups = ["P1", "P2", "P3"]

    for i in range(count):

        pid = random.choice(process_groups)

        thread = {
            "pid": pid,
            "tid": f"T{i+1}",
            "arrival": random.randint(0, 10),
            "burst": random.randint(1, 8),
            "priority": random.randint(1, 5)
        }

        threads.append(thread)

    return threads

CONTEXT_SWITCH_COST = 1

def thread_round_robin(threads, quantum=2):

    threads = sorted(threads, key=lambda t: t["arrival"])

    time = 0

    ready_queue = deque()

    schedule = []

    remaining = {
        t["tid"]: t["burst"]
        for t in threads
    }

    arrived = []

    last_thread = None

    while len(arrived) < len(threads) or ready_queue:

        for t in threads:

            if t["arrival"] <= time and t not in arrived:
                ready_queue.append(t)
                arrived.append(t)

        if not ready_queue:
            time += 1
            continue

        thread = ready_queue.popleft()

        # Context switch overhead
        if last_thread is not None and last_thread != thread["tid"]:

            schedule.append([
                "CS",
                time,
                time + CONTEXT_SWITCH_COST
            ])

            time += CONTEXT_SWITCH_COST

        start = time

        run_time = min(
            quantum,
            remaining[thread["tid"]]
        )

        end = start + run_time

        schedule.append([
            f'{thread["pid"]}-{thread["tid"]}',
            start,
            end
        ])

        time = end

        remaining[thread["tid"]] -= run_time

        if remaining[thread["tid"]] > 0:
            ready_queue.append(thread)

        last_thread = thread["tid"]

    return schedule

def comparison_chart(results_summary):

    import matplotlib.pyplot as plt

    algorithms = list(results_summary.keys())
    wt_values = [results_summary[a]["WT"] for a in algorithms]
    tat_values = [results_summary[a]["TAT"] for a in algorithms]

    x = range(len(algorithms))

    plt.figure(figsize=(8, 4))

    plt.bar(x, wt_values, label="Waiting Time")
    plt.bar(x, tat_values, bottom=wt_values, label="Turnaround Time")

    plt.xticks(x, algorithms)
    plt.ylabel("Time")
    plt.title("Scheduling Algorithm Comparison")
    plt.legend()

    os.makedirs("docs/screenshots", exist_ok=True)

    plt.savefig("docs/screenshots/comparison_chart.png")
    plt.close()

    print("Comparison chart saved.")

if __name__ == "__main__":

    args = parse_arguments()

    # ================= THREAD MODE =================
    if args.mode == "thread":

        print("\n=== THREAD MODE ENABLED ===")

        threads = generate_thread_processes(
            args.random if args.random else 6,
            args.seed
        )

        for t in threads:
            print(t)

        thread_schedule = thread_round_robin(
            threads,
            quantum=2
        )

        generate_gantt_chart(
            thread_schedule,
            "THREAD_ROUND_ROBIN"
        )

        print("\nThread scheduling completed.")

        exit()

    # ================= NORMAL PROCESS MODE =================

    if args.random:
        processes = generate_random_processes(
            args.random,
            args.seed
        )

    elif args.file:
        processes = load_from_csv(args.file)

    elif args.pcb:
        processes = load_from_pcb_snapshot(args.pcb)

    else:
        print("No input source provided")
        exit()

    print("\n=== INPUT PROCESSES ===")

    for p in processes:
        print(p)

    results_summary = {}

    # ================= FCFS =================
    print(processes)
    fcfs_schedule = fcfs(processes)
    fcfs_metrics = calculate_metrics(fcfs_schedule, processes)

    wt, tat, rt = print_metrics_table(fcfs_metrics, "FCFS")

    generate_gantt_chart(fcfs_schedule, "FCFS")

    results_summary["FCFS"] = {
        "WT": wt,
        "TAT": tat
    }

    # ================= SJF =================
    sjf_schedule = sjf(processes)
    sjf_metrics = calculate_metrics(sjf_schedule, processes)

    wt, tat, rt = print_metrics_table(sjf_metrics, "SJF")

    generate_gantt_chart(sjf_schedule, "SJF")

    results_summary["SJF"] = {
        "WT": wt,
        "TAT": tat
    }

    # ================= PRIORITY =================
    pr_schedule = priority_scheduling(processes)
    pr_metrics = calculate_metrics(pr_schedule, processes)

    wt, tat, rt = print_metrics_table(pr_metrics, "PRIORITY")

    generate_gantt_chart(pr_schedule, "PRIORITY")

    results_summary["PRIORITY"] = {
        "WT": wt,
        "TAT": tat
    }

    # ================= ROUND ROBIN =================
    rr_schedule = round_robin(processes, 2)
    rr_metrics = calculate_metrics(rr_schedule, processes)

    wt, tat, rt = print_metrics_table(rr_metrics, "ROUND ROBIN")

    generate_gantt_chart(rr_schedule, "ROUND_ROBIN")

    results_summary["ROUND ROBIN"] = {
        "WT": wt,
        "TAT": tat
    }

    # ================= COMPARISON =================
    comparison_chart(results_summary)