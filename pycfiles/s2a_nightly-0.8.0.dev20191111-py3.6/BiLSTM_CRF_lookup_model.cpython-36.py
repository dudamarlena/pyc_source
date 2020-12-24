# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/algorithms/BiLSTM_CRF_lookup_model.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 1361 bytes
import tensorflow as tf
from seq2annotation.algorithms.lookup_model import LookupModel

class BilstmCrfLookupModel(LookupModel):

    def bilstm_layer(self, embeddings, nwords):
        t = tf.transpose(embeddings, perm=[1, 0, 2])
        lstm_cell_fw = tf.contrib.rnn.LSTMBlockFusedCell(self.params['lstm_size'])
        lstm_cell_bw = tf.contrib.rnn.LSTMBlockFusedCell(self.params['lstm_size'])
        lstm_cell_bw = tf.contrib.rnn.TimeReversedFusedRNN(lstm_cell_bw)
        output_fw, _ = lstm_cell_fw(t, dtype=(tf.float32), sequence_length=nwords)
        output_bw, _ = lstm_cell_bw(t, dtype=(tf.float32), sequence_length=nwords)
        output = tf.concat([output_fw, output_bw], axis=(-1))
        output = tf.transpose(output, perm=[1, 0, 2])
        return output

    def call(self, embeddings, nwords):
        data = self.bilstm_layer(embeddings, nwords)
        return data