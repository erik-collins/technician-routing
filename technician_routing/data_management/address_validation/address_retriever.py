from geopy.geocoders import GoogleV3

__all__ = ['AddressRetriever',]


class AddressRetriever:
    
    def __init__(self, google_api_key):
        if not google_api_key:
            raise ValueError('Google API Key was missing')
        
        self.geolocator = GoogleV3(google_api_key)

    def get_api_location(self, address_dirty):
        if not address_dirty:
            return None
        
        result = geolocator.geocode(address_dirty)
        if not result:
            return None
        
        address = result.address
        latitude = result.latitude
        longitude = result.longitude
        raw = result.raw
        
        return (address, latitude, longitude, raw)
