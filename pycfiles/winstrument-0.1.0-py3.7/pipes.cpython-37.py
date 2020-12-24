# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\winstrument\modules\pipes.py
# Compiled at: 2020-02-05 20:03:04
# Size of source mod 2**32: 1042 bytes
from winstrument.base_module import BaseInstrumentation

class Pipes(BaseInstrumentation):
    modulename = 'pipes'
    pipe_enums = {1:'PIPE_ACCESS_INBOUND', 
     2:'PIPE_ACCESS_OUTBOUND',  3:'PIPE_ACCESS_DUPLEX',  524288:'FILE_FLAG_FIRST_PIPE_INSTANCE'}

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)