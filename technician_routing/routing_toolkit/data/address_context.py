from ..config import Config
from .technician_availability import read_availability_file
from .client_addresses import read_client_address_file

__all__ = ['AddressContext',]


class AddressContext:
    def __init__(self, df_tech_availability, df_client_addresses):
        self.df_tech_availability = df_tech_availability
        self.df_client_addresses = df_client_addresses





    @classmethod
    def from_config(config: Config, month: int)
        df_client_addresses = read_client_address_file(config.client_addresses_filepath, month)
        df_tech_availability = read_availability_file(config.technician_availability_filepath)
        return AddressContext(
            df_tech_availability,
            df_client_addresses
        )