# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: E:\01_Work\15_PhD\11_Python_neural_mass_models\PyRates\pyrates\frontend\file.py
# Compiled at: 2019-06-26 16:26:50
# Size of source mod 2**32: 3295 bytes
__doc__ = '\n'
import importlib
from pyrates import PyRatesException
from pyrates.frontend import yaml as _yaml
__author__ = 'Daniel Rose'
__status__ = 'Development'
file_loader_mapping = {'yaml':_yaml.to_dict, 
 'yml':_yaml.to_dict}

def parse_path(path: str):
    """Parse a path of form path.to.template, returning a tuple of (name, file, abspath)."""
    if '/' in path or '\\' in path:
        import os
        file, template_name = os.path.split(path)
        dirs, file = os.path.split(file)
        abspath = os.path.abspath(dirs)
    elif '.' in path:
        *modules, file, template_name = path.split('.')
        parentdir = '.'.join(modules)
        try:
            module = importlib.import_module(parentdir)
        except ModuleNotFoundError:
            raise PyRatesException(f"Could not find Python (module) directory associated to path `{parentdir}` of Template `{path}`.")

        try:
            abspath = module.__path__
            abspath = abspath[0] if type(abspath) is list else abspath._path[0]
        except TypeError:
            raise PyRatesException(f"Something is wrong with the given YAML template path `{path}`.")

    else:
        raise NotImplementedError(f"Was base specified in template '{path}', but left empty?")
    return (
     template_name, file, abspath)