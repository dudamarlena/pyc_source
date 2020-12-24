# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/util/debug.py
# Compiled at: 2014-09-26 04:50:19
__doc__ = '\n\n  debug utils\n  ~~~~~~~~~~~\n\n  :author: Sam Gammon <sg@samgammon.com>\n  :copyright: (c) Sam Gammon, 2014\n  :license: This software makes use of the MIT Open Source License.\n            A copy of this license is included as ``LICENSE.md`` in\n            the root of the project.\n\n'
import sys
try:
    import logbook as logging
except ImportError:
    import logging
    logging.basicConfig(stream=sys.stdout, level=10, format='%(message)s')

def Logger(name):
    """  """
    logger = logging.getLogger(name)
    logger.setLevel(10)
    return logger