# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/crmsh/clidisplay.py
# Compiled at: 2016-05-04 07:56:27
__doc__ = '\nDisplay output for various syntax elements.\n'
from contextlib import contextmanager
from . import config
_pretty = True

def enable_pretty():
    global _pretty
    _pretty = True


def disable_pretty():
    global _pretty
    _pretty = False


@contextmanager
def nopretty(cond=True):
    if cond:
        disable_pretty()
    try:
        yield
    finally:
        if cond:
            enable_pretty()


def colors_enabled():
    return 'color' in config.color.style and _pretty


def _colorize(s, colors):
    if s and colors_enabled():
        return ('').join('${%s}' % clr.upper() for clr in colors) + s + '${NORMAL}'
    return s


def error(s):
    return _colorize(s, config.color.error)


def ok(s):
    return _colorize(s, config.color.ok)


def info(s):
    return _colorize(s, config.color.info)


def warn(s):
    return _colorize(s, config.color.warn)


def keyword(s):
    if 'uppercase' in config.color.style:
        s = s.upper()
    if 'color' in config.color.style:
        s = _colorize(s, config.color.keyword)
    return s


def prompt(s):
    if colors_enabled():
        s = '${RLIGNOREBEGIN}${GREEN}${BOLD}${RLIGNOREEND}' + s
        return s + '${RLIGNOREBEGIN}${NORMAL}${RLIGNOREEND}'
    return s


def prompt_noreadline(s):
    if colors_enabled():
        return '${GREEN}${BOLD}' + s + '${NORMAL}'
    return s


def help_header(s):
    return _colorize(s, config.color.help_header)


def help_keyword(s):
    return _colorize(s, config.color.help_keyword)


def help_topic(s):
    return _colorize(s, config.color.help_topic)


def help_block(s):
    return _colorize(s, config.color.help_block)


def ident(s):
    return _colorize(s, config.color.identifier)


def attr_name(s):
    return _colorize(s, config.color.attr_name)


def attr_value(s):
    return _colorize(s, config.color.attr_value)


def rscref(s):
    return _colorize(s, config.color.resource_reference)


def idref(s):
    return _colorize(s, config.color.id_reference)


def score(s):
    return _colorize(s, config.color.score)


def ticket(s):
    return _colorize(s, config.color.ticket)