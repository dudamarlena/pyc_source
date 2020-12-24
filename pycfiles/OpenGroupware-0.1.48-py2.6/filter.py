# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/net/ossf/filter.py
# Compiled at: 2012-10-12 07:02:39
import logging
from coils.core import AnonymousContext

class OpenGroupwareServerSideFilter(object):

    def __init__(self, rfile, mimetype, parameters, log=None, ctx=None):
        self._rfile = rfile
        self._mimetype = mimetype
        for key in parameters:
            setattr(self, ('_{0}').format(key), parameters[key])
            print key, parameters[key]

        self._log = log
        self._ctx = ctx

    @property
    def log(self):
        if self._log is None:
            self._log = logging.getLogger('ossf')
        return self._log

    @property
    def ctx(self):
        if self._ctx is None:
            self._ctx = AnonymousContext()
        return self._ctx

    @property
    def handle(self):
        raise NotImplementedException('This OSSF is not implemented.')

    @property
    def mimetype(self):
        raise NotImplementedException('This OSSF is not implemented.')