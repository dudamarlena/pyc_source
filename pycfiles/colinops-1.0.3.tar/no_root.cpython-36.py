# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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