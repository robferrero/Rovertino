import RPi.GPIO as GPIO
import time

pan = 22
sleepTime = .5

GPIO.setmode(GPIO.BOARD)

GPIO.setup(pan, GPIO.OUT)


p = GPIO.PWM(pan,50)

p.start(7.5)

for i in range(1, 4):
	time.sleep(sleepTime)
	p.ChangeDutyCycle(2.5)
	time.sleep(sleepTime)
	p.ChangeDutyCycle(12.5)

p.ChangeDutyCycle(7.5)
time.sleep(sleepTime)
	

# except KeyboardInterrupt:
GPIO.cleanup()
