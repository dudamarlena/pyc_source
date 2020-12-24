# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/mongomock_mate-project/mongomock_mate/patch_write_concern.py
# Compiled at: 2018-07-30 23:07:59
# Size of source mod 2**32: 495 bytes
"""
monkey patch ``mongomock.write_concern``
"""
from mongomock.write_concern import WriteConcern

def _write_concern_init(self, w=None, wtimeout=None, j=None, fsync=None):
    self.__document = {}
    self.acknowledged = True
    self.server_default = not self.document


@property
def _write_concern_document(self):
    return self.__document.copy()


WriteConcern.__init__ = _write_concern_init
WriteConcern.document = _write_concern_document