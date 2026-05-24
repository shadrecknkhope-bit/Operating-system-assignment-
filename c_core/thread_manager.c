#include "thread_manager.h"
#include <stdio.h>
#include <unistd.h>
#include <string.h>

// ================= QUEUE FUNCTIONS =================

static void queue_init(TaskQueue *q)
{
    q->front = 0;
    q->rear = 0;
    q->count = 0;
}

static void queue_push(TaskQueue *q, Task task)
{
    if (q->count >= MAX_TASKS)
    {
        printf("Queue full!\n");
        return;
    }

    q->tasks[q->rear] = task;
    q->rear = (q->rear + 1) % MAX_TASKS;
    q->count++;
}

static Task queue_pop(TaskQueue *q)
{
    Task t = {0};

    if (q->count == 0)
        return t;

    t = q->tasks[q->front];
    q->front = (q->front + 1) % MAX_TASKS;
    q->count--;

    return t;
}

// ================= WORKER THREAD =================

void* worker_thread(void *arg)
{
    ThreadPool *pool = (ThreadPool*)arg;

    while (1)
    {
        pthread_mutex_lock(&pool->lock);

        while (pool->queue.count == 0 && !pool->shutdown)
        {
            pthread_cond_wait(&pool->cond, &pool->lock);
        }

        if (pool->shutdown)
        {
            pthread_mutex_unlock(&pool->lock);
            break;
        }

        Task task = queue_pop(&pool->queue);

        pthread_mutex_unlock(&pool->lock);

        printf("[THREAD %llu] Executing Task %d: %s\n",
               (unsigned long long)pthread_self(),
               task.task_id,
               task.task_name);

        sleep(task.duration);
    }

    return NULL;
}

// ================= INIT THREAD POOL =================

void init_thread_pool(ThreadPool *pool)
{
    pool->shutdown = 0;
    queue_init(&pool->queue);

    pthread_mutex_init(&pool->lock, NULL);
    pthread_cond_init(&pool->cond, NULL);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        pthread_create(&pool->threads[i], NULL, worker_thread, pool);
    }

    printf("[THREAD POOL] Initialized with %d threads\n", THREAD_POOL_SIZE);
}

// ================= ADD TASK =================

void add_task(ThreadPool *pool, Task task)
{
    pthread_mutex_lock(&pool->lock);

    queue_push(&pool->queue, task);

    pthread_cond_signal(&pool->cond);

    pthread_mutex_unlock(&pool->lock);

    printf("[TASK ADDED] %d - %s\n",
           task.task_id,
           task.task_name);
}

// ================= DESTROY POOL =================

void destroy_thread_pool(ThreadPool *pool)
{
    pthread_mutex_lock(&pool->lock);
    pool->shutdown = 1;
    pthread_cond_broadcast(&pool->cond);
    pthread_mutex_unlock(&pool->lock);

    for (int i = 0; i < THREAD_POOL_SIZE; i++)
    {
        pthread_join(pool->threads[i], NULL);
    }

    pthread_mutex_destroy(&pool->lock);
    pthread_cond_destroy(&pool->cond);

    printf("[THREAD POOL] Shutdown complete\n");
}