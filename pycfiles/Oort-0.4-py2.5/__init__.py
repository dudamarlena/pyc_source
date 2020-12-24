# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/__init__.py
# Compiled at: 2007-10-06 12:03:02
"""
The Oort core package.
"""
__docformat__ = 'reStructuredText en'
__author__ = 'Niklas Lindström'
__version__ = '0.4'
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)