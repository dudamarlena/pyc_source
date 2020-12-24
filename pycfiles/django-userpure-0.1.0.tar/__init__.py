# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Abe/Dropbox/work/library/django-userpure/userpure/__init__.py
# Compiled at: 2013-03-05 02:17:30
VERSION = (0, 1, 0)
__version__ = ('.').join(str(each) for each in VERSION[:4])

def get_version():
    """
    Returns string with digit parts only as version.

    """
    return ('.').join(str(each) for each in VERSION[:3])