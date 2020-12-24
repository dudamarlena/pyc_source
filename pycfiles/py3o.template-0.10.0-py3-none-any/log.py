# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/log.py
# Compiled at: 2014-10-15 11:33:17
__author__ = 'faide'
import logging
FORMAT = '%(asctime)-15s %(levelname)s %(module)s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)