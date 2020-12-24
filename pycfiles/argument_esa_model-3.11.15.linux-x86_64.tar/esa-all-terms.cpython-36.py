# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/esa-all-terms.py
# Compiled at: 2020-05-12 09:02:27
# Size of source mod 2**32: 940 bytes
import sys, argparse, pandas as pd
from esa import ESA

def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--similarity', required=True)
    parser.add_argument('--matrix-path', required=True)
    parser.add_argument('--model-path', required=True)
    parser.add_argument('--model-vocab', required=True)
    parser.add_argument('--text', required=True)
    return parser


def main():
    parser = create_argparser()
    args = parser.parse_args()
    similarity = vars(args)['similarity']
    matrix_path = vars(args)['matrix_path']
    model_path = vars(args)['model_path']
    vocab_path = vars(args)['model_vocab']
    text = vars(args)['text']
    e = ESA(matrix_path=matrix_path, model_path=model_path, vocab_path=vocab_path, similarity=similarity)
    result = e.process(text, False)
    print(result)


if __name__ == '__main__':
    main()