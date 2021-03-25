from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import RPi.GPIO as GPIO

# Порт серво
panServo = 27
# Порт мотора
motor = 21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor, GPIO.OUT)

def positionServo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

# Централизация объекта
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 10
        if panAngle > 140:
            panAngle = 140
        positionServo (panServo, panAngle)
 
    if (x > 280):
        panAngle -= 10
        if panAngle < 40:
            panAngle = 40
        positionServo (panServo, panAngle)


print("[INFO] waiting for camera to warmup...")
vs = VideoStream(0).start()
time.sleep(2.0)
# Параметры цветовой модели
colorLower = (24, 100, 100)
colorUpper = (44, 255, 255)

GPIO.output(motor, GPIO.LOW)
motor_state = False

# Стартовая позиция сервопривода
global panAngle
panAngle = 90

positionServo (panServo, panAngle)

while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	#frame = imutils.rotate(frame, angle=180)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, colorLower, colorUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)


	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = cnts[0] if imutils.is_cv2() else cnts[1]
	center = None

	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			
			mapServoPosition(int(x))
			
			if not motor_state:
				GPIO.output(motor_state, GPIO.HIGH)
				motor_state = True

	elif motor_state:
		GPIO.output(motor, GPIO.LOW)
		motor_state = False

	cv2.imshow("Frame", frame)
	
	key = cv2.waitKey(1) & 0xFF
	if key == 27:
            break

# do a bit of cleanup
print("\n [INFO] Программа завершина \n")
positionServo (panServo, 90)
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()