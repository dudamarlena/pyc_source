# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/styles/base.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 2490 bytes
__doc__ = '\nThe base classes for the styling.\n'
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from six import with_metaclass
__all__ = ('Attrs', 'DEFAULT_ATTRS', 'ANSI_COLOR_NAMES', 'Style', 'DynamicStyle')
Attrs = namedtuple('Attrs', 'color bgcolor bold underline italic blink reverse')
DEFAULT_ATTRS = Attrs(color=None, bgcolor=None, bold=False, underline=False, italic=False,
  blink=False,
  reverse=False)
ANSI_COLOR_NAMES = [
 'ansiblack', 'ansiwhite', 'ansidefault',
 'ansired', 'ansigreen', 'ansiyellow', 'ansiblue', 'ansifuchsia', 'ansiturquoise', 'ansilightgray',
 'ansidarkgray', 'ansidarkred', 'ansidarkgreen', 'ansibrown', 'ansidarkblue',
 'ansipurple', 'ansiteal']

class Style(with_metaclass(ABCMeta, object)):
    """Style"""

    @abstractmethod
    def get_attrs_for_token(self, token):
        """
        Return :class:`.Attrs` for the given token.
        """
        pass

    @abstractmethod
    def invalidation_hash(self):
        """
        Invalidation hash for the style. When this changes over time, the
        renderer knows that something in the style changed, and that everything
        has to be redrawn.
        """
        pass


class DynamicStyle(Style):
    """DynamicStyle"""

    def __init__(self, get_style):
        self.get_style = get_style

    def get_attrs_for_token(self, token):
        style = self.get_style()
        assert isinstance(style, Style)
        return style.get_attrs_for_token(token)

    def invalidation_hash(self):
        return self.get_style().invalidation_hash()