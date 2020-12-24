# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/executors.py
# Compiled at: 2019-12-16 10:40:53
# Size of source mod 2**32: 1127 bytes
from dataclasses import dataclass
from typing import Callable
import subprocess, logging
logger = logging.getLogger(__name__)

class Task:

    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        pass


def cmd_command(command: str, *args):
    subprocess.run(([command] + list(args)), shell=True, check=True)


@dataclass
class Executor:
    callback = None
    callback: Callable
    args = None
    args: list
    kwargs = None
    kwargs: list
    known_exceptions = None
    known_exceptions: list

    @property
    def knowledge_errors(self) -> list:
        return self.known_exceptions or []

    def on_error(self, exception):
        logger.exception(f"{self}. {exception}")

    def on_success(self):
        logger.exception(f"{self} Task {self.callback.__name__} successful performed")

    def run(self):
        _task = self.callback
        t_args = self.args or []
        t_kwargs = self.kwargs or {}
        try:
            _task(*t_args, **t_kwargs)
        except Exception as e:
            try:
                if e in self.knowledge_errors:
                    self.on_error(e)
            finally:
                e = None
                del e

    def __str__(self):
        return f'"{type(self).__name__}". {self.__doc__}.'