# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/dev/models/models.py
# Compiled at: 2020-02-01 17:09:05
# Size of source mod 2**32: 2763 bytes
"""
Project, Job, Routine and Subprocess classes
"""
from utils.colours import green
from abc import ABC, abstractmethod
from utils.strings import join_paths
from dataclasses import dataclass, field
from utils.tags import substitute_exec_form
from subprocess import run, CompletedProcess
from typing import List, Type, TypeVar, Union
T = TypeVar('T')

@dataclass
class Process:
    call: str
    path: str
    alias: str

    def trigger(self) -> CompletedProcess:
        return run((self.call), cwd=(self.path))

    def __str__(self):
        return self.alias


@dataclass
class Project:
    name: str
    path: str
    context = field(default_factory=dict)
    context: dict

    def abs_path(self, config_path):
        return join_paths(config_path, self.path)

    @classmethod
    def from_config(cls: Type[T], dct: dict) -> List[T]:
        return [cls(name=k, **v) for k, v in dct.items()]


@dataclass
class Job:
    name: str
    command = ''
    command: str
    function = ''
    function: str
    context = field(default_factory=dict)
    context: dict
    targets = field(default_factory=list)
    targets: Union[(str, List[str])]
    skips = field(default_factory=list)
    skips: Union[(str, List[str])]

    def resolve_targets(self, projects: List[Project]) -> List[Project]:
        matches = []
        if self.targets:
            matches = [p for p in projects if not p.name in self.targets if self.targets == 'all']
        else:
            if self.skips:
                matches = [p for p in projects if not p.name in self.skips if not self.skips == 'all']
            else:
                local = matches or Project(name='Local', path='.')
                matches.append(local)
            return matches

    def resolve_process(self, target: Project, context_overrides: dict, config_path: str) -> Process:
        context = dict(self.context, **context_overrides, **target.context)
        path = target.abs_path(config_path)
        alias = f"Job: {self.name}, project: {target.name}"
        if self.command:
            call = substitute_exec_form(self.command, context, alias)
        else:
            if self.function:
                kwargs = f"context={context}"
                module, funct = str.rsplit(self.function, ':', 1)
                call = f"getattr(__import__({module}), {funct})({kwargs})"
        return Process(call, path, alias)

    @classmethod
    def from_config(cls: Type[T], dct: dict) -> List[T]:
        return [cls(name=k, **v) for k, v in dct.items()]


@dataclass
class Routine:
    name: str
    jobs: List[str]

    def resolve_jobs(self, jobs: List[Job]) -> List[Job]:
        return [j for j in jobs if j.name in self.jobs]

    @classmethod
    def from_config(cls: Type[T], dct: dict) -> List[T]:
        return [cls(name=k, jobs=v) for k, v in dct.items()]