from json import dump as json_dump, load as json_load
from os.path import exists, makedirs, split
from typing import Optional

from .cache import Cache
    
__all__ = ['JsonCache',]


class JsonCache(Cache):

    def __init__(self, filepath: str):
        self.filepath = filepath or raise ValueError('Missing filepath')

        containing_directory, _ = split(filepath)
        if not exists(containing_directory):
            makedirs(containing_directory)

        super().__init__(self)

    def save(self) -> None:
        with open(self.filepath, 'w') as fl:
            json_dump(self.data, fl)

    def load(self) -> None:
        if not exists(self.filepath):
            return None

        with open(self.filepath,'r') as fl:
            self.data = json_load(fl)
        print('Read Cache, elements:', len(self.data))
