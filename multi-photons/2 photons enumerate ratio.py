import numpy as np

# parameter
order = 3

close_threshold = 0.01


##########################################################

def print2d(array):
    for i in range(0, array.shape[0]+1, 1):
        for j in range(0, array.shape[1]+1, 1):
            print(array[i][j], end="")
        print("")


n = 4**order

all = []
same = {}
close = {}

# All output for single photon
for i in range(1, n+1, 1):
    I1 = 2*n/(2*i-1)
    I2 = 2*n/(2*n-2*i+1)
    all.append((i, 0, I1, I2))

    # All output for two photons
for i in range(1, n+1, 1):
    for j in range(i+1, n+1, 1):
        I1 = 2*n * (1/(2*i-1)+1/(2*j-1))
        I2 = 2*n * (1/(2*n-2*i+1) + 1/(2*n-2*j+1))
        all.append((i, j, I1, I2))

for i in range(0, len(all), 1):
    for j in range(i+1, len(all), 1):
        if all[j][2] / all[i][2] == all[j][3] / all[i][3]:
            same.update({all[i]: all[j]})
        if abs(all[j][2] / all[i][2] - all[j][3] / all[i][3] < close_threshold):
            close.update({all[i]: all[j]})


print("Same: \n ", same)
print("Close: \n ", close)
