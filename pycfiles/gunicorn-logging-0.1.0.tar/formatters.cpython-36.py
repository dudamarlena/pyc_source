# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/api/gunicorn-logging/gunicorn_logging/formatters.py
# Compiled at: 2018-06-19 06:26:04
# Size of source mod 2**32: 444 bytes
from . import settings
from pythonjsonlogger import jsonlogger

class GunicornJsonFormatter(jsonlogger.JsonFormatter):

    def add_fields(self, log_record, record, message_dict):
        super(GunicornJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['type'] = settings.LOGSTASH_MESSAGE_TYPE
        log_record['subtype'] = settings.LOGSTASH_MESSAGE_SUBTYPE
        log_record.update(settings.LOGSTASH_EXTRA)