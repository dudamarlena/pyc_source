# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/loader/DataClayObjectLoader.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 4093 bytes
""" Class description goes here. """
import logging
from abc import ABCMeta, abstractmethod
import six

@six.add_metaclass(ABCMeta)
class DataClayObjectLoader(object):
    __doc__ = '\n    @summary: This class is responsible to create DataClayObjects and load them with data coming from different resources. All possible\n    constructions of DataClayObject should be included here. All possible "filling instance" use-cases should be managed here.\n    Most lockers should be located here.\n    '
    logger = logging.getLogger(__name__)

    def __init__(self, theruntime):
        """
        Constructor
        @param theruntime: Runtime being managed. 
        """
        self.runtime = theruntime

    @abstractmethod
    def new_instance(self, class_id, object_id):
        """ 
        @postcondition: create a new instance using proper class. This function is abstract.
        @param class_id: id of the class of the object.
        @param object_id: id of the object to get/create
        @return instance with object id provided
        """
        pass

    def new_instance_internal(self, class_id, object_id, hint):
        """ 
        @postcondition: create a new instance. 
        @param class_id: id of the class of the object. Can be none. If none, means that class_id should be obtained from metadata of the obj.
        @param object_id: id of the object to get/create
        @param hint: hint of the object in case it is created. 
        @return instance with object id provided
        """
        obj = self.new_instance(class_id, object_id)
        if hint is not None:
            obj.set_hint(hint)
        return obj

    def get_or_new_persistent_instance(self, class_id, object_id, hint):
        """
        @postcondition: check if instance is in heap. if so, return it. otherwise, create a new persistent instance with proper flags.
        @param class_id: id of class of the instance. Can be none. If none, means that class_id should be obtained from metadata of the obj.
        @param object_id: id of the object to get/create
        @param hint: hint of the object in case it is created. 
        @return instance with object id provided
        """
        self.logger.verbose('Get or create new persistent instance with object id %s in Heap ', str(object_id))
        obj = self.runtime.get_from_heap(object_id)
        if obj is None:
            self.logger.debug('Object %s not found in heap', object_id)
            self.runtime.lock(object_id)
            try:
                obj = self.runtime.get_from_heap(object_id)
                if obj is None:
                    self.logger.debug('Creating new instance for %s', object_id)
                    obj = self.new_instance_internal(class_id, object_id, hint)
                obj.initialize_object_as_persistent()
            finally:
                self.runtime.unlock(object_id)

        else:
            self.logger.debug('Object %s found in heap', object_id)
            if obj is None:
                self.logger.debug('Object %s found in heap IS NONE', object_id)
        return obj

    @abstractmethod
    def get_or_new_volatile_instance_and_load(self, class_id, object_id, hint, obj_with_data, ifacebitmaps):
        """
        @postcondition: Get from Heap or create a new volatile in EE and load data on it.
        @param class_id: id of the class of the object
        @param object_id: id of the object
        @param hint: hint of the object 
        @param obj_with_data: data of the volatile 
        @param ifacebitmaps: interface bitmaps 
        """
        pass