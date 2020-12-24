# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utils/learning_schedules_test.py
# Compiled at: 2018-06-15 01:29:00
# Size of source mod 2**32: 2406 bytes
"""Tests for object_detection.utils.learning_schedules."""
import tensorflow as tf
from object_detection.utils import learning_schedules

class LearningSchedulesTest(tf.test.TestCase):

    def testExponentialDecayWithBurnin(self):
        global_step = tf.placeholder(tf.int32, [])
        learning_rate_base = 1.0
        learning_rate_decay_steps = 3
        learning_rate_decay_factor = 0.1
        burnin_learning_rate = 0.5
        burnin_steps = 2
        exp_rates = [0.5, 0.5, 1, 0.1, 0.1, 0.1, 0.01, 0.01]
        learning_rate = learning_schedules.exponential_decay_with_burnin(global_step, learning_rate_base, learning_rate_decay_steps, learning_rate_decay_factor, burnin_learning_rate, burnin_steps)
        with self.test_session() as (sess):
            output_rates = []
            for input_global_step in range(8):
                output_rate = sess.run(learning_rate, feed_dict={global_step: input_global_step})
                output_rates.append(output_rate)

            self.assertAllClose(output_rates, exp_rates)

    def testManualStepping(self):
        global_step = tf.placeholder(tf.int64, [])
        boundaries = [2, 3, 7]
        rates = [1.0, 2.0, 3.0, 4.0]
        exp_rates = [1.0, 1.0, 2.0, 3.0, 3.0, 3.0, 3.0, 4.0, 4.0, 4.0]
        learning_rate = learning_schedules.manual_stepping(global_step, boundaries, rates)
        with self.test_session() as (sess):
            output_rates = []
            for input_global_step in range(10):
                output_rate = sess.run(learning_rate, feed_dict={global_step: input_global_step})
                output_rates.append(output_rate)

            self.assertAllClose(output_rates, exp_rates)


if __name__ == '__main__':
    tf.test.main()