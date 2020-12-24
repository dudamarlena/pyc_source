# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/khan/utils/i18n.py
# Compiled at: 2010-05-12 10:25:54
"""
Khan 内部的国际化支持
=================================

索引
=================================

* :func:`_`

=================================

.. autofunction:: _
"""
import os, gettext
__all__ = [
 '_']
DOMAIN = 'khan'
gettext.bindtextdomain(DOMAIN, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'locales'))
gettext.textdomain(DOMAIN)
_ = gettext.gettext