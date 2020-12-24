# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/despres/MAIN/Users/despres/Desktop/reaper/scripts/reapy/reapy/core/project/region.py
# Compiled at: 2019-02-23 06:05:11
# Size of source mod 2**32: 5578 bytes
import reapy
from reapy import reascript_api as RPR
from reapy.core import ReapyObject
from reapy.tools import Program

class Region(ReapyObject):
    _class_name = 'Region'

    def __init__(self, parent_project=None, index=None, parent_project_id=None):
        if parent_project_id is None:
            message = 'One of `parent_project` or `parent_project_id` must be specified.'
            assert parent_project is not None, message
            parent_project_id = parent_project.id
        self.project_id = parent_project_id
        self.index = index

    def _get_enum_index(self):
        """
        Return region index as needed by RPR.EnumProjectMarkers2.
        """
        code = '\n        index = [\n            i for i, r in enumerate(project.regions)\n            if r.index == region.index\n        ][0]\n        '
        index = Program(code, 'index').run(region=self, project=reapy.Project(self.project_id))[0]
        return index

    @property
    def _kwargs(self):
        return {'index': self.index, 'parent_project_id': self.project_id}

    def add_rendered_track(self, track):
        """
        Add track to region render matrix for this region.

        Parameters
        ----------
        track : Track
            Track to add.

        See also
        --------
        Region.add_rendered_tracks
            Efficiently add several tracks to region render matrix.
        Region.remove_rendered_track
        Region.remove_rendered_tracks
        """
        RPR.SetRegionRenderMatrix(self.project_id, self.index, track.id, 1)

    def add_rendered_tracks(self, tracks):
        """
        Efficiently add  several tracks to region render matrix.

        Parameters
        ----------
        tracks : list of Track
            Tracks to add.

        See also
        --------
        Region.remove_rendered_tracks
        """
        code = '\n        for track in tracks:\n            region.add_rendered_track(track)\n        '
        Program(code).run(region=self, tracks=tracks)

    @property
    def end(self):
        """
        Region end.

        :type: float
            Region end in seconds.
        """
        code = '\n        index = region._get_enum_index()\n        end = RPR.EnumProjectMarkers2(\n            region.project_id, index, 0, 0, 0, 0, 0\n        )[5]\n        '
        end = Program(code, 'end').run(region=self)[0]
        return end

    @end.setter
    def end(self, end):
        """
        Set region end.

        Parameters
        ----------
        end : float
            region end in seconds.
        """
        code = '\n        RPR.SetProjectMarker2(\n            region.project_id, region.index, True, region.start, end, ""\n        )\n        '
        Program(code).run(region=self, end=end)

    def delete(self):
        """
        Delete region.
        """
        RPR.DeleteProjectMarker(self.project_id, self.index, True)

    def remove_rendered_track(self, track):
        """
        Remove track from region render matrix for this region.

        Parameters
        ----------
        track : Track
            Track to remove.

        See also
        --------
        Region.add_rendered_tracks
        Region.remove_rendered_track
        Region.remove_rendered_tracks
            Efficiently remove several tracks from render matrix.
        """
        RPR.SetRegionRenderMatrix(self.project_id, self.index, track.id, -1)

    def remove_rendered_tracks(self, tracks):
        """
        Efficiently remove  several tracks from region render matrix.

        Parameters
        ----------
        tracks : list of Track
            Tracks to remove.

        See also
        --------
        Region.add_rendered_tracks
        """
        code = '\n        for track in tracks:\n            region.remove_rendered_track(track)\n        '
        Program(code).run(region=self, tracks=tracks)

    @property
    def rendered_tracks(self):
        """
        List of tracks for this region in region render matrix.

        :type: list of Track
        """
        code = '\n        i = 0\n        tracks = []\n        while i == 0 or tracks[-1]._is_defined:\n            track_id = RPR.EnumRegionRenderMatrix(\n                region.project_id, region.index, i\n            )\n            tracks.append(reapy.Track(track_id))\n            i += 1\n        tracks = tracks[:-1]\n        '
        rendered_tracks = Program(code, 'tracks').run(region=self)[0]
        return rendered_tracks

    @property
    def start(self):
        """
        Region start.

        :type: float
        """
        code = '\n        index = region._get_enum_index()\n        start = RPR.EnumProjectMarkers2(\n            region.project_id, index, 0, 0, 0, 0, 0\n        )[4]\n        '
        start = Program(code, 'start').run(region=self)[0]
        return start

    @start.setter
    def start(self, start):
        """
        Set region start.

        Parameters
        ----------
        start : float
            region start in seconds.
        """
        code = '\n        RPR.SetProjectMarker2(\n            region.project_id, region.index, 1, start, region.end, ""\n        )\n        '
        Program(code).run(region=self, start=start)