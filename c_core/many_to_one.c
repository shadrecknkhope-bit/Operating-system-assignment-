#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 5

// shared resource (simulating kernel thread execution)
int shared_counter = 0;

void *thread_function(void *arg)
{
    int id = *(int *)arg;

    printf("Thread %d started (user-level)\n", id);

    // simulate work
    for (int i = 0; i < 3; i++) {
        shared_counter++;
        printf("Thread %d -> counter = %d\n", id, shared_counter);
        usleep(100000); // 0.1 sec
    }

    printf("Thread %d finished\n", id);
    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("=== MANY-TO-ONE THREAD MODEL SIMULATION ===\n");

    // create threads
    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, thread_function, &ids[i]);
    }

    // join threads
    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Final counter value: %d\n", shared_counter);
    printf("=== END ===\n");

    return 0;
}