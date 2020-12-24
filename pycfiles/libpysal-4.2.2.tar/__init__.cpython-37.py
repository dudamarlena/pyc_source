# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jovyan/libpysal/examples/__init__.py
# Compiled at: 2020-01-04 10:33:20
# Size of source mod 2**32: 1219 bytes
"""
The :mod:`libpysal.examples` module includes a number of small built-in example datasets as well as functions to fetch larger datasets.
"""
from .base import example_manager
from .remotes import datasets as remote_datasets
from .remotes import download as fetch_all
from .builtin import datasets as builtin_datasets
__all__ = [
 'get_path', 'available', 'explain', 'fetch_all']
example_manager.add_examples(remote_datasets)
example_manager.add_examples(builtin_datasets)

def available():
    """
    List available datasets
    """
    return example_manager.available()


def explain(name):
    """
    Explain a dataset by name
    """
    return example_manager.explain(name)


def load_example(example_name):
    """
    Load example dataset instance
    """
    return example_manager.load(example_name)


def get_path(file_name):
    """
    get the path for a file by searching installed datasets
    """
    installed = example_manager.get_installed_names()
    for name in installed:
        example = example_manager.datasets[name]
        pth = example.get_path(file_name, verbose=False)
        if pth:
            return pth

    print('{} is not a file in any installed dataset.'.format(file_name))