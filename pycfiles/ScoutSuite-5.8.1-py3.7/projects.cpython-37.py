# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/resources/projects.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1344 bytes
from ScoutSuite.providers.gcp.resources.base import GCPCompositeResources

class Projects(GCPCompositeResources):
    __doc__ = 'This class represents a collection of GCP Resources that are grouped by project. \n    Classes extending Projects should implement the method _fetch_children() with a project ID as paramater.\n    The children resources will be stored with the following structure {<projects>: {<project_id>: {<child_name>: {<child_id>: <child_instance>}}}}.\n    '

    async def fetch_all(self):
        """This method fetches all the GCP projects that can be accessed with the given run configuration.
        It then fetches all the children defined in _children and groups them by project.
        """
        raw_projects = await self.facade.get_projects()
        self['projects'] = {raw_project['projectId']:{} for raw_project in raw_projects}
        await self._fetch_children_of_all_resources(resources=(self['projects']),
          scopes={project_id:{'project_id': project_id} for project_id in self['projects']})
        self._set_counts()

    def _set_counts(self):
        for _, child_name in self._children:
            self[child_name + '_count'] = sum([project[(child_name + '_count')] for project in self['projects'].values()])