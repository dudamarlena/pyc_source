# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ross/github/octodns/tests/helpers.py
# Compiled at: 2020-01-15 20:00:35
from __future__ import absolute_import, division, print_function, unicode_literals
from shutil import rmtree
from tempfile import mkdtemp

class SimpleSource(object):

    def __init__(self, id=b'test'):
        pass


class SimpleProvider(object):
    SUPPORTS_GEO = False
    SUPPORTS_DYNAMIC = False
    SUPPORTS = set(('A', ))
    id = b'test'

    def __init__(self, id=b'test'):
        pass

    def populate(self, zone, source=False, lenient=False):
        pass

    def supports(self, record):
        return True

    def __repr__(self):
        return self.__class__.__name__


class GeoProvider(object):
    SUPPORTS_GEO = True
    SUPPORTS_DYNAMIC = False
    id = b'test'

    def __init__(self, id=b'test'):
        pass

    def populate(self, zone, source=False, lenient=False):
        pass

    def supports(self, record):
        return True

    def __repr__(self):
        return self.__class__.__name__


class DynamicProvider(object):
    SUPPORTS_GEO = False
    SUPPORTS_DYNAMIC = True
    id = b'test'

    def __init__(self, id=b'test'):
        pass

    def populate(self, zone, source=False, lenient=False):
        pass

    def supports(self, record):
        return True

    def __repr__(self):
        return self.__class__.__name__


class NoSshFpProvider(SimpleProvider):

    def supports(self, record):
        return record._type != b'SSHFP'


class TemporaryDirectory(object):

    def __init__(self, delete_on_exit=True):
        self.delete_on_exit = delete_on_exit

    def __enter__(self):
        self.dirname = mkdtemp()
        return self

    def __exit__(self, *args, **kwargs):
        if self.delete_on_exit:
            rmtree(self.dirname)
        else:
            raise Exception(self.dirname)