# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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