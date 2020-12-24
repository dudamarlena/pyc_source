# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/log.py
# Compiled at: 2014-10-15 11:33:17
__author__ = 'faide'
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(module)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)