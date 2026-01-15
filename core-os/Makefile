CC=gcc
CFLAGS=-Wall -Wextra -O2

all: core_os_module

core_os_module: core_os_module.o
	$(CC) $(CFLAGS) -o core_os_module core_os_module.o

core_os_module.o: core_os_module.c
	$(CC) $(CFLAGS) -c core_os_module.c

clean:
	rm -f core_os_module core_os_module.o
