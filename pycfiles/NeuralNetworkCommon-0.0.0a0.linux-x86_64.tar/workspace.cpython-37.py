# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/neuralnetworkcommon/workspace.py
# Compiled at: 2019-05-04 11:31:07
# Size of source mod 2**32: 394 bytes
import pythoncommontools.objectUtil.POPO as POPO

class Workspace(POPO):

    @staticmethod
    def constructFromAttributes(id, comments=''):
        workspace = Workspace()
        workspace.id = id
        workspace.comments = comments
        return workspace