# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: e:\01_work\15_phd\11_python_neural_mass_models\pyrates\pyrates\utility\filestorage.py
# Compiled at: 2019-07-12 12:51:27
# Size of source mod 2**32: 11805 bytes
__doc__ = ' Utility functions to store Circuit configurations and data in JSON files\nand read/construct circuit from JSON.\n'
from collections import OrderedDict
from typing import Generator, Tuple, Any, Union, List, Dict
from networkx import node_link_data
from inspect import getsource
import numpy as np, json
from pandas import DataFrame
import pandas as pd
__author__ = 'Daniel Rose'
__status__ = 'Development'

class CustomEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        else:
            if isinstance(obj, np.floating):
                return float(obj)
            else:
                if isinstance(obj, np.ndarray):
                    return obj.tolist()
                if hasattr(obj, 'to_json'):
                    return obj.to_dict()
                if callable(obj):
                    return getsource(obj)
            return super().default(obj)


class RepresentationBase(object):
    """RepresentationBase"""

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        _init_dict = {**kwargs}
        if args:
            _init_dict['args'] = args
        instance._init_dict = _init_dict
        return instance

    def __repr__(self) -> str:
        """Magic method that returns to repr(object). It retrieves the signature of __init__ and maps it to class
        attributes to return a representation in the form 'module.Class(arg1=x, arg2=y, arg3=3)'. Raises AttributeError,
        if the a parameter in the signature cannot be found (is not saved). The current implementation """
        from copy import copy
        init_dict = copy(self._init_dict)
        param_str = '*args, **kwargs'
        _module = self.__class__.__module__
        _class = self.__class__.__name__
        try:
            return f"{_class} '{self.key}'"
        except AttributeError:
            return (f"{_class}")

    def _defaults(self) -> Generator[(Tuple[(str, Any)], None, None)]:
        """Inspects the __init__ special method and yields tuples of init parameters and their default values."""
        import inspect
        sig = inspect.signature(self.__init__)
        for name, param in sig.parameters.items():
            if np.all(param.default != inspect.Parameter.empty):
                yield (name, param.default)

    def to_dict(self, include_defaults=False, include_graph=False, recursive=False) -> OrderedDict:
        """Parse representation string to a dictionary to later convert it to json."""
        _dict = OrderedDict()
        _dict['class'] = {'__module__':self.__class__.__module__,  '__name__':self.__class__.__name__}
        for name, value in self._init_dict.items():
            _dict[name] = value

        if include_defaults:
            default_dict = {}
            for name, value in self._defaults():
                if name not in _dict:
                    default_dict[name] = value

            _dict['defaults'] = default_dict
        else:
            if include_graph:
                if hasattr(self, 'network_graph'):
                    net_dict = node_link_data(self.network_graph)
                    if recursive:
                        for node in net_dict['nodes']:
                            node['data'] = node['data'].to_dict(include_defaults=include_defaults, recursive=True)

                    _dict['network_graph'] = net_dict
        if recursive:
            for key, item in _dict.items():
                if hasattr(item, 'to_dict'):
                    _dict[key] = item.to_dict(include_defaults=include_defaults, recursive=True)

        return _dict

    def to_json(self, include_defaults=False, include_graph=False, path='', filename=''):
        """Parse a dictionary into """
        _dict = self.to_dict(include_defaults=include_defaults, include_graph=include_graph, recursive=True)
        if filename:
            import os
            filepath = os.path.join(path, filename)
            create_directory(filepath)
            if not filepath.lower().endswith('.json'):
                filepath = f"{filepath}.json"
            with open(filepath, 'w') as (outfile):
                json.dump(_dict, outfile, cls=CustomEncoder, indent=4)
        return json.dumps(_dict, cls=CustomEncoder, indent=2)


def get_simulation_data(circuit, state_variable='membrane_potential', pop_keys: Union[(tuple, list)]=None, time_window: tuple=None) -> Tuple[(dict, DataFrame)]:
    """Obtain all simulation data from a circuit, including run parameters"""
    run_info = circuit.run_info
    states = circuit.get_population_states(state_variable=state_variable, population_keys=pop_keys, time_window=time_window)
    labels = [pop for pop in circuit.populations.keys() if 'dummy' not in pop]
    states = DataFrame(data=states, index=(run_info.index), columns=labels)
    return (
     run_info, states)


def save_simulation_data_to_file(output_data: DataFrame, run_info: dict, dirname: str, path: str='', out_format: str='csv'):
    """Save simulation output and inputs that were given to the run function to a file."""
    import os
    dirname = os.path.join(path, dirname) + '/'
    create_directory(dirname)
    filename = f"output.{out_format}"
    filepath = os.path.join(dirname, filename)
    if out_format == 'json':
        output_data.to_json(filepath, orient='split')
    else:
        if out_format == 'csv':
            output_data.to_csv(filepath, sep='\t')
        else:
            raise ValueError(f"Unknown output format '{out_format}'")
    if 'time_vector' in run_info:
        run_info.pop('time_vector')
    for key, item in run_info.items():
        filename = f"{key}.{out_format}"
        filepath = os.path.join(dirname, filename)
        if item is None:
            pass
        else:
            if out_format == 'json':
                item.to_json(filepath, orient='split')
            else:
                item.to_csv(filepath, sep='\t')


def create_directory(path):
    """check if a directory exists and create it otherwise"""
    import os, errno
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise


def read_simulation_data_from_file(dirname: str, path='', filenames: list=None) -> Dict[(str, DataFrame)]:
    """Read simulation data from files. The assumed data structure is:
    <path>/<dirname>/
        output.csv
        synaptic_inputs.csv
        extrinsic_current.csv
        extrinsic_modulation.csv

    This is the expected output from 'save_simulation_data_to_file', but if 'names' is specified, other data
    may also be read.
    """
    import os
    if filenames is None:
        filenames = [
         'output', 'synaptic_inputs', 'extrinsic_current', 'extrinsic_modulation']
        ignore_missing = True
    else:
        ignore_missing = False
    data = {}
    path = os.path.join(path, dirname)
    for label in filenames:
        if label == 'output':
            header = 0
        else:
            header = [
             0, 1]
        filename = label + '.csv'
        filepath = os.path.join(path, filename)
        try:
            data[label] = pd.read_csv(filepath, sep='\t', header=header, index_col=0)
        except FileNotFoundError:
            if not ignore_missing:
                raise

    return data