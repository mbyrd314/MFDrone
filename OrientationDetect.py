import RPi.GPIO as GPIO
import time

#pins = {2, 3, 4, 17}

#GPIO.setmode(GPIO.BCM)

#for pin in pins:
#	GPIO.setup(pin, GPIO.IN)

def read_ir(pins):
	total = 0
	status = []
	for i, pin in enumerate(pins):
		status.append( GPIO.input(pin))
		total += status[i]
	return total, status
	
def print_state(status):
	for i, s in enumerate(status):
		print("Sensor %d %d\t" %( i, s))
		
def detect(pins):
	count = 0
	i = 0
	
	while(True):
		total, status = read_ir(pins)
		
		if total == 4:
			count += 1
			print("Match detected")
		
		if i % 100 == 0:
			print_state(status)
			
		if count == 20:
			break
			
		i += 1
		#time.sleep(1)
