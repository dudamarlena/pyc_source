# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/DataClayObjProperties.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 5275 bytes
""" Class description goes here. """
from collections import namedtuple
import logging
from dataclay.commonruntime.Runtime import getRuntime
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2016 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)
DCLAY_PROPERTY_PREFIX = '_dataclay_property_'
DCLAY_GETTER_PREFIX = '$$get'
DCLAY_SETTER_PREFIX = '$$set'
DCLAY_REPLICATED_SETTER_PREFIX = '$$rset'
PreprocessedProperty = namedtuple('PreprocessedProperty', field_names=[
 'name', 'position', 'type', 'beforeUpdate', 'afterUpdate', 'inMaster'])

class DynamicProperty(property):
    __doc__ = 'DataClay implementation of the `property` Python mechanism.\n\n    This class is similar to property but is not expected to be used with\n    decorators. Instead, the initialization is done from the ExecutionGateway\n    metaclass, containing the required information about the property\n    '
    __slots__ = ('p_name', )

    def __init__(self, property_name):
        logger.debug('Initializing DynamicProperty %s', property_name)
        self.p_name = property_name

    def __get__(self, obj, type_=None):
        """Getter for the dataClay property

        If the object is loaded, perform the getter to the local instance (this
        is the scenario for local instances and Execution Environment fully
        loaded instances).

        If the object is not loaded, perform a remote execution (this is the
        scenario for client remote instances and also Execution Environment
        non-loaded instances, which may either "not-yet-loaded" or remote)
        """
        is_exec_env = getRuntime().is_exec_env()
        logger.debug('Calling getter for property %s in %s', self.p_name, 'an execution environment' if is_exec_env else 'the client')
        if not (is_exec_env and obj.is_loaded()):
            if not is_exec_env:
                if not obj.is_persistent():
                    try:
                        obj.set_dirty(True)
                        return object.__getattribute__(obj, '%s%s' % (DCLAY_PROPERTY_PREFIX, self.p_name))
                    except AttributeError:
                        logger.warning('Received AttributeError while accessing property %s on object %r', self.p_name, obj)
                        logger.debug('Internal dictionary of the object: %s', obj.__dict__)
                        raise

            return getRuntime().execute_implementation_aux(DCLAY_GETTER_PREFIX + self.p_name, obj, (), obj.get_hint())

    def __set__(self, obj, value):
        """Setter for the dataClay property

        See the __get__ method for the basic behavioural explanation.
        """
        logger.debug('Calling setter for property %s', self.p_name)
        is_exec_env = getRuntime().is_exec_env()
        is_exec_env and obj.is_loaded() or is_exec_env or obj.is_persistent() or object.__setattr__(obj, '%s%s' % (DCLAY_PROPERTY_PREFIX, self.p_name), value)
        if is_exec_env:
            obj.set_dirty(True)
        else:
            getRuntime().execute_implementation_aux(DCLAY_SETTER_PREFIX + self.p_name, obj, (value,), obj.get_hint())


class ReplicatedDynamicProperty(DynamicProperty):

    def __init__(self, property_name, before_method, after_method, in_master):
        logger.debug('Initializing ReplicatedDynamicProperty %s | BEFORE = %s | AFTER = %s | INMASTER = %s', property_name, before_method, after_method, in_master)
        super(ReplicatedDynamicProperty, self).__init__(property_name)
        self.beforeUpdate = before_method
        self.afterUpdate = after_method
        self.inMaster = in_master

    def __set__(self, obj, value):
        """Setter for the dataClay property

        See the __get__ method for the basic behavioural explanation.
        """
        logger.debug('Calling replicated setter for property %s', self.p_name)
        is_client = not getRuntime().is_exec_env()
        if is_client:
            obj.is_persistent() or object.__setattr__(obj, '%s%s' % (DCLAY_PROPERTY_PREFIX, self.p_name), value)
        else:
            if not is_client:
                obj.is_loaded() or getRuntime().execute_implementation_aux(DCLAY_SETTER_PREFIX + self.p_name, obj, (value,), obj.get_hint())
            else:
                if self.inMaster:
                    logger.debug('Calling update in master [%s] for property %s with value %s', obj.get_master_location, self.p_name, value)
                    getRuntime().execute_implementation_aux('__setUpdate__', obj, (obj, self.p_name, value, self.beforeUpdate, self.afterUpdate), obj.get_master_location())
                else:
                    logger.debug('Calling update locally for property %s with value %s', self.p_name, value)
                    obj.__setUpdate__(obj, self.p_name, value, self.beforeUpdate, self.afterUpdate)
                obj.set_dirty(True)