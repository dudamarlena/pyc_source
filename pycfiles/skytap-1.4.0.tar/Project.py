# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: skytap/models/Project.py
# Compiled at: 2016-12-16 14:55:45
"""Support for Projects."""
from skytap.models.SkytapResource import SkytapResource
from skytap.Users import Users

class Project(SkytapResource):
    """One Skytap project."""

    def __init__(self, project_json):
        """Build one Skytap project."""
        super(Project, self).__init__(project_json)

    def _calculate_custom_data(self):
        """Make the list of users into a Users list."""
        self.data['users'] = Users(self.users)
        for key in self.users.keys():
            if self.users[key].url == self.owner_url:
                self.owner_name = self.users[key].name
                break