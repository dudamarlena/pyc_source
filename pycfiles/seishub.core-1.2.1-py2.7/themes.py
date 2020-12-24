# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\packages\admin\web\themes.py
# Compiled at: 2010-12-23 17:42:58
"""
Various CSS themes for the administration pages.
"""
from seishub.core.core import Component, implements
from seishub.core.packages.interfaces import IAdminTheme

class OldTheme(Component):
    """
    Old WebAdmin theme.
    """
    implements(IAdminTheme)
    theme_id = 'oldstyle'
    theme_css_resource = '/css/oldstyle.css'


class MagicTheme(Component):
    """
    New *magic* WebAdmin theme.
    """
    implements(IAdminTheme)
    theme_id = 'magic'
    theme_css_resource = '/css/magic.css'