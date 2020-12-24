# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomislav/dev/seveno_pyutil/build/lib/seveno_pyutil/logging_utilities/standard_metadata_filter.py
# Compiled at: 2019-01-17 13:53:03
# Size of source mod 2**32: 1695 bytes
import logging, socket
from datetime import datetime
import pytz, tzlocal

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