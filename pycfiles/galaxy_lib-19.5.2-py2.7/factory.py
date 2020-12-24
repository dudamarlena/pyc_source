# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/toolbox/lineages/factory.py
# Compiled at: 2018-04-20 03:19:42
from galaxy.util.tool_version import remove_version_from_guid
from .interface import ToolLineage

class LineageMap(object):
    """ Map each unique tool id to a lineage object.
    """

    def __init__(self, app):
        self.lineage_map = {}
        self.app = app

    def register(self, tool):
        tool_id = tool.id
        versionless_tool_id = remove_version_from_guid(tool_id)
        lineage = self.lineage_map.get(versionless_tool_id)
        if not lineage:
            lineage = ToolLineage.from_tool(tool)
        else:
            lineage.register_version(tool.version)
        if versionless_tool_id and versionless_tool_id not in self.lineage_map:
            self.lineage_map[versionless_tool_id] = lineage
        if tool_id not in self.lineage_map:
            self.lineage_map[tool_id] = lineage
        return self.lineage_map[tool_id]

    def get(self, tool_id):
        """
        Get lineage for `tool_id`.

        By preference the lineage for a version-agnostic tool_id is returned.
        Falls back to fetching the lineage only when this fails.
        This happens when the tool_id does not contain a version.
        """
        lineage = self._get_versionless(tool_id)
        if lineage:
            return lineage
        if tool_id not in self.lineage_map:
            tool = self.app.toolbox._tools_by_id.get(tool_id)
            if tool:
                lineage = ToolLineage.from_tool(tool)
            if lineage:
                self.lineage_map[tool_id] = lineage
        return self.lineage_map.get(tool_id)

    def _get_versionless(self, tool_id):
        versionless_tool_id = remove_version_from_guid(tool_id)
        return self.lineage_map.get(versionless_tool_id, None)


__all__ = ('LineageMap', )