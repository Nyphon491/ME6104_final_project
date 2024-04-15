from abc import ABC, abstractmethod
import numpy as np

class slice_path(ABC):
    def __init__(self, coords):
        self.coords = coords

    @abstractmethod
    def angles(self, angle):
        pass


class lines_path(slice_path):
    def __init__(self, coords):
        super().__init__(coords)

    def get_segments(self):
        segments = []
        coords = self.coords
        for i in range(1, len(coords)):
            segments.append([coords[i - 1], coords[i]])
        return segments

    def angles(self):
        segments = np.array(self.get_segments())
        angles = []
        for segment in segments:
            diff = segment[1, :-1] - segment[0, :-1]
            line_angle = np.abs(np.arctan(diff[1] / diff[0]))
            angles.append(line_angle)
        return angles
    
    def cont_paths_by_angle(self, change_allowed):
        segments = np.array(self.get_segments())
        angles = self.angles()
        cont_paths = []
        cont_path = [segments[0, 0, :]]
        for i in range(1, len(angles)):
            if np.abs(angles[i] - angles[i - 1]) < change_allowed:
                cont_path.append(segments[i, 0, :])
            else:
                cont_paths.append(np.vstack(cont_path))
                cont_path = [segments[i, 0, :]]
        cont_path.append(segments[i, 1, :])
        cont_paths.append(np.vstack(cont_path))
        return cont_paths
