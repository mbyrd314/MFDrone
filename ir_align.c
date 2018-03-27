//This file tests the IR circuits to ensure
//that the breakers work properly

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <wiringPi.h>


//Initializes all IR pins given an arra of the GPIO pinout numbers and array size
void initialize_ir(int *pin_nums, int size){
    
    wiringPiSetupGpio();    
    for(int i = 0; i < size; i++){
        pinMode(pin_nums[i], INPUT);
        digitalWrite(pin_nums[i], HIGH);
        
    }
    
    printf("Initializing IR sensor ...\n");
    delay(2000);
    
}
// Read values of all IR sensors and return total number of sensors that are aligned
int read_ir(int *pin_nums, int size, int *ir_status){
     int total = 0;
     for(int i = 0; i < size; i++){
        ir_status[i] = digitalRead(pin_nums[i]);
        total += ir_status[i];
     }
     return total;

}
//Prints current status of all IR pins
void print_state(int *ir_status, int size){
    for(int i = 0; i < size; i++){
        printf("Sensor %d: %d \t", i,ir_status[i]);
    }
    printf("\n");
}

/*
int main() {
    // Initialize sensors
    int a_size = 4;
    int pinout[] = {2,3,4,17};
    int ir_status[a_size];
    long i;
    int allstate;


    initialize_ir(pinout, a_size);


    while(1){
        allstate = read_ir(pinout,a_size,ir_status);

       //  printf("%d\n", allstate);
 
        if (allstate == a_size){
            printf("YOU GOT A MATCH! CONGRATS!!!!\n");
        }
        else if(i%100 == 0){
             print_state(ir_status, a_size);
        }
       i++;
    }
 return 0;
}*/
