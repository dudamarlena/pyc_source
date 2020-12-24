# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ttws/__init__.py
# Compiled at: 2020-02-21 03:16:25
# Size of source mod 2**32: 9349 bytes
"""Trimming of trailing white spaces.

Author-email: "Dietmar Winkler" <dietmar.winkler@dwe.no>

License: See UNLICENSE file

This script will recursively remove all trailing white spaces in all
text files in a given directory. Binary files and files residing in
version control specific directories are skipped.

As an addition one can also let it clean out obsolete or empty/superfluous
Modelica annotations from Modelica (`*.mo`) files.

It uses [Adam Hupp](http://hupp.org/adam)'s
[python-magic](https://github.com/ahupp/python-magic) as binary tester.

As a fallback (especially if libmagic is not available, like on Windows)
it acts only on files with a given file extension listed in 'extstring'.

"""
import os, textwrap, io
from pyparsing import White, Keyword, nestedExpr, lineEnd, Suppress, ZeroOrMore, Optional, ParseException, FollowedBy, CaselessLiteral
extstring = '.mo,.mos,.c,.h,.cpp,.txt,.order'
BLACKLIST = [
 '.bzr', '.cvs', '.git', '.hg', '.svn', '.#']
listofexts = extstring.split(',')

def unknownOption(script_name, args):
    """Warning message for unknown options."""
    warning = '\n        UNKNOWN OPTION: "%s"\n\n        Use %s -h [--help] for usage instructions.\n        ' % (args, script_name)
    print(textwrap.dedent(warning))


def unknownDirectory(args):
    """Warning message for unknown directory."""
    warning = '\n        WARNING: Ignoring unknown directory: "%s"\n        ' % args
    print(textwrap.dedent(warning))


def detecttype(filepath):
    """Detect the mime type of the text file."""
    try:
        from magic import Magic
        mime = Magic(mime=True)
        type = mime.from_file(filepath)
        root, ext = os.path.splitext(filepath)
        if ext in '.mo':
            return 'mo'
        else:
            if 'text/' in type:
                return 'text'
            return type
    except (ImportError, TypeError):
        root, ext = os.path.splitext(filepath)
        if ext in '.mo':
            return 'mo'
        else:
            if ext in listofexts:
                return 'text'
            return 'unknown'


def trimWhitespace(filepath, eol):
    """Trim trailing white spaces from a given filepath."""
    try:
        with io.open(filepath, 'r') as (source):
            lines = [line.rstrip() for line in source]
            while len(lines) > 1 and not lines[(-1)]:
                lines.pop(-1)

        with io.open(filepath, 'w', newline='') as (target):
            target.write(eol.join(lines) + eol)
    except (UnicodeDecodeError, TypeError) as err:
        print('\nOops! Failing to process file: %s\nAre you sure it is of pure ASCII or UTF8 encoding?\nMessage: %s\n') % (
         source.name, err)
        raise


def flatten(arg):
    ret = []
    for item in arg:
        if type(item) == list:
            ret = ret + flatten(item)
        else:
            if type(item) == tuple:
                ret = ret + flatten(list(item))
            else:
                ret.append(item)

    return ret


def skipNonEmptyGraphics(s, loc, tokens):
    flattened = flatten(tokens.args[0].asList())
    joinedFlattened = ''.join(flattened)
    graphicsPresent = False
    lastGraphics = 'graphics' in flattened[(-1)]
    extentPresent = 'extent' in joinedFlattened
    extentDefault = 'extent={{-100,-100},{100,100}}' in joinedFlattened
    for substring in flattened:
        if 'graphics' in substring:
            if lastGraphics:
                graphicsPresent = False
            else:
                graphicsPresent = True

    removeGraphics = not graphicsPresent and (not extentPresent or extentDefault)
    if not removeGraphics:
        raise ParseException('graphics defined, skipping...')


def cleanAnnotation(filepath, eol):
    """Clean out the obsolete or superfluous annotations."""
    with io.open(filepath, 'r') as (mo_file):
        string = mo_file.read()
        WindowRef = ZeroOrMore(White(' \t')) + (Keyword('Window') | Keyword('Coordsys')) + nestedExpr() + ',' + ZeroOrMore(White(' \t') + lineEnd)
        out = Suppress(WindowRef).transformString(string)
        WindowLastRef = Optional(',') + ZeroOrMore(White(' \t')) + (Keyword('Window') | Keyword('Coordsys')) + nestedExpr() + ZeroOrMore(White(' \t') + lineEnd)
        out = Suppress(WindowLastRef).transformString(out)
        dymolaRef = ZeroOrMore(White(' \t')) + (Optional('__Dymola_') + 'experimentSetupOutput' | Keyword('DymolaStoredErrors')) + ~nestedExpr() + ',' + ZeroOrMore(White(' \t'))
        out = Suppress(dymolaRef).transformString(out)
        lastDymolaRef = Optional(',') + ZeroOrMore(White(' \t')) + (Optional('__Dymola_') + 'experimentSetupOutput' | Keyword('DymolaStoredErrors')) + ~nestedExpr() + ZeroOrMore(White(' \t'))
        out = Suppress(lastDymolaRef).transformString(out)
        defaultRef = (Keyword('rotation') | Keyword('visible') | Keyword('origin')) + ZeroOrMore(White(' \t')) + '=' + ZeroOrMore(White(' \t')) + (Keyword('0') | Keyword('true') | Keyword('{0,0}')) + ',' + ZeroOrMore(White(' \t'))
        out = Suppress(defaultRef).transformString(out)
        iniSRef = Keyword('initialScale') + ZeroOrMore(White(' \t')) + '=' + ZeroOrMore(White(' \t')) + Keyword('0.1') + ',' + ZeroOrMore(White(' \t'))
        out = Suppress(iniSRef).transformString(out)
        lastDefaultRef = Optional(',') + (Keyword('rotation') | Keyword('visible') | Keyword('origin')) + ZeroOrMore(White(' \t')) + '=' + ZeroOrMore(White(' \t')) + (Keyword('0') | Keyword('true') | Keyword('{0,0}')) + ZeroOrMore(White(' \t'))
        out = Suppress(lastDefaultRef).transformString(out)
        lastIniSRef = Optional(',') + Keyword('initialScale') + ZeroOrMore(White(' \t')) + '=' + ZeroOrMore(White(' \t')) + Keyword('0.1') + ZeroOrMore(White(' \t'))
        out = Suppress(lastIniSRef).transformString(out)
        docRef = ZeroOrMore(White(' \t')) + Keyword('Documentation') + ~nestedExpr() + ',' + ZeroOrMore(White(' \t'))
        out = Suppress(docRef).transformString(out)
        lastDocRef = Optional(',') + ZeroOrMore(White(' \t')) + Keyword('Documentation') + ~FollowedBy('/') + ~nestedExpr() + ZeroOrMore(White(' \t'))
        out = Suppress(lastDocRef).transformString(out)
        emptyRef = ZeroOrMore(White(' \t')) + (Keyword('Icon') | Keyword('Diagram')) + nestedExpr()('args') + ',' + ZeroOrMore(White(' \t') + lineEnd)
        emptyRef.setParseAction(skipNonEmptyGraphics)
        out = Suppress(emptyRef).transformString(out)
        lastEmptyRef = Optional(',') + ZeroOrMore(White(' \t')) + (Keyword('Icon') | Keyword('Diagram')) + nestedExpr()('args') + ZeroOrMore(White(' \t') + lineEnd)
        lastEmptyRef.setParseAction(skipNonEmptyGraphics)
        out = Suppress(lastEmptyRef).transformString(out)
        AnnotationRef = ZeroOrMore(White(' \t')) + Keyword('annotation') + nestedExpr('(', ');', content=' ') + ZeroOrMore(White(' \t') + lineEnd)
        out = Suppress(AnnotationRef).transformString(out)
    with io.open(filepath, 'w', newline=eol) as (mo_file):
        mo_file.write(out)


def stripDocString(filepath, eol):
    """Strip spaces between string start/end and tag"""
    with io.open(filepath, 'r') as (mo_file):
        string = mo_file.read()
        opener = White().suppress() + CaselessLiteral('<html>')
        closer = CaselessLiteral('</html>') + White().suppress()
        either = opener | closer
        either.leaveWhitespace()
        out = either.transformString(string)
    with io.open(filepath, 'w', newline=eol) as (mo_file):
        mo_file.write(out)