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

// Get the number of picks per draw
int get_int() {

	int i;

	scanf("%d", &i);
	while (getchar() != '\n');

	return i;
}

// Generate 6 random balls between 1 and 50
int balls_gen() {
  	time_t t;
	int balls;
	
  	srand((unsigned)time(&t));
	
  	for(int i =0; i<5;i++) {
    		balls = rand()% 50 + 1;
    		printf("%i", balls);
		
	}
    	return balls;
}

int main() {
	// Iterators
	int choice, i, p;
	
	// Quik picks
  	int quick_picks[10];

	// Quick draw
  	int quick_draw;
  
	init();

	// 
	while (1) {

		printf("Welcome To Trojans Mega Quick Picks! Are your lucky?.. Let's Play!!!");
		printf("Select the menu option?: ");
		printf("(1) Quick Picks, (2) View Pick, (3) Delete Pick, (4) Edit Pick, (5) Play Picks, (6) Cancel Play, (7) Confirm Play\n");
		printf("Choice: ");
		choice = get_int();

		switch(choice) {

			case 1:	// Quick Picks
				printf("How many picks do you want to make (10 maximum)?: ");
				i = get_int();
				for (i=0; i<10 && quick_picks[i]; i++);
					if (i < 10) {
						quick_picks[i] = malloc(24);
						quick_picks[i] = balls_gen();
						printf("Quick pick ID-#%d is: #%d", i, quick_picks[i]);
					} else {
						printf("You must specify the number of picks to play\n");
				}
				break;

			case 2: // View Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				if (i < (sizeof(quick_picks)/size(quick_picks[0]))) {
					printf("Quick pick ID-#%d is: #%d", i, quick_picks[i]);
				} else {
					printf("Invalid quick pick number\n");
				}
				break;

			case 3: // Delete Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				if (i < (sizeof(quick_picks)/size(quick_picks[0]))) {
					free(quick_picks[i]);
				} else {
					printf("Invalid quick pick ID\n");
				}
				break;

			case 4: // Edit Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				if (i < (sizeof(quick_picks)/size(quick_picks[0]))) {
					printf("Quick pick ID-#%d is: #%d", i, quick_picks[i]);
					free(quick_picks[i];
					quick_picks[i] = balls_gen();
					printf("Quick pick ID-#%d has changed to: #%d", i, quick_picks[i]);
				} else {
					printf("Invalid quick pick ID\n");
				}
				break;

			case 5: // Play Picks
				quick_draw = malloc(24);
				quick_draw = balls_gen();
				break;
			
			case 7: // Confirm Play
				for (i=0; i <= (sizeof(quick_picks)/size(quick_picks[0]))) && quick_picks[i]; i++); {
					if (quick_picks[i] == quickdraw); {
						printd("Wait while we print your Trojan Mega Quick Pick ticket\n");
						for (p=0; p < 20; p++) {
							printf("*");
						}
						sleep(5);
						printf("Congratulations!!! Your quick pick ID-#%d, pick: #%d is a match!!\n", i, quick_picks[i]);
						printf("You have $500,000,000.00 in the Trojans Mega Quick Picks\n");
						printf("Redeem your ticket at the Trojans Mega Quick Pick Office.");
					} else {
						printf("Your quick picks did not match, try again....\n");
					}
				}
				break;

			default:
				printf("Invalid choice\n");
		}
	}
	
	return 0;

}
