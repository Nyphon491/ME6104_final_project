## test speed measure
from pathlib import Path
import gcode, geo
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 10})
gcode_file_name = "box_large"

a = 30
del_mae_stop = 0.1

if __name__ == '__main__':
    img_dir = Path(Path.cwd() / "imgs")
    work_dir = Path(Path.cwd() / "test")
    gcode_file = Path(work_dir / "GCODE" / f"{gcode_file_name}.gcode")
    coords = gcode.load(gcode_file)
    slices = gcode.slice_sep(coords)

    mae = [-100]
    times_converge = []

    n_min = 2
    n_max = 2
    del_mae = del_mae_stop + 1
    while del_mae > del_mae_stop and not n_max > 100:
        n_max += 1

        new_slices = []
        slice_errors = []
        slice_segments = []

        num_lines = []
        new_num_lines = []
        segments = []
        errors = []
        times = []
        new_times = []

        for i, slice in enumerate(slices):
            slice_path = geo.pathtools.lines_path(slice[:, :-1], slice[:, -1])
            times.append(slice_path.get_path_time())
            num_lines.append(len(slice_path.segments))

            cont_paths = slice_path.cont_paths_by_angle(a)
            bezier_approx_lines = []
            for cont_path in cont_paths:
                if len(cont_path.coords) < n_min:
                    n = n_min
                elif len(cont_path.coords) > n_max:
                    n = n_max
                else:
                    n = len(cont_path.coords)
                approx_coords = np.array(geo.BezierCurve(cont_path.coords.T, n)).T
                approx_speeds = np.mean(cont_path.speeds[1:]) * np.ones(len(approx_coords))
                approx_path = geo.lines_path(approx_coords, approx_speeds)

                bezier_approx_lines.append(approx_path.coords)
                errors.append(approx_path.get_errors_by_segments(cont_path.coords))
                segments.append(approx_path.segments)
                new_times.append(approx_path.get_path_time())
                new_num_lines.append(len(approx_path.segments))
            new_slices.append(np.vstack(bezier_approx_lines))
            slice_segments.append(np.vstack(segments))
        
        del_mae = np.abs(np.mean(np.hstack(errors)) - mae[-1])
        mae.append(np.mean(np.hstack(errors)))
        times_converge.append(np.sum(new_times))
    mae = mae[1:]
        
    

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    x = range(n_min + 1, n_max + 1)
    ax1.plot(x, mae, label="MAE", c='b')
    ax2.plot(x, times_converge, label = "time", c='r')
    ax2.plot([n_min + 1, n_max], [np.sum(times), np.sum(times)], 'c--', label="original time")
    ax1.set_xlabel('n_max')
    ax1.set_ylabel('MAE', c='b')
    ax2.set_ylabel('time (min)', c='r')
    plt.title(f"model={gcode_file_name}, a={a}")
    plt.savefig(img_dir / f'{gcode_file_name}_convergence_plot_nmax_sweep_{a}.png')
    plt.close()

    lines_comp = [np.sum(num_lines), np.sum(new_num_lines)]
    times_comp = [str(np.around(np.sum(times), 2)), str(np.around(np.sum(new_times), 2))]

    colors = plt.cm.rainbow(np.linspace(0, 1, len(slices)))

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i, slice in enumerate(slices):
        ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i], alpha=0.75)
    plt.title(f"original slice\n# lines={lines_comp[0]}, time={times_comp[0]}")
    plt.savefig(img_dir / f"{gcode_file_name}.png")
    plt.close()

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    for i, slice in enumerate(new_slices):
        ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i], alpha=0.75)
    plt.title(f"new slice\nparameters: n_max={n_max}, a={a}"
              + f"\nmetrics: MAE={np.around(np.mean(np.hstack(errors)),2)}, "
              + f"# lines={lines_comp[1]}, time={times_comp[1]}")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(img_dir / f"{gcode_file_name}_{n_max}_{a}.png")
    plt.close()

    # plt.show()
    ##### graphs for presentation #####

    # slice = slices[1]
    # new_slice = new_slices[1]

    # p = geo.BezierCurve(slice.T, 100).T
    # p_coarse = geo.BezierCurve(p.T, 5).T
    # plt.figure()
    # plt.scatter(slice[:,0], slice[:,1], c='r', marker='o', label='g-code points')
    # plt.plot(p[:,0], p[:,1], c='b', linewidth=2, label='bezier curve', alpha=0.75)
    # plt.scatter(p_coarse[:,0], p_coarse[:,1], c='g', marker='o', label='sampled points')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.savefig(img_dir / f'polygonal_approximation_smooth_curve_recover.png')

    # p_path = geo.lines_path(np.array(geo.BezierCurve(slice.T, n_max).T))
    # errors = p_path.get_errors_by_segments(slice)

    # ermin = np.amin(errors)
    # ermax = np.amax(errors)
    # colors = plt.cm.viridis(np.linspace(0, 1, 100))

    # fig, ax = plt.subplots(layout='constrained')
    # ax.scatter(slice[:,0], slice[:,1], c='r')
    # for i, segment in enumerate(p_path.segments):
    #     color_index = np.argmin(np.abs(np.linspace(ermin, ermax, 100) - errors[i]))
    #     ax.plot(segment[:,0], segment[:,1], c=colors[color_index], linewidth=4)
    # fig.colorbar(
    #     mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(ermin, ermax), cmap=mpl.cm.viridis),
    #     ax=ax,  orientation='vertical', label='MAE error')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig(img_dir / f'polygonal_approximation_compare_to_original.png')

    # fig, ax = plt.subplots(layout='constrained')
    # ax.scatter(slice[:,0], slice[:,1], c='r')
    # for cont_path in geo.pathtools.lines_path(slice).cont_paths_by_angle(a):
    #     if len(cont_path.coords) < n_min:
    #         n = n_min
    #     elif len(cont_path.coords) > n_max:
    #         n = n_max
    #     else:
    #         n = len(cont_path.coords)
    #     approx_path = geo.lines_path(np.array(geo.BezierCurve(cont_path.coords.T, n)).T)
    #     errors = approx_path.get_errors_by_segments(cont_path.coords)
    #     for i, segment in enumerate(approx_path.segments):
    #         color_index = np.argmin(np.abs(np.linspace(ermin, ermax, 100) - errors[i]))
    #         ax.plot(segment[:,0], segment[:,1], c=colors[color_index], linewidth=4)
    # fig.colorbar(
    #     mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(ermin, ermax), cmap=mpl.cm.viridis),
    #     ax=ax,  orientation='vertical', label='MAE error')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig(img_dir / f'polygonal_approximation_compare_to_original_segmented.png')

    