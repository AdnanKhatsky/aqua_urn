from __future__ import print_function
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import RPi.GPIO as GPIO

# Подключение мотора
motor = 21
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(redLed, GPIO.OUT)

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())

print("[INFO] waiting for camera to warmup...")
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)
# Параметры цветовой модели
colorLower = (24, 100, 100) 
colorUpper = (44, 255, 255) 

print("\n Запуск..... ==> Нажми 'esc' чтобы завершить \n")
GPIO.output(redLed, GPIO.LOW)
motor_state = False

while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	frame = imutils.rotate(frame, angle=180)
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

			if not motor_state:
				GPIO.output(redLed, GPIO.HIGH)
				ledOn = True

	elif motor_state:
		GPIO.output(redLed, GPIO.LOW)
		motor_state = False

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	if (key == 27):
		break

print("\n Программа была завершина \n")
GPIO.cleanup()
cv2.destroyAllWindows()
vs.stop()