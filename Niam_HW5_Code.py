## Niam HW5 Code
from numpy import linspace, meshgrid, mean, array
from matplotlib.pyplot import figure, savefig
from skimage.measure import marching_cubes
from geo import sphere, cuboid, cylinder, r_intersect, r_union

def create_mesh(center, domain, size, padding=1):
    return array(meshgrid(linspace(center[0] - domain[0]/2 - padding, center[0] + domain[0]/2 + padding, size),
                          linspace(center[1] - domain[1]/2 - padding, center[1] + domain[1]/2 + padding, size),
                          linspace(center[2] - domain[2]/2 - padding, center[2] + domain[2]/2 + padding, size)))

def visualize_geometry(shape_function, center, dimensions, grid, figure_id, subplot_position, image_name):
    shape_data = shape_function(center, *dimensions, grid)
    vertices, faces, _, _ = marching_cubes(shape_data, level=0, spacing=[1]*3)
    vertices -= mean(vertices, axis=0)
    ax = figure_id.add_subplot(subplot_position, projection='3d')
    ax.plot_trisurf(vertices[:, 0], vertices[:, 1], faces, vertices[:, 2])
    savefig(image_name)

def main():
    center = [0, 0, 0]
    dimensions = [2, 2, 2]  # Used for cuboid and cube; for sphere and cylinder, only the first element is used.
    grid_size = 100
    image_prefix = './alternative_imgs/'

    # Sphere
    sphere_grid = create_mesh(center, [1, 1, 1], grid_size, 0)
    fig = figure(figsize=(12, 5))
    visualize_geometry(sphere, center, [1], sphere_grid, fig, 111, f'{image_prefix}sphere_alternative.png')

    # Cuboid
    cuboid_grid = create_mesh(center, dimensions, grid_size)
    fig = figure(figsize=(12, 5))
    visualize_geometry(cuboid, center, dimensions, cuboid_grid, fig, 111, f'{image_prefix}cuboid_alternative.png')

    # Cylinder
    cylinder_grid = create_mesh(center, [1, 1, 4], grid_size)
    fig = figure(figsize=(12, 5))
    visualize_geometry(cylinder, center, [1, 4], cylinder_grid, fig, 111, f'{image_prefix}cylinder_alternative.png')

    # Additional examples can be added following the structure above.

if __name__ == '__main__':
    main()
