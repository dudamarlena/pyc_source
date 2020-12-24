# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lerry/pytenpay/pytenpay/_private.py
# Compiled at: 2013-07-18 01:30:41
from os.path import join
from os import getcwd

class TENPAY:
    CERT = join(getcwd(), 'tenpay.pem')
    SP_ID = 1215995301
    SP_KEY = '0317e233a9b1b5836ed5c211cf80d15d'
    OP_USER = '1215995301'
    OP_PASSWORD = 'tenpaykanrss42qu'


if __name__ == '__main__':
    import sys
    if sys.getdefaultencoding() == 'ascii':
        reload(sys)
        sys.setdefaultencoding('utf-8')