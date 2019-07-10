# EyeTrace

This is a computer vision python(2 and 3) application that provides a webcam-based eye tracking system. It gives you the exact position of the pupils and the gaze direction in real-time. Using calibration we can use these pupil coordinates to give us the eye-trace of a user's gaze while looking at something on a screen. 

## **Installation:** 

### **Clone this project :**

```
git clone https://github.com/aditi15ashley/EyeTrace.git
```

### **Install these dependencies :**

```
pip install -r requirements.txt 
```
> The Dlib library has four primary prerequisites: Boost, Boost.Python, CMake and X11/XQuartx. If you don't have them, you can read this article to know how to easily install them : https://www.pyimagesearch.com/2017/03/27/how-to-install-dlib/

> OpenCV 4 is not supported yet, make sure to install version 3.4

### **Run the demo :**

```
python gaze.py 
```
## How it works

This is a deep-learning based application which uses the dlib library containing the implementation of deep metric learning which is used to construct our face embeddings used for the actual recognition process. 

This library is used as a face detector to detect faces and get facial landmarks of a given face. Using these landmarks we detects the iris of an eye and estimate the position of the pupil. 

Now to use these pupil coordinates to get our gaze on the screen, we use the 9-point calibration system. 

To do this, we make a calibration page on the server with 9 buttons. Whenever a user clicks on these buttons we store the screen coordinates of where the user clicks and at the same time store the coordinates of our pupils in the webcam frame.

We try to obtain a function mapping the screen coordinates to pupil coordinates in webcam frame in `9point.py`. This function is used to obtain the screen coordinates for our real-time pupil detection while looking at the screen and hence is used to produce our eye-trace in `9pointoutput.py`. 

Calibration would be more accurate if we click on each of the 9 buttons 4-5 times, and even better if we use a 25-point calibration system. Our results would of course be more accurate if we don't move our head much from the position it was during calibration while actual gaze-detection. 

The back-end of the server has been implemented in Flask in `server.py`.


