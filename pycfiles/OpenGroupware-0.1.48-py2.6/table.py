# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/tables/table.py
# Compiled at: 2012-10-12 07:02:39
import logging, inspect, yaml, uuid
from coils.foundation import *
from coils.core import *

class Table(object):
    _TABLES = None

    def __init__(self, context=None, process=None, scope=None):
        self.log = logging.getLogger('workflow')
        self.c = {'name': uuid.uuid4().hex}
        self.setup(context=context, process=process, scope=scope)

    def setup(self, context=None, process=None, scope=None):
        self._context = context
        self._process = process
        self._scope = scope

    @property
    def context(self):
        if self._context:
            return self._context
        self.log.warn(('Generating default Anonymous context for table "{0}", application should supply a context.').format(self))
        self._context = AnonymousContext()
        return self._context

    def set_description(self, fd):
        """ Abstract function; child class must implement."""
        pass

    def lookup_value(self, value):
        raise Exception('lookup_value for this Table type not implemented')

    def shutdown(self):
        pass

    @property
    def name(self):
        return self.c.get('name')

    def as_yaml(self):
        return yaml.dump(self.c, default_flow_style=False, indent=2)

    @staticmethod
    def Load_Table_Types():
        Table._TABLES = {}
        bundle = __import__('coils.logic.workflow.tables', fromlist=['*'])
        for (name, data) in inspect.getmembers(bundle, inspect.isclass):
            if data.__module__[:len(bundle.__name__)] == bundle.__name__:
                if issubclass(data, Table):
                    logging.getLogger('workflow').info(('Table class {0} loaded').format(name))
                    Table._TABLES[name] = data
                else:
                    logging.getLogger('workflow').info(('Class {0} not loaded').format(name))

    @staticmethod
    def Marshall(name):
        if Table._TABLES is None:
            Table.Load_Table_Types()
        if name in Table._TABLES:
            return Table._TABLES.get(name)()
        else:
            return

    @staticmethod
    def Load(name):
        handle = BLOBManager.Open(Table.Filename(name), 'rb', encoding='binary')
        if handle:
            try:
                try:
                    description = yaml.load(handle)
                except Exception, e:
                    raise CoilsException(('Table definition "{0}" is corrupted').format(name))

            finally:
                BLOBManager.Close(handle)

            table = Table.Marshall(description.get('class'))
            table.set_description(description)
            return table
        raise CoilsException(('Table named "{0}" does not exist.').format(name))

    @staticmethod
    def Save(table):
        filename = Table.Filename(table.name)
        handle = BLOBManager.Create(filename, encoding='binary')
        handle.write(yaml.dump(table.c))
        BLOBManager.Close(handle)

    @staticmethod
    def Filename(name):
        return ('wf/t/{0}.yaml').format(name)

    @staticmethod
    def Delete(name):
        return BLOBManager.Delete(Table.Filename(name))

    @staticmethod
    def List():
        result = []
        for name in BLOBManager.List('wf/t/'):
            result.append(name[:-5])

        return result