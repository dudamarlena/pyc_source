# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paicli/utils.py
# Compiled at: 2019-07-22 01:15:24
# Size of source mod 2**32: 389 bytes
import logging
logger = logging.getLogger(__name__)

def to_str(inp):
    _type = type(inp)
    try:
        unicode
        inp = inp.decode('utf-8')
    except NameError:
        try:
            inp = str(inp, 'utf-8')
        except TypeError:
            pass

    logger.debug('Casted "{}" from {} to {}'.format(inp, _type, type(inp)))
    return inp