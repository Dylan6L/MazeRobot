import Commands as c
import RPi.GPIO as GPIO
import time

maze = [["O"]]
x = 0
y = 0

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


try:

    c.Setup()

    for i in range(0, 10):
        dist = front_sense()

    while True: 
        if not forced_forward:
            distancef = c.front_sense()
            if distancef > 20:
                front_clear = True
                if not left_clear:
                    if not going_forward:
                        c.forward(start_time, going_forward)
                else:
                    front_clear = False
                    c.stop_going_forward()
                    time.sleep(1)
                    c.left(direction)
            else:
                if not left_clear:
                    c.stop_going_forward(going_forward, start_time)
                    time.sleep(0.3)
                    c.turn_around()
                    direciton = c.change_direction(direction, 'turnaround')
                else:
                    c.stop_going_forward(going_forward, start_time)
                    time.sleep(1)
                    c.left()
                    direciton = c.change_direction(direction, 'left')

            # LEFT SENSOR
            distancel = c.left_sense()
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