# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/kwl2text/l10n.py
# Compiled at: 2016-04-24 12:28:01
import os, sys

def longest_prefix_match(search, urllist):
    matches = [ url for url in urllist if url.startswith(search) ]
    if matches:
        return max(matches, key=len)
    else:
        return ''


def longest_suffix_match(search, urllist):
    matches = [ url for url in urllist if url.endswith(search) ]
    if matches:
        return max(matches, key=len)
    else:
        return ''


def get_word_prefix(word, prefixes=[]):
    key = longest_prefix_match(word[0:2], prefixes.keys())
    try:
        prefix = prefixes[key]
    except KeyError:
        prefix = ''

    return (
     key, prefix)


def get_word_suffix(word, suffixes=[]):
    key = longest_suffix_match(word[-2:0], suffixes.keys())
    try:
        suffix = suffixes[key]
    except KeyError:
        suffix = ''

    return (
     key, suffix)


def plural(grammar, noun, number=2, nclass=None):
    """Return the plural form of this language. noun is a Unicode string."""
    prefix = ''
    suffix = ''
    stem = noun.strip()
    if number == 1:
        return noun
    if grammar.language == 'english':
        pl = '%ss' % stem
        if pl[-4:] == 'tchs':
            suffix = 'es'
        else:
            suffix = 's'
    elif grammar.language == 'akan':
        if ' ' in stem:
            data = stem.split(' ')
            return plural(grammar, data[0], number) + ' ' + plural(grammar, (' ').join(data[1:]), number)
        if stem[0] in ('[', 'l', 'r', 'v', '0', '1', '2', '3', '4', '5', '6', '7',
                       '8', '9'):
            pass
        elif stem[-1:] in 'l':
            pass
        elif stem[-2:] in ('bɔ', 'da', 'kɔ', 'yɛ'):
            pass
        elif stem[-3:] == 'nyi':
            prefix = 'a'
            stem = stem[:-3]
            suffix = 'fo'
        elif stem[0] in ('b', 'f', 'p'):
            prefix = 'm'
        elif stem[0] not in ('n', 'm'):
            prefix = 'n'
        stem = stem.lstrip('aeioɔu')
        pl = '%(prefix)s%(noun)s%(suffix)s' % {'noun': noun.lstrip('aeioɔu'), 'prefix': prefix, 
           'suffix': suffix}
    elif 'plural' in grammar.data:
        try:
            replace, prefix = get_word_prefix(noun, grammar.data['plural']['prefix'])
            stem = noun[len(replace):]
        except (IndexError, KeyError) as e:
            pass

        try:
            replace, suffix = get_word_suffix(noun, grammar.data['plural']['suffix'])
            stem = noun[:len(noun) - len(replace)]
        except (IndexError, KeyError) as e:
            pass

    pl = '%(prefix)s%(stem)s%(suffix)s' % {'prefix': prefix, 'stem': stem, 'suffix': suffix}
    return pl