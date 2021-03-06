# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/colin/checks/dynamic.py
# Compiled at: 2018-06-08 08:01:48
# Size of source mod 2**32: 1191 bytes
from colin.core.checks.cmd import CmdAbstractCheck

class ShellRunableCheck(CmdAbstractCheck):
    name = 'shell_runnable'

    def __init__(self):
        super(ShellRunableCheck, self).__init__(message='Shell has to be runnable.',
          description='The target has to be able to invoke shell.',
          reference_url='https://docs.docker.com/engine/reference/run/',
          tags=[
         'sh', 'cmd', 'shell', 'output'],
          cmd=[
         'sh', '-c', 'exit', '0'])