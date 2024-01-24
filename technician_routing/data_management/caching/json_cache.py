from json import dump as json_dump, load as json_load
from os.path import exists, split
from os import makedirs
from typing import Optional

from .cache import Cache
    
__all__ = ['JsonCache',]


class JsonCache(Cache):

    def __init__(self, filepath: str):
        if not filepath:
            raise ValueError('Missing filepath')

        self.filepath = filepath

        containing_directory, _ = split(filepath)
        if not exists(containing_directory):
            makedirs(containing_directory)

        super().__init__()

    def save(self) -> None:
        with open(self.filepath, 'w') as fl:
            json_dump(self.data, fl)

    def load(self) -> None:
        if not exists(self.filepath):
            print(f'Warning, no data at {self.filepath}')
            self.data = {}
            return

        with open(self.filepath,'r') as fl:
            self.data = json_load(fl)
        print('Read Cache, elements:', len(self.data))
