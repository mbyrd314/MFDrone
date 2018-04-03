import thread
import time
import RPi.GPIO as GPIO

# Ultrasonic Sensor initialization
TRIG = 22
ECHO = 23

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)

print("Distance Measurement In Progress... ")

print("Waiting For Sensors To Settle")
time.sleep(2)

#Threading methods go here
def distance(trigger, echo):
   #Emit 10 usec pulse
    GPIO.output(trigger, True)
    time.sleep(0.00001)
    GPIO.output(trigger, False)

    pulse_start = time.time()
    pulse_end = time.time()
    #Record time for return echo
    while GPIO.input(echo) == 0:
        pulse_start = time.time()
    while GPIO.input(echo) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    dist = pulse_duration * 17150
    dist = round(dist,2)
    #print(distance)
    return dist

#Recieves directions from vision detection protocol on which direction the drone should move
#/based on alignment
def IRDetect:
    pass

def Vision:
    #Call circle detecting algorithm here
    pass

# TODO: Change from reading from android to sending to android app
#Reads in user input from Android App. Determines which sensors need to be checked for safety
def User:
    pass

if __name__ == '__main__':
    try:
        print("Measuring")
        thread.start_new_thread( distance, (TRIG, ECHO, ) )
        dist = distance(TRIG, ECHO)

    finally:
        print("Measurement stopped by User")
        GPIO.cleanup()
