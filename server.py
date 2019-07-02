from flask import Flask, render_template, Response

import cv2
from eye_tracking import EyeTracking
from datetime import datetime
import numpy as np 
from scipy.optimize import curve_fit
import csv
import time


app = Flask(__name__)

curr_time = datetime.now()
formatted_time = curr_time.strftime('%H:%M:%S')
filepath1 = 'points' + formatted_time + '.txt'#actual points for prediction
filepath2 = 'calib' + formatted_time + '.txt'#points for calibration on the sceen

gaze = EyeTracking()

global webcam
webcam = cv2.VideoCapture(0)

global x_mid
global y_mid
global a0,a1,a2,a3,a4,a5#calibration result points
global b0,b1,b2,b3,b4,b5


def detect_cal():#this should be running all the time during calibration

	while True:
		_, frame = webcam.read()
		gaze.refresh(frame)
		frame = gaze.annotated_frame()

		if gaze.pupil_left_coords() is not None:
			x_left, y_left = gaze.pupil_left_coords()
			x_right, y_right = gaze.pupil_right_coords()
			x_mid = (x_left + x_right)/2
			y_mid = (y_left + y_right)/2

	return 'success'	    


def shot():
	#saves the pupil coordinates(x,y) when button is pressed 

	with open(filepath2, 'a') as fh:
		fh.write('{} {}\n'.format(x_mid, y_mid))    

	return 'success'    

def detect():	        	
	#runs all the time for prediction of eye-gaze

	while True:
		# We get a new frame from the webcam
		_, frame = webcam.read()

		# We send this frame to EyeTracking to analyze it
		gaze.refresh(frame)

		frame = gaze.annotated_frame()
		'''text = ""

		if gaze.is_blinking():
			text = "Blinking"
		elif gaze.is_right():
			text = "Looking right"
		elif gaze.is_left():
			text = "Looking left"
		elif gaze.is_center():
			text = "Looking center"

		cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)'''

		left_pupil = gaze.pupil_left_coords()
		right_pupil = gaze.pupil_right_coords()

		if gaze.pupil_left_coords() is not None:
			x_left, y_left = gaze.pupil_left_coords()
			x_right, y_right = gaze.pupil_right_coords()
			x_mid = (x_left + x_right)/2
			y_mid = (y_left + y_right)/2

			with open(filepath1, 'a') as fh:
				fh.write('{} {}\n'.format(x_mid, y_mid))


		cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
		cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

		cv2.imshow("Demo", frame)

		if cv2.waitKey(1) == 27:
			break

	return 'success'


def stop():
	#closes the webcam

	webcam.release()
	return 'success'

##helper functions for calibration
def funcx(X,a0,a1,a2,a3,a4,a5):
	x,y = X
	return a0 + a1*x + a2*y + a3*x*y + a4*x*x + a5*y*y

def funcy(X,b0,b1,b2,b3,b4,b5):
	x,y = X
	return b0 + b1*x + b2*y + b3*x*y + b4*x*x + b5*y*y

def calibrate():

	x = []
	y = []
	Sx = []
	Sy = []

	with open(filepath2,'r') as f:
		reader = csv.reader(f,delimiter=' ')

		for row in reader:

			x_cal = row[0]
			y_cal = row[1]

			x.append(x_cal)
			y.append(y_cal)

	##similarly append values of screen coordinates


	#popt = Optimal values for the parameters so that the sum of the squared residuals of f(xdata, *popt) - ydata is minimized
	poptx, pcovx = curve_fit(funcx, (x,y), Sx)
	popty, pcovy = curve_fit(funcy, (x,y), Sy)

	a0 = poptx[1]
	a1 = poptx[2]
	a2 = poptx[3]
	a3 = poptx[4]
	a4 = poptx[5]
	a5 = poptx[6]

	b0 = popty[1]
	b1 = popty[2]
	b2 = popty[3]
	b3 = popty[4]
	b4 = popty[5]
	b5 = popty[6]

	return 'success'

def eye_gaze():

	calibrate() #values of ai and bi which are global will be updated

	image = cv2.imread("image.jpg")

	x_true = []
	y_true = []

	with open('filepath1','r') as f:
		reader = csv.reader(f,delimiter=' ')
		for row in reader:

			x_cam = row[0]
			y_cam = row[1]

			x_real = funcx((x_cam,y_cam),a0,a1,a2,a3,a4,a5)
			x_real = funcy((x_cam,y_cam),b0,b1,b2,b3,b4,b5)

			if(x_real>0 and y_real>0):
				x_true.append(x_real)
				y_true.append(y_real)

	for i in range(len(x_true)-1):
		if i>0:
			cv2.arrowedLine(image, (int(x_true[i-1]),int(y_true[i-1])), (int(x_true[i]),int(y_true[i])), (0,0,255), 2)

	fileName = 'outputImage_' + time.strftime("%Y%m%d-%H%M") + '.png'
	cv2.imwrite(fileName, image)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/calibration')
def calib():
	detect_cal()
	return 'calibration process'

@app.route('/detection')
def find_points():	
	detect()
	return 'finding gaze points'

@app.route('/vstop')
def vstop():
	stop()
	return 'finish'

@app.route('/result')
def display():
	eye_gaze();
	return 'done'

	

