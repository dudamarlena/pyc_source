# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
    """NoHeaderErrorFilter"""

    def filter(self, record):
        """Filter out Header Parsing Errors."""
        return 'Failed to parse headers' not in record.getMessage()