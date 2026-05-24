#ifndef THREAD_MANAGER_H
#define THREAD_MANAGER_H

#include <pthread.h>

#define MAX_TASKS 100
#define THREAD_POOL_SIZE 4

// Task structure (like a "process job")
typedef struct {
    int task_id;
    char task_name[64];
    int duration;   // simulated execution time
} Task;

// Queue structure
typedef struct {
    Task tasks[MAX_TASKS];
    int front;
    int rear;
    int count;
} TaskQueue;

// Thread pool structure
typedef struct {
    pthread_t threads[THREAD_POOL_SIZE];
    TaskQueue queue;

    pthread_mutex_t lock;
    pthread_cond_t cond;

    int shutdown;
} ThreadPool;

// Functions
void init_thread_pool(ThreadPool *pool);
void add_task(ThreadPool *pool, Task task);
void* worker_thread(void *arg);
void destroy_thread_pool(ThreadPool *pool);

#endif