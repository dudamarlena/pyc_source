# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/holmium/core/logger.py
# Compiled at: 2016-02-28 21:16:09
"""
global logger
"""
import logging
log = logging.Logger('holmium.core')
log.setLevel(logging.INFO)
_shandler = logging.StreamHandler()
_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(_format)
_shandler.setFormatter(formatter)
log.addHandler(_shandler)