#!/usr/bin/env python3
"""FIFOCache Module
"""

from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """Defines LRU caching module
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
                self.cache_data.pop(self.keys[0])
                print("DISCARD: {}".format(self.keys[0]))
                self.keys.pop(0)
            if key in self.keys:
                self.keys.remove(key)
            self.keys.append(key)
            self.cache_data[key] = item

    def get(self, key):
        """Return value linked to key from cache.
        """
        if key in self.keys:
            self.keys.remove(key)
            self.keys.append(key)
        return self.cache_data.get(key)
