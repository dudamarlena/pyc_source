# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/mediatypes.py
# Compiled at: 2018-10-11 03:49:58
# Size of source mod 2**32: 2684 bytes
from __future__ import absolute_import, division, print_function, with_statement
from collections import namedtuple
from tornado import gen
ContentTypeT = namedtuple('ContentType', ['content_type', 'vendor',
 'version'])

def ContentType(content_type, vendor=None, version=None):
    if version:
        if not isinstance(version, float):
            raise AssertionError('Version must be a float')
    return ContentTypeT(content_type, vendor, version)


class MediaType(object):
    __doc__ = 'Collection of content types.'
    ApplicationJson = 'application/json'
    ApplicationJsonPatch = 'application/json-patch+json'
    TextHtml = 'text/html'


ReturnInformationT = namedtuple('ReturnInformation', ['code', 'message'])

def ReturnInformation(code, message=None):
    return ReturnInformationT(code, message=message)


class Return(gen.Return):
    pass


class Ok(Return):

    def __init__(self, code=200, additional=None):
        v = {'ok': True}
        if additional:
            assert isinstance(additional, dict), 'Additional messages must be of type dict'
            v.update(additional)
        super(Ok, self).__init__(ReturnInformation(code, message=v))


class OkCreated(Ok):

    def __init__(self, additional=None):
        super(OkCreated, self).__init__(201, additional=additional)


class NoContent(Return):

    def __init__(self):
        super(NoContent, self).__init__(ReturnInformation(204))


class Error(Return):

    def __init__(self, code=400, additional=None):
        v = {'error': True}
        if additional:
            assert isinstance(additional, dict), 'Additional messages must be of type dict'
            v.update(additional)
        super(Error, self).__init__(ReturnInformation(code, message=v))