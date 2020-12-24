# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luisteixeira/fchampalimaud/pybpod/base/pybpod-gui-plugin/pybpodgui_plugin/resources/__init__.py
# Compiled at: 2019-11-07 13:01:56
# Size of source mod 2**32: 831 bytes
import os

def path(filename):
    return os.path.join(os.path.dirname(__file__), 'icons', filename)


BOARD_SMALL_ICON = path('board.png')
BOARDS_SMALL_ICON = path('boards.png')
BOX_SMALL_ICON = path('box.png')
SUBJECT_SMALL_ICON = path('subject.png')
SUBJECTS_SMALL_ICON = path('subjects.png')
UPLOAD_SMALL_ICON = path('upload.png')
EXPERIMENT_SMALL_ICON = path('experiment.png')
EXPERIMENTS_SMALL_ICON = path('experiments.png')
TASK_SMALL_ICON = path('task.png')
TASKS_SMALL_ICON = path('tasks.png')
CODEFILE_SMALL_ICON = path('codefile.png')
OTHERFILE_SMALL_ICON = path('otherfile.png')
PERSON_SMALL_ICON = path('person.png')
PERSONS_SMALL_ICON = path('persons.png')
REFRESH_SMALL_ICON = path('refresh.png')