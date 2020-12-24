# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Jakob/Jest/Jalapeno/GUI/Gutils/gtheme.py
# Compiled at: 2017-03-04 23:58:55
# Size of source mod 2**32: 236 bytes
from Jalapeno.GUI.G import gui
from Jalapeno.lib import themeMgr
gui_theme = theme = themeMgr.Theme('GUI')

@gui.context_processor
def gui_theme_processor():
    gui_assets = gui_theme.static_url_for()
    return dict(gui=gui_assets)