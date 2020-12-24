# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/management/classmgr/MetaClass.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 5308 bytes
""" Class description goes here. """
from lru import LRU
from dataclay.util.MgrObject import ManagementObject
from .Type import Type
from .Utils import STATIC_ATTRIBUTE_FOR_EXTERNAL_INIT, stub_only_def, py_code

class MetaClass(ManagementObject):
    _fields = [
     'dataClayID',
     'namespace',
     'name',
     'parentType',
     'properties',
     'operations',
     'isAbstract',
     'languageDepInfos',
     'ecas']
    _internal_fields = [
     'namespaceID',
     '_implementation_id_to_operation_cache']
    _typed_fields = {'parentType': Type}

    def get_operation_from_name(self, op_name):
        """Return the operation from its name."""
        for op in self.operations:
            if op.name == op_name:
                return op

        raise KeyError('Operation with name %s was not found in dataClay class %s' % (
         op_name, self.name))

    def get_operation(self, implementation_id):
        """Return an Operation (management object) from an ImplementationID

        :param uuid.UUID implementation_id: The requested ImplementationID

        Given the UUID for a certain Implementation, lookup and return the
        corresponding Operation. Note that this method is memoized (cached) in
        order to improve performance (given that the lookup is slow).
        """
        if not hasattr(self, '_implementation_id_to_operation_cache'):
            setattr(self, '_implementation_id_to_operation_cache', LRU(50))
        try:
            return self._implementation_id_to_operation_cache[implementation_id]
        except KeyError:
            pass

        for op in self.operations:
            for imp in op.implementations:
                if imp.dataClayID == implementation_id:
                    self._implementation_id_to_operation_cache[implementation_id] = op
                    return op

        raise KeyError('Operation for ImplementationID {%s} not found in class %s (in namespace %s)' % (
         implementation_id, self.name, self.namespace))

    def juxtapose_code(self, exeenv_flag=False):
        """Return the complete source code for the current MetaClass.

        :param exeenv_flag: Set to true to generate code for the ExecutionEnvironment.
        :return: A valid source for this class.

        Note that this class will use the "local_implementation" of its
        operations > implementations when available. Undefined behaviour if
        not available.

        In scenarios where implementations are *not* `PythonImplementation` a
        pure-stub (intended for only persistent work mode) function is used. If
        the constructor is one of those non-Python methods, then the class is
        flagged as EXTERNAL_INIT only (see ExecutionGateway for further info).
        """
        import dataclay.util.management.classmgr.python.PythonImplementation as PythonImplementation
        imp_codes = list()
        ops_done = set()
        for op in self.operations:
            if op.name.startswith('$$'):
                continue
            else:
                if op.name in ops_done:
                    continue
                ops_done.add(op.name)
                if len(op.implementations) != 1:
                    raise NotImplementedError('Found %d operations, but currently I only support one' % op.implementations)
                imp = op.implementations[0]
                if isinstance(imp, PythonImplementation):
                    imp_codes.append(imp.code)
            if not op.name == '__init__':
                if op.name == '<init>':
                    imp_codes.append('\n    %s = %s' % (
                     STATIC_ATTRIBUTE_FOR_EXTERNAL_INIT, str(True)))
                    op.name = '__init__'
                imp_codes.append(stub_only_def.render({'func_name':op.name, 
                 'param_names':op.paramsOrder}))

        return py_code.render({'class_name':self.name.rsplit('.', 1)[-1], 
         'parent_name':self.parentType.typeName if self.parentType else 'DataClayObject', 
         'metaclass':self, 
         'imp_codes':imp_codes})