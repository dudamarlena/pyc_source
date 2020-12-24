# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/diff.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 4873 bytes
"""
    pygments.lexers.diff
    ~~~~~~~~~~~~~~~~~~~~

    Lexers for diff/patch formats.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups
from pygments.token import Text, Comment, Operator, Keyword, Name, Generic, Literal
__all__ = [
 'DiffLexer', 'DarcsPatchLexer', 'WDiffLexer']

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
        else:
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
    tokens = {'root':[
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
     'comment':[
      (
       '[^\\]].*\\n', Comment),
      (
       '\\]', Operator, '#pop')], 
     'specialText':[
      (
       '\\n', Text, '#pop'),
      (
       '\\[_[^_]*_]', Operator)], 
     'insert':[
      include('specialText'),
      (
       '\\[', Generic.Inserted),
      (
       '[^\\n\\[]+', Generic.Inserted)], 
     'delete':[
      include('specialText'),
      (
       '\\[', Generic.Deleted),
      (
       '[^\\n\\[]+', Generic.Deleted)]}


class WDiffLexer(RegexLexer):
    __doc__ = '\n    A `wdiff <https://www.gnu.org/software/wdiff/>`_ lexer.\n\n    Note that:\n\n    * only to normal output (without option like -l).\n    * if target files of wdiff contain "[-", "-]", "{+", "+}",\n      especially they are unbalanced, this lexer will get confusing.\n\n    .. versionadded:: 2.2\n    '
    name = 'WDiff'
    aliases = ['wdiff']
    filenames = ['*.wdiff']
    mimetypes = []
    flags = re.MULTILINE | re.DOTALL
    ins_op = '\\{\\+'
    ins_cl = '\\+\\}'
    del_op = '\\[\\-'
    del_cl = '\\-\\]'
    normal = '[^{}[\\]+-]+'
    tokens = {'root':[
      (
       ins_op, Generic.Inserted, 'inserted'),
      (
       del_op, Generic.Deleted, 'deleted'),
      (
       normal, Text),
      (
       '.', Text)], 
     'inserted':[
      (
       ins_op, Generic.Inserted, '#push'),
      (
       del_op, Generic.Inserted, '#push'),
      (
       del_cl, Generic.Inserted, '#pop'),
      (
       ins_cl, Generic.Inserted, '#pop'),
      (
       normal, Generic.Inserted),
      (
       '.', Generic.Inserted)], 
     'deleted':[
      (
       del_op, Generic.Deleted, '#push'),
      (
       ins_op, Generic.Deleted, '#push'),
      (
       ins_cl, Generic.Deleted, '#pop'),
      (
       del_cl, Generic.Deleted, '#pop'),
      (
       normal, Generic.Deleted),
      (
       '.', Generic.Deleted)]}