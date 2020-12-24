# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/menorah/confluence.py
# Compiled at: 2015-10-26 17:11:49
from riverpy import RiverViewClient
from riverstream import RiverStream
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

class Confluence(object):
    """
  A collection of River Streams from River View. This class will create data 
  streams across any number of River Streams, allowing you to stream them into
  a function or write all the data to CSV for swarming and running NuPIC models.
  """

    def __init__(self, dataIds, since=None, until=None, limit=None, debug=False):
        self._dataIds = dataIds
        self._since = since
        self._until = until
        self._limit = limit
        self._debug = debug
        self._streams = []

    def __iter__(self):
        return self

    def _createStreams(self):
        client = RiverViewClient(debug=self._debug)
        for dataId in self._dataIds:
            self._streams.append(RiverStream(client, dataId, since=self._since, until=self._until, limit=self._limit))

    def _loadData(self):
        [ stream.load() for stream in self._streams ]

    def load(self):
        self._createStreams()
        self._loadData()

    def resetStreams(self):
        [ stream.reset() for stream in self._streams ]

    def next(self):
        if self._isEmpty():
            raise StopIteration
        earliest = min([ stream.getTime() for stream in self._streams ])
        rowData = [ stream.advance(earliest) for stream in self._streams ]
        out = [earliest] + rowData
        return out

    def _isEmpty(self):
        smallest = min([ len(stream) for stream in self._streams ])
        return smallest is 0

    def createFieldDescriptions(self):
        return [ stream.createFieldDescription() for stream in self._streams ]

    def getStreamIds(self):
        return [ str(stream) for stream in self._streams ]

    def getDataTypes(self):
        return [ stream.getDataType() for stream in self._streams ]