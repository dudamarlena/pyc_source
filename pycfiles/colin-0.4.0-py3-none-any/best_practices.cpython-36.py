# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/checks/best_practices.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 4201 bytes
import logging
from colin.core.checks.containers import ContainerAbstractCheck
from colin.core.checks.filesystem import FileCheck
from colin.core.checks.images import ImageAbstractCheck
from colin.core.result import CheckResult
from colin.core.target import inspect_object
logger = logging.getLogger(__name__)

class CmdOrEntrypointCheck(ContainerAbstractCheck, ImageAbstractCheck):
    name = 'cmd_or_entrypoint'

    def __init__(self):
        super(CmdOrEntrypointCheck, self).__init__(message='Cmd or Entrypoint has to be specified',
          description='An ENTRYPOINT allows you to configure a container that will run as an executable. The main purpose of a CMD is to provide defaults for an executing container.',
          reference_url='https://fedoraproject.org/wiki/Container:Guidelines#CMD.2FENTRYPOINT_2',
          tags=[
         'cmd', 'entrypoint'])

    def check(self, target):
        metadata = inspect_object(target.instance)['Config']
        cmd_present = 'Cmd' in metadata and metadata['Cmd']
        msg_cmd_present = 'Cmd {}specified.'.format('' if cmd_present else 'not ')
        logger.debug(msg_cmd_present)
        entrypoint_present = 'Entrypoint' in metadata and metadata['Entrypoint']
        msg_entrypoint_present = 'Entrypoint {}specified.'.format('' if entrypoint_present else 'not ')
        logger.debug(msg_entrypoint_present)
        passed = cmd_present or entrypoint_present
        return CheckResult(ok=passed, description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[
         msg_cmd_present, msg_entrypoint_present])


class HelpFileOrReadmeCheck(FileCheck):
    name = 'help_file_or_readme'

    def __init__(self):
        super(HelpFileOrReadmeCheck, self).__init__(message="The 'helpfile' has to be provided.",
          description="Just like traditional packages, containers need some 'man page' information about how they are to be used, configured, and integrated into a larger stack.",
          reference_url='https://fedoraproject.org/wiki/Container:Guidelines#Help_File',
          files=[
         '/help.1', '/README.md'],
          tags=[
         'filesystem', 'helpfile', 'man'],
          all_must_be_present=False)


class NoRootCheck(ContainerAbstractCheck, ImageAbstractCheck):
    name = 'no_root'

    def __init__(self):
        super(NoRootCheck, self).__init__(message='Service should not run as root by default.',
          description='It can be insecure to run service as root.',
          reference_url='?????',
          tags=[
         'root', 'user'])

    def check(self, target):
        metadata = inspect_object(target.instance)['Config']
        root_present = 'User' in metadata and metadata['User'] in ('', '0', 'root')
        return CheckResult(ok=(not root_present), description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[])