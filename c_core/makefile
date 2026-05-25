CC = gcc
CFLAGS = -Wall -Wextra -pthread

TARGET = eduos.exe

SRCS = main_sim.c process_manager.c thread_manager.c ipc_module.c

all:
	$(CC) $(CFLAGS) $(SRCS) -o $(TARGET)

clean:
	del $(TARGET)

race:
	# compile without mutex

fixed:
	# compile with mutex

memcheck:
	valgrind --leak-check=full ./eduos