# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/__init__.py
# Compiled at: 2017-10-04 05:21:49
__author__ = 'Paul Ross'
__date__ = '2014-03-03'
__version__ = '0.9.7'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
__all__ = [
 'core', 'util', 'plot']
CPIP_VERSION = (0, 9, 7)
RELEASE_NOTES = [
 'Release Notes (latest at top).\n==============================\n2017-10-04: Version 0.9.7. Tested on Python 2.7 and 3.6.\n\n2017-10-03: Version 0.9.5, migrate to GitHub. Tested on Python 2.7 and 3.6.\n\n2014-09-03: Version 0.9.1, various minor fixes. Tested on Python 2.7 and 3.3.\n\n2014-01-11: Revisited SVG and HTML code to make it faster and cross browser.\n\n2012-03-26: Updated to Python 3.\n\n2011-07-10: First public release of CPIP.\n']

class ExceptionCpip(Exception):
    """Simple specialisation of an exception class for CPIP and its modules."""


INDENT_ML = True
SVG_COMMENT_FUNCTIONS = False