# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\frontend\yaml.py
# Compiled at: 2019-06-26 16:26:50
# Size of source mod 2**32: 3472 bytes
__doc__ = ' Some utility functions for parsing YAML-based definitions of circuits and components.\n'
from pyrates.frontend._registry import register_interface
__author__ = 'Daniel Rose'
__status__ = 'Development'

@register_interface
def to_dict(path: str):
    """Load a template from YAML and return the resulting dictionary.

    Parameters
    ----------

    path
        string containing path of YAML template of the form path.to.template or path/to/template.file.TemplateName.
        The dot notation refers to a path that can be found using python's import functionality. The slash notation
        refers to a file in an absolute or relative path from the current working directory.
    """
    from pyrates.frontend.file import parse_path
    template_name, filename, directory = parse_path(path)
    import os
    if '.' in filename:
        filepath = os.path.join(directory, filename)
    else:
        for ext in ('yaml', 'yml'):
            filepath = os.path.join(directory, '.'.join((filename, ext)))
            if os.path.exists(filepath):
                break
        else:
            raise FileNotFoundError(f"Could not identify file with name {filename} in directory {directory}.")

    from ruamel.yaml import YAML
    yaml = YAML(typ='safe', pure=True)
    with open(filepath, 'r') as (file):
        file_dict = yaml.load(file)
    if template_name in file_dict:
        template_dict = file_dict[template_name]
        template_dict['path'] = path
        template_dict['name'] = template_name
    else:
        raise AttributeError(f"Could not find {template_name} in {filepath}.")
    return template_dict


@register_interface
def from_circuit(circuit, path: str, name: str):
    from pyrates.frontend.dict import from_circuit
    dict_repr = {name: from_circuit(circuit)}
    from ruamel.yaml import YAML
    yaml = YAML()
    from pyrates.utility.filestorage import create_directory
    create_directory(path)
    from pathlib import Path
    path = Path(path)
    yaml.dump(dict_repr, path)


@register_interface
def to_template(path: str, template_cls):
    return template_cls.from_yaml(path)