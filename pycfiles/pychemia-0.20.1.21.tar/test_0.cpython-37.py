# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gufranco/PyChemia/tests/test_0.py
# Compiled at: 2019-05-14 13:43:02
# Size of source mod 2**32: 216 bytes
__author__ = 'Guillermo Avendano-Franco'

def test_good():
    """
    Simple test import pychemia                                  :
    """
    from pychemia import pcm_log
    pcm_log.debug('DEBUGGING')