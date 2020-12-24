# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/tests/test_integrity.py
# Compiled at: 2017-07-25 11:36:22
# Size of source mod 2**32: 568 bytes
import os
from pytrack_analysis.profile import *
from pytrack_analysis.database import *
if __name__ == '__main__':
    thisscript = os.path.basename(__file__).split('.')[0]
    PROFILE = get_profile('Vero eLife 2016', 'degoldschmidt', script=thisscript)
    DB = Database(get_db(PROFILE))
    print('0003A01R01Cam03.avi is in:', DB.find('Videofilename=0003A01R01Cam03.avi'))
    this_session = DB.experiment('CANS').session('005')
    print(this_session.keys())