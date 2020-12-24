# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/util/tools/python/PythonMetaClassFactory.py
# Compiled at: 2019-11-11 07:06:07
# Size of source mod 2**32: 3796 bytes
""" Class description goes here. """
from dataclay import DataClayObject
from importlib import import_module
import logging
from dataclay.commonruntime.ExecutionGateway import loaded_classes
import dataclay.util.management.classmgr.UserType as UserType
from dataclay.exceptions.exceptions import DataClayException
import traceback
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)

class MetaClassFactory(object):
    __doc__ = 'Tracker of classes and generator of dataClay MetaClasses.\n\n    One of the functions of this class is managing a set of classes, which\n    may have cross dependencies between them. Additionally, this factory helps\n    to manage a set of MetaClasses (prior to a registration process).\n\n    The keyword parameters are used to complete the containers for the\n    MetaClass being registered.\n    '

    def __init__(self, namespace, responsible_account):
        """Simple class initialization.

        :param str namespace: The string of the namespace.
        :param str responsible_account: The registrator account (username).
        """
        self.classes = list()
        self.types = dict()
        self._responsible_account = responsible_account
        self._namespace = namespace
        self._prefix = None
        self._ignored_prefixes = -1

    def import_and_add(self, import_str):
        """Perform a import operation while adding classes.

        This method calls to importlib.import_module, while watching the
        StorageObject classes that are being loaded. All the classes that are
        loaded as a result of the import will be added to this factory.

        :param import_str: A string that can be used as parameter to import_module.
        """
        loaded_classes.clear()
        try:
            import_module(import_str)
        except ImportError as e:
            try:
                traceback.print_exc()
                logger.warning('Tried to import `%s` and failed, ignoring', import_str)
                logger.warning('Error: %s', e)
            finally:
                e = None
                del e

        else:
            for k in loaded_classes:
                if k.__module__.startswith('dataclay'):
                    continue
                else:
                    self.add_class(k)

    def add_class(self, klass):
        """Add a class to this factory, from the class' Python object.

        Note that the caller provides de class, which should be an instance of
        ExecutionGateway.

        :param klass: The class object.
        """
        if not issubclass(klass, DataClayObject):
            raise DataClayException('Can only use DataClayObject classes')
        logger.verbose('Adding class %s to the MetaClassFactory', klass)
        class_container = klass._prepare_metaclass(self._namespace, self._responsible_account)
        complete_name = class_container.name
        logger.debug('[add_class] Using `%s` as `name` field of Type', complete_name)
        if complete_name not in self.types:
            self.types[complete_name] = UserType(signature=('L{};'.format(complete_name).replace('.', '/')),
              includes=[],
              namespace=(self._namespace),
              typeName=complete_name)
        self.classes.append(class_container)
        parent = klass.__bases__[0]
        if parent is not DataClayObject:
            self.add_class(parent)
        logger.debug('Class %s finished', class_container.name)

    def __str__(self):
        return 'MetaClass Factory containing:\n{}'.format(str(self.classes))