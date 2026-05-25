#include "include/eduos.h"
#include "thread_manager.h"
#include <stdio.h>

void write_pcb_snapshot() {
    FILE *f = fopen("pcb_snapshot.json", "w");

    if (!f) {
        perror("fopen failed");
        return;
    }

    if (f == NULL) {
        printf("Failed to create PCB file\n");
        return;
    }

    fprintf(f, "[\n");

    fprintf(f, "  {\"pid\": \"P1\", \"arrival\": 0, \"burst\": 5},\n");
    fprintf(f, "  {\"pid\": \"P2\", \"arrival\": 1, \"burst\": 3},\n");
    fprintf(f, "  {\"pid\": \"P3\", \"arrival\": 2, \"burst\": 4}\n");

    fprintf(f, "]\n");

    fclose(f);

    printf("[PCB] Snapshot written successfully\n");
}


int main()
{
    write_pcb_snapshot();

    //thread
    ThreadPool pool;

    init_thread_pool(&pool);

    Task t1 = {1, "Load Process Table", 2};
    Task t2 = {2, "Schedule Processes", 3};
    Task t3 = {3, "Execute PCB", 1};

    add_task(&pool, t1);
    add_task(&pool, t2);
    add_task(&pool, t3);

    sleep(10);

    destroy_thread_pool(&pool);

    //ipc
    printf("=== IPC DEMO START ===\n");

    demo_pipe_ipc();

    printf("\n----------------------\n");

    demo_shared_memory();

    printf("=== IPC DEMO END ===\n");

    return 0;
}