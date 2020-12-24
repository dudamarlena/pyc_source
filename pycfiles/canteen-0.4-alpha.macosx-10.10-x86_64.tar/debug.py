# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/canteen/util/debug.py
# Compiled at: 2014-09-26 04:50:19
"""

  debug utils
  ~~~~~~~~~~~

  :author: Sam Gammon <sg@samgammon.com>
  :copyright: (c) Sam Gammon, 2014
  :license: This software makes use of the MIT Open Source License.
            A copy of this license is included as ``LICENSE.md`` in
            the root of the project.

"""
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