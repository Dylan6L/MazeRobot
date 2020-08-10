import PID, time, os
import RPi.GPIO as GPIO

time.sleep(5)

targetT = 0
P = 2
I = 1
D = 1

dir = ''

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

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

def readConfig ():
	global targetT
	with open ('/tmp/pid.conf', 'r') as f:
		config = f.readline().split(',')
		pid.SetPoint = float(config[0])
		targetT = pid.SetPoint
		pid.setKp (float(config[1]))
		pid.setKi (float(config[2]))
		pid.setKd (float(config[3]))

def createConfig ():
	if not os.path.isfile('/tmp/pid.conf'):
		with open ('/tmp.pid.conf', 'w') as f:
			f.write('%s,%s,%s,%s'%(targetT,P,I,D))


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


def main():
	try:

		#createConfig()

		pid.setKp (P)
		pid.setKi (I)
		pid.setKd (D)

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


		lp.ChangeDutyCycle(50)
		rp.ChangeDutyCycle(50)
		lDC = 50
		rDC = 50
		GPIO.output(5, True)
		GPIO.output(19, False)
		GPIO.output(13, False)
		GPIO.output(6, True)


		for i in range(0, 40):

			#readConfig()

			# calculate error form encoders
			le = leftFE + leftBE
			re = rightFE + rightBE
			error = le - re

			pid.update(error)
			targetPwm = pid.output
			dir = 'right' if targetPwm > 0 else 'left'
			print(str(dir) + ' ' + str(targetPwm))
			targetPwm = abs(targetPwm)
			targetPwm = max(min( int(targetPwm), 100 ),0)

			print ("Target: %.1f | Current: %.1f | PWM: %s %%"%(targetT, error, targetPwm))

			if dir == 'left':
				lDC = targetPwm
				#if lDC + targetPwm < 101:
				#	lDC += targetPwm
				#else:
				#	lDC = 100
				#lp.ChangeDutyCycle(lDC)
			else:
				rDC = targetPwm
				#if rDC + targetPwm < 101:
				#	rDC += targetPwm
				#else:
				#	rDC = 100
				#rp.ChangeDutyCycle(targetPwm)

			time.sleep(0.2)

		GPIO.output(5, False)
		GPIO.output(19, False)
		GPIO.output(13, False)
		GPIO.output(6, False)

		GPIO.cleanup()

	except Exception as e:
		print(e)
		GPIO.cleanup()



if __name__ == "__main__":
	main()
