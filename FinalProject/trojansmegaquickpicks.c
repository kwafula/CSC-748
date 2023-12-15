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
    		printf("%i ", balls);

	}
    	return balls;
}

int main() {
	// Iterators
	int choice, i, j, *p;
	
	// Quik picks
  	int quick_picks[10];

	// Quick draw
  	int quick_draw;
  
	init();

	// 
	printf("Welcome To Trojans Mega Quick Picks! Are your lucky?.. Let's Play!!!\n");
	while (1) {

		printf("Select the menu option?: \n");
		printf("(1) Quick Picks, (2) View Pick, (3) Delete Pick, (4) Edit Pick, (5) Play Picks, (6) Confirm The Play\n");
		printf("Choice: ");
		choice = get_int();
		printf("\n\n");

		switch(choice) {

			case 1:	// Quick Picks
				printf("How many picks do you want to make (10 maximum)?: ");
				i = get_int();
				printf("\n");
				for (i=0; i<10 && quick_picks[i]; i++) {
					if (i < 10) {
						p = (quick_picks + i);
						p = malloc(24);
						*p = balls_gen();
						quick_picks[i] = *(p + i);
						printf("Quick pick ID-#%d is: %i\n", i, quick_picks[i]);
					} else {
						printf("You must specify the number of picks to play\n\n");
					}
				}
				break;

			case 2: // View Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				printf("\n");
				if (i < (sizeof(quick_picks)/sizeof(quick_picks[0]))) {
					printf("Quick pick ID-#%d is: %i\n\n", i, quick_picks[i]);
				} else {
					printf("Invalid quick pick number\n\n");
				}
				break;

			case 3: // Delete Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				printf("\n\n");
				if (i < (sizeof(quick_picks)/sizeof(quick_picks[0]))) {
					p = (quick_picks + i);
					free(p);
				} else {
					printf("Invalid quick pick ID\n\n");
				}
				break;

			case 4: // Edit Pick
				printf("Enter quick pick ID: ");
				i = get_int();
				printf("\n");
				if (i < (sizeof(quick_picks)/sizeof(quick_picks[0]))) {
					printf("Quick pick ID-#%d is: %i\n", i, quick_picks[i]);
					p = (quick_picks + i);
					free(p);
					*p = balls_gen();
					printf("Quick pick ID-#%d has changed to: %i\n\n", i, quick_picks[i]);
				} else {
					printf("Invalid quick pick ID\n\n");
				}
				break;

			case 5: // Play Picks
				p = &quick_draw;
				p = malloc(24);
				*p = balls_gen();
				break;
			
			case 7: // Confirm Play
				for (i=0; i <= ( (sizeof(quick_picks)/sizeof(quick_picks[0])) ) && quick_picks[i]; i++) {
					if (quick_picks[i] == quick_draw) {
						printf("Wait while we print your Trojan Mega Quick Pick ticket\n");
						for (j=0; j < 20; j++) {
							printf("*");
						}
						printf("\n");
						sleep(5);
						printf("Congratulations!!! Your quick pick ID-#%d, pick: %i is a match!!\n", i, quick_picks[i]);
						printf("You have won $500,000,000.00 in the Trojans Mega Quick Picks\n");
						printf("Redeem your ticket at the Trojans Mega Quick Pick Office.\n\n");
					} else {
						printf("Your quick picks did not match, try again....\n\n");
					}
				}
				break;

			default:
				printf("Invalid choice\n\n");
		}
	
	}
	return 0;
	
}
