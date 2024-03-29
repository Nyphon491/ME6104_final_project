## test python environment
import numpy as np
import matplotlib.pyplot as plt
from skimage import measure
import geo


def plot_verts(f, domain, domain_length, fig, subplt_loc, subplt_spc=-0.25):
    spacing = [(domain[0][1] - domain[0][0])/domain_length,
               (domain[1][1] - domain[1][0])/domain_length,
               (domain[2][1] - domain[2][0])/domain_length]
    verts, faces, normals, values = measure.marching_cubes(f, 0, spacing=spacing)
    verts[:, 0] = verts[:, 0] - np.mean(verts[:, 0])
    verts[:, 1] = verts[:, 1] - np.mean(verts[:, 1])
    verts[:, 2] = verts[:, 2] - np.mean(verts[:, 2])
    if subplt_loc == 121:
        subplt_spc = -subplt_spc
    ax = fig.add_subplot(subplt_loc, projection='3d', position=(subplt_spc, 0, 1, 1))
    ax.plot_trisurf(verts[:, 0], verts[:, 1], faces, verts[:, 2])


if __name__ == '__main__':
    #----------------------    Sphere    ----------------------#
    gsize = 100  # increase for smoothness
    c = [0,0,0]
    r = 1
    gdom = [c[0] - r, c[0] + r]

    glinspace = np.linspace(gdom[0], gdom[1], gsize)
    ginc = (gdom[1] - gdom[0])/gsize
    grid = np.array(np.meshgrid(glinspace, glinspace, glinspace))

    f = geo.sphere(c, r, grid)

    fig = plt.figure(figsize=(12,5))
    plot_verts(f, [gdom, gdom, gdom], gsize, fig, 111, subplt_spc=0)
    plt.savefig('./imgs/sphere.png')


    #----------------------    Cuboid    ----------------------#
    gsize = 100
    c = np.array([0,0,0])
    dims = [2, 2, 2]
    pad = 1
    gdom = [[c[0] - dims[0]/2 - pad, c[0] + dims[0]/2 + pad],
            [c[1] - dims[1]/2 - pad, c[1] + dims[1]/2 + pad],
            [c[2] - dims[2]/2 - pad, c[2] + dims[2]/2 + pad]]
    grid = np.array(np.meshgrid(np.linspace(gdom[0][0], gdom[0][1], gsize),
                                np.linspace(gdom[1][0], gdom[1][1], gsize),
                                np.linspace(gdom[2][0], gdom[2][1], gsize)))

    f_max = geo.cuboid(c, dims, grid)
    f_r = geo.cuboid(c, dims, grid,
                     intersect_fn= lambda f_list : geo.r_intersect(f_list, 0))

    fig = plt.figure(figsize=(12,5))
    plot_verts(f_max, gdom, gsize, fig, 111)
    plot_verts(f_r, gdom, gsize, fig, 121)
    plt.savefig('./imgs/cuboid.png')


    #----------------------    Cylinder    ----------------------#
    gsize = 100
    c = [0,0,0]
    h = 4
    r = 1
    pad = 1
    gdom = [[c[0] - r - pad, c[0] + r + pad],
            [c[1] - r - pad, c[1] + r + pad],
            [c[2] - h/2 - pad, c[2] + h/2 + pad]]
    grid = np.array(np.meshgrid(np.linspace(gdom[0][0], gdom[0][1], gsize),
                                np.linspace(gdom[1][0], gdom[1][1], gsize),
                                np.linspace(gdom[2][0], gdom[2][1], gsize)))

    f_max = geo.cylinder(c, r, h, grid)
    f_r = geo.cylinder(c, r, h, grid,
                       intersect_fn= lambda f_list : geo.r_intersect(f_list, 0))

    fig = plt.figure(figsize=(12,5))
    plot_verts(f_max, gdom, gsize, fig, 111)
    plot_verts(f_r, gdom, gsize, fig, 121)
    plt.savefig('./imgs/cylinder.png')


    #----------------------    Cube & Cylinder union    ----------------------#
    gsize = 100
    c = [0,0,0]
    pad = 2
    gdom = [[c[0] - pad, c[0] + pad],
            [c[1] - pad, c[1] + pad],
            [c[2] - pad, c[2] + pad]]
    grid = np.array(np.meshgrid(np.linspace(gdom[0][0], gdom[0][1], gsize),
                                np.linspace(gdom[1][0], gdom[1][1], gsize),
                                np.linspace(gdom[2][0], gdom[2][1], gsize)))

    f_cube = geo.cuboid([0, 0, 0], [1, 1, 1], grid)
    f_cylinder = geo.cylinder([0, 0, 0.6], 0.1, 0.2, grid)
    f_maxmin = np.min([f_cube, f_cylinder], axis=0)

    f_cube = geo.cuboid([0, 0, 0], [1, 1, 1], grid,
                        intersect_fn= lambda f_list : geo.r_intersect(f_list, 0))
    f_cylinder = geo.cylinder([0, 0, 0.6], 0.1, 0.2, grid,
                              intersect_fn= lambda f_list : geo.r_intersect(f_list, 0))
    f_r = geo.r_union([f_cube, f_cylinder], 0)

    fig = plt.figure(figsize=(12,5))
    plot_verts(f_maxmin, gdom, gsize, fig, 111)
    plot_verts(f_r, gdom, gsize, fig, 121)
    plt.savefig('./imgs/cube_cyl_union.png')


    #----------------------    Sphere -> Box metamorphasis    ----------------------#
    f_sphere = geo.sphere([0,0,0], 1, grid)
    
    t = np.linspace(0, 1, 11)
    f_metamorph = geo.metamorphasis(f_sphere, f_r, t)
    for i, f in enumerate(f_metamorph):
        fig = plt.figure()
        plot_verts(f, gdom, gsize, fig, 111, subplt_spc=0)
        plt.savefig(f'./imgs/cube_sphere_metamorph_{i}.png')