# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/Jkob/Dev/Jalapeno/GUI/Gutils/assets.py
# Compiled at: 2017-03-03 21:28:37
# Size of source mod 2**32: 418 bytes
from flask import url_for, Blueprint
import os
from Jalapeno.lib.fileMgr import Mgr
from Jalapeno.path import APP_DIR
gasset = Blueprint('Gassets', __name__)
gui_assets_path = APP_DIR + os.sep + 'Jalapeno' + os.sep + 'GUI'
gui_files = Mgr(gui_assets_path).tree_dict()
print(gui_files)

@gasset.context_processor
def gui_theme_processor():
    gui_assets = Mgr.url_builder('static', gui_files)
    return dict(asset=gui_assets)