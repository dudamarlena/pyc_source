# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/zmi/macros.py
# Compiled at: 2012-06-20 12:11:31
__docformat__ = 'restructuredtext'
from zope.app.basicskin.standardmacros import StandardMacros as BaseMacros

class StandardMacros(BaseMacros):
    macro_pages = BaseMacros.macro_pages + ('formlib_macros', 'widget_macros', 'view_macros')