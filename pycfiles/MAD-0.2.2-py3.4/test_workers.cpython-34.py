# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\simulation\test_workers.py
# Compiled at: 2016-04-27 08:08:14
# Size of source mod 2**32: 3697 bytes
from unittest import TestCase
from mad.simulation.workers import WorkerPool

class WorkerPoolTests(TestCase):

    def test_all_busy(self):
        pool = WorkerPool(['a', 'b', 'c'])
        self.assertTrue(pool.are_available)
        for i in range(3):
            pool.acquire_one()

        self.assertFalse(pool.are_available)

    def test_acquiring_idle_worker(self):
        pool = WorkerPool(['a', 'b', 'c'])
        worker = pool.acquire_one()
        self.assertTrue(worker in pool.busy_workers)
        self.assertEqual(pool.idle_worker_count, 2)

    def test_release_worker(self):
        pool = WorkerPool(['a', 'b', 'c'])
        worker = pool.acquire_one()
        pool.release(worker)
        self.assertTrue(worker not in pool.busy_workers)
        self.assertTrue(worker in pool.idle_workers)
        self.assertEqual(pool.idle_worker_count, 3)

    def test_add_new_workers(self):
        pool = WorkerPool(['w1'])
        pool.add_workers(['w2', 'w3', 'w4'])
        self.assertEqual(4, pool.idle_worker_count)

    def test_shutting_down_only_idle_workers(self):
        pool = WorkerPool(['w1', 'w2', 'w3', 'w4'])
        pool.shutdown(3)
        self.assertEqual(1, pool.capacity)
        self.assertEqual(1, pool.idle_worker_count)

    def test_shutting_down_busy_workers(self):
        pool = WorkerPool(['w1', 'w2', 'w3', 'w4'])
        w1 = pool.acquire_one()
        w2 = pool.acquire_one()
        pool.shutdown(3)
        self.assertEqual(0, pool.idle_worker_count)
        self.assertEqual(1, pool.capacity)
        self.assertTrue(w1 in pool.stopped_workers)
        pool.release(w1)
        self.assertEqual(0, pool.idle_worker_count)
        self.assertEqual(1, pool.capacity)
        pool.release(w2)
        self.assertEqual(1, pool.idle_worker_count)
        self.assertEqual(1, pool.capacity)

    def test_acquire_is_not_permitted_on_empty_pools(self):
        pool = WorkerPool(['w1'])
        pool.acquire_one()
        with self.assertRaises(ValueError):
            pool.acquire_one()

    def test_utilisation(self):
        pool = WorkerPool(['w1', 'w2', 'w3', 'w4'])
        self.assertAlmostEqual(pool.utilisation, float(0))
        wA = pool.acquire_one()
        wB = pool.acquire_one()
        self.assertAlmostEqual(pool.utilisation, float(50.0))
        pool.add_workers(['w5', 'w6'])
        self.assertAlmostEqual(pool.utilisation, float(33.333333333333336))
        pool.release(wB)
        self.assertAlmostEqual(pool.utilisation, float(16.666666666666668))
        pool.shutdown(4)
        self.assertAlmostEqual(pool.utilisation, float(50.0))

    def test_add_worker(self):
        pool = WorkerPool(['w1', 'w2'])
        self.assertEqual(2, pool.capacity)
        pool.add_workers(['w3', 'w4'])
        self.assertEqual(4, pool.capacity)


if __name__ == '__main__':
    import unittest.main
    unittest.main()