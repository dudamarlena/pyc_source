# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/create_project.py
# Compiled at: 2012-10-12 07:02:39
from pytz import timezone
from datetime import datetime, timedelta
from time import time
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_PROJECT_KEYMAP
from command import ProjectCommand

class CreateProject(CreateCommand, ProjectCommand):
    __domain__ = 'project'
    __operation__ = 'new'

    def prepare(self, ctx, **params):
        self.keymap = COILS_PROJECT_KEYMAP
        self.entity = Project
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)

    def fill_missing_values(self):
        if self.obj.start is None:
            self.obj.start = datetime.now()
        if self.obj.end is None:
            self.obj.end = datetime(2032, 12, 31, 18, 59, 59)
        if self.obj.sky_url is None:
            pass
        if self.obj.is_fake is None:
            self.obj.is_fake = 0
        return

    def run(self):
        CreateCommand.run(self)
        self.fill_missing_values()
        self.set_contacts()
        self.set_enterprises()
        self.set_assignment_acls()
        self.obj.status = 'inserted'
        self.save()
        if self.obj.number is None:
            self.obj.number = ('P{0}').format(self.obj.object_id)
        folder = self._ctx.run_command('folder::new', values={'projectId': self.obj.object_id, 'name': self.obj.number})
        self.notify()
        return