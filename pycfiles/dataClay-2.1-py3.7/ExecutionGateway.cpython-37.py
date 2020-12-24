# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/ExecutionGateway.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 8908 bytes
"""Management of Python Classes.

This module is responsible of management of the Class Objects. A central Python
Metaclass is responsible of Class (not object) instantiation.

Note that this managers also includes most serialization/deserialization code
related to classes and function call parameters.
"""
from decorator import getfullargspec
import inspect
from logging import getLogger
import six
import dataclay.util.management.classmgr.MetaClass as MetaClass
import dataclay.util.management.classmgr.Operation as Operation
import dataclay.util.management.classmgr.Property as Property
import dataclay.util.management.classmgr.Type as Type
from dataclay.util.management.classmgr.Utils import STATIC_ATTRIBUTE_FOR_EXTERNAL_INIT
import dataclay.util.management.classmgr.python.PythonClassInfo as PythonClassInfo
import dataclay.util.management.classmgr.python.PythonImplementation as PythonImplementation
from dataclay.exceptions.exceptions import DataClayException
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'
logger = getLogger(__name__)
loaded_classes = set()
class_extradata_cache_exec_env = dict()
class_extradata_cache_client = dict()

class ExecutionGateway(type):
    __doc__ = 'Python\' Metaclass dataClay "magic"\n\n    This type-derived Metaclass is used by DataClayObject to control the class\n    instantiation and also object instances.\n    '

    def __new__(mcs, classname, bases, dct):
        if classname == 'DataClayObject':
            return super(ExecutionGateway, mcs).__new__(mcs, classname, bases, dct)
        klass = super(ExecutionGateway, mcs).__new__(mcs, classname, bases, dct)
        loaded_classes.add(klass)
        return klass

    def __init__(cls, name, bases, dct):
        logger.verbose('Initialization of class %s in module %s', name, cls.__module__)
        super(ExecutionGateway, cls).__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        if cls.__name__ == 'DataClayObject':
            raise TypeError('Cannot create base objects')
        elif getattr(cls, STATIC_ATTRIBUTE_FOR_EXTERNAL_INIT, False):
            logger.debug('New Persistent Instance (remote init) of class `%s`', cls.__name__)
            raise NotImplementedError('External initialization not implemented')
        else:
            ret = object.__new__(cls)
            logger.debug('New regular dataClay instance of class `%s`', cls.__name__)
            ret._populate_internal_fields()
            (cls.__init__)(ret, *args, **kwargs)
            return ret

    def new_dataclay_instance(cls, deserializing, **kwargs):
        """Return a new instance, without calling to the class methods."""
        logger.debug('New dataClay instance (without __call__) of class `%s`', cls.__name__)
        ret = object.__new__(cls)
        (ret._populate_internal_fields)(deserializing=deserializing, **kwargs)
        return ret

    def _prepare_metaclass(cls, namespace, responsible_account):
        """Build a dataClay "MetaClass" for this class.

        :param str namespace: The namespace for this class' MetaClass.
        :param str responsible_account: Responsible account's username.
        :return: A MetaClass Container.
        """
        try:
            class_extradata = cls.get_class_extradata()
        except AttributeError:
            raise ValueError('MetaClass can only be prepared for correctly initialized DataClay Classes')

        logger.verbose('Preparing MetaClass container for class %s (%s)', class_extradata.classname, class_extradata.full_name)
        current_python_info = PythonClassInfo(imports=(list()))
        current_class = MetaClass(namespace=namespace,
          name=(class_extradata.full_name),
          parentType=None,
          operations=(list()),
          properties=(list()),
          isAbstract=False,
          languageDepInfos={'LANG_PYTHON': current_python_info})
        predicate = inspect.isfunction if six.PY3 else inspect.ismethod
        for name, dataclay_func in inspect.getmembers(cls, predicate):
            if not getattr(dataclay_func, '_dclay_method', False):
                logger.verbose("Method `%s` doesn't have attribute `_dclay_method`", dataclay_func)
                continue
            original_func = dataclay_func._dclay_entrypoint
            logger.debug('MetaClass container will contain method `%s`, preparing', name)
            current_operation = Operation(namespace=namespace,
              className=(class_extradata.full_name),
              descriptor=(str()),
              signature=(str()),
              name=name,
              nameAndDescriptor=name,
              params=(dict()),
              paramsOrder=(list()),
              returnType=(Type.build_from_type(dataclay_func._dclay_ret)),
              implementations=(list()),
              isAbstract=False,
              isStaticConstructor=False)
            signature = getfullargspec(original_func)
            if not signature.varargs:
                if signature.varkw:
                    raise NotImplementedError('No support for varargs or varkw yet')
                current_operation.paramsOrder[:] = signature.args[1:]
                current_operation.params.update({k:Type.build_from_type(v) for k, v in dataclay_func._dclay_args.items()})
                if len(current_operation.paramsOrder) != len(current_operation.params):
                    raise DataClayException('All the arguments are expected to be annotated, there is some error in %s::%s|%s' % (
                     namespace, class_extradata.full_name, name))
                current_implementation = PythonImplementation(responsibleAccountName=responsible_account,
                  namespace=namespace,
                  className=(class_extradata.full_name),
                  opNameAndDescriptor=name,
                  position=0,
                  includes=(list()),
                  accessedProperties=(list()),
                  accessedImplementations=(list()),
                  requiredQuantitativeFeatures=(dict()),
                  requiredQualitativeFeatures=(dict()),
                  code=(inspect.getsource(dataclay_func._dclay_entrypoint)))
                current_operation.implementations.append(current_implementation)
                current_class.operations.append(current_operation)

        for n, p in class_extradata.properties.items():
            current_property = Property(namespace=namespace,
              className=(class_extradata.full_name),
              name=n,
              position=(p.position),
              type=(p.type),
              beforeUpdate=(p.beforeUpdate),
              afterUpdate=(p.afterUpdate),
              inMaster=(p.inMaster))
            current_class.properties.append(current_property)

        current_python_info.imports.extend(class_extradata.imports)
        return current_class