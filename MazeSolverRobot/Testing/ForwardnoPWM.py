import RPi.GPIO as GPIO
import time


prPWM = 18
plPWM = 19

# Left Front Encoder Value
leftFE = 0
leftBE = 0
rightFE = 0
rightBE = 0

def sensorCallback(channel):
    global cLeftFE, cLeftBE, cRightFE, cRightBE, leftFE, leftBE, rightFE, rightBE
    # If no input then sensor went high, add value to value variable
    if not GPIO.input(channel):
        if channel == cLeftFE:
            leftFE += 1
        elif channel == cLeftBE:
            leftBE += 1
        elif channel == cRightFE:
            rightFE += 1
        elif channel == cRightBE:
            rightBE += 1

try:

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(cLeftFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(cLeftFE, GPIO.BOTH, callback=sensorCallback, bouncetime=20)
    GPIO.setup(cLeftBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(cLeftBE, GPIO.BOTH, callback=sensorCallback, bouncetime=20)
    GPIO.setup(cRightFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(cRightFE, GPIO.BOTH, callback=sensorCallback, bouncetime=20)
    GPIO.setup(cRightBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(cRightBE, GPIO.BOTH, callback=sensorCallback, bouncetime=20)

    GPIO.setup(plPWM, GPIO.OUT)
    GPIO.setup(prPWM, GPIO.OUT)

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

    for i in range(0, 100):
        time.sleep(0.5)
        print(f"leftFE: {leftFE} leftBE: {leftBE} rightFE: {rightFE} rightBE: {rightBE}")

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)

    GPIO.cleanup()

except Exception as e: 
    print(e)
    GPIO.cleanup()