# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/utils.py
# Compiled at: 2019-11-07 21:17:24
# Size of source mod 2**32: 1969 bytes
import os, pathlib, shutil
from typing import Text, Any, Type

def remove_files_in_dir(data_dir):
    input_file_list = [i.absolute() for i in pathlib.Path(data_dir).iterdir() if i.is_file()]
    for i in input_file_list:
        os.remove(i)


def remove_content_in_dir(data_dir):
    input_file_list = pathlib.Path(data_dir).iterdir()
    for i in input_file_list:
        file_path = str(i.absolute())
        if i.is_dir():
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)


def create_dir_if_needed(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def create_file_dir_if_needed(file):
    directory = os.path.dirname(file)
    create_dir_if_needed(directory)
    return file


def join_path(a, b):
    return os.path.join(a, str(pathlib.PurePosixPath(b)))


def class_from_module_path(module_path: Text) -> Type[Any]:
    """Given the module name and path of a class, tries to retrieve the class.

    The loaded class can be used to instantiate new objects. """
    import importlib
    if '.' in module_path:
        module_name, _, class_name = module_path.rpartition('.')
        m = importlib.import_module(module_name)
        return getattr(m, class_name)
    else:
        return globals()[module_path]


def load_hook(hook_config):
    hook_instances = []
    for i in hook_config:
        class_ = class_from_module_path(i['class'])
        hook_instances.append(class_(**i.get('params', {})))

    return hook_instances