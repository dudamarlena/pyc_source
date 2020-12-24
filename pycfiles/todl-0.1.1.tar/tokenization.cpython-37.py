# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/bert/tokenization.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 16775 bytes
"""Tokenization classes implementation.

The file is forked from:
https://github.com/google-research/bert/blob/master/tokenization.py.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, re, unicodedata, six, tensorflow as tf, sentencepiece as spm
SPIECE_UNDERLINE = '▁'

def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
    """Checks whether the casing config is consistent with the checkpoint name."""
    if not init_checkpoint:
        return
        m = re.match('^.*?([A-Za-z0-9_-]+)/bert_model.ckpt', init_checkpoint)
        if m is None:
            return
    else:
        model_name = m.group(1)
        lower_models = [
         'uncased_L-24_H-1024_A-16', 'uncased_L-12_H-768_A-12',
         'multilingual_L-12_H-768_A-12', 'chinese_L-12_H-768_A-12']
        cased_models = [
         'cased_L-12_H-768_A-12', 'cased_L-24_H-1024_A-16',
         'multi_cased_L-12_H-768_A-12']
        is_bad_config = False
        if model_name in lower_models:
            if not do_lower_case:
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
         actual_flag, init_checkpoint, model_name, case_name, opposite_flag))


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
    with tf.io.gfile.GFile(vocab_file, 'r') as (reader):
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

    def __init__(self, vocab_file, do_lower_case=True, split_on_punc=True):
        self.vocab = load_vocab(vocab_file)
        self.inv_vocab = {v:k for k, v in self.vocab.items()}
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case,
          split_on_punc=split_on_punc)
        self.wordpiece_tokenizer = WordpieceTokenizer(vocab=(self.vocab))

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

    def __init__(self, do_lower_case=True, split_on_punc=True):
        """Constructs a BasicTokenizer.

    Args:
      do_lower_case: Whether to lower case the input.
      split_on_punc: Whether to apply split on punctuations. By default BERT
        starts a new token for punctuations. This makes detokenization difficult
        for tasks like seq2seq decoding.
    """
        self.do_lower_case = do_lower_case
        self.split_on_punc = split_on_punc

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
            if self.split_on_punc:
                split_tokens.extend(self._run_split_on_punc(token))
            else:
                split_tokens.append(token)

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

 L. 292         0  LOAD_FAST                'cp'
                2  LOAD_CONST               19968
                4  COMPARE_OP               >=
                6  POP_JUMP_IF_FALSE    16  'to 16'
                8  LOAD_FAST                'cp'
               10  LOAD_CONST               40959
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_TRUE    128  'to 128'
             16_0  COME_FROM             6  '6'

 L. 293        16  LOAD_FAST                'cp'
               18  LOAD_CONST               13312
               20  COMPARE_OP               >=
               22  POP_JUMP_IF_FALSE    32  'to 32'
               24  LOAD_FAST                'cp'
               26  LOAD_CONST               19903
               28  COMPARE_OP               <=
               30  POP_JUMP_IF_TRUE    128  'to 128'
             32_0  COME_FROM            22  '22'

 L. 294        32  LOAD_FAST                'cp'
               34  LOAD_CONST               131072
               36  COMPARE_OP               >=
               38  POP_JUMP_IF_FALSE    48  'to 48'
               40  LOAD_FAST                'cp'
               42  LOAD_CONST               173791
               44  COMPARE_OP               <=
               46  POP_JUMP_IF_TRUE    128  'to 128'
             48_0  COME_FROM            38  '38'

 L. 295        48  LOAD_FAST                'cp'
               50  LOAD_CONST               173824
               52  COMPARE_OP               >=
               54  POP_JUMP_IF_FALSE    64  'to 64'
               56  LOAD_FAST                'cp'
               58  LOAD_CONST               177983
               60  COMPARE_OP               <=
               62  POP_JUMP_IF_TRUE    128  'to 128'
             64_0  COME_FROM            54  '54'

 L. 296        64  LOAD_FAST                'cp'
               66  LOAD_CONST               177984
               68  COMPARE_OP               >=
               70  POP_JUMP_IF_FALSE    80  'to 80'
               72  LOAD_FAST                'cp'
               74  LOAD_CONST               178207
               76  COMPARE_OP               <=
               78  POP_JUMP_IF_TRUE    128  'to 128'
             80_0  COME_FROM            70  '70'

 L. 297        80  LOAD_FAST                'cp'
               82  LOAD_CONST               178208
               84  COMPARE_OP               >=
               86  POP_JUMP_IF_FALSE    96  'to 96'
               88  LOAD_FAST                'cp'
               90  LOAD_CONST               183983
               92  COMPARE_OP               <=
               94  POP_JUMP_IF_TRUE    128  'to 128'
             96_0  COME_FROM            86  '86'

 L. 298        96  LOAD_FAST                'cp'
               98  LOAD_CONST               63744
              100  COMPARE_OP               >=
              102  POP_JUMP_IF_FALSE   112  'to 112'
              104  LOAD_FAST                'cp'
              106  LOAD_CONST               64255
              108  COMPARE_OP               <=
              110  POP_JUMP_IF_TRUE    128  'to 128'
            112_0  COME_FROM           102  '102'

 L. 299       112  LOAD_FAST                'cp'
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

 L. 300       128  LOAD_CONST               True
              130  RETURN_VALUE     
            132_0  COME_FROM           126  '126'
            132_1  COME_FROM           118  '118'

 L. 302       132  LOAD_CONST               False
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


def _is_whitespace--- This code section failed: ---

 L. 384         0  LOAD_FAST                'char'
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

 L. 385        32  LOAD_CONST               True
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L. 386        36  LOAD_GLOBAL              unicodedata
               38  LOAD_METHOD              category
               40  LOAD_FAST                'char'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  STORE_FAST               'cat'

 L. 387        46  LOAD_FAST                'cat'
               48  LOAD_STR                 'Zs'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    58  'to 58'

 L. 388        54  LOAD_CONST               True
               56  RETURN_VALUE     
             58_0  COME_FROM            52  '52'

 L. 389        58  LOAD_CONST               False
               60  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 60


def _is_control(char):
    """Checks whether `chars` is a control character."""
    if char == '\t' or char == '\n' or char == '\r':
        return False
    cat = unicodedata.category(char)
    if cat in ('Cc', 'Cf'):
        return True
    return False


def _is_punctuation--- This code section failed: ---

 L. 406         0  LOAD_GLOBAL              ord
                2  LOAD_FAST                'char'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  STORE_FAST               'cp'

 L. 411         8  LOAD_FAST                'cp'
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

 L. 412        40  LOAD_FAST                'cp'
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

 L. 413        72  LOAD_CONST               True
               74  RETURN_VALUE     
             76_0  COME_FROM            70  '70'
             76_1  COME_FROM            62  '62'

 L. 414        76  LOAD_GLOBAL              unicodedata
               78  LOAD_METHOD              category
               80  LOAD_FAST                'char'
               82  CALL_METHOD_1         1  '1 positional argument'
               84  STORE_FAST               'cat'

 L. 415        86  LOAD_FAST                'cat'
               88  LOAD_METHOD              startswith
               90  LOAD_STR                 'P'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  POP_JUMP_IF_FALSE   100  'to 100'

 L. 416        96  LOAD_CONST               True
               98  RETURN_VALUE     
            100_0  COME_FROM            94  '94'

 L. 417       100  LOAD_CONST               False
              102  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 76_1


def preprocess_text(inputs, remove_space=True, lower=False):
    """Preprocesses data by removing extra space and normalize data.

  This method is used together with sentence piece tokenizer and is forked from:
  https://github.com/google-research/google-research/blob/master/albert/tokenization.py

  Args:
    inputs: The input text.
    remove_space: Whether to remove the extra space.
    lower: Whether to lowercase the text.

  Returns:
    The preprocessed text.

  """
    outputs = inputs
    if remove_space:
        outputs = ' '.join(inputs.strip().split())
    if six.PY2:
        if isinstance(outputs, str):
            try:
                outputs = six.ensure_text(outputs, 'utf-8')
            except UnicodeDecodeError:
                outputs = six.ensure_text(outputs, 'latin-1')

    outputs = unicodedata.normalize('NFKD', outputs)
    outputs = ''.join([c for c in outputs if not unicodedata.combining(c)])
    if lower:
        outputs = outputs.lower()
    return outputs


def encode_pieces(sp_model, text, sample=False):
    """Segements text into pieces.

  This method is used together with sentence piece tokenizer and is forked from:
  https://github.com/google-research/google-research/blob/master/albert/tokenization.py

  Args:
    sp_model: A spm.SentencePieceProcessor object.
    text: The input text to be segemented.
    sample: Whether to randomly sample a segmentation output or return a
      deterministic one.

  Returns:
    A list of token pieces.
  """
    if six.PY2:
        if isinstance(text, six.text_type):
            text = six.ensure_binary(text, 'utf-8')
    elif not sample:
        pieces = sp_model.EncodeAsPieces(text)
    else:
        pieces = sp_model.SampleEncodeAsPieces(text, 64, 0.1)
    new_pieces = []
    for piece in pieces:
        piece = printable_text(piece)
        if len(piece) > 1:
            if piece[(-1)] == ',' and piece[(-2)].isdigit():
                cur_pieces = sp_model.EncodeAsPieces(piece[:-1].replace(SPIECE_UNDERLINE, ''))
                if piece[0] != SPIECE_UNDERLINE and cur_pieces[0][0] == SPIECE_UNDERLINE:
                    if len(cur_pieces[0]) == 1:
                        cur_pieces = cur_pieces[1:]
            else:
                cur_pieces[0] = cur_pieces[0][1:]
            cur_pieces.append(piece[(-1)])
            new_pieces.extend(cur_pieces)
        else:
            new_pieces.append(piece)

    return new_pieces


def encode_ids(sp_model, text, sample=False):
    """Segments text and return token ids.

  This method is used together with sentence piece tokenizer and is forked from:
  https://github.com/google-research/google-research/blob/master/albert/tokenization.py

  Args:
    sp_model: A spm.SentencePieceProcessor object.
    text: The input text to be segemented.
    sample: Whether to randomly sample a segmentation output or return a
      deterministic one.

  Returns:
    A list of token ids.
  """
    pieces = encode_pieces(sp_model, text, sample=sample)
    ids = [sp_model.PieceToId(piece) for piece in pieces]
    return ids


class FullSentencePieceTokenizer(object):
    __doc__ = 'Runs end-to-end sentence piece tokenization.\n\n  The interface of this class is intended to keep the same as above\n  `FullTokenizer` class for easier usage.\n  '

    def __init__(self, sp_model_file):
        """Inits FullSentencePieceTokenizer.

    Args:
      sp_model_file: The path to the sentence piece model file.
    """
        self.sp_model = spm.SentencePieceProcessor()
        self.sp_model.Load(sp_model_file)
        self.vocab = {self.sp_model.IdToPiece(i):i for i in six.moves.range(self.sp_model.GetPieceSize())}

    def tokenize(self, text):
        """Tokenizes text into pieces."""
        return encode_pieces(self.sp_model, text)

    def convert_tokens_to_ids(self, tokens):
        """Converts a list of tokens to a list of ids."""
        return [self.sp_model.PieceToId(printable_text(token)) for token in tokens]

    def convert_ids_to_tokens(self, ids):
        """Converts a list of ids ot a list of tokens."""
        return [self.sp_model.IdToPiece(id_) for id_ in ids]