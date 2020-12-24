# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/pygenesis/utils.py
# Compiled at: 2019-11-19 13:31:58
# Size of source mod 2**32: 620 bytes
import logging

def filter_urllib3_logging():
    """Filter header errors from urllib3 due to a urllib3 bug."""
    urllib3_logger = logging.getLogger('urllib3.connectionpool')
    if not any((isinstance(x, NoHeaderErrorFilter) for x in urllib3_logger.filters)):
        urllib3_logger.addFilter(NoHeaderErrorFilter())


class NoHeaderErrorFilter(logging.Filter):
    __doc__ = 'Filter out urllib3 Header Parsing Errors due to a urllib3 bug.'

    def filter(self, record):
        """Filter out Header Parsing Errors."""
        return 'Failed to parse headers' not in record.getMessage()