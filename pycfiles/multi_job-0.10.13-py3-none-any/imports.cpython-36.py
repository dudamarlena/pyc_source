# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/multi_job/utils/imports.py
# Compiled at: 2020-02-18 13:48:05
# Size of source mod 2**32: 892 bytes
import sys
from dataclasses import dataclass
from os import path
from types import ModuleType

def from_path(module_path: str) -> ModuleType:
    module_name = path.basename(path.normpath(module_path))
    module_dir = path.dirname(path.normpath(module_path))
    with PathControl(module_dir):
        module = __import__(module_name)
    return module


common_package_dir = path.realpath(path.join(__file__, '../../common'))
common_dirs = [
 path.join(common_package_dir, 'dev_actions'),
 path.join(common_package_dir, 'prod_actions')]

@dataclass
class PathControl:
    module_dir: str

    def __enter__(self) -> None:
        sys.path.append(self.module_dir)
        sys.path += common_dirs

    def __exit__(self, type, value, tb) -> None:
        sys.path.remove(self.module_dir)
        sys.path = list(set(sys.path) - set(common_dirs))