# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/carbonium_fb/_i18n.py
# Compiled at: 2019-09-02 08:45:08
# Size of source mod 2**32: 256 bytes
__doc__ = 'This module provides internationalization'
import gettext, os
localedir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'locales')
tr = gettext.translation('carbonium', localedir=localedir, fallback=True)
tr.install()
_ = tr.gettext