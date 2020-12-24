# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/py3compat.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 1280 bytes
"""
    Helper to support Python v2 and v3
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    Some ideas borrowed from six
    
    See also:
        http://python3porting.com
        https://bitbucket.org/gutworth/six/src/tip/six.py
        http://packages.python.org/six/
"""
from __future__ import division, absolute_import, print_function, unicode_literals
import sys, doctest, re
PY3 = sys.version_info[0] == 3
if PY3:
    TEXT_TYPE = str
    BINARY_TYPE = bytes
else:
    TEXT_TYPE = unicode
    BINARY_TYPE = str
    origin_OutputChecker = doctest.OutputChecker

    class OutputChecker2(origin_OutputChecker):

        def check_output(self, want, got, optionflags):
            got = got.replace("u'", "'").replace('u"', '"')
            return origin_OutputChecker.check_output(self, want, got, optionflags)


    doctest.OutputChecker = OutputChecker2

def repr2(obj):
    """
    Don't mark unicode strings with u in Python 2
    """
    if not PY3:
        return repr(obj).lstrip('u')
    return repr(obj)