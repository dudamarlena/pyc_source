# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/xinci/xinci/utils.py
# Compiled at: 2018-06-19 23:08:50
"""This module contains some utility functions and classes."""
from __future__ import unicode_literals
import codecs, re, logging, argparse
from six.moves import xrange
ch = logging.StreamHandler()

class WordCountDict(dict):

    def add(self, word):
        self[word] = self.get(word) + 1

    def get(self, word):
        return super(WordCountDict, self).get(word, 0)

    def count(self):
        return sum(self.values())


def data_reader(filename, cn_only=False):
    try:
        with codecs.open(filename, encoding=b'utf-8') as (f):
            text = f.read()
    except UnicodeDecodeError:
        with codecs.open(filename, encoding=b'gbk') as (f):
            text = f.read()

    if cn_only:
        re_non_cn = re.compile(b'[^一-龥]+')
        text = re_non_cn.sub(b'', text)
    return text


class TextUtils:

    @staticmethod
    def is_chinese(char):
        return b'一' <= char <= b'龥'

    @staticmethod
    def is_english(char):
        return char.isalpha()

    @staticmethod
    def is_numeric(char):
        return char.isdigit()

    @staticmethod
    def match(src, off, dest):
        src_len = len(src)
        dest_len = len(dest)
        for i in xrange(dest_len):
            if src_len <= off + i:
                return False
            if src[(off + i)] != dest[i]:
                return False

        return True


def get_opt():
    parser = argparse.ArgumentParser(description=b'Xinci.')
    parser.add_argument(b'-f', b'--corpus_file', type=str, help=b'Required, input corpus file path to xinci.')
    parser.add_argument(b'-d', b'--common_words_file', type=str, help=b'Optional, common words file path. ')
    parser.add_argument(b'--min_candidate_len', type=int, default=2, help=b'Candidate word min length.')
    parser.add_argument(b'--max_candidate_len', type=int, default=5, help=b'Candidate word max length.')
    parser.add_argument(b'--least_cnt_threshold', type=int, default=5, help=b'Least word count.')
    parser.add_argument(b'--solid_rate_threshold', type=float, default=0.018, help=b'Solid rate threshold.')
    parser.add_argument(b'--entropy_threshold', type=float, default=1.92, help=b'Entropy.')
    parser.add_argument(b'-o', b'--save_file', type=str, help=b'New words output path.')
    parser.add_argument(b'-a', b'--all_words', action=b'store_true', help=b'Set to extract all words.')
    parser.add_argument(b'-v', b'--verbose', action=b'store_true', help=b'Verbose.')
    args, unparsed = parser.parse_known_args()
    if args.verbose:
        print b'verbosity turned on'
    return args


def get_logger():
    """Return a logger instance. """
    logger = logging.getLogger(b'xinci')
    formatter = logging.Formatter(b'%(asctime)s-%(name)s-%(levelname)s: %(message)s')
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger