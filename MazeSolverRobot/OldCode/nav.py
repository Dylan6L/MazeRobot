import RPi.GPIO as GPIO
import time

time.sleep(2)

front_clear = True
left_clear = False
forced_forward = False

timf = []
lv = []
going_forward = False
start_time = 0
direction = 0
right_motor_speed = 30
turn_time = 1


def forward():
    global start_time
    global going_forward
    going_forward = True
    if not start_time > 0:
        start_time = time.time()
    print('forward')
    p.ChangeDutyCycle(right_motor_speed)
    GPIO.output(5, True)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)


def turn_around():
    global direction
    lv.append(-1)
    lv.append(-1)

    if direction == 180:
        direction = 0
    elif direction == 0:
        direction = 180
    elif direction == 90:
        direction = 270
    elif direction == 270:
        direction = 90

    print('turn around')
    p.ChangeDutyCycle(100)
    GPIO.output(5, False)
    GPIO.output(19, True)
    GPIO.output(13, False)
    GPIO.output(6, True)
    time.sleep(turn_time * 2)
    gen_stop()

    # above stop() could cause problem with time.time


def stop_going_forward():
    global going_forward, start_time
    timf.append(time.time() - start_time)
    start_time = 0
    going_forward = False
    print('stop going forward')
    p.ChangeDutyCycle(0)
    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)


# General Stop
def gen_stop():
    print('gen stop')
    p.ChangeDutyCycle(0)
    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)


def force_forward():
    global forced_forward, start_time
    print('forcedforward')
    start_time = time.time()
    forced_forward = True
    for e in range(0, 10):
        time.sleep(0.1)
        front_dist = front_sense()
        print(front_dist)
        if front_dist > 20:
            print('forward')
            p.ChangeDutyCycle(right_motor_speed)
            GPIO.output(5, True)
            GPIO.output(19, False)
            GPIO.output(13, False)
            GPIO.output(6, True)
        else:
            stop_going_forward()
    forced_forward = False


def left():
    global direction
    lv.append(-1)

    if direction == 270:
        direction = 0
    else:
        direction += 90

    print('left')
    p.ChangeDutyCycle(100)
    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, True)
    time.sleep(turn_time)
    gen_stop()
    force_forward()


def front_sense():
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


try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    TRIG = 22
    ECHO = 16
    maxTime = 0.04
    TRIG2 = 23
    ECHO2 = 24

    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(18, GPIO.OUT)
    p = GPIO.PWM(18, 100)
    p.start(0)

    GPIO.output(5, False)
    GPIO.output(19, False)
    GPIO.output(13, False)
    GPIO.output(6, False)

    for i in range(0, 10):
        dist = front_sense()

    while True:
        if not forced_forward:
            distancef = front_sense()
            if distancef > 20:
                front_clear = True
                if not left_clear:
                    if not going_forward:
                        forward()
                else:
                    front_clear = False
                    stop_going_forward()
                    time.sleep(1)
                    left()
            else:
                if not left_clear:
                    stop_going_forward()
                    time.sleep(.3)
                    turn_around()
                else:
                    stop_going_forward()
                    time.sleep(1)
                    left()

            # LEFT SENSOR
            distancel = left_sense()
            lv.append(distancel)
            if distancel > 100:
                left_clear = True
                print('left Clear')
            else:
                left_clear = False


except:
    timf.append(time.time() - start_time)
    print(timf)
    lv.append(-1)
    print(lv)
    GPIO.cleanup()

