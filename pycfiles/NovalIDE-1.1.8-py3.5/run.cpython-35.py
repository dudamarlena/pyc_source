# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/run.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 435 bytes
from noval.launcher import run
import noval.model as model

def main():
    run(model.LANGUAGE_DEFAULT)