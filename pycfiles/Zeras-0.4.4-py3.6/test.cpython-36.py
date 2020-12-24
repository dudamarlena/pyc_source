# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Zeras/test.py
# Compiled at: 2020-03-15 07:46:43
# Size of source mod 2**32: 474 bytes
import tensorflow as tf

def test_tensorflow_gpu():
    """
    """
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name='a')
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name='b')
    c = tf.matmul(a, b)
    sess = tf.Session(config=tf.ConfigProto(log_device_placement=True))
    print(sess.run(c))


if __name__ == '__main__':
    test_tensorflow_gpu()