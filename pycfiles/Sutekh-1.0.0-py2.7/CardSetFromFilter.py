# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/gui/plugins/CardSetFromFilter.py
# Compiled at: 2019-12-11 16:37:54
"""Converts a filter into a card set"""
from sutekh.gui.PluginManager import SutekhPlugin
from sutekh.base.gui.plugins.BaseFromFilter import BaseFromFilter

class CardSetFromFilter(SutekhPlugin, BaseFromFilter):
    """Converts a filter into a Card Set."""
    pass


plugin = CardSetFromFilter