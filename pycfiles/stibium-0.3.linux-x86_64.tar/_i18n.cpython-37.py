# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/stibium/_i18n.py
# Compiled at: 2019-09-02 08:41:04
# Size of source mod 2**32: 254 bytes
"""This module provides internationalization"""
import gettext, os
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
tr = gettext.translation('stibium', localedir=localedir, fallback=True)
tr.install()
_ = tr.gettext