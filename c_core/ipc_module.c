#include "include/eduos.h"

#define MAX_MESSAGES 10
#define MESSAGE_SIZE 256

typedef struct {
    int pid;
    char message[MESSAGE_SIZE];
} IPCMessage;

IPCMessage message_queue[MAX_MESSAGES];
int msg_count = 0;

/* Initialize IPC */
void ipc_init() {
    msg_count = 0;
    printf("IPC Module Initialized\n");
}

/* Send Message */
void ipc_send(pid_t pid, const char *msg) {

    if (msg_count >= MAX_MESSAGES) {
        printf("Message Queue Full\n");
        return;
    }

    message_queue[msg_count].pid = pid;

    strcpy(message_queue[msg_count].message, msg);

    printf("Message sent to PID %lld: %s\n",
           (long long)pid,
           msg);

    msg_count++;
}

/* Receive Message */
void ipc_receive(pid_t pid) {

    for (int i = 0; i < msg_count; i++) {

        if (message_queue[i].pid == pid) {

            printf("PID %lld received: %s\n",
                   (long long)pid,
                   message_queue[i].message);

            return;
        }
    }

    printf("No messages for PID %lld\n",
           (long long)pid);
}

/* Cleanup IPC */
void ipc_cleanup() {
    msg_count = 0;
    printf("IPC Module Cleaned Up\n");

}

/* Simulated Pipe IPC */
void demo_pipe_ipc() {

    printf("\n=== PIPE IPC DEMO ===\n");

    char pipe_data[100] = "Message through simulated pipe";

    printf("Writing to pipe...\n");

    printf("Reading from pipe...\n");

    printf("Received: %s\n", pipe_data);
}

/* Simulated Shared Memory */
void demo_shared_memory() {

    printf("\n=== SHARED MEMORY DEMO ===\n");

    char shared_memory[100];

    strcpy(shared_memory, "Shared memory communication");

    printf("Shared Memory Contains: %s\n", shared_memory);
}