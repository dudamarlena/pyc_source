# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/xoc_utils/kafka/KProducer.py
# Compiled at: 2018-05-18 14:49:22
# Size of source mod 2**32: 1205 bytes
from confluent_kafka import Producer
from xoc_utils import Singleton

class KProducer(metaclass=Singleton):

    def __init__(self, server_origin, service_name):
        self.server_origin = server_origin
        self.service_name = service_name
        self.k_producer = Producer({'bootstrap.servers': server_origin})

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def delivery_callback(err, msg):
        """
            Callback function that is trigger when producer deliver the message to Kafka service.
        """
        if err:
            print('Message failed delivery: ' + err)
        else:
            print('Message delivered to ' + msg.topic())

    def produce(self, topic, data, callback=delivery_callback):
        """
            Produce a message by pushing the data to Kafka service.

            Arguments:
                topic <string> - Kafka topic.
                data <string> - the message data to push.
                callback <function> - callback function when message delivered.
        """
        self.k_producer.produce(topic, data, callback=callback)
        self.k_producer.flush()