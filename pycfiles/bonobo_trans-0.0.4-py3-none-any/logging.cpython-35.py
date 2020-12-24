# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_sqlalchemy/logging.py
# Compiled at: 2018-07-15 06:26:26
# Size of source mod 2**32: 145 bytes
import logging, bonobo_sqlalchemy, mondrian
mondrian.setup(excepthook=True)
logger = logging.getLogger(bonobo_sqlalchemy.__name__)