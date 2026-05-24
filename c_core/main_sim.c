#include "include/eduos.h"
#include "thread_manager.h"

int main()
{
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

    return 0;
}