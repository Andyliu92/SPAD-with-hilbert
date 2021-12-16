import numpy as np
from numpy import linalg


################## user-define parameters #######################
order = 1

close_threshold = 1000

output_path = "D:/Work/04_Research_Project/21.04.28_Hilbert's_curve/python project/multi-photons/result/order1_svd.txt"

# wire parameters
line_width = 0.2
spad_dist = 10
Rsq = 0.1

# SPAD parameters
Rt = 20e3                 # SPAD conduct resistance
u = 3.3                     # SPAD source voltage. commonly used: 1.2 1.8 2.5 3.3

# sensor position
sensor_dist = spad_dist     # Readout sensor's distance to the last SPAD sensor

############################# Functions ####################################


def print2d(array):
    if isinstance(array, np.ndarray):
        for i in range(0, array.shape[0], 1):
            for j in range(0, array.shape[1], 1):
                print(array[i][j], "  ", end="")
            print("")
    else:
        print(array)


def rMatrixGen(n, Rt, r, r_end) -> np.ndarray:
    if n <= 0:
        print("Error! n <= 0")
        exit()
    elif n == 1:
        result = r_end
    else:
        result = np.zeros((n, n), dtype=np.float64)
        result[0, 0] = Rt + r
        result[n-1, n-1] = Rt + r_end
        result[0, 1] = result[n-1, n-2] = -Rt
        for i in range(1, n-1, 1):
            result[i, i-1] = result[i, i+1] = -Rt
            result[i, i] = 2 * Rt + r

    return result


def iSensor(rMatrix: np.ndarray, u):
    if isinstance(rMatrix, np.ndarray):
        b = np.zeros((rMatrix.shape[0]), dtype=np.float64)
        b[0] = u
        U, s, v = linalg.svd(rMatrix)
        sol = sol = U.T@linalg.inv(np.diag(s))@v@b.T
        r = sol[rMatrix.shape[0]-1]
        return r

    else:
        return u / rMatrix


def r_eq(rMatrix: np.ndarray, u):
    if isinstance(rMatrix, np.ndarray):
        b = np.zeros((rMatrix.shape[0]), dtype=np.float64)
        b[0] = u
        U, s, v = linalg.svd(rMatrix)
        sol = sol = U.T@linalg.inv(np.diag(s))@v@b.T
        r = u / sol[0]
        return r
    else:
        return rMatrix


def iArray(n, Rt, r, r_end, u) -> tuple[np.ndarray, np.ndarray]:
    I_left = np.zeros((n), dtype=np.float64)
    I_right = np.zeros((n), dtype=np.float64)
    for i in range(0, n, 1):
        rMatrixLeft = rMatrixGen(i+1, Rt, r, r_end)
        rMatrixRight = rMatrixGen(n-(i+1)+1, Rt, r, r_end)
        r_netLeft = r_eq(rMatrixLeft, 1)
        r_netRight = r_eq(rMatrixRight, 1)
        r_net = (r_netLeft * r_netRight)/(r_netLeft+r_netRight)
        u_net = u * (r_net / (Rt + r_net))
        I_left[i] = iSensor(rMatrixLeft, u_net)
        I_right[i] = iSensor(rMatrixRight, u_net)
    return I_left, I_right


def r_wire(length, width, Rsq):
    return length / width * Rsq


###################### Innate parameters #######################

# wire resistance between 2 sensors
r = r_wire(spad_dist, line_width, Rsq)

r_end = r_wire(sensor_dist, line_width, Rsq)

# manipulate for avoiding overflow.
scaling_factor = 1
u *= scaling_factor
Rsq *= scaling_factor
Rt *= scaling_factor

################################################################

n = 4**order

all = []
same = {}
close = {}
smallestStep = 1000000

outfile = open(output_path, 'w')

I_left, I_right = iArray(n, Rt, r, r_end, u)
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
        if all[j][2] == all[i][2] and all[j][3] == all[i][3]:
            same.update({all[i]: all[j]})
        if d1 < close_threshold and d2 < close_threshold:
            close.update({all[i]: all[j]})
            smallestStep = min(smallestStep, max(d1, d2))
            # logic: distinguish two situation by distinguishing the larger difference.

    print("finshed round %d" % i)


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

print("Smallest Step:\n ", smallestStep)
outfile.write("Smallest Step:\n " + format(smallestStep))

outfile.write("\n\n############################################\n\n")

print("Largest Current:\n ", largestCurrent)
outfile.write("Largest Current:\n "+format(largestCurrent))
