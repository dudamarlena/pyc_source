# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/trainer/cli_keras_with_constraint.py
# Compiled at: 2019-11-04 07:23:49
# Size of source mod 2**32: 7917 bytes
import json, os
from collections import Counter
import numpy as np, tensorflow as tf
from tensorflow.python.keras import models
from tensorflow.python.keras.layers import Embedding, Bidirectional, LSTM
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras import layers
from ioflow.configure import read_configure
from ioflow.corpus import get_corpus_processor
from seq2annotation.input import generate_tagset, Lookuper, index_table_from_file
from tf_crf_layer.layer import CRF
from tf_crf_layer.loss import crf_loss
from tf_crf_layer.metrics import crf_accuracy
from tokenizer_tools.tagset.converter.offset_to_biluo import offset_to_biluo
config = read_configure()
corpus = get_corpus_processor(config)
corpus.prepare()
train_data_generator_func = corpus.get_generator_func(corpus.TRAIN)
eval_data_generator_func = corpus.get_generator_func(corpus.EVAL)
corpus_meta_data = corpus.get_meta_info()
raw_tag_data = corpus_meta_data['tags']
tags_data = generate_tagset(corpus_meta_data['tags'])
train_data = list(train_data_generator_func())
eval_data = list(eval_data_generator_func())
tag_lookuper = Lookuper({v:i for i, v in enumerate(tags_data)})
vocab_data_file = os.path.join(os.path.dirname(__file__), '../data/unicode_char_list.txt')
vocabulary_lookuper = index_table_from_file(vocab_data_file)

def one_hot(a, num_classes):
    return np.squeeze(np.eye(num_classes)[a.reshape(-1)])


def preprocss(data, maxlen=None, intent_lookup_table=None):
    raw_x = []
    raw_y = []
    raw_intent = []
    for offset_data in data:
        tags = offset_to_biluo(offset_data)
        words = offset_data.text
        label = offset_data.extra_attr[config['intent_field']] if config['intent_field'] not in ('label', ) else getattr(offset_data, config['intent_field'])
        tag_ids = [tag_lookuper.lookup(i) for i in tags]
        word_ids = [vocabulary_lookuper.lookup(i) for i in words]
        raw_x.append(word_ids)
        raw_y.append(tag_ids)
        raw_intent.append(label)

    if not intent_lookup_table:
        raw_intent_set = list(set(raw_intent))
        intent_lookup_table = Lookuper({v:i for i, v in enumerate(raw_intent_set)})
    intent_int_list = [intent_lookup_table.lookup(i) for i in raw_intent]
    if not maxlen:
        maxlen = max(len(s) for s in raw_x)
    x = tf.keras.preprocessing.sequence.pad_sequences(raw_x, maxlen, padding='post')
    y = tf.keras.preprocessing.sequence.pad_sequences(raw_y, maxlen, value=0, padding='post')
    intent_np_array = np.array(intent_int_list)
    intent_one_hot = one_hot(intent_np_array, np.max(intent_np_array) + 1)
    return (
     x, intent_one_hot, y, intent_lookup_table)


MAX_LEN = 25
train_x, train_intent, train_y, intent_lookup_table = preprocss(train_data, MAX_LEN)
test_x, test_intent, test_y, _ = preprocss(eval_data, MAX_LEN, intent_lookup_table)
intent_number = train_intent.shape[1]
from tf_crf_layer.crf_dynamic_constraint_helper import generate_constraint_table, filter_constraint, sort_constraint
constraint_file = config.get('constraint')
with open(constraint_file) as (fd):
    constraint = json.load(fd)
tag_set = raw_tag_data
intent_set = intent_lookup_table.index_table.keys()
valid_constraint = filter_constraint(constraint, tag_set, intent_set)
wrong_constraint_mapping = list(valid_constraint.values())
right_constraint_mapping = sort_constraint(valid_constraint, intent_lookup_table.index_table)
tag_dict = tag_lookuper.inverse_index_table
expected_constraint_table = np.array([
 [
  [
   1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
 [
  [
   1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [
   0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [
   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]],
  dtype=(np.bool))
constraint_table = generate_constraint_table(right_constraint_mapping, tag_dict)
EPOCHS = 10
EMBED_DIM = 64
BiRNN_UNITS = 200
vacab_size = vocabulary_lookuper.size()
tag_size = tag_lookuper.size()
raw_input = layers.Input(shape=(MAX_LEN,))
embedding_layer = Embedding(vacab_size, EMBED_DIM, mask_zero=True)(raw_input)
bilstm_layer = Bidirectional(LSTM((BiRNN_UNITS // 2), return_sequences=True))(embedding_layer)
crf_layer = CRF(units=tag_size,
  transition_constraint_matrix=constraint_table)
dynamic_constraint_input = layers.Input(shape=(intent_number,))
output_layer = crf_layer([bilstm_layer, dynamic_constraint_input])
model = models.Model([raw_input, dynamic_constraint_input], output_layer)
model.summary()
callbacks_list = []
model.compile('adam', loss=crf_loss, metrics=[crf_accuracy])
model.fit([
 train_x, train_intent],
  train_y, epochs=EPOCHS,
  validation_data=[
 [
  test_x, test_intent], test_y],
  callbacks=callbacks_list)