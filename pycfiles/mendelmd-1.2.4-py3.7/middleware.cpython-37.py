# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pagination/middleware.py
# Compiled at: 2019-05-07 08:43:55
# Size of source mod 2**32: 564 bytes


def get_page(self):
    """
    A function which will be monkeypatched onto the request to get the current
    integer representing the current page.
    """
    try:
        return int(self.REQUEST['page'])
    except (KeyError, ValueError, TypeError):
        return 1


class PaginationMiddleware(object):
    __doc__ = '\n    Inserts a variable representing the current page onto the request object if\n    it exists in either **GET** or **POST** portions of the request.\n    '

    def process_request(self, request):
        request.__class__.page = property(get_page)