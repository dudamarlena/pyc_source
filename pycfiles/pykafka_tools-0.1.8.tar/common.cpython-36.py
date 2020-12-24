# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/common.py
# Compiled at: 2018-07-19 17:44:23
# Size of source mod 2**32: 1632 bytes
__doc__ = '\nAuthor: Keith Bourgoin\n'
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['Message', 'CompressionType', 'OffsetType']
import datetime as dt, logging
log = logging.getLogger(__name__)
EPOCH = dt.datetime(1970, 1, 1)

class Message(object):
    """Message"""
    __slots__ = []


class CompressionType(object):
    """CompressionType"""
    NONE = 0
    GZIP = 1
    SNAPPY = 2
    LZ4 = 3


class OffsetType(object):
    """OffsetType"""
    EARLIEST = -2
    LATEST = -1