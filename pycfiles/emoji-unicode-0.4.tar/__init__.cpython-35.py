# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/__init__.py
# Compiled at: 2015-11-19 09:59:51
# Size of source mod 2**32: 279 bytes
from __future__ import unicode_literals
from .pattern import RE_PATTERN_TEMPLATE
from .parser import replace, normalize
from .models import Emoji
__version__ = '0.2'
__all__ = [
 'RE_PATTERN_TEMPLATE',
 'replace',
 'normalize',
 'Emoji']