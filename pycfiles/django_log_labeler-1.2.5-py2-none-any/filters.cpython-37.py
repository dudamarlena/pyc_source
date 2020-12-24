# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hermann/work/Vodacom-Django-Log-Labeler/log_labeler/filters.py
# Compiled at: 2020-03-24 05:56:10
# Size of source mod 2**32: 617 bytes
import logging
from django.conf import settings
from log_labeler import local, DEFAULT_HEADER_VALUE, LOG_LABEL_REQUEST_SETTING

class HeaderToLabelFilter(logging.Filter):

    def filter(self, record):
        if hasattr(settings, LOG_LABEL_REQUEST_SETTING):
            if isinstance(getattr(settings, LOG_LABEL_REQUEST_SETTING), dict):
                for label in getattr(settings, LOG_LABEL_REQUEST_SETTING):
                    header_value = getattr(local, label, DEFAULT_HEADER_VALUE)
                    setattr(record, label, header_value)

        return True