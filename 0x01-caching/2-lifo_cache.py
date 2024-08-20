#!/usr/bin/env python3
"""FIFOCache Module
"""

from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Defines LIFO caching module
    """

    def __init__(self):
        """Initiliaze
        """
        super().__init__()
        self.keys = list()

    def put(self, key, item):
        """Assign item to cache using LIFO replacement policy.
        """
        data = self.cache_data
        if key and item:
            if key not in data and len(data) >= self.MAX_ITEMS:
                self.cache_data.pop(self.keys[-1])
                print("DISCARD: {}".format(self.keys.pop()))
            self.cache_data[key] = item
            self.keys.append(key)

    def get(self, key):
        """Return value linked to key from cache.
        """
        return self.cache_data.get(key)
