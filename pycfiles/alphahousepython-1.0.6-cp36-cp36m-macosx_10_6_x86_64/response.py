# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/alphahome/response/response.py
# Compiled at: 2017-08-07 10:54:31


class Response(object):
    u"""
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
    u"""
    成功返回值
    """

    def __init__(self, appinfo):
        super(Success, self).__init__(200, appinfo)


class Failure(Response):
    u"""
    失败返回值
    """

    def __init__(self, status_code, message):
        super(Failure, self).__init__(status_code, message=message)


_200_SUCCESS = 200
_400_BAD_REQUEST = 400
_404_NOT_FOUND = 404