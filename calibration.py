#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 18:05:54 2023

@author: lizier
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os


inputpath = './tests-calib/'
outputpath = './tests-calib-output/'

images = []
files = os.listdir(inputpath)
for file_name in files:
    if os.path.isfile(inputpath + file_name):
        if file_name.endswith('.png'):
            images.append(file_name)
 
images.sort()

for f in images:    
        
    img = cv2.imread(inputpath + f)
    h,  w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d points in image plane.
    
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
       
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))
        
    
    # undistort
    mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w,h), 5)
    dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite(outputpath + f, dst)