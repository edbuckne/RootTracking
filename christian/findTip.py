#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 12:18:41 2018

@author: crichar9
"""

import numpy as np
import skimage
from skimage import io, color, transform
import cv2
from scipy.io import loadmat
import matplotlib.pyplot as plt

def findTip(avPath, I):
    Ib = io.imread(I); #read stack
    I = Ib/2**16; #convert image to 64bit float
    y = loadmat(avPath);#load avPath .mat file 
    av= y['av'];
    
    for z in range(0,np.size(I, axis=0)): #blur and find gradient of each slice
        tempimg = cv2.GaussianBlur(I[z],(5,5),0); #gaussian blur on slice
        sX = cv2.Scharr(tempimg, cv2.CV_64F,1, 0);#horizontal gradient 
        sY = cv2.Scharr(tempimg, cv2.CV_64F,0, 1); #vertical gradient
        I[z] = cv2.addWeighted(sX, 0.5, sY, 0.5, 0); #add two gradient pictures 
    
    Imax = np.amax(I, axis = 0); #create Max. Proj. image 
    Imax = skimage.transform.resize(Imax, [480,480]); #resize MP image
    Imaxsmooth = Imax; 
        
    Sfilt = av.shape; #find dimensions of av file in avPath
    Sim = Imax.shape; #find dimensions of Imax resized img (480,480)
    #import pdb; pdb.set_trace()    
    L = (Sfilt[0]-1)/2; #subtract 1 from # rows in av, divide by 2 to create pad size
    L = int(L);
    Imaxpad = np.pad(Imaxsmooth, ((L,L),(L,L)), mode='constant',constant_values=0); #pad MP image with 0
    Ifilt = np.zeros(Sim); #create zeros matrix with dimensions of MP image
    
    for row in range(0,Sim[0]): #iterate across rows of MP image
        for col in range(0,Sim[1]): #iterate across columns
            Ismall = Imaxpad[row:(row+Sfilt[0]), col:(col+Sfilt[1])]; #crop a section of padded image
            
            isAV = np.mean(Ismall); #find mean of cropped img for normalization
            isStd = np.std(Ismall); #find std dev. of cropped image for normalization
            Ismall = (Ismall-isAV)/isStd; #takes diff. btwn cropped img values and mean, then divides by std dev.
            
            Ifilt[row,col] = abs(Ismall-av).sum(axis=0).sum(axis=0); #least difference squared of normalized cropped img & trained img
    
    
    Ifilt = Ifilt[L:Ifilt.shape[1]-L, L:Ifilt.shape[1]-L]; #crop out padded zone
    newS = Ifilt.shape; #store dim of image
    p = np.argmin(Ifilt); #returns flattened array index of min. value in Ifilt 
    [row, col] = np.unravel_index([p], newS); #returns row, col. index of p (flattened array index)
    
    x = (col+L)*4; #to adjust for inaccuracy of root tip coord. from padding
    y = (row+L)*4; 
    
    #plot x,y on image and display
# =============================================================================
#     implot = plt.imshow(Ib[int(np.size(I, axis=0)/2)]);
#     plt.scatter([x],[y], c='r', s=40);
#     plt.show()
# =============================================================================

    
    return x, y
            
        
        