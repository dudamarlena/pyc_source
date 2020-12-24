# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/exceptions.py
# Compiled at: 2018-08-15 14:24:35
# Size of source mod 2**32: 9171 bytes
"""
Author: Keith Bourgoin, Emmett Butler
"""
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'

class KafkaException(Exception):
    __doc__ = 'Generic exception type. The base of all pykafka exception types.'


class UnicodeException(Exception):
    __doc__ = 'Indicates that an error was encountered while processing a unicode string'


class NoBrokersAvailableError(KafkaException):
    __doc__ = "Indicates that no brokers were available to the cluster's metadata update attempts\n    "


class LeaderNotFoundError(KafkaException):
    __doc__ = 'Indicates that the leader broker for a given partition was not found during\n        an update in response to a MetadataRequest\n    '


class SocketDisconnectedError(KafkaException):
    __doc__ = 'Indicates that the socket connecting this client to a kafka broker has\n        become disconnected\n    '


class ProduceFailureError(KafkaException):
    __doc__ = 'Indicates a generic failure in the producer'


class ConsumerStoppedException(KafkaException):
    __doc__ = 'Indicates that the consumer was stopped when an operation was attempted that required it to be running'


class NoMessagesConsumedError(KafkaException):
    __doc__ = 'Indicates that no messages were returned from a MessageSet'


class MessageSetDecodeFailure(KafkaException):
    __doc__ = 'Indicates a generic failure in the decoding of a MessageSet from the broker'


class ProducerQueueFullError(KafkaException):
    __doc__ = "Indicates that one or more of the AsyncProducer's internal queues contain at least max_queued_messages messages"


class ProducerStoppedException(KafkaException):
    __doc__ = 'Raised when the Producer is used while not running'


class OffsetRequestFailedError(KafkaException):
    __doc__ = 'Indicates that OffsetRequests for offset resetting failed more times than the configured maximum'


class PartitionOwnedError(KafkaException):
    __doc__ = 'Indicates a given partition is still owned in Zookeeper.'

    def __init__(self, partition, *args, **kwargs):
        (super(PartitionOwnedError, self).__init__)(*args, **kwargs)
        self.partition = partition


class ProtocolClientError(KafkaException):
    __doc__ = 'Base class for protocol errors'
    ERROR_CODE = None


class UnknownError(ProtocolClientError):
    __doc__ = 'An unexpected server error'
    ERROR_CODE = -1


class OffsetOutOfRangeError(ProtocolClientError):
    __doc__ = 'The requested offset is outside the range of offsets maintained by the\n        server for the given topic/partition.\n    '
    ERROR_CODE = 1


class InvalidMessageError(ProtocolClientError):
    __doc__ = 'This indicates that a message contents does not match its CRC'
    ERROR_CODE = 2


class UnknownTopicOrPartition(ProtocolClientError):
    __doc__ = 'This request is for a topic or partition that does not exist on this\n        broker.\n    '
    ERROR_CODE = 3


class InvalidMessageSize(ProtocolClientError):
    __doc__ = 'The message has a negative size'
    ERROR_CODE = 4


class LeaderNotAvailable(ProtocolClientError):
    __doc__ = 'This error is thrown if we are in the middle of a leadership election\n        and there is currently no leader for this partition and hence it is\n        unavailable for writes.\n    '
    ERROR_CODE = 5


class NotLeaderForPartition(ProtocolClientError):
    __doc__ = "This error is thrown if the client attempts to send messages to a\n        replica that is not the leader for some partition. It indicates that\n        the client's metadata is out of date.\n    "
    ERROR_CODE = 6


class RequestTimedOut(ProtocolClientError):
    __doc__ = 'This error is thrown if the request exceeds the user-specified time\n        limit in the request.\n    '
    ERROR_CODE = 7


class MessageSizeTooLarge(ProtocolClientError):
    __doc__ = 'The server has a configurable maximum message size to avoid unbounded\n        memory allocation. This error is thrown if the client attempts to\n        produce a message larger than this maximum.\n    '
    ERROR_CODE = 10


class OffsetMetadataTooLarge(ProtocolClientError):
    __doc__ = 'If you specify a string larger than configured maximum for offset\n        metadata\n    '
    ERROR_CODE = 12


class GroupLoadInProgress(ProtocolClientError):
    __doc__ = 'The broker returns this error code for an offset fetch request if it is\n        still loading offsets (after a leader change for that offsets topic\n        partition), or in response to group membership requests (such as\n        heartbeats) when group metadata is being loaded by the coordinator.\n    '
    ERROR_CODE = 14


class GroupCoordinatorNotAvailable(ProtocolClientError):
    __doc__ = 'The broker returns this error code for consumer metadata requests or\n        offset commit requests if the offsets topic has not yet been created.\n    '
    ERROR_CODE = 15


class NotCoordinatorForGroup(ProtocolClientError):
    __doc__ = 'The broker returns this error code if it receives an offset fetch or\n        commit request for a consumer group that it is not a coordinator for.\n    '
    ERROR_CODE = 16


class InvalidTopic(ProtocolClientError):
    __doc__ = 'For a request which attempts to access an invalid topic (e.g. one which has\n        an illegal name), or if an attempt is made to write to an internal topic\n        (such as the consumer offsets topic).\n    '
    ERROR_CODE = 17


class IllegalGeneration(ProtocolClientError):
    __doc__ = 'Returned from group membership requests (such as heartbeats) when the generation\n        id provided in the request is not the current generation\n    '
    ERROR_CODE = 22


class InconsistentGroupProtocol(ProtocolClientError):
    __doc__ = 'Returned in join group when the member provides a protocol type or set of protocols\n        which is not compatible with the current group.\n    '
    ERROR_CODE = 23


class UnknownMemberId(ProtocolClientError):
    __doc__ = 'Returned from group requests (offset commits/fetches, heartbeats, etc) when the\n        memberId is not in the current generation. Also returned if SimpleConsumer is\n        incorrectly instantiated with a non-default consumer_id.\n    '
    ERROR_CODE = 25


class InvalidSessionTimeout(ProtocolClientError):
    __doc__ = 'Returned in join group when the requested session timeout is outside of the allowed\n        range on the broker\n    '
    ERROR_CODE = 26


class RebalanceInProgress(ProtocolClientError):
    __doc__ = 'Returned in heartbeat requests when the coordinator has begun rebalancing the\n        group. This indicates to the client that it should rejoin the group.\n    '
    ERROR_CODE = 27


class TopicAuthorizationFailed(ProtocolClientError):
    __doc__ = 'Returned by the broker when the client is not authorized to access the requested\n        topic.\n    '
    ERROR_CODE = 29


class GroupAuthorizationFailed(ProtocolClientError):
    __doc__ = 'Returned by the broker when the client is not authorized to access a particular\n    groupId.\n    '
    ERROR_CODE = 30


ERROR_CODES = dict((exc.ERROR_CODE, exc) for exc in (UnknownError,
 OffsetOutOfRangeError,
 InvalidMessageError,
 UnknownTopicOrPartition,
 InvalidMessageSize,
 LeaderNotAvailable,
 NotLeaderForPartition,
 RequestTimedOut,
 MessageSizeTooLarge,
 OffsetMetadataTooLarge,
 GroupLoadInProgress,
 GroupCoordinatorNotAvailable,
 NotCoordinatorForGroup,
 InvalidTopic,
 IllegalGeneration,
 InconsistentGroupProtocol,
 UnknownMemberId,
 InvalidSessionTimeout,
 RebalanceInProgress,
 TopicAuthorizationFailed,
 GroupAuthorizationFailed))

class RdKafkaException(KafkaException):
    __doc__ = "Error in rdkafka extension that hasn't any equivalent pykafka exception\n\n    In `pykafka.rdkafka._rd_kafka` we try hard to emit the same exceptions\n    that the pure pykafka classes emit.  This is a fallback for the few cases\n    where we can't find a suitable exception\n    "


class RdKafkaStoppedException(RdKafkaException):
    __doc__ = 'Consumer or producer handle was stopped\n\n    Raised by the C extension, to be translated to ConsumerStoppedException or\n    ProducerStoppedException by the caller\n    '