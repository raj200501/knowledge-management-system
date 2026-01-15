#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <getopt.h>

#define BUFFER_SIZE 1024

static char *encrypt_content(const char *content) {
    size_t len = strlen(content);
    char *encrypted_content = malloc(len + 1);
    if (!encrypted_content) {
        perror("Failed to allocate memory for encryption");
        return NULL;
    }

    for (size_t i = 0; i < len; ++i) {
        encrypted_content[i] = content[i] ^ 0xAA;
    }
    encrypted_content[len] = '\0';

    return encrypted_content;
}

static int write_secure_file(const char *filename, const char *content) {
    char *encrypted_content = encrypt_content(content);
    if (!encrypted_content) {
        return 1;
    }

    int fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (fd < 0) {
        perror("Failed to open file for writing");
        free(encrypted_content);
        return 1;
    }
    write(fd, encrypted_content, strlen(encrypted_content));
    close(fd);

    free(encrypted_content);
    return 0;
}

static void perform_secure_operations() {
    printf("Performing secure core OS operations...\n");
    if (write_secure_file("secure_file.txt", "This is some sensitive data.")) {
        fprintf(stderr, "Secure file operation failed.\n");
        return;
    }
    printf("Secure file operation completed.\n");
}

static void print_system_info() {
    struct sysinfo sys_info;
    if (sysinfo(&sys_info) != 0) {
        perror("sysinfo");
        return;
    }

    printf("System uptime: %ld seconds\n", sys_info.uptime);
    printf("Total RAM: %lu MB\n", sys_info.totalram / (1024 * 1024));
    printf("Free RAM: %lu MB\n", sys_info.freeram / (1024 * 1024));
    printf("Process count: %d\n", sys_info.procs);
}

static void monitor_performance(int iterations, int interval) {
    printf("Monitoring system performance...\n");
    for (int i = 0; i < iterations; i++) {
        print_system_info();
        sleep(interval);
    }
}

static void print_usage(const char *program) {
    fprintf(stderr, "Usage: %s <operation> [options]\n", program);
    fprintf(stderr, "Operations: secure, monitor\n");
    fprintf(stderr, "Options for monitor:\n");
    fprintf(stderr, "  --iterations <n>  Number of iterations (default: 3)\n");
    fprintf(stderr, "  --interval <n>    Seconds between checks (default: 1)\n");
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        print_usage(argv[0]);
        return 1;
    }

    const char *operation = argv[1];
    int iterations = 3;
    int interval = 1;

    if (strcmp(operation, "monitor") == 0) {
        static struct option long_options[] = {
            {"iterations", required_argument, 0, 'i'},
            {"interval", required_argument, 0, 't'},
            {0, 0, 0, 0}
        };

        int opt;
        int option_index = 0;
        while ((opt = getopt_long(argc - 1, argv + 1, "", long_options, &option_index)) != -1) {
            switch (opt) {
                case 'i':
                    iterations = atoi(optarg);
                    break;
                case 't':
                    interval = atoi(optarg);
                    break;
                default:
                    print_usage(argv[0]);
                    return 1;
            }
        }

        if (iterations <= 0) {
            fprintf(stderr, "Iterations must be positive.\n");
            return 1;
        }
        if (interval <= 0) {
            fprintf(stderr, "Interval must be positive.\n");
            return 1;
        }

        monitor_performance(iterations, interval);
        return 0;
    }

    if (strcmp(operation, "secure") == 0) {
        perform_secure_operations();
        return 0;
    }

    fprintf(stderr, "Invalid operation: %s\n", operation);
    print_usage(argv[0]);
    return 1;
}
