# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/language.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import UnicodeMixin, base_text_type, u, s
from guessit.fileutils import load_file_in_same_dir
from guessit.country import Country
import re, logging
__all__ = [
 b'is_iso_language', b'is_language', b'lang_set', b'Language',
 b'ALL_LANGUAGES', b'ALL_LANGUAGES_NAMES', b'UNDETERMINED',
 b'search_language', b'guess_language']
log = logging.getLogger(__name__)
_iso639_contents = load_file_in_same_dir(__file__, b'ISO-639-2_utf-8.txt')
_iso639_contents = _iso639_contents[1:]
language_matrix = [ l.strip().split(b'|') for l in _iso639_contents.strip().split(b'\n')
                  ]
language_matrix += [[b'mol', b'', b'mo', b'Moldavian', b'moldave'],
 [
  b'ass', b'', b'', b'Assyrian', b'assyrien']]
for lang in language_matrix:
    if lang[2] == b'se' or lang[2] == b'br':
        lang[2] = b''
    if lang[0] == b'und':
        lang[2] = b'un'
    if lang[0] == b'srp':
        lang[1] = b'scc'

lng3 = frozenset(l[0] for l in language_matrix if l[0])
lng3term = frozenset(l[1] for l in language_matrix if l[1])
lng2 = frozenset(l[2] for l in language_matrix if l[2])
lng_en_name = frozenset(lng for l in language_matrix for lng in l[3].lower().split(b'; ') if lng)
lng_fr_name = frozenset(lng for l in language_matrix for lng in l[4].lower().split(b'; ') if lng)
lng_all_names = lng3 | lng3term | lng2 | lng_en_name | lng_fr_name
lng3_to_lng3term = dict((l[0], l[1]) for l in language_matrix if l[1])
lng3term_to_lng3 = dict((l[1], l[0]) for l in language_matrix if l[1])
lng3_to_lng2 = dict((l[0], l[2]) for l in language_matrix if l[2])
lng2_to_lng3 = dict((l[2], l[0]) for l in language_matrix if l[2])
lng3_to_lng_en_name = dict((l[0], l[3].split(b'; ')[0]) for l in language_matrix if l[3])
lng_en_name_to_lng3 = dict((en_name.lower(), l[0]) for l in language_matrix if l[3] for en_name in l[3].split(b'; '))
lng3_to_lng_fr_name = dict((l[0], l[4].split(b'; ')[0]) for l in language_matrix if l[4])
lng_fr_name_to_lng3 = dict((fr_name.lower(), l[0]) for l in language_matrix if l[4] for fr_name in l[4].split(b'; '))
lng_exceptions = {b'unknown': ('und', None), b'inconnu': ('und', None), 
   b'unk': ('und', None), 
   b'un': ('und', None), 
   b'gr': ('gre', None), 
   b'greek': ('gre', None), 
   b'esp': ('spa', None), 
   b'español': ('spa', None), 
   b'se': ('swe', None), 
   b'po': ('pt', 'br'), 
   b'pb': ('pt', 'br'), 
   b'pob': ('pt', 'br'), 
   b'br': ('pt', 'br'), 
   b'brazilian': ('pt', 'br'), 
   b'català': ('cat', None), 
   b'cz': ('cze', None), 
   b'ua': ('ukr', None), 
   b'cn': ('chi', None), 
   b'chs': ('chi', None), 
   b'jp': ('jpn', None), 
   b'scr': ('hrv', None)}

def is_iso_language(language):
    return language.lower() in lng_all_names


def is_language(language):
    return is_iso_language(language) or language in lng_exceptions


def lang_set(languages, strict=False):
    """Return a set of guessit.Language created from their given string
    representation.

    if strict is True, then this will raise an exception if any language
    could not be identified.
    """
    return set(Language(l, strict=strict) for l in languages)


class Language(UnicodeMixin):
    """This class represents a human language.

    You can initialize it with pretty much anything, as it knows conversion
    from ISO-639 2-letter and 3-letter codes, English and French names.

    You can also distinguish languages for specific countries, such as
    Portuguese and Brazilian Portuguese.

    There are various properties on the language object that give you the
    representation of the language for a specific usage, such as .alpha3
    to get the ISO 3-letter code, or .opensubtitles to get the OpenSubtitles
    language code.

    >>> Language('fr')
    Language(French)

    >>> s(Language('eng').french_name)
    'anglais'

    >>> s(Language('pt(br)').country.english_name)
    'Brazil'

    >>> s(Language('Español (Latinoamérica)').country.english_name)
    'Latin America'

    >>> Language('Spanish (Latin America)') == Language('Español (Latinoamérica)')
    True

    >>> s(Language('zz', strict=False).english_name)
    'Undetermined'

    >>> s(Language('pt(br)').opensubtitles)
    'pob'
    """
    _with_country_regexp = re.compile(b'(.*)\\((.*)\\)')
    _with_country_regexp2 = re.compile(b'(.*)-(.*)')

    def __init__(self, language, country=None, strict=False, scheme=None):
        language = u(language.strip().lower())
        with_country = Language._with_country_regexp.match(language) or Language._with_country_regexp2.match(language)
        if with_country:
            self.lang = Language(with_country.group(1)).lang
            self.country = Country(with_country.group(2))
            return
        else:
            self.lang = None
            self.country = Country(country) if country else None
            if scheme == b'opensubtitles':
                if language == b'br':
                    self.lang = b'bre'
                    return
                if language == b'se':
                    self.lang = b'sme'
                    return
            elif scheme is not None:
                log.warning(b'Unrecognized scheme: "%s" - Proceeding with standard one' % scheme)
            if len(language) == 2:
                self.lang = lng2_to_lng3.get(language)
            elif len(language) == 3:
                self.lang = language if language in lng3 else lng3term_to_lng3.get(language)
            else:
                self.lang = lng_en_name_to_lng3.get(language) or lng_fr_name_to_lng3.get(language)
            if self.lang is None and language in lng_exceptions:
                lang, country = lng_exceptions[language]
                self.lang = Language(lang).alpha3
                self.country = Country(country) if country else None
            msg = b'The given string "%s" could not be identified as a language' % language
            if self.lang is None and strict:
                raise ValueError(msg)
            if self.lang is None:
                log.debug(msg)
                self.lang = b'und'
            return

    @property
    def alpha2(self):
        return lng3_to_lng2[self.lang]

    @property
    def alpha3(self):
        return self.lang

    @property
    def alpha3term(self):
        return lng3_to_lng3term[self.lang]

    @property
    def english_name(self):
        return lng3_to_lng_en_name[self.lang]

    @property
    def french_name(self):
        return lng3_to_lng_fr_name[self.lang]

    @property
    def opensubtitles(self):
        if self.lang == b'por' and self.country and self.country.alpha2 == b'br':
            return b'pob'
        if self.lang in ('gre', 'srp'):
            return self.alpha3term
        return self.alpha3

    @property
    def tmdb(self):
        if self.country:
            return b'%s-%s' % (self.alpha2, self.country.alpha2.upper())
        return self.alpha2

    def __hash__(self):
        return hash(self.lang)

    def __eq__(self, other):
        if isinstance(other, Language):
            return self.lang == other.lang
        if isinstance(other, base_text_type):
            try:
                return self == Language(other)
            except ValueError:
                return False

        return False

    def __ne__(self, other):
        return not self == other

    def __nonzero__(self):
        return self.lang != b'und'

    def __unicode__(self):
        if self.country:
            return b'%s(%s)' % (self.english_name, self.country.alpha2)
        else:
            return self.english_name

    def __repr__(self):
        if self.country:
            return b'Language(%s, country=%s)' % (self.english_name, self.country)
        else:
            return b'Language(%s)' % self.english_name


UNDETERMINED = Language(b'und')
ALL_LANGUAGES = frozenset(Language(lng) for lng in lng_all_names) - frozenset([UNDETERMINED])
ALL_LANGUAGES_NAMES = lng_all_names

def search_language(string, lang_filter=None):
    """Looks for language patterns, and if found return the language object,
    its group span and an associated confidence.

    you can specify a list of allowed languages using the lang_filter argument,
    as in lang_filter = [ 'fr', 'eng', 'spanish' ]

    >>> search_language('movie [en].avi')
    (Language(English), (7, 9), 0.8)

    >>> search_language('the zen fat cat and the gay mad men got a new fan', lang_filter = ['en', 'fr', 'es'])
    (None, None, None)
    """
    lng_common_words = frozenset([
     b'is', b'it', b'am', b'mad', b'men', b'man', b'run', b'sin', b'st', b'to',
     b'no', b'non', b'war', b'min', b'new', b'car', b'day', b'bad', b'bat', b'fan',
     b'fry', b'cop', b'zen', b'gay', b'fat', b'cherokee', b'got', b'an', b'as',
     b'cat', b'her', b'be', b'hat', b'sun', b'may', b'my', b'mr',
     b'bas', b'de', b'le', b'son', b'vo', b'vf', b'ne', b'ca', b'ce', b'et', b'que',
     b'mal', b'est', b'vol', b'or', b'mon', b'se',
     b'la', b'el', b'del', b'por', b'mar',
     b'ind', b'arw', b'ts', b'ii', b'bin', b'chan', b'ss', b'san', b'oss', b'iii',
     b'vi', b'ben'])
    sep = b'[](){} \\._-+'
    if lang_filter:
        lang_filter = lang_set(lang_filter)
    slow = b' %s ' % string.lower()
    confidence = 1.0
    for lang in lng_all_names:
        if lang in lng_common_words:
            continue
        pos = slow.find(lang)
        if pos != -1:
            end = pos + len(lang)
            if slow[(pos - 1)] not in sep or slow[end] not in sep:
                continue
            language = Language(slow[pos:end])
            if lang_filter and language not in lang_filter:
                continue
            if language.lang not in lng3_to_lng2:
                continue
            if len(lang) == 2:
                confidence = 0.8
            elif len(lang) == 3:
                confidence = 0.9
            else:
                confidence = 0.3
            return (
             language, (pos - 1, end - 1), confidence)

    return (None, None, None)


def guess_language(text):
    """Guess the language in which a body of text is written.

    This uses the external guess-language python module, and will fail and return
    Language(Undetermined) if it is not installed.
    """
    try:
        from guess_language import guessLanguage
        return Language(guessLanguage(text))
    except ImportError:
        log.error(b'Cannot detect the language of the given text body, missing dependency: guess-language')
        log.error(b'Please install it from PyPI, by doing eg: pip install guess-language')
        return UNDETERMINED