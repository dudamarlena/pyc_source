# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/alphahome/response/response.py
# Compiled at: 2017-08-07 10:54:31


class Response(object):
    """
    views返回值
    """

    def __init__(self, status_code, appinfo=None, message=None):
        self.code = status_code
        self.appinfo = appinfo
        self.message = message
        if appinfo is None:
            self.appinfo = {}
        if message is None:
            self.message = ''
        return


class Success(Response):
    """
    成功返回值
    """

    def __init__(self, appinfo):
        super(Success, self).__init__(200, appinfo)


class Failure(Response):
    """
    失败返回值
    """

    def __init__(self, status_code, message):
        super(Failure, self).__init__(status_code, message=message)


_200_SUCCESS = 200
_400_BAD_REQUEST = 400
_404_NOT_FOUND = 404