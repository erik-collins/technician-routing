from numpy import zeros

__all__ = ['calculate_distance_matrix',]


def calculate_distance_matrix(
        coordinates, 
        distance_delegate):
    """
    
        Calculate an N x N matrix of distances between coordinates
         - N = length of coordinates
    
        Parameters:
        - coordinates: list of coordinates, tuples of latitude and longitude
        - distance_delegate:  function from (coordinates_1, coordinates_2) to distance between them

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
