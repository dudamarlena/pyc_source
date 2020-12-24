# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ricardo/bitbucket/pybpod-project/pybpod/libraries/pyforms-generic-editor/pyforms_generic_editor/resources/__init__.py
# Compiled at: 2018-09-06 08:04:53
# Size of source mod 2**32: 588 bytes
import os

def path(filename):
    return os.path.join(os.path.dirname(__file__), 'icons', filename)


ADD_SMALL_ICON = path('add.png')
NEW_SMALL_ICON = path('new.png')
OPEN_SMALL_ICON = path('open.png')
SAVE_SMALL_ICON = path('save.png')
EXIT_SMALL_ICON = path('exit.png')
CLOSE_SMALL_ICON = path('close.png')
USER_SETTINGS_ICON = path('settings.png')
PLAY_SMALL_ICON = path('play.png')
BUSY_SMALL_ICON = path('busy.png')
PROJECT_SMALL_ICON = path('project.png')
REMOVE_SMALL_ICON = path('remove.png')
APP_LOGO_ICON = path('cf-original.png')