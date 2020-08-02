# Import required libraries
import time
import datetime
import RPi.GPIO as GPIO

def sensorCallback(channel):
  # Called if sensor output changes
  timestamp = time.time()
  stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
  if GPIO.input(channel):
    # No magnet
    print("Sensor HIGH " + stamp)
  else:
    # Magnet
    print("Sensor LOW " + stamp)

def main():

  # Get initial reading
  sensorCallback(22)

  try:
    while True :
      time.sleep(0.1)

  except KeyboardInterrupt:
    # Reset GPIO settings
    GPIO.cleanup()

# Tell GPIO library to use GPIO references
GPIO.setmode(GPIO.BCM)

GPIO.setup(22 , GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(22, GPIO.BOTH, callback=sensorCallback, bouncetime=200)

if __name__=="__main__":
   main()