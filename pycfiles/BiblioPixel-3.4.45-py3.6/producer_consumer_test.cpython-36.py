# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/threads/producer_consumer_test.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 987 bytes
import random, threading, time, unittest
from bibliopixel.util.threads import producer_consumer

class ProducerConsumerTest(unittest.TestCase):

    def test_all(self):
        buffer = producer_consumer.Queues([], [])
        counter = [
         0]

        def producer():
            for i in range(10):
                time.sleep(random.uniform(0.001, 0.02))
                with buffer.produce() as (i):
                    i[:] = counter
                    counter[0] += 1

        producer_thread = threading.Thread(target=producer)
        result = []

        def consumer():
            for i in range(10):
                time.sleep(random.uniform(0.003, 0.01))
                with buffer.consume() as (o):
                    result.extend(o)

        consumer_thread = threading.Thread(target=consumer)
        producer_thread.start()
        consumer_thread.start()
        producer_thread.join()
        consumer_thread.join()
        self.assertEqual(result, list(range(10)))