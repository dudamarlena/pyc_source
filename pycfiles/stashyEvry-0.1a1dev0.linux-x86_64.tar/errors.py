# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/e210990/bin/python26/lib/python2.6/site-packages/stashy/errors.py
# Compiled at: 2014-06-25 10:41:27
from functools import wraps
from decorator import decorator

class NotFoundException(Exception):

    def __init__(self, response):
        try:
            self.data = response.json()
            if 'errors' in self.data:
                msg = self.data['errors'][0]['message']
            else:
                msg = str(self.data)
        except ValueError:
            msg = 'Not found: ' + response.url

        super(NotFoundException, self).__init__(msg)


class GenericException(Exception):

    def __init__(self, response):
        try:
            self.data = response.json()
            msg = '%d: %s' % (response.status_code, self.data)
        except ValueError:
            msg = 'Unknown error: ' + response.status_code

        super(GenericException, self).__init__(msg)


def maybe_throw(response):
    if not response.ok:
        if response.status_code == 404:
            raise NotFoundException(response)
        else:
            e = GenericException(response)
            try:
                e.data = response.json()
            except ValueError:
                e.content = response.content
            else:
                raise e


@decorator
def ok_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.ok


@decorator
def response_or_error(fn, *args, **kw):
    response = fn(*args, **kw)
    maybe_throw(response)
    return response.json()