from typing import Callable

from .cache import Cache

__all__ = ['MemoizedFunction',]


class MemoizedFunction:

    def __init__(self, cache: Cache, delegate: Callable):
        self.cache = cache or ValueError(f'Cache manager is required')
        self.delegate = delegate or ValueError('Delegate is missing')

    
    def new_reader(self, persistence_frequency = 100):
        freq = persistence_frequency
        cache = self.cache
        f = self.delegate
        i = 0
        def get_item(key):
            nonlocal i
            #print(key)
            if key in cache:
                #print('Read Cache for',key)
                return cache[key]
            item = f(key)
            #print('Hit API for', key)
            cache[key] = item
            i = i + 1
            if i % freq == 0:
                cache.save()
                
            return item
                
        return get_item
