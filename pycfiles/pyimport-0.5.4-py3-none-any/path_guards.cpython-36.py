# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Streamline/pyimport/pyimport/path_guards.py
# Compiled at: 2020-03-10 20:18:14
# Size of source mod 2**32: 807 bytes
import os, sys, inspect
from .exceptions import PathDoesNotExist, InitMissing

def path_guard(*rel_module_paths: str) -> None:
    frame = inspect.stack()[1]
    source_path = frame[0].f_code.co_filename
    for rel_module_path in rel_module_paths:
        module_path = os.path.join(source_path, rel_module_path)
        if not os.path.exists(module_path):
            raise PathDoesNotExist(module_path)
        if module_path not in sys.path:
            sys.path.append(module_path)


def init_guard() -> None:
    frame = inspect.stack()[1]
    source_path = frame[0].f_code.co_filename
    folder = os.path.dirname(source_path)
    if '__init__.py' not in os.listdir(folder):
        raise InitMissing(folder)
    else:
        return __import__(os.path.join(folder, '__init__.py'))