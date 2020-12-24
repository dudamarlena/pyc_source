# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/templ8/templ8/models.py
# Compiled at: 2020-03-04 08:43:07
# Size of source mod 2**32: 2758 bytes
import os, subprocess
from pyimport import path_guard
path_guard(__file__, '..')
from exceptions import MissingConfig
from utils import get_child_files
from dataclasses import dataclass, field
from typing import List, Tuple, Any, Callable, Dict, Iterator, Union
from jinja2 import Environment, FileSystemLoader, Template

@dataclass
class Context:
    name: str
    default: Any = None

    def emit_from_config(self, config: dict) -> Tuple[(str, Any)]:
        if config:
            if self.name in config:
                return (
                 self.name, config[self.name])
        if self.default:
            return (
             self.name, self.default)
        raise MissingConfig(self.name)


@dataclass
class Alias:
    context: Context
    formatter = lambda x: str(x).replace('-', '_')
    formatter: Callable[([Any], str)]

    def resolve(self, config: dict) -> str:
        name, value = self.context.emit_from_config(config)
        return self.formatter(value)


@dataclass
class Callback:
    call: List[Union[(str, Alias)]]

    def run(self, config: dict, output_dir: str) -> None:
        resolved_call = [i.resolve(config) if isinstance(i, Alias) else i for i in self.call]
        subprocess.run(resolved_call, cwd=output_dir)


@dataclass
class Spec:
    root_name: str
    dependencies = field(default_factory=list)
    dependencies: List[str]
    context_set = field(default_factory=list)
    context_set: List[Context]
    folder_aliases = field(default_factory=dict)
    folder_aliases: Dict[(str, Alias)]
    callbacks = field(default_factory=list)
    callbacks: List[Callback]

    def check_condition(self, config: dict) -> bool:
        required_names = [self.root_name] + self.dependencies
        if not config or not all(name in config for name in required_names):
            return False
        else:
            return all(config[name] for name in required_names)

    def load_templates(self, config: dict, template_dir: str, output_dir: str) -> Iterator[Tuple[(Template, str)]]:
        spec_root = os.path.join(template_dir, self.root_name)
        loader = Environment(loader=(FileSystemLoader(spec_root)),
          trim_blocks=True,
          lstrip_blocks=True,
          keep_trailing_newline=True)
        for file in get_child_files(spec_root):
            rel_input_path = os.path.relpath(file, spec_root)
            folder_path, filename = os.path.split(rel_input_path)
            for folder_name in self.folder_aliases:
                folder_path = folder_path.replace(folder_name, self.folder_aliases[folder_name].resolve(config))

            output_path = os.path.join(output_dir, folder_path, filename)
            template = loader.get_template(rel_input_path)
            yield (template, output_path)