import numpy as np 
from scipy.optimize import curve_fit


def funcx(X,a0,a1,a2,a3,a4,a5):
	x,y = X
	return a0 + a1*x + a2*y + a3*x*y + a4*x*x + a5*y*y

def funcy(X,b0,b1,b2,b3,b4,b5):
	x,y = X
	return b0 + b1*x + b2*y + b3*x*y + b4*x*x + b5*y*y	

#We click on 9 points on the screen and store the results here 
#pupil coordinates in the webcam frame
x = []
y = []
#Screen coordinates where we click
Sx = []
Sy = []


#The following tries to achieve a mapping between the pupil coordinates and where we are looking at on the screeen

#popt = Optimal values for the parameters so that the sum of the squared residuals of [f(xdata, *popt) - ydata] is minimized
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






