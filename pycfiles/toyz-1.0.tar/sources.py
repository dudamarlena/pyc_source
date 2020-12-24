# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/data-beta/users/fmooleka/git_projects/toyz/toyz/utils/sources.py
# Compiled at: 2015-08-06 17:07:51
"""
Functions and classes for workspace data sources and image sources
"""
from __future__ import print_function, division
import numpy as np
from datetime import datetime
import warnings
from collections import OrderedDict
import toyz.utils.io
from toyz.utils import core
from toyz.utils.errors import ToyzDataError
from toyz.web import session_vars

class DataSource:

    def __init__(self, module_info, data=None, data_type=None, data_kwargs={}, paths={}, user_id='', **kwargs):
        if not all([ k in ('data', 'meta', 'log') for k in paths ]):
            raise ToyzDataError("'paths' must be a dict of file parameters with the keys 'data', 'meta', 'log'")
        path_options = {'toyz_module': '', 
           'io_module': '', 
           'file_type': '', 
           'file_options': {}}
        default_paths = {f:dict(path_options) for f in ['data', 'meta', 'log']}
        self.user_id = user_id
        self.paths = core.merge_dict(default_paths, paths)
        if self.paths['data']['toyz_module'] == 'toyz':
            self.data_module = toyz.utils.sources
        else:
            import importlib
            self.data_module = importlib.import_module(self.paths['data']['toyz_module'])
        self.set_data(data, data_type, data_kwargs)
        default_options = {'selected': [], 'meta': {'creation': {'time': datetime.now(), 
                                 'software': 'unknown'}}, 
           'links': {}, 'log': [], 'fillna': 'NaN'}
        options = core.merge_dict(default_options, kwargs, True)
        for k, v in options.items():
            setattr(self, k, v)

    def name_columns(self, columns=None):
        self.columns = None
        if columns is not None:
            self.columns = columns
            if self.data_type == 'pandas.core.frame.DataFrame':
                self.data.columns = columns
        if self.data_type == 'pandas.core.frame.DataFrame':
            self.columns = self.data.columns.values.tolist()
        elif self.data_type == 'numpy.ndarray':
            if len(self.data.dtype) == 0:
                self.columns = [ 'col-' + str(n) for n in range(self.data.shape[1]) ]
            else:
                self.columns = list(self.data.dtype.names)
        if self.columns is None:
            warnings.warn('Unable to load column names for the given data type')
            self.columns = [ ('col{0}').format(n) for n in range(len(self.data[0])) ]
        return self.columns

    def check_instance(self, data, data_kwargs={}):
        if isinstance(data, np.ndarray):
            self.data = np.ndaray(data, **data_kwargs)
            self.data_type = 'numpy.ndarray'
        elif isinstance(data, list):
            self.data = data
            self.data_type = 'list'
        else:
            try:
                from pandas import DataFrame
                if isinstance(data, DataFrame):
                    self.data = DataFrame(data, **data_kwargs)
                    self.data_type = 'pandas.core.frame.DataFrame'
            except ImportError:
                pass

        return self.data_type is None

    def set_data(self, data=None, data_type=None, data_kwargs={}):
        """
        Set the data for the given source based on the data type or a user specified type
        """
        import toyz.utils.io
        if data is None:
            print('DATA IS NONE')
            if self.paths['data']['io_module'] == '':
                raise ToyzDataError('You must supply a data object or file info to initialize a DataSource')
            else:
                self.data = toyz.utils.io.load_data(**self.paths['data'])
                if data_type is None:
                    self.data_type = type(self.data).__module__ + '.' + type(self.data).__name__
                else:
                    self.data_type = data_type
        elif data_type is None:
            module_info = core.get_module_info(toyz_settings, tid, params)
            for data_source in module_info['data_sources']:
                if data_source.check_instance(data, data_kwargs):
                    break

        else:
            self.data_type = data_type
            if data_type == 'pandas.core.frame.DataFrame':
                from pandas import DataFrame
                self.data = DataFrame(data, **data_kwargs)
            elif data_type == 'numpy.ndarray':
                self.data = numpy.ndarray(data, **data_kwargs)
            elif data_type == 'list':
                self.data = list(data)
                if 'columns' in data_kwargs:
                    self.columns = data_kwargs['columns']
                else:
                    self.columns = [ 'col-' + n for n in range(len(self.data)) ]
            else:
                self.data = data
                self.data_type = data_type
        self.name_columns()
        return

    def to_dict(self, columns=None):
        """
        Convert columns of a data object into a dictionary with column names as the keys
        and a python list as the values. This is useful for json encoding the dataset
        so that it can be sent to the client.
        """

        def isnan(x):
            if np.isnan(x):
                return 'NaN'
            else:
                return x

        if columns is None:
            columns = self.columns
        if self.data_type == 'pandas.core.frame.DataFrame':
            data_dict = {col:self.data[col].astype(object).fillna(self.fillna).values.tolist() for col in columns}
        elif self.data_type == 'numpy.ndarray':
            import numpy as np
            data_dict = {col:map(isnan, data[col].tolist()) for col in columns}
        elif self.data_type == 'list':
            col_indices = [ self.columns.index(col) for col in columns ]
            data_dict = {col:[ isnan(self.data[i][col_indices[n]]) for i in range(len(self.data)) ] for n, col in enumerate(columns)}
        else:
            data_dict = self.data_module.data_types[self.data_type].to_dict(self.data, columns)
        return data_dict

    def save(self, save_paths={}):
        """
        Save the DataSource and, if applicable, the metadata and log.
        """
        for data_type, file_info in self.paths.items():
            if file_info['io_module'] != '':
                save_path = dict(file_info)
                save_path['file_options'] = toyz.utils.io.convert_options(file_info['toyz_module'], file_info['io_module'], file_info['file_type'], file_info['file_options'], 'load2save')
                if data_type in save_paths:
                    core.merge_dict(save_path, save_paths[data_type])
            elif data_type == 'data':
                raise ToyzDataError("You must supply 'toyz_module', 'io_module', 'file_type', and 'file_options' to save")
            elif data_type in save_paths:
                save_path = save_paths[data_type]
            else:
                save_path = None
            if save_path is not None:
                print(data_type, save_path)
                self.paths[data_type]['file_options'] = toyz.utils.io.save_data(self.data, save_path['toyz_module'], save_path['io_module'], save_path['file_type'], save_path['file_options'])
            else:
                print('No path for data_type', data_type)

        print('self.path', self.paths)
        return self.paths['data']['file_options']

    def remove_rows(self, points):
        if self.data_type == 'pandas.core.frame.DataFrame':
            import numpy as np
            self.data.drop(self.data.index[points], inplace=True)
        elif self.data_type == 'numpy.ndarray':
            import numpy as np
            np.delete(self.data, np.array(points))
        elif self.data_type == 'list':
            for p in points:
                del self.data[p]

        else:
            data_dict = self.data_module.data_types[self.data_type].remove_data_points(self.data, points)


class ImageSource:
    pass


data_types = [
 'pandas.core.frame.DataFrame', 'numpy.ndarray', 'list']
image_types = ['fits', 'hdf', 'other']
src_types = OrderedDict([
 [
  'DataSource', DataSource],
 [
  'ImageSource', ImageSource]])