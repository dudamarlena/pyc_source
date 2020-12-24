# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_docker/logging.py
# Compiled at: 2018-01-01 16:23:40
# Size of source mod 2**32: 137 bytes
import logging, bonobo_docker, mondrian
mondrian.setup(excepthook=True)
logger = logging.getLogger(bonobo_docker.__name__)