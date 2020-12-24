# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpRigToolkit/utils/resource.py
# Compiled at: 2020-02-05 21:34:07
# Size of source mod 2**32: 1708 bytes
"""
Module that contains manager to handle resources for tpRigToolkit
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
from Qt.QtGui import QIcon, QPixmap
from tpPyUtils import decorators
from tpQtLib.core import resource
import tpRigToolkit

class ResourceTypes(object):
    ICON = 'icon'
    PIXMAP = 'pixmap'


@decorators.Singleton
class ResourceManager(object):
    __doc__ = '\n    Class that handles all resources stored in registered paths\n    '

    def __init__(self):
        self._resources = dict()

    def register_resource(self, resources_path):
        """
        Registers given resource path
        :param str resources_path: path to register.
        :param str key: optional key for the resource path.
        :return:
        """
        if resources_path in self._resources:
            return
        self._resources[resources_path] = resource.Resource(resources_path)

    def icon(self, *args, **kwargs):
        """
        Returns icon
        :param args: list
        :param kwargs: kwargs
        :return: QIcon
        """
        if not self._resources:
            return
        else:
            return (self.get)(args, resource_type=ResourceTypes.ICON, **kwargs) or QIcon()

    def pixmap(self, *args, **kwargs):
        """
        Returns pixmap
        :param args: list
        :param kwargs: dict
        :return: QPixmap
        """
        return (self.get)(args, resource_type=ResourceTypes.PIXMAP, **kwargs) or QPixmap()


tpRigToolkit.register.register_class('resource', ResourceManager)