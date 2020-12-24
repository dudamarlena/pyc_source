# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/lexers/hexdump.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 3507 bytes
"""
    pygments.lexers.hexdump
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for hexadecimal dumps.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Text, Name, Number, String, Punctuation
__all__ = [
 'HexdumpLexer']

class HexdumpLexer(RegexLexer):
    __doc__ = '\n    For typical hex dump output formats by the UNIX and GNU/Linux tools ``hexdump``,\n    ``hd``, ``hexcat``, ``od`` and ``xxd``, and the DOS tool ``DEBUG``. For example:\n\n    .. sourcecode:: hexdump\n\n        00000000  7f 45 4c 46 02 01 01 00  00 00 00 00 00 00 00 00  |.ELF............|\n        00000010  02 00 3e 00 01 00 00 00  c5 48 40 00 00 00 00 00  |..>......H@.....|\n\n    The specific supported formats are the outputs of:\n\n    * ``hexdump FILE``\n    * ``hexdump -C FILE`` -- the `canonical` format used in the example.\n    * ``hd FILE`` -- same as ``hexdump -C FILE``.\n    * ``hexcat FILE``\n    * ``od -t x1z FILE``\n    * ``xxd FILE``\n    * ``DEBUG.EXE FILE.COM`` and entering ``d`` to the prompt.\n\n    .. versionadded:: 2.1\n    '
    name = 'Hexdump'
    aliases = ['hexdump']
    hd = '[0-9A-Ha-h]'
    tokens = {'root':[
      (
       '\\n', Text),
      include('offset'),
      (
       '(' + hd + '{2})(\\-)(' + hd + '{2})',
       bygroups(Number.Hex, Punctuation, Number.Hex)),
      (
       hd + '{2}', Number.Hex),
      (
       '(\\s{2,3})(\\>)(.{16})(\\<)$',
       bygroups(Text, Punctuation, String, Punctuation), 'bracket-strings'),
      (
       '(\\s{2,3})(\\|)(.{16})(\\|)$',
       bygroups(Text, Punctuation, String, Punctuation), 'piped-strings'),
      (
       '(\\s{2,3})(\\>)(.{1,15})(\\<)$',
       bygroups(Text, Punctuation, String, Punctuation)),
      (
       '(\\s{2,3})(\\|)(.{1,15})(\\|)$',
       bygroups(Text, Punctuation, String, Punctuation)),
      (
       '(\\s{2,3})(.{1,15})$', bygroups(Text, String)),
      (
       '(\\s{2,3})(.{16}|.{20})$', bygroups(Text, String), 'nonpiped-strings'),
      (
       '\\s', Text),
      (
       '^\\*', Punctuation)], 
     'offset':[
      (
       '^(' + hd + '+)(:)', bygroups(Name.Label, Punctuation), 'offset-mode'),
      (
       '^' + hd + '+', Name.Label)], 
     'offset-mode':[
      (
       '\\s', Text, '#pop'),
      (
       hd + '+', Name.Label),
      (
       ':', Punctuation)], 
     'piped-strings':[
      (
       '\\n', Text),
      include('offset'),
      (
       hd + '{2}', Number.Hex),
      (
       '(\\s{2,3})(\\|)(.{1,16})(\\|)$',
       bygroups(Text, Punctuation, String, Punctuation)),
      (
       '\\s', Text),
      (
       '^\\*', Punctuation)], 
     'bracket-strings':[
      (
       '\\n', Text),
      include('offset'),
      (
       hd + '{2}', Number.Hex),
      (
       '(\\s{2,3})(\\>)(.{1,16})(\\<)$',
       bygroups(Text, Punctuation, String, Punctuation)),
      (
       '\\s', Text),
      (
       '^\\*', Punctuation)], 
     'nonpiped-strings':[
      (
       '\\n', Text),
      include('offset'),
      (
       '(' + hd + '{2})(\\-)(' + hd + '{2})',
       bygroups(Number.Hex, Punctuation, Number.Hex)),
      (
       hd + '{2}', Number.Hex),
      (
       '(\\s{19,})(.{1,20}?)$', bygroups(Text, String)),
      (
       '(\\s{2,3})(.{1,20})$', bygroups(Text, String)),
      (
       '\\s', Text),
      (
       '^\\*', Punctuation)]}