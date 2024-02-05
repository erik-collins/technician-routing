__all__ = ['Config',]

class Config:
    def __init__(
            self,
            google_api_key_filepath,
            technician_availability_filepath,
            client_addresses_filepath
    ):
        self.google_api_key_filepath = google_api_key_filepath
        self.technician_availability_filepath = technician_availability_filepath
        self.client_addresses_filepath = client_addresses_filepath
