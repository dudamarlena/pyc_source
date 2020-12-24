# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vermeul/openbis/obis/src/python/obis/dm/commands/addref.py
# Compiled at: 2018-09-27 20:05:19
# Size of source mod 2**32: 1263 bytes
import os
from .openbis_command import OpenbisCommand
from ..command_result import CommandResult, CommandException
from ..utils import complete_openbis_config

class Addref(OpenbisCommand):
    __doc__ = '\n    Command to add the current folder, which is supposed to be an obis repository, as \n    a new content copy to openBIS.\n    '

    def __init__(self, dm):
        super(Addref, self).__init__(dm)

    def run(self):
        self.update_external_dms_id()
        result = self.check_obis_repository()
        if result.failure():
            return result
        else:
            self.openbis.new_content_copy(self.path(), self.commit_id(), self.repository_id(), self.external_dms_id(), self.data_set_id())
            return CommandResult(returncode=0, output='')

    def update_external_dms_id(self):
        self.set_external_dms_id(None)
        self.prepare_external_dms()

    def check_obis_repository(self):
        if os.path.exists('.obis'):
            return CommandResult(returncode=0, output='')
        else:
            return CommandResult(returncode=(-1), output='This is not an obis repository.')

    def commit_id(self):
        result = self.git_wrapper.git_commit_hash()
        if result.failure():
            return result
        else:
            return result.output