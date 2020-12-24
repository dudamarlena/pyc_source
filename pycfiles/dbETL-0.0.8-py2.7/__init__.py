# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dbETL/__init__.py
# Compiled at: 2018-02-25 15:31:19
from .pyAPI import api
import sys

def main():
    ID, start, end = sys.argv[1:]
    print ID, start, end
    api(ID, start, end)


def preset():
    import os
    os.system('dbETL 2 1 50 & dbETL 3 1 50 & dbETL 8 1 50 & dbETL 9 1 50 &')