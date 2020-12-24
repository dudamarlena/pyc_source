# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/teamsfolder.py
# Compiled at: 2012-10-12 07:02:39
from datetime import datetime
from coils.foundation import CTag
from coils.net import DAVFolder
from teamobject import TeamObject
from groupwarefolder import GroupwareFolder

class TeamsFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self.get_ctag()

    def get_ctag(self):
        return self.get_ctag_for_entity('Team')

    def _load_contents(self):
        teams = self.context.run_command('team::get')
        for team in teams:
            self.insert_child(team.object_id, team, alias=('{0}.vcf').format(team.object_id))

        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.load_contents():
            if name in ('.ls', '.json'):
                return self.get_collection_representation(name, self.get_children())
            if name == '.ctag':
                return self.get_ctag_representation(self.get_ctag_for_entity('Team'))
            team = self.get_child(name)
            if team is not None:
                return self.get_entity_representation(name, team, is_webdav=is_webdav)
        self.no_such_path()
        return