# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\sip\decorator.py
# Compiled at: 2009-05-24 05:43:15
__doc__ = '\nCreated on 2009-5-3\n\n@author: mingqi\n'
import logging
logger = logging.getLogger('sip.decorator')

def iter_fetch(max_result):
    """
    """

    def decorate(f):

        def fetch(*args_list, **agrs_dict):
            _iter_fetcher = IterFetcher(max_result, f, *args_list, **agrs_dict)
            return _iter_fetcher

        return fetch

    return decorate


class IterFetcher:

    def __init__(self, max_result, fetcher, *args_list, **args_dict):
        self.__fetcher = fetcher
        self.__args_list = args_list
        self.__args_dict = args_dict
        self.__max_result = max_result
        self.__count = 0
        self.__iter = iter([])

    def __iter__(self):
        return self

    def next(self):
        try:
            if self.__count >= self.__max_result:
                raise StopIteration()
            _o = self.__iter.next()
            self.__count = self.__count + 1
            return _o
        except StopIteration, e:
            if self.__count >= self.__max_result:
                raise e
            _container = self.__fetcher(*self.__args_list, **self.__args_dict)
            if _container == None:
                raise e
            if len(_container) == 0:
                raise e
            self.__iter = iter(_container)
            if not self.__args_dict.has_key('page_no'):
                self.__args_dict['page_no'] = 1
            self.__args_dict['page_no'] = self.__args_dict['page_no'] + 1
            return self.next()

        return