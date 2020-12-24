# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/lineage/datasets.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4340 bytes
import six
from typing import List
from jinja2 import Environment

def _inherited(cls):
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in _inherited(c)])


class DataSet(object):
    attributes = []
    type_name = 'dataSet'

    def __init__(self, qualified_name=None, data=None, **kwargs):
        self._qualified_name = qualified_name
        self.context = None
        self._data = dict()
        self._data.update(dict((key, value) for key, value in six.iteritems(kwargs) if key in set(self.attributes)))
        if data:
            if 'qualifiedName' in data:
                self._qualified_name = data.pop('qualifiedName')
            self._data = dict((key, value) for key, value in six.iteritems(data) if key in set(self.attributes))

    def set_context(self, context):
        self.context = context

    @property
    def qualified_name(self):
        if self.context:
            env = Environment()
            return (env.from_string(self._qualified_name).render)(**self.context)
        else:
            return self._qualified_name

    def __getattr__(self, attr):
        if attr in self.attributes:
            if self.context:
                env = Environment()
                return (env.from_string(self._data.get(attr)).render)(**self.context)
            else:
                return self._data.get(attr)
        raise AttributeError(attr)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __iter__(self):
        for key, value in six.iteritems(self._data):
            yield (key, value)

    def as_dict(self):
        attributes = dict(self._data)
        attributes.update({'qualifiedName': self.qualified_name})
        env = Environment()
        if self.context:
            for key, value in six.iteritems(attributes):
                attributes[key] = (env.from_string(value).render)(**self.context)

        d = {'typeName':self.type_name,  'attributes':attributes}
        return d

    @staticmethod
    def map_type(name):
        for cls in _inherited(DataSet):
            if cls.type_name == name:
                return cls

        raise NotImplementedError('No known mapping for {}'.format(name))


class DataBase(DataSet):
    type_name = 'dbStore'
    attributes = ['dbStoreType', 'storeUse', 'source', 'description', 'userName',
     'storeUri', 'operation', 'startTime', 'endTime', 'commandlineOpts',
     'attribute_db']


class File(DataSet):
    type_name = 'fs_path'
    attributes = ['name', 'path', 'isFile', 'isSymlink']

    def __init__(self, name=None, data=None):
        super(File, self).__init__(name=name, data=data)
        self._qualified_name = 'file://' + self.name
        self._data['path'] = self.name


class HadoopFile(File):
    cluster_name = 'none'
    attributes = ['name', 'path', 'clusterName']
    type_name = 'hdfs_file'

    def __init__(self, name=None, data=None):
        super(File, self).__init__(name=name, data=data)
        self._qualified_name = '{}@{}'.format(self.name, self.cluster_name)
        self._data['path'] = self.name
        self._data['clusterName'] = self.cluster_name


class Operator(DataSet):
    type_name = 'airflow_operator'
    attributes = [
     'dag_id', 'task_id', 'command', 'conn_id', 'name', 'execution_date',
     'start_date', 'end_date', 'inputs', 'outputs']