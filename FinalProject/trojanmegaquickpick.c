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

// Get the number of pick per draw
int num_picks() {

	int i;

	scanf("%d", &i);
	while (getchar() != '\n');

	return i;
}

// Generate 6 random white balls between 1 and 70
int white_balls_gen() {
  	time_t t;
	int white_balls
  	srand((unsigned)time(&t));
  	for(int i =0; i<5;i++) {
    		white_balls = rand()% 70 + 1;
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
	// Quik picks
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

	// Quick draw
  	int quick_draw_ [6] = {0};
  
	init();

	// CODE GOES HERE
	while (1) {

		printf("What would you like to do?: ");
		printf("(1) New, (2) View, (3) Delete, (4) Edit, (5) Load flag into memory\n");
		printf("Choice: ");
		choice = get_int();

		switch(choice) {

			case 1:	// New
				for (i=0; i<32 && notes[i]; i++);
				if (i < 32) {
					notes[i] = malloc(64);
					printf("Contents: ");
					scanf("%63s", notes[i]);		// safe! no overflow here
					printf("Note saved! (ID#%d)\n", i);
				} else {
					printf("sorry, too many notes\n");
				}
				break;

			case 2: // View
				printf("Note ID?: ");
				choice = get_int();
				if (choice >= 0 && choice < 32) {
					printf("Contents: ");
					write(1, notes[choice], 64);
				} else
					printf("Invalid note ID\n");
				break;

			case 3: // Delete
				printf("Note ID?: ");
				choice = get_int();
				if (choice >= 0 && choice < 32)
					free(notes[choice]);
				else
					printf("Invalid note ID\n");
				break;

			case 4: // Edit
				printf("Hacker tool, not allowed! >:(\n");
				break;

			case 5: // Load flag into memory
				fp = fopen("flag.txt", "r");
				flag = malloc(64);
				fgets(flag, 64, fp);
				fclose(fp);
				break;

			default:
				printf("Invalid choice\n");

	return 0;

}
