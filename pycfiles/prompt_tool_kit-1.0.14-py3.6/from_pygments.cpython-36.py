# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/styles/from_pygments.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2349 bytes
"""
Adaptor for building prompt_tool_kit styles, starting from a Pygments style.

Usage::

    from pygments.styles.tango import TangoStyle
    style = style_from_pygments(pygments_style_cls=TangoStyle)
"""
from __future__ import unicode_literals
from .base import Style
from .from_dict import style_from_dict
__all__ = ('PygmentsStyle', 'style_from_pygments')
try:
    from pygments.style import Style as pygments_Style
    from pygments.styles.default import DefaultStyle as pygments_DefaultStyle
except ImportError:
    pygments_Style = None
    pygments_DefaultStyle = None

def style_from_pygments(style_cls=pygments_DefaultStyle, style_dict=None, include_defaults=True):
    """
    Shortcut to create a :class:`.Style` instance from a Pygments style class
    and a style dictionary.

    Example::

        from prompt_tool_kit.styles.from_pygments import style_from_pygments
        from pygments.styles import get_style_by_name
        style = style_from_pygments(get_style_by_name('monokai'))

    :param style_cls: Pygments style class to start from.
    :param style_dict: Dictionary for this style. `{Token: style}`.
    :param include_defaults: (`bool`) Include prompt_tool_kit extensions.
    """
    if not style_dict is None:
        assert isinstance(style_dict, dict)
        if not style_cls is None:
            assert issubclass(style_cls, pygments_Style)
    else:
        styles_dict = {}
        if style_cls is not None:
            styles_dict.update(style_cls.styles)
        if style_dict is not None:
            styles_dict.update(style_dict)
    return style_from_dict(styles_dict, include_defaults=include_defaults)


class PygmentsStyle(Style):
    __doc__ = ' Deprecated. '

    def __new__(cls, pygments_style_cls):
        assert issubclass(pygments_style_cls, pygments_Style)
        return style_from_dict(pygments_style_cls.styles)

    def invalidation_hash(self):
        pass

    @classmethod
    def from_defaults(cls, style_dict=None, pygments_style_cls=pygments_DefaultStyle, include_extensions=True):
        """ Deprecated. """
        return style_from_pygments(style_cls=pygments_style_cls,
          style_dict=style_dict,
          include_defaults=include_extensions)