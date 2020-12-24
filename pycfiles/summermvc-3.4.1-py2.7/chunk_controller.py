# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/controller/chunk_controller.py
# Compiled at: 2018-05-30 05:31:20
from summermvc.decorator import *

@rest_controller
class ChunkController(object):

    @request_mapping('/chunk', produce='text/plain')
    def test_chunk(self):
        for i in range(3):
            yield 'this is %3d.\n' % i

        yield help_func()