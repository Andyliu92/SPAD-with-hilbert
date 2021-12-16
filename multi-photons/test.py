import numpy as np
from numpy import linalg

a = np.array(((2, 0, 0), (0, 2, 0), (0, 0, 1)))
b = np.array((1, 2, 3))

print(a)
u, s, v = linalg.svd(a)
print(u)
print(s)
print(v)


sol = u.T@linalg.inv(np.diag(s))@v@b.T

print(np.diag(s))
print(sol)
