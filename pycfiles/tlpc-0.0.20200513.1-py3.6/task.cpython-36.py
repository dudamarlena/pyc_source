# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tlp/task.py
# Compiled at: 2020-05-13 17:51:52
# Size of source mod 2**32: 1789 bytes
import collections, enum
from typing import Union
import tlp.verilog.xilinx

class Task:
    __doc__ = 'Describes a TLP task.\n\n  Attributes:\n    level: Task.Level, upper or lower.\n    name: str, name of the task, function name as defined in the source code.\n    code: str, HLS C++ code of this task.\n    tasks: A dict mapping child task names to json instance description objects.\n    fifos: A dict mapping child fifo names to json FIFO description objects.\n    module: rtl.Module, should be attached after RTL code is generated.\n\n  Properties:\n    is_upper: bool, True if this task is an upper-level task.\n    is_lower: bool, True if this task is an lower-level task.\n  '

    class Level(enum.Enum):
        LOWER = 0
        UPPER = 1

    def __init__(self, **kwargs):
        level = kwargs.pop('level')
        if isinstance(level, str):
            if level == 'lower':
                level = Task.Level.LOWER
            elif level == 'upper':
                level = Task.Level.UPPER
        if not isinstance(level, Task.Level):
            raise TypeError('unexpected `level`: ' + level)
        self.level = level
        self.name = kwargs.pop('name')
        self.code = kwargs.pop('code')
        self.tasks = collections.OrderedDict()
        self.fifos = collections.OrderedDict()
        if self.is_upper:
            self.tasks = collections.OrderedDict(sorted((item for item in kwargs.pop('tasks').items()), key=(lambda x: x[0])))
            self.fifos = collections.OrderedDict(sorted((item for item in kwargs.pop('fifos').items()), key=(lambda x: x[0])))
        self.module = tlp.verilog.xilinx.Module('')

    @property
    def is_upper(self) -> bool:
        return self.level == Task.Level.UPPER

    @property
    def is_lower(self) -> bool:
        return self.level == Task.Level.LOWER