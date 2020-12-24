# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/nkoshelev/code/github/aio-space-track-api/aio_space_track_api/log.py
# Compiled at: 2017-05-26 04:33:51
# Size of source mod 2**32: 226 bytes
import logging
DEFAULT_LOG_FORMAT = '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s'
DEFAULT_LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logger = logging.getLogger('aio_space_track_api')