# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/colin/checks/dockerfile/from_tag.py
# Compiled at: 2018-04-05 06:15:36
# Size of source mod 2**32: 544 bytes
from colin.checks.abstract.dockerfile import InstructionCheck

class FromTagCheck(InstructionCheck):

    def __init__(self):
        super().__init__(name='is_tag_latest', message='',
          description='',
          reference_url='https://docs.docker.com/engine/reference/builder/#from',
          tags=[
         'from', 'dockerfile', 'latest'],
          instruction='FROM',
          regex='.*/latest$',
          required=False)