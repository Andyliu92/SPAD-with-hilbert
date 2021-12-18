import numpy as np
import numpy.linalg as linalg


def print2d(array):
    if isinstance(array, np.ndarray):
        for i in range(0, array.shape[0], 1):
            for j in range(0, array.shape[1], 1):
                print(array[i][j], "  ", end="")
            print("")
    else:
        print(array)


def rMatrixGen(n, Rtn, r, r_end) -> np.ndarray:
    if n <= 0:
        print("Error! n <= 0")
        exit()
    elif n == 1:
        result = r_end
    else:
        result = np.zeros((n, n), dtype=np.float64)
        result[0, 0] = Rtn + r
        result[n-1, n-1] = Rtn + r_end
        result[0, 1] = result[n-1, n-2] = -Rtn
        for i in range(1, n-1, 1):
            result[i, i-1] = result[i, i+1] = -Rtn
            result[i, i] = 2 * Rtn + r
    return result


def iSensor(rMatrix: np.ndarray, u):
    if isinstance(rMatrix, np.ndarray):
        b = np.zeros((rMatrix.shape[0]), dtype=np.float64)
        b[0] = u
        sol = linalg.solve(rMatrix, b)
        i = sol[rMatrix.shape[0]-1]
        return i

    else:
        return u / rMatrix


def r_eq(rMatrix: np.ndarray, u):
    if isinstance(rMatrix, np.ndarray):
        b = np.zeros((rMatrix.shape[0]), dtype=np.float64)
        b[0] = u
        sol = linalg.solve(rMatrix, b)
        r = u / sol[0]
        return r
    else:
        return rMatrix


def iArray(n, Rtn, Rtp, r, r_end, u) -> tuple[np.ndarray, np.ndarray]:
    I_left = np.zeros((n), dtype=np.float64)
    I_right = np.zeros((n), dtype=np.float64)
    for i in range(0, n, 1):
        rMatrixLeft = rMatrixGen(i+1, Rtn, r, r_end)
        rMatrixRight = rMatrixGen(n-(i+1)+1, Rtn, r, r_end)
        r_netLeft = r_eq(rMatrixLeft, 1)
        r_netRight = r_eq(rMatrixRight, 1)
        r_net = (r_netLeft * r_netRight)/(r_netLeft+r_netRight)
        u_net = u * (r_net / (Rtp + r_net))
        I_left[i] = iSensor(rMatrixLeft, u_net)
        I_right[i] = iSensor(rMatrixRight, u_net)
    return I_left, I_right


def r_wire(length, width, Rsq):
    return length / width * Rsq
