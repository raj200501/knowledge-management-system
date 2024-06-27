#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/sysinfo.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

#define BUFFER_SIZE 1024

void perform_secure_operations() {
    printf("Performing secure core OS operations...\n");
    // Example secure operation: File encryption (simplified)
    char *filename = "secure_file.txt";
    char *content = "This is some sensitive data.";
    char *encrypted_content = encrypt_content(content);

    int fd = open(filename, O_WRONLY | O_CREAT, 0600);
    if (fd < 0) {
        perror("Failed to open file for writing");
        return;
    }
    write(fd, encrypted_content, strlen(encrypted_content));
    close(fd);

    free(encrypted_content);
    printf("Secure file operation completed.\n");
}

char *encrypt_content(const char *content) {
    size_t len = strlen(content);
    char *encrypted_content = malloc(len + 1);
    if (!encrypted_content) {
        perror("Failed to allocate memory for encryption");
        return NULL;
    }

    for (size_t i = 0; i < len; ++i) {
        encrypted_content[i] = content[i] ^ 0xAA; // Simple XOR encryption
    }
    encrypted_content[len] = '\0';

    return encrypted_content;
}

void print_system_info() {
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

void monitor_performance() {
    printf("Monitoring system performance...\n");
    while (1) {
        print_system_info();
        sleep(5);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <operation>\n", argv[0]);
        fprintf(stderr, "Operations: secure, monitor\n");
        return 1;
    }

    if (strcmp(argv[1], "secure") == 0) {
        perform_secure_operations();
    } else if (strcmp(argv[1], "monitor") == 0) {
        monitor_performance();
    } else {
        fprintf(stderr, "Invalid operation: %s\n", argv[1]);
        return 1;
    }

    return 0;
}
