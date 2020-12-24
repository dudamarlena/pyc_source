# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/exceptions.py
# Compiled at: 2018-08-15 14:24:35
# Size of source mod 2**32: 9171 bytes
__doc__ = '\nAuthor: Keith Bourgoin, Emmett Butler\n'
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'

class KafkaException(Exception):
    """KafkaException"""
    pass


class UnicodeException(Exception):
    """UnicodeException"""
    pass


class NoBrokersAvailableError(KafkaException):
    """NoBrokersAvailableError"""
    pass


class LeaderNotFoundError(KafkaException):
    """LeaderNotFoundError"""
    pass


class SocketDisconnectedError(KafkaException):
    """SocketDisconnectedError"""
    pass


class ProduceFailureError(KafkaException):
    """ProduceFailureError"""
    pass


class ConsumerStoppedException(KafkaException):
    """ConsumerStoppedException"""
    pass


class NoMessagesConsumedError(KafkaException):
    """NoMessagesConsumedError"""
    pass


class MessageSetDecodeFailure(KafkaException):
    """MessageSetDecodeFailure"""
    pass


class ProducerQueueFullError(KafkaException):
    """ProducerQueueFullError"""
    pass


class ProducerStoppedException(KafkaException):
    """ProducerStoppedException"""
    pass


class OffsetRequestFailedError(KafkaException):
    """OffsetRequestFailedError"""
    pass


class PartitionOwnedError(KafkaException):
    """PartitionOwnedError"""

    def __init__(self, partition, *args, **kwargs):
        (super(PartitionOwnedError, self).__init__)(*args, **kwargs)
        self.partition = partition


class ProtocolClientError(KafkaException):
    """ProtocolClientError"""
    ERROR_CODE = None


class UnknownError(ProtocolClientError):
    """UnknownError"""
    ERROR_CODE = -1


class OffsetOutOfRangeError(ProtocolClientError):
    """OffsetOutOfRangeError"""
    ERROR_CODE = 1


class InvalidMessageError(ProtocolClientError):
    """InvalidMessageError"""
    ERROR_CODE = 2


class UnknownTopicOrPartition(ProtocolClientError):
    """UnknownTopicOrPartition"""
    ERROR_CODE = 3


class InvalidMessageSize(ProtocolClientError):
    """InvalidMessageSize"""
    ERROR_CODE = 4


class LeaderNotAvailable(ProtocolClientError):
    """LeaderNotAvailable"""
    ERROR_CODE = 5


class NotLeaderForPartition(ProtocolClientError):
    """NotLeaderForPartition"""
    ERROR_CODE = 6


class RequestTimedOut(ProtocolClientError):
    """RequestTimedOut"""
    ERROR_CODE = 7


class MessageSizeTooLarge(ProtocolClientError):
    """MessageSizeTooLarge"""
    ERROR_CODE = 10


class OffsetMetadataTooLarge(ProtocolClientError):
    """OffsetMetadataTooLarge"""
    ERROR_CODE = 12


class GroupLoadInProgress(ProtocolClientError):
    """GroupLoadInProgress"""
    ERROR_CODE = 14


class GroupCoordinatorNotAvailable(ProtocolClientError):
    """GroupCoordinatorNotAvailable"""
    ERROR_CODE = 15


class NotCoordinatorForGroup(ProtocolClientError):
    """NotCoordinatorForGroup"""
    ERROR_CODE = 16


class InvalidTopic(ProtocolClientError):
    """InvalidTopic"""
    ERROR_CODE = 17


class IllegalGeneration(ProtocolClientError):
    """IllegalGeneration"""
    ERROR_CODE = 22


class InconsistentGroupProtocol(ProtocolClientError):
    """InconsistentGroupProtocol"""
    ERROR_CODE = 23


class UnknownMemberId(ProtocolClientError):
    """UnknownMemberId"""
    ERROR_CODE = 25


class InvalidSessionTimeout(ProtocolClientError):
    """InvalidSessionTimeout"""
    ERROR_CODE = 26


class RebalanceInProgress(ProtocolClientError):
    """RebalanceInProgress"""
    ERROR_CODE = 27


class TopicAuthorizationFailed(ProtocolClientError):
    """TopicAuthorizationFailed"""
    ERROR_CODE = 29


class GroupAuthorizationFailed(ProtocolClientError):
    """GroupAuthorizationFailed"""
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
    """RdKafkaException"""
    pass


class RdKafkaStoppedException(RdKafkaException):
    """RdKafkaStoppedException"""
    pass