# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/init.py
# Compiled at: 2020-04-23 12:05:14
# Size of source mod 2**32: 185 bytes
from hama.tagging.dict import Dict
from hama.tagging.hmm import TagHMM

def init(callback=None):
    Dict().load()
    TagHMM().load()
    if callback is not None:
        callback()