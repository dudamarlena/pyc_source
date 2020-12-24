# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/wikir/tests/test_syntax.py
# Compiled at: 2009-05-15 12:00:28
from textwrap import dedent
from wikir import *
from wikir.tests import *
from nose.tools import eq_

@attr(syntax=1)
def test_option_list():
    match(publish_string(dedent('\n    -h, --help            display this help and exit\n    --version             output version information and exit\n    -p, --ping=VERBOSITY  use the machine that goes PING\n    ')), '`-h` `--help` \n  display this help and exit\n\n`--version` \n  output version information and exit\n\n`-p` `--ping=VERBOSITY` \n  use the machine that goes PING\n\n')


@attr(syntax=1)
def test_new_lines_to_spaces():
    match(publish_string('foo *bar*\nquux'), 'foo *bar* quux\n\n')


@attr(syntax=1)
def test_headers():
    match(publish_string(dedent('\n    =====\n    Title\n    =====\n    \n    Some Headline\n    =============\n    \n    More Headlines\n    --------------\n    \n    Even More\n    ~~~~~~~~~\n    \n    Another Big One\n    ===============\n    \n    Descending\n    ----------\n    \n    Deeper\n    ~~~~~~\n    \n    And More\n    ++++++++\n    ')), dedent('    = Title =\n    \n    = Some Headline =\n    \n    == More Headlines ==\n    \n    === Even More ===\n    \n    = Another Big One =\n    \n    == Descending ==\n    \n    === Deeper ===\n    \n    ==== And More ====\n    \n    '))


@attr(syntax=1)
def test_link():
    match(publish_string(dedent('\n    `Google Code`_\n    \n    .. _Google Code: http://code.google.com/\n    \n    ')), dedent('    [http://code.google.com/ Google Code]\n    \n    '))


@attr(syntax=1)
def test_bullet_list():
    match(publish_string(dedent('\n    - toast\n    - eggs\n    \n      - pancakes\n      - omelettes\n      \n        - goat cheese\n    \n    - tomatoes\n    ')), '  * toast\n  * eggs\n    * pancakes\n    * omelettes\n      * goat cheese\n  * tomatoes\n    \n    \n')


@attr(syntax=1)
def test_definition_list():
    match(publish_string(dedent('\n    Brontosaurus\n        All brontosauruses are thin at one end,\n        much much thicker in the middle\n        and then thin again at the far end.\n    ')), 'Brontosaurus\n  All brontosauruses are thin at one end, much much thicker in the middle and then thin again at the far end.\n\n\n    ')


@attr(syntax=1)
def test_definition_list_with_classifier():
    match(publish_string(dedent('\n    Brontosaurus : herbivore\n        All brontosauruses are thin at one end,\n        much much thicker in the middle\n        and then thin again at the far end.\n    ')), 'Brontosaurus : _herbivore_\n  All brontosauruses are thin at one end, much much thicker in the middle and then thin again at the far end.\n\n\n    ')


@attr(syntax=1)
@attr(deferred=1)
def test_num_list():
    match(publish_string(dedent('\n    1. toast\n    2. eggs\n    \n      - pancakes\n      - omelettes\n      \n        - goat cheese\n    \n    3. tomatoes\n    ')), '  # toast\n  # eggs\n    * pancakes\n    * omelettes\n      * goat cheese\n  # tomatoes\n    \n    \n')


@attr(syntax=1)
def test_bullet_list_then_section():
    match(publish_string(dedent('\n    - toast\n    - eggs\n    \n      - pancakes\n      - omelettes\n      \n        - goat cheese\n    \n    - tomatoes\n    \n    This Is A Title\n    ---------------\n    ')), dedent('      * toast\n      * eggs\n        * pancakes\n        * omelettes\n          * goat cheese\n      * tomatoes\n    \n    \n    = This Is A Title =\n    \n    '))


@attr(syntax=1)
def test_literal_block():
    match(publish_string(dedent("\n    ::\n    \n        some pseudo (code {\n            'doing',\n            'crazy'\n            }).acrobatics(\n            \n        1,2,3)\n    \n    ")), dedent("    {{{\n    some pseudo (code {\n        'doing',\n        'crazy'\n        }).acrobatics(\n        \n    1,2,3)\n    }}}\n    \n    "))


@attr(syntax=1)
def test_paragraphs():
    match(publish_string(dedent('\n    This is a paragraph.\n\n    Paragraphs line up at their left\n    edges, and are normally separated\n    by blank lines. \n    ')), dedent('    This is a paragraph.\n\n    Paragraphs line up at their left edges, and are normally separated by blank lines.\n    \n    '))


@attr(syntax=1)
def test_doctest():
    match(publish_string(dedent('\n    ::\n        \n        >>> 1 + 1\n        2\n        >>> 3 + 4\n        7\n        \n    ')), dedent('    {{{\n    >>> 1 + 1\n    2\n    >>> 3 + 4\n    7\n    }}}\n    \n    '))


@attr(syntax=1)
def test_auto_urls():
    match(publish_string(dedent('    Plain URLs such as http://www.google.com/ or ftp://ftp.kernel.org/ or https://secret/ are\n    automatically made into links.\n    ')), dedent('    Plain URLs such as http://www.google.com/ or ftp://ftp.kernel.org/ or https://secret/ are automatically made into links.\n    \n    '))


@attr(syntax=1)
def test_inline_literal():
    match(publish_string('``inline literal``'), dedent('        `inline literal`\n        \n        '))


@attr(syntax=1)
def test_interpretted_text():
    match(publish_string('`interpretted text`'), dedent('        `interpretted text`\n        \n        '))


@attr(syntax=1)
def test_emphasis():
    match(publish_string('*emphasis*'), dedent('        *emphasis*\n        \n        '))


@attr(syntax=1)
def test_strong_emphasis():
    match(publish_string('**emphasis**'), dedent('        *emphasis*\n        \n        '))


@attr(syntax=1)
def test_crossreferences():
    match(publish_string(dedent('\n    Internal crossreferences, like example_.\n\n    .. _example:\n\n    This is an example crossreference target. ')), dedent('    Internal crossreferences, like [#example example].\n\n    This is an example crossreference target.\n    \n    '))


@attr(syntax=1)
def test_table_of_contents():
    match(publish_string(dedent('\n    \n    .. contents::\n    \n    The Beginning\n    =============\n    \n    The Middle\n    ----------\n    \n    The Almost End\n    ~~~~~~~~~~~~~~\n    \n    A New Section\n    =============\n    ')), dedent('    == Contents ==\n\n      * The Beginning\n        * The Middle\n          * The Almost End\n      * A New Section\n\n\n    = The Beginning =\n\n    == The Middle ==\n\n    === The Almost End ===\n\n    = A New Section =\n\n    '))


@attr(syntax=1)
def test_comment():
    match(publish_string(dedent('\n    .. This text will not be shown\n       (but, for instance, in HTML might be\n       rendered as an HTML comment)\n       \n    ')), '')


@attr(syntax=1)
def test_empty_comment():
    match(publish_string(dedent('\n    An "empty comment" does not\n    consume following blocks.\n\n    ..\n\n            So this block is not "lost",\n            despite its indentation.\n            \n    ')), dedent('    An "empty comment" does not consume following blocks.\n    \n    So this block is not "lost", despite its indentation.\n    \n    '))


@attr(syntax=1)
def test_substitutions():
    match(publish_string(dedent('\n    Systematic Dysfunctioner (tm)\n    (c) Gemma Ryan\n    \n    .. Substitutions for reST:\n\n    .. |(tm)| unicode:: U+2122\n       :ltrim:\n    .. |(c)| unicode:: 0xA9\n    ')), dedent('    Systematic Dysfunctioner (tm) (c) Gemma Ryan\n    \n    '))


@attr(syntax=1)
@attr(deferred=1)
def test_grid_table():
    match(publish_string(dedent('\n    +-----+---------+-------+\n    | you | are     | sick  |\n    +=====+=========+=======+\n    | for | writing | grids |\n    +-----+---------+-------+\n    ')), dedent('    || *you* || *are* || *sick* ||\n    || for || writing || grids ||\n    \n    '))


@attr(syntax=1)
def test_note():
    match(publish_string(dedent('\n    .. note::\n        something really important\n    ')), dedent('    *Note*: something really important\n    \n    '))