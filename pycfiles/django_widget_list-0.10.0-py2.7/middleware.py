# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\widget_list\middleware.py
# Compiled at: 2013-05-18 11:27:44


def request(self):
    """
    Get request
    """
    return self.REQUEST


class PaginationMiddleware(object):
    """
    Inserts a variable representing the current page onto the request object if
    it exists in either **GET** or **POST** portions of the request.
    """

    def process_request(self, request):
        request.__class__.page = property(get_page)