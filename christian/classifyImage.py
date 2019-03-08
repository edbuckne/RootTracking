# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import scipy.ndimage.filters
import numpy
from scipy.io import loadmat
from skimage import io

def classifyImage(I): #classObj for CO must first be converted to struct in matlab, then saved to new matfile and loaded via x = loadmat(filepath); var = x['classObj']; var['attr']
    co = loadmat('D:/Christian/Documents/IMPS/code/classDir/classobj.mat'); #loads mat file
    CO = co['classObj']; #retrieves classObj struct. and saves in CO
    I = io.imread(I); #load img path
    I = I/2**16; #convert img from int 16 to double
    s = I.shape; #get dimensions of img, must reverse b.c. dim come in backwards
    if numpy.size(s) == 2: #adds third dimension to dim from img if img isnt 3D
        s = [s, (1)];
    #if numpy.size(s)>2
    #   for z = 1:s[0]
    #       I[z,:,:] = scipy.ndimage.filters.gaussian_filter(I[z,:,:],CO.Sigma);
    #else
    #   I = scipy.ndimage.filters.gaussian_filter(I,CO['Sigma'][0,0]);
    #
    
    if CO['Type'][0,0] == 'TH':
        I1 = I;
    elif CO['Type'][0,0] == 'SVM-Y' or CO['Type'][0,0] == 'NN':
        Iy = numpy.zeros(s); #create zeros array of stack
        for y in range(0, s[1]): #iterates across rows of zeros index
            Iy[:,y,:] = numpy.ones((1, s[0], s[2]))*y;
        I1 = I;
        I2 = Iy;
    #import pdb; pdb.set_trace() 
# =============================================================================
#     if CO['Type'][0,0] == 'NN':
#         if numpy.size(s) == 3:
#             Iclass = zeros(s);
#             for z in range(1,s[0]):
#                 I11 = I1[z,:,:];
#                 I22 = I2[z,:,:];
#                 X = numpy.concatenate((I11, I22));
#                 IcTmp = reshape(CO['NN'][0,0].knn.predict(CO['NN'][0,0].))
# =============================================================================
  
    if CO['D'][0,0]==1:
        Iclass = CO['Weights'][0,0][0,0]*I1+CO['Biases'][0,0];
        Iclass = Iclass > 0;
    elif CO['D'][0,0]==2:
        Iclass = -(CO['Weights'][0,0][0,0]*I1+CO['Weights'][0,0][0,1]*I2+CO['Biases'][0,0]);
        Iclass = Iclass>CO['NNth'][0,0];
    
# =============================================================================
#     if CO['Type'][0,0] == 'NN':
#         if numpy.size(s) == 3:
#             Iclass = zeros(s);
#             for z in range(1, s[0]):
#                 I11 = I1[z,:,:];
#                 I22 = I2[z,:,:];
#                 X = [I11, I22];
#                IcTmp
# =============================================================================
    return Iclass
