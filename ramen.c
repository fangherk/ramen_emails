// Mek Jenrungrot and Herrick Fang
// Chris McLeroy, Darien Joso, John Lee
// Ramen Machine Logic, Hackathon
// Turn on 3 De-multiplexers. 10/28/2017
#include "EasyPIO.h"
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <stdlib.h>

const int WAITTIME_MILLI = 5000; // 5 seconds to get ramen

const int NROWS = 3;
const int rows_pins[] = {16,20,21};

const int NCOLS = 3;
const int cols_pins[] = {13,19,26};

int isValidRow(char ch){
	// expected 'a' or 'b' or 'c'
	ch = toupper(ch);
	if(ch == 'A') return 0;
	else if(ch == 'B') return 1;
	else if(ch == 'C') return 2;
	return -1; // Unexpected value
}

int isValidCol(char ch){
	// expected 1-4
	if(ch > '4' || ch < '1') return -1;
	return ch - '1';
}

void reset(){
	// Turn off all the pins.
	for(int i=0;i<NROWS;i++) digitalWrite(rows_pins[i], 0);
	for(int i=0;i<NCOLS;i++) digitalWrite(cols_pins[i], 0);
}

// Coil Swag
void function(int row, int col){
	// Run the functions on and off. 
	printf("Call function(row=%d, col=%d)\n",row,col);
	
	
	int base;
	// Turn off all the pins 
	reset(); 
	
	// Open a ramen door.
	digitalWrite(rows_pins[row], 1);
	
	base = col*2;
	for(int i=0;i<3;i++){
		if((base&(1<<i))){
			digitalWrite(cols_pins[i], 1);
		}
	}
	
	// Keep door opening for X amount of time.
	delayMillis(WAITTIME_MILLI);
	
	// Pause the ramen door motion at open. 
	digitalWrite(rows_pins[row], 0);
	for(int i=0;i<3;i++){
		if(base&(1<<i)){
			digitalWrite(cols_pins[i], 0);
		}
	}
	
	// Close the ramen door. Reverse coil.
	digitalWrite(rows_pins[row], 1);
	base = col*2+1 ;
	for(int i=0;i<3;i++){
		if((base&(1<<i))){
			digitalWrite(cols_pins[i], 1);
		}
	}
	
	// Keep closing door for X amount of time.
	delayMillis(WAITTIME_MILLI);
	
	// Pause the ramen door motion at close.
	digitalWrite(rows_pins[row], 0);
	for(int i=0;i<3;i++){
		if(base&(1<<i)){
			digitalWrite(cols_pins[i], 0);
		}
	}
}

int main(int argc, char* argv[]){
	pioInit();

	// Set up GPIO Output Pins
	for(int i=0;i<NROWS;i++){
		pinMode(rows_pins[i], OUTPUT);
	}
	for(int i=0;i<NCOLS;i++){
		pinMode(cols_pins[i], OUTPUT);
	}

	
	// Read in ramen logic.
	if(argc == 2){
		fprintf(stdout, "Input is [%s]\n", argv[1]);
		int len = strlen(argv[1]);
		
		if(len != 2){
			fprintf(stderr, "Input of length 2. (%d given)\n", len);
			exit(0);
		}
		
		// Check for valid row and col. 
		int row = isValidRow(argv[1][0]);
		int col = isValidCol(argv[1][1]);
		
		// Incorrect input format.
		if(row == -1 || col == -1){
			fprintf(stderr, "Input format is incorrect (Regular expression (a|b|c|A|B|C)[1-4] expected)\n"); 
			exit(0);
		}
		
		// Coil Swag. 
		function(row, col);
	}else{
		fprintf(stderr, "Number of input errors. (argc expected 2, %d given)\n", argc);
		exit(0);
	}
	
	
	return 0;
}
