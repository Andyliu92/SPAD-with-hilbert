'''
n = int(input("What is the order of the hilbert curve?\n"))

p = float(input("What's the persentage of the point on the curve?\n"))

'''
from math import *
import numpy as np

n = 2
p = 15/16

if(n <= 0 or p < 0 or p > 1):
    print("data error!\n")
    exit()

angle = 0
direction = 1

position = np.array([1, 1])

for i in range(n, 0, -1):
    stepLen = 2 ** (i-1)
    if(p <= 0.25):    # 1st block, flip involved
        angle = pi/2 - angle
        direction *= -1
        p *= 4

    elif(p > 0.25 and p <= 0.5):    # 2nd block
        position = position + stepLen * \
            np.array([cos(angle + direction * pi/2),
                     sin(angle + direction * pi/2)])
        position = np.rint(position)
        p = (p-0.25)*4

    elif(p > 0.5 and p <= 0.75):    # 3rd block
        position = position + sqrt(2) * stepLen * \
            np.array([cos(angle + direction * pi/4),
                     sin(angle + direction * pi/4)])
        position = np.rint(position)
        p = (p-0.5)*4

    else:     # 4th block, flip involved
        position = position + stepLen * np.array([cos(angle), sin(angle)])
        position = position + sqrt(2) * (stepLen-1) * \
            np.array([cos(angle + direction * pi/4),
                     sin(angle + direction * pi/4)])
        position = np.rint(position)
        angle = -pi/2 - angle
        direction *= -1
        p = (p-0.75)*4

print(position)
