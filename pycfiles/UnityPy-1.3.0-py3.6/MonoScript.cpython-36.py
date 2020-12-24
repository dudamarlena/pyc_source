# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\MonoScript.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 1013 bytes
from .NamedObject import NamedObject

class MonoScript(NamedObject):

    def __init__(self, reader):
        super().__init__(reader=reader)
        if self.version[0] > 3 or self.version[0] == 3 and self.version[1] >= 4:
            self.execution_order = reader.read_int()
        else:
            if self.version[0] < 5:
                self.properties_hash = reader.read_u_int()
            else:
                self.properties_hash = reader.read_bytes(16)
        if self.version[0] < 3:
            self.path_name = reader.read_aligned_string()
        self.class_name = reader.read_aligned_string()
        if self.version[0] >= 3:
            self.namespace = reader.read_aligned_string()
        self.assembly_name = reader.read_aligned_string()
        if self.version[0] < 2018 or self.version[0] == 2018 and self.version[1] < 2:
            self.is_editor_script = reader.read_boolean()