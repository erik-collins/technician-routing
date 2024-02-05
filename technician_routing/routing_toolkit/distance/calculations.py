from numpy import zeros
# from haversine import haversine, Unit

# from typing import Callable

# __all__ = ['locateOptimalElbow', 'calculate_distances', 'get_drive_distance']

__all__ = ['calculate_distance_matrix',]


def calculate_distance_matrix(coordinates, distance_delegate):
    """
    
        Calculate an N x N matrix of distances between coordinates
         - N = length of coordinates
    

    """

    size = len(coordinates)
    distances = zeros(shape=tuple([size,]*2))

    for ix in range(size):
        coordinates_x = coordinates[ix]
        for iy in range(size):
            if ix == iy:
                continue # already zero
            elif ix > iy:
                distances[ix, iy] = distances[iy, ix] # already calculated
            else:
                coordinates_y = coordinates[iy]
                distances[ix, iy] = distance_delegate(coordinates_x, coordinates_y)
    
    return distances

# def locateOptimalElbow(x, y):
#     # START AND FINAL POINTS
#     p1 = (x[0], y[0])
#     p2 = (x[-1], y[-1])
    
#     # EQUATION OF LINE: y = mx + c
#     m = (p2[1] - p1[1]) / (p2[0] - p1[0])
#     c = (p2[1] - (m * p2[0]))
    
#     # DISTANCE FROM EACH POINTS TO LINE mx - y + c = 0
#     a, b = m, -1
#     dist = np.array([abs(a*x0+b*y0+c)/math.sqrt(a**2+b**2) for x0, y0 in zip(x,y)])
#     return np.argmax(dist) + x[0]


# def calculate_distances(df, mph = 30):
#     addresses = df['address'].unique()
#     distances = np.zeros(shape = (len(addresses), len(addresses)))
    
#     for i_idx, i in enumerate(addresses):
#         i_coord = tuple(df[df['address'] == i][['lat', 'long']].values.tolist()[0])
#         for j_idx, j in enumerate(addresses):
#             j_coord = tuple(df[df['address'] == j][['lat', 'long']].values.tolist()[0])
#             distances[i_idx, j_idx] = hs.haversine(i_coord, j_coord, unit=Unit.MILES) / (mph / 60)
    
#     return distances

# def calculate_durations(coordinates,  mph = None):

    

# def calculate_duration(coordinates_a, coordinates_b, mph = None):
#     if mph is None:
#         mph = 30
#     elif mph <= 0:
#         raise ValueError(f'Invalid mph {mph}')
    
#     distance = hs.haversine(coordinates_a, coordinates_b, unit=Unit.MILES)

#     return distance / (mph / 60)