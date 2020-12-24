# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/external/baselines/baselines/gail/statistics.py
# Compiled at: 2018-04-01 14:21:44
# Size of source mod 2**32: 1802 bytes
"""
This code is highly based on https://github.com/carpedm20/deep-rl-tensorflow/blob/master/agents/statistic.py
"""
import tensorflow as tf, numpy as np, baselines.common.tf_util as U

class stats:

    def __init__(self, scalar_keys=[], histogram_keys=[]):
        self.scalar_keys = scalar_keys
        self.histogram_keys = histogram_keys
        self.scalar_summaries = []
        self.scalar_summaries_ph = []
        self.histogram_summaries_ph = []
        self.histogram_summaries = []
        with tf.variable_scope('summary'):
            for k in scalar_keys:
                ph = tf.placeholder('float32', None, name=k + '.scalar.summary')
                sm = tf.summary.scalar(k + '.scalar.summary', ph)
                self.scalar_summaries_ph.append(ph)
                self.scalar_summaries.append(sm)

            for k in histogram_keys:
                ph = tf.placeholder('float32', None, name=k + '.histogram.summary')
                sm = tf.summary.scalar(k + '.histogram.summary', ph)
                self.histogram_summaries_ph.append(ph)
                self.histogram_summaries.append(sm)

        self.summaries = tf.summary.merge(self.scalar_summaries + self.histogram_summaries)

    def add_all_summary(self, writer, values, iter):
        if np.sum(np.isnan(values) + 0) != 0:
            return
        sess = U.get_session()
        keys = self.scalar_summaries_ph + self.histogram_summaries_ph
        feed_dict = {}
        for k, v in zip(keys, values):
            feed_dict.update({k: v})

        summaries_str = sess.run(self.summaries, feed_dict)
        writer.add_summary(summaries_str, iter)