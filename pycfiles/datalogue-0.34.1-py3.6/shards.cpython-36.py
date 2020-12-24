# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/kinesis/shards.py
# Compiled at: 2020-05-07 16:37:14
# Size of source mod 2**32: 8137 bytes
import datetime
from abc import ABC, abstractmethod
from typing import List, Union
from datalogue.errors import DtlError
from datalogue.dtl_utils import _parse_string_list

class ShardIterator(ABC):
    __doc__ = '\n    Abstract class containing the five subclasses:\n      TrimHorizon, for beginning at the beginning of the stream\n      Latest, for beginning at the most recent record\n      AtTimestamp, for beginning at a specified time\n      AtSequenceNumber, for beginning at a specified sequence number\n      AfterSequenceNumber, for beginning just after a specified sequence number\n    '
    type_field = 'type'
    type_str = ''

    def __init__(self, type):
        self.type = type
        super().__init__()

    def _base_payload(self) -> dict:
        base = [(ShardIterator.type_field, self.type_str)]
        return dict(base)

    @abstractmethod
    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object
        :return:
        """
        pass

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'ShardIterator')]:
        type_field = d.get(ShardIterator.type_field)
        if not isinstance(type_field, str):
            return DtlError('The type is missing from JSON')
        if type_field == TrimHorizon.type_str:
            return TrimHorizon()
        if type_field == Latest.type_str:
            return Latest()
        if type_field == AtSequenceNumber.type_str:
            return AtSequenceNumber._from_payload(d)
        if type_field == AfterSequenceNumber.type_str:
            return AfterSequenceNumber._from_payload(d)
        else:
            if type_field == AtTimestamp.type_str:
                return AtTimestamp._from_payload(d)
            return DtlError('The object %s is not a ShardIterator definition' % str(d))


class TrimHorizon(ShardIterator):
    __doc__ = '\n      Begins reading stream from the beginning\n    '
    type_str = 'TrimHorizon'

    def __init__(self):
        super().__init__(TrimHorizon.type_str)

    def __repr__(self):
        return (f"{self.__class__.__name__}")

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        return base


class Latest(ShardIterator):
    __doc__ = '\n      Begins reading stream from the beginning\n    '
    type_str = 'Latest'

    def __init__(self):
        super().__init__(Latest.type_str)

    def __repr__(self):
        return (f"{self.__class__.__name__}")

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        return base


class AtSequenceNumber(ShardIterator):
    __doc__ = '\n      Begins reading stream starting from element of specified sequence number\n    '
    type_str = 'AtSequenceNumber'

    def __init__(self, sequence_number):
        self.sequence_number = sequence_number
        super().__init__(AtSequenceNumber.type_str)

    def __repr__(self):
        return f"{self.__class__.__name__}(sequence_number: {self.sequence_number})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['sequenceNumber'] = self.sequence_number
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'AtSequenceNumber')]:
        sequence_number = d.get('sequenceNumber')
        if sequence_number is None:
            return DtlError('The `sequenceNumber` is missing from JSON')
        else:
            return AtSequenceNumber(sequence_number)


class AfterSequenceNumber(ShardIterator):
    __doc__ = '\n      Begins reading stream starting immediately after element of specified sequence number\n    '
    type_str = 'AfterSequenceNumber'

    def __init__(self, sequence_number):
        self.sequence_number = sequence_number
        super().__init__(AfterSequenceNumber.type_str)

    def __repr__(self):
        return f"{self.__class__.__name__}(sequence_number: {self.sequence_number})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['sequenceNumber'] = self.sequence_number
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'AfterSequenceNumber')]:
        sequence_number = d.get('sequenceNumber')
        if sequence_number is None:
            return DtlError('The `sequenceNumber` is missing from JSON')
        else:
            return AfterSequenceNumber(sequence_number)


class AtTimestamp(ShardIterator):
    __doc__ = '\n      Begins reading stream from specified timestamp\n    '
    type_str = 'AtTimestamp'

    def __init__(self, timestamp):
        self.timestamp = timestamp
        super().__init__(AtTimestamp.type_str)

    def __repr__(self):
        return f"{self.__class__.__name__}(timestamp: {self.timestamp})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        base = self._base_payload()
        base['timestamp'] = self.timestamp
        return base

    @staticmethod
    def _from_payload(d: dict) -> Union[(DtlError, 'AtTimestamp')]:
        timestamp = d.get('timestamp')
        if timestamp is None:
            return DtlError('The `timestamp` is missing from JSON')
        else:
            timestamp = datetime.datetime.fromtimestamp(timestamp, tz=(datetime.timezone.utc))
            if not isinstance(timestamp, datetime.datetime):
                return DtlError('The `timestamp` parsed from JSON is not a datetime format.')
            return AtTimestamp(timestamp)


class ShardAttributes(object):
    __doc__ = '\n    Configures the shard attributes for the streaming source\n    :param partition_keys can be used to specify to read from a specific partition key or partition keys. If unspecified, reads from all partition keys (consequently, all shards) of the stream\n    :param shard_iterator: iterator type used for this source, as a subclass of ShardIterator\n    :param refresh_interval: time between requests for data loads, in milliseconds\n    :param limit: maximum number of transactions ingested from stream per second (for Kinesis, max supported is 5 and each transaction can contain 10k records)\n    '

    def __init__(self, partition_keys: List[str]=[], shard_iterator: ShardIterator=TrimHorizon(), refresh_interval: float=1, limit: int=5):
        if len(partition_keys) == 0:
            if isinstance(shard_iterator, AtSequenceNumber) or isinstance(shard_iterator, AfterSequenceNumber):
                raise DtlError('Please input the shard_id of the shard referenced by the specified sequence_number')
        self.partition_keys = partition_keys
        self.shard_iterator = shard_iterator
        self.refresh_interval = refresh_interval
        self.limit = limit

    def __repr__(self):
        return f"{self.__class__.__name__}(partition_keys: {self.partition_keys}, shard_iterator: {self.shard_iterator}, refresh_interval: {self.refresh_interval}, limit: {self.limit})"

    def _as_payload(self) -> dict:
        """
        Dictionary representation of the object with camelCase keys
        :return:
        """
        json = {}
        json['partitionKeys'] = self.partition_keys
        json['shardIterator'] = self.shard_iterator._as_payload()
        json['refreshInterval'] = self.refresh_interval
        json['limit'] = self.limit
        return json

    @staticmethod
    def _from_payload(shard_attributes: dict) -> Union[(DtlError, 'ShardAttributes')]:
        partition_keys = _parse_string_list(shard_attributes['partitionKeys'])
        shard_iterator = ShardIterator._from_payload(shard_attributes['shardIterator'])
        refresh_interval = shard_attributes['refreshInterval']
        limit = shard_attributes['limit']
        return ShardAttributes(partition_keys, shard_iterator, refresh_interval, limit)