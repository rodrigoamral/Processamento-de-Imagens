#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 09:46:15 2023

@author: lizier
"""

import cv2
import os
import markers

def preproc( image ):
    try:
        imgb = cv2.copyMakeBorder(image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255,255,255))
        corners, ids = markers.detectMarkers( imgb )   
        img_preproc = markers.correctDeformation(imgb, corners)
    except:
        img_preproc = ''
    return img_preproc


if __name__ == '__main__':
    
    inputpath = './tests2/'
    outputpath = './tests2-preproc/'
    
    images = []
    files = os.listdir(inputpath)
    for file_name in files:
        if os.path.isfile(inputpath + file_name):
            if file_name.endswith('.png'):
                images.append(file_name)
     
    images.sort()
    
    for f in images:    
        img = cv2.imread(inputpath + f)
        print(f)
        
        
        #imgb = cv2.copyMakeBorder(img, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255,255,255))
        #corners, ids = markers.detectMarkers( imgb )   
        #img_preproc = markers.correctDeformation(imgb, corners)
        img_preproc = preproc( img )
        cv2.imwrite(outputpath + f, img_preproc)
    
    
    