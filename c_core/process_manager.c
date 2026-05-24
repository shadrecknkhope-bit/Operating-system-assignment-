#include "include/eduos.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_PROCESSES 100

// ===================== GLOBAL VARIABLES =====================
PCB process_table[MAX_PROCESSES];
int process_count = 0;
static pid_t next_pid = 1;

// ===================== SAVE JSON SNAPSHOT =====================
void save_pcb_snapshot()
{
    FILE *fp = fopen("pcb_snapshot.json", "w");
    if (!fp)
    {
        perror("JSON file error");
        return;
    }

    fprintf(fp, "[\n");

    for (int i = 0; i < process_count; i++)
    {
        PCB p = process_table[i];

        fprintf(fp,
                "{ \"pid\": %lld, \"name\": \"%s\", \"state\": %d, \"priority\": %d }",
                (long long)p.pid,
                p.name,
                p.state,
                p.priority);

        if (i < process_count - 1)
            fprintf(fp, ",");

        fprintf(fp, "\n");
    }

    fprintf(fp, "]");
    fclose(fp);
}

// ===================== FORK =====================
pid_t edu_fork(PCB *parent)
{
    if (process_count >= MAX_PROCESSES)
    {
        printf("Process table full!\n");
        return -1;
    }

    PCB child = *parent;

    child.pid = next_pid++;
    child.parent_pid = parent->pid;
    child.state = NEW;
    child.creation_time = time(NULL);

    process_table[process_count++] = child;

    printf("[FORK] %lld -> created child PID %lld\n",
           (long long)parent->pid,
           (long long)child.pid);

    child.state = READY;

    save_pcb_snapshot();

    return child.pid;
}

// ===================== EXEC =====================
void edu_exec(pid_t pid, char *prog_name)
{
    for (int i = 0; i < process_count; i++)
    {
        if (process_table[i].pid == pid)
        {
            strncpy(process_table[i].name,
                    prog_name,
                    sizeof(process_table[i].name) - 1);

            process_table[i].name[sizeof(process_table[i].name) - 1] = '\0';

            process_table[i].state = RUNNING;
            process_table[i].burst_time = 100;
            process_table[i].remaining_time = 100;

            printf("[EXEC] PID %lld running %s\n",
                   (long long)pid,
                   prog_name);

            save_pcb_snapshot();
            return;
        }
    }
}

// ===================== WAIT =====================
int edu_wait(pid_t parent_pid)
{
    for (int i = 0; i < process_count; i++)
    {
        if (process_table[i].parent_pid == parent_pid)
        {
            printf("[WAIT] Parent %lld waiting...\n",
                   (long long)parent_pid);

            while (process_table[i].state != TERMINATED)
            {
                sleep(1);
            }

            return process_table[i].exit_code;
        }
    }

    return -1;
}

// ===================== EXIT =====================
void edu_exit(pid_t pid, int exit_code)
{
    for (int i = 0; i < process_count; i++)
    {
        if (process_table[i].pid == pid)
        {
            process_table[i].state = TERMINATED;
            process_table[i].exit_code = exit_code;

            printf("[EXIT] PID %lld exited with code %d\n",
                   (long long)pid,
                   exit_code);

            save_pcb_snapshot();
            return;
        }
    }
}

// ===================== PS (PROCESS TABLE) =====================
void edu_ps()
{
    printf("\n===== PROCESS TABLE =====\n");
    printf("PID\tNAME\t\tSTATE\tPRIORITY\n");

    for (int i = 0; i < process_count; i++)
    {
        printf("%lld\t%s\t\t%d\t%d\n",
               (long long)process_table[i].pid,
               process_table[i].name,
               process_table[i].state,
               process_table[i].priority);
    }

    printf("=========================\n");
}