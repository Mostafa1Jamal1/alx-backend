#!/usr/bin/env python3
"""LFUCache Module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Defines LFU caching module
    """

    def __init__(self):
        """Initiliaze
        """
        super().__init__()
        self.keys = list()

    def put(self, key, item):
        """Assign item to cache using LFU replacement policy.
        """
        if key is None or item is None:
            return
        freq = 0
        if key not in self.cache_data:
            if len(self.cache_data) >= self.MAX_ITEMS:
                # Discard
                self.cache_data.pop(self.keys[0][0])
                print("DISCARD: {}".format(self.keys[0][0]))
                self.keys.pop(0)
        else:
            for t_key in self.keys:
                if key in t_key:
                    freq = t_key[1]
                    self.keys.remove(t_key)
        self.cache_data[key] = item
        self.keys.append([key, freq + 1])
        # arrange
        for i, t_key in reversed(list(enumerate(self.keys))):
            if self.keys[i][1] >= self.keys[i - 1][1] or i == 0:
                break
            temp = self.keys[i]
            self.keys[i] = self.keys[i - 1]
            self.keys[i - 1] = temp

    def get(self, key):
        """Return value linked to key from cache.
        """
        for i in range(len(self.keys)):
            if key == self.keys[i][0]:
                self.keys[i][1] += 1
                break
        for i in range(len(self.keys) - 1):
            to_get = self.keys[i][0]
            if self.keys[i][1] >= self.keys[i + 1][1] and key == to_get:
                temp = self.keys[i]
                self.keys[i] = self.keys[i + 1]
                self.keys[i + 1] = temp
        return self.cache_data.get(key)
