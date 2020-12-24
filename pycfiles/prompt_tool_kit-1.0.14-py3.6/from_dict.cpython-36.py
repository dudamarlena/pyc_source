# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/styles/from_dict.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 4580 bytes
"""
Tool for creating styles from a dictionary.

This is very similar to the Pygments style dictionary, with some additions:
- Support for reverse and blink.
- Support for ANSI color names. (These will map directly to the 16 terminal
  colors.)
"""
from collections import Mapping
from .base import Style, DEFAULT_ATTRS, ANSI_COLOR_NAMES
from .defaults import DEFAULT_STYLE_EXTENSIONS
from .utils import merge_attrs, split_token_in_parts
from six.moves import range
__all__ = ('style_from_dict', )

def _colorformat(text):
    """
    Parse/validate color format.

    Like in Pygments, but also support the ANSI color names.
    (These will map to the colors of the 16 color palette.)
    """
    if text[0:1] == '#':
        col = text[1:]
        if col in ANSI_COLOR_NAMES:
            return col
        if len(col) == 6:
            return col
        if len(col) == 3:
            return col[0] * 2 + col[1] * 2 + col[2] * 2
    else:
        if text == '':
            return text
    raise ValueError('Wrong color format %r' % text)


def style_from_dict(style_dict, include_defaults=True):
    """
    Create a ``Style`` instance from a dictionary or other mapping.

    The dictionary is equivalent to the ``Style.styles`` dictionary from
    pygments, with a few additions: it supports 'reverse' and 'blink'.

    Usage::

        style_from_dict({
            Token: '#ff0000 bold underline',
            Token.Title: 'blink',
            Token.SomethingElse: 'reverse',
        })

    :param include_defaults: Include the defaults (built-in) styling for
        selected text, etc...)
    """
    assert isinstance(style_dict, Mapping)
    if include_defaults:
        s2 = {}
        s2.update(DEFAULT_STYLE_EXTENSIONS)
        s2.update(style_dict)
        style_dict = s2
    token_to_attrs = {}
    for ttype, styledef in sorted(style_dict.items()):
        attrs = DEFAULT_ATTRS
        if 'noinherit' not in styledef:
            for i in range(1, len(ttype) + 1):
                try:
                    attrs = token_to_attrs[ttype[:-i]]
                except KeyError:
                    pass
                else:
                    break

        for part in styledef.split():
            if part == 'noinherit':
                pass
            else:
                if part == 'bold':
                    attrs = attrs._replace(bold=True)
                else:
                    if part == 'nobold':
                        attrs = attrs._replace(bold=False)
                    else:
                        if part == 'italic':
                            attrs = attrs._replace(italic=True)
                        else:
                            if part == 'noitalic':
                                attrs = attrs._replace(italic=False)
                            else:
                                if part == 'underline':
                                    attrs = attrs._replace(underline=True)
                                else:
                                    if part == 'nounderline':
                                        attrs = attrs._replace(underline=False)
                                    else:
                                        if part == 'blink':
                                            attrs = attrs._replace(blink=True)
                                        else:
                                            if part == 'noblink':
                                                attrs = attrs._replace(blink=False)
                                            else:
                                                if part == 'reverse':
                                                    attrs = attrs._replace(reverse=True)
                                                else:
                                                    if part == 'noreverse':
                                                        attrs = attrs._replace(reverse=False)
                                                    else:
                                                        if part in ('roman', 'sans',
                                                                    'mono'):
                                                            continue
                                                        if part.startswith('border:'):
                                                            continue
                                                        if part.startswith('bg:'):
                                                            attrs = attrs._replace(bgcolor=(_colorformat(part[3:])))
                                                        else:
                                                            attrs = attrs._replace(color=(_colorformat(part)))

        token_to_attrs[ttype] = attrs

    return _StyleFromDict(token_to_attrs)


class _StyleFromDict(Style):
    __doc__ = '\n    Turn a dictionary that maps `Token` to `Attrs` into a style class.\n\n    :param token_to_attrs: Dictionary that maps `Token` to `Attrs`.\n    '

    def __init__(self, token_to_attrs):
        self.token_to_attrs = token_to_attrs

    def get_attrs_for_token(self, token):
        list_of_attrs = []
        for token in split_token_in_parts(token):
            list_of_attrs.append(self.token_to_attrs.get(token, DEFAULT_ATTRS))

        return merge_attrs(list_of_attrs)

    def invalidation_hash(self):
        return id(self.token_to_attrs)