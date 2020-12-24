# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/mautil/tf_net/bert/tokenization.py
# Compiled at: 2019-07-15 21:40:48
# Size of source mod 2**32: 12257 bytes
"""Tokenization classes."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, re, unicodedata, six, tensorflow as tf

def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
    """Checks whether the casing config is consistent with the checkpoint name."""
    if not init_checkpoint:
        return
    m = re.match('^.*?([A-Za-z0-9_-]+)/bert_model.ckpt', init_checkpoint)
    if m is None:
        return
    model_name = m.group(1)
    lower_models = [
     'uncased_L-24_H-1024_A-16', 'uncased_L-12_H-768_A-12',
     'multilingual_L-12_H-768_A-12', 'chinese_L-12_H-768_A-12']
    cased_models = [
     'cased_L-12_H-768_A-12', 'cased_L-24_H-1024_A-16',
     'multi_cased_L-12_H-768_A-12']
    is_bad_config = False
    if model_name in lower_models and not do_lower_case:
        is_bad_config = True
        actual_flag = 'False'
        case_name = 'lowercased'
        opposite_flag = 'True'
    if model_name in cased_models and do_lower_case:
        is_bad_config = True
        actual_flag = 'True'
        case_name = 'cased'
        opposite_flag = 'False'
    if is_bad_config:
        raise ValueError('You passed in `--do_lower_case=%s` with `--init_checkpoint=%s`. However, `%s` seems to be a %s model, so you should pass in `--do_lower_case=%s` so that the fine-tuning matches how the model was pre-training. If this error is wrong, please just comment out this check.' % (
         actual_flag, init_checkpoint,
         model_name, case_name, opposite_flag))


def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if six.PY3:
        if isinstance(text, str):
            return text
        if isinstance(text, bytes):
            return text.decode('utf-8', 'ignore')
        raise ValueError('Unsupported string type: %s' % type(text))
    else:
        if six.PY2:
            if isinstance(text, str):
                return text.decode('utf-8', 'ignore')
            if isinstance(text, unicode):
                return text
            raise ValueError('Unsupported string type: %s' % type(text))
        else:
            raise ValueError('Not running on Python2 or Python 3?')


def printable_text(text):
    """Returns text encoded in a way suitable for print or `tf.logging`."""
    if six.PY3:
        if isinstance(text, str):
            return text
        if isinstance(text, bytes):
            return text.decode('utf-8', 'ignore')
        raise ValueError('Unsupported string type: %s' % type(text))
    else:
        if six.PY2:
            if isinstance(text, str):
                return text
            if isinstance(text, unicode):
                return text.encode('utf-8')
            raise ValueError('Unsupported string type: %s' % type(text))
        else:
            raise ValueError('Not running on Python2 or Python 3?')


def load_vocab(vocab_file):
    """Loads a vocabulary file into a dictionary."""
    vocab = collections.OrderedDict()
    index = 0
    with tf.gfile.GFile(vocab_file, 'r') as (reader):
        while True:
            token = convert_to_unicode(reader.readline())
            if not token:
                break
            token = token.strip()
            vocab[token] = index
            index += 1

    return vocab


def convert_by_vocab(vocab, items):
    """Converts a sequence of [tokens|ids] using the vocab."""
    output = []
    for item in items:
        output.append(vocab[item])

    return output


def convert_tokens_to_ids(vocab, tokens):
    return convert_by_vocab(vocab, tokens)


def convert_ids_to_tokens(inv_vocab, ids):
    return convert_by_vocab(inv_vocab, ids)


def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


class FullTokenizer(object):
    __doc__ = 'Runs end-to-end tokenziation.'

    def __init__(self, vocab_file, do_lower_case=True):
        self.vocab = load_vocab(vocab_file)
        self.inv_vocab = {v:k for k, v in self.vocab.items()}
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=self.vocab)

    def tokenize(self, text):
        split_tokens = []
        for token in self.basic_tokenizer.tokenize(text):
            for sub_token in self.wordpiece_tokenizer.tokenize(token):
                split_tokens.append(sub_token)

        return split_tokens

    def convert_tokens_to_ids(self, tokens):
        return convert_by_vocab(self.vocab, tokens)

    def convert_ids_to_tokens(self, ids):
        return convert_by_vocab(self.inv_vocab, ids)


class BasicTokenizer(object):
    __doc__ = 'Runs basic tokenization (punctuation splitting, lower casing, etc.).'

    def __init__(self, do_lower_case=True):
        """Constructs a BasicTokenizer.

    Args:
      do_lower_case: Whether to lower case the input.
    """
        self.do_lower_case = do_lower_case

    def tokenize(self, text):
        """Tokenizes a piece of text."""
        text = convert_to_unicode(text)
        text = self._clean_text(text)
        text = self._tokenize_chinese_chars(text)
        orig_tokens = whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                token = token.lower()
                token = self._run_strip_accents(token)
            split_tokens.extend(self._run_split_on_punc(token))

        output_tokens = whitespace_tokenize(' '.join(split_tokens))
        return output_tokens

    def _run_strip_accents(self, text):
        """Strips accents from a piece of text."""
        text = unicodedata.normalize('NFD', text)
        output = []
        for char in text:
            cat = unicodedata.category(char)
            if cat == 'Mn':
                pass
            else:
                output.append(char)

        return ''.join(output)

    def _run_split_on_punc(self, text):
        """Splits punctuation on a piece of text."""
        chars = list(text)
        i = 0
        start_new_word = True
        output = []
        while i < len(chars):
            char = chars[i]
            if _is_punctuation(char):
                output.append([char])
                start_new_word = True
            else:
                if start_new_word:
                    output.append([])
                start_new_word = False
                output[(-1)].append(char)
            i += 1

        return [''.join(x) for x in output]

    def _tokenize_chinese_chars(self, text):
        """Adds whitespace around any CJK character."""
        output = []
        for char in text:
            cp = ord(char)
            if self._is_chinese_char(cp):
                output.append(' ')
                output.append(char)
                output.append(' ')
            else:
                output.append(char)

        return ''.join(output)

    def _is_chinese_char(self, cp):
        """Checks whether CP is the codepoint of a CJK character."""
        if cp >= 19968 and cp <= 40959 or cp >= 13312 and cp <= 19903 or cp >= 131072 and cp <= 173791 or cp >= 173824 and cp <= 177983 or cp >= 177984 and cp <= 178207 or cp >= 178208 and cp <= 183983 or cp >= 63744 and cp <= 64255 or cp >= 194560 and cp <= 195103:
            return True
        return False

    def _clean_text(self, text):
        """Performs invalid character removal and whitespace cleanup on text."""
        output = []
        for char in text:
            cp = ord(char)
            if not cp == 0:
                if not cp == 65533:
                    if _is_control(char):
                        pass
                    else:
                        if _is_whitespace(char):
                            output.append(' ')
                        else:
                            output.append(char)

        return ''.join(output)


class WordpieceTokenizer(object):
    __doc__ = 'Runs WordPiece tokenziation.'

    def __init__(self, vocab, unk_token='[UNK]', max_input_chars_per_word=200):
        self.vocab = vocab
        self.unk_token = unk_token
        self.max_input_chars_per_word = max_input_chars_per_word

    def tokenize(self, text):
        """Tokenizes a piece of text into its word pieces.

    This uses a greedy longest-match-first algorithm to perform tokenization
    using the given vocabulary.

    For example:
      input = "unaffable"
      output = ["un", "##aff", "##able"]

    Args:
      text: A single token or whitespace separated tokens. This should have
        already been passed through `BasicTokenizer.

    Returns:
      A list of wordpiece tokens.
    """
        text = convert_to_unicode(text)
        output_tokens = []
        for token in whitespace_tokenize(text):
            chars = list(token)
            if len(chars) > self.max_input_chars_per_word:
                output_tokens.append(self.unk_token)
                continue
                is_bad = False
                start = 0
                sub_tokens = []
                while start < len(chars):
                    end = len(chars)
                    cur_substr = None
                    while start < end:
                        substr = ''.join(chars[start:end])
                        if start > 0:
                            substr = '##' + substr
                        if substr in self.vocab:
                            cur_substr = substr
                            break
                        end -= 1

                    if cur_substr is None:
                        is_bad = True
                        break
                    sub_tokens.append(cur_substr)
                    start = end

                if is_bad:
                    output_tokens.append(self.unk_token)
                else:
                    output_tokens.extend(sub_tokens)

        return output_tokens


def _is_whitespace(char):
    """Checks whether `chars` is a whitespace character."""
    if char == ' ' or char == '\t' or char == '\n' or char == '\r':
        return True
    cat = unicodedata.category(char)
    if cat == 'Zs':
        return True
    return False


def _is_control(char):
    """Checks whether `chars` is a control character."""
    if char == '\t' or char == '\n' or char == '\r':
        return False
    cat = unicodedata.category(char)
    if cat in ('Cc', 'Cf'):
        return True
    return False


def _is_punctuation(char):
    """Checks whether `chars` is a punctuation character."""
    cp = ord(char)
    if cp >= 33 and cp <= 47 or cp >= 58 and cp <= 64 or cp >= 91 and cp <= 96 or cp >= 123 and cp <= 126:
        return True
    cat = unicodedata.category(char)
    if cat.startswith('P'):
        return True
    return False