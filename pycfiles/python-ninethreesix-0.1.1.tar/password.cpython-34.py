# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brad/python-nine-three-six/ninethreesix/password.py
# Compiled at: 2015-04-04 13:10:58
# Size of source mod 2**32: 2353 bytes
import argparse, os
from random import sample
from re import sub, findall

class Password(object):
    __doc__ = 'Creates a XKCD 936-style password using words from a word list. The\n    bundled word list currently comes from the Moby Word list by Grady Ward,\n    which is listed in the public domain.\n\n    The bundled word file is COMMON.TXT, which is:\n\n        74,550 common dictionary words (common.txt)\n        A list of words in common with two or more published dictionaries.\n        This gives the developer of a custom spelling checker a good\n        beginning pool of relatively common words.\n\n    For the original sources, see: http://www.gutenberg.org/ebooks/3201\n\n    This class accepts the following parameters:\n\n    * num_words -- the number of words that will be used to generate the\n      passowrd. Default is 3.\n    * min_len -- the minimum length for any word. Default is 3.\n    * max_len -- the maximum length for any word. Default is 6 (big words are\n      hard to remember!)\n\n    '

    def __init__(self, num_words=3, min_len=3, max_len=6):
        self.num_words = num_words
        self.min_len = min_len
        self.max_len = max_len
        self.content = self._words()

    def _words(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        word_list = os.path.join(parent_dir, 'COMMON.TXT')
        content = open(word_list).read()
        return sub('\\s', ' ', content)

    def password(self):
        pattern = '\\b\\w{{{0},{1}}}\\b'.format(self.min_len, self.max_len)
        words = findall(pattern, self.content)
        return sample(words, self.num_words)

    def as_string(self, delimiter='-'):
        return delimiter.join(self.password())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for Password')
    parser.add_argument('-n', '--num', type=int, default=3, help='Number of words to use in your password')
    parser.add_argument('-m', '--min', type=int, default=3, help='Minimum lenth of each word (default is 3)')
    parser.add_argument('-x', '--max', type=int, default=6, help='Maximum lenth of each word (default is 6)')
    args = parser.parse_args()
    p = Password(num_words=args.num, min_len=args.min, max_len=args.max)
    print('\n{0}\n'.format(p.as_string()))