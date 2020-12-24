# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/pyenv/py3/lib/python3.5/site-packages/mautil/tf_net/bert/tokenization_test.py
# Compiled at: 2019-07-15 21:40:48
# Size of source mod 2**32: 4589 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, tempfile, tokenization, six, tensorflow as tf

class TokenizationTest(tf.test.TestCase):

    def test_full_tokenizer(self):
        vocab_tokens = [
         '[UNK]', '[CLS]', '[SEP]', 'want', '##want', '##ed', 'wa', 'un', 'runn',
         '##ing', ',']
        with tempfile.NamedTemporaryFile(delete=False) as (vocab_writer):
            if six.PY2:
                vocab_writer.write(''.join([x + '\n' for x in vocab_tokens]))
            else:
                vocab_writer.write(''.join([x + '\n' for x in vocab_tokens]).encode('utf-8'))
            vocab_file = vocab_writer.name
        tokenizer = tokenization.FullTokenizer(vocab_file)
        os.unlink(vocab_file)
        tokens = tokenizer.tokenize('UNwantéd,running')
        self.assertAllEqual(tokens, ['un', '##want', '##ed', ',', 'runn', '##ing'])
        self.assertAllEqual(tokenizer.convert_tokens_to_ids(tokens), [7, 4, 5, 10, 8, 9])

    def test_chinese(self):
        tokenizer = tokenization.BasicTokenizer()
        self.assertAllEqual(tokenizer.tokenize('ah博推zz'), [
         'ah', '博', '推', 'zz'])

    def test_basic_tokenizer_lower(self):
        tokenizer = tokenization.BasicTokenizer(do_lower_case=True)
        self.assertAllEqual(tokenizer.tokenize(' \tHeLLo!how  \n Are yoU?  '), [
         'hello', '!', 'how', 'are', 'you', '?'])
        self.assertAllEqual(tokenizer.tokenize('Héllo'), ['hello'])

    def test_basic_tokenizer_no_lower(self):
        tokenizer = tokenization.BasicTokenizer(do_lower_case=False)
        self.assertAllEqual(tokenizer.tokenize(' \tHeLLo!how  \n Are yoU?  '), [
         'HeLLo', '!', 'how', 'Are', 'yoU', '?'])

    def test_wordpiece_tokenizer(self):
        vocab_tokens = [
         '[UNK]', '[CLS]', '[SEP]', 'want', '##want', '##ed', 'wa', 'un', 'runn',
         '##ing']
        vocab = {}
        for i, token in enumerate(vocab_tokens):
            vocab[token] = i

        tokenizer = tokenization.WordpieceTokenizer(vocab=vocab)
        self.assertAllEqual(tokenizer.tokenize(''), [])
        self.assertAllEqual(tokenizer.tokenize('unwanted running'), [
         'un', '##want', '##ed', 'runn', '##ing'])
        self.assertAllEqual(tokenizer.tokenize('unwantedX running'), ['[UNK]', 'runn', '##ing'])

    def test_convert_tokens_to_ids(self):
        vocab_tokens = [
         '[UNK]', '[CLS]', '[SEP]', 'want', '##want', '##ed', 'wa', 'un', 'runn',
         '##ing']
        vocab = {}
        for i, token in enumerate(vocab_tokens):
            vocab[token] = i

        self.assertAllEqual(tokenization.convert_tokens_to_ids(vocab, ['un', '##want', '##ed', 'runn', '##ing']), [7, 4, 5, 8, 9])

    def test_is_whitespace(self):
        self.assertTrue(tokenization._is_whitespace(' '))
        self.assertTrue(tokenization._is_whitespace('\t'))
        self.assertTrue(tokenization._is_whitespace('\r'))
        self.assertTrue(tokenization._is_whitespace('\n'))
        self.assertTrue(tokenization._is_whitespace('\xa0'))
        self.assertFalse(tokenization._is_whitespace('A'))
        self.assertFalse(tokenization._is_whitespace('-'))

    def test_is_control(self):
        self.assertTrue(tokenization._is_control('\x05'))
        self.assertFalse(tokenization._is_control('A'))
        self.assertFalse(tokenization._is_control(' '))
        self.assertFalse(tokenization._is_control('\t'))
        self.assertFalse(tokenization._is_control('\r'))
        self.assertFalse(tokenization._is_control('💩'))

    def test_is_punctuation(self):
        self.assertTrue(tokenization._is_punctuation('-'))
        self.assertTrue(tokenization._is_punctuation('$'))
        self.assertTrue(tokenization._is_punctuation('`'))
        self.assertTrue(tokenization._is_punctuation('.'))
        self.assertFalse(tokenization._is_punctuation('A'))
        self.assertFalse(tokenization._is_punctuation(' '))


if __name__ == '__main__':
    tf.test.main()