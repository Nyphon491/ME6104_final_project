import numpy as np

def load(file):
    coords = []
    with open(file, 'r') as f:
        lines = f.readlines()
        z = '0'
        for line in lines:
            line = line.split(' ')
            for item in line:
                if len(item) > 0 and item[0] == 'Z':
                    z = item[1:]
            # if len(line) > 4 and line[0] == 'G0' and line[4][0] == 'Z':
            #     z = line[3][1:]
            if line[0] == 'G1' and line[-1][:1] == 'E':
                coords.append([line[1][1:], line[2][1:], z])
    return np.array(coords).astype(np.float32)

def slice_sep(coords):
    slices = []
    slice = [coords[0, ...]]
    for coord in coords[1:, ...]:
        if coord[-1] == slice[-1][-1]:
            slice.append(coord)
        else:
            slices.append(np.array(slice))
            slice = [coord]
    return slices