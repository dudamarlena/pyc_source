# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/common.py
# Compiled at: 2018-07-19 17:44:23
# Size of source mod 2**32: 1632 bytes
"""
Author: Keith Bourgoin
"""
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['Message', 'CompressionType', 'OffsetType']
import datetime as dt, logging
log = logging.getLogger(__name__)
EPOCH = dt.datetime(1970, 1, 1)

class Message(object):
    __doc__ = 'Message class.\n\n    :ivar response_code: Response code from Kafka\n    :ivar topic: Originating topic\n    :ivar payload: Message payload\n    :ivar key: (optional) Message key\n    :ivar offset: Message offset\n    '
    __slots__ = []


class CompressionType(object):
    __doc__ = 'Enum for the various compressions supported.\n\n    :cvar NONE: Indicates no compression in use\n    :cvar GZIP: Indicates gzip compression in use\n    :cvar SNAPPY: Indicates snappy compression in use\n    '
    NONE = 0
    GZIP = 1
    SNAPPY = 2
    LZ4 = 3


class OffsetType(object):
    __doc__ = 'Enum for special values for earliest/latest offsets.\n\n    :cvar EARLIEST: Indicates the earliest offset available for a partition\n    :cvar LATEST: Indicates the latest offset available for a partition\n    '
    EARLIEST = -2
    LATEST = -1