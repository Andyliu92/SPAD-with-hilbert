import numpy as np
from numpy import linalg
import csv
import os
import module.circuit as circuit
import module.file as file


################## user-define parameters #######################
order = 2

close_threshold = 5e-8

log_path = "D:/Work/04_Research_Project/21.04.28_Hilbert's_curve/python project/multi-photons/result/log/" + \
    format(order)+".txt"
csv_path = "D:/Work/04_Research_Project/21.04.28_Hilbert's_curve/python project/multi-photons/result/csv/" + \
    format(order)


# wire parameters
line_width = 0.2
spad_dist = 10
Rsq = 0.1

# SPAD parameters
Rt = 20e3                 # SPAD conduct resistance
u = 3.3                     # SPAD source voltage. commonly used: 1.2 1.8 2.5 3.3

# sensor position
sensor_dist = spad_dist     # Readout sensor's distance to the last SPAD sensor


TESTING = False


###################### Innate parameters #######################

outfile = open(log_path, 'w')

# manipulate for avoiding overflow.
scaling_factor = 1e0

csv_write_step = 1000

if TESTING == True:
    outfile.write("u = %lf\n" % u)
    outfile.write("Rsq = %lf\n" % Rsq)
    outfile.write("Rt = %lf\n" % Rt)


############################# Functions ####################################


############################# Main #########################################


# data preparation
n = 4**order


u *= scaling_factor
Rsq *= scaling_factor
Rt *= scaling_factor

# wire resistance between 2 sensors
r = circuit.r_wire(spad_dist, line_width, Rsq)

r_end = circuit.r_wire(sensor_dist, line_width, Rsq)


all = []
allstep = []
same = {}
close = {}
smallestStep = 1000000

if os.path.exists(csv_path+"_step.csv"):
    os.remove(csv_path+"_step.csv")


# simulation
I_left, I_right = circuit.iArray(n, Rt, r, r_end, u)
print("got I array.")

outfile.write(format(I_left))
outfile.write("\n\n")

largestCurrent = I_left[0] + I_left[1]

# All output for single photon
for i in range(1, n+1, 1):
    I1 = I_left[i-1]
    I2 = I_right[i-1]
    all.append((i, 0, I1, I2))
print("got all output for a single photon")


# All output for two photons
for i in range(1, n+1, 1):
    for j in range(i+1, n+1, 1):
        I1 = I_left[i-1] + I_left[j-1]
        I2 = I_right[i-1] + I_right[j-1]
        all.append((i, j, I1, I2))
print("got all output for 2 photons")

for i in range(0, len(all), 1):
    for j in range(i+1, len(all), 1):
        d1 = abs(all[j][2] - all[i][2])
        d2 = abs(all[j][3] - all[i][3])
        allstep.append(
            (all[i][0], all[i][1], all[j][0], all[j][1], max(d1, d2)))
        if all[j][2] == all[i][2] and all[j][3] == all[i][3]:
            same.update({all[i]: all[j]})
        if d1 < close_threshold and d2 < close_threshold:
            close.update({all[i]: all[j]})
            smallestStep = min(smallestStep, max(d1, d2))
            # logic: distinguish two situation by distinguishing the larger difference.
    if i % csv_write_step == 0:
        file.writeStepCSV(allstep, csv_path+"_step.csv")
        del allstep
        allstep = []
    print("\rfinshed round %d" % i, end='')

file.writeStepCSV(allstep, csv_path+"_step.csv")


print('\n')

# Result output
print(len(all), " Combinations in total.")
outfile.write(format(len(all)))
outfile.write(' Combinations in total.\n\n\n')

print("Same: \n ", same)
outfile.write("Same:\n ")
outfile.write(format(same))
outfile.write('\n')

outfile.write("\n\n############################################\n\n")

print("Close: \n ", close)
outfile.write("Close:\n ")
outfile.write(format(close))
outfile.write('\n')

outfile.write("\n\n############################################\n\n")

print("For all close pairs:")
for i in close:
    print(i, ':\n', close[i], '\ncurrent pair max step:', max(
        abs(i[2]-close[i][2]), abs(i[3]-close[i][3])))
    outfile.write(format(i)+':\n' + format(close[i]) + '\ncurrent pair max step:' + format(max(
        abs(i[2]-close[i][2]), abs(i[3]-close[i][3]))) + '\n\n')

outfile.write("\n\n############################################\n\n")

print("Smallest Step = ", smallestStep)
outfile.write("Smallest Step = " + format(smallestStep)+"\n")

print("Largest Current = ", largestCurrent)
outfile.write("Largest Current = " + format(largestCurrent)+"\n")

ratio = largestCurrent/smallestStep

bit = np.log2(ratio)

print("ratio = ", ratio)
outfile.write("ratio = "+format(ratio)+"\n")
print("bit = ", bit)
outfile.write("bit = "+format(bit)+"\n")

outfile.close()

file.writeCSV(all, csv_path+".csv")
