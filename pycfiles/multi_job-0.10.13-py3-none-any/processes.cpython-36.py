# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/models/processes.py
# Compiled at: 2020-02-05 05:11:49
# Size of source mod 2**32: 979 bytes
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from subprocess import run
from typing import Callable

@dataclass
class Process(ABC):
    path: str
    alias: str

    @abstractmethod
    def trigger(self) -> str:
        pass

    @abstractproperty
    def raw(self) -> str:
        pass

    def show(self, verbose: bool) -> str:
        if verbose:
            return self.raw
        else:
            return self.alias


@dataclass
class CommandProcess(Process):
    call: str

    def trigger(self) -> str:
        output = run((self.call), cwd=(self.path))
        return str(output)

    @property
    def raw(self) -> str:
        return f"{self.call} in {self.path}"


@dataclass
class FunctionProcess(Process):
    function: Callable
    context: dict

    def trigger(self) -> str:
        return self.function(self.path, self.context)

    @property
    def raw(self) -> str:
        return f"{self.function} with path arg: {self.path} and context arg: {self.context}"