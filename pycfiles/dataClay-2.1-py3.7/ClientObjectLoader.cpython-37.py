# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/loader/ClientObjectLoader.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 4043 bytes
""" Class description goes here. """
import dataclay.loader.DataClayObjectLoader as DataClayObjectLoader
import importlib
import dataclay.commonruntime.ExecutionGateway as ExecutionGateway
from dataclay.serialization.lib.DeserializationLibUtils import DeserializationLibUtilsSingleton

class ClientObjectLoader(DataClayObjectLoader):
    __doc__ = '\n    @summary: This class is responsible to create DataClayObjects and load them with data coming from different resources. All possible\n    constructions of DataClayObject should be included here. All possible "filling instance" use-cases should be managed here.\n    Most lockers should be located here.\n    '

    def __init__(self, theruntime):
        """
        @postcondition: Constructor of the object 
        @param theruntime: Runtime being managed 
        """
        DataClayObjectLoader.__init__(self, theruntime)

    def new_instance(self, class_id, object_id):
        """
        TODO: Refactor this function
        """
        self.logger.verbose('Creating an instance from the class: {%s}', class_id)
        try:
            full_class_name = self.runtime.local_available_classes[class_id]
        except KeyError:
            raise RuntimeError('Class {%s} is not amongst the locally available classes, check contracts and/or initialization' % class_id)

        package_name, class_name = full_class_name.rsplit('.', 1)
        m = importlib.import_module(package_name)
        klass = getattr(m, class_name)
        return ExecutionGateway.new_dataclay_instance(klass, deserializing=True, object_id=object_id)

    def get_or_new_volatile_instance_and_load(self, class_id, object_id, hint, obj_with_data, ifacebitmaps):
        """
        @postcondition: Get from Heap or create a new volatile in EE and load data on it.
        @param class_id: id of the class of the object
        @param object_id: id of the object
        @param hint: hint of the object 
        @param obj_with_data: data of the volatile 
        @param ifacebitmaps: interface bitmaps 
        """
        self.runtime.lock(object_id)
        self.logger.verbose('Get or create new client volatile instance with object id %s in Heap ', str(object_id))
        try:
            volatile_obj = self.runtime.get_from_heap(object_id)
            if volatile_obj is None:
                volatile_obj = self.new_instance_internal(class_id, object_id, hint)
            DeserializationLibUtilsSingleton.deserialize_object_with_data_in_client(obj_with_data, volatile_obj, ifacebitmaps, self.runtime, self.runtime.get_session_id())
            volatile_obj.initialize_object_as_volatile()
        finally:
            self.runtime.unlock(object_id)

        return volatile_obj