# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/data_input/char_and_ngrams.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 1617 bytes
from tokenizer_tools.conll.reader import read_conll
from hanzi_char_lookup_feature.n_gram_lookup.load_dicts_from_files import load_dicts_from_files
from hanzi_char_lookup_feature.n_gram_lookup.ngrams_feature import ngrams_feature_mapping
from hanzi_char_lookup_feature.n_gram_lookup.ngrams_feature import generate_lookup_feature, load_data_set

def parse_fn(word_tag_pairs, t, params):
    words = [i[0] for i in word_tag_pairs]
    tags = [i[1] for i in word_tag_pairs]
    assert len(words) == len(tags), "Words and tags lengths don't match"
    words_char = ''.join(words)
    lookup_feature = generate_lookup_feature(words_char, 4, t, ['person'], dropout_rate=(params['dropout_rate']))
    return (
     (
      words, len(words), lookup_feature), tags)


def generator_fn(input_file, params):
    t = load_data_set(params['trie_data_mapping'])
    sentence_list = read_conll(input_file, sep=None)
    for sentence in sentence_list:
        word_tag_pairs = [(i[0], i[1]) for i in sentence]
        yield parse_fn(word_tag_pairs, t, params)


if __name__ == '__main__':
    for i in generator_fn('/Users/howl/PyCharmProjects/seq2annotation/data/test.txt', {'trie_data_mapping': {'person': ['/Users/howl/PyCharmProjects/hanzi_char_lookup_feature/data/THUOCL_lishimingren.txt']}}):
        print(i)