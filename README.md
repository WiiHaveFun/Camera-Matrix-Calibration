# Camera-Matrix-Calibration
A program that allows you to quickly create camera matrix and distortion matrix pickle files.
## Requirements
1. A computer that can run python3 files
2. The necessary modules listed in the file
3. A camera calibration checkerboard
## How To Use
The software will open the camera as a 720p stream. You can change which camera is opened and the settings in lines 13-16
```python
cap = cv2.VideoCapture("/dev/video0")
# 720p calibration images
cap.set(3,1280)
cap.set(4,720)
```
You can change the number of images taken by changing line 34
```python
if i <= 20:
```
By default the program will take 20 images, once every 5 seconds. Once it is done, it will run a camera calibration algorithm, detection program. It will generate a pickle file and print out the camera and distortion matrices. If you already have a set of images you want to use, you can skip taking images by pressing 'q'. If a pickle file is detected under the path "./distortion_correction_pickle.p", it will skip creating the file and make a test undistortion image.

By defualt, the checkerboard you will use is a 9 by 6 board. You will want to print it and place it on a flat surface. It is best to put it on a flat box to make it moveable.

Here's a helpful link:
https://docs.opencv.org/2.4/doc/tutorials/calib3d/camera_calibration/camera_calibration.html

And a link to a checkerboard you can print:
https://docs.opencv.org/2.4/_downloads/pattern.png
