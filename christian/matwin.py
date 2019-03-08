# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 20:35:48 2018

@author: Christian Ward Richardson cricha50@eagles.nccu.edu

Matfile Creation program: When initialized opens a window for entering the values necessary to create the mat files used by zenAI
Saves matfile in the same directory the script is located in
Should be converted to .exe, or run via console: python matwin.py 
Note: a matfile created for an experiment is unique to the imaging session/specimen and zenAI must be run using the matfile at each timestamp to avoid errors 
Requires: PyQt5, scipy.io
"""

import sys
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QApplication, QWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import Qt
from scipy.io import savemat

class matwin(QWidget):
    
    def __init__(self):
        super(matwin, self).__init__()
        self.initUI()
        
    def initUI(self):
        global matname, lzF, lzL, lxCur, lyCur, lgvX, lgvY, ldZ, ldXY
        self.setGeometry(50,50,400,520)
        self.setWindowTitle("Enter Specimen info for .mat file")

        intval = QIntValidator()
        
        matname = QLineEdit(self)
   
        lmatname = QLabel(self)
        lmatname.setText("Enter mat file name without .mat")
   
        val = QDoubleValidator()
        val.setDecimals(3)
        
        lzF = QLineEdit(self)
        lzF.setValidator(val)
        
        zFlabel = QLabel(self)
        zFlabel.setText("Z First")
        
        lzL = QLineEdit(self)
        lzL.setValidator(val)
        
        zLlabel = QLabel(self)
        zLlabel.setText("Z Last")
        
        lxCur = QLineEdit(self)
        lxCur.setValidator(val)
        
        xCurlabel = QLabel(self)
        xCurlabel.setText("X Position")
        
        lyCur = QLineEdit(self)
        lyCur.setValidator(val)
        
        yCurlabel = QLabel(self)
        yCurlabel.setText("Y Position")
        
        lgvX = QLineEdit(self)
        lgvX.setValidator(val)
        
        gvXlabel = QLabel(self)
        gvXlabel.setText("Growth Vector (x)")
        
        lgvY = QLineEdit(self)
        lgvY.setValidator(val)
        
        gvYlabel = QLabel(self)
        gvYlabel.setText("Growth Vector (y)")
        
        ldZ = QLineEdit(self)
        ldZ.setValidator(val)
        
        dZlabel = QLabel(self)
        dZlabel.setText("Z axis pixels to microns")
        
        ldXY = QLineEdit(self)
        ldXY.setValidator(val)
        
        dXYlabel = QLabel(self)
        dXYlabel.setText("X/Y axis pixels to microns")
        
        OK = QPushButton("OK", self)
        OK.clicked.connect(self.automat)
        
        vbox = QVBoxLayout()
        vbox.addWidget(lmatname)
        vbox.addWidget(matname)
        vbox.addWidget(zFlabel)
        vbox.addWidget(lzF)
        vbox.addWidget(zLlabel)
        vbox.addWidget(lzL)
        vbox.addWidget(xCurlabel)
        vbox.addWidget(lxCur)
        vbox.addWidget(yCurlabel)
        vbox.addWidget(lyCur)
        vbox.addWidget(gvXlabel)
        vbox.addWidget(lgvX)
        vbox.addWidget(gvYlabel)
        vbox.addWidget(lgvY)
        vbox.addWidget(dZlabel)
        vbox.addWidget(ldZ)
        vbox.addWidget(dXYlabel)
        vbox.addWidget(ldXY)
        vbox.addWidget(OK)
        self.setLayout(vbox)
        
        self.show()
        
    def automat(self):  #creates mat file using gvar's here
        def popup(self, field):
            popup = QMessageBox.question(self, "Py", "Please enter a value for "+field, QMessageBox.Yes, QMessageBox.Yes)
            if popup == QMessageBox.Yes:
                pass
            
        gmatname = matname.text()
        if gmatname == "":
            popup(self,'mat')
        
        try:
            gzF = float(lzF.text())
        except:
            popup(self,'zF')
            
        try:    
            gzL = float(lzL.text())
        except:
            popup(self,'zL')
            
        try:    
            gxCur = float(lxCur.text())
        except:
            popup(self,'xCur')
            
        try:    
            gyCur = float(lyCur.text())
        except:
            popup(self,'yCur')
            
        try:    
            ggvX = float(lgvX.text())
        except:
            popup(self,'gvX')
            
        try:    
            ggvY = float(lgvY.text())
        except:
            popup(self,'gvY')
            
        try:    
            gdZ = float(ldZ.text())
        except:
            popup(self,'dZ')
            
        try:    
            gdXY = float(ldXY.text())
        except:
            popup(self,'dXY')
    
        
        zlist ={
                "zF" : gzF,
                "zL" : gzL,
                "xCur" : gxCur,
                "yCur" : gyCur,
                "gvX" : ggvX,
                "gvY" : ggvY,
                "dZ" : gdZ,
                "dXY" : gdXY,
                }
        savemat(gmatname+'.mat',zlist)
        self.close()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.automat()
    
            
def main():
    app = QApplication(sys.argv)  
    win = matwin()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()


                     