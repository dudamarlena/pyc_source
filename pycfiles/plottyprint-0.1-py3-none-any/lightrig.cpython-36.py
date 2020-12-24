# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/files/lightrig.py
# Compiled at: 2020-04-15 09:53:56
# Size of source mod 2**32: 1187 bytes
__doc__ = '\nModule that contains implementations for light rig files in Plot Twist\n'
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import logging, tpDcc as tp, artellapipe
from artellapipe.core import file
LOGGER = logging.getLogger()

class PlotTwistLightRigFile(file.ArtellaFile, object):

    def __init__(self, project, file_name, file_path=None, file_extension=None):
        super(PlotTwistLightRigFile, self).__init__(project=project,
          file_name=file_name,
          file_path=file_path,
          file_extension=file_extension)

    def get_template_dict(self, **kwargs):
        """
        Implements get_template_dict() function
        :return: dict
        """
        return {'project_id':self._project.id, 
         'project_id_number':self._project.id_number, 
         'light_rig_name':self.name}

    def _reference_file(self, file_path, *args, **kwargs):
        LOGGER.info('Referencing: {}'.format(file_path))
        tp.Dcc.reference_file(file_path)