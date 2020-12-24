# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/esa_all_terms.py
# Compiled at: 2020-04-09 07:23:04
# Size of source mod 2**32: 1194 bytes
import sys, argparse
from argument_esa_model.esa import ESA
e = None

def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--similarity', required=True)
    parser.add_argument('--matrix-path', required=True)
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--model-vocab', required=True)
    parser.add_argument('--text', required=True)
    return parser


def initialize_model():
    global e
    e = None


def model_topic(path_matrix, path_model, path_vocab, similarity, text):
    global e
    if e == None:
        e = ESA(matrix_path=path_matrix, model_path=path_model, vocab_path=path_vocab, similarity=similarity)
    result = e.process(text, False)
    return result


def main():
    parser = create_argparser()
    args = parser.parse_args()
    similarity = vars(args)['similarity']
    path_matrix = vars(args)['matrix_path']
    path_model = vars(args)['model_path']
    path_vocab = vars(args)['model_vocab']
    text = vars(args)['text']
    result = model_topic(path_matrix, path_model, path_vocab, similarity, text)
    print(result)


if __name__ == '__main__':
    main()