# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kafka_python_with_confluent_kafka\kafka_producer.py
# Compiled at: 2018-10-31 04:33:03
# Size of source mod 2**32: 1650 bytes
import json, traceback
from confluent_kafka import Producer
from kafka_python_with_confluent_kafka.kafka_admin import KafkaAdmin

class KafkaProducer:

    def __init__(self, brokers):
        self.producer = None
        self.cache_topics = None
        self.brokers = brokers

    def produce(self, topic_name, push_data, create_topic=False):
        if create_topic:
            if self.cache_topics is None or len(self.cache_topics) is 0:
                self._update_cache_list()
            if topic_name not in self.cache_topics:
                client = KafkaAdmin(self.brokers)
                client.create_topic(topic_name)
                self._update_cache_list()
        if self.producer is None:
            self.producer = self._get_producer()
        self.producer.produce(topic_name, value=(str(json.dumps(push_data))))

    def flush(self):
        if self.producer:
            self.producer.flush()

    def _get_producer(self):
        config = {'bootstrap.servers': self.brokers}
        producer = Producer(config)
        return producer

    def _update_cache_list(self):
        client = KafkaAdmin()
        try:
            self.cache_topics = client.list_topic()
        except:
            self.cache_topics = None
            traceback.print_exc()