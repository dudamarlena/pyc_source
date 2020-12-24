# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/sacrebleu/tokenizer.py
# Compiled at: 2020-04-30 19:36:10
# Size of source mod 2**32: 10675 bytes
import re, sys, unicodedata, functools

def tokenize_13a(line):
    """
    Tokenizes an input line using a relatively minimal tokenization that is however equivalent to mteval-v13a, used by WMT.

    :param line: a segment to tokenize
    :return: the tokenized line
    """
    norm = line
    norm = norm.replace('<skipped>', '')
    norm = norm.replace('-\n', '')
    norm = norm.replace('\n', ' ')
    norm = norm.replace('&quot;', '"')
    norm = norm.replace('&amp;', '&')
    norm = norm.replace('&lt;', '<')
    norm = norm.replace('&gt;', '>')
    norm = ' {} '.format(norm)
    norm = re.sub('([\\{-\\~\\[-\\` -\\&\\(-\\+\\:-\\@\\/])', ' \\1 ', norm)
    norm = re.sub('([^0-9])([\\.,])', '\\1 \\2 ', norm)
    norm = re.sub('([\\.,])([^0-9])', ' \\1 \\2', norm)
    norm = re.sub('([0-9])(-)', '\\1 \\2 ', norm)
    norm = re.sub('\\s+', ' ', norm)
    norm = re.sub('^\\s+', '', norm)
    norm = re.sub('\\s+$', '', norm)
    return norm


class UnicodeRegex:
    __doc__ = 'Ad-hoc hack to recognize all punctuation and symbols.\n\n    without depending on https://pypi.python.org/pypi/regex/.'

    @staticmethod
    def _property_chars(prefix):
        return ''.join((chr(x) for x in range(sys.maxunicode) if unicodedata.category(chr(x)).startswith(prefix)))

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def punctuation():
        return UnicodeRegex._property_chars('P')

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def nondigit_punct_re():
        return re.compile('([^\\d])([' + UnicodeRegex.punctuation() + '])')

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def punct_nondigit_re():
        return re.compile('([' + UnicodeRegex.punctuation() + '])([^\\d])')

    @staticmethod
    @functools.lru_cache(maxsize=1)
    def symbol_re():
        return re.compile('([' + UnicodeRegex._property_chars('S') + '])')


def tokenize_v14_international(string):
    r"""Tokenize a string following the official BLEU implementation.

    See https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/mteval-v14.pl#L954-L983
    In our case, the input string is expected to be just one line
    and no HTML entities de-escaping is needed.
    So we just tokenize on punctuation and symbols,
    except when a punctuation is preceded and followed by a digit
    (e.g. a comma/dot as a thousand/decimal separator).

    Note that a number (e.g., a year) followed by a dot at the end of sentence is NOT tokenized,
    i.e. the dot stays with the number because `s/(\p{P})(\P{N})/ $1 $2/g`
    does not match this case (unless we add a space after each sentence).
    However, this error is already in the original mteval-v14.pl
    and we want to be consistent with it.
    The error is not present in the non-international version,
    which uses `$norm_text = " $norm_text "` (or `norm = " {} ".format(norm)` in Python).

    :param string: the input string
    :return: a list of tokens
    """
    string = UnicodeRegex.nondigit_punct_re().sub('\\1 \\2 ', string)
    string = UnicodeRegex.punct_nondigit_re().sub(' \\1 \\2', string)
    string = UnicodeRegex.symbol_re().sub(' \\1 ', string)
    return string.strip()


def tokenize_zh(sentence):
    """MIT License
    Copyright (c) 2017 - Shujian Huang <huangsj@nju.edu.cn>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.

    The tokenization of Chinese text in this script contains two steps: separate each Chinese
    characters (by utf-8 encoding); tokenize the non Chinese part (following the mteval script).
    Author: Shujian Huang huangsj@nju.edu.cn

    :param sentence: input sentence
    :return: tokenized sentence
    """

    def is_chinese_char(uchar):
        """
        :param uchar: input char in unicode
        :return: whether the input char is a Chinese character.
        """
        if uchar >= '㐀':
            if uchar <= '䶵':
                return True
            else:
                if uchar >= '一':
                    if uchar <= '龥':
                        return True
                    else:
                        if uchar >= '龦':
                            if uchar <= '龻':
                                return True
                            else:
                                if uchar >= '豈':
                                    if uchar <= '鶴':
                                        return True
                                    else:
                                        if uchar >= '侮':
                                            if uchar <= '頻':
                                                return True
                                        if uchar >= '並':
                                            if uchar <= '龎':
                                                return True
                                        if uchar >= '\u20000' and uchar <= '⩭6':
                                            return True
                                    if uchar >= '⾀0':
                                        if uchar <= '⾡d':
                                            return True
                                else:
                                    if uchar >= '\uff00':
                                        if uchar <= '\uffef':
                                            return True
                                    if uchar >= '⺀' and uchar <= '\u2eff':
                                        return True
                                if uchar >= '\u3000' and uchar <= '〿':
                                    return True
                            if uchar >= '㇀':
                                if uchar <= '\u31ef':
                                    return True
                        else:
                            if uchar >= '⼀':
                                if uchar <= '\u2fdf':
                                    return True
                            if uchar >= '⿰' and uchar <= '\u2fff':
                                return True
                        if uchar >= '\u3100' and uchar <= '\u312f':
                            return True
                    if uchar >= 'ㆠ':
                        if uchar <= '\u31bf':
                            return True
                else:
                    if uchar >= '︐':
                        if uchar <= '\ufe1f':
                            return True
                    if uchar >= '︰' and uchar <= '﹏':
                        return True
                if uchar >= '☀' and uchar <= '⛿':
                    return True
            if uchar >= '✀':
                if uchar <= '➿':
                    return True
        else:
            if uchar >= '㈀':
                if uchar <= '\u32ff':
                    return True
            if uchar >= '㌀' and uchar <= '㏿':
                return True
        return False

    sentence = sentence.strip()
    sentence_in_chars = ''
    for char in sentence:
        if is_chinese_char(char):
            sentence_in_chars += ' '
            sentence_in_chars += char
            sentence_in_chars += ' '
        else:
            sentence_in_chars += char

    sentence = sentence_in_chars
    sentence = re.sub('([\\{-\\~\\[-\\` -\\&\\(-\\+\\:-\\@\\/])', ' \\1 ', sentence)
    sentence = re.sub('([^0-9])([\\.,])', '\\1 \\2 ', sentence)
    sentence = re.sub('([\\.,])([^0-9])', ' \\1 \\2', sentence)
    sentence = re.sub('([0-9])(-)', '\\1 \\2 ', sentence)
    sentence = re.sub('\\s+', ' ', sentence)
    sentence = sentence.strip()
    return sentence


class TokenizeMeCab:

    def __init__(self):
        self.initialized = False

    def tokenize(self, line):
        """
        Tokenizes an Japanese input line using MeCab morphological analyzer.

        :param line: a segment to tokenize
        :return: the tokenized line
        """
        if not self.initialized:
            try:
                import MeCab
            except ImportError:
                raise ImportError('Please install mecab-python3 for evaluating Japanese (pip install mecab-python3).')

            self.tagger = MeCab.Tagger('-Owakati')
            d = self.tagger.dictionary_info()
            assert d.size == 392126, 'Please make sure to use IPA dictionary for MeCab'
            assert d.next is None
            self.initialized = True
        line = line.strip()
        sentence = self.tagger.parse(line).strip()
        return sentence

    def signature(self):
        """
        Returns the MeCab parameters.

        :return: signature string
        """
        signature = self.tagger.version() + '-IPA'
        return signature


TOKENIZERS = {'13a':tokenize_13a, 
 'intl':tokenize_v14_international, 
 'zh':tokenize_zh, 
 'ja-mecab':TokenizeMeCab().tokenize, 
 'none':lambda x: x}