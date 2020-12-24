# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/colortext/logger.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 2609 bytes
import sys, logging

def logger(name, lvl='info'):
    logging.basicConfig(format='[%(asctime)-19s]%(lineno)-6d:%(filename)s%(module)s:%(funcName)s: %(message)s', datefmt='%F.%T')
    return logging