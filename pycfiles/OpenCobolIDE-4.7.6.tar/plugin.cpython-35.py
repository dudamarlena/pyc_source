# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/plugin.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 1862 bytes
"""
    pygments.plugin
    ~~~~~~~~~~~~~~~

    Pygments setuptools plugin interface. The methods defined
    here also work if setuptools isn't installed but they just
    return nothing.

    lexer plugins::

        [pygments.lexers]
        yourlexer = yourmodule:YourLexer

    formatter plugins::

        [pygments.formatters]
        yourformatter = yourformatter:YourFormatter
        /.ext = yourformatter:YourFormatter

    As you can see, you can define extensions for the formatter
    with a leading slash.

    syntax plugins::

        [pygments.styles]
        yourstyle = yourstyle:YourStyle

    filter plugin::

        [pygments.filter]
        yourfilter = yourfilter:YourFilter

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
try:
    import pkg_resources
except ImportError:
    pkg_resources = None

LEXER_ENTRY_POINT = 'pygments.lexers'
FORMATTER_ENTRY_POINT = 'pygments.formatters'
STYLE_ENTRY_POINT = 'pygments.styles'
FILTER_ENTRY_POINT = 'pygments.filters'

def find_plugin_lexers():
    if pkg_resources is None:
        return
    for entrypoint in pkg_resources.iter_entry_points(LEXER_ENTRY_POINT):
        yield entrypoint.load()


def find_plugin_formatters():
    if pkg_resources is None:
        return
    for entrypoint in pkg_resources.iter_entry_points(FORMATTER_ENTRY_POINT):
        yield (
         entrypoint.name, entrypoint.load())


def find_plugin_styles():
    if pkg_resources is None:
        return
    for entrypoint in pkg_resources.iter_entry_points(STYLE_ENTRY_POINT):
        yield (
         entrypoint.name, entrypoint.load())


def find_plugin_filters():
    if pkg_resources is None:
        return
    for entrypoint in pkg_resources.iter_entry_points(FILTER_ENTRY_POINT):
        yield (
         entrypoint.name, entrypoint.load())