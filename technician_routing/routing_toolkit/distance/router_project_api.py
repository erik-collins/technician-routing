from json import loads
from requests import get as get_request

__all__ = ['get_drive_distance', 'get_drive_distance_df']


URI_ROOT = 'http://router.project-osrm.org/route/v1/car/'

def get_drive_distance_df(df, a,b):
    srs_a = df[df.loc[:, 'address'] == a]
    longitude_a = srs_a.loc[:, 'longitude'].values[0]
    latitude_a = srs_a.loc[:, 'latitude'].values[0]

    srs_b = df[df.loc[:, 'address'] == b]
    longitude_b = srs_b.loc[:, 'longitude'].values[0]
    latitude_b = srs_b.loc[:, 'latitude'].values[0]

    return get_drive_distance(
        (longitude_a, latitude_a),
        (longitude_b, latitude_b)
    )
    

def get_drive_distance(coordinates_a, coordinates_b):
    longitude_a, latitude_a = coordinates_a
    longitude_b, latitude_b = coordinates_b

    r = get_request(f"{URI_ROOT}{longitude_a},{latitude_a};{longitude_b},{latitude_b}")
    req = loads(r.content)
    duration = req['routes'][0]['duration'] / 60
    return duration
