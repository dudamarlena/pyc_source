# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wikir/tests/test_shelldoc.py
# Compiled at: 2009-03-26 18:20:42
from textwrap import dedent
from cStringIO import StringIO
from nose.tools import eq_
from wikir.tests import *
from wikir.tests.shelldoc import *

def rebuild_sess(session, include_indent=False):
    lines = []
    for (indent, token, line) in session:
        full = ''
        if include_indent:
            full = indent
        full += token + ' ' + line
        lines.append(full)

    return ('').join(lines)


def test_find_single_valid_shell_session():
    text = '\n        $ cd ../somewhere\n        $ echo "pet me"\n        | pet me\n    '
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    match(sess[0], dedent('        $ cd ../somewhere\n        $ echo "pet me"\n        | pet me\n        '))


def test_allow_empty_command():
    text = dedent('\n    this is a valid shell test::\n    \n        $\n        \n    ')
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    match(sess[0], dedent('        $ \n        '))


def test_sessions_must_be_indented():
    text = dedent('\n    $ cd ../somewhere\n    $ echo "pet me"\n    | pet me\n    ')
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    eq_(len(sess), 0)


def test_allow_unicode_output():
    text = dedent(('\n    this is a shell test with unicode output:\n    \n        $ systematic_dysfunctioner\n        | you will earn many € Euros\n        \n    ').encode('utf-8'))
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    match(sess[0], dedent('        $ systematic_dysfunctioner\n        | you will earn many € Euros\n        '))


def test_single_command():
    text = dedent('\n    this is a valid shell test::\n    \n        $ cd ../elsewhere\n        \n    ')
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    match(sess[0], dedent('        $ cd ../elsewhere\n        '))


def test_allow_session_with_invalid_indent():
    text = dedent('\n    this is an invalid shell test::\n    \n        $ cd ../somewhere\n          $ echo "pet me"\n        | pet me\n        \n    ')
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    match(sess[0], dedent('        $ cd ../somewhere\n        $ echo "pet me"\n        | pet me\n        '))


def test_find_multiple_shell_sessions():
    text = dedent('\n    This is A Document\n    ==================\n    \n    this is a shell test::\n    \n        $ cd ../somewhere\n        $ echo "pet me"\n        | pet me\n    \n    this is another shell test::\n        \n        $ cd /nowhere\n        $ cat bah.txt\n        | pretend\n        | this is bah.txt\n        $ echo produce_multi_lines\n        | This is line one\n        | \n        | Notice the blank line above\n        | - - - \n        | THE END\n        \n    ')
    sess = [ rebuild_sess(c) for c in find_shell_sessions(StringIO(text)) ]
    eq_(len(sess), 2)
    match(sess[0], dedent('        $ cd ../somewhere\n        $ echo "pet me"\n        | pet me\n        '))
    match(sess[1], dedent('        $ cd /nowhere\n        $ cat bah.txt\n        | pretend\n        | this is bah.txt\n        $ echo produce_multi_lines\n        | This is line one\n        | \n        | Notice the blank line above\n        | - - - \n        | THE END\n        '))


def test_fix_trailing_space_empty_string():
    eq_(fix_trailing_space(''), '')


def test_fix_trailing_space_new_line():
    eq_(fix_trailing_space('\n'), '\n')


def test_fix_trailing_space_two_new_lines():
    eq_(fix_trailing_space('\n\n'), '\n\n')


def test_fix_trailing_space_ignore_space():
    eq_(fix_trailing_space(' '), ' ')


def test_fix_trailing_space_when_trailing():
    eq_(fix_trailing_space('\n '), '\n')


def test_fix_trailing_space_when_multi_trailing():
    eq_(fix_trailing_space('\n \n'), '\n \n')


def test_fix_trailing_space_with_tab():
    eq_(fix_trailing_space('\n   \t  '), '\n')


def test_fix_trailing_space_with_word_and_tab():
    eq_(fix_trailing_space('barbed \n   \t  '), 'barbed \n')