# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lapis-hong/Documents/Sina/Project/xinci/xinci/__init__.py
# Compiled at: 2018-06-20 01:11:11
"""This package contains interfaces and functionality to xinci. """
from __future__ import unicode_literals
from .dictionary import Dictionary
from .word_extraction import extract
__version__ = b'1.1.0'
__all__ = [
 Dictionary, extract]