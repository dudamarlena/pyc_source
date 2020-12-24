# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nn_wtf/summary_writer_mixin.py
# Compiled at: 2016-12-21 17:26:02
from nn_wtf.neural_network_graph_mixin import NeuralNetworkGraphMixin, DEFAULT_TRAIN_DIR
from nn_wtf.trainer import Trainer
import tensorflow as tf
__author__ = 'Lene Preuss <lene.preuss@gmail.com>'

class SummaryWriterMixin(NeuralNetworkGraphMixin):

    def __init__(self, session, verbose=False, train_dir=DEFAULT_TRAIN_DIR):
        super().__init__(session, train_dir)
        self.verbose = verbose
        self._setup_summaries()

    def write_summary(self, feed_dict, loss_value, step):
        if self.verbose:
            print 'Step %d: loss = %.2f ' % (step, loss_value)
        summary_str = self.session.run(self.summary_op, feed_dict=feed_dict)
        self.summary_writer.add_summary(summary_str, step)

    def print_evaluations(self, data_sets, batch_size):
        assert isinstance(self.trainer, Trainer), 'used SummaryMixin on a class other than NeuralNetworkGraph'
        self._print_eval(data_sets.train, batch_size, 'Training Data Eval:')
        self._print_eval(data_sets.validation, batch_size, 'Validation Data Eval:')
        self._print_eval(data_sets.test, batch_size, 'Test Data Eval:')

    def _print_eval(self, data_set, batch_size, message):
        if self.verbose:
            print message
            evaluation = self.trainer.do_eval(data_set, batch_size)
            print ('  Num examples: {}  Num correct: {}  Precision @ 1: {:5.2f}').format(evaluation.num_examples, evaluation.true_count, evaluation.precision)

    def _setup_summaries(self):
        self.summary_op = tf.summary.merge_all()
        self.summary_writer = tf.summary.FileWriter(self.train_dir, graph=self.session.graph)