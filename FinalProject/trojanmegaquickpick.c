#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <time.h>

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

// Generate 6 random white balls between 1 and 70
int white_balls_gen() {
  time_t t;
  srand((unsigned)time(&t));
  for(int i =0; i<5;i++) {
    int white_balls = rand()% 70 + 1;
    printf("%i", white_balls);
    return white_balls;
  }

// Generate 1 random mega ball between 1 and 25
int mega_ball_gen() {
  int mega_ball = rand()% 25 + 1;
  printf("%i", mega_ball);
  return mega_ball;
}

int main() {
  int quick_pick_1 [6] = {0};
  int quick_pick_2 [6] = {0};
  int quick_pick_3 [6] = {0};
  int quick_pick_4 [6] = {0};
  int quick_pick_5 [6] = {0};
  int quick_pick_6 [6] = {0};
  int quick_pick_7 [6] = {0};
  int quick_pick_8 [6] = {0};
  int quick_pick_9 [6] = {0};
  int quick_pick_10 [6] = {0};
  int quick_draw_ [6] = {0};
  
	// set up some things before we begin
	init();

	// CODE GOES HERE

	return 0;

}
