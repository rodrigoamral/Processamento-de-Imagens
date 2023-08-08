#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# https://colab.research.google.com/drive/1eqUZxgAjtJ3BEJp-5eu1JvCbnQSU5B4G#scrollTo=AuXA7RfbXOut


import cv2
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter


def removeBlack(estimator_labels, estimator_cluster):
    
  # Check for black
  hasBlack = False
  
  # Get the total number of occurance for each color
  occurance_counter = Counter(estimator_labels)

  
  # Quick lambda function to compare to lists
  compare = lambda x, y: Counter(x) == Counter(y)
   
  # Loop through the most common occuring color
  for x in occurance_counter.most_common(len(estimator_cluster)):
    
    # Quick List comprehension to convert each of RBG Numbers to int
    color = [int(i) for i in estimator_cluster[x[0]].tolist() ]
    
  
    
    # Check if the color is [0,0,0] that if it is black 
    if compare(color , [0,0,0]) == True:
      # delete the occurance
      del occurance_counter[x[0]]
      # remove the cluster 
      hasBlack = True
      estimator_cluster = np.delete(estimator_cluster,x[0],0)
      break
      
   
  return (occurance_counter,estimator_cluster,hasBlack)


def getColorInformation(estimator_labels, estimator_cluster,hasThresholding=False):
  
  # Variable to keep count of the occurance of each color predicted
  occurance_counter = None
  
  # Output list variable to return
  colorInformation = []
  
  
  #Check for Black
  hasBlack =False
  
  # If a mask has be applied, remove th black
  if hasThresholding == True:
    
    (occurance,cluster,black) = removeBlack(estimator_labels,estimator_cluster)
    occurance_counter =  occurance
    estimator_cluster = cluster
    hasBlack = black
    
  else:
    occurance_counter = Counter(estimator_labels)
 
  # Get the total sum of all the predicted occurances
  totalOccurance = sum(occurance_counter.values()) 
  
 
  # Loop through all the predicted colors
  for x in occurance_counter.most_common(len(estimator_cluster)):
    
    index = (int(x[0]))
    
    # Quick fix for index out of bound when there is no threshold
    index =  (index-1) if ((hasThresholding & hasBlack)& (int(index) !=0)) else index
    
    # Get the color number into a list
    color = estimator_cluster[index].tolist()
    
    # Get the percentage of each color
    color_percentage= (x[1]/totalOccurance)
    
    #make the dictionay of the information
    colorInfo = {"cluster_index":index , "color": color , "color_percentage" : color_percentage }
    
    # Add the dictionary to the list
    colorInformation.append(colorInfo)
    
      
  return colorInformation 


def getColor(image, center, radius, save = '' ):

    #cv2.circle(image, center[0], center[1], radius, (255, 0, 0), 10)
    
    mask = np.zeros(image.shape[:2],dtype='uint8')
    
    cv2.circle(mask, center, radius, 255, -1)
    c_img = cv2.bitwise_and(image, image, mask=mask)
    c_img_hsv = cv2.cvtColor(c_img,cv2.COLOR_BGR2HSV)
    colored_img = c_img_hsv.reshape((c_img_hsv.shape[0]*c_img_hsv.shape[1]) , 3)
    estimator = KMeans(n_clusters=2, random_state=0)
    estimator.fit(colored_img)
    colorInformation = getColorInformation(estimator.labels_,estimator.cluster_centers_,True)
        
    corH = int(colorInformation[0]['color'][0])
    corS = int(colorInformation[0]['color'][1])
    corV = int(colorInformation[0]['color'][2])    
    corHSV = [corH, corS, corV]
    
    if save != '' :
        mask_inv = cv2.bitwise_not(mask)
        img_fundo = np.zeros((image.shape[0],image.shape[1],3),np.uint8)
        fundo = cv2.add(img_fundo, (corH,corS,corV, 1),mask=mask_inv)
        #fundo = cv2.bitwise_and(fundo, fundo, mask=mask_inv)
        final = cv2.add(fundo,c_img_hsv)
        img_final = cv2.cvtColor(final,cv2.COLOR_HSV2BGR)
        cv2.imwrite(save, img_final)
    
    
    return corHSV


def getColor2(image, center, radius, save = '' ):

    #cv2.circle(image, center[0], center[1], radius, (255, 0, 0), 10)
    
    mask = np.zeros(image.shape[:2],dtype='uint8')
    
    cv2.circle(mask, center, radius, 255, -1)
    c_img = cv2.bitwise_and(image, image, mask=mask)
    colored_img = c_img.reshape((c_img.shape[0]*c_img.shape[1]) , 3)
    estimator = KMeans(n_clusters=2, random_state=0)
    estimator.fit(colored_img)
    colorInformation = getColorInformation(estimator.labels_,estimator.cluster_centers_,True)
        
    corB = int(colorInformation[0]['color'][0])
    corG = int(colorInformation[0]['color'][1])
    corR = int(colorInformation[0]['color'][2])
    cor = np.zeros((1,1,3),np.uint8)
    cor[0][0] = np.array((corB, corG, corR))
    corHSV = cv2.cvtColor(cor, cv2.COLOR_BGR2HSV)
    
    if save != '' :
        mask_inv = cv2.bitwise_not(mask)
        img_fundo = np.zeros((image.shape[0],image.shape[1],3),np.uint8)
        fundo = cv2.add(img_fundo, (corB,corG,corR, 1),mask=mask_inv)
        img_final = cv2.add(fundo,c_img)
        cv2.imwrite(save, img_final)
    
    
    return corHSV[0][0]
