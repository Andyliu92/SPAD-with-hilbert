import numpy as np
import os
import module.circuit as circuit
import module.file as file
import module.statistic as statistic

##################### Description #############################
'''
main changes:

1. use heuristic method to compute largestCurrent and smallestStep
    - the computation for I step of each pair is to figure out the magnitude distribution
2. innate pdf cdf, processed data output.
'''

################## user-define parameters #######################
order = 4

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

# Statistic parameter
seq_N = 100                # total number of separation

x_axis_function = "np.log10(x)"

X_AXIS_AUTO_SCALING = True
x_axis_min = 0              # disabled if X_AXIS_AUTO_SCALING = True
x_axis_max = 100            # disabled if X_AXIS_AUTO_SCALING = True

'''
Y_AXIS_AUTO_SCALING = True
y_axis_min = 0              # disabled if Y_AXIS_AUTO_SCALING = True
y_axis_max = 100            # disabled if Y_AXIS_AUTO_SCALING = True
'''

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

for i in all:
    if i[0] == n/2 and i[1] == n/2+1:
        element1 = i
    if i[0] == n/2-1 and i[1] == n/2+2:
        element2 = i


# data preparation for next step statistic operation
smallestStep = max(abs(element1[2]-element2[2]),
                   abs(element1[3]-element2[3]))
ratio = largestCurrent/smallestStep
bit = np.log2(ratio)


div_count = np.zeros((seq_N), dtype=np.int64)

for i in range(0, len(all), 1):
    for j in range(i+1, len(all), 1):
        d1 = abs(all[j][2] - all[i][2])
        d2 = abs(all[j][3] - all[i][3])
        if X_AXIS_AUTO_SCALING == True:
            statistic.fxcount(smallestStep, largestCurrent, max(
                d1, d2), x_axis_function, div_count)
        else:
            statistic.fxcount(x_axis_min, x_axis_max, max(
                d1, d2), x_axis_function, div_count)
        if all[j][2] == all[i][2] and all[j][3] == all[i][3]:
            same.update({all[i]: all[j]})
        if d1 < close_threshold and d2 < close_threshold:
            close.update({all[i]: all[j]})
    print("\rfinished round %d / %d, %.3f %% complete" %
          (i, len(all), i/len(all)*100), end='')

pdfRes = statistic.pdf(div_count)
cumulate_sum, cdfRes = statistic.cdf(div_count)

if X_AXIS_AUTO_SCALING == True:
    div_center = statistic.fDivCenter(
        smallestStep, largestCurrent, x_axis_function, seq_N)
else:
    div_center = statistic.fDivCenter(
        x_axis_min, x_axis_max, x_axis_function, seq_N)

file.writePdfCdf(div_center, div_count, cumulate_sum,
                 pdfRes, cdfRes, csv_path+"_pdfcdf.csv")

file.result_output(all, same, close, smallestStep,
                   largestCurrent, ratio, bit, outfile)

outfile.close()

file.writeCSV(all, csv_path+".csv")
