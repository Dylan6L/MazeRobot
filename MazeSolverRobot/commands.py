import RPi.GPIO as GPIO
import time
import MainNav

#front
TRIG = 21
ECHO = 20
maxTime = 0.04
# Left
TRIG2 = 23
ECHO2 = 24
# Right
TRIG3 = 27
ECHO3 = 22


def Setup():
    print('setup_command')

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)


def forward():
    print('forward command')
    #print('forward')
    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)


def left():
    #print('left')
    #p.ChangeDutyCycle(100)
    GPIO.output(5, False)
    # make 19 True for pinpoint turn
    GPIO.output(19, True)
    GPIO.output(13, False)
    GPIO.output(6, True)


def force_forward():
    MainNav.forced_forward = True
    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)


def turn_around():
    #print('turn around')
    #p.ChangeDutyCycle(100)
    GPIO.output(5, False)
    GPIO.output(19, True)
    GPIO.output(13, False)
    GPIO.output(6, True)
    # stop() could cause problem with time.time  EDIT: changed to gen_stop I think
    gen_stop()


def gen_stop():
    #print('gen stop')
    #p.ChangeDutyCycle(0)
    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)


def stop_going_forward():
    #print('stop going forward')
    #p.ChangeDutyCycle(0)
    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)


def front_sense():
    global TRIG, ECHO, maxTime
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)

    GPIO.output(TRIG, False)

    time.sleep(0.01)

    GPIO.output(TRIG, True)

    time.sleep(0.00001)

    GPIO.output(TRIG, False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance





def left_sense():
    global TRIG2, ECHO2, maxTime
    GPIO.setup(TRIG2, GPIO.OUT)
    GPIO.setup(ECHO2, GPIO.IN)

    GPIO.output(TRIG2, False)

    time.sleep(0.01)

    GPIO.output(TRIG2, True)

    time.sleep(0.00001)

    GPIO.output(TRIG2, False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO2) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO2) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    # print(distance)
    return distance



def right_sense():
    global TRIG3, ECHO3, maxTime
    GPIO.setup(TRIG3, GPIO.OUT)
    GPIO.setup(ECHO3, GPIO.IN)

    GPIO.output(TRIG3, False)

    time.sleep(0.01)

    GPIO.output(TRIG3, True)

    time.sleep(0.00001)

    GPIO.output(TRIG3, False)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO3) == 0 and pulse_start < timeout:
        pulse_start = time.time()

    pulse_end = time.time()
    timeout = pulse_end + maxTime
    while GPIO.input(ECHO3) == 1 and pulse_end < timeout:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance


def change_direction(cur_direction, turn_direction):

    direction = cur_direction

    if turn_direction == 'turnaround':
        if cur_direction == 180:
            direction = 0
        elif cur_direction == 0:
            direction = 180
        elif cur_direction == 90:
            direction = 270
        elif cur_direction == 270:
            direction = 90
    elif turn_direction == 'left':
        if cur_direction == 270:
            direction = 0
        else:
            direction += 90
    elif turn_direction == 'right':
        if cur_direction == 0:
            direction = 270
        else:
            direction += 90

    return direciton


def sense_all():
    senses = []

    if (left_sense() < 20):
        senses.append(True)
    else:
        senses.append(False)

    if (front_sense() < 20):
        senses.append(True)
    else:
        senses.append(False)

    if (right_sense() < 20):
        senses.append(True)
    else:
        senses.append(False)

    return senses


def clean():
    GPIO.cleanup()
