# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/utils/file_utils.py
# Compiled at: 2019-03-20 07:49:31
# Size of source mod 2**32: 1107 bytes
import pickle

def save_obj(obj, file_path):
    with open(file_path + '.pkl', 'wb') as (f):
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(file_path):
    with open(file_path + '.pkl', 'rb') as (f):
        return pickle.load(f)


def get_unique_vocab(analogy_file_path, write_out_file):
    """

    :param analogy_file_path:
    :param write_out_file:
    :return:
    """
    vocab_dict = {}
    with open(analogy_file_path, 'r') as (freader):
        for line in freader:
            if line.__contains__(' | '):
                word_parts = line.split(' | ')
                for word in word_parts:
                    word = word.rstrip()
                    vocab_dict[word] = 0

    fwriter = open(write_out_file, 'w')
    for word in vocab_dict.keys():
        fwriter.write(word + '\n')

    fwriter.close()
    print('Write dictionary file to %s' % write_out_file)
    return vocab_dict


if __name__ == '__main__':
    get_unique_vocab('../data/embedding_analogies/portuguese/LX-4WAnalogies-ETNLP.txt', '../data/embedding_analogies/portuguese/vocab.txt')