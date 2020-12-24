# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dyntftpd/handlers/clever.py
# Compiled at: 2015-04-16 06:00:42
import urllib
from . import TFTPUDPHandler
from .fs import FileSystemHandler, Session as FSSession
from .http import HTTPHandler, Session as HTTPSession

class CleverHandler(TFTPUDPHandler):

    def make_session(self, filename):
        maybe_url = urllib.unquote(filename)
        if maybe_url.startswith('http://') or maybe_url.startswith('https://'):
            return HTTPSession(self, filename)
        return FSSession(self, filename)