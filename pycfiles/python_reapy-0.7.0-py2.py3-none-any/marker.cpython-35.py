# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/project/marker.py
# Compiled at: 2019-02-21 08:18:57
# Size of source mod 2**32: 2181 bytes
import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program

class Marker(ReapyObject):
    _class_name = 'Marker'

    def __init__(self, parent_project=None, index=None, parent_project_id=None):
        if parent_project_id is None:
            message = 'One of `parent_project` or `parent_project_id` must be specified.'
            assert parent_project is not None, message
            parent_project_id = parent_project.id
        self.project_id = parent_project_id
        self.index = index

    def _get_enum_index(self):
        """
        Return marker index as needed by RPR.EnumProjectMarkers2.
        """
        code = '\n        index = [\n            i for i, m in enumerate(project.markers)\n            if m.index == marker.index\n        ][0]\n        '
        index = Program(code, 'index').run(marker=self, project=reapy.Project(self.project_id))[0]
        return index

    @property
    def _kwargs(self):
        return {'index': self.index, 'parent_project_id': self.project_id}

    def delete(self):
        """
        Delete marker.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, False)

    @property
    def position(self):
        """
        Return marker position.

        Returns
        -------
        position : float
            Marker position in seconds.
        """
        code = '\n        index = marker._get_enum_index()\n        position = RPR.EnumProjectMarkers2(\n            marker.project_id, index, 0, 0, 0, 0, 0\n        )[4]\n        '
        position = Program(code, 'position').run(marker=self)[0]
        return position

    @position.setter
    def position(self, position):
        """
        Set marker position.

        Parameters
        ----------
        position : float
            Marker position in seconds.
        """
        RPR.SetProjectMarker2(self.project_id, self.index, False, position, 0, '')