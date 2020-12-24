# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kafka_python_with_confluent_kafka\kafka_admin.py
# Compiled at: 2018-10-31 04:32:02
# Size of source mod 2**32: 4597 bytes
import re, traceback
from confluent_kafka.admin import AdminClient, NewTopic, NewPartitions
from kafka.client import SimpleClient
from kafka.consumer import KafkaConsumer
from kafka.common import OffsetRequestPayload, TopicPartition

class KafkaAdmin:

    def __init__(self, brokers):
        self.brokers = brokers
        self.broker_list = self.brokers.split(',')

    def list_topic(self):
        list = []
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)
        for t in iter(md.topics.values()):
            list.append(str(t))

        return list

    def find_topics_by_regex(self, regex):
        topic_names = []
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)
        for t in iter(md.topics.values()):
            if re.search(regex, str(t)) is not None:
                topic_names.append(str(t))

        print('topics: [%s]' % ', '.join(map(str, topic_names)))
        return topic_names

    def delete_topic(self, topic_name):
        admin_client = self._get_admin_client()
        fs = admin_client.delete_topics([topic_name], operation_timeout=30)
        for topic, f in fs.items():
            try:
                f.result()
                print('Topic {} deleted'.format(topic))
            except Exception as e:
                print('Failed to delete topic {}: {}'.format(topic, e))

    def get_group_lag(self, topic, group):
        lag = -1
        try:
            topic_offset = self.get_topic_offset(topic)
            group_offset = self._get_group_offset(group, topic)
            lag = topic_offset - group_offset
        except:
            print("Can't get sum of lag in topic({}) with group({})".format(topic, group))

        if lag >= 0:
            return lag
        else:
            return -1

    def create_topic(self, topic, number_partition=1):
        admin_client = self._get_admin_client()
        if self.is_topic_exist(topic):
            self._create_partitions(topic, number_partition)
        else:
            new_topic = [
             NewTopic(topic, num_partitions=(int(number_partition)), replication_factor=1)]
            fs = admin_client.create_topics(new_topic)
            for topic, f in fs.items():
                try:
                    f.result()
                    print('Topic {} created'.format(topic))
                except Exception as e:
                    print('Failed to create topic {}: {}'.format(topic, e))

    def is_topic_exist(self, topic_name):
        admin_client = self._get_admin_client()
        md = admin_client.list_topics(timeout=10)
        for t in iter(md.topics.values()):
            if str(t) == topic_name:
                return True

        return False

    def _create_partitions(self, topic, new_partition):
        admin_client = self._get_admin_client()
        new_part = [
         NewPartitions(topic, int(new_partition))]
        fs = admin_client.create_partitions(new_part, validate_only=False)
        for topic, f in fs.items():
            try:
                f.result()
                print('Set partitions({}) to topic {}'.format(str(new_partition), topic))
            except Exception as e:
                print('Failed to set partitions({}) to topic {}: {}'.format(str(new_partition), topic, e))

    def _get_admin_client(self):
        admin_config = {'bootstrap.servers': self.brokers}
        admin_client = AdminClient(admin_config)
        return admin_client

    def get_topic_offset(self, topic):
        client = SimpleClient(self.broker_list)
        partitions = client.topic_partitions[topic]
        offset_requests = [OffsetRequestPayload(topic, p, -1, 1) for p in partitions.keys()]
        offsets_responses = client.send_offset_request(offset_requests)
        return sum([r.offsets[0] for r in offsets_responses])

    def _get_group_offset(self, group_id, topic):
        consumer = KafkaConsumer(bootstrap_servers=(self.broker_list), group_id=group_id)
        pts = [TopicPartition(topic=topic, partition=i) for i in consumer.partitions_for_topic(topic)]
        result = consumer._coordinator.fetch_committed_offsets(pts)
        return sum([r.offset for r in result.values()])