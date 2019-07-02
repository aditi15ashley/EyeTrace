import csv
import cv2
import time

#Take values of a0-a5, b0-b5 calculated from 9point.py

x,y = [],[]#stores the coordinates on the screen we are looking at 

image = cv2.imread("image.jpg")#Tracking our gaze while we are looking at this image

with open('data.txt','r') as f:#data.txt is the file which stores our pupil coordinates in webcam frame
	reader = csv.reader(f,delimiter=' ')
	for row in reader:

		x_cam = row[0]
		y_cam = row[1]

		#mapping the pupil coordinates to the screen coordinates
		x_real = funcx((x_cam,y_cam),a0,a1,a2,a3,a4,a5)
		x_real = funcy((x_cam,y_cam),b0,b1,b2,b3,b4,b5)

		if(x_real>0 and y_real>0):
			x.append(x_real)
			y.append(y_real)

for i in range(len(x)-1):
	if i>0:
		cv2.arrowedLine(image, (int(x[i-1]),int(y[i-1])), (int(x[i]),int(y[i])), (0,0,255), 2)#arrowed line showing us the gaze

fileName = 'outputImage_' + time.strftime("%Y%m%d-%H%M") + '.png'
cv2.imwrite(fileName, image)#saving the image with our eye-gaze 
			