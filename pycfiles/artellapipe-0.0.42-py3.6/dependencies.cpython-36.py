# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/managers/dependencies.py
# Compiled at: 2020-04-17 19:05:38
# Size of source mod 2**32: 2696 bytes
"""
Module that contains manager for DCC dependencies
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, logging, tpDcc as tp
from tpDcc.libs.python import decorators
import artellapipe.register
LOGGER = logging.getLogger()

class ArtellaDependenciesManager(object):

    def __init__(self):
        self._project = None

    def set_project(self, project):
        """
        Sets the project this manager belongs to
        :param project: ArtellaProject
        """
        self._project = project

    @decorators.abstractmethod
    def get_dependencies(self, file_path, parent_path=None, found_files=None):
        """
        Returns all dependencies that are currently loaded in the given file
        :param file_path: str, file path we want to get dependencies of
        :param parent_path: str
        :param found_files: list(str)
        :param fix_paths: bool
        :return: list(str)
        """
        raise NotImplementedError('get_dependencies function is not implemented in "{}"'.format(self.__class__.__name__))

    @decorators.abstractmethod
    def fix_dependencies_paths(self, file_path):
        """
        Tries to fix paths that are not valid in the given file
        :param file_path: str, file path we want to fix paths of
        """
        raise NotImplementedError('fix_dependencies_paths function is not implemented in "{}"'.format(self.__class__.__name__))

    def get_current_scene_dependencies(self):
        """
        Returns all dependencies that are currently loaded in current scene
        :return: list(str)
        """
        file_path = tp.Dcc.scene_name()
        if not file_path or not os.path.isfile(file_path):
            LOGGER.warning('Impossible to retrieve dependencies from current scene file: "{}"'.format(file_path))
            return
        else:
            return self.get_dependencies(file_path=file_path)

    @decorators.abstractmethod
    def update_dependencies(self, file_path):
        """
        Updates all the dependencies of the given file path
        :param file_path: str
        """
        raise NotImplementedError('update_dependencies function is not implemented in "{}"'.format(self.__class__.__name__))


@decorators.Singleton
class ArtellaDependenciesManagerSingleton(ArtellaDependenciesManager, object):

    def __init__(self):
        ArtellaDependenciesManager.__init__(self)


artellapipe.register.register_class('DepsMgr', ArtellaDependenciesManagerSingleton)