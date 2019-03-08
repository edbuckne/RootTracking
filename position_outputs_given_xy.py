import scipy.io as io
import fun.gridPositions as grid

matFile = io.loadmat("config.mat")  # Load the config.mat file that holds the experimental setup metadata
configData = matFile['array']  # 'array' string holds the dictionary key for the configData table
spmNumber = configData.shape[0]  # Get the number of specimen from the configData array size (# of rows = # of specimen)

print(configData)
print("Number of specimen: " + str(spmNumber))

#  This additional information below needs to be handled by create_config.py
h, w = input("Enter the size of the digital image in pixels (H,W): ").split(',')  # Get additional information from the user
h = eval(h)
w = eval(w)
res = eval(input("What is the xy pixel resolution in microns? "))
N = eval(input("How many positions is the specimen to be moved? "))

print("Calculating grid .... \n")

for i in range(spmNumber):
    g = grid.calcGrid(configData[0, 1], configData[0, 2], h, w, res, N)
    print('Grid for specimen ' + str(i+1))
    grid.printGrid(g)
    print('\n')
    io.savemat("specimen" + str(i+1) + "Grid.mat", {'grid':g})
