# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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