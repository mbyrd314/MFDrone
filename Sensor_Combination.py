import threading
import time
import RPi.GPIO as GPIO
import DroneDetect as DD
import OrientationDetect as OD

# Ultrasonic Sensor initialization
GPIO.setmode(GPIO.BCM)

TRIG = 2
ECHO = 3
#PINS = [4, 17, 22, 23]
PINS = [4]
Actuate = 0
Yaw =0
Rotate_Begin = 0

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG, False)
for pin in PINS:
	GPIO.setup(pin, GPIO.IN)


class myThread( threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		distance()

class myVisionThread( threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		DD.circle_detect()

class myIRThread( threading.Thread):
	def __init__(self, threadID, name, pins):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.pins = pins

	def run(self):
		while(True):
			if Rotate_Begin == 1:
				OD.detect(self.pins)
				Yaw = 1
				break
class ControlSystem(threading.Thread):
	def __init__(self, threadID, name):
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name

	def run(self):
		if Yaw and Actuate:
			print("Motor Actuation Begin")


#Threading methods go here
def distance():
	trigger =  TRIG
	echo = ECHO
	print("Distance Measurement In Progress... ")

	print("Waiting For Sensors To Settle")
	time.sleep(2)

	while(True):
	   #Emit 10 usec pulse
		GPIO.output(trigger, True)
		time.sleep(0.00001)
		GPIO.output(trigger, False)

		pulse_start = time.time()
		pulse_end = time.time()

	    #Record time for return echo
		while GPIO.input(echo) == 0 :
			pulse_start = time.time()
		while GPIO.input(echo) == 1:
			pulse_end = time.time()

		pulse_duration = pulse_end - pulse_start
		dist = pulse_duration * 17150
		dist = round(dist,2)
		print(dist)
		if dist < 15:
			Actuate = 1
		if dist < 50:
			Rotate_Begin = 1
		time.sleep(1)
	    #return dist


	

#Create new thread
ultrasonic_thread = myThread(1,"Thread1" )
vision_thread = myVisionThread(2,"Thread2" )
ir_thread = myIRThread(3,"Thread3", PINS)

#start new thread
ultrasonic_thread.start()
vision_thread.start()
ir_thread.start()

ultrasonic_thread.join()
vision_thread.join()
ir_thread.join()

print("Measurement stopped by User")
GPIO.cleanup()

