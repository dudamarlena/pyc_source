# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: .\django\core\beans.py
# Compiled at: 2018-01-30 07:05:48
# Size of source mod 2**32: 1925 bytes


class Struct(object):

    def __init__(self, adict={}):
        self.__dict__.update(adict)
        for k, v in adict.items():
            if isinstance(v, dict):
                self.__dict__[k] = Struct(v)

    def create(adict):
        return Struct(adict)


class Result(object):
    STATUS = Struct({'SUCCESS': 'SUCCESS', 
     'INPROGRESS': 'INPROGRESS', 
     'FAILED': 'FAILED', 
     'ERROR': 'ERROR'})

    def __init__(self):
        self.status = None
        self.error = None
        self.data = None
        self.info = None

    def __iter__(self):
        yield (
         'status', self.status)
        yield ('error', self.error)
        yield ('data', self.data)
        yield ('info', self.info)

    def create(status, data=None, error=None, info=None):
        r = Result()
        if isinstance(status, str):
            r.status = status
        r.data = data
        if error is not None and isinstance(error, (dict, list, str)):
            r.error = error
        if info is not None and isinstance(error, (dict, str)):
            r.info = info
        return r

    def success(data=None, info=None):
        return Result.create(Result.STATUS.SUCCESS, data, None, info)

    def error(error=None, info=None):
        return Result.create(Result.STATUS.ERROR, None, error, info)

    def error(code, text=None, info=None):
        de = {'code': code}
        if text is not None and isinstance(text, str):
            de['text'] = text
        return Result.create(Result.STATUS.ERROR, None, de, info)