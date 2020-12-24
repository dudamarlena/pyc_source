# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\python362\Lib\site-packages\novainstrumentation\tictac.py
# Compiled at: 2017-03-06 22:19:14
# Size of source mod 2**32: 581 bytes
import time

def tic():
    """@brief Saves the current time.
    @see also tac()
    """
    global _tic
    _tic = time.time()


def tac(label=''):
    """@brief This function prints in the screen the difference between
    the time saved with function tic.py and current time.

    @param label String: if something is desired to print (default = '').

    @see also tic()
    """
    delta_t = time.time() - _tic
    if label != '':
        print('%s - %3.4f s' % (label, delta_t))
    else:
        print('%3.4f s' % delta_t)