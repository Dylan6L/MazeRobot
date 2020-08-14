import commands as c
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


timf = []
forced_forward = False


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


def get_rightenc():
    global rightFE, rightBE
    return rightFE + rightBE


def add_time(time):
    timf.append(time)


def tune_encoders():
    print('forward_W_Enc')
    le = leftFE + leftBE
    re = rightFE + rightBE
    error = le - re
    """ Error is negative if right side has too much power
        Make sure its a significant difference, then add more to left
        and remove from right: 0 <= dutycycle <= 100 """
    if error < -3 and lDC < 100:
        lDC += motor_offset
        rDC -= motor_offset
    elif error > 3 and  rDC < 100:
        lDC -= motor_offset
        rDC += motor_offse
    lp.ChangeDutyCycle(lDC)
    rp.ChangeDutyCycle(rDC)
    print(f'Left: {lDC}, Right: {rDC}')



def turn_left():
    print("left")
    c.stop_going_forward(going_forward, start_time)
    time.sleep(1)
    c.left()
    lv.append(-1)
    direciton = c.change_direction(direction, 'left')


def main():
    global leftFE, leftBE, rightFE, rightBE, timf, forced_forward

    maze = [["O"]]
    x = 0
    y = 0

    front_clear = True
    left_clear = False

    lv = []
    going_forward = False
    start_time = 0
    direction = 0
    right_motor_speed = 30
    turn_time = 1

    # Pin values for PWM
    prPWM = 18
    plPWM = 25
    # Keep track of current duty cycle
    lDC = 0
    rDC = 0

    # Change in motor PWM when one side has too much power
    motor_offset = 3

    time.sleep(2)

    try:

        GPIO.setmode(GPIO.BCM)

        # Setup motors (all motor gpio control is done through commands.py)
        c.Setup()

        # Encoders
        GPIO.setup(cLeftFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cLeftFE, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
        GPIO.setup(cLeftBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cLeftBE, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
        GPIO.setup(cRightFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cRightFE, GPIO.BOTH, callback=sensorCallback, bouncetime=200)
        GPIO.setup(cRightBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cRightBE, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

        GPIO.setup(plPWM, GPIO.OUT)
        GPIO.setup(prPWM, GPIO.OUT)

        # Set up PWM (lp = Left PWM)
        lp = GPIO.PWM(plPWM, 100)
        lp.start(0)
        rp = GPIO.PWM(prPWM, 100)
        rp.start(0)
        lDC = 0
        rDC = 0

        while True:
            if not forced_forward:
                distancef = c.front_sense()
                if distancef > 20:
                    front_clear = True
                    if not left_clear:
                        if not going_forward:
                            c.forward(start_time)
                            going_forward = False
                            print('forward')
                            lp.ChangeDutyCycle(60)
                            rp.ChangeDutyCycle(40)
                            lDC = 60
                            rDC = 40
                        else:
                            tune_encoders()
                    else:
                        going_forward = False
                        turn_left()
                else:
                    front_clear = False
                    if not left_clear:
                        print("turn around")
                        c.stop_going_forward(start_time)
                        going_forward = False
                        time.sleep(0.3)
                        c.turn_around()
                        lv.append(-1, -1)
                        direciton = c.change_direction(direction, 'turnaround')
                    else:
                        turn_left()

                # LEFT SENSOR
                distancel = c.left_sense()
                lv.append(distancel)
                if distancel > 100:
                    left_clear = True
                    print('left Clear')
                else:
                    left_clear = False


    except Exception as e:
        print(e)
        timf.append(time.time() - start_time)
        print(timf)
        lv.append(-1)
        print(lv)
        GPIO.cleanup()



if __name__ == "__main__":
    main()
