import sys
import numpy as np
import cv2blue = sys.argv[1]
green = sys.argv[2]
red = sys.argv[3]  color = np.uint8([[[blue, green, red]]])
hsv_color = cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
hue = hsv_color[0][0][0]print("Нижние границы цвета :"),
print("[" + str(hue-10) + ", 100, 100]\n")
print("Верхние границы цвета :"),
print("[" + str(hue + 10) + ", 255, 255]")