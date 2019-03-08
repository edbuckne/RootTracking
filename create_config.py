import numpy as np
import scipy.io

specimen = eval(input("What is the number of specimen?"))  # input reads integers
data_matrix = np.empty([specimen, 9])
i = 0
while i < specimen:
    # taking in parameters of specimens
    x_start = eval(input("What is the initial x coordinate for specimen"+str(i+1)))
    y_start = eval(input("What is the initial y coordinate?"+str(i+1)))
    z1_start = eval(input("What is the z1 coordinate?"+str(i+1)))
    z2_start = eval(input("What is the z2 coordinate?"+str(i+1)))
    delta_x = eval(input("What is delta x"+str(i+1)))
    delta_y = eval(input("What is delta y"+str(i+1)))
    n_time_stamps = eval(input("What is the number of time stamps?"+str(i+1)))
    capture_frequency = eval(input("What is the capture frequency of the specimen?"+str(i+1)))
    # storing the values in the config data matrix
    data_matrix[i][0] = i
    data_matrix[i][1] = x_start
    data_matrix[i][2] = y_start
    data_matrix[i][3] = z1_start
    data_matrix[i][4] = z2_start
    data_matrix[i][5] = delta_x
    data_matrix[i][6] = delta_y
    data_matrix[i][7] = n_time_stamps
    data_matrix[i][8] = capture_frequency
    i = i+1
# put the data of the array into list form
matDict = {"array": data_matrix}
scipy.io.savemat("config.mat", matDict)
print(data_matrix)
