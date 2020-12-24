# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\b3\pkg_handler.py
# Compiled at: 2016-03-08 18:42:10
__author__ = 'ThorN'
__version__ = '1.4'
import os, sys
from b3.functions import main_is_frozen
__all__ = [
 'resource_directory']

def resource_directory(module):
    """
    Use this if pkg_resources is NOT installed
    """
    return os.path.dirname(sys.modules[module].__file__)


if not main_is_frozen():
    try:
        import pkg_resources
    except ImportError:
        pkg_resources = None
    else:

        def resource_directory_from_pkg_resources(module):
            """
            Use this if pkg_resources is installed
            """
            return pkg_resources.resource_filename(module, '')


        resource_directory = resource_directory_from_pkg_resources