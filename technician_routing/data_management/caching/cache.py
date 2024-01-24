from abc import ABC

__all__ = ['Cache',]


class Cache(ABC):

    def __init__(self):
        self.data = None

    def save(self) -> None:
        pass

    def load(self) -> None:
        pass
