#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

// catches the timeout signal and exits the program
void sig_handler(int signum) {

	printf("Timeout\n");
	exit(0);

}

void init() {

	// set up a 60-second timeout
	alarm(60);
	signal(SIGALRM, sig_handler);

	// disable I/O buffering.  this makes interaction more predictable
	setvbuf(stdin, NULL, _IONBF, 0);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);

	// switch to the current user's home directory.
	chdir(getenv("HOME"));

}

int main() {

	// set up some things before we begin
	init();

	// CODE GOES HERE

	return 0;

}
