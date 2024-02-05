from pandas import read_csv

__all__ = ['read_availability_file']


def read_availability_file(filepath):
    """
    
    Reads the tech availability CSV file

    Returns:
        Dataframe with columns
            - address
            - latitude
            - longitude
            - Tech [name]
            - % of Routes
    
    """
    df = read_csv(filepath)
    return df
