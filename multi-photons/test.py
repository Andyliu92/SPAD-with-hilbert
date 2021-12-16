import numpy as np


################## user-define parameters #######################
order = 4

close_threshold = 1e-3

output_path = "D:/Work/04_Research_Project/21.04.28_Hilbert's_curve/python project/multi-photons/result/order1.txt"

# wire parameters
line_width = 0.2
spad_dist = 10
Rsq = 0.1  # 100kOhm

# SPAD parameters
Rt = 20e3                     # SPAD conduct resistance, 100kOhm
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
        Dn = rMatrix.copy()
        Dn[0, Dn.shape[1]-1] = u
        for i in range(1, Dn.shape[0], 1):
            Dn[i, Dn.shape[1]-1] = 0
        # print("rMatrix:")
        # print2d(rMatrix)
        # print("Dn:")
        # print2d(Dn)
        a = np.linalg.det(Dn)
        b = np.linalg.det(rMatrix)
        return np.linalg.det(Dn) / np.linalg.det(rMatrix)

    else:
        return u / rMatrix


def r_eq(rMatrix: np.ndarray, u):
    if isinstance(rMatrix, np.ndarray):
        D1 = rMatrix.copy()
        D1[0, 0] = u
        for i in range(1, D1.shape[0], 1):
            D1[i, 0] = 0
        # print("rMatrix:")
        # print2d(rMatrix)
        # print("D1:")
        # print2d(D1)
        a = np.linalg.det(D1)
        b = np.linalg.det(rMatrix)
        return u / (np.linalg.det(D1) / np.linalg.det(rMatrix))

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
    return max(length, width) / min(length, width) * Rsq


###################### Innate parameters #######################

# wire resistance between 2 sensors
r = r_wire(spad_dist, line_width, Rsq)

r_end = r_wire(sensor_dist, line_width, Rsq)

################################################################

n = 4**order

I1, I2 = iArray(n, Rt, r, r_end, u)

print(I1)
print(I2)
