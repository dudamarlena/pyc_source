# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qndex/classify.py
# Compiled at: 2017-04-13 05:28:56
# Size of source mod 2**32: 1654 bytes
import argtyp, extenteten as ex, tensorflow as tf, qnd

def def_num_classes():
    qnd.add_required_flag('num_classes', type=int)

    def num_classes():
        return qnd.FLAGS.num_classes

    return num_classes


def def_num_labels():
    qnd.add_flag('num_labels', type=int)

    def num_labels():
        return qnd.FLAGS.num_labels

    return num_labels


def def_classify():
    get_num_classes = def_num_classes()
    get_num_labels = def_num_labels()
    qnd.add_flag('hidden_layer_sizes', type=(argtyp.int_list), default=[100])
    qnd.add_flag('dropout_keep_prob', type=float)

    def classify(feature, true_label=None, *, mode, key=None, predictions={}, regularization_scale=1e-08):
        num_classes = get_num_classes()
        if num_classes <= 1:
            raise ValueError('Number of classes must be greater than 1.')
        num_labels = get_num_labels() or ex.num_labels(true_label)
        return ex.classify(ex.mlp(feature,
          layer_sizes=[
         *qnd.FLAGS.hidden_layer_sizes,
         
          ex.num_logits(num_labels, num_classes)],
          dropout_keep_prob=(qnd.FLAGS.dropout_keep_prob if mode == tf.contrib.learn.ModeKeys.TRAIN else None)),
          true_label,
          num_classes=num_classes,
          num_labels=num_labels,
          key=key,
          predictions=predictions,
          regularization_scale=regularization_scale)

    return classify