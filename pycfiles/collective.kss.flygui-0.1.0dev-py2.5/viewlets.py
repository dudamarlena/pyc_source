# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/kss/flygui/browser/viewlets.py
# Compiled at: 2008-05-01 14:12:35
from plone.app.viewletmanager.manager import OrderedViewletManager

class HiddenViewletManager(OrderedViewletManager):

    def filter(self, viewlets):
        return []