import numpy as np
import math


class CompositeBezierCurve2():
    def __init__(self, pts, order):
        self.curves = []
        num_crvs = (len(pts)+1)/(order+1)
        for i in range(int(num_crvs)):
            if i == 0:
                pt_rng = (0, order+1)
            else:
                pt_rng = (order*i, order*(i+1)+1)
            self.curves.append(
                BezierCurve(pts[pt_rng[0]:pt_rng[1],:]))
        self.domain = len(self.curves)

    def pts(self):
        return np.array([crv.pts for crv in self.curves])

    def evaluate(self, u):
        p = []
        for i in range(self.domain):
            p_local = u[(i <= u) & (u < i+1)] - i
            p.append(self.curves[i].evaluate(p_local))
        return np.vstack(p)


class BezierCurve2():
    def __init__(self, pts):
        self.pts = pts
        n = len(pts)
        self.n = n
        self.coef = np.zeros((len(pts), len(pts)))
        pascal_tri = np.array([math.comb(n-1, i) for i in range(n)])
        for i in range(n):
            pascal_tri_i = np.array([math.comb(i, k)*(-1)**(k) for k in range(i+1)][::-1])
            self.coef[n-i-1, :len(pascal_tri_i)] = pascal_tri_i*pascal_tri[i]

    def evaluate(self, u):
        u_poly = np.fliplr(np.array([u**i for i in range(self.n)]).T)
        return u_poly @ self.coef @ self.pts
    
    def error(self, u):
        lines = self.evaluate(u)




def BernsteinPoly(u, k, n):
    return math.comb(n, k) * u**k * (1 - u)**(n-k)


def BezierCurveAcc(cp, num):
    n = cp.shape[1] - 1
    u = np.linspace(0, 1, num)
    Bpp = np.array([BernsteinPoly(u,k,n-2) for k in range(n-1)])
    cpp = np.array([cp[:, i-2] - 2*cp[:, i-1] + cp[:, i] for i in range(2, n+1)]).T
    return cpp @ Bpp


def BezierCurve(cp, num):
    n = cp.shape[1] - 1
    u = np.linspace(0, 1, num)
    B = np.array([BernsteinPoly(u,k,n) for k in range(n+1)])
    return cp @ B
