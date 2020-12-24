# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/artellapipe/libs/pyblish/validators/scene/studentlicense.py
# Compiled at: 2020-04-17 19:10:25
# Size of source mod 2**32: 2167 bytes
"""
Module that contains student license check validator
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
import os, tpDcc as tp, pyblish.api

class CleanStudentLicense(pyblish.api.Action):
    label = 'Clean Student License'
    on = 'failed'

    def process(self, context, plugin):
        if not tp.is_maya():
            self.log.warning('Clean Student License Action is only available in Maya!')
            return False
        else:
            from tpDcc.dccs.maya.core import helpers
            scene_name = tp.Dcc.scene_name()
            if not scene_name:
                self.log.error('Error while cleaning student license. Save your scene first!')
                return False
            if not os.path.isfile(scene_name):
                self.log.error('Error while cleaning student license. File "{}" does not exist!'.format(scene_name))
                return False
            self.log.info('Cleaning student license ...')
            valid_clean = helpers.clean_student_line(scene_name)
            if not valid_clean:
                self.log.error('Was not possible to clean student license>!')
                return False
            self.log.info('Student License cleaned successfully!')
            return True


class ValidateStudentLicense(pyblish.api.ContextPlugin):
    __doc__ = '\n    Checks if current scene has student license or not\n    '
    label = 'Check Student License'
    order = pyblish.api.ValidatorOrder
    hosts = ['maya']
    optional = False
    actions = [CleanStudentLicense]

    def process(self, context):
        context.data['comment'] = ''
        from tpDcc.dccs.maya.core import helpers
        file_path = context.data.get('path', None)
        if not file_path:
            file_path = tp.Dcc.scene_name()
        else:
            assert file_path and os.path.isfile(file_path), 'File Path "{}" does not exist!'.format(file_path)
            has_student_license = helpers.file_has_student_line(file_path)
            assert not has_student_license, 'File "{}" has student license!'.format(file_path)