# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/chrisjsewell/ase-notebook/ase_notebook/data/__init__.py
# Compiled at: 2020-04-09 06:47:30
# Size of source mod 2**32: 689 bytes
"""Module for storing and loading data files."""
import json, importlib_resources
from ase_notebook import data
from ase_notebook.atoms_convert import deserialize_atoms

def load_data_file(name, load_json=True, as_binary=False):
    """Load a data file."""
    if as_binary:
        return importlib_resources.read_binary(data, name)
    else:
        string = importlib_resources.read_text(data, name)
        if load_json:
            if name.endswith('.json'):
                return json.loads(string)
        return string


def get_example_atoms(name='pyrite'):
    """Load an example ase.Atoms instance."""
    data = load_data_file(f"example_{name}.atoms.json", load_json=False)
    return deserialize_atoms(data)