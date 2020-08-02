import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 100)
p.start(0)

try:
    p.ChangeDutyCycle(40)
    GPIO.output(5, False)
    GPIO.output(19, True)
    GPIO.output(13, True)
    GPIO.output(6, False)
    time.sleep(1)
    p.ChangeDutyCycle(0)
    GPIO.output(19, False)
    GPIO.output(6, False)
    GPIO.output(13, False)
    GPIO.output(5, False)

    GPIO.cleanup()

except:
    GPIO.cleanup()

