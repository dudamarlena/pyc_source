# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/tests/dummy.py
# Compiled at: 2008-10-23 05:55:15
"""
Stubs for testing
$Id: dummy.py 61129 2008-03-25 16:00:44Z glenfant $
"""
from ZPublisher.HTTPRequest import FileUpload as BaseFileUpload

class FileUpload(BaseFileUpload):
    """Dummy upload object.

    Used to fake uploaded files and images.
    """
    __module__ = __name__
    __allow_access_to_unprotected_subobjects__ = 1
    filename = 'dummy.gif'
    headers = {}

    def __init__(self, filename=None, headers=None, file=None):
        self.file = file
        if filename is not None:
            self.filename = filename
        if headers is not None:
            self.headers = headers
        return

    def seek(self, *args):
        return self.file.seek(*args)

    def tell(self, *args):
        return self.file.tell(*args)

    def read(self, *args):
        return self.file.read(*args)