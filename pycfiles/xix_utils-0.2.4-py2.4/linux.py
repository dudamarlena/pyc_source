# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/linux.py
# Compiled at: 2007-01-21 20:27:15
"""
Linux-only hodge-podge utilities.

Copyright (c) 2005 Drew Smathers
See LICENSE for details.

$Id: linux.py 399 2007-01-22 01:27:13Z djfroofy $

"""
import sys
from xix.utils.comp.interface import implements
from xix.utils import console
from xix.utils.python import setAll
_islinux = sys.platform == 'linux-i386' or sys.platform == 'linux2'
if _islinux:

    def changeXtermTitle(title):
        sys.stdout.write('%c%c]2;%s%c' % (7, 27, title, 7))


else:

    def changeXtermTitle(title):
        pass


__all__ = [
 'changeXtermTitle']