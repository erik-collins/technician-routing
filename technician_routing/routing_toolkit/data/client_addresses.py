from pandas import read_csv

__all__ = ['read_client_address_file',]


def read_client_address_file(filepath, month):
    """
    
    Reads the client addresses CSV file

    Returns:
        Dataframe with columns
            - address
            - latitude
            - longitude
            - Month [of service?]
    
    """
    df = read_csv(filepath)
    filtered = df[df.loc[:, 'Month'] == f'{month}']
    return filtered
