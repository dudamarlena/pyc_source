# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ssd/bscheers/github/gsm/gsm/db/qf.py
# Compiled at: 2018-01-17 15:38:38
import os.path, gsm

def queryfile(rel_qfile):
    p = os.path.abspath(os.path.dirname(gsm.__file__))
    return os.path.join(p, rel_qfile)