# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/captcha/__init__.py
# Compiled at: 2019-07-28 08:45:30
VERSION = (0, 5, 12)

def get_version(svn=False):
    """Return the version as a human-format string."""
    return ('.').join([ str(i) for i in VERSION ])