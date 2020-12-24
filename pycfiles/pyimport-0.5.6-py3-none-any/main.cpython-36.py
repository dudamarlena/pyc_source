# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ../pyimport/main.py
# Compiled at: 2020-03-03 13:46:16
# Size of source mod 2**32: 1572 bytes
import os, sys
from dataclasses import dataclass
from types import ModuleType

def path_guard(module_path: str) -> None:
    if not os.path.exists(module_path):
        raise PathNotResolvable(module_path)
    if module_path not in sys.path:
        sys.path.append(module_path)


def get_resource(module_path: str) -> ModuleType:
    print(module_path)
    if not os.path.exists(module_path):
        raise PathNotResolvable(module_path)
    module_dir = os.path.dirname(os.path.normpath(module_path))
    module_name = os.path.basename(os.path.normpath(module_path))
    if module_name.endswith('.py'):
        module_name = module_name[:-3]
    with PathControl(module_dir):
        module = __import__(module_name)
    return module


def init_guard(file_path: str) -> ModuleType:
    folder = os.path.dirname(file_path)
    contents = os.listdir(folder)
    if '__init__.py' not in contents:
        raise InitNotFound(folder)
    else:
        return get_resource(os.path.join(folder, '__init__.py'))


@dataclass
class PathControl:
    module_dir: str

    def __enter__(self) -> None:
        sys.path.append(self.module_dir)

    def __exit__(self, type, value, tb) -> None:
        sys.path.remove(self.module_dir)


class PathNotResolvable(Exception):

    def __init__(self, name):
        msg = f"The path '{name}' is not resolvable"
        super().__init__(msg)


class InitNotFound(Exception):

    def __init__(self, folder):
        msg = f"The folder '{folder}' has no file called __init__.py"
        super().__init__(msg)