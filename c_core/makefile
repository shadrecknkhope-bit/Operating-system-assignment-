CC = gcc

CFLAGS = -Wall -Wextra -pthread -std=c11

SRCS = main_sim.c process_manager.c thread_manager.c ipc_module.c

TARGET = eduos

all:
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

race:
	$(CC) $(CFLAGS) race_demo.c -o race_demo

fixed:
	$(CC) $(CFLAGS) fixed_demo.c -o fixed_demo

many_to_one:
	$(CC) $(CFLAGS) many_to_one.c -o many_to_one

memcheck:
	valgrind --leak-check=full ./$(TARGET)

clean:
	del /Q *.exe 2>nul || rm -f *.exe