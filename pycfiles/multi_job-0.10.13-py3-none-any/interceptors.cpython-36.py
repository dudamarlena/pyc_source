# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/interface/interceptors.py
# Compiled at: 2020-02-19 11:45:10
# Size of source mod 2**32: 268 bytes
from docopt import docopt
from art import text2art

def intercept(interface: str) -> dict:
    prefix = text2art('Multi job')
    prefix += 'Jobs:\n'
    prefix += 'Routines:\n'
    prefix += 'Options:\n'
    print(prefix)
    return docopt(interface)