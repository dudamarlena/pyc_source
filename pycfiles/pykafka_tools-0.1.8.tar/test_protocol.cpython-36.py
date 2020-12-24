# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pykafka/test_protocol.py
# Compiled at: 2018-07-24 18:54:49
# Size of source mod 2**32: 73102 bytes
import operator, unittest2
from pykafka import protocol
from pykafka.common import CompressionType
from pykafka.membershipprotocol import RangeProtocol
from pykafka.utils.compat import buffer

class TestMetadataAPI(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequest()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00\x15\x00\x03\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x00\x00\x00'))

    def test_response(self):
        cluster = protocol.MetadataResponse(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])

    def test_partition_error(self):
        response = protocol.MetadataResponse(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x02\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(response.topics['test'].partitions[0].err, 3)

    def test_topic_error(self):
        response = protocol.MetadataResponse(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\x00\x00\x00\x01\x00\x03\x00\x04test\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(response.topics['test'].err, 3)


class TestMetadataAPIV1(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequestV1()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x15\x00\x03\x00\x01\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff'))

    def test_response(self):
        cluster = protocol.MetadataResponseV1(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.brokers[0].rack, None)
        self.assertEqual(cluster.controller_id, 0)
        self.assertEqual(cluster.topics['test'].is_internal, False)


class TestMetadataAPIV2(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequestV2()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x15\x00\x03\x00\x02\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff'))

    def test_response(self):
        cluster = protocol.MetadataResponseV2(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\xff\xff\x00\x01a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.brokers[0].rack, None)
        self.assertEqual(cluster.controller_id, 0)
        self.assertEqual(cluster.cluster_id, 'a')
        self.assertEqual(cluster.topics['test'].is_internal, False)


class TestMetadataAPIV3(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequestV3()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x15\x00\x03\x00\x03\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff'))

    def test_response(self):
        cluster = protocol.MetadataResponseV3(buffer(b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\xff\xff\x00\x01a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.brokers[0].rack, None)
        self.assertEqual(cluster.throttle_time_ms, 0)
        self.assertEqual(cluster.controller_id, 0)
        self.assertEqual(cluster.cluster_id, 'a')
        self.assertEqual(cluster.topics['test'].is_internal, False)


class TestMetadataAPIV4(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequestV4()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x16\x00\x03\x00\x04\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff\x01'))

    def test_response(self):
        cluster = protocol.MetadataResponseV4(buffer(b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\xff\xff\x00\x01a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.brokers[0].rack, None)
        self.assertEqual(cluster.throttle_time_ms, 0)
        self.assertEqual(cluster.controller_id, 0)
        self.assertEqual(cluster.cluster_id, 'a')
        self.assertEqual(cluster.topics['test'].is_internal, False)


class TestMetadataAPIV5(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        req = protocol.MetadataRequestV5()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x16\x00\x03\x00\x05\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff\x01'))

    def test_response(self):
        cluster = protocol.MetadataResponseV5(buffer(b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\tlocalhost\x00\x00#\x84\xff\xff\x00\x01a\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x04test\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(cluster.brokers[0].host, 'localhost')
        self.assertEqual(cluster.brokers[0].port, 9092)
        self.assertEqual(cluster.topics['test'].partitions[0].leader, cluster.brokers[0].id)
        self.assertEqual(cluster.topics['test'].partitions[0].replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].isr, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.topics['test'].partitions[0].offline_replicas, [
         cluster.brokers[0].id])
        self.assertEqual(cluster.brokers[0].rack, None)
        self.assertEqual(cluster.throttle_time_ms, 0)
        self.assertEqual(cluster.controller_id, 0)
        self.assertEqual(cluster.cluster_id, 'a')
        self.assertEqual(cluster.topics['test'].is_internal, False)


class TestProduceAPI(unittest2.TestCase):
    maxDiff = None
    test_messages = [
     protocol.Message('this is a test message', partition_key='asdf'),
     protocol.Message('this is a test message', partition_key='asdf', timestamp=1497302164,
       protocol_version=1),
     protocol.Message('this is also a test message', partition_key='test_key'),
     protocol.Message("this doesn't have a partition key")]

    def test_request(self):
        message = self.test_messages[0]
        req = protocol.ProduceRequest()
        req.add_message(message, 'test', 0)
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b"\x00\x00\x00a\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x01\x00\x00'\x10\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x004\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00(\x0e\x8a\x19O\x00\x00\x00\x00\x00\x04asdf\x00\x00\x00\x16this is a test message"))

    def test_request_message_timestamp(self):
        message = self.test_messages[1]
        req = protocol.ProduceRequest()
        req.add_message(message, 'test', 0)
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b"\x00\x00\x00i\x00\x00\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x01\x00\x00'\x10\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00<\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x000Z\x92\x80\t\x01\x00\x00\x00\x00\x00Y?\x04\x94\x00\x00\x00\x04asdf\x00\x00\x00\x16this is a test message"))

    def test_gzip_compression(self):
        req = protocol.ProduceRequest(compression_type=(CompressionType.GZIP))
        [req.add_message(m, 'test_gzip', 0) for m in self.test_messages]
        msg = req.get_bytes()
        self.assertEqual(len(msg), 230)

    def test_snappy_compression(self):
        req = protocol.ProduceRequest(compression_type=(CompressionType.SNAPPY))
        [req.add_message(m, 'test_snappy', 0) for m in self.test_messages]
        msg = req.get_bytes()
        self.assertEqual(len(msg), 240)

    def test_partition_error(self):
        response = protocol.ProduceResponse(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(response.topics['test'][0].err, 3)

    def test_response(self):
        response = protocol.ProduceResponse(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(response.topics, {'test': {0: protocol.ProducePartitionResponse(0, 2)}})


class _FetchAPITestBase(object):
    maxDiff = None

    def msg_to_dict(self, msg):
        """Helper to extract data from Message slots"""
        attr_names = protocol.Message.__slots__
        f = (operator.attrgetter)(*attr_names)
        return dict(zip(attr_names, f(msg)))


class TestFetchAPI(unittest2.TestCase, _FetchAPITestBase):

    def _get_expected(self):
        return [
         {'partition_key':'asdf', 
          'compression_type':0, 
          'value':'this is a test message', 
          'offset':0, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':0, 
          'protocol_version':0, 
          'partition':None},
         {'partition_key':'test_key', 
          'compression_type':0, 
          'value':'this is also a test message', 
          'offset':1, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':0, 
          'protocol_version':0, 
          'partition':None},
         {'partition_key':None, 
          'compression_type':0, 
          'value':"this doesn't have a partition key", 
          'offset':2, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':0, 
          'protocol_version':0, 
          'partition':None}]

    def test_request(self):
        preq = protocol.PartitionFetchRequest('test', 0, 1)
        req = protocol.FetchRequest(partition_requests=[preq])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00;\x00\x01\x00\x00\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff\x00\x00\x03\xe8\x00\x00\x04\x00\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x10\x00\x00'))

    def test_partition_error(self):
        response = protocol.FetchResponse(buffer(b'\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x006\xa3 ^B\x00\x00\x00\x00\x00\x12test_partition_key\x00\x00\x00\x16this is a test message'))
        self.assertEqual(response.topics['test'][0].err, 3)

    def test_response(self):
        resp = protocol.FetchResponse(buffer(b'\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x006\xa3 ^B\x00\x00\x00\x00\x00\x12test_partition_key\x00\x00\x00\x16this is a test message'))
        self.assertEqual(len(resp.topics['test'][0].messages), 1)
        self.assertEqual(resp.topics['test'][0].max_offset, 2)
        message = resp.topics['test'][0].messages[0]
        self.assertEqual(message.value, 'this is a test message')
        self.assertEqual(message.partition_key, 'test_partition_key')
        self.assertEqual(message.compression_type, 0)
        self.assertEqual(message.offset, 1)

    def test_gzip_decompression(self):
        msg = ''.join([
         b'\x00\x00\x00\x01\x00\ttest_gzip\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\xad\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\xa1S\x82\x9d\xff\x00\x01\xff\xff\xff\xff\x00\x00\x00\x93\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x03\r\xbe.I\x7f0\x8b%\xb18%\rH\x8b\x95dd\x16+\x00Q\xa2BIjq\x89Bnjqqbz*T=#\x10\x1b\xb2\xf3\xcb\xf4\x81y\x1c \x15\xf1\xd9\xa9\x95@\xb64\\_Nq>v\xcdL@\xac\x7f\xb5(\xd9\x98\x81\xe1?\x10\x00y\x8a`M)\xf9\xa9\xc5y\xea%\n\x19\x89e\xa9@\x9d\x05\x89E%\x99%\x99\xf9y\n\x10\x93A\x80\x19\x88\xcd/\x9a<1\xc5\xb0\x97h#X\xc8\xb0\x1d\x00Bj\t\\*\x01\x00\x00\x00\x00\x00\x00'])
        response = protocol.FetchResponse(msg)
        expected_data = self._get_expected()
        for i in range(len(expected_data)):
            self.assertDictEqual(self.msg_to_dict(response.topics['test_gzip'][0].messages[i]), expected_data[i])

    def test_snappy_decompression(self):
        msg = ''.join([
         b'\x00\x00\x00\x01\x00\x0btest_snappy\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\xb5\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\xa9\xc1\xf2\xa3\xe1\x00\x02\xff\xff\xff\xff\x00\x00\x00\x9b\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x87\xac\x01\x00\x00\x19\x01\x10(\x0e\x8a\x19O\x05\x0fx\x04asdf\x00\x00\x00\x16this is a test message\x05$(\x00\x00\x01\x00\x00\x001\x07\x0f\x1c\x8e\x05\x10\x00\x08\x01"\x1c_key\x00\x00\x00\x1b\x158\x08lsoV=\x00H\x02\x00\x00\x00/\xd5rc3\x00\x00\xff\xff\xff\xff\x00\x00\x00!\x055ldoesn\'t have a partition key'])
        response = protocol.FetchResponse(msg)
        expected_data = self._get_expected()
        for i in range(len(expected_data)):
            self.assertDictEqual(self.msg_to_dict(response.topics['test_snappy'][0].messages[i]), expected_data[i])


class TestFetchAPIV1(unittest2.TestCase, _FetchAPITestBase):
    RESPONSE_CLASS = protocol.FetchResponseV1

    def _get_expected(self):
        return [
         {'partition_key':'asdf', 
          'compression_type':0, 
          'value':'this is a test message', 
          'offset':0, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':1497393304998, 
          'protocol_version':1, 
          'partition':None},
         {'partition_key':'test_key', 
          'compression_type':0, 
          'value':'this is also a test message', 
          'offset':1, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':1497393305005, 
          'protocol_version':1, 
          'partition':None},
         {'partition_key':None, 
          'compression_type':0, 
          'value':"this doesn't have a partition key", 
          'offset':2, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':1497393305013, 
          'protocol_version':1, 
          'partition':None},
         {'partition_key':'test_key', 
          'compression_type':0, 
          'value':'this has a partition key and a timestamp', 
          'offset':3, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':1497302164, 
          'protocol_version':1, 
          'partition':None},
         {'partition_key':None, 
          'compression_type':0, 
          'value':'this has a timestamp', 
          'offset':4, 
          'partition_id':0, 
          'produce_attempt':0, 
          'delivery_report_q':None, 
          'timestamp':1497302164, 
          'protocol_version':1, 
          'partition':None}]

    def test_partition_error(self):
        response = self.RESPONSE_CLASS(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x006\xa3 ^B\x00\x00\x00\x00\x00\x12test_partition_key\x00\x00\x00\x16this is a test message'))
        self.assertEqual(response.topics['test'][0].err, 3)

    def test_response(self):
        resp = self.RESPONSE_CLASS(buffer(b'\x00\x00\x00\x01\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x006\xa3 ^B\x00\x00\x00\x00\x00\x12test_partition_key\x00\x00\x00\x16this is a test message'))
        self.assertEqual(resp.throttle_time, 1)
        self.assertEqual(len(resp.topics['test'][0].messages), 1)
        self.assertEqual(resp.topics['test'][0].max_offset, 2)
        message = resp.topics['test'][0].messages[0]
        self.assertEqual(message.value, 'this is a test message')
        self.assertEqual(message.partition_key, 'test_partition_key')
        self.assertEqual(message.compression_type, 0)
        self.assertEqual(message.offset, 1)

    def test_gzip_decompression(self):
        msg = ''.join([
         b'\x00\x00\x00\x00\x00\x00\x00\x01\x00\x0btest_gzip_5\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x02\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Z\xb1Z\xf4\xc3\x01\x01\x00\x00\x01\\\xa3\x98\x95\xa6\xff\xff\xff\xff\x00\x00\x00D\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x03\x03\x97?.{\x19\x81\x0c\xc6\x98\xc53\xa6.\x032X\x12\x8bS\xd2\x80\xb4XIFf\xb1\x02\x10%*\x94\xa4\x16\x97(\xe4\xa6\x16\x17\'\xa6\xa7\x02\x00N\xddm\x92<\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00`\xcdX\t\xed\x01\x01\x00\x00\x01\\\xa3\x98\x95\xad\xff\xff\xff\xff\x00\x00\x00J\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x03\xcb%\xf2\x01\x99\x8c@\x06c\xcc\xe2\x19S\xd7\x02\x19\x1c%\xa9\xc5%\xf1\xd9\xa9\x95@\xb6tIFf\xb1\x02\x10%\xe6\x14\xe7+$*\x80\xa4\x14rS\x8b\x8b\x13\xd3S\x01\xfe<~BE\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00b\xba\xb0lN\x01\x01\x00\x00\x01\\\xa3\x98\x95\xb5\xff\xff\xff\xff\x00\x00\x00L\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x03s\xfb\xad2\x07\x19\x81\x0c\xc6\x98\xc53\xa6n\xfd\x0f\x04@\x8ebIFf\xb1BJ~jq\x9ez\x89BFbY\xaaB\xa2BAbQIfIf~\x9eBvj%\x00\xc8f?\xe3C\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00l\x9f\xd7)\xa0\x01\x01\x00\x00\x00\x00Y?\x04\x94\xff\xff\xff\xff\x00\x00\x00V\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x037\x86wK\x8f0\x82\x99\x91\xf6,S\x80\x14GIjqI|vj%\x90\xadQ\x92\x91Y\xac\x90\x91X\xac\x90\xa8P\x90XT\x92Y\x92\x99\x9f\xa7\x00\x94SH\xccK\x01\x8a\x95d\xe6\x02\x15\'\xe6\x16\x00\x00\xac\xc0O.R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00S\xd8"\xff7\x01\x01\x00\x00\x00\x00Y?\x04\x94\xff\xff\xff\xff\x00\x00\x00=\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00c`\x80\x03\xad\x0f\xae\x97^2\x82\x99\x91\xf6,S\xfe\x03\x01\x90)R\x92\x91Y\xac\x90\x91X\xac\x90\xa8P\x92\x99\x9bZ\\\x92\x98[\x00\x00\x83\x0f\xe5\xc16\x00\x00\x00\x00\x00\x00\x00'])
        response = self.RESPONSE_CLASS(msg)
        expected_data = self._get_expected()
        for i in range(len(expected_data)):
            self.assertDictEqual(self.msg_to_dict(response.topics['test_gzip_5'][0].messages[i]), expected_data[i])

    def test_snappy_decompression(self):
        msg = ''.join([
         b"\x00\x00\x00\x00\x00\x00\x00\x01\x00\x0btest_snappy\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x02=\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00a\xaa\x92\x19\xe2\x01\x02\x00\x00\x01\\\xa3\xa5\xab/\xff\xff\xff\xff\x00\x00\x00K\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x007<\x00\x00\x19\x01\xc00\x86\xf55\x85\x01\x00\x00\x00\x01\\\xa3\xa5\xab/\x00\x00\x00\x04asdf\x00\x00\x00\x16this is a test message\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00jI\xfc\xe7\xf6\x01\x02\x00\x00\x01\\\xa3\xa5\xab\xa1\xff\xff\xff\xff\x00\x00\x00T\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00@E\x00\x00\x19\x01\xe49\xd4\r\xf8v\x01\x00\x00\x00\x01\\\xa3\xa5\xab\xa1\x00\x00\x00\x08test_key\x00\x00\x00\x1bthis is also a test message\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00h\x80\t0\x95\x01\x02\x00\x00\x01\\\xa3\xa5\xab\xe1\xff\xff\xff\xff\x00\x00\x00R\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00>C\x00\x00\x19\x01\xdc72\x98C\xe8\x01\x00\x00\x00\x01\\\xa3\xa5\xab\xe1\xff\xff\xff\xff\x00\x00\x00!this doesn't have a partition key\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00uJ\xab\xd0\xdf\x01\x02\x00\x00\x00\x00Y?\x04\x94\xff\xff\xff\xff\x00\x00\x00_\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00KR\x00\x00\x19\x01\x14F\x00\xee\xa5\xc4\x01\x05\x10\xecY?\x04\x94\x00\x00\x00\x08test_key\x00\x00\x00(this has a partition key and a timestamp\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00Y\xfb!\x15\xce\x01\x02\x00\x00\x00\x00Y?\x04\x94\xff\xff\xff\xff\x00\x00\x00C\x82SNAPPY\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00/6\x00\x00\x19\x01\x14*\xf0E\xd2\xe9\x01\x05\x10|Y?\x04\x94\xff\xff\xff\xff\x00\x00\x00\x14this has a timestamp\x00\x00\x00\x00"])
        response = self.RESPONSE_CLASS(msg)
        expected_data = self._get_expected()
        for i in range(len(expected_data)):
            returned = self.msg_to_dict(response.topics['test_snappy'][0].messages[i])
            expected = expected_data[i]
            if i <= 2:
                returned.pop('timestamp')
                expected.pop('timestamp')
            self.assertDictEqual(returned, expected)


class TestFetchAPIV2(TestFetchAPIV1):
    RESPONSE_CLASS = protocol.FetchResponseV2


class TestListOffsetAPI(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        preq = protocol.PartitionOffsetRequest('test', 0, -1, 1)
        req = protocol.ListOffsetRequest(partition_requests=[preq])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x003\x00\x02\x00\x00\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff\x00\x00\x00\x01'))

    def test_partition_error(self):
        response = protocol.ListOffsetResponse(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(response.topics['test'][0].err, 3)

    def test_response(self):
        resp = protocol.ListOffsetResponse(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(resp.topics['test'][0].offset, [2])


class TestListOffsetAPIV1(unittest2.TestCase):
    maxDiff = None

    def test_request(self):
        preq = protocol.PartitionOffsetRequest('test', 0, -1, 1)
        req = protocol.ListOffsetRequestV1(partition_requests=[preq])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00/\x00\x02\x00\x01\x00\x00\x00\x00\x00\x07pykafka\xff\xff\xff\xff\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\xff\xff\xff\xff\xff\xff\xff\xff'))

    def test_partition_error(self):
        response = protocol.ListOffsetResponseV1(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(response.topics['test'][0].err, 3)

    def test_response(self):
        resp = protocol.ListOffsetResponseV1(buffer('\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x02'))
        self.assertEqual(resp.topics['test'][0].offset, [2])
        self.assertEqual(resp.topics['test'][0].timestamp, 2)


class TestOffsetCommitFetchAPI(unittest2.TestCase):
    maxDiff = None

    def test_consumer_metadata_request(self):
        req = protocol.GroupCoordinatorRequest('test')
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00\x17\x00\n\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x04test'))

    def test_consumer_metadata_response(self):
        response = protocol.GroupCoordinatorResponse(buffer(b'\x00\x00\x00\x00\x00\x00\x00\remmett-debian\x00\x00#\x84'))
        self.assertEqual(response.coordinator_id, 0)
        self.assertEqual(response.coordinator_host, 'emmett-debian')
        self.assertEqual(response.coordinator_port, 9092)

    def test_offset_commit_request(self):
        preq = protocol.PartitionOffsetCommitRequest('test', 0, 68, 1426632066, 'testmetadata')
        req = protocol.OffsetCommitRequest('test',
          1, 'pykafka', partition_requests=[preq])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00T\x00\x08\x00\x01\x00\x00\x00\x00\x00\x07pykafka\x00\x04test\x00\x00\x00\x01\x00\x07pykafka\x00\x00\x00\x01\x00\x04test\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00D\x00\x00\x00\x00U\x08\xad\x82\x00\x0ctestmetadata'))

    def test_offset_commit_response(self):
        response = protocol.OffsetCommitResponse(buffer('\x00\x00\x00\x01\x00\x0cemmett.dummy\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'))
        self.assertEqual(response.topics['emmett.dummy'][0].err, 0)

    def test_offset_fetch_request(self):
        preq = protocol.PartitionOffsetFetchRequest('testtopic', 0)
        req = protocol.OffsetFetchRequest('test', partition_requests=[preq])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00.\x00\t\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x04test\x00\x00\x00\x01\x00\ttesttopic\x00\x00\x00\x01\x00\x00\x00\x00'))

    def test_offset_fetch_response(self):
        response = protocol.OffsetFetchResponse(buffer('\x00\x00\x00\x01\x00\x0cemmett.dummy\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00'))
        self.assertEqual(response.topics['emmett.dummy'][0].metadata, '')
        self.assertEqual(response.topics['emmett.dummy'][0].offset, 1)


class TestOffsetCommitFetchAPIV2(unittest2.TestCase):
    maxDiff = None

    def test_offset_fetch_request(self):
        req = protocol.OffsetFetchRequestV2('test', partition_requests=[])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\x1b\x00\t\x00\x02\x00\x00\x00\x00\x00\x07pykafka\x00\x04test\xff\xff\xff\xff'))

    def test_offset_fetch_response(self):
        response = protocol.OffsetFetchResponseV2(buffer('\x00\x00\x00\x01\x00\x0cemmett.dummy\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00'))
        self.assertEqual(response.topics['emmett.dummy'][0].metadata, '')
        self.assertEqual(response.topics['emmett.dummy'][0].offset, 1)
        self.assertEqual(response.err, 0)


class TestGroupMembershipAPI(unittest2.TestCase):
    maxDiff = None

    def test_consumer_group_protocol_metadata(self):
        meta = protocol.ConsumerGroupProtocolMetadata()
        msg = meta.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00\x00\x00\x01\x00\ndummytopic\x00\x00\x00\x0ctestuserdata'))

    def test_join_group_request(self):
        topic_name = 'abcdefghij'
        membership_protocol = RangeProtocol
        membership_protocol.metadata.topic_names = [topic_name]
        req = protocol.JoinGroupRequest('dummygroup', 'testmember', topic_name, membership_protocol)
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00h\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\ndummygroup\x00\x00u0\x00\ntestmember\x00\x08consumer\x00\x00\x00\x01\x00\x05range\x00\x00\x00"\x00\x00\x00\x00\x00\x01\x00\nabcdefghij\x00\x00\x00\x0ctestuserdata'))

    def test_join_group_response(self):
        response = protocol.JoinGroupResponse(bytearray('\x00\x00\x00\x00\x00\x01\x00\x17dummyassignmentstrategy\x00,pykafka-b2361322-674c-4e26-9194-305962636e57\x00,pykafka-b2361322-674c-4e26-9194-305962636e57\x00\x00\x00\x01\x00,pykafka-b2361322-674c-4e26-9194-305962636e57\x00\x00\x00"\x00\x00\x00\x00\x00\x01\x00\ndummytopic\x00\x00\x00\x0ctestuserdata\x00\x00\x00\x00'))
        self.assertEqual(response.generation_id, 1)
        self.assertEqual(response.group_protocol, 'dummyassignmentstrategy')
        member_id = 'pykafka-b2361322-674c-4e26-9194-305962636e57'
        self.assertEqual(response.leader_id, member_id)
        self.assertEqual(response.member_id, member_id)
        self.assertTrue(member_id in response.members)
        metadata = response.members[member_id]
        self.assertEqual(metadata.version, 0)
        self.assertEqual(metadata.topic_names, ['dummytopic'])
        self.assertEqual(metadata.user_data, 'testuserdata')

    def test_member_assignment_construction(self):
        assignment = protocol.MemberAssignment([('mytopic1', [3, 5, 7, 9]),
         (
          'mytopic2', [2, 4, 6, 8])])
        msg = assignment.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x01\x00\x00\x00\x02\x00\x08mytopic1\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\t\x00\x08mytopic2\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x06\x00\x00\x00\x08'))

    def test_sync_group_request(self):
        req = protocol.SyncGroupRequest('dummygroup', 1, 'testmember1', [
         (
          'a',
          protocol.MemberAssignment([('mytopic1', [3, 5, 7, 9]),
           (
            'mytopic2', [3, 5, 7, 9])])),
         (
          'b',
          protocol.MemberAssignment([('mytopic1', [2, 4, 6, 8]),
           (
            'mytopic2', [2, 4, 6, 8])]))])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray(b'\x00\x00\x00\xc4\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\ndummygroup\x00\x00\x00\x01\x00\x0btestmember1\x00\x00\x00\x02\x00\x01a\x00\x00\x00B\x00\x01\x00\x00\x00\x02\x00\x08mytopic1\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\t\x00\x08mytopic2\x00\x00\x00\x04\x00\x00\x00\x03\x00\x00\x00\x05\x00\x00\x00\x07\x00\x00\x00\t\x00\x01b\x00\x00\x00B\x00\x01\x00\x00\x00\x02\x00\x08mytopic1\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x06\x00\x00\x00\x08\x00\x08mytopic2\x00\x00\x00\x04\x00\x00\x00\x02\x00\x00\x00\x04\x00\x00\x00\x06\x00\x00\x00\x08'))

    def test_sync_group_response(self):
        response = protocol.SyncGroupResponse(bytearray('\x00\x00\x00\x00\x00H\x00\x01\x00\x00\x00\x01\x00\x14testtopic_replicated\x00\x00\x00\n\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x08\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00\x05,pyk'))
        self.assertEqual(response.error_code, 0)
        expected_assignment = [('testtopic_replicated', [6, 7, 8, 9, 0, 1, 2, 3, 4, 5])]
        self.assertEqual(response.member_assignment.partition_assignment, expected_assignment)

    def test_heartbeat_request(self):
        req = protocol.HeartbeatRequest('dummygroup', 1, 'testmember')
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00-\x00\x0c\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\ndummygroup\x00\x00\x00\x01\x00\ntestmember'))

    def test_heartbeat_response(self):
        response = protocol.HeartbeatResponse(bytearray('\x00\x00'))
        self.assertEqual(response.error_code, 0)

    def test_leave_group_request(self):
        req = protocol.LeaveGroupRequest('dummygroup', 'testmember')
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00)\x00\r\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\ndummygroup\x00\ntestmember'))

    def test_leave_group_response(self):
        response = protocol.LeaveGroupResponse(bytearray('\x00\x00'))
        self.assertEqual(response.error_code, 0)


class TestAdministrativeAPI(unittest2.TestCase):
    maxDiff = None

    def test_list_groups_request(self):
        req = protocol.ListGroupsRequest()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00\x11\x00\x10\x00\x00\x00\x00\x00\x00\x00\x07pykafka'))

    def test_list_groups_response(self):
        response = protocol.ListGroupsResponse(bytearray('\x00\x00\x00\x00\x00\x01\x00\ttestgroup\x00\x08consumer'))
        self.assertEqual(len(response.groups), 1)
        group = response.groups['testgroup']
        self.assertEqual(group.group_id, 'testgroup')
        self.assertEqual(group.protocol_type, 'consumer')

    def test_describe_groups_request(self):
        req = protocol.DescribeGroupsRequest(['testgroup'])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00 \x00\x0f\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x00\x00\x01\x00\ttestgroup'))

    def test_describe_groups_response(self):
        response = protocol.DescribeGroupsResponse(bytearray('\x00\x00\x00\x01\x00\x00\x00\ttestgroup\x00\x06Stable\x00\x08consumer\x00\x05range\x00\x00\x00\x01\x00,pykafka-d42426fb-c295-4cd9-b585-6dd79daf3afe\x00\x07pykafka\x00\n/127.0.0.1\x00\x00\x00"\x00\x00\x00\x00\x00\x01\x00\ndummytopic\x00\x00\x00\x0ctestuserdata\x00\x00\x00H\x00\x01\x00\x00\x00\x01\x00\x14testtopic_replicated\x00\x00\x00\n\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x08\x00\x00\x00\x03\x00\x00\x00\t\x00\x00\x00\x04\x00\x00\x00\x05\x00\x00\x00\x06\x00\x00\x00\x07\x00\x00\x00\x00'))
        self.assertTrue('testgroup' in response.groups)
        group_response = response.groups['testgroup']
        self.assertEqual(group_response.error_code, 0)
        self.assertEqual(group_response.group_id, 'testgroup')
        self.assertEqual(group_response.state, 'Stable')
        self.assertEqual(group_response.protocol_type, 'consumer')
        self.assertEqual(group_response.protocol, 'range')
        member_id = 'pykafka-d42426fb-c295-4cd9-b585-6dd79daf3afe'
        self.assertTrue(member_id in group_response.members)
        member = group_response.members[member_id]
        self.assertEqual(member.member_id, member_id)
        self.assertEqual(member.client_id, 'pykafka')
        self.assertEqual(member.client_host, '/127.0.0.1')
        metadata = member.member_metadata
        self.assertEqual(metadata.version, 0)
        self.assertEqual(metadata.topic_names, ['dummytopic'])
        self.assertEqual(metadata.user_data, 'testuserdata')
        assignment = member.member_assignment
        self.assertEqual(assignment.version, 1)
        self.assertEqual(assignment.partition_assignment, [
         (
          'testtopic_replicated', [0, 1, 2, 8, 3, 9, 4, 5, 6, 7])])

    def test_create_topics_request(self):
        req = protocol.CreateTopicsRequest([
         protocol.CreateTopicRequest('mycooltopic', 4, 2, [], [])])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x004\x00\x13\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x00\x00\x01\x00\x0bmycooltopic\x00\x00\x00\x04\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'))

    def test_create_topics_response(self):
        response = protocol.CreateTopicsResponse(bytearray('\x00\x00\x00\x01\x00\ttesttopic\x00\x00'))

    def test_delete_topics_request(self):
        req = protocol.DeleteTopicsRequest(['mycooltopic'])
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00&\x00\x14\x00\x00\x00\x00\x00\x00\x00\x07pykafka\x00\x00\x00\x01\x00\x0bmycooltopic\x00\x00\x00\x00'))

    def test_delete_topics_response(self):
        response = protocol.DeleteTopicsResponse(bytearray('\x00\x00\x00\x01\x00\ttesttopic\x00\x00'))

    def test_api_versions_request(self):
        req = protocol.ApiVersionsRequest()
        msg = req.get_bytes()
        self.assertEqual(msg, bytearray('\x00\x00\x00\x11\x00\x12\x00\x00\x00\x00\x00\x00\x00\x07pykafka'))

    def test_api_versions_response(self):
        response = protocol.ApiVersionsResponse(bytearray('\x00\x00\x00\x00\x00\x15\x00\x00\x00\x00\x00\x02\x00\x01\x00\x00\x00\x03\x00\x02\x00\x00\x00\x01\x00\x03\x00\x00\x00\x02\x00\x04\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x06\x00\x00\x00\x02\x00\x07\x00\x01\x00\x01\x00\x08\x00\x00\x00\x02\x00\t\x00\x00\x00\x01\x00\n\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x01\x00\x0c\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x13\x00\x00\x00\x00\x00\x14\x00\x00\x00\x00\x00\x00\x00\x00'))
        self.assertEqual(len(response.api_versions), 21)
        self.assertEqual(response.api_versions[1].max, 3)
        self.assertEqual(response.api_versions[5].min, 0)
        self.assertEqual(response.api_versions[12].key, 12)


if __name__ == '__main__':
    unittest2.main()