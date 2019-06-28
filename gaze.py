import cv2
from eye_tracking import EyeTracking
from datetime import datetime
#import wx
#from pyside import QtGui
#from AppKit import NSScreen
'''app = wx.App(False)
width, height = wx.GetDisplaySize()

app = QtGui.QApplication([])
screen_resolution = app.desktop().screenGeometry()
width, height = screen_resolution.width(), screen_resolution.height()'''

#width = NSScreen.mainScreen().frame().size.width
#height = NSScreen.mainScreen().frame().size.height

curr_time = datetime.now()
formatted_time = curr_time.strftime('%H:%M:%S')
filepath = 'points' + formatted_time + '.txt'

gaze = EyeTracking()
webcam = cv2.VideoCapture(0)

#x_cord = []
#y_cord = []
#x_cord.append(0)

######
#resolution = Screen.PrimaryScreen.Bounds
'''app = wx.App(False)
width, height = wx.GetDisplaySize()

print(width)
print(height)'''
'''
#image dimensions(same as webcam frame here)
width = 1280
height = 720'''

#iris location
#width = 42
#height = 69

while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    '''
    text = ""

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

#Width = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
#Height = vcap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    #Width = 1280
    #Height = 720

    #my code
#filename = data.txt
    if gaze.pupil_left_coords() is not None:
        x_left, y_left = gaze.pupil_left_coords()
        x_right, y_right = gaze.pupil_right_coords()
        x_mid = (x_left + x_right)/2
        y_mid = (y_left + y_right)/2
        #x_cord.append(x_mid)
        #y_cord.append(y_mid)
        
        #x_mid = x_mid - 718
        #y_mid = y_mid - 318
        
        ##########
        #realX = ((x_mid-620) *Width)/width
        #realY = ((y_mid-310) *Height)/height
            
        with open(filepath, 'a') as fh:
    #for x, y in left_pupil:
    #if x_mid is not None:
    #fh.write('{} {} {} {}\n'.format(x_mid, y_mid, realX, realY))
            fh.write('{} {}\n'.format(x_mid, y_mid))
#print ("lenx" + str(len(x_cord))+ '\n')
#print ("leny" + str(len(y_cord)) + '\n')

    cv2.putText(frame, "Left pupil:  " + str(left_pupil), (90, 130), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)
    cv2.putText(frame, "Right pupil: " + str(right_pupil), (90, 165), cv2.FONT_HERSHEY_DUPLEX, 0.9, (147, 58, 31), 1)

    cv2.imshow("Demo", frame)

    if cv2.waitKey(1) == 27:
        break



'''
print ("yes")
with open('data.txt', 'w') as fh:
    for x, y in zip(x_cord,y_cord):
        #if x_mid is not None:
        fh.write('{} {}\n'.format(x,y))'''
