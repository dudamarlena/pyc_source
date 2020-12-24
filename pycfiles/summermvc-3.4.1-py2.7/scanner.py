# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/scanner.py
# Compiled at: 2018-05-30 05:31:20
__all__ = [
 'scan_package', 'scan_path']
__authors__ = ['Tim Chow']
from pkgutil import iter_modules
import importlib, os

def __scan_package(base_package):
    mods = []
    mod = importlib.import_module(base_package)
    mods.append(mod)
    if not hasattr(mod, '__path__'):
        return mods
    for importer, name, ispkg in iter_modules(mod.__path__):
        full_name = base_package + '.' + name
        if ispkg:
            mods.extend(scan_package(full_name))
            continue
        mod = importer.find_module(full_name).load_module(full_name)
        mods.append(mod)

    return mods


def scan_package(*base_packages):
    mods = set()
    for base_package in base_packages:
        mods.update(__scan_package(base_package))

    return mods


def __scan_path(base_path, base_package_name=None):
    mods = set()
    for importer, name, ispkg in iter_modules([base_path]):
        full_name = base_package_name and base_package_name + '.' + name or name
        mod = importer.find_module(full_name).load_module(full_name)
        mods.add(mod)
        if ispkg:
            mods.update(__scan_path(os.path.join(base_path, name), full_name))

    return mods


def scan_path(*paths):
    mods = set()
    for path in paths:
        mods.update(__scan_path(path))

    return mods