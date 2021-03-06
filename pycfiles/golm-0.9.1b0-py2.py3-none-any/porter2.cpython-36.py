# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/nlp/tools/porter2.py
# Compiled at: 2018-04-15 14:00:29
# Size of source mod 2**32: 11553 bytes
"""pyporter2: An implementation of the Porter2 stemming algorithm.

See http://snowball.tartarus.org/algorithms/english/stemmer.html"""
import re
regexp = re.compile('[^aeiouy]*[aeiouy]+[^aeiouy](\\w*)')

def get_r1(word):
    if word.startswith('gener') or word.startswith('arsen'):
        return 5
    else:
        if word.startswith('commun'):
            return 6
        match = regexp.match(word)
        if match:
            return match.start(1)
        return len(word)


def get_r2(word):
    match = regexp.match(word, get_r1(word))
    if match:
        return match.start(1)
    else:
        return len(word)


def ends_with_short_syllable(word):
    if len(word) == 2:
        if re.match('^[aeiouy][^aeiouy]$', word):
            return True
    if re.match('.*[^aeiouy][aeiouy][^aeiouywxY]$', word):
        return True
    else:
        return False


def is_short_word(word):
    if ends_with_short_syllable(word):
        if get_r1(word) == len(word):
            return True
    return False


def remove_initial_apostrophe(word):
    if word.startswith("'"):
        return word[1:]
    else:
        return word


def capitalize_consonant_ys(word):
    if word.startswith('y'):
        word = 'Y' + word[1:]
    return re.sub('([aeiouy])y', '\\g<1>Y', word)


def step_0(word):
    if word.endswith("'s'"):
        return word[:-3]
    else:
        if word.endswith("'s"):
            return word[:-2]
        if word.endswith("'"):
            return word[:-1]
        return word


def step_1a(word):
    if word.endswith('sses'):
        return word[:-4] + 'ss'
    else:
        if word.endswith('ied') or word.endswith('ies'):
            if len(word) > 4:
                return word[:-3] + 'i'
            else:
                return word[:-3] + 'ie'
        else:
            if word.endswith('us') or word.endswith('ss'):
                return word
            if word.endswith('s'):
                preceding = word[:-1]
                if re.search('[aeiouy].', preceding):
                    return preceding
                else:
                    return word
        return word


def step_1b(word, r1):
    if word.endswith('eedly'):
        if len(word) - 5 >= r1:
            return word[:-3]
        return word
    else:
        if word.endswith('eed'):
            if len(word) - 3 >= r1:
                return word[:-1]
            else:
                return word

        def ends_with_double(word):
            doubles = [
             'bb', 'dd', 'ff', 'gg', 'mm', 'nn', 'pp', 'rr', 'tt']
            for double in doubles:
                if word.endswith(double):
                    return True

            return False

        def step_1b_helper(word):
            if word.endswith('at') or word.endswith('bl') or word.endswith('iz'):
                return word + 'e'
            else:
                if ends_with_double(word):
                    return word[:-1]
                if is_short_word(word):
                    return word + 'e'
                return word

        suffixes = ['ed', 'edly', 'ing', 'ingly']
        for suffix in suffixes:
            if word.endswith(suffix):
                preceding = word[:-len(suffix)]
                if re.search('[aeiouy]', preceding):
                    return step_1b_helper(preceding)
                else:
                    return word

        return word


def step_1c(word):
    if word.endswith('y') or word.endswith('Y'):
        if word[(-2)] not in 'aeiouy':
            if len(word) > 2:
                return word[:-1] + 'i'
    return word


def step_2(word, r1):

    def step_2_helper(end, repl, prev):
        if word.endswith(end):
            if len(word) - len(end) >= r1:
                if prev == []:
                    return word[:-len(end)] + repl
                for p in prev:
                    if word[:-len(end)].endswith(p):
                        return word[:-len(end)] + repl

            return word

    triples = [
     (
      'ization', 'ize', []),
     (
      'ational', 'ate', []),
     (
      'fulness', 'ful', []),
     (
      'ousness', 'ous', []),
     (
      'iveness', 'ive', []),
     (
      'tional', 'tion', []),
     (
      'biliti', 'ble', []),
     (
      'lessli', 'less', []),
     (
      'entli', 'ent', []),
     (
      'ation', 'ate', []),
     (
      'alism', 'al', []),
     (
      'aliti', 'al', []),
     (
      'ousli', 'ous', []),
     (
      'iviti', 'ive', []),
     (
      'fulli', 'ful', []),
     (
      'enci', 'ence', []),
     (
      'anci', 'ance', []),
     (
      'abli', 'able', []),
     (
      'izer', 'ize', []),
     (
      'ator', 'ate', []),
     (
      'alli', 'al', []),
     (
      'bli', 'ble', []),
     (
      'ogi', 'og', ['l']),
     (
      'li', '', ['c', 'd', 'e', 'g', 'h', 'k', 'm', 'n', 'r', 't'])]
    for trip in triples:
        attempt = step_2_helper(trip[0], trip[1], trip[2])
        if attempt:
            return attempt

    return word


def step_3(word, r1, r2):

    def step_3_helper(end, repl, r2_necessary):
        if word.endswith(end):
            if len(word) - len(end) >= r1:
                return r2_necessary or word[:-len(end)] + repl
            else:
                if len(word) - len(end) >= r2:
                    return word[:-len(end)] + repl
                return word

    triples = [('ational', 'ate', False),
     ('tional', 'tion', False),
     ('alize', 'al', False),
     ('icate', 'ic', False),
     ('iciti', 'ic', False),
     ('ative', '', True),
     ('ical', 'ic', False),
     ('ness', '', False),
     ('ful', '', False)]
    for trip in triples:
        attempt = step_3_helper(trip[0], trip[1], trip[2])
        if attempt:
            return attempt

    return word


def step_4(word, r2):
    delete_list = [
     'al', 'ance', 'ence', 'er', 'ic', 'able', 'ible', 'ant', 'ement', 'ment', 'ent', 'ism', 'ate', 'iti',
     'ous', 'ive', 'ize']
    for end in delete_list:
        if word.endswith(end):
            if len(word) - len(end) >= r2:
                return word[:-len(end)]
            else:
                return word

    if word.endswith('sion') or word.endswith('tion'):
        if len(word) - 3 >= r2:
            return word[:-3]
    return word


def step_5(word, r1, r2):
    if word.endswith('l'):
        if len(word) - 1 >= r2:
            if word[(-2)] == 'l':
                return word[:-1]
        return word
    else:
        if word.endswith('e'):
            if len(word) - 1 >= r2:
                return word[:-1]
            if len(word) - 1 >= r1:
                if not ends_with_short_syllable(word[:-1]):
                    return word[:-1]
        return word


def normalize_ys(word):
    return word.replace('Y', 'y')


exceptional_forms = {'skis':'ski', 
 'skies':'sky', 
 'dying':'die', 
 'lying':'lie', 
 'tying':'tie', 
 'idly':'idl', 
 'gently':'gentl', 
 'ugly':'ugli', 
 'early':'earli', 
 'only':'onli', 
 'singly':'singl', 
 'sky':'sky', 
 'news':'news', 
 'howe':'howe', 
 'atlas':'atlas', 
 'cosmos':'cosmos', 
 'bias':'bias', 
 'andes':'andes'}
exceptional_early_exit_post_1a = [
 'inning', 'outing', 'canning', 'herring', 'earring', 'proceed', 'exceed', 'succeed']

def stem(word):
    """The main entry point in the old version of the API."""
    raise DeprecationWarning('stem() is deprecated starting with v1.0.0')


def algorithms():
    """Get a list of the names of the available stemming algorithms.

    The only algorithm currently supported is the "english", or porter2,
    algorithm.
    """
    return [
     'english']


def version():
    """Get the version number of the stemming module.

    This is the version number of the Stemmer module as a whole (not for an
    individual algorithm).
    """
    return '1.0.0'


class Stemmer:
    __doc__ = 'An instance of a stemming algorithm.\n\n    When creating a Stemmer object, there is one required argument:\n    the name of the algorithm to use in the new stemmer. A list of the\n    valid algorithm names may be obtained by calling the algorithms()\n    function in this module. In addition, the appropriate stemming algorithm\n    for a given language may be obtained by using the 2 or 3 letter ISO 639\n    language codes.\n    '
    max_cache_size = 10000

    def __init__(self, algorithm, cache_size=None):
        if algorithm not in ('english', 'eng', 'en'):
            raise KeyError("Stemming algorithm '%s' not found" % algorithm)
        if cache_size:
            self.max_cache_size = cache_size

    def stemWord(self, word):
        """Stem a word.

        This takes a single argument, word, which should either be a UTF-8
        encoded string, or a unicode object.

        The result is the stemmed form of the word. If the word supplied
        was a unicode object, the result will be a unicode object: if the
        word supplied was a string, the result will be a UTF-8 encoded string.
        """
        return Stemmer._stem(word)

    def stemWords(self, words):
        """Stem a list of words.

        This takes a single argument, words, which must be a sequence,
        iterator, generator or similar.

        The entries in words should either be UTF-8 encoded strings,
        or a unicode objects.

        The result is a list of the stemmed forms of the words. If the word
        supplied was a unicode object, the stemmed form will be a unicode
        object: if the word supplied was a string, the stemmed form will
        be a UTF-8 encoded string.
        """
        return [self.stemWord(word) for word in words]

    @classmethod
    def _stem(cls, word):
        if len(word) <= 2:
            return word
        else:
            word = remove_initial_apostrophe(word)
            if word in exceptional_forms:
                return exceptional_forms[word]
            word = capitalize_consonant_ys(word)
            r1 = get_r1(word)
            r2 = get_r2(word)
            word = step_0(word)
            word = step_1a(word)
            if word in exceptional_early_exit_post_1a:
                return word
            word = step_1b(word, r1)
            word = step_1c(word)
            word = step_2(word, r1)
            word = step_3(word, r1, r2)
            word = step_4(word, r2)
            word = step_5(word, r1, r2)
            word = normalize_ys(word)
            return word