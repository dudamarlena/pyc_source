# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/apydia/helpers.py
# Compiled at: 2007-12-01 06:26:29
"""
    Some helper functions used inside the templates
"""
from pprint import pformat

def is_included(pathname, options):
    """ Check if a pathname is to be included in the documentation """
    modules = options.modules
    exclude_modules = options.exclude_modules
    for m in exclude_modules:
        if pathname.startswith(m):
            return False

    if not [ True for m in modules if pathname.startswith(m) ]:
        return False
    return True


def safe_get(member, key):
    try:
        return member.get(key, None)
    except:
        return

    return