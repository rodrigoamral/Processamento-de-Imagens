#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np


def InRangeMask(hsv, Hmin, Hmax):

    rangeMask = np.ones(hsv.shape[:2],dtype='uint8')
    
    if Hmin[0]<=Hmax[0]:
        cv2.inRange(hsv, Hmin, Hmax, rangeMask)
    else:
        rangeMaskA = np.zeros(hsv.shape[:2],dtype='uint8')
        rangeMaskB = np.zeros(hsv.shape[:2],dtype='uint8')
        
        min1 = np.array((0, Hmin[1], Hmin[2]))
        max1 = np.array((Hmin[0], Hmax[1], Hmax[2]))
        min2 = np.array((Hmax[0], Hmin[1], Hmin[2]))
        max2 = np.array((179, Hmax[1], Hmax[2]))

        cv2.inRange(hsv, min1, max1, rangeMaskA)
        cv2.inRange(hsv, min2, max2, rangeMaskB)
        rangeMask = rangeMaskA ^ rangeMaskB;
    
    return rangeMask


def byColor(image, color, delta = [10, 50, 50], blur = 21, morf = 25, save = '' ):
    
    median = cv2.medianBlur(image, blur)
    
    image_hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    
    lower_bound = np.array( [ (color[0]+180-delta[0])%180,
                              max(0,color[1]-delta[1]), 
                              max(0,color[2]-delta[2])] )
    upper_bound = np.array( [ (color[0]+delta[0])%180, 255,255 ])
                              #min(255,color[1]+delta[1]), 
                              #min(255,color[2]+delta[2])] )
                           
    mask = InRangeMask(image_hsv, lower_bound, upper_bound)
    
    
    #define kernel size
    kernel = np.ones((morf,morf),np.uint8)
    
    # Remove unnecessary noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # Segment only the detected region
    segmented_img = cv2.bitwise_and(median, median, mask=mask)
    #final = cv2.hconcat((img, median, segmented_img))

    if save != '' :
        cv2.imwrite(save, mask)

