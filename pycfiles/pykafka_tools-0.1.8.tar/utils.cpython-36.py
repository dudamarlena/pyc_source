# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/test/utils.py
# Compiled at: 2017-12-20 01:12:43
# Size of source mod 2**32: 1463 bytes
import time, os
from pykafka.test.kafka_instance import KafkaInstance, KafkaConnection

def get_cluster():
    """Gets a Kafka cluster for testing, using one already running is possible.

    An already-running cluster is determined by environment variables:
    BROKERS, ZOOKEEPER, KAFKA_BIN.  This is used primarily to speed up tests
    in our Travis-CI environment.
    """
    if os.environ.get('BROKERS', None):
        if os.environ.get('ZOOKEEPER', None):
            if os.environ.get('KAFKA_BIN', None):
                return KafkaConnection(os.environ['KAFKA_BIN'], os.environ['BROKERS'], os.environ['ZOOKEEPER'], os.environ.get('BROKERS_SSL', None))
    return KafkaInstance(num_instances=3)


def stop_cluster(cluster):
    """Stop a created cluster, or merely flush a pre-existing one."""
    if isinstance(cluster, KafkaInstance):
        cluster.terminate()
    else:
        cluster.flush()


def retry(assertion_callable, retry_time=10, wait_between_tries=0.1, exception_to_retry=AssertionError):
    """Retry assertion callable in a loop"""
    start = time.time()
    while True:
        try:
            return assertion_callable()
        except exception_to_retry as e:
            if time.time() - start >= retry_time:
                raise e
            time.sleep(wait_between_tries)