# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_log.py
# Compiled at: 2017-07-17 17:16:47
# Size of source mod 2**32: 619 bytes
import os
from pytrack_analysis.profile import get_profile
from pytrack_analysis.logger import Logger
if __name__ == '__main__':
    thisscript = os.path.basename(__file__).split('.')[0]
    PROFILE = get_profile('Vero eLife 2016', 'degoldschmidt', script=thisscript)
    log = Logger(PROFILE, scriptname=thisscript)
    log.close()
    log.show()