#include "include/eduos.h"

PCB process_table[MAX_PROCESSES];
int process_count = 0;
static pid_t next_pid = 1;

void save_pcb_json() {

    FILE *fp = fopen("pcb_snapshot.json", "w");

    if (fp == NULL) {
        printf("Failed to create JSON file\n");
        return;
    }

    fprintf(fp, "[\n");

    for (int i = 0; i < process_count; i++) {

        fprintf(fp,
        "{ \"pid\": %d, \"name\": \"%s\", \"state\": %d }",
        process_table[i].pid,
        process_table[i].name,
        process_table[i].state);

        if (i < process_count - 1)
            fprintf(fp, ",");

        fprintf(fp, "\n");
    }

    fprintf(fp, "]");

    fclose(fp);
}

pid_t edu_fork(PCB *parent) {

    PCB child = *parent;

    child.pid = next_pid++;
    child.parent_pid = parent->pid;
    child.state = READY;
    child.creation_time = time(NULL);

    process_table[process_count++] = child;

    printf("[%ld] FORK: Process %d created\n",
           time(NULL),
           child.pid);

    save_pcb_json();

    return child.pid;
}

void edu_exec(pid_t pid, char *prog_name) {

    for (int i = 0; i < process_count; i++) {

        if (process_table[i].pid == pid) {

            strcpy(process_table[i].name, prog_name);

            process_table[i].remaining_time =
            process_table[i].burst_time;

            printf("[%ld] EXEC: PID %d running %s\n",
                   time(NULL),
                   pid,
                   prog_name);
        }
    }

    save_pcb_json();
}

int edu_wait(pid_t parent_pid) {

    printf("[%ld] WAIT: Parent %d waiting\n",
           time(NULL),
           parent_pid);

    Sleep(2000);

    return 0;
}

void edu_exit(pid_t pid, int exit_code) {

    for (int i = 0; i < process_count; i++) {

        if (process_table[i].pid == pid) {

            process_table[i].state = TERMINATED;
            process_table[i].exit_code = exit_code;

            printf("[%ld] EXIT: PID %d terminated\n",
                   time(NULL),
                   pid);
        }
    }

    save_pcb_json();
}

void edu_ps() {

    printf("\nPID\tNAME\tSTATE\tPRIORITY\n");

    for (int i = 0; i < process_count; i++) {

        printf("%d\t%s\t%d\t%d\n",
               process_table[i].pid,
               process_table[i].name,
               process_table[i].state,
               process_table[i].priority);
    }
}