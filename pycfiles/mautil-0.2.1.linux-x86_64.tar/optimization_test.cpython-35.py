# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/mautil/tf_net/bert/optimization_test.py
# Compiled at: 2019-07-15 21:40:48
# Size of source mod 2**32: 1721 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import optimization, tensorflow as tf

class OptimizationTest(tf.test.TestCase):

    def test_adam(self):
        with self.test_session() as (sess):
            w = tf.get_variable('w', shape=[
             3], initializer=tf.constant_initializer([0.1, -0.2, -0.1]))
            x = tf.constant([0.4, 0.2, -0.5])
            loss = tf.reduce_mean(tf.square(x - w))
            tvars = tf.trainable_variables()
            grads = tf.gradients(loss, tvars)
            global_step = tf.train.get_or_create_global_step()
            optimizer = optimization.AdamWeightDecayOptimizer(learning_rate=0.2)
            train_op = optimizer.apply_gradients(zip(grads, tvars), global_step)
            init_op = tf.group(tf.global_variables_initializer(), tf.local_variables_initializer())
            sess.run(init_op)
            for _ in range(100):
                sess.run(train_op)

            w_np = sess.run(w)
            self.assertAllClose(w_np.flat, [0.4, 0.2, -0.5], rtol=0.01, atol=0.01)


if __name__ == '__main__':
    tf.test.main()