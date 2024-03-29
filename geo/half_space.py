import numpy as np


def metamorphasis(f1, f2, t_steps):
    f = []
    for t in t_steps:
        f.append(f1*(1 - t) + f2*t)
    return f

def r_intersect(f_list, a):
    f = f_list[0]
    for f2 in f_list[1:]:
        f = (1/(1+a))*(f + f2 + np.sqrt(f**2 + f2**2 - 2*a*f*f2))
    return f


def r_union(f_list, a):
    f = f_list[0]
    for f2 in f_list[1:]:
        f = (1/(1+a))*(f + f2 - np.sqrt(f**2 + f2**2 - 2*a*f*f))
    return f


def sphere(center, radius, mesh_grid):
    x = mesh_grid[0,...]
    y = mesh_grid[1,...]
    z = mesh_grid[2,...]
    return (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 - radius**2


def cuboid(center, dims, mesh_grid,
           intersect_fn = lambda f_list : np.max(f_list, axis=0)):
    x = mesh_grid[0,...]
    y = mesh_grid[1,...]
    z = mesh_grid[2,...]
    dx = center[0] + dims[0]/2
    dy = center[1] + dims[1]/2
    dz = center[2] + dims[2]/2

    f_right = x - dx
    f_left = -dx - x
    f_back = y - dy
    f_front = -dy - y
    f_top = z - dz
    f_bottom = -dz - z
    return intersect_fn([f_right, f_left, f_back, f_front, f_top, f_bottom])


def cylinder(center, radius, height, mesh_grid,
            intersect_fn = lambda f_list : np.max(f_list, axis=0)):
    x = mesh_grid[0,...]
    y = mesh_grid[1,...]
    z = mesh_grid[2,...]
    dz = center[2] + height/2

    f_top = z - dz
    f_bottom = -dz - z
    f_cylinder = (x - center[0])**2 + (y - center[1])**2 - radius**2
    return intersect_fn([f_top, f_bottom, f_cylinder])
