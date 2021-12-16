import numpy as np

a = np.array(((2, 0, 0), (0, 1, 0), (0, 0, 1)))
b = np.array((1, 2, 3))

x = np.linalg.solve(a, b)

print(x)
