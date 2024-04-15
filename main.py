## test slice path coarsener
from pathlib import Path
import gcode, geo
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    work_dir = Path(Path.cwd() / "test")
    gcode_file = Path(work_dir / "GCODE" / "box.gcode")
    coords = gcode.load(gcode_file)
    slices = gcode.slice_sep(coords)
    new_slices = []

    n_max = 6
    n_min = 2
    a = np.pi/12

    num_lines = len(np.vstack(slices)) - 1

    for i, slice in enumerate(slices):
        slice_path = geo.pathtools.lines_path(slice)
        cont_paths = slice_path.cont_paths_by_angle(a)
        bezier_lines = []
        for cont_path in cont_paths:
            if len(cont_path) < n_min:
                n = n_min
            elif len(cont_path) > n_max:
                n = n_max
            else:
                n = len(cont_path)
            bezier_lines.append(np.array(geo.BezierCurve(cont_path.T, n)).T)
        new_slices.append(np.vstack(bezier_lines))

    new_num_lines = len(np.vstack(new_slices)) - 1

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    colors = plt.cm.rainbow(np.linspace(0, 1, len(slices)))
    for i, slice in enumerate(slices):
        ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i])
    plt.title(f"original slice: {num_lines} lines")
    plt.savefig(work_dir / 'test_read_box.png')

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i, slice in enumerate(new_slices):
        ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i])
    plt.title(f"new slice: {new_num_lines} lines")
    plt.savefig(work_dir / 'test_cont_path_bezier_box.png')