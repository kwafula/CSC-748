
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>

char charset[] = "abcdefghijklmnopqrstuvwxyz0123456789";
char rand_text[16];
char input_text[16];

void sig_handler(int signum) {

    printf("Too slow :(\n");
    exit(0);

}

void init() {

    int i;

    srand(time(0) * getpid());

    for (i=0; i<15; i++)
        rand_text[i] = charset[rand() % (sizeof(charset) - 1)];

    chdir(getenv("HOME"));

    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);

    alarm(1);
    signal(SIGALRM, sig_handler);

}

int main() {

    init();

    printf(
        "Hello! Echo the following string back\n"
        "to me in <= 1 second, win a shell.\n"
        "\n"
    );

    printf("%s\n\n", rand_text);

    scanf("%15s", input_text);

    if (strncmp(input_text, rand_text, 16) == 0) {
        alarm(0);
        execl("/bin/bash", "/bin/bash", NULL);
    } else {
        printf("Incorrect :(\n");
    }

    return 0;

}
