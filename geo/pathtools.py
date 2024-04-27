from abc import ABC, abstractmethod
import numpy as np

class slice_path(ABC):
    def __init__(self, coords, speeds):
        self.coords = coords
        self.speeds = speeds

    @abstractmethod
    def angles(self, angle):
        pass


class lines_path(slice_path):
    def __init__(self, coords, speeds):
        super().__init__(coords, speeds)
        self.segments = self.get_segments()

    def get_segments(self):
        return np.array([[self.coords[i-1], self.coords[i]] for i in range(1, len(self.coords))])

    def angles(self):
        angles = []
        for segment in self.segments[:, :2]:
            diff = segment[1] - segment[0]
            angles.append(np.abs(np.arctan(diff[1] / diff[0])))
        return np.degrees(angles)
    
    def cont_paths_by_angle(self, change_allowed):

        angles = self.angles()
        cont_paths = []
        cont_path = [np.hstack([self.segments[0, 0, :], self.speeds[0]])]
        for i in range(1, len(angles)):
            if np.abs(angles[i] - angles[i - 1]) < change_allowed:
                cont_path.append(np.hstack([self.segments[i, 0, :], self.speeds[i]]))
            else:
                cont_path.append(np.hstack([self.segments[i-1, 1, :], self.speeds[i]]))
                cont_paths.append(lines_path(np.vstack(cont_path)[:,:-1], np.vstack(cont_path)[:,-1]))
                cont_path = [np.hstack([self.segments[i, 0, :], self.speeds[i]])]
        cont_path.append(np.hstack([self.segments[-1, 1, :], self.speeds[-1]]))
        cont_paths.append(lines_path(np.vstack(cont_path)[:,:-1], np.vstack(cont_path)[:,-1]))
        return cont_paths
    
    def get_errors_by_segments(self, p):
        errors = []
        for segment in self.segments[...,:2]:
            dxdy = segment[1] - segment[0]
            norm = np.array([-1*dxdy[1], dxdy[0]])
            errors.append(np.mean(np.abs(np.dot(p[:,:2], norm) - np.dot(segment[0], norm))))
        return np.array(errors)
    
    def get_segment_lengths(self):
        return np.array([np.linalg.norm(segment[1] - segment[0]) for segment in self.segments])
    
    def get_path_time(self):
        return np.sum(self.get_segment_lengths() / self.speeds[1:])
