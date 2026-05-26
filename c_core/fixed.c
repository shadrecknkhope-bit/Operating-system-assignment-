// fixed.c
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 5

int shared_counter = 0;
pthread_mutex_t lock;

void *increment(void *arg)
{
    int id = *(int *)arg;

    for (int i = 0; i < 100000; i++) {

        pthread_mutex_lock(&lock);   // 🔒 LOCK

        shared_counter++;

        pthread_mutex_unlock(&lock); // 🔓 UNLOCK
    }

    printf("Thread %d done\n", id);
    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    pthread_mutex_init(&lock, NULL);

    printf("=== FIXED VERSION (MUTEX PROTECTED) ===\n");

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, increment, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    pthread_mutex_destroy(&lock);

    printf("Expected: %d\n", NUM_THREADS * 100000);
    printf("Actual:   %d\n", shared_counter);

    printf("=== END ===\n");

    return 0;
}