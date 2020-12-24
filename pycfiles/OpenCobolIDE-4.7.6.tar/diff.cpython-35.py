# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/diff.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 3243 bytes
"""
    pygments.lexers.diff
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for diff/patch formats.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, Generic, Literal
__all__ = [
 'DiffLexer', 'DarcsPatchLexer']

class DiffLexer(RegexLexer):
    __doc__ = '\n    Lexer for unified or context-style diffs or patches.\n    '
    name = 'Diff'
    aliases = ['diff', 'udiff']
    filenames = ['*.diff', '*.patch']
    mimetypes = ['text/x-diff', 'text/x-patch']
    tokens = {'root': [
              (
               ' .*\\n', Text),
              (
               '\\+.*\\n', Generic.Inserted),
              (
               '-.*\\n', Generic.Deleted),
              (
               '!.*\\n', Generic.Strong),
              (
               '@.*\\n', Generic.Subheading),
              (
               '([Ii]ndex|diff).*\\n', Generic.Heading),
              (
               '=.*\\n', Generic.Heading),
              (
               '.*\\n', Text)]}

    def analyse_text(text):
        if text[:7] == 'Index: ':
            return True
        if text[:5] == 'diff ':
            return True
        if text[:4] == '--- ':
            return 0.9


class DarcsPatchLexer(RegexLexer):
    __doc__ = '\n    DarcsPatchLexer is a lexer for the various versions of the darcs patch\n    format.  Examples of this format are derived by commands such as\n    ``darcs annotate --patch`` and ``darcs send``.\n\n    .. versionadded:: 0.10\n    '
    name = 'Darcs Patch'
    aliases = ['dpatch']
    filenames = ['*.dpatch', '*.darcspatch']
    DPATCH_KEYWORDS = ('hunk', 'addfile', 'adddir', 'rmfile', 'rmdir', 'move', 'replace')
    tokens = {'root': [
              (
               '<', Operator),
              (
               '>', Operator),
              (
               '\\{', Operator),
              (
               '\\}', Operator),
              (
               '(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)(\\])',
               bygroups(Operator, Keyword, Name, Text, Name, Operator, Literal.Date, Text, Operator)),
              (
               '(\\[)((?:TAG )?)(.*)(\\n)(.*)(\\*\\*)(\\d+)(\\s?)',
               bygroups(Operator, Keyword, Name, Text, Name, Operator, Literal.Date, Text), 'comment'),
              (
               'New patches:', Generic.Heading),
              (
               'Context:', Generic.Heading),
              (
               'Patch bundle hash:', Generic.Heading),
              (
               '(\\s*)(%s)(.*\\n)' % '|'.join(DPATCH_KEYWORDS),
               bygroups(Text, Keyword, Text)),
              (
               '\\+', Generic.Inserted, 'insert'),
              (
               '-', Generic.Deleted, 'delete'),
              (
               '.*\\n', Text)], 
     
     'comment': [
                 (
                  '[^\\]].*\\n', Comment),
                 (
                  '\\]', Operator, '#pop')], 
     
     'specialText': [
                     (
                      '\\n', Text, '#pop'),
                     (
                      '\\[_[^_]*_]', Operator)], 
     
     'insert': [
                include('specialText'),
                (
                 '\\[', Generic.Inserted),
                (
                 '[^\\n\\[]+', Generic.Inserted)], 
     
     'delete': [
                include('specialText'),
                (
                 '\\[', Generic.Deleted),
                (
                 '[^\\n\\[]+', Generic.Deleted)]}