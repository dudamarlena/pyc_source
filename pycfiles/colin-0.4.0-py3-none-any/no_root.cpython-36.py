# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/checks/best_practices/no_root.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 1013 bytes
from colin.checks.abstract.containers import ContainerCheck
from colin.checks.abstract.images import ImageCheck
from colin.checks.result import CheckResult

class NoRootCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super().__init__(name='no_root', message='Service should not run as root by default.',
          description='',
          reference_url='?????',
          tags=[
         'root', 'user'])

    def check(self, target):
        metadata = target.instance.get_metadata()['Config']
        root_present = 'User' in metadata and metadata['User'] in ('', '0', 'root')
        return CheckResult(ok=(not root_present), severity=(self.severity),
          description=(self.description),
          message=(self.message),
          reference_url=(self.reference_url),
          check_name=(self.name),
          logs=[])