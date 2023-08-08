#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import os
import polish
import segmentation
import markers



inputpath = './tests/'
outputpath = './tests-detected/'
outputpathcolor = './tests-colors/'
outputpathcolor2 = './tests-colors2/'

images = []
files = os.listdir(inputpath)
for file_name in files:
    if os.path.isfile(inputpath + file_name):
        if file_name.endswith('.png'):
            images.append(file_name)
 
images.sort()

for f in images:    
    filename = inputpath + f
    img = cv2.imread(filename)
    print(filename)
    center, radius = markers.detect(img)
    #color = polish.getColor(img,center,radius, save=outputpathcolor + f)
    color2 = polish.getColor2(img,center,radius, save=outputpathcolor2 + f)
    #print(color)
    print(color2)
    segmentation.byColor(img, color2, save=outputpath + f)
    
    