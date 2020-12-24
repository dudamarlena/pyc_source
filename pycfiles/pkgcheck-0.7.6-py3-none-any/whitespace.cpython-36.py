# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/whitespace.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 5450 bytes
import re, sys
from typing import NamedTuple
from snakeoil.demandload import demand_compile_regexp
from snakeoil.strings import pluralism
from .. import results, sources
from . import Check
demand_compile_regexp('indent_regexp', '^\t* \t+')

class _Whitespace(results.VersionResult, results.Warning):

    @property
    def lines_str(self):
        s = pluralism(self.lines)
        lines = ', '.join(map(str, self.lines))
        return f"line{s}: {lines}"


class WhitespaceFound(_Whitespace):
    __doc__ = 'Leading or trailing whitespace found.'

    def __init__(self, leadtrail, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.lines = tuple(lines)
        self.leadtrail = leadtrail

    @property
    def desc(self):
        return f"ebuild has {self.leadtrail} whitespace on {self.lines_str}"


class WrongIndentFound(_Whitespace):
    __doc__ = 'Incorrect indentation whitespace found.'

    def __init__(self, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.lines = tuple(lines)

    @property
    def desc(self):
        return f"ebuild has whitespace in indentation on {self.lines_str}"


class DoubleEmptyLine(_Whitespace):
    __doc__ = 'Unneeded blank lines found.'

    def __init__(self, lines, **kwargs):
        (super().__init__)(**kwargs)
        self.lines = tuple(lines)

    @property
    def desc(self):
        return f"ebuild has unneeded empty {self.lines_str}"


class TrailingEmptyLine(results.VersionResult, results.Warning):
    __doc__ = 'Unneeded trailing blank lines found.'
    desc = 'ebuild has trailing blank line(s)'


class NoFinalNewline(results.VersionResult, results.Warning):
    __doc__ = "Ebuild's last line does not have a final newline."
    desc = 'ebuild lacks an ending newline'


class BadWhitespaceCharacter(results.LineResult, results.Warning):
    __doc__ = "Ebuild uses whitespace that isn't a tab, newline, or single space.\n\n    Bash does not treat unicode whitespace characters as regular whitespace so\n    commands or operators separated by such characters will be treated as one\n    string. This usually causes execution errors if the characters are used for\n    separation purposes outside of comments or regular strings.\n    "

    def __init__(self, char, position, **kwargs):
        (super().__init__)(**kwargs)
        self.char = char
        self.position = position

    @property
    def desc(self):
        return f"bad whitespace character {self.char} on line {self.lineno}, char {self.position}: {self.line}"


class WhitespaceData(NamedTuple):
    __doc__ = 'Data format to register hardcoded list of bad whitespace characters.'
    unicode_version: str
    chars: tuple


whitespace_data = WhitespaceData(unicode_version='12.1.0',
  chars=('\x0b', '\x0c', '\r', '\x1c', '\x1d', '\x1e', '\x1f', '\x85', '\xa0', '\u1680',
         '\u2000', '\u2001', '\u2002', '\u2003', '\u2004', '\u2005', '\u2006', '\u2007',
         '\u2008', '\u2009', '\u200a', '\u2028', '\u2029', '\u202f', '\u205f', '\u3000'))

def generate_whitespace_data():
    """Generate bad whitespace list for the current python version."""
    import unicodedata
    all_whitespace_chars = set(re.findall('\\s', ''.join(chr(c) for c in range(sys.maxunicode + 1))))
    allowed_whitespace_chars = {'\t', '\n', ' '}
    bad_whitespace_chars = tuple(sorted(all_whitespace_chars - allowed_whitespace_chars))
    return WhitespaceData(unicodedata.unidata_version, bad_whitespace_chars)


class WhitespaceCheck(Check):
    __doc__ = 'Scan ebuild for useless whitespace.'
    _source = sources.EbuildFileRepoSource
    known_results = frozenset([
     WhitespaceFound, WrongIndentFound, DoubleEmptyLine,
     TrailingEmptyLine, NoFinalNewline, BadWhitespaceCharacter])

    def __init__(self, *args):
        (super().__init__)(*args)
        bad_whitespace = ''.join(whitespace_data.chars)
        self.bad_whitespace_regex = re.compile(f"(?P<char>[{bad_whitespace}])")

    def feed(self, pkg):
        lastlineempty = False
        trailing = []
        leading = []
        indent = []
        double_empty = []
        for lineno, line in enumerate(pkg.lines, 1):
            for match in self.bad_whitespace_regex.finditer(line):
                yield BadWhitespaceCharacter((repr(match.group('char'))),
                  (match.end('char')), line=(repr(line)),
                  lineno=lineno,
                  pkg=pkg)

            if line != '\n':
                lastlineempty = False
                if line[-2:-1] == ' ' or line[-2:-1] == '\t':
                    trailing.append(lineno)
                elif line[0] == ' ':
                    leading.append(lineno)
            elif indent_regexp.match(line):
                indent.append(lineno)
            else:
                if lastlineempty:
                    double_empty.append(lineno)
                else:
                    lastlineempty = True

        if trailing:
            yield WhitespaceFound('trailing', trailing, pkg=pkg)
        if leading:
            yield WhitespaceFound('leading', leading, pkg=pkg)
        if indent:
            yield WrongIndentFound(indent, pkg=pkg)
        if double_empty:
            yield DoubleEmptyLine(double_empty, pkg=pkg)
        if lastlineempty:
            yield TrailingEmptyLine(pkg=pkg)
        if pkg.lines:
            if not pkg.lines[(-1)].endswith('\n'):
                yield NoFinalNewline(pkg=pkg)