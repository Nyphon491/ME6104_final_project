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
        self.segments = self.get_segments()

    def get_segments(self):
        segments = []
        for i in range(1, len(self.coords)):
            segments.append([self.coords[i - 1], self.coords[i]])
        return np.array(segments)

    def angles(self):
        angles = []
        for segment in self.segments:
            diff = segment[1, :-1] - segment[0, :-1]
            line_angle = np.abs(np.arctan(diff[1] / diff[0]))
            angles.append(line_angle)
        return np.degrees(angles)
    
    def cont_paths_by_angle(self, change_allowed):
        angles = self.angles()
        cont_paths = []
        cont_path = [self.segments[0, 0, :]]
        for i in range(1, len(angles)):
            if np.abs(angles[i] - angles[i - 1]) < change_allowed:
                cont_path.append(self.segments[i, 0, :])
            else:
                cont_path.append(self.segments[i-1, 1, :])
                cont_paths.append(lines_path(np.vstack(cont_path)))
                cont_path = [self.segments[i, 0, :]]
        cont_path.append(self.segments[-1, 1, :])
        cont_paths.append(lines_path(np.vstack(cont_path)))
        return cont_paths
    
    def get_errors_by_segments(self, p):
        errors = []
        for segment in self.segments[:,:,:2]:
            dxdy = segment[1] - segment[0]
            norm = np.array([-1*dxdy[1], dxdy[0]])
            errors.append(np.mean(np.abs(np.dot(p[:,:2], norm) - np.dot(segment[0], norm))))
        return np.array(errors)
