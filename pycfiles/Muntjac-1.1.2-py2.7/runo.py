# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/themes/runo.py
# Compiled at: 2013-04-04 15:36:36
from muntjac.ui.themes.base_theme import BaseTheme

class Runo(BaseTheme):
    THEME_NAME = 'runo'

    @classmethod
    def themeName(cls):
        return cls.THEME_NAME.lower()

    BUTTON_SMALL = 'small'
    BUTTON_BIG = 'big'
    BUTTON_DEFAULT = 'default'
    PANEL_LIGHT = 'light'
    TABSHEET_SMALL = 'light'
    SPLITPANEL_REDUCED = 'rounded'
    SPLITPANEL_SMALL = 'small'
    LABEL_H1 = 'h1'
    LABEL_H2 = 'h2'
    LABEL_SMALL = 'small'
    LAYOUT_DARKER = 'darker'
    CSSLAYOUT_SHADOW = 'box-shadow'
    CSSLAYOUT_SELECTABLE = 'selectable'
    CSSLAYOUT_SELECTABLE_SELECTED = 'selectable-selected'
    TEXTFIELD_SMALL = 'small'
    TABLE_SMALL = 'small'
    TABLE_BORDERLESS = 'borderless'
    ACCORDION_LIGHT = 'light'
    WINDOW_DIALOG = 'dialog'