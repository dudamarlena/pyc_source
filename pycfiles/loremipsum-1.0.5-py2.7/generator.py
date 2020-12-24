# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/loremipsum/generator.py
# Compiled at: 2014-09-15 11:00:17
"""
This module provides a simple way to generate "Lorem Ipsum" paragraphs,
sentences, or just random words.
"""
from __future__ import unicode_literals
from random import normalvariate, choice
from pkg_resources import resource_string
import math, re, sys
if sys.version_info[0] == 3:
    unicode = str
_SENTENCE_DELIMITERS = [
 b'.', b'?', b'!']
_WORD_DELIMITERS = [
 b','] + _SENTENCE_DELIMITERS
_SAMPLE = resource_string(__name__, b'default/sample.txt')
_DICTIONARY = resource_string(__name__, b'default/dictionary.txt').split()
_LOREM_IPSUM = b'lorem ipsum dolor sit amet, consecteteur adipiscing elit'

def _paragraphs(text):
    """
    Splits a piece of text into paragraphs, separated by empty lines.
    """
    paragraphs = [[]]
    for line in text.splitlines():
        if line.strip():
            paragraphs[(-1)].append(line)
        elif paragraphs[(-1)]:
            paragraphs.append([])

    return [ (b' ').join(lines).strip() for lines in paragraphs ]


def _sentences(text):
    """
    Splits a piece of text into sentences, separated by periods, question
    marks and exclamation marks.
    """
    delimiters = b'[%s]' % (b'').join([ b'\\' + d for d in _SENTENCE_DELIMITERS ])
    sentences = re.split(delimiters, text.strip())
    return [ s.strip() for s in sentences if s.strip() ]


def _mean(values):
    """
    Calculate the mean for a list of integers.
    """
    return sum(values) / float(max(len(values), 1))


def _variance(values):
    """
    Calculate the variance for a list of integers.
    """
    return _mean([ v ** 2 for v in values ]) - _mean(values) ** 2


def _sigma(values):
    """
    Calculate the sigma for a list of integers.
    """
    return math.sqrt(_variance(values))


class DictionaryError(Exception):
    """
    The dictionary must be a list of one or more words.
    """

    def __str__(self):
        return self.__doc__


class SampleError(Exception):
    """
    The sample text must contain one or more empty-line delimited paragraphs,
    and each paragraph must contain one or more period, question mark, or
    exclamation mark delimited sentences.
    """

    def __str__(self):
        return self.__doc__


class Generator(object):
    """
    Generates random strings of "lorem ipsum" text.

    Markov chains are used to generate the random text based on the analysis
    of a sample text. In the analysis, only paragraph, sentence and word
    lengths, and some basic punctuation matter -- the actual words are
    ignored. A provided list of words is then used to generate the random text,
    so that it will have a similar distribution of paragraph, sentence and word
    lengths.

    :param sample: a string containing the sample text
    :type sample: str
    :param dictionary: a string containing a list of words
    :type dictionary: list
    """
    __dictionary = dict()
    __words = list()
    __chains = dict()
    __starts = list()
    __sample = b''
    __sentence_mean = 0
    __sentence_sigma = 0
    __paragraph_mean = 0
    __paragraph_sigma = 0
    __generated_sentence_mean = 0
    __generated_sentence_sigma = 0
    __generated_paragraph_mean = 0
    __generated_paragraph_sigma = 0

    def __init__(self, sample=None, dictionary=None):
        self.sample = unicode(sample or _SAMPLE)
        self.dictionary = dictionary or _DICTIONARY

    def __get_sentence_mean(self):
        """
        A non-negative value determining the mean sentence length (in words)
        of generated sentences. Is changed to match the sample text when the
        sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__sentence_mean

    def __set_sentence_mean(self, mean):
        """
        Set sentence mean.
        """
        if mean < 0:
            raise ValueError(b'Mean sentence length must be non-negative.')
        self.__sentence_mean = mean

    sentence_mean = property(__get_sentence_mean, __set_sentence_mean)

    def __get_sentence_sigma(self):
        """
        A non-negative value determining the standard deviation of sentence
        lengths (in words) of generated sentences. Is changed to match the
        sample text when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__sentence_sigma

    def __set_sentence_sigma(self, sigma):
        """
        Set sentence sigma.
        """
        if sigma < 0:
            raise ValueError(b'Standard deviation of sentence length must be non-negative.')
        self.__sentence_sigma = sigma

    sentence_sigma = property(__get_sentence_sigma, __set_sentence_sigma)

    def __get_paragraph_mean(self):
        """
        A non-negative value determining the mean paragraph length (in
        sentences) of generated sentences. Is changed to match the sample text
        when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__paragraph_mean

    def __set_paragraph_mean(self, mean):
        """
        Set paragraph mean.
        """
        if mean < 0:
            raise ValueError(b'Mean paragraph length must be non-negative.')
        self.__paragraph_mean = mean

    paragraph_mean = property(__get_paragraph_mean, __set_paragraph_mean)

    def __get_paragraph_sigma(self):
        """
        A non-negative value determining the standard deviation of paragraph
        lengths (in sentences) of generated sentences. Is changed to match the
        sample text when the sample text is updated.

        :rtype: int
        :raises: :py:exc:`ValueError` if value is lesser then 0
        """
        return self.__paragraph_sigma

    def __set_paragraph_sigma(self, sigma):
        """
        Set paragraph sigma.
        """
        if sigma < 0:
            raise ValueError(b'Standard deviation of paragraph length must be non-negative.')
        self.__paragraph_sigma = sigma

    paragraph_sigma = property(__get_paragraph_sigma, __set_paragraph_sigma)

    def reset_statistics(self):
        """
        Resets the values of :py:attr:`sentence_mean`,
        :py:attr:`sentence_sigma`, :py:attr:`paragraph_mean`, and
        :py:attr:`paragraph_sigma` to their values as calculated from the
        sample text.
        """
        self.sentence_mean = self.__generated_sentence_mean
        self.sentence_sigma = self.__generated_sentence_sigma
        self.paragraph_mean = self.__generated_paragraph_mean
        self.paragraph_sigma = self.__generated_paragraph_sigma

    def __get_sample(self):
        """
        The sample text that generated sentences are based on.

        Sentences are generated so that they will have a similar distribution
        of word, sentence and paragraph lengths and punctuation.

        Sample text should be a string consisting of a number of paragraphs,
        each separated by empty lines. Each paragraph should consist of a
        number of sentences, separated by periods, exclamation marks and/or
        question marks. Sentences consist of words, separated by white space.

        :param sample: the sample text
        :type sample: str
        :rtype: str
        :raises: :py:exc:`SampleError` if no words in sample text
        """
        return self.__sample

    def __set_sample(self, sample):
        """
        Set sample text.
        """
        words = sample.split()
        previous = (0, 0)
        chains = {}
        starts = [previous]
        for word in words:
            length, delimiter = len(word), b''
            for word_delimiter in _WORD_DELIMITERS:
                if word.endswith(word_delimiter):
                    length, delimiter = length - 1, delimiter
                    break

            if length > 0:
                chains.setdefault(previous, []).append((length, delimiter))
                if delimiter:
                    starts.append(previous)
                previous = (
                 previous[1], length)

        if chains:
            self.__sample = sample
            self.__chains = chains
            self.__starts = starts
            sentences = _sentences(sample)
            sentences_lengths = [ len(s.split()) for s in sentences ]
            self.__generated_sentence_mean = _mean(sentences_lengths)
            self.__generated_sentence_sigma = _sigma(sentences_lengths)
            paragraphs = _paragraphs(sample)
            paragraphs_lengths = [ len(_sentences(p)) for p in paragraphs ]
            self.__generated_paragraph_mean = _mean(paragraphs_lengths)
            self.__generated_paragraph_sigma = _sigma(paragraphs_lengths)
            self.reset_statistics()
        else:
            raise SampleError

    sample = property(__get_sample, __set_sample)

    def __get_dictionary(self):
        """
        A dictionary of words that generated sentences are made of, grouped by
        words length.

        :param words: list of words
        :type words: list
        :rtype: dict
        :raises: :py:exc:`DictionaryError` if no valid words in dictionary
        """
        return self.__dictionary.copy()

    def __set_dictionary(self, words):
        """
        Set dictionary.
        """
        self.__dictionary = dict()
        self.__words = list()
        for word in words:
            try:
                word = unicode(word)
            except TypeError:
                continue
            else:
                self.__dictionary.setdefault(len(word), set()).add(word)
                self.__words.append(word)

        if not (self.__dictionary and self.__words):
            raise DictionaryError

    dictionary = property(__get_dictionary, __set_dictionary)

    @property
    def words(self):
        """
        The plain list of words in the dictionary.
        """
        return self.__words[:]

    def generate_sentence(self, start_with_lorem=False):
        """
        Generates a single sentence, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        mean, sigma = self.sentence_mean, self.sentence_sigma
        sentence_length = max(2, int(round(normalvariate(mean, sigma))))
        words = []
        previous = ()
        last_word = b''
        word_delimiter = b''
        if start_with_lorem:
            words.extend(_LOREM_IPSUM.split()[:sentence_length])
            last_char = words[(-1)][(-1)]
            if last_char in _WORD_DELIMITERS:
                word_delimiter = last_char
        need, more_words = next, iter(range(sentence_length - len(words)))
        while need(more_words, False) is not False:
            if previous not in self.__chains:
                starts = set(self.__starts)
                chains = set(self.__chains.keys())
                previous = choice(list(chains.intersection(starts)))
            chain = choice(self.__chains[previous])
            word_length = chain[0]
            if chain[1] in _SENTENCE_DELIMITERS:
                word_delimiter = b''
            else:
                word_delimiter = chain[1]
            lengths = list(self.__dictionary.keys())
            closest = lengths[0]
            for length in lengths:
                if abs(word_length - length) < abs(word_length - closest):
                    closest = length

            word = choice(list(self.__dictionary[closest]))
            while word == last_word and len(self.__dictionary[closest]) > 1:
                word = choice(list(self.__dictionary[closest]))

            last_word = word
            words.append(word + word_delimiter)
            previous = (previous[1], word_length)

        sentence = (b' ').join(words).capitalize().rstrip(word_delimiter) + b'.'
        return (1, len(words), sentence)

    def generate_sentences(self, amount, start_with_lorem=False):
        """
        Generator method that yields sentences, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        yield self.generate_sentence(start_with_lorem)
        need, more_sentences = next, iter(range(amount - 1))
        while need(more_sentences, False) is not False:
            yield self.generate_sentence()

    def generate_paragraph(self, start_with_lorem=False):
        """
        Generates a single lorem ipsum paragraph, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        mean, sigma = self.paragraph_mean, self.paragraph_sigma
        sentences = max(2, int(round(normalvariate(mean, sigma))))
        words = 0
        paragraph = []
        generator = self.generate_sentences(sentences, start_with_lorem)
        for void, word_count, sentence in generator:
            words += word_count
            paragraph.append(sentence)

        return (
         sentences, words, (b' ').join(paragraph))

    def generate_paragraphs(self, amount, start_with_lorem=False):
        """
        Generator method that yields paragraphs, of random length.

        :param start_with_lorem: if True, then the text will begin with the
                                 standard "Lorem ipsum..." first sentence.
        :type start_with_lorem: bool
        """
        yield self.generate_paragraph(start_with_lorem)
        need, more_paragraphs = next, iter(range(amount - 1))
        while need(more_paragraphs, False) is not False:
            yield self.generate_paragraph()