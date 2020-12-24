# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/whooshdoc/util.py
# Compiled at: 2009-02-23 01:54:38
""" Utilities for WhooshDoc.
"""
import os, struct, sys
from whoosh import index
from whoosh.fields import KEYWORD, Schema, TEXT
query_help = '\nThe Whoosh query syntax supports conjunctions with AND and OR, negation with\nNOT, grouping with (parentheses), and phrases with "quotes". Once can use\nthe * wildcard at the end of a term, but not the beginning or middle. By\ndefault, all search terms are ANDed together.\n\nBy default, search terms are applied to the docstring content itself. There\nare additional fields that can be searched with the syntax\n"field_name:search_expr". The fields are:\n\n    - docstring: Just in case you want to be explicit.\n\n    - name: The preferred name of the object. It may be any single part of\n        the dotted name, or any number of leading parts of the name.\n        For example, the function numpy.linalg.lstsq can be found in all the\n        searches "name:lstsq", "name:numpy", "name:numpy.linalg", and\n        "name:linalg".\n\n    - aliases: All of the discovered names of the object, including the\n        preferred one. When an object is created in one place, and exposed\n        higher up in the package hierarchy, the higher name is "preferred".\n        For example, if we have a function defined as foo.bar.baz() but is\n        imported into the foo.__init__ module to be exposed as foo.baz(), it\n        will have a "name" of foo.baz, but "aliases" will also have\n        foo.bar.baz.\n\n    - kind: Either "function", "class", "method" or "module" depending on\n        the kind of object. For example, to find only functions (or\n        methods), use "kind:function". To exclude modules, use "not\n        kind:module".\n\n    - summary: The docstring summary is the first contiguous paragraph in\n        a docstring, usually just a sentence. While you can use this field\n        to just search the summary sentence, this is not usually an\n        improvement over just searching the docstring itself. This field is\n        used to internally to show more informative results.\n\nExamples\n--------\nbessel kind:function\n    Find Bessel functions, but not modules that use the word "bessel".\n\nbessel or airy not filter\n    Find both Bessel functions and Airy functions but not Bessel filters.\n\nname:linalg\n    Look for anything with the component \'linalg\' in its preferred name.\n\n"minimize a function"\n    Find docstrings with the phrase "minimize a function".\n\nthe\n    Should return no results. Common English connective words like "the"\n    (i.e. so-called "stop" words) are omitted during indexing and cannot be\n    searched for.\n\nname:fmin*\n    Search for all objects with names that start with "fmin" like fmin_tnc,\n    fmin, and fminbound.\n'
schema = Schema(kind=KEYWORD(stored=True), name=KEYWORD(stored=True), group=KEYWORD(stored=True), aliases=KEYWORD(stored=True), docstring=TEXT(stored=True), summary=TEXT(stored=True))

def create_or_open_index(dirname):
    """ Open an index, or create it if necessary.
    """
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    if os.listdir(dirname):
        ix = index.open_dir(dirname)
    else:
        ix = index.create_in(dirname, schema=schema)
    return ix


def terminal_size():
    """ Return the width and height of the terminal in a cross-platform manner.
    """
    if sys.platform == 'win32':
        (width, height) = _terminal_size_win32()
    else:
        (width, height) = _terminal_size_unix()
    return (
     width, height)


def _terminal_size_win32():
    """ Return the width and height of the terminal on 32-bit Windows.

    This code derives from the Python Cookbook recipe by Alexander Belchenko
    available under the PSF license.
    http://code.activestate.com/recipes/440694/
    """
    from ctypes import windll, create_string_buffer
    width = 80
    height = 25
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy) = struct.unpack('hhhhHhhhhhh', csbi.raw)
        width = right - left + 1
        height = bottom - top + 1
    width -= 1
    return (width, height)


def _terminal_size_unix():
    """ Return the width and height of the terminal on UNIX-type systems.
    """
    width = -1
    height = -1
    try:
        import fcntl, termios
        (height, width) = struct.unpack('hh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ, '1234'))
    except (ImportError, AttributeError, IOError), e:
        pass

    if width <= 0:
        width = os.environ.get('COLUMNS', -1)
    if height <= 0:
        height = os.environ.get('LINES', -1)
    if width <= 0:
        width = 80
    if height <= 0:
        height = 25
    return (
     width, height)


def default_index():
    """ Try to find the default index.

    First, the egg entry point "WhooshDoc.index" is checked, then "_index" is
    assumed.
    """
    try:
        import pkg_resources
        ep = iter(pkg_resources.iter_entry_points('WhooshDoc.index')).next()
        indexname = ep.load(require=False)
    except (ImportError, StopIteration), e:
        indexname = '_index'

    return indexname