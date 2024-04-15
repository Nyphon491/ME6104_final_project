import numpy as np
import matplotlib.pyplot as plt
import math


def BernsteinPoly(u, k, n):
    return math.comb(n, k) * u**k * (1 - u)**(n-k)


def BezierCurve(cp, num):
    n = cp.shape[1] - 1
    u = np.linspace(0, 1, num)
    B = np.array([BernsteinPoly(u,k,n) for k in range(n+1)])
    return cp @ B
