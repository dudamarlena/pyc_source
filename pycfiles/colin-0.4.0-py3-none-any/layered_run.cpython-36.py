# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/checks/dockerfile/layered_run.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 426 bytes
from colin.checks.abstract.dockerfile import DockerfileCheck

class LayeredRunCheck(DockerfileCheck):

    def __init__(self):
        super().__init__(name='maintainer_deprecated', message='',
          description='',
          reference_url='',
          tags=[
         'run', 'dockerfile'])

    def check(self, target):
        pass