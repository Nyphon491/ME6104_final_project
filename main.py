## test gcode parser
from pathlib import Path
import gcode
import matplotlib.pyplot as plt
import numpy as np


if __name__ == '__main__':
    work_dir = Path(Path.cwd() / "test")
    gcode_file = Path(work_dir / "GCODE" / "box_small.gcode")
    coords = gcode.load(gcode_file)
    slices = gcode.slice_sep(coords)


    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    color = plt.cm.rainbow(np.linspace(0, 1, len(slices)))
    for i, slice in enumerate(slices):
        ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=color[i])
    plt.savefig(work_dir / 'test_read.png')