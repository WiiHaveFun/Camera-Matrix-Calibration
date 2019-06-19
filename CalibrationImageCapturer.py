# saves a frame to the pi every five seconds to use for calibration

# import the necessary packages
import numpy as np
import cv2
import glob
from pathlib import Path
import time

cap = cv2.VideoCapture("/dev/video0")
# 720p calibration images
cap.set(3,1280)
cap.set(4,720)

i = 1

global startTime
startTime = time.time()

while(True):

    ret, frame = cap.read()

    if ret:
        cv2.imshow("camera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    if time.time() - startTime > 5:
        if i <= 20:
            cv2.imwrite('calibration' + str(i) + '.jpg', frame)
            print("saved ", i)
            
            startTime = time.time()

            i += 1
        else:
            break

# Detect corners
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d points in real world space
imgpoints = [] # 2d points in image plane.

distortion_correction_file = Path("./distortion_correction_pickle.p")
if distortion_correction_file.is_file():
    print('Distortion correction file already created')
else:
    # Make a list of calibration images
    images = glob.glob('./calibration*.jpg')
    # Step through the list and search for chessboard corners
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (9,6), corners, ret)
            cv2.imshow('img',img)
            cv2.waitKey(500)

    cv2.destroyAllWindows()


# Generate pickle file
import pickle

if distortion_correction_file.is_file():
    with open('./distortion_correction_pickle.p', mode='rb') as f:
        calibration_file = pickle.load(f)
        mtx, dist = calibration_file['mtx'], calibration_file['dist']
else:
    # Do camera calibration given object points and image points
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, (720,1280),None,None)
    # Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
    dist_pickle = {}
    dist_pickle["mtx"] = mtx
    dist_pickle["dist"] = dist
    pickle.dump( dist_pickle, open( './distortion_correction_pickle.p', 'wb' ) )

# apply distortion correction to the camera calibration image
filename = './calibration1.jpg'
img = cv2.imread(filename)
dst = cv2.undistort(img, mtx, dist, None, mtx)
# Process the file name for saving to a different directory
undistorted_filename = 'undistort_test.jpg'
cv2.imwrite(undistorted_filename, dst)

print("mtx\n\n", mtx)
print("\n\ndist\n\n", dist)
