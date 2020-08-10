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


motor_offset = 3


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

    time.sleep(2)

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

    # Set up PWM (lp = Left PWM)
    GPIO.setup(plPWM, GPIO.OUT)
    GPIO.setup(prPWM, GPIO.OUT)
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


    lp.ChangeDutyCycle(60)
    rp.ChangeDutyCycle(40)
    lDC = 60
    rDC = 40
    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)

    for i in range(0, 20):
        time.sleep(0.4)
        le = leftFE + leftBE
        re = rightFE + rightBE
        error = le - re
        # Error is negative if right side has too much power
        # Make sure its a significant difference, then add more to left
        # or remove from right: 0 <= dutycycle <= 100
        if error < -3 and lDC < 100:
            lDC += motor_offset
            rDC -= motor_offset
        elif error > 3 and  rDC < 100:
            lDC -= motor_offset
            rDC += motor_offset

        lp.ChangeDutyCycle(lDC)
        rp.ChangeDutyCycle(rDC)
        print(f'left: {le}, right: {re}')
        print(f'left: {lDC}, right: {rDC}')
        print('')

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)

    GPIO.cleanup()

except Exception as e:
    print(e)

    try:
    	GPIO.setup(5, GPIO.OUT)
    	GPIO.setup(19, GPIO.OUT)
    	GPIO.setup(13, GPIO.OUT)
    	GPIO.setup(6, GPIO.OUT)
    	GPIO.output(5, False)
    	GPIO.output(19, False)
    	GPIO.output(13, False)
    	GPIO.output(6, False)
    except:
        GPIO.cleanup()

    GPIO.cleanup()
