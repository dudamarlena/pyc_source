# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/inflection/inflection.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 11082 bytes
"""
    inflection
    ~~~~~~~~~~~~

    A port of Ruby on Rails' inflector to Python.

    :copyright: (c) 2012-2015 by Janne Vanhala

    :license: MIT, see LICENSE for more details.
"""
import re, unicodedata
__version__ = '0.3.1'
PLURALS = [
 ('(?i)(quiz)$', '\\1zes'),
 ('(?i)^(oxen)$', '\\1'),
 ('(?i)^(ox)$', '\\1en'),
 ('(?i)(m|l)ice$', '\\1ice'),
 ('(?i)(m|l)ouse$', '\\1ice'),
 ('(?i)(matr|vert|ind)(?:ix|ex)$', '\\1ices'),
 ('(?i)(x|ch|ss|sh)$', '\\1es'),
 ('(?i)([^aeiouy]|qu)y$', '\\1ies'),
 ('(?i)(hive)$', '\\1s'),
 ('(?i)([lr])f$', '\\1ves'),
 ('(?i)([^f])fe$', '\\1ves'),
 ('(?i)sis$', 'ses'),
 ('(?i)([ti])a$', '\\1a'),
 ('(?i)([ti])um$', '\\1a'),
 ('(?i)(buffal|potat|tomat)o$', '\\1oes'),
 ('(?i)(bu)s$', '\\1ses'),
 ('(?i)(alias|status)$', '\\1es'),
 ('(?i)(octop|vir)i$', '\\1i'),
 ('(?i)(octop|vir)us$', '\\1i'),
 ('(?i)^(ax|test)is$', '\\1es'),
 ('(?i)s$', 's'),
 ('$', 's')]
SINGULARS = [
 ('(?i)(database)s$', '\\1'),
 ('(?i)(quiz)zes$', '\\1'),
 ('(?i)(matr)ices$', '\\1ix'),
 ('(?i)(vert|ind)ices$', '\\1ex'),
 ('(?i)^(ox)en', '\\1'),
 ('(?i)(alias|status)(es)?$', '\\1'),
 ('(?i)(octop|vir)(us|i)$', '\\1us'),
 ('(?i)^(a)x[ie]s$', '\\1xis'),
 ('(?i)(cris|test)(is|es)$', '\\1is'),
 ('(?i)(shoe)s$', '\\1'),
 ('(?i)(o)es$', '\\1'),
 ('(?i)(bus)(es)?$', '\\1'),
 ('(?i)(m|l)ice$', '\\1ouse'),
 ('(?i)(x|ch|ss|sh)es$', '\\1'),
 ('(?i)(m)ovies$', '\\1ovie'),
 ('(?i)(s)eries$', '\\1eries'),
 ('(?i)([^aeiouy]|qu)ies$', '\\1y'),
 ('(?i)([lr])ves$', '\\1f'),
 ('(?i)(tive)s$', '\\1'),
 ('(?i)(hive)s$', '\\1'),
 ('(?i)([^f])ves$', '\\1fe'),
 ('(?i)(t)he(sis|ses)$', '\\1hesis'),
 ('(?i)(s)ynop(sis|ses)$', '\\1ynopsis'),
 ('(?i)(p)rogno(sis|ses)$', '\\1rognosis'),
 ('(?i)(p)arenthe(sis|ses)$', '\\1arenthesis'),
 ('(?i)(d)iagno(sis|ses)$', '\\1iagnosis'),
 ('(?i)(b)a(sis|ses)$', '\\1asis'),
 ('(?i)(a)naly(sis|ses)$', '\\1nalysis'),
 ('(?i)([ti])a$', '\\1um'),
 ('(?i)(n)ews$', '\\1ews'),
 ('(?i)(ss)$', '\\1'),
 ('(?i)s$', '')]
UNCOUNTABLES = set([
 'equipment',
 'fish',
 'information',
 'jeans',
 'money',
 'rice',
 'series',
 'sheep',
 'species'])

def _irregular(singular, plural):
    """
    A convenience function to add appropriate rules to plurals and singular
    for irregular words.

    :param singular: irregular word in singular form
    :param plural: irregular word in plural form
    """

    def caseinsensitive(string):
        return ''.join('[' + char + char.upper() + ']' for char in string)

    if singular[0].upper() == plural[0].upper():
        PLURALS.insert(0, (
         '(?i)(%s)%s$' % (singular[0], singular[1:]),
         '\\1' + plural[1:]))
        PLURALS.insert(0, (
         '(?i)(%s)%s$' % (plural[0], plural[1:]),
         '\\1' + plural[1:]))
        SINGULARS.insert(0, (
         '(?i)(%s)%s$' % (plural[0], plural[1:]),
         '\\1' + singular[1:]))
    else:
        PLURALS.insert(0, (
         '%s%s$' % (singular[0].upper(), caseinsensitive(singular[1:])),
         plural[0].upper() + plural[1:]))
        PLURALS.insert(0, (
         '%s%s$' % (singular[0].lower(), caseinsensitive(singular[1:])),
         plural[0].lower() + plural[1:]))
        PLURALS.insert(0, (
         '%s%s$' % (plural[0].upper(), caseinsensitive(plural[1:])),
         plural[0].upper() + plural[1:]))
        PLURALS.insert(0, (
         '%s%s$' % (plural[0].lower(), caseinsensitive(plural[1:])),
         plural[0].lower() + plural[1:]))
        SINGULARS.insert(0, (
         '%s%s$' % (plural[0].upper(), caseinsensitive(plural[1:])),
         singular[0].upper() + singular[1:]))
        SINGULARS.insert(0, (
         '%s%s$' % (plural[0].lower(), caseinsensitive(plural[1:])),
         singular[0].lower() + singular[1:]))


def camelize(string, uppercase_first_letter=True):
    """
    Convert strings to CamelCase.

    Examples::

        >>> camelize("device_type")
        "DeviceType"
        >>> camelize("device_type", False)
        "deviceType"

    :func:`camelize` can be though as a inverse of :func:`underscore`, although
    there are some cases where that does not hold::

        >>> camelize(underscore("IOError"))
        "IoError"

    :param uppercase_first_letter: if set to `True` :func:`camelize` converts
        strings to UpperCamelCase. If set to `False` :func:`camelize` produces
        lowerCamelCase. Defaults to `True`.
    """
    if uppercase_first_letter:
        return re.sub('(?:^|_)(.)', lambda m: m.group(1).upper(), string)
    else:
        return string[0].lower() + camelize(string)[1:]


def dasherize(word):
    """Replace underscores with dashes in the string.

    Example::

        >>> dasherize("puni_puni")
        "puni-puni"

    """
    return word.replace('_', '-')


def humanize(word):
    """
    Capitalize the first word and turn underscores into spaces and strip a
    trailing ``"_id"``, if any. Like :func:`titleize`, this is meant for
    creating pretty output.

    Examples::

        >>> humanize("employee_salary")
        "Employee salary"
        >>> humanize("author_id")
        "Author"

    """
    word = re.sub('_id$', '', word)
    word = word.replace('_', ' ')
    word = re.sub('(?i)([a-z\\d]*)', lambda m: m.group(1).lower(), word)
    word = re.sub('^\\w', lambda m: m.group(0).upper(), word)
    return word


def ordinal(number):
    """
    Return the suffix that should be added to a number to denote the position
    in an ordered sequence such as 1st, 2nd, 3rd, 4th.

    Examples::

        >>> ordinal(1)
        "st"
        >>> ordinal(2)
        "nd"
        >>> ordinal(1002)
        "nd"
        >>> ordinal(1003)
        "rd"
        >>> ordinal(-11)
        "th"
        >>> ordinal(-1021)
        "st"

    """
    number = abs(int(number))
    if number % 100 in (11, 12, 13):
        return 'th'
    else:
        return {1:'st', 
         2:'nd', 
         3:'rd'}.get(number % 10, 'th')


def ordinalize(number):
    """
    Turn a number into an ordinal string used to denote the position in an
    ordered sequence such as 1st, 2nd, 3rd, 4th.

    Examples::

        >>> ordinalize(1)
        "1st"
        >>> ordinalize(2)
        "2nd"
        >>> ordinalize(1002)
        "1002nd"
        >>> ordinalize(1003)
        "1003rd"
        >>> ordinalize(-11)
        "-11th"
        >>> ordinalize(-1021)
        "-1021st"

    """
    return '%s%s' % (number, ordinal(number))


def parameterize(string, separator='-'):
    """
    Replace special characters in a string so that it may be used as part of a
    'pretty' URL.

    Example::

        >>> parameterize(u"Donald E. Knuth")
        'donald-e-knuth'

    """
    string = transliterate(string)
    string = re.sub('(?i)[^a-z0-9\\-_]+', separator, string)
    if separator:
        re_sep = re.escape(separator)
        string = re.sub('%s{2,}' % re_sep, separator, string)
        string = re.sub('(?i)^%(sep)s|%(sep)s$' % {'sep': re_sep}, '', string)
    return string.lower()


def pluralize(word):
    """
    Return the plural form of a word.

    Examples::

        >>> pluralize("post")
        "posts"
        >>> pluralize("octopus")
        "octopi"
        >>> pluralize("sheep")
        "sheep"
        >>> pluralize("CamelOctopus")
        "CamelOctopi"

    """
    if not word or word.lower() in UNCOUNTABLES:
        return word
    else:
        for rule, replacement in PLURALS:
            if re.search(rule, word):
                return re.sub(rule, replacement, word)

        return word


def singularize(word):
    """
    Return the singular form of a word, the reverse of :func:`pluralize`.

    Examples::

        >>> singularize("posts")
        "post"
        >>> singularize("octopi")
        "octopus"
        >>> singularize("sheep")
        "sheep"
        >>> singularize("word")
        "word"
        >>> singularize("CamelOctopi")
        "CamelOctopus"

    """
    for inflection in UNCOUNTABLES:
        if re.search('(?i)\\b(%s)\\Z' % inflection, word):
            return word

    for rule, replacement in SINGULARS:
        if re.search(rule, word):
            return re.sub(rule, replacement, word)

    return word


def tableize(word):
    """
    Create the name of a table like Rails does for models to table names. This
    method uses the :func:`pluralize` method on the last word in the string.

    Examples::

        >>> tableize('RawScaledScorer')
        "raw_scaled_scorers"
        >>> tableize('egg_and_ham')
        "egg_and_hams"
        >>> tableize('fancyCategory')
        "fancy_categories"
    """
    return pluralize(underscore(word))


def titleize(word):
    """
    Capitalize all the words and replace some characters in the string to
    create a nicer looking title. :func:`titleize` is meant for creating pretty
    output.

    Examples::

      >>> titleize("man from the boondocks")
      "Man From The Boondocks"
      >>> titleize("x-men: the last stand")
      "X Men: The Last Stand"
      >>> titleize("TheManWithoutAPast")
      "The Man Without A Past"
      >>> titleize("raiders_of_the_lost_ark")
      "Raiders Of The Lost Ark"

    """
    return re.sub("\\b('?[a-z])", lambda match: match.group(1).capitalize(), humanize(underscore(word)))


def transliterate(string):
    """
    Replace non-ASCII characters with an ASCII approximation. If no
    approximation exists, the non-ASCII character is ignored. The string must
    be ``unicode``.

    Examples::

        >>> transliterate(u'älämölö')
        u'alamolo'
        >>> transliterate(u'Ærøskøbing')
        u'rskbing'

    """
    normalized = unicodedata.normalize('NFKD', string)
    return normalized.encode('ascii', 'ignore').decode('ascii')


def underscore(word):
    """
    Make an underscored, lowercase form from the expression in the string.

    Example::

        >>> underscore("DeviceType")
        "device_type"

    As a rule of thumb you can think of :func:`underscore` as the inverse of
    :func:`camelize`, though there are cases where that does not hold::

        >>> camelize(underscore("IOError"))
        "IoError"

    """
    word = re.sub('([A-Z]+)([A-Z][a-z])', '\\1_\\2', word)
    word = re.sub('([a-z\\d])([A-Z])', '\\1_\\2', word)
    word = word.replace('-', '_')
    return word.lower()


_irregular('person', 'people')
_irregular('man', 'men')
_irregular('human', 'humans')
_irregular('child', 'children')
_irregular('sex', 'sexes')
_irregular('move', 'moves')
_irregular('cow', 'kine')
_irregular('zombie', 'zombies')