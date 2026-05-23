#ifndef EDUOS_H
#define EDUOS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>
#include <time.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <semaphore.h>

#define MAX_PROCESSES 100
#define THREAD_POOL_SIZE 4
#define QUEUE_SIZE 20

typedef struct {
    pid_t pid;
    pid_t parent_pid;
    char name[64];
    int state;
    int priority;
    int burst_time;
    int arrival_time;
    int remaining_time;
    int memory_req_kb;
    int thread_count;
    int owner_id;
    int exit_code;
    time_t creation_time;
} PCB;

enum {
    NEW,
    READY,
    RUNNING,
    WAITING,
    TERMINATED
};

extern PCB process_table[MAX_PROCESSES];
extern int process_count;

/* Process Management */
pid_t edu_fork(PCB *parent);
void edu_exec(pid_t pid, char *prog_name);
int edu_wait(pid_t parent_pid);
void edu_exit(pid_t pid, int exit_code);
void edu_ps();
void save_pcb_json();

/* Threading */
void run_thread_pool();
void race_condition_demo();
void mutex_fixed_demo();
void producer_consumer_demo();
void deadlock_demo();

/* IPC */
void shared_memory_demo();
void pipe_demo();

#endif