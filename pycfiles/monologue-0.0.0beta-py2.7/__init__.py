# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/monologue/__init__.py
# Compiled at: 2012-01-16 10:51:06
"""
For convenience, all standard debug level are importable from this module
"""
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from .core import get_logger, PROGRESS
import core