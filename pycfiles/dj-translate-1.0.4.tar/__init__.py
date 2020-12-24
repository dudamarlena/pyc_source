# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dadasu/demo/django/dj-translate/autotranslate/__init__.py
# Compiled at: 2016-10-06 05:50:14
VERSION = (1, 0, 4)

def get_version(svn=False, limit=3):
    """Return the version as a human-format string."""
    return ('.').join([ str(i) for i in VERSION[:limit] ])