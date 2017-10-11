//This file tests the IR circuits to ensure
//that the breakers work properly

#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <wiringPi.h>

#define DPIN 2
int main() {
    wiringPiSetupGpio();
    pinMode(DPIN,INPUT);
    digitalWrite(DPIN, HIGH);
    delay(2000);
    int prevstate;
    while(1){
        int sensorState = digitalRead(DPIN);
        if (sensorState == HIGH && sensorState != prevstate){
            printf("YOU GOT A MATCH! CONGRATS!!!!\n");
        }
        if (prevstate != sensorState && sensorState == LOW){
            printf("Your match has been broken! :(\n");
        }
        prevstate = sensorState;
      
    }
 return 0;   
}    
