# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/colortext/logger.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 2609 bytes
import sys, logging

def logger(name, lvl='info'):
    logging.basicConfig(format='[%(asctime)-19s]%(lineno)-6d:%(filename)s%(module)s:%(funcName)s: %(message)s', datefmt='%F.%T')
    return logging