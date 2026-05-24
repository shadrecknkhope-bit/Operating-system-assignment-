#ifndef EDUOS_H
#define EDUOS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>

#define MAX_PROCESSES 100

// Process States
typedef enum {
    NEW,
    READY,
    RUNNING,
    WAITING,
    TERMINATED
} ProcessState;

// PCB Structure
typedef struct {

    pid_t pid;              // system-defined type (NO typedef needed)
    pid_t parent_pid;

    char name[64];

    int state;
    int priority;

    int burst_time;
    int arrival_time;
    int remaining_time;

    int memory_req_kb;
    int thread_count;

    time_t creation_time;

    int exit_code;

} PCB;

// Global process table
extern PCB process_table[MAX_PROCESSES];
extern int process_count;

// Function declarations
pid_t edu_fork(PCB *parent);

void edu_exec(pid_t pid, char *prog_name);

int edu_wait(pid_t parent_pid);

void edu_exit(pid_t pid, int exit_code);

void edu_ps();

void save_pcb_snapshot();

#endif