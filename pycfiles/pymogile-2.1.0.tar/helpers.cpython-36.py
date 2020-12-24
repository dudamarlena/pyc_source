# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Kitsu\helpers.py
# Compiled at: 2017-08-03 07:38:56
# Size of source mod 2**32: 1456 bytes
import requests

class SearchWrapper(list):
    """SearchWrapper"""

    def __init__(self, data, link, headers):
        super().__init__(data)
        self._url = link
        self.header = headers

    def __iter__(self):
        return self

    def __next__(self):
        if self.__len__():
            return self.pop()
        else:
            if self._url is None:
                raise StopIteration
            else:
                r = requests.get((self._url), headers=(self.header))
                if r.status_code != 200:
                    raise StopIteration
                else:
                    jsd = r.json()
                    self._url = jsd['links']['next'] if 'next' in jsd['links'] else None
                    self.extend(jsd['data'])
                    return self.pop()

    def next(self):
        """
        This is simply an alias for __next__. Included for compatibility and ease of use.

        :return: the next result
        """
        return self.__next__()