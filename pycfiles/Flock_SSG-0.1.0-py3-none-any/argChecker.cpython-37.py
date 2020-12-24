# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\conne\Desktop\Flock_SSG-master\Flock\src\argChecker.py
# Compiled at: 2018-12-05 20:24:20
# Size of source mod 2**32: 1204 bytes
from . import settings
import Flock.src.docs.showDocs as UsageDocs
HELP_FLAG = '-help'
VERBOSE_FLAG = '-verbose'
IS_LOCAL_FLAG = '-local'

def parse(argv):
    RETURN_BOOL = False
    if len(argv) > 1:
        for arg in argv:
            if arg == HELP_FLAG:
                settings.LOG('-help called')
                UsageDocs.showDocs(1)
            elif arg == VERBOSE_FLAG:
                settings.LOG('-verbose called')
                RETURN_BOOL = True
            else:
                settings.LOG('Argument [ ' + arg + ' ] invalid!')

    return RETURN_BOOL