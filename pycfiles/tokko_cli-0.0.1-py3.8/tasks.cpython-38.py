# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/tasks.py
# Compiled at: 2019-12-10 13:46:48
# Size of source mod 2**32: 343 bytes


class Helper:
    __doc__ = 'Base Helper'


class Git(Helper):
    __doc__ = 'Create project from GH templates'

    def create(self) -> None:
        pass

    def init(self) -> None:
        pass

    def login(self) -> None:
        pass


class Terminal(Helper):
    __doc__ = 'Terminal Helper'

    def get_docker_io(self) -> None:
        pass

    def get_docker_compose(self) -> None:
        pass