# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hoangpham/git_project/nnvlp-package/nnvlp/nnvlp.py
# Compiled at: 2017-09-25 00:48:35
import os, subprocess, shlex, cPickle as pickle, numpy as np
from alphabet import Alphabet
import network, codecs, theano, lasagne, utils
from pyvi.pyvi import ViTokenizer
from nltk.tokenize import sent_tokenize
import threading
LOCK = threading.Lock()
current_dir = os.path.dirname(os.path.realpath(__file__))
with open(current_dir + '/embedding/words.pl', 'rb') as (handle):
    embedd_words = pickle.load(handle)
unknown_embedd = np.load(current_dir + '/embedding/unknown.npy')

def download():
    subprocess.call(shlex.split('bash embedding.sh'), cwd=current_dir)


def load_config(config_file):
    config = dict()
    with codecs.open(config_file + '/config.ini', 'r', 'utf-8') as (f):
        for line in f:
            line = line.strip().split('\t')
            config[line[0]] = line[1]

    max_sent_length = int(config['max_sent_length'])
    max_char_length = int(config['max_char_length'])
    num_labels = int(config['num_labels'])
    embedd_dim_concat = int(config['embedd_dim_concat'])
    return (max_sent_length, max_char_length, num_labels, embedd_dim_concat)


def load_config_pos(config_path, char_embedd_dim):
    max_sent_length, max_char_length, num_labels, embedd_dim_concat = load_config(config_path)
    alphabet_char = Alphabet('char', keep_growing=False)
    alphabet_char.load(config_path, 'alphabet_char')
    alphabet_label = Alphabet('label', keep_growing=False)
    alphabet_label.load(config_path, 'alphabet_label')
    scale = np.sqrt(3.0 / char_embedd_dim)
    char_embedd_table = np.random.uniform(-scale, scale, [alphabet_char.size(), char_embedd_dim]).astype(theano.config.floatX)
    return (max_sent_length, max_char_length, num_labels, embedd_dim_concat, alphabet_char, alphabet_label,
     char_embedd_table)


def load_config_chunk(config_path, char_embedd_dim):
    max_sent_length, max_char_length, num_labels, embedd_dim_concat = load_config(config_path)
    alphabet_pos = Alphabet('pos', keep_growing=False)
    alphabet_pos.load(config_path, 'alphabet_pos')
    alphabet_char = Alphabet('char', keep_growing=False)
    alphabet_char.load(config_path, 'alphabet_char')
    alphabet_label = Alphabet('label', keep_growing=False)
    alphabet_label.load(config_path, 'alphabet_label')
    scale = np.sqrt(3.0 / char_embedd_dim)
    char_embedd_table = np.random.uniform(-scale, scale, [alphabet_char.size(), char_embedd_dim]).astype(theano.config.floatX)
    return (max_sent_length, max_char_length, num_labels, embedd_dim_concat, alphabet_char, alphabet_label,
     alphabet_pos, char_embedd_table)


def load_config_ner(config_path, char_embedd_dim):
    max_sent_length, max_char_length, num_labels, embedd_dim_concat = load_config(config_path)
    alphabet_pos = Alphabet('pos', keep_growing=False)
    alphabet_pos.load(config_path, 'alphabet_pos')
    alphabet_chunk = Alphabet('chunk', keep_growing=False)
    alphabet_chunk.load(config_path, 'alphabet_chunk')
    alphabet_char = Alphabet('char', keep_growing=False)
    alphabet_char.load(config_path, 'alphabet_char')
    alphabet_label = Alphabet('label', keep_growing=False)
    alphabet_label.load(config_path, 'alphabet_label')
    scale = np.sqrt(3.0 / char_embedd_dim)
    char_embedd_table = np.random.uniform(-scale, scale, [alphabet_char.size(), char_embedd_dim]).astype(theano.config.floatX)
    return (max_sent_length, max_char_length, num_labels, embedd_dim_concat, alphabet_char, alphabet_label,
     alphabet_pos, alphabet_chunk, char_embedd_table)


def set_weights(filename, model):
    with np.load(filename) as (f):
        param_values = [ f[('arr_%d' % i)] for i in range(len(f.files)) ]
    lasagne.layers.set_all_param_values(model, param_values)


def predict_label(words, masks, chars, predict_fn, alphabet_label):
    predict_list = []
    for batch in utils.iterate_minibatches(words, masks=masks, char_inputs=chars):
        word_inputs, mask_inputs, char_inputs = batch
        with LOCK:
            predicts = predict_fn(word_inputs, mask_inputs, char_inputs)
        predict_list += utils.output_predictions(predicts, mask_inputs, alphabet_label)

    return predict_list


def load_data_pos(sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length, max_char_length, alphabet_char):
    words, masks = utils.construct_tensor_word(sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length)
    index_chars = utils.get_character_indexes(sents, alphabet_char, max_char_length)
    chars = utils.construct_tensor_char(index_chars, max_sent_length, max_char_length, alphabet_char)
    return (words, masks, chars)


def load_data_chunk(sents, pos_sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length, max_char_length, alphabet_char, alphabet_pos):
    words, masks = utils.construct_tensor_word(sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length)
    index_poss = utils.map_string_2_id_close(pos_sents, alphabet_pos)
    poss = utils.construct_tensor_onehot(index_poss, max_sent_length, alphabet_pos.size())
    words = np.concatenate((words, poss), axis=2)
    index_chars = utils.get_character_indexes(sents, alphabet_char, max_char_length)
    chars = utils.construct_tensor_char(index_chars, max_sent_length, max_char_length, alphabet_char)
    return (words, masks, chars)


def load_data_ner(sents, pos_sents, chunk_sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length, max_char_length, alphabet_char, alphabet_pos, alphabet_chunk):
    words, masks = utils.construct_tensor_word(sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length)
    index_poss = utils.map_string_2_id_close(pos_sents, alphabet_pos)
    poss = utils.construct_tensor_onehot(index_poss, max_sent_length, alphabet_pos.size())
    index_chunks = utils.map_string_2_id_close(chunk_sents, alphabet_chunk)
    chunks = utils.construct_tensor_onehot(index_chunks, max_sent_length, alphabet_chunk.size())
    words = np.concatenate((words, poss), axis=2)
    words = np.concatenate((words, chunks), axis=2)
    index_chars = utils.get_character_indexes(sents, alphabet_char, max_char_length)
    chars = utils.construct_tensor_char(index_chars, max_sent_length, max_char_length, alphabet_char)
    return (words, masks, chars)


def token_data(raw_texts):
    output_texts = []
    len_texts = []
    token_texts = sent_tokenize(raw_texts)
    for text in token_texts:
        token_text = ViTokenizer.tokenize(text).split()
        len_text = len(token_text)
        len_texts.append(len_text)
        output_texts += [ token_text[i:i + max_sent_length] for i in xrange(0, len(token_text), max_sent_length) ]

    return (
     output_texts, len_texts)


def predict(sents):
    pos_words, pos_masks, pos_chars = load_data_pos(sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length_pos, max_char_length_pos, alphabet_char_pos)
    pos_sents = predict_label(pos_words, pos_masks, pos_chars, predict_fn_pos, alphabet_label_pos)
    chunk_words, chunk_masks, chunk_chars = load_data_chunk(sents, pos_sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length_chunk, max_char_length_chunk, alphabet_char_chunk, alphabet_pos_chunk)
    chunk_sents = predict_label(chunk_words, chunk_masks, chunk_chars, predict_fn_chunk, alphabet_label_chunk)
    ner_words, ner_masks, ner_chars = load_data_ner(sents, pos_sents, chunk_sents, unknown_embedd, embedd_words, embedd_vectors, embedd_dim, max_sent_length_ner, max_char_length_ner, alphabet_char_ner, alphabet_pos_ner, alphabet_chunk_ner)
    ner_sents = predict_label(ner_words, ner_masks, ner_chars, predict_fn_ner, alphabet_label_ner)
    return (pos_sents, chunk_sents, ner_sents)


def merge_sent(token_texts, poss, chunks, ners, len_texts):
    merge_token_texts = []
    merge_poss = []
    merge_chunks = []
    merge_ners = []
    for len_text in len_texts:
        token_text = []
        pos = []
        chunk = []
        ner = []
        while 1:
            token_text += token_texts.pop(0)
            pos += poss.pop(0)
            chunk += chunks.pop(0)
            ner += ners.pop(0)
            if len(token_text) == len_text:
                break

        merge_token_texts.append(token_text)
        merge_poss.append(pos)
        merge_chunks.append(chunk)
        merge_ners.append(ner)

    return (
     merge_token_texts, merge_poss, merge_chunks, merge_ners)


class NNVLP(object):

    def __init__(self):
        self.char_embedd_dim = 30
        self.dropout = True
        self.num_filters = 30
        self.num_units = 30
        self.grad_clipping = 5.0
        self.peepholes = True
        self.max_sent_length_pos, self.max_char_length_pos, self.num_labels_pos, self.embedd_dim_pos, self.alphabet_char_pos, self.alphabet_label_pos, self.char_embedd_table_pos = load_config_pos(current_dir + '/pre-trained-model/pos', self.char_embedd_dim)
        self.max_sent_length_chunk, self.max_char_length_chunk, self.num_labels_chunk, self.embedd_dim_chunk, self.alphabet_char_chunk, self.alphabet_label_chunk, self.alphabet_pos_chunk, self.char_embedd_table_chunk = load_config_chunk(current_dir + '/pre-trained-model/chunk', self.char_embedd_dim)
        self.max_sent_length_ner, self.max_char_length_ner, self.num_labels_ner, self.embedd_dim_ner, self.alphabet_char_ner, self.alphabet_label_ner, self.alphabet_pos_ner, self.alphabet_chunk_ner, self.char_embedd_table_ner = load_config_ner(current_dir + '/pre-trained-model/ner', self.char_embedd_dim)
        self.pos_model, self.predict_fn_pos = network.build_model(self.embedd_dim_pos, self.max_sent_length_pos, self.max_char_length_pos, self.alphabet_char_pos.size(), self.char_embedd_dim, self.num_labels_pos, self.dropout, self.num_filters, self.num_units, self.grad_clipping, self.peepholes, self.char_embedd_table_pos)