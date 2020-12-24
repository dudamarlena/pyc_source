# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/amarin/dev/sphinx-mediatel/src/sphinx_paw/translation.py
# Compiled at: 2019-11-19 10:51:04
# Size of source mod 2**32: 189 bytes
"""Init internal translations"""
from sphinx.locale import get_translator
from sphinx_paw.constants import PACKAGE_NAME
translator = get_translator(PACKAGE_NAME)