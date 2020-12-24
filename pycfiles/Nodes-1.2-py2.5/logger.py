# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/logger.py
# Compiled at: 2009-06-08 07:12:47
"""Node logger."""
import logging
defaultFormatter = logging.Formatter('%(module)-6s: %(name)-12s: %(levelname)-5s: %(message)s')
defaultHandler = logging.StreamHandler()
defaultHandler.setFormatter(defaultFormatter)
defaultHandler.setLevel(logging.INFO)

def enable():
    logging.getLogger('').addHandler(defaultHandler)


def filename(fname):
    fileHandler = logging.FileHandler(fname)
    fileHandler.setFormatter(defaultFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logging.getLogger('').addHandler(fileHandler)