# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/checks/best_practices/cmd_or_entrypoint.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 1506 bytes
import logging
from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.images import ImageCheck
from colin.checks.result import CheckResult
logger = logging.getLogger(__name__)

class CmdOrEntrypointCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super().__init__(name='cmd_or_entrypoint', message='Cmd or Entrypoint has to be specified',
          description='',
          reference_url='?????',
          tags=[
         'cmd', 'entrypoint', 'required'])

    def check(self, target):
        metadata = target.instance.get_metadata()['Config']
        cmd_present = 'Cmd' in metadata and metadata['Cmd']
        msg_cmd_present = 'Cmd {}specified.'.format('' if cmd_present else 'not ')
        logger.debug(msg_cmd_present)
        entrypoint_present = 'Entrypoint' in metadata and metadata['Entrypoint']
        msg_entrypoint_present = 'Entrypoint {}specified.'.format('' if entrypoint_present else 'not ')
        logger.debug(msg_entrypoint_present)
        passed = cmd_present or entrypoint_present
        return CheckResult(ok=passed, severity=(self.severity),
          description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[
         msg_cmd_present, msg_entrypoint_present])