# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/core/project.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 1725 bytes
__doc__ = '\nModule that contains implementation for Solstice Artella project\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, artellapipe
from artellapipe.core import project as artella_project

class PlotTwist(artella_project.ArtellaProject, object):

    def __init__(self):
        super(PlotTwist, self).__init__(name='PlotTwist')

    def init(self, force_skip_hello=False):
        super(PlotTwist, self).init(force_skip_hello=force_skip_hello)
        self.create_ocio_manager()

    def create_ocio_manager(self):
        """
        Creates instance of the OCIO Mnaager used by the project
        :return: ArtellaOCIOManager
        """
        ocio_manager = artellapipe.OCIOMgr()
        ocio_manager.set_project(self)
        return ocio_manager

    def get_toolsets_paths(self):
        """
        Overrides base ArtellaProject get_toolsets_paths
        Returns path where project toolsets are located
        :return: list(str)
        """
        import plottwist.toolsets
        return [
         os.path.dirname(os.path.abspath(plottwist.toolsets.__file__))]

    def get_resources_paths(self):
        """
        Overrides base ArtellaProject get_resources_paths
        Returns path where project resources are located
        :return: dict(str, str)
        """
        resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
        return {'project':resources_path, 
         'shelf':os.path.join(resources_path, 'icons', 'shelf')}