# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hugo/.virtualenvs/gitinspector/lib/python2.7/site-packages/gitinspector/version.py
# Compiled at: 2015-08-05 12:31:15
from __future__ import print_function
from __future__ import unicode_literals
try:
    import localization
    localization.init()
except:
    import gitinspector.localization
    gitinspector.localization.init()

__version__ = b'0.3.2'
__doc__ = _(b'Copyright © 2012-2014 Ejwa Software. All rights reserved.\nLicense GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>.\nThis is free software: you are free to change and redistribute it.\nThere is NO WARRANTY, to the extent permitted by law.\n\nWritten by Adam Waldenberg.')

def output():
    print((b'gitinspector {0}\n').format(__version__) + __doc__)