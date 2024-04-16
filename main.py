## test slice path coarsener
from pathlib import Path
import gcode, geo
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 10})

if __name__ == '__main__':
    img_dir = Path(Path.cwd() / "imgs")
    work_dir = Path(Path.cwd() / "test")
    gcode_file = Path(work_dir / "GCODE" / "box_small.gcode")
    coords = gcode.load(gcode_file)
    slices = gcode.slice_sep(coords)


    # for a in [30, 15, 5]:
    #     fig, ax1 = plt.subplots()
    #     angle_total_num_lines = []
    #     angle_total_errors = []
    #     for n_max in range(3, 11):
    new_slices = []
    slice_errors = []
    slice_segments = []

    n_max = 6
    n_min = 2
    a = 15

    num_lines = len(np.vstack(slices)) - 1
    errors = []
    segments = []

    for i, slice in enumerate(slices):
        slice_path = geo.pathtools.lines_path(slice)
        cont_paths = slice_path.cont_paths_by_angle(a)
        bezier_approx_lines = []
        for cont_path in cont_paths:
            if len(cont_path.coords) < n_min:
                n = n_min
            elif len(cont_path.coords) > n_max:
                n = n_max
            else:
                n = len(cont_path.coords)
            approx_path = geo.lines_path(np.array(geo.BezierCurve(cont_path.coords.T, n)).T)
            bezier_approx_lines.append(approx_path.coords)
            errors.append(approx_path.get_errors_by_segments(cont_path.coords))
            segments.append(approx_path.segments)
        new_slices.append(np.vstack(bezier_approx_lines))
        slice_errors.append(np.hstack(errors))
        slice_segments.append(np.vstack(segments))


        #     angle_total_num_lines.append(new_num_lines)
        #     angle_total_errors.append(total_error)
        # ax2 = ax1.twinx()
        # ax1.plot(range(3, 11), angle_total_num_lines, label="number of lines", c='b')
        # ax2.plot(range(3, 11), angle_total_errors, label = "MAE", c='r')
        # ax1.set_xlabel('n_max')
        # ax1.set_ylabel('number of lines', c='b')
        # ax2.set_ylabel('MAE', c='r')
        # # plt.legend()
        # plt.title(f"speed versus accuracy trade-off for a = {a}")
        # plt.savefig(img_dir / f'convergence_plot_nmax_sweep_{a}.png')
        # plt.close()


            # ermin = np.amin(np.hstack(slice_errors))
            # ermax = np.amax(np.hstack(slice_errors))
            # colors = plt.cm.rainbow(np.linspace(0, 1, len(slices)))

            # fig = plt.figure()
            # ax = fig.add_subplot(projection='3d')
            # for i, slice in enumerate(slices):
            #     ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i], alpha=0.75)
            # # plt.title(f"original slice: {num_lines} lines")
            # plt.title(f"original")
            # plt.savefig(img_dir / 'box_large.png')

            # fig = plt.figure()
            # ax = fig.add_subplot(projection='3d')
            # for i, slice in enumerate(new_slices):
            #     ax.plot(slice[..., 0], slice[..., 1], slice[..., 2], c=colors[i], alpha=0.75)
            # # for i, segments in enumerate(slice_segments):
            # #     for j, segment in enumerate(segments):
            # #         ci = np.argmin(np.abs(np.linspace(ermin, ermax, 100) - slice_errors[i][j]))
            # #         ax.plot(segment[..., 0], segment[..., 1], segment[..., 2], c=colors[ci])
            # plt.title(f"{n_max} lines per segment, a = {a}\nMAE = {np.around(np.mean(np.hstack(slice_errors)),2)}")
            # # fig.colorbar(
            # #     mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(ermin, ermax), cmap=mpl.cm.viridis),
            # #     ax=ax,  orientation='vertical', label='MAE error')
            # plt.xlabel('x')
            # plt.ylabel('y')
            # plt.savefig(img_dir / f'box_large_{n_max}_{a}.png')
            # plt.close()

    # plt.show()
    ##### graphs for presentation #####

    slice = slices[1]
    new_slice = new_slices[1]

    p = geo.BezierCurve(slice.T, 100).T
    p_coarse = geo.BezierCurve(p.T, 5).T
    plt.figure()
    plt.scatter(slice[:,0], slice[:,1], c='r', marker='o', label='g-code points')
    plt.plot(p[:,0], p[:,1], c='b', linewidth=2, label='bezier curve', alpha=0.75)
    plt.scatter(p_coarse[:,0], p_coarse[:,1], c='g', marker='o', label='sampled points')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.savefig(img_dir / f'polygonal_approximation_smooth_curve_recover.png')

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
    
    # pts = np.array([
    # [-2, -2],
    # [3, 15],
    # [5, 2],
    # [11, 10]])
    # bcurve = geo.BezierCurve2(pts)

    # for i in range(2, 15):
    #     u_fine = np.linspace(0, 1, 1000)
    #     p1 = bcurve.evaluate(u_fine)
    #     u_sparse = np.linspace(0, 1, i)
    #     p2 = bcurve.evaluate(u_sparse)
    #     plt.figure()
    #     plt.plot(p1[:,0], p1[:,1], c='blue', label='Cubic curve')
    #     plt.plot(p2[:,0], p2[:,1], c='red', label='polygonal approximate')
    #     plt.legend()
    #     plt.savefig(img_dir / f'polygonal_approximation_example_{i}.png')

    # u = np.linspace(0, 1, 10)
    # p = bcurve.evaluate(u)
    # polycurve = geo.pathtools.lines_path(np.hstack([p, np.zeros([len(p), 1])]))
    # angles = polycurve.angles()
    # amin = np.amin(angles)
    # amax = np.amax(angles)
    # segs = polycurve.get_segments()
    # colors = plt.cm.viridis(np.linspace(0, 1, len(segs)))
    # fig, ax = plt.subplots(layout='constrained')
    # for i, seg in enumerate(segs):
    #     color_index = np.argmin(np.abs(np.linspace(amin, amax, len(segs)) - angles[i]))
    #     ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]],
    #             c=colors[color_index], linewidth=4)
    # fig.colorbar(
    #     mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(amin, amax), cmap=mpl.cm.viridis),
    #     ax=ax,  orientation='vertical', label='angle (°) to x-axis')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig(img_dir / f'polygonal_approximation_angle.png')


    # angle_diffs = []
    # for i in range(1, len(angles)):
    #     angle_diffs.append(np.abs(angles[i] - angles[i-1]))
    # angle_diffs.append(0)
    # amin = np.amin(angle_diffs)
    # amax = np.amax(angle_diffs)
    # colors = plt.cm.viridis(np.linspace(0, 1, len(segs)))
    # fig, ax = plt.subplots(layout='constrained')
    # for i, seg in enumerate(segs):
    #     color_index = np.argmin(np.abs(np.linspace(amin, amax, len(segs)) - angle_diffs[i]))
    #     ax.plot([seg[0][0], seg[1][0]], [seg[0][1], seg[1][1]],
    #             c=colors[color_index], linewidth=4)
    # fig.colorbar(
    #     mpl.cm.ScalarMappable(norm=mpl.colors.Normalize(amin, amax), cmap=mpl.cm.viridis),
    #     ax=ax,  orientation='vertical', label='angle (°) difference to next angle')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.savefig(img_dir / f'polygonal_approximation_angle_diffs.png')

    # angle_threshold = 20
    # cont_paths = []
    # cont_path = [segs[0]]
    # for i in range(1, len(angle_diffs)):
    #     if angle_diffs[i] < angle_threshold:
    #         cont_path.append(segs[i])
    #     else:
    #         cont_paths.append(np.vstack(cont_path))
    #         cont_path = [segs[i]]
    # cont_paths.append(np.vstack(cont_path))
    # colors = plt.cm.rainbow(np.linspace(0, 1, len(cont_paths)))
    # fig, ax = plt.subplots(layout='constrained')
    # for i, path in enumerate(cont_paths):
    #     ax.plot(path[:,0], path[:,1], c=colors[i], label=f"curve {i+1}",
    #             linewidth=4)
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.legend()
    # plt.savefig(img_dir / f'polygonal_approximation_angle_cont_paths.png')

    