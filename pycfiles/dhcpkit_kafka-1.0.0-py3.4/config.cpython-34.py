# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_kafka/server_extension/config.py
# Compiled at: 2016-12-08 10:51:43
# Size of source mod 2**32: 1316 bytes
"""
Configuration elements for the SOL_MAX_RT option handlers
"""
import string
from dhcpkit.ipv6.server.handlers import HandlerFactory
from dhcpkit_kafka.server_extension import KafkaHandler
topic_chars = string.ascii_letters + string.digits + '._-'
topic_max_length = 255

def topic_name(value: str) -> str:
    """
    Data validation for Kafka topic names.

    :param value: The value from the configuration file
    :return: The validated value
    """
    if value in ('', '.', '..'):
        raise ValueError("Topic name can not be empty, '.' or '..'")
    if len(value) > topic_max_length:
        raise ValueError('Topic name must be {} characters or less'.format(topic_max_length))
    if any([char not in topic_chars for char in value]):
        raise ValueError('Topic names may only contain {}'.format(topic_chars))
    return value


class KafkaHandlerFactory(HandlerFactory):
    __doc__ = '\n    Create the handler for the Kafka producer.\n    '

    def create(self) -> KafkaHandler:
        """
        Create a handler of this class based on the configuration in the config section.

        :return: A handler object
        """
        return KafkaHandler(source_address=self.source_address, brokers=self.brokers, topic_name=self.topic, server_name=self.server_name)