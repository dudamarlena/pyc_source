# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/termine/genericlogger.py
# Compiled at: 2012-07-17 05:28:56
import logging, sys
logger = logging.getLogger('gwiseLogger')
logger.setLevel(logging.ERROR)
ch = logging.StreamHandler(sys.__stdout__)
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)