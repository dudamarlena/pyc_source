# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wenlincms/core/exceptions.py
# Compiled at: 2015-06-18 06:25:30
from __future__ import unicode_literals

class FileSystemEncodingChanged(RuntimeError):

    def __init__(self):
        msg = b"Access was attempted on a file that contains unicode characters in its path, but somehow the current locale does not support utf-8. You may need to set 'LC_ALL' to a correct value, eg: 'en_US.UTF-8'."
        RuntimeError.__init__(self, msg)