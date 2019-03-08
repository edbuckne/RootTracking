#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 10:47:23 2018

@authors: Christian Ward Richardson, cricha50@eagles.nccu.edu
classifyImage and findTip are courtesy of Eli Buckner, NCSU ECE Dept.
Note: The mat file used to run this script must be in the same directory as this script
Note2: The window for path name entry will freeze during program execution, this is normal do not attempt to close the window 
Libraries required: numpy,scipy.io,skimage.io,PyQt5
Files required(all must be in same dir as this script): classifyImage.py, findTip.py, classDir folder containing proper classifier, av.mat, matfile for specimen 
"""

import sys

import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QMessageBox
from findTip import findTip
from scipy.io import loadmat
from scipy.io import savemat
from skimage import io

from christian.classifyImage import classifyImage


class winzen(QWidget): #On zenAI initialization, this window opens and user enters full path to fluorescent/brightfield images, in addition to the name of the .mat file created for the experiment
    
    def __init__(self):
        super(winzen, self).__init__()
        self.initUI()
        
    def go(self): #go method reads paths from line edit fields and uses the paths to run zenAIFinal
        def popup(self): #error message box pop up in the event that zenAIFinal didnt run
            popup = QMessageBox.question(self, "Error", "Attempt to run zenAI failed, check file paths", QMessageBox.Yes, QMessageBox.Yes)
            if popup == QMessageBox.Yes: #once user clicks yes, just goes back to main window
                pass
            
        iflp = flu.text()
        ibfp = bf.text()
        mat = lmat.text()

        try:     #error pops up ifzenAIFinal doesn't run
            zenAIFinal(iflp, ibfp, mat)
            self.close()
            
        except:
            popup(self)
               
    def initUI(self): #creates the window
        global bf, flu, lmat #must define global variables due to errors with passing them as args.
        self.setGeometry(800,450,600,300) 
        self.setWindowTitle("ZenAI: Enter czifile paths")
        
        flabel = QLabel("Enter Fluorescent img path (ends with C=0) with .tif")   
        flabel.setFont(QFont("Times", 10))
        flu = QLineEdit(self)
        
        blabel = QLabel("Enter Brightfield img path (ends with C=1) with .tif")  
        blabel.setFont(QFont("Times", 10))
        bf = QLineEdit(self)
        
        mlabel = QLabel("Enter mat file name without .mat")  
        mlabel.setFont(QFont("Times", 10))
        lmat = QLineEdit(self)
        
        ok = QPushButton("OK", self)
        ok.clicked.connect(self.go) #when ok button is clicked, go method attempts to run zenAIFinal
        
        vbox = QVBoxLayout(self) #add gui elements to layout widget 
        vbox.addWidget(flabel)
        vbox.addWidget(flu)
        vbox.addWidget(blabel)
        vbox.addWidget(bf)
        vbox.addWidget(mlabel)
        vbox.addWidget(lmat)
        vbox.addWidget(ok)
        self.setLayout(vbox)
    	
        self.show() #displays window after building it 'behind the scenes'
        
    def keyPressEvent(self, event): #attempts to run zenAI using inputs when enter is clicked
            if event.key() == Qt.Key_Return:
                self.go()
            
def main(): #launches 'winzen' window
    app = QApplication(sys.argv)  
    win = winzen()
    sys.exit(app.exec_()) 
    
class prog(QWidget):
    
    def __init__(self):
        super(prog, self).__init__()
        self.progUI()
        
        
    def progUI(self):
        self.setGeometry(800,450,300,200)
        self.setWindowTitle("zenAI is running")
        ptxt = QLabel(self)
        ptxt.setText("zenAI is running, please wait")
        ptxt.move(50,100)
        self.show()
        
def zenAI(iflp, ibfp, matnomat): #iflp = path to fluorescent image, ibfp path to brightfield img, mat path to mat file without .mat at the end
    #matfile importing/image file loading
    ifl = io.imread(iflp)#read in images via skimage.io
    ibf = io.imread(ibfp)
    
    zenai = loadmat(str(matnomat)+'.mat') #loads mat, then checks if the run counter variable exists, which would mean this isn't the first imaging of the experiment. 
    try: #Mat file variables must be loaded as squeezed arrays for proper indexing after the first tile zenAI is run using the mat file
        zenai['rC']
        zenai = loadmat(str(matnomat)+'.mat', squeeze_me=True)
    except:
        pass #first time the script is run the non-squeezed arrays are used to avoid attempting to append to integers
    
    dXY = zenai['dXY'] #variables from mat file are re-named to ease referencing 
    dZ = zenai['dZ']
    xCur = zenai['xCur']
    yCur = zenai['yCur']
    zF = zenai['zF']
    zL = zenai['zL']
    gvX = zenai['gvX']
    gvY = zenai['gvY']
    
    try:
        xShift = zenai['xShift'] #variables that dont exist on the first zenAI run are avoided using try/except expression
    except:
        pass
    try:
        yShift = zenai['yShift']
    except:
        pass
    try:
        xPoint = zenai['xPoint']
    except:
        pass
    try:
        yPoint = zenai['yPoint']
    except:
        pass
    try:
        rC = zenai['rC']
    except:
        rC = 0 #on the first run, rC is set to zero and incremented by one at the end of the script

     #ZStack Adjustment
    Ifl_mask = classifyImage(iflp) #classifyImage script is used to quantify gene expression via fluorescence in fluorescent img
    iDex = np.asarray([]) #initialize empty array iDex
    for z in range(0,Ifl_mask.shape[0]): #iterates from 0 to the number of zslices within the fluorescent img (if errors arise here check that the first 'size' returned corresponds to the # of zslices)
        if iDex.any(): #if iDex is empty, any() returns false and iDex is returned as an array carrying 1st result from loop (if exp. may be unnecessary, as np.append should work on empty arrays)
            iDex = np.append(iDex, sum(sum(Ifl_mask[z]))) #per z slice, find sum of 1's in classified image representing gene expression along x,y axes. This value is used to determine if a zslice has the threshold amount of gene expression
        else:
            iDex = np.asarray(sum(sum(Ifl_mask[z])))
 
    frame = np.flatnonzero(iDex>1000) #returns indices representing zslices over the threshold of 1000, as a list (frame) 
    
    if sum(frame) > 0: #checks if any zslices contain gene expression, in event that imaging errors occurred the most recent z first/z last values are re-used for microscope automation
        
        first = frame[0] #first z slice is the first index within frame i.e. the first zslice with expression above threshold
        last = frame[-1] #last z slice w/ expression
        
        cF = zF[-1] - (first - 3) * dZ #first zslice is subtracted by buffer zone value (3), converted to microns, then subtracted from most recent zF value (if first<3, positive value is added to zF which expands the imaging range)
        cL = zL[-1] - (last - ifl.shape[0] + 3) * dZ #last zslice is subtracted by the total # of zslices, 3 slices are added as a buffer, this result is converted to microns and subtracted from most recent zL values (note that if the last z slice contains expression, the z range is expanded by 3 zslices)
        zF = np.append(zF, cF); #new zF/zL values are appended to the prev. list, using temporary variables cF/cL
        zL = np.append(zL, cL); 
        del cF, cL #save space by deleting temporary variables

    else:
        print('Image '+str(rC+1)+' has no gene expression, check for errors') #if no gene expression is found, error msg is printed referencing img w/o expression
        zF = np.append(zF,zF[-1])
        zL = np.append(zL, zL[-1]) #values are reused if img cannot be analyzed

    if zF[-1] >= 4850: #these checks ensure that zF/zL values never exceed the limits of the microscope
        zF[-1] = 4850
    if zF[-1] <= -4850:
        zF[-1] = -4850
    if zL[-1] >= 4850:
        zL[-1] = 4850
    if zL[-1] <= -4850:
        zL[-1] = -4850
        
    print('New Near ZStack: ',str(zF[-1]),'µm    New Far ZStack: ',str(zL[-1]),'µm') #new zF/zL values are printed
        
    #Root Tip Tracking 
    P = ibf[round(ibf.shape[0]/2)] #P is the 'middle' zslice within the brightfield stack
    rootChk = np.mean(P) #middle zslice is used to determine whether the brightfield stack can be analyzed (not too dark), by finding the mean pixel intensity value within the middle slice (if it's below the threshold .1, it's assumed that this stack wasn't img'ed properly)
    
    if(rootChk > .1): #checks for whether stack has adequate lighting (see above comment)
        
        if rC > 0: #if this is not the first imaging of the session/specimen:
            
            [tCx, tCy] = findTip("av.mat", ibfp) #findTip returns the x,y coord. in pixels of the root tip, brightfield only
            
            cX = (tCx - xPoint)*dXY #calc. xError (aka xShift) by taking difference between x root loc. and nominal x loc., then converting to microns
            cY = (tCy - yPoint)*dXY #calc. yError (aka yShift)
            xShift = np.append(xShift, cX) #Appends new error/shift 
            yShift = np.append(yShift, cY)
            
            try:
                gX = gvX[-1] + xShift[-1] #calc. new gvX/gvY by adding error to old gvX/gvY Note:gvX/gvY are loaded as 1 value linear arrays before 1st run. After 1st run they're still 1 val. linear arrays, and when the mat file is loaded with squeeze_me=True, gvX and gvY are loaded as integers, not arrays. Thus, this try/except expression handles the instance when gvx/gvy aren't subscriptable
            except:
                gX = gvX + xShift[-1]
            try:
                gY = gvY[-1] + yShift[-1] #calc. gvY
            except:
                gY = gvY + yShift[-1]

            gvX = np.append(gvX, gX) #new gvX/gvY values are appended to the old ones
            gvY = np.append(gvY, gY)
            del gX,gY,cX, cY #temp. variables deleted
            
        else: #on first run of zenAIFinal, root tip location is stored in xPoint and yPoint, which are used as nominal points for error calc.
            [xPoint, yPoint] = findTip("av.mat", ibfp)
            xShift = np.asarray([0]) #x/yShift are initialized and set to zero on first run (since no error should be calculated at this point)
            yShift = np.asarray([0])
            
    else: #if brightfield imgs cannot be analyzed, the previous gvX/gvY values are re-used and new x/yShift is appended as 0. 
        gvX = np.append(gvX, gvX[-1])
        gvY = np.append(gvY, gvY[-1])
        xShift = np.append(xShift, 0)
        yShift = np.append(yShift, 0)
        print('Image ',str(rC),' is too dark to be processed') #this message shows which img was not able to be analyzed   
        
    tX = xCur[-1]-gvX[-1]-xShift[-1] #new x/yCur is calculated, by subtracting from the previous x/yCur the new gvX/Y, and x/yShift. Since x and y shift are originally created as 
    xCur = np.append(xCur, tX)
    del tX #temp. variables are deleted

    tY = yCur[-1]-gvY[-1]-yShift[-1]
    yCur = np.append(yCur, tY)
    del tY
     
    
    if xCur[-1] <= -4850: #checks are done to ensure microscope position limits are not exceeded
        xCur[-1] = -4850
    elif xCur[-1] >= 4850:
        xCur[-1] = 4850
    if yCur[-1] <= -49850:
        yCur[-1] = -49850
    elif yCur[-1] >= 49850:
        yCur[-1] = 49850
     
    
    print('X position:',str(xCur[-1]),'µm    Y position:',str(yCur[-1]),'µm') #new x/yCur are printed

    rC = rC + 1 #run counter is incremented
    
    #the following block of code is used to generate a txt file containing relevant data for AutoIT automation
    f = open(str(matnomat)+'.txt', "w+")
    f.write('#include <AutoItConstants.au3>'
    '\n#include <MsgBoxConstants.au3>'
    '\n'
    '\n$xpos = '+str(round(xCur[-1],2))+
    '\n$ypos = '+str(round(yCur[-1],2))+
    '\n$zfpos = '+str(round(zF[-1],2))+
    '\n$zlpos = '+str(round(zL[-1],2))+
    '\n$scount = $CmdLine[1]'
    '\nMouseClick($MOUSE_CLICK_LEFT, 276, 510, 1, 60) ;click on lowest item in list'
    '\nMouseClick($MOUSE_CLICK_LEFT, 322, 494, 1, 60) ;click on move'
    '\nMouseClick($MOUSE_CLICK_LEFT, 258, 494, 1, 60) ;click on add item'
    '\nMouseClick($MOUSE_CLICK_LEFT, 288, 513 + (17*($scount)), 1, 30) ;click on the new item to edit it'
    '\nMouseClick($MOUSE_CLICK_LEFT, 322, 494, 1, 60) ;click on move'
    '\nMouseClick($MOUSE_CLICK_LEFT, 85, 590, 3, 300) ;double-click on xpos field'
    '\nSend("{BACKSPACE}") ;clear xpos field'
    '\nSend($xpos) ;enter xpos info'
    '\nMouseClick($MOUSE_CLICK_LEFT, 85, 638, 3, 300) ;double-click ypos field'
    '\nSend("{BACKSPACE}") ;clear ypos field'
    '\nSend($ypos) ;enter ypos info'
    '\nMouseClick($MOUSE_CLICK_LEFT, 85, 686, 3, 300) ;double-click zpos field'
    '\nSend("{BACKSPACE}") ;clear zpos field'     
    '\nSend($zfpos) ;enter z first'
    '\nMouseClick($MOUSE_CLICK_LEFT, 184, 507, 1, 60) ;click set first'
    '\nMouseClick($MOUSE_CLICK_LEFT, 102, 686, 3, 300) ;double-click zpos field'
    '\nSend("{BACKSPACE}") ;clear zpos field'
    '\nSend($zlpos) ;enter z last'
    '\nMouseClick($MOUSE_CLICK_LEFT, 184, 547, 1, 60) ;click set last'
    '\nMouseClick($MOUSE_CLICK_LEFT, 272, 512, 1, 60) ;click on lowest item in the list'
    '\nMouseClick($MOUSE_CLICK_LEFT, 292, 494, 1, 60) ;click remove button')
    f.close()
    
    zenlist ={ #values saved to matfile via creating a python dictionary
            "xCur" : xCur,
            "yCur" : yCur,
            "zF" : zF,
            "zL" : zL,
            "gvX" : gvX,
            "gvY" : gvY,
            "xShift" : xShift,
            "yShift" : yShift,
            "xPoint" : xPoint,
            "yPoint" : yPoint,
            "rC" : rC,
            "dZ" : dZ,
            "dXY" : dXY,
            }
    
    savemat(str(matnomat)+'.mat',zenlist) #save new values to matfile
     
if __name__ == '__main__': #when zenAI.py is run, this main loop initializes the opening window
    main()
 
    