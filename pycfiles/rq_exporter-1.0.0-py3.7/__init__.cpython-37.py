# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rq_exporter/__init__.py
# Compiled at: 2020-04-22 09:28:46
# Size of source mod 2**32: 386 bytes
"""
Python RQ Prometheus Exporter.

"""
import logging
logger = logging.getLogger(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
if gunicorn_logger.hasHandlers():
    logger.handlers = gunicorn_logger.handlers
    logger.setLevel(gunicorn_logger.level)
from .exporter import register_collector, create_app