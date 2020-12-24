# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_docker/logging.py
# Compiled at: 2018-01-01 16:23:40
# Size of source mod 2**32: 137 bytes
import logging, bonobo_docker, mondrian
mondrian.setup(excepthook=True)
logger = logging.getLogger(bonobo_docker.__name__)