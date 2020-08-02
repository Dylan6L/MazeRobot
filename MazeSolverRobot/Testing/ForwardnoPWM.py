import RPi.GPIO as GPIO
import time


prPWM = 18
plPWM = 19

try:

    GPIO.setmode(GPIO.BCM)

    lp = GPIO.PWM(plPWM, 100)
    lp.start(0)
    rp = GPIO.PWM(prPWM, 100)
    rp.start(0)

    lp.ChangeDutyCycle(50)
    rp.ChangeDutyCycle(50)

    # 26 and 5 are for left motors

    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)

    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)

    time.sleep(5)

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)

    GPIO.cleanup()

except Exception as e: 
    print(e)
    GPIO.cleanup()