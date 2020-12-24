# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/main.py
# Compiled at: 2020-04-09 07:14:27
# Size of source mod 2**32: 1517 bytes
import argparse
from esa import ESA
from preprocessor import Preprocessor

def create_argparser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', required=True)
    parser.add_argument('-s', required=False, default='cos', choices=[
     'cos', 'max', 'avg'],
      help='similarity measure to use')
    parser.add_argument('document', nargs=(argparse.REMAINDER))
    return parser


def main():
    parser = create_argparser()
    args = parser.parse_args()
    word_level = False
    matrix_path = vars(args)['c']
    similarity = vars(args)['s']
    model_path = '../../../../resources/esa-w2v/GoogleNews-vectors-negative300.bin'
    matrix_path = '../../../../resources/esa-w2v/debatepedia.mat'
    vocab_path = '../../../../resources/esa-w2v/w2v-vocab.p'
    similarity = 'max'
    try:
        input_document = vars(args)['document'][0]
        esa = ESA(matrix_path, model_path, vocab_path, similarity)
        results = esa.process(input_document, word_level)
        if not word_level:
            for result in results:
                print(f"{results[result]:30.30f} {result}")

        else:
            for result in results:
                print(f"{result} - {results[result]}")

    except IndexError:
        print('ERROR: no input text specified')


if __name__ == '__main__':
    main()