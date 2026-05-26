#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#define NUM_THREADS 5

int shared_counter = 0;

void *increment(void *arg)
{
    int id = *(int *)arg;

    for (int i = 0; i < 100000; i++) {
        // ❌ NO MUTEX -> race condition happens here
        shared_counter++;
    }

    printf("Thread %d done\n", id);
    return NULL;
}

int main()
{
    pthread_t threads[NUM_THREADS];
    int ids[NUM_THREADS];

    printf("=== RACE CONDITION DEMO (UNSAFE) ===\n");

    for (int i = 0; i < NUM_THREADS; i++) {
        ids[i] = i + 1;
        pthread_create(&threads[i], NULL, increment, &ids[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }

    printf("Expected: %d\n", NUM_THREADS * 100000);
    printf("Actual:   %d\n", shared_counter);

    printf("=== END ===\n");

    return 0;
}