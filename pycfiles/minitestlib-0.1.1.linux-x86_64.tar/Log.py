# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/minitestlib/Log.py
# Compiled at: 2009-01-13 10:19:58
"""
Logging module
"""
__author__ = 'Andy Shevchenko <andy.shevchenko@gmail.com>'
__revision__ = '$Id$'
__all__ = [
 'logger']
import logging, sys

def get():
    """ Setup stream based logger """
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s', '%b %d %H:%M:%S')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    log = logging.getLogger('org.teleca.minitestlib')
    log.addHandler(handler)
    log.setLevel(logging.WARNING)
    return log


logger = get()