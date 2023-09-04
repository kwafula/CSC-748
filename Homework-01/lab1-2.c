#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

void sig_handler(int signum) {

	printf("Timeout\n");
	exit(0);

}

void init() {

	alarm(60);
	signal(SIGALRM, sig_handler);

	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	chdir(getenv("HOME"));

}

void win() {

	alarm(0);
	execl("/bin/bash", "/bin/bash", NULL);

}

int main() {

	long ptr;

	init();

	printf("Hello! Give me a pointer, (as a decimal number), and I'll call it. :)\n");

	scanf("%ld", &ptr);

	((void(*)(void)) ptr)();

	return 0;

}
