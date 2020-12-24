# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mdipierro/make_web2py/web2py/gluon/contrib/minify/jsmin.py
# Compiled at: 2013-10-14 11:16:24
r"""
=====================
 Javascript Minifier
=====================

Javascript Minifier based on `jsmin.c by Douglas Crockford`_\.

This module is a re-implementation based on the semantics of jsmin.c. Usually
it produces the same results. It differs in the following ways:

- there is no error detection: unterminated string, regex and comment
  literals are treated as regular javascript code and minified as such.
- Control characters inside string and regex literals are left untouched; they
  are not converted to spaces (nor to \n)
- Newline characters are not allowed inside string and regex literals, except
  for line continuations in string literals (ECMA-5).
- "return /regex/" is recognized correctly.
- rjsmin does not handle streams, but only complete strings. (However, the
  module provides a "streamy" interface).

Besides the list above it differs from direct python ports of jsmin.c in
speed. Since most parts of the logic are handled by the regex engine it's way
faster than the original python port by Baruch Even. The speed factor varies
between about 6 and 55 depending on input and python version (it gets faster
the more compressed the input already is). Compared to the speed-refactored
python port by Dave St.Germain the performance gain is less dramatic but still
between 1.2 and 7. See the docs/BENCHMARKS file for details.

rjsmin.c is a reimplementation of rjsmin.py in C and speeds it up even more.

Both python 2 and python 3 are supported.

.. _jsmin.c by Douglas Crockford:
   http://www.crockford.com/javascript/jsmin.c

Original author of Python version: Andr\xe9 Malo
Home page: http://opensource.perlig.de/rjsmin/
Modified by Ross Peoples <ross.peoples@gmail.com> for inclusion into web2py.
"""
__author__ = b'Andr\xe9 Malo'
__author__ = getattr(__author__, 'decode', lambda x: __author__)('latin-1')
__docformat__ = 'restructuredtext en'
__license__ = 'Apache License, Version 2.0'
__version__ = '1.0.2'
__all__ = ['jsmin', 'jsmin_for_posers']
import re as _re

def _make_jsmin(extended=True, python_only=True):
    """
    Generate JS minifier based on `jsmin.c by Douglas Crockford`_

    .. _jsmin.c by Douglas Crockford:
       http://www.crockford.com/javascript/jsmin.c

    :Parameters:
      `extended` : ``bool``
        Extended Regexps? (using lookahead and lookbehind). This is faster,
        because it can be optimized way more. The regexps used with `extended`
        being false are only left here to allow easier porting to platforms
        without extended regex features (and for my own reference...)

      `python_only` : ``bool``
        Use only the python variant. If true, the c extension is not even
        tried to be loaded.

    :Return: Minifier
    :Rtype: ``callable``
    """
    if not python_only:
        try:
            import _rjsmin
        except ImportError:
            pass
        else:
            return _rjsmin.jsmin

    try:
        xrange
    except NameError:
        xrange = range

    space_chars = '[\\000-\\011\\013\\014\\016-\\040]'
    line_comment = '(?://[^\\r\\n]*)'
    space_comment = '(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/)'
    string1 = '(?:\\047[^\\047\\\\\\r\\n]*(?:\\\\(?:[^\\r\\n]|\\r?\\n|\\r)[^\\047\\\\\\r\\n]*)*\\047)'
    string2 = '(?:"[^"\\\\\\r\\n]*(?:\\\\(?:[^\\r\\n]|\\r?\\n|\\r)[^"\\\\\\r\\n]*)*")'
    strings = '(?:%s|%s)' % (string1, string2)
    charclass = '(?:\\[[^\\\\\\]\\r\\n]*(?:\\\\[^\\r\\n][^\\\\\\]\\r\\n]*)*\\])'
    nospecial = '[^/\\\\\\[\\r\\n]'
    if extended:
        regex = '(?:/(?![\\r\\n/*])%s*(?:(?:\\\\[^\\r\\n]|%s)%s*)*/)' % (
         nospecial, charclass, nospecial)
    else:
        regex = '(?:/(?:[^*/\\\\\\r\\n\\[]|%s|\\\\[^\\r\\n])%s*(?:(?:\\\\[^\\r\\n]|%s)%s*)*/)'
        regex = regex % (charclass, nospecial, charclass, nospecial)
    space = '(?:%s|%s)' % (space_chars, space_comment)
    newline = '(?:%s?[\\r\\n])' % line_comment

    def fix_charclass(result):
        """ Fixup string of chars to fit into a regex char class """
        pos = result.find('-')
        if pos >= 0:
            result = '%s%s-' % (result[:pos], result[pos + 1:])

        def sequentize(string):
            """
            Notate consecutive characters as sequence

            (1-4 instead of 1234)
            """
            first, last, result = None, None, []
            for char in map(ord, string):
                if last is None:
                    first = last = char
                elif last + 1 == char:
                    last = char
                else:
                    result.append((first, last))
                    first = last = char

            if last is not None:
                result.append((first, last))
            return ('').join([ '%s%s%s' % (chr(first), last > first + 1 and '-' or '', last != first and chr(last) or '') for first, last in result
                             ])

        return _re.sub('([\\000-\\040\\047])', lambda m: '\\%03o' % ord(m.group(1)), sequentize(result).replace('\\', '\\\\').replace('[', '\\[').replace(']', '\\]'))

    def id_literal_(what):
        """ Make id_literal like char class """
        match = _re.compile(what).match
        result = ('').join([ chr(c) for c in xrange(127) if not match(chr(c)) ])
        return '[^%s]' % fix_charclass(result)

    def not_id_literal_(keep):
        """ Make negated id_literal like char class """
        match = _re.compile(id_literal_(keep)).match
        result = ('').join([ chr(c) for c in xrange(127) if not match(chr(c)) ])
        return '[%s]' % fix_charclass(result)

    not_id_literal = not_id_literal_('[a-zA-Z0-9_$]')
    preregex1 = '[(,=:\\[!&|?{};\\r\\n]'
    preregex2 = '%(not_id_literal)sreturn' % locals()
    if extended:
        id_literal = id_literal_('[a-zA-Z0-9_$]')
        id_literal_open = id_literal_('[a-zA-Z0-9_${\\[(+-]')
        id_literal_close = id_literal_('[a-zA-Z0-9_$}\\])"\\047+-]')
        space_sub = _re.compile('([^\\047"/\\000-\\040]+)|(%(strings)s[^\\047"/\\000-\\040]*)|(?:(?<=%(preregex1)s)%(space)s*(%(regex)s[^\\047"/\\000-\\040]*))|(?:(?<=%(preregex2)s)%(space)s*(%(regex)s[^\\047"/\\000-\\040]*))|(?<=%(id_literal_close)s)%(space)s*(?:(%(newline)s)%(space)s*)+(?=%(id_literal_open)s)|(?<=%(id_literal)s)(%(space)s)+(?=%(id_literal)s)|%(space)s+|(?:%(newline)s%(space)s*)+' % locals()).sub

        def space_subber(match):
            """ Substitution callback """
            groups = match.groups()
            if groups[0]:
                return groups[0]
            else:
                if groups[1]:
                    return groups[1]
                if groups[2]:
                    return groups[2]
                if groups[3]:
                    return groups[3]
                if groups[4]:
                    return '\n'
                if groups[5]:
                    return ' '
                return ''

        def jsmin(script):
            r"""
            Minify javascript based on `jsmin.c by Douglas Crockford`_\.

            Instead of parsing the stream char by char, it uses a regular
            expression approach which minifies the whole script with one big
            substitution regex.

            .. _jsmin.c by Douglas Crockford:
               http://www.crockford.com/javascript/jsmin.c

            :Parameters:
              `script` : ``str``
                Script to minify

            :Return: Minified script
            :Rtype: ``str``
            """
            return space_sub(space_subber, '\n%s\n' % script).strip()

    else:
        pre_regex = '(?:%(preregex1)s|%(preregex2)s)' % locals()
        not_id_literal_open = not_id_literal_('[a-zA-Z0-9_${\\[(+-]')
        not_id_literal_close = not_id_literal_('[a-zA-Z0-9_$}\\])"\\047+-]')
        space_norm_sub = _re.compile('(%(strings)s)|(?:(%(pre_regex)s)%(space)s*(%(regex)s))|(%(space)s)+|(?:(%(newline)s)%(space)s*)+' % locals()).sub

        def space_norm_subber(match):
            """ Substitution callback """
            groups = match.groups()
            if groups[0]:
                return groups[0]
            if groups[1]:
                return groups[1].replace('\r', '\n') + groups[2]
            if groups[3]:
                return ' '
            if groups[4]:
                return '\n'

        space_sub1 = _re.compile('[\\040\\n]?(%(strings)s|%(pre_regex)s%(regex)s)|\\040(%(not_id_literal)s)|\\n(%(not_id_literal_open)s)' % locals()).sub

        def space_subber1(match):
            """ Substitution callback """
            groups = match.groups()
            return groups[0] or groups[1] or groups[2]

        space_sub2 = _re.compile('(%(strings)s)\\040?|(%(pre_regex)s%(regex)s)[\\040\\n]?|(%(not_id_literal)s)\\040|(%(not_id_literal_close)s)\\n' % locals()).sub

        def space_subber2(match):
            """ Substitution callback """
            groups = match.groups()
            return groups[0] or groups[1] or groups[2] or groups[3]

        def jsmin(script):
            r"""
            Minify javascript based on `jsmin.c by Douglas Crockford`_\.

            Instead of parsing the stream char by char, it uses a regular
            expression approach. The script is minified with three passes:

            normalization
                Control character are mapped to spaces, spaces and newlines
                are squeezed and comments are stripped.
            space removal 1
                Spaces before certain tokens are removed
            space removal 2
                Spaces after certain tokens are remove

            .. _jsmin.c by Douglas Crockford:
               http://www.crockford.com/javascript/jsmin.c

            :Parameters:
              `script` : ``str``
                Script to minify

            :Return: Minified script
            :Rtype: ``str``
            """
            return space_sub2(space_subber2, space_sub1(space_subber1, space_norm_sub(space_norm_subber, '\n%s\n' % script))).strip()

    return jsmin


jsmin = _make_jsmin()

def jsmin_for_posers(script):
    r"""
    Minify javascript based on `jsmin.c by Douglas Crockford`_\.

    Instead of parsing the stream char by char, it uses a regular
    expression approach which minifies the whole script with one big
    substitution regex.

    .. _jsmin.c by Douglas Crockford:
       http://www.crockford.com/javascript/jsmin.c

    :Warning: This function is the digest of a _make_jsmin() call. It just
              utilizes the resulting regex. It's just for fun here and may
              vanish any time. Use the `jsmin` function instead.

    :Parameters:
      `script` : ``str``
        Script to minify

    :Return: Minified script
    :Rtype: ``str``
    """

    def subber(match):
        """ Substitution callback """
        groups = match.groups()
        return groups[0] or groups[1] or groups[2] or groups[3] or groups[4] and '\n' or groups[5] and ' ' or ''

    return _re.sub('([^\\047"/\\000-\\040]+)|((?:(?:\\047[^\\047\\\\\\r\\n]*(?:\\\\(?:[^\\r\\n]|\\r?\\n|\\r)[^\\047\\\\\\r\\n]*)*\\047)|(?:"[^"\\\\\\r\\n]*(?:\\\\(?:[^\\r\\n]|\\r?\\n|\\r)[^"\\\\\\r\\n]*)*"))[^\\047"/\\000-\\040]*)|(?:(?<=[(,=:\\[!&|?{};\\r\\n])(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))*((?:/(?![\\r\\n/*])[^/\\\\\\[\\r\\n]*(?:(?:\\\\[^\\r\\n]|(?:\\[[^\\\\\\]\\r\\n]*(?:\\\\[^\\r\\n][^\\\\\\]\\r\\n]*)*\\]))[^/\\\\\\[\\r\\n]*)*/)[^\\047"/\\000-\\040]*))|(?:(?<=[\\000-#%-,./:-@\\[-^`{-~-]return)(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))*((?:/(?![\\r\\n/*])[^/\\\\\\[\\r\\n]*(?:(?:\\\\[^\\r\\n]|(?:\\[[^\\\\\\]\\r\\n]*(?:\\\\[^\\r\\n][^\\\\\\]\\r\\n]*)*\\]))[^/\\\\\\[\\r\\n]*)*/)[^\\047"/\\000-\\040]*))|(?<=[^\\000-!#%&(*,./:-@\\[\\\\^`{|~])(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))*(?:((?:(?://[^\\r\\n]*)?[\\r\\n]))(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))*)+(?=[^\\000-#%-\\047)*,./:-@\\\\-^`|-~])|(?<=[^\\000-#%-,./:-@\\[-^`{-~-])((?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/)))+(?=[^\\000-#%-,./:-@\\[-^`{-~-])|(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))+|(?:(?:(?://[^\\r\\n]*)?[\\r\\n])(?:[\\000-\\011\\013\\014\\016-\\040]|(?:/\\*[^*]*\\*+(?:[^/*][^*]*\\*+)*/))*)+', subber, '\n%s\n' % script).strip()


if __name__ == '__main__':
    import sys as _sys
    _sys.stdout.write(jsmin(_sys.stdin.read()))