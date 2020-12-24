# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/sjzwind/5829E2A27A97CAA9/PycharmProjects/bert-sent-encoding/bert_sent_encoding/pytorch_pretrained_bert/tokenization.py
# Compiled at: 2019-01-22 06:01:26
# Size of source mod 2**32: 14399 bytes
"""Tokenization classes."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, unicodedata, os, logging
from .file_utils import cached_path
logger = logging.getLogger(__name__)
PRETRAINED_VOCAB_ARCHIVE_MAP = {'bert-base-uncased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-uncased-vocab.txt', 
 'bert-large-uncased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-uncased-vocab.txt', 
 'bert-base-cased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-cased-vocab.txt', 
 'bert-large-cased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-large-cased-vocab.txt', 
 'bert-base-multilingual-uncased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-multilingual-uncased-vocab.txt', 
 'bert-base-multilingual-cased':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-multilingual-cased-vocab.txt', 
 'bert-base-chinese':'https://s3.amazonaws.com/models.huggingface.co/bert/bert-base-chinese-vocab.txt'}
PRETRAINED_VOCAB_POSITIONAL_EMBEDDINGS_SIZE_MAP = {'bert-base-uncased':512, 
 'bert-large-uncased':512, 
 'bert-base-cased':512, 
 'bert-large-cased':512, 
 'bert-base-multilingual-uncased':512, 
 'bert-base-multilingual-cased':512, 
 'bert-base-chinese':512}
VOCAB_NAME = 'vocab.txt'

def load_vocab(vocab_file):
    """Loads a vocabulary file into a dictionary."""
    vocab = collections.OrderedDict()
    index = 0
    with open(vocab_file, 'r', encoding='utf-8') as (reader):
        while True:
            token = reader.readline()
            if not token:
                break
            token = token.strip()
            vocab[token] = index
            index += 1

    return vocab


def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a peice of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


class BertTokenizer(object):
    __doc__ = 'Runs end-to-end tokenization: punctuation splitting + wordpiece'

    def __init__(self, vocab_file, do_lower_case=True, max_len=None, never_split=('[UNK]', '[SEP]', '[PAD]', '[CLS]', '[MASK]')):
        if not os.path.isfile(vocab_file):
            raise ValueError("Can't find a vocabulary file at path '{}'. To load the vocabulary from a Google pretrained model use `tokenizer = BertTokenizer.from_pretrained(PRETRAINED_MODEL_NAME)`".format(vocab_file))
        self.vocab = load_vocab(vocab_file)
        self.ids_to_tokens = collections.OrderedDict([(ids, tok) for tok, ids in self.vocab.items()])
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case, never_split=never_split)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=(self.vocab))
        self.max_len = max_len if max_len is not None else int(1000000000000.0)

    def tokenize(self, text):
        split_tokens = []
        for token in self.basic_tokenizer.tokenize(text):
            for sub_token in self.wordpiece_tokenizer.tokenize(token):
                split_tokens.append(sub_token)

        return split_tokens

    def convert_tokens_to_ids(self, tokens):
        """Converts a sequence of tokens into ids using the vocab."""
        ids = []
        for token in tokens:
            ids.append(self.vocab[token])

        if len(ids) > self.max_len:
            raise ValueError('Token indices sequence length is longer than the specified maximum  sequence length for this BERT model ({} > {}). Running this sequence through BERT will result in indexing errors'.format(len(ids), self.max_len))
        return ids

    def convert_ids_to_tokens(self, ids):
        """Converts a sequence of ids in wordpiece tokens using the vocab."""
        tokens = []
        for i in ids:
            tokens.append(self.ids_to_tokens[i])

        return tokens

    @classmethod
    def from_pretrained(cls, pretrained_model_name, cache_dir=None, *inputs, **kwargs):
        """
        Instantiate a PreTrainedBertModel from a pre-trained model file.
        Download and cache the pre-trained model file if needed.
        """
        if pretrained_model_name in PRETRAINED_VOCAB_ARCHIVE_MAP:
            vocab_file = PRETRAINED_VOCAB_ARCHIVE_MAP[pretrained_model_name]
        else:
            vocab_file = pretrained_model_name
        if os.path.isdir(vocab_file):
            vocab_file = os.path.join(vocab_file, VOCAB_NAME)
        try:
            resolved_vocab_file = cached_path(vocab_file, cache_dir=cache_dir)
        except FileNotFoundError:
            logger.error("Model name '{}' was not found in model name list ({}). We assumed '{}' was a path or url but couldn't find any file associated to this path or url.".format(pretrained_model_name, ', '.join(PRETRAINED_VOCAB_ARCHIVE_MAP.keys()), vocab_file))
            return
        else:
            if resolved_vocab_file == vocab_file:
                logger.info('loading vocabulary file {}'.format(vocab_file))
            else:
                logger.info('loading vocabulary file {} from cache at {}'.format(vocab_file, resolved_vocab_file))
            if pretrained_model_name in PRETRAINED_VOCAB_POSITIONAL_EMBEDDINGS_SIZE_MAP:
                max_len = PRETRAINED_VOCAB_POSITIONAL_EMBEDDINGS_SIZE_MAP[pretrained_model_name]
                kwargs['max_len'] = min(kwargs.get('max_len', int(1000000000000.0)), max_len)
            tokenizer = cls(resolved_vocab_file, *inputs, **kwargs)
            return tokenizer


class BasicTokenizer(object):
    __doc__ = 'Runs basic tokenization (punctuation splitting, lower casing, etc.).'

    def __init__(self, do_lower_case=True, never_split=('[UNK]', '[SEP]', '[PAD]', '[CLS]', '[MASK]')):
        """Constructs a BasicTokenizer.
        Args:
          do_lower_case: Whether to lower case the input.
        """
        self.do_lower_case = do_lower_case
        self.never_split = never_split

    def tokenize(self, text):
        """Tokenizes a piece of text."""
        text = self._clean_text(text)
        text = self._tokenize_chinese_chars(text)
        orig_tokens = whitespace_tokenize(text)
        split_tokens = []
        for token in orig_tokens:
            if self.do_lower_case:
                if token not in self.never_split:
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
                continue
            output.append(char)

        return ''.join(output)

    def _run_split_on_punc(self, text):
        """Splits punctuation on a piece of text."""
        if text in self.never_split:
            return [
             text]
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

    def _is_chinese_char--- This code section failed: ---

 L. 248         0  LOAD_FAST                'cp'
                2  LOAD_CONST               19968
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_FALSE    16  'to 16'
                8  LOAD_FAST                'cp'
               10  LOAD_CONST               40959
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_TRUE    128  'to 128'
             16_0  COME_FROM             6  '6'

 L. 249        16  LOAD_FAST                'cp'
               18  LOAD_CONST               13312
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_FALSE    32  'to 32'
               24  LOAD_FAST                'cp'
               26  LOAD_CONST               19903
               28  COMPARE_OP               <=
               30  POP_JUMP_IF_TRUE    128  'to 128'
             32_0  COME_FROM            22  '22'

 L. 250        32  LOAD_FAST                'cp'
               34  LOAD_CONST               131072
               36  COMPARE_OP               >=
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  LOAD_FAST                'cp'
               42  LOAD_CONST               173791
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_TRUE    128  'to 128'
             48_0  COME_FROM            38  '38'

 L. 251        48  LOAD_FAST                'cp'
               50  LOAD_CONST               173824
               52  COMPARE_OP               >=
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_FAST                'cp'
               58  LOAD_CONST               177983
               60  COMPARE_OP               <=
               62  POP_JUMP_IF_TRUE    128  'to 128'
             64_0  COME_FROM            54  '54'

 L. 252        64  LOAD_FAST                'cp'
               66  LOAD_CONST               177984
               68  COMPARE_OP               >=
               70  POP_JUMP_IF_FALSE    80  'to 80'
               72  LOAD_FAST                'cp'
               74  LOAD_CONST               178207
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_TRUE    128  'to 128'
             80_0  COME_FROM            70  '70'

 L. 253        80  LOAD_FAST                'cp'
               82  LOAD_CONST               178208
               84  COMPARE_OP               >=
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_FAST                'cp'
               90  LOAD_CONST               183983
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_TRUE    128  'to 128'
             96_0  COME_FROM            86  '86'

 L. 254        96  LOAD_FAST                'cp'
               98  LOAD_CONST               63744
              100  COMPARE_OP               >=
              102  POP_JUMP_IF_FALSE   112  'to 112'
              104  LOAD_FAST                'cp'
              106  LOAD_CONST               64255
              108  COMPARE_OP               <=
              110  POP_JUMP_IF_TRUE    128  'to 128'
            112_0  COME_FROM           102  '102'

 L. 255       112  LOAD_FAST                'cp'
              114  LOAD_CONST               194560
              116  COMPARE_OP               >=
              118  POP_JUMP_IF_FALSE   132  'to 132'
              120  LOAD_FAST                'cp'
              122  LOAD_CONST               195103
              124  COMPARE_OP               <=
              126  POP_JUMP_IF_FALSE   132  'to 132'
            128_0  COME_FROM           110  '110'
            128_1  COME_FROM            94  '94'
            128_2  COME_FROM            78  '78'
            128_3  COME_FROM            62  '62'
            128_4  COME_FROM            46  '46'
            128_5  COME_FROM            30  '30'
            128_6  COME_FROM            14  '14'

 L. 256       128  LOAD_CONST               True
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'
            132_1  COME_FROM           118  '118'

 L. 258       132  LOAD_CONST               False
              134  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 132_1

    def _clean_text(self, text):
        """Performs invalid character removal and whitespace cleanup on text."""
        output = []
        for char in text:
            cp = ord(char)
            if not cp == 0:
                if cp == 65533 or _is_control(char):
                    continue
                if _is_whitespace(char):
                    output.append(' ')
                else:
                    output.append(char)

        return ''.join(output)


class WordpieceTokenizer(object):
    __doc__ = 'Runs WordPiece tokenization.'

    def __init__(self, vocab, unk_token='[UNK]', max_input_chars_per_word=100):
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
            already been passed through `BasicTokenizer`.
        Returns:
          A list of wordpiece tokens.
        """
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


def _is_whitespace--- This code section failed: ---

 L. 334         0  LOAD_FAST                'char'
                2  LOAD_STR                 ' '
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_TRUE     32  'to 32'
                8  LOAD_FAST                'char'
               10  LOAD_STR                 '\t'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  LOAD_FAST                'char'
               18  LOAD_STR                 '\n'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'char'
               26  LOAD_STR                 '\r'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'

 L. 335        32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 336        36  LOAD_GLOBAL              unicodedata
               38  LOAD_METHOD              category
               40  LOAD_FAST                'char'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  STORE_FAST               'cat'

 L. 337        46  LOAD_FAST                'cat'
               48  LOAD_STR                 'Zs'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 338        54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 339        58  LOAD_CONST               False
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 60


def _is_control(char):
    """Checks whether `chars` is a control character."""
    if char == '\t' or char == '\n' or char == '\r':
        return False
    cat = unicodedata.category(char)
    if cat.startswith('C'):
        return True
    return False


def _is_punctuation--- This code section failed: ---

 L. 356         0  LOAD_GLOBAL              ord
                2  LOAD_FAST                'char'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'cp'

 L. 361         8  LOAD_FAST                'cp'
               10  LOAD_CONST               33
               12  COMPARE_OP               >=
               14  POP_JUMP_IF_FALSE    24  'to 24'
               16  LOAD_FAST                'cp'
               18  LOAD_CONST               47
               20  COMPARE_OP               <=
               22  POP_JUMP_IF_TRUE     72  'to 72'
             24_0  COME_FROM            14  '14'
               24  LOAD_FAST                'cp'
               26  LOAD_CONST               58
               28  COMPARE_OP               >=
               30  POP_JUMP_IF_FALSE    40  'to 40'
               32  LOAD_FAST                'cp'
               34  LOAD_CONST               64
               36  COMPARE_OP               <=
               38  POP_JUMP_IF_TRUE     72  'to 72'
             40_0  COME_FROM            30  '30'

 L. 362        40  LOAD_FAST                'cp'
               42  LOAD_CONST               91
               44  COMPARE_OP               >=
               46  POP_JUMP_IF_FALSE    56  'to 56'
               48  LOAD_FAST                'cp'
               50  LOAD_CONST               96
               52  COMPARE_OP               <=
               54  POP_JUMP_IF_TRUE     72  'to 72'
             56_0  COME_FROM            46  '46'
               56  LOAD_FAST                'cp'
               58  LOAD_CONST               123
               60  COMPARE_OP               >=
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  LOAD_FAST                'cp'
               66  LOAD_CONST               126
               68  COMPARE_OP               <=
               70  POP_JUMP_IF_FALSE    76  'to 76'
             72_0  COME_FROM            54  '54'
             72_1  COME_FROM            38  '38'
             72_2  COME_FROM            22  '22'

 L. 363        72  LOAD_CONST               True
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            62  '62'

 L. 364        76  LOAD_GLOBAL              unicodedata
               78  LOAD_METHOD              category
               80  LOAD_FAST                'char'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'cat'

 L. 365        86  LOAD_FAST                'cat'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'P'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_JUMP_IF_FALSE   100  'to 100'

 L. 366        96  LOAD_CONST               True
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'

 L. 367       100  LOAD_CONST               False
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 76_1