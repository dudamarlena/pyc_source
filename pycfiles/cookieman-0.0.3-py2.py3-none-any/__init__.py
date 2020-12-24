# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/orpheus/Development/cookieman/cookieman/resources/__init__.py
# Compiled at: 2019-12-21 08:06:38
"""Cookieman resources."""
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