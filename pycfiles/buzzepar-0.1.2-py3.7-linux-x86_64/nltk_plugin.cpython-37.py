# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/benepar/nltk_plugin.py
# Compiled at: 2020-05-05 12:30:15
# Size of source mod 2**32: 5131 bytes
import nltk
from nltk import Tree
from .base_parser import BaseParser, IS_PY2, STRING_TYPES, PTB_TOKEN_ESCAPE
TOKENIZER_LOOKUP = {'en':'english', 
 'de':'german', 
 'fr':'french', 
 'pl':'polish', 
 'sv':'swedish'}

class Parser(BaseParser):
    __doc__ = '\n    Berkeley Neural Parser (benepar), integrated with NLTK.\n\n    Sample usage:\n    >>> parser = benepar.Parser("benepar_en")\n    >>> parser.parse("The quick brown fox jumps over the lazy dog.")\n\n    Note that the self-attentive parsing model is only tasked with constructing\n    constituency parse trees from tokenized, untagged, single-sentence inputs.\n    Any other elements of the NLP pipeline (i.e. sentence segmentation,\n    tokenization, and part-of-speech tagging) will be done using the default\n    NLTK models.\n    '

    def __init__(self, name, batch_size=64):
        """
        Load a parsing model given a short model name (e.g. "benepar_en") or a
        filename on disk.

        name (str): Model name, or path to uncompressed TensorFlow model graph
        batch_size (int): Maximum number of sentences to process per batch
        """
        super(Parser, self).__init__(name, batch_size)
        self._tokenizer_lang = TOKENIZER_LOOKUP.get(self._language_code, None)

    def _make_nltk_tree(self, sentence, tags, score, p_i, p_j, p_label):
        last_splits = []
        idx_cell = [
         -1]

        def make_tree():
            idx_cell[0] += 1
            idx = idx_cell[0]
            i, j, label_idx = p_i[idx], p_j[idx], p_label[idx]
            label = self._label_vocab[label_idx]
            if i + 1 >= j:
                if self._provides_tags:
                    word = sentence[i]
                    tag = self._tag_vocab[tags[i]]
                else:
                    word, tag = sentence[i]
                tag = PTB_TOKEN_ESCAPE.get(tag, tag)
                word = PTB_TOKEN_ESCAPE.get(word, word)
                tree = Tree(tag, [word])
                for sublabel in label[::-1]:
                    tree = Tree(sublabel, [tree])

                return [
                 tree]
            left_trees = make_tree()
            right_trees = make_tree()
            children = left_trees + right_trees
            if label:
                tree = Tree(label[(-1)], children)
                for sublabel in reversed(label[:-1]):
                    tree = Tree(sublabel, [tree])

                return [
                 tree]
            return children

        tree = make_tree()[0]
        tree.score = score
        return tree

    def _nltk_process_sents(self, sents):
        for sentence in sents:
            if isinstance(sentence, STRING_TYPES):
                if self._tokenizer_lang is None:
                    raise ValueError('No word tokenizer available for this language. Please tokenize before calling the parser.')
                sentence = nltk.word_tokenize(sentence, self._tokenizer_lang)
            if IS_PY2:
                sentence = [word.decode('utf-8', 'ignore') if isinstance(word, str) else word for word in sentence]
            if not self._provides_tags:
                sentence = nltk.pos_tag(sentence)
                yield ([word for word, tag in sentence], sentence)
            else:
                yield (
                 sentence, sentence)

    def parse(self, sentence):
        """
        Parse a single sentence

        The argument "sentence" can be a list of tokens to be passed to the
        parser. It can also be a string, in which case the sentence will be
        tokenized using the default NLTK tokenizer.

        sentence (str or List[str]): sentence to parse

        Returns: nltk.Tree
        """
        return list(self.parse_sents([sentence]))[0]

    def parse_sents(self, sents):
        """
        Parse multiple sentences

        If "sents" is a string, it will be segmented into sentences using NLTK.
        Otherwise, each element of "sents" will be treated as a sentence.

        sents (str or Iterable[str] or Iterable[List[str]]): sentences to parse

        Returns: Iter[nltk.Tree]
        """
        if isinstance(sents, STRING_TYPES):
            if self._tokenizer_lang is None:
                raise ValueError('No tokenizer available for this language. Please split into individual sentences and tokens before calling the parser.')
            sents = nltk.sent_tokenize(sents, self._tokenizer_lang)
        for parse_raw, tags_raw, sentence in self._batched_parsed_raw(self._nltk_process_sents(sents)):
            yield (self._make_nltk_tree)(sentence, tags_raw, *parse_raw)