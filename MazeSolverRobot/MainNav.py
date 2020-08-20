import commands as c
import RPi.GPIO as GPIO
import time

# TODO after first turn encoders do not detect much
# Maybe check encoders in another script running parallel

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

rDC = 0
lDC = 0
motor_offset = 3

timf = []
forced_forward = False


def sensorCallback(channel):
    # print('callback')
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
    print(f'right: {rightFE}, {rightBE}, Left: {leftFE}, {leftBE}')


def get_rightenc():
    global rightFE, rightBE
    return rightFE + rightBE


def add_time(time):
    timf.append(time)


def tune_encoders(lp, rp):
    global lDC, rDC, motor_offset
    print('forward_W_Enc')
    le = leftFE + leftBE
    re = rightFE + rightBE
    error = le - re
    """ Error is negative if right side has too much power
        Make sure its a significant difference, then add more to left
        and remove from right: 0 <= dutycycle <= 100 """
    if error < -motor_offset and lDC < 100 - motor_offset:
        lDC += motor_offset
        rDC -= motor_offset
    elif error > motor_offset and  rDC < 100 - motor_offset:
        lDC -= motor_offset
        rDC += motor_offset
    lp.ChangeDutyCycle(lDC)
    rp.ChangeDutyCycle(rDC)
    #print(f'Left: {lDC}, Right: {rDC}')



def turn_left(start_time, lp, rp):
    global leftFE, leftBE, rightFE, rightBE, lDC, rDC
    print("left")
    c.stop_going_forward()
    time.sleep(1)
    lp.ChangeDutyCycle(100)
    rp.ChangeDutyCycle(100)
    c.left()

    # wait for full 90 turn
    rightEnc = 0
    startingRightVal = get_rightenc()
    while rightEnc - startingRightVal < 11:
        # Calculated (eng3 notebook) amount of enc values (43.173) for 90 deg turn
        print(rightEnc - startingRightVal)
        rightEnc = get_rightenc()

    c.gen_stop()
    c.force_forward()

    # force forward
    initTime = time.time()
    while time.time() - initTime < 1000:
        tune_encoders(lp, rp)

    forced_forward = False
    lv.append(-1)
    lp.ChangeDutyCycle(lDC)
    rp.ChangeDutyCycle(rDC)
    direciton = c.change_direction(direction, 'left')
    #leftFE = 0
    #leftBE = 0
    #rightFE = 0
    #rightBE = 0



def main():
    global leftFE, leftBE, rightFE, rightBE, timf, forced_forward, rDC, lDC, motor_offset

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

    time.sleep(2)

    try:

        GPIO.setmode(GPIO.BCM)

        # Setup motors (all motor gpio control is done through commands.py)
        c.Setup()

        # Encoders
        GPIO.setup(cLeftFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cLeftFE, GPIO.BOTH, callback=sensorCallback)
        GPIO.setup(cLeftBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cLeftBE, GPIO.BOTH, callback=sensorCallback)
        GPIO.setup(cRightFE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cRightFE, GPIO.BOTH, callback=sensorCallback)
        GPIO.setup(cRightBE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(cRightBE, GPIO.BOTH, callback=sensorCallback)

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
                            c.forward()
                            if not start_time > 0:
                                start_time = time.time()
                            going_forward = True
                            print('forward \n \n \n')
                            lp.ChangeDutyCycle(60)
                            rp.ChangeDutyCycle(40)
                            lDC = 60
                            rDC = 40
                        else:
                            tune_encoders(lp, rp)
                            print(f'Left: {lDC}, Right: {rDC}')
                    else:
                        time.sleep(0.3)
                        going_forward = False
                        turn_left(start_time, lp, rp)
                        add_time(time.time() - start_time)
                        start_time = 0
                else:
                    front_clear = False
                    if not left_clear:
                        print("turn around")
                        c.stop_going_forward()
                        add_time(time.time() - start_time)
                        start_time = 0
                        going_forward = False
                        time.sleep(0.3)
                        c.turn_around()

                        # wait for 180 turn to complete
                        rightEnc = 0
                        startingRightVal = get_rightenc()
                        while rightEnc - startingRightVal < 22:
                            rightEnc = get_rightenc()

                        lv.append(-1, -1)
                        direciton = c.change_direction(direction, 'turnaround')
                    else:
                        turn_left(start_time, lp, rp)
                        add_time(time.time() - start_time)
                        start_time = 0

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
