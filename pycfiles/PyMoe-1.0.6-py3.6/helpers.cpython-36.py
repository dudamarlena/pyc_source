# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\Pymoe\Kitsu\helpers.py
# Compiled at: 2017-08-03 07:38:56
# Size of source mod 2**32: 1456 bytes
import requests

class SearchWrapper(list):
    __doc__ = '\n        :ivar _url str: Link to the next set of results\n        :ivar header dict: Headers needed for API calls\n    '

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