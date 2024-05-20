#!/usr/bin/env python3
''' Simple helper function '''

import csv
import math
from typing import List


def index_range(page: int, page_size: int) -> tuple:
    """return a tuple of size two containing
    a start index and an end index corresponding to the range of indexes
    """
    return tuple([(page - 1) * page_size, page * page_size])


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """verify that both arguments are integers greater than 0
        return the appropriate page of the dataset (the correct list of rows)
        """
        assert type(page) == int
        assert type(page_size) == int
        assert page > 0
        assert page_size > 0
        i_range = index_range(page, page_size)
        return self.dataset()[i_range[0]: i_range[1]]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """Hypermedia pagination
        """
        data = self.get_page(page, page_size)
        total_pages = math.ceil(len(self.__dataset) / page_size)
        return {'page_size': len(data),
                'page': page,
                'data': data,
                'next_page': None if page > total_pages else page + 1,
                'prev_page': None if page == 1 else page - 1,
                'total_pages': total_pages,
                }
