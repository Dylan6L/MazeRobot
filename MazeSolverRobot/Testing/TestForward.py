import RPi.GPIO as GPIO
import time

# Left Front Encoder Channel
cLeftFE = 16
cLeftBE = 12
cRightFE = 17
cRightBE = 4

# Left Front Encoder Value
leftFE = 0
leftBE = 0
rightFE = 0
rightBE = 0

# Pin values for PWM
prPWM = 18
plPWM = 25
# Keep track of current duty cycle
lDC = 0
rDC = 0


def sensorCallback(channel):
    # Called if sensor output changes
    timestamp = time.time()
    stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
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

    # Set up PWM (lp = Left PWM)
    lp = GPIO.PWM(plPWM, 100)
    lp.start(0)
    rp = GPIO.PWM(prPWM, 100)
    rp.start(0)
    lDC = 0
    rDC = 0


    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)


    lp.ChangeDutyCycle(50)
    rp.ChangeDutyCycle(50)
    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)

    for i in range(0, 100):
        time.sleep(0.1)
        le = leftFE + leftBE
        re = rightFE + rightBE
        error = le - re
        # Error is negative if right side has too much power
        # Make sure its a significant difference, then add more to left
        # or remove from right: 0 <= dutycycle <= 100
        if error < -20:
            if lDC < 85:
                lDC += 10
                lp.ChangeDutyCycle(lDC)
            else:
                if rDC >= 10:
                    rDC -= 10
                    rp.ChangeDutyCycle(rDC)
                elif error > 20:
                    if rDC < 85:
                        rDC += 10
                        rp.ChangeDutyCycle(rDC)
                    else:
                        # WARNING - this may not work because ldc could be 0 this way
                        if lDC >= 10:
                            lDC -= 10
                            lp.ChangeDutyCycle(lDC)
        print('left: {0}, right: {1}', lDC, rDC)

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)

    GPIO.cleanup()

except Exception as e: 
    print(e)
    print('fail')
    GPIO.cleanup()