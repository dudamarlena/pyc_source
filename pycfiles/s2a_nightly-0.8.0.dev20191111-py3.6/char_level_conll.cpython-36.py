# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/data_input/char_level_conll.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 921 bytes
from tokenizer_tools.conll.reader import read_conll

def parse_fn(word_tag_pairs):
    words = [i[0] for i in word_tag_pairs]
    tags = [i[1] for i in word_tag_pairs]
    assert len(words) == len(tags), "Words and tags lengths don't match"
    return ((words, len(words)), tags)


def generator_fn(input_file):
    sentence_list = read_conll(input_file, sep=None)
    for sentence in sentence_list:
        word_tag_pairs = [(i[0], i[1]) for i in sentence]
        yield parse_fn(word_tag_pairs)


if __name__ == '__main__':
    for i in generator_fn('data/corpus/test.txt'):
        print(i)