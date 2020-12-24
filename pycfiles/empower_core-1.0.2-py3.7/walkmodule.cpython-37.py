# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/empower_core/walkmodule.py
# Compiled at: 2020-04-12 15:15:49
# Size of source mod 2**32: 1821 bytes
"""Inspect the specified module for services."""
import pkgutil

def walk_module(package):
    """Inspect the specified module for services."""
    results = {}
    pkgs = pkgutil.walk_packages(package.__path__)
    for importer, module_name, is_pkg in pkgs:
        if not is_pkg:
            continue
        if not any((importer.path.startswith(p) for p in package.__path__)):
            continue
        __import__(package.__name__ + '.' + module_name)
        if not hasattr(package, module_name):
            continue
        module = getattr(package, module_name)
        if not hasattr(module, 'MANIFEST'):
            continue
        manifest = getattr(module, 'MANIFEST')
        if 'name' not in manifest:
            name = package.__name__ + '.' + module_name + '.' + module_name
            manifest['name'] = name
        if 'modules' not in manifest:
            manifest['modules'] = []
        if 'label' not in manifest:
            manifest['label'] = module_name
        if 'desc' not in manifest:
            manifest['desc'] = 'No description available'
        results[manifest['name']] = manifest

    return results