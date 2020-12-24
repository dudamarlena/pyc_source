# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/logging_utilities/single_line_formatter.py
# Compiled at: 2019-03-13 06:22:26
# Size of source mod 2**32: 2361 bytes
import logging, socket
from datetime import datetime
import colorlog, pytz, tzlocal

class StandardMetadataFilter(logging.Filter):
    __doc__ = '\n    Filter that adds few more attributes to log records.\n\n    +-------------------+----------------------------------------------+\n    | placeholder       | description                                  |\n    +-------------------+----------------------------------------------+\n    | %(hostname)s      | hostname                                     |\n    +-------------------+----------------------------------------------+\n    | %(isotime)s       | Local time represented as ISO8601            |\n    +-------------------+----------------------------------------------+\n    | %(isotime_utc)s   | local time converted to UTC and represented  |\n    |                   | as ISO8601 string                            |\n    +-------------------+----------------------------------------------+\n    '
    try:
        _HOSTNAME = socket.gethostname()
    except Exception as exception:
        _HOSTNAME = '-'

    _LOCAL_TZ = tzlocal.get_localzone()

    def filter(self, record):
        dt = self._LOCAL_TZ.localize(datetime.fromtimestamp(record.created))
        record.isotime = dt.isoformat()
        record.isotime_utc = dt.astimezone(pytz.utc).isoformat()
        record.hostname = self._HOSTNAME
        return super(StandardMetadataFilter, self).filter(record)


class SingleLineFormatter(logging.Formatter):
    __doc__ = '\n    logging.Formatter that escapes all new lines forcing log record to be\n    logged as single line.\n    '

    def format(self, record):
        return super(SingleLineFormatter, self).format(record).replace('\n', '\\n')


class SingleLineColoredFormatter(colorlog.ColoredFormatter):
    __doc__ = '\n    logging.Formatter that escapes all new lines forcing log record to be\n    logged as single line but it also preserves colored log sequences.\n    '

    def format(self, record):
        return super(SingleLineColoredFormatter, self).format(record).replace('\n', '\\n')