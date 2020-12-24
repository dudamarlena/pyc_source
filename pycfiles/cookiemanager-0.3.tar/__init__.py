# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/orpheus/Development/cookieman/cookieman/resources/__init__.py
# Compiled at: 2019-12-21 08:06:38
__doc__ = 'Cookieman resources.'
try:
    import importlib.resources as res
except ImportError:
    import importlib_resources as res

def read_text(resource_name):
    """
    Get resource content by name.

    :param resource_name: name of resource to load
    :returns: decoded resource content
    """
    return res.read_text(__name__, resource_name)