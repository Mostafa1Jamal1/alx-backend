#!/usr/bin/env python3
"""BasicCache Module
"""

from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """Defines basic caching module
    """
    def put(self, key, item):
        """assign to the dictionary self.cache_data
        the item value for the key key.
        If key or item is None, this method will do nothing.
        """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """return the value in self.cache_data linked to key.
        """
        return self.cache_data.get(key)
