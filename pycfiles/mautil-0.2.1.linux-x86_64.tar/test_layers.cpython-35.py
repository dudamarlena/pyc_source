# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/test/test_layers.py
# Compiled at: 2019-06-04 20:04:19
# Size of source mod 2**32: 1286 bytes
import numpy as np, logging, sys, tensorflow as tf
from mautil.tf_layers import EMB, RNN
from mautil.tf_models import TF, InputFeature
from sklearn.model_selection import train_test_split

class Model(TF):

    def _init_input_features(self):
        features = []
        features.append(InputFeature('inputs', [None, 5, 16], tf.float32))
        features.append(InputFeature('inputs_len', [None], tf.float32))
        features.append(InputFeature('tgt', [None, 16], tf.float32))
        return features

    def _add_main_graph(self):
        dims = [
         16, 16]
        rnn = RNN(dims, bidirection=False)
        _, outs = rnn(self.inputs, inputs_lens=self.inputs_len)
        self._loss = tf.losses.mean_squared_error(outs[(-1)], self.tgt)


def main():
    train_num = 900
    x = np.random.rand(1000, 5, 16)
    y = np.sum(x, -2)
    x, xV, y, yV = train_test_split(x, y, test_size=0.1, shuffle=False)
    x = {'inputs': x, 'inputs_len': np.ones([len(x)])}
    xV = {'inputs': xV, 'inputs_len': np.ones(len(xV))}
    y = {'tgt': y}
    yV = {'tgt': yV}
    model = Model()
    loss, val_loss = model.fit(x, y, xV, yV)


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(levelname)s:%(threadName)s %(message)s')
    main()