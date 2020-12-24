# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/pykafka/rdkafka/test_simple_consumer.py
# Compiled at: 2018-07-24 12:58:48
# Size of source mod 2**32: 2989 bytes
import pytest
from tests.pykafka import test_simpleconsumer, test_balancedconsumer
from pykafka.utils.compat import range
try:
    from pykafka.rdkafka import _rd_kafka
    RDKAFKA = True
except ImportError:
    RDKAFKA = False

@pytest.mark.skipif((not RDKAFKA), reason='rdkafka')
class TestRdKafkaSimpleConsumer(test_simpleconsumer.TestSimpleConsumer):
    USE_RDKAFKA = True

    def test_update_cluster(self):
        super(TestRdKafkaSimpleConsumer, self).test_update_cluster()

    def test_offset_commit_agrees(self):
        """Check rdkafka-obtained offsets arrive correctly

        In RdKafkaSimpleConsumer.consume we bypass most of the internals of
        simpleconsumer.OwnedPartition, but then expect it to still commit
        offsets for us correctly.  This warrants very explicit testing.
        """
        with self._get_simple_consumer(consumer_group='test_offset_commit_agrees') as (consumer):
            latest_offs = _latest_partition_offsets_by_reading(consumer, 100)
            consumer.commit_offsets()
            retrieved_offs = {r[0]:r[1].offset - 1 for r in consumer.fetch_offsets() if r[0] in latest_offs}
            self.assertEquals(retrieved_offs, latest_offs)

    def test_offset_resume_agrees(self):
        """Check the rdkafka consumer returns messages at specified offset

        Make sure reads from the underlying rdkafka consumer really do start
        at the offsets dictated by SimpleConsumer
        """
        with self._get_simple_consumer(consumer_group='test_offset_resume_agrees') as (consumer):
            latest_offs = _latest_partition_offsets_by_reading(consumer, 100)
            consumer.commit_offsets()
        with self._get_simple_consumer(consumer_group='test_offset_resume_agrees') as (consumer):
            while latest_offs:
                msg = consumer.consume()
                if msg.partition_id not in latest_offs:
                    pass
                else:
                    expected_offset = latest_offs[msg.partition_id] + 1
                    self.assertEquals(msg.offset, expected_offset)
                    del latest_offs[msg.partition_id]


def _latest_partition_offsets_by_reading(consumer, n_reads):
    """Obtain message offsets from consumer, return grouped by partition"""
    latest_offs = {}
    for _ in range(n_reads):
        msg = consumer.consume()
        latest_offs[msg.partition_id] = msg.offset

    return latest_offs


@pytest.mark.skipif((not RDKAFKA), reason='rdkafka')
class RdkBalancedConsumerIntegrationTests(test_balancedconsumer.BalancedConsumerIntegrationTests):
    USE_RDKAFKA = True