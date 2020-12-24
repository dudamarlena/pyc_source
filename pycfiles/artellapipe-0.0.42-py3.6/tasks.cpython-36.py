# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/managers/tasks.py
# Compiled at: 2020-04-17 19:05:38
# Size of source mod 2**32: 1704 bytes
"""
Module that contains manager to handle tasks
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging
from tpDcc.libs.python import decorators
import artellapipe
LOGGER = logging.getLogger()

class ArtellaTasksManager(object):

    def __init__(self):
        self._project = None

    def set_project(self, project):
        """
        Sets the project this manager belongs to
        :param project: ArtellaProject
        """
        self._project = project

    def get_tasks_for_shot(self, shot_name):
        """
        Returns all tasks attached to the given shot
        :param shot_name: str
        :return:
        """
        shot_found = artellapipe.ShotsMgr().find_shot(shot_name)
        if not shot_found:
            LOGGER.warning('No shot found with name: "{}"!'.format(shot_name))
            return
        else:
            return artellapipe.Tracker().get_tasks_in_shot(shot_found.get_id())

    def get_task_names_for_shot(self, shot_name):
        """
        Returns all names of the tasks attached to the given shot
        :param shot_name: str
        :return: list(str)
        """
        tasks_for_shot = self.get_tasks_for_shot(shot_name)
        if not tasks_for_shot:
            return
        else:
            return [task.name for task in tasks_for_shot]


@decorators.Singleton
class ArtellaTasksManagerSingleton(ArtellaTasksManager, object):

    def __init__(self):
        ArtellaTasksManager.__init__(self)


artellapipe.register.register_class('TasksMgr', ArtellaTasksManagerSingleton)