from tkinter import *

ts = []
turn_times = []
lv = []
turn_i = [0]
time_i = 0

maze = [[]]
mx = 0
my = 0

map_speed = 10

sense_intervals = 0
move_intervals = 0
interval_value = 0

direction = 0

root = Tk()
canvas = Canvas(root, width=1000, height=600)
canvas.pack()
of = 10

robot = canvas.create_rectangle(200, 300, 200 + of, 300 + of)
robotX = 200
robotY = 300
# robot velocity
robot_v = 40


def move_loop():
    global robotX, robotY, move_intervals, interval_value, robot, sense_intervals, turn_times, time_i
    interval_senses = turn_times[time_i]
    sense_distance = sum(interval_senses[interval_value:sense_intervals + interval_value]) / sense_intervals
    if direction == 0:
        canvas.move(robot, 5, 0)
        robotX += 5
        canvas.create_rectangle(robotX, robotY - sense_distance, robotX + of, robotY + of - sense_distance, fill='black')
    elif direction == 90:
        canvas.move(robot, 0, -5)
        robotY -= 5
        canvas.create_rectangle(robotX - sense_distance, robotY, robotX - sense_distance + of, robotY + of, fill='black')
    elif direction == 180:
        robotX -= 5
        canvas.move(robot, -5, 0)
        canvas.create_rectangle(robotX, robotY + sense_distance, robotX + of, robotY + of + sense_distance, fill='black')
    elif direction == 270:
        robot += 5
        canvas.move(robot, 0, 5)
        canvas.create_rectangle(robotX + sense_distance, robotY, robotX + sense_distance + of, robotY + of, fill='black')
    interval_value += 1
    if interval_value == move_intervals:
        time_i += 1
        root.after(0, change_direction)
        if direction == 0:
            canvas.move(robot, robot_v, -robot_v)
            robotX += robot_v
            robotY -= robot_v
        elif direction == 90:
            canvas.move(robot, -robot_v, -robot_v)
            robotX -= robot_v
            robotY -= robot_v
        elif direction == 180:
            canvas.move(robot, -robot_v, robot_v)
            robotX -= robot_v
            robotY += robot_v
        elif direction == 270:
            canvas.move(robot, robot_v, robot_v)
            robotX += robot_v
            robotY += robot_v
    else:
        root.after(map_speed, move_loop)


def move_robot():
    global time_i, direction, move_intervals, sense_intervals, interval_value

    interval_value = 0
    try:
        move_intervals = int((ts[time_i] * robot_v) / 5)
        sense_intervals = len(turn_times[time_i]) / move_intervals
        sense_intervals = round(sense_intervals)
        print(sense_intervals)
        root.after(100, move_loop())
    except IndexError:
        print('Mapping Done')


def change_direction():
    global direction
    if direction == 270:
        direction = 0
    else:
        direction += 90
    #print(direction)
    root.after(0, move_robot)


def map_path(times, left_v):
    global ts
    global lv
    global direction
    ts = times
    lv = left_v
    sense_i = 0
    for val in lv:
        sense_i += 1
        if val == -1:
            turn_i.append(sense_i)
            turn_s = lv[turn_i[-2]:(turn_i[-1]) - 1]
            turn_times.append(turn_s)
    root.after(1000, move_robot)


map_path([5.3430397510528564, 3.8243753910064697, 2.840815782546997], [51.62, 51.22, 51.28, 51.28, 51.25, 51.19, 51.64, 52.16, 51.82, 51.99, 52.06, 51.66, 51.79, 51.9, 52.42, 52.15, 52.29, 52.75, 52.77, 52.44, 52.51, 52.54, 52.59, 52.25, 52.75, 52.44, 52.88, 52.96, 53.06, 53.01, 53.04, 53.07, 53.04, 53.03, 53.09, 52.73, 53.14, 53.28, 53.18, 52.92, 53.42, 53.39, 53.31, 53.42, 53.52, 53.47, 53.51, 53.33, 53.43, 53.4, 53.35, 53.97, 53.57, 53.63, 54.13, 54.55, 54.28, 53.86, 54.4, 54.05, 54.66, 54.36, 54.72, 54.4, 54.67, 55.18, 54.86, 54.9, 55.39, 55.45, 55.22, 55.3, 55.42, 55.55, 55.5, 55.6, 55.72, 55.85, 55.99, 56.42, 56.5, 56.25, 56.41, 56.48, 56.36, 56.53, 56.57, 56.99, 56.61, 56.59, 56.73, 56.33, 56.79, 56.38, 56.77, 56.77, 56.93, 56.7, 56.86, 56.87, 56.82, 56.91, 57.01, 57.02, 57.08, 57.06, 57.51, 57.19, 57.18, 57.17, 56.69, 56.78, 57.16, 56.77, 56.76, 57.16, 56.85, 56.89, 57.33, 56.86, 57.36, 57.44, 56.84, 57.2, 56.85, 57.29, 57.27, 57.15, 57.44, 58.35, 58.5, 59.99, 60.1, 59.82, 60.35, 61.17, 61.42, 60.3, 60.51, 60.42, 61.87, 63.12, 62.3, 63.78, 64.25, 65.84, 147.03, -1, 39.81, 39.48, 40.79, 41.1, 40.39, 38.87, 39.47, 39.17, 39.55, 39.46, 40.04, 40.73, 39.74, 40.15, 40.32, 40.38, 40.61, 40.76, 41.01, 41.33, 41.63, 41.81, 42.1, 42.27, 42.33, 42.7, 42.93, 43.28, 43.47, 43.67, 43.9, 43.99, 44.02, 43.85, 44.15, 45.09, 46.14, 48.05, 49.75, 48.12, 50.39, 49.56, 680.1, -1, 40.66, 39.59, 39.87, 39.29, 39.53, 39.9, 40.14, 40.41, 40.63, 40.96, 41.2, 41.42, 42.14, 41.99, 42.21, 42.43, 43.58, 45.07, 46.28, 48.43, 57.07, 41.54, 40.66, 41.16, 40.05, 40.61, 40.65, 40.45, 40.81, 41.41, 41.21, 40.93, 41.69, 41.18, 41.52, 41.24, 41.44, 41.99, 41.7, 42.63, 42.45, 42.52, 42.85, 42.94, 42.75, 43.46, 43.86, 43.62, 44.23, 44.04, 44.56, 44.84, 44.51, 44.58, 44.82, 44.98, -1])

root.mainloop()