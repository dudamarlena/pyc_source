# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/commonruntime/ExecutionEnvironmentRuntime.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 24600 bytes
""" Class description goes here. """
import logging, time, uuid, datetime
from dataclay.communication.grpc.messages.common.common_messages_pb2 import LANG_PYTHON
from dataclay.exceptions.exceptions import DataClayException
import dataclay.commonruntime.DataClayRuntime as DataClayRuntime
import dataclay.commonruntime.RuntimeType as RuntimeType
from dataclay.commonruntime.Settings import settings
from dataclay.serialization.lib.SerializationLibUtils import SerializationLibUtilsSingleton
import dataclay.heap.ExecutionEnvironmentHeapManager as ExecutionEnvironmentHeapManager
import dataclay.loader.ExecutionObjectLoader as ExecutionObjectLoader
from dataclay.commonruntime.Runtime import threadLocal
from dataclay.util import Configuration
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)
current_milli_time = lambda : int(round(time.time() * 1000))

class ExecutionEnvironmentRuntime(DataClayRuntime):

    def __init__(self, theexec_env):
        DataClayRuntime.__init__(self)
        self.current_type = RuntimeType.exe_env
        self.execution_environment = theexec_env
        self.references_hold_by_sessions = dict()
        self.quarantine_sessions = set()
        self.session_expires_dates = dict()
        self.alias_references = set()

    def initialize_runtime_aux(self):
        self.dataclay_heap_manager = ExecutionEnvironmentHeapManager(self)
        self.dataclay_object_loader = ExecutionObjectLoader(self)

    def is_exec_env(self):
        return True

    def get_or_new_instance_from_db(self, object_id, retry):
        """
        @postcondition: Get object from memory or database and WAIT in case we are still waiting for it to be persisted.
        @param object_id: ID of object to get or create 
        @param retry: indicates if we should retry and wait 
        """
        return self.dataclay_object_loader.get_or_new_instance_from_db(object_id, retry)

    def load_object_from_db(self, instance, retry):
        """
        @postcondition: Load DataClayObject from Database
        @param instance: DataClayObject instance to fill
        @param retry: Indicates retry loading in case it is not in db.
        """
        return self.dataclay_object_loader.load_object_from_db(instance, retry)

    def get_hint(self):
        """
        @postcondition: Get hint of the current EE 
        @return Hint of current EE
        """
        return settings.environment_id

    def flush_all(self):
        """
        @postcondition: Flush all objects in memory to disk.
        """
        self.dataclay_heap_manager.flush_all()

    def get_session_id(self):
        """
        @postcondition: Get Session ID associated to current thread 
        @return: Session ID associated to current thread 
        """
        return threadLocal.session_id

    def get_execution_environment(self):
        """
        @return: Return execution environment using this runtime 
        """
        return self.execution_environment

    def store_object(self, instance):
        if not instance.is_persistent():
            raise RuntimeError('StoreObject should only be called on Persistent Objects. Ensure to call make_persistent first')
        self.internal_store(instance, make_persistent=False)

    def make_persistent(self, instance, alias, backend_id, recursive):
        """ This method creates a new Persistent Object using the provided stub
        instance and, if indicated, all its associated objects also Logic module API used for communication
        This function is called from a stub/execution class
        :param instance: Instance to make persistent
        :param backend_id: Indicates which is the destination backend
        :param recursive: Indicates if make persistent is recursive
        :param alias: Alias for the object
        :returns: ID of the backend in which te object was persisted.
        :type instance: DataClayExecutionObject
        :type backend_id: DataClayID
        :type recursive: boolean
        :type alias: string
        :rtype: DataClayID
        :raises RuntimeError: if backend id is UNDEFINED_LOCAL.
        """
        self.logger.debug('Starting make persistent object for instance %s with id %s', instance, instance.get_object_id())
        if alias is not None:
            if instance.is_pending_to_register():
                reg_info = [instance.get_object_id(), instance.get_class_extradata().class_id,
                 self.get_session_id(), instance.get_dataset_id()]
                self.ready_clients['@LM'].register_object(reg_info, instance.get_hint(), alias, LANG_PYTHON)
            else:
                self.ready_clients['@LM'].add_alias(instance.get_object_id(), alias)
        return instance.get_location()

    def execute_implementation_aux(self, operation_name, instance, parameters, exeenv_id=None):
        object_id = instance.get_object_id()
        logger.debug('Calling execute_implementation inside EE for operation %s and object id %s', operation_name, object_id)
        under_deserialization = self.check_and_fill_volatile_under_deserialization(instance, None)
        if under_deserialization:
            logger.debug('Object %s is a volatile under deserialization, executing', object_id)
            return self.execution_environment.internal_exec_impl(operation_name, instance, parameters)
        thisExecEnv = settings.environment_id
        using_hint = False
        if exeenv_id is None:
            if instance.get_hint() is not None:
                exeenv_id = instance.get_hint()
                using_hint = True
                logger.debug('Using hint %s for object id %s', exeenv_id, object_id)
            else:
                logger.debug('Asking for EE of object with id %s', object_id)
                exeenv_id = next(iter(self.get_metadata(object_id).locations))
        elif exeenv_id == thisExecEnv:
            logger.debug('Object execution is local')
            try:
                fat_instance = self.execution_environment.get_local_instance(object_id)
                assert instance is fat_instance, 'A tiny mess with get_local_instance and heap management, check that'
                return self.execution_environment.internal_exec_impl(operation_name, fat_instance, parameters)
            except Exception as e:
                try:
                    return self.execution_environment.internal_exec_impl(operation_name, instance, parameters)
                finally:
                    e = None
                    del e

        else:
            logger.debug('Object execution is not local')
            object_id = instance.get_object_id()
            return self.call_execute_to_ds(instance, parameters, operation_name, exeenv_id, using_hint)

    def internal_store(self, instance, make_persistent=True):
        """Perform the storage (StoreObject call) for an instance.
    
        :param instance: The DataClayObject willing to be stored.
        :param make_persistent: Flag, True when DS_STORE_OBJECT should be called
        and False when DS_UPSERT_OBJECT is the method to be called.
        :return: A dictionary containing the classes for all stored objects.
    
        This function works for two main scenarios: the makePersistent one (in
        which the instance is not yet persistent) and the update (in which the
        instance is persistent).
    
        The return dictionary is the same in both cases, but note that the update
        should not use the provided instance for updating metadata to the LM.
        """
        logger.debug('Store procedure for instance %r', instance)
        client = self.ready_clients['@STORAGE']
        pending_objs = [
         instance]
        stored_objects_classes = dict()
        serialized_objs = list()
        reg_infos = list()
        dataset_id = self.execution_environment.thread_local_info.dataset_id
        while pending_objs:
            current_obj = pending_objs.pop()
            current_obj_id = current_obj.get_object_id()
            self.lock(current_obj_id)
            try:
                if not current_obj.is_loaded():
                    current_obj = self.get_or_new_instance_from_db(current_obj_id, False)
                dcc_extradata = current_obj.get_class_extradata()
                object_id = current_obj.get_object_id()
                if make_persistent:
                    if current_obj.is_persistent():
                        continue
                    dcc_extradata = current_obj.get_class_extradata()
                    infos = [object_id, dcc_extradata.class_id,
                     self.execution_environment.thread_local_info.session_id, dataset_id]
                    reg_infos.append(infos)
                current_obj.set_persistent(True)
                current_obj.set_hint(settings.environment_id)
                logger.debug('Setting loaded to true from internal store for object %s' % str(object_id))
                current_obj.set_loaded(True)
                if not object_id:
                    if not make_persistent:
                        raise DataClayException('Objects should never be uuid-less for non-make_persistent use cases')
                    object_id = uuid.uuid4()
                    current_obj.set_object_id(object_id)
                    current_obj.set_dataset_id(self.execution_environment.thread_local_info.dataset_id)
                logger.debug('Ready to make persistent object {%s} of class %s {%s}' % (
                 object_id, dcc_extradata.classname, dcc_extradata.class_id))
                stored_objects_classes[object_id] = dcc_extradata.class_id
                serialized_objs.append(SerializationLibUtilsSingleton.serialize_dcobj_with_data(current_obj, pending_objs, False, None, self, False))
            finally:
                self.unlock(current_obj_id)

        if make_persistent:
            lm_client = self.ready_clients['@LM']
            lm_client.register_objects(reg_infos, settings.environment_id, None, None, LANG_PYTHON)
            client.ds_store_objects(self.execution_environment.thread_local_info.session_id, serialized_objs, False, None)
        else:
            client.ds_upsert_objects(self.execution_environment.thread_local_info.session_id, serialized_objs)

    def get_operation_info(self, object_id, operation_name):
        dcc_extradata = self.get_object_by_id(object_id).get_class_extradata()
        metaclass_container = dcc_extradata.metaclass_container
        operation = metaclass_container.get_operation_from_name(operation_name)
        return operation

    def get_implementation_id(self, object_id, operation_name, implementation_idx=0):
        operation = self.get_operation_info(object_id, operation_name)
        return operation.implementations[0].dataClayID

    def check_and_fill_volatile_under_deserialization(self, volatile_obj, ifacebitmaps):
        """ Check if there is a volatile object with ID provided pending to deserialize and if so, deserialize it since it is needed.
        :param volatile_obj: object to check 
        :param ifacebitmaps: Interface bitmaps for deserialization
        :returns: true if it was filled and volatile, false otherwise
        :type volatile_obj: DataClayObject
        :type ifacebitmaps: dict 
        :rtype: boolean
        """
        object_id = volatile_obj.get_object_id()
        if hasattr(self.thread_local_info, 'volatiles_under_deserialitzation'):
            if self.thread_local_info.volatiles_under_deserialitzation is not None:
                for obj_with_data in self.thread_local_info.volatiles_under_deserialitzation.values():
                    curr_obj_id = obj_with_data[0]
                    if object_id == curr_obj_id:
                        metaclass_id = volatile_obj.get_class_extradata().class_id
                        hint = volatile_obj.get_hint()
                        self.get_or_new_volatile_instance_and_load(object_id, metaclass_id, hint, obj_with_data, ifacebitmaps)
                        return True

        return False

    def add_alias_reference(self, object_id):
        """
        @summary Add +1 reference due to a new alias.
        @param object_id ID of object with alias
        """
        self.alias_references.add(object_id)

    def add_session_reference(self, object_id):
        """
        @summary Add +1 reference associated to thread session
        @param object_id ID of object.
        """
        session_id = self.get_session_id()
        if session_id is None:
            return
        elif object_id not in self.references_hold_by_sessions:
            self.lock(object_id)
            try:
                if object_id not in self.references_hold_by_sessions:
                    session_refs = set()
                    self.references_hold_by_sessions[object_id] = session_refs
            finally:
                self.unlock(object_id)

        else:
            session_refs = self.references_hold_by_sessions.get(object_id)
        session_refs.add(session_id)
        if session_id not in self.session_expires_dates:
            if Configuration.CHECK_SESSION:
                pass
            else:
                expiration_date = Configuration.NOCHECK_SESSION_EXPIRATION
            self.lock(session_id)
            try:
                self.session_expires_dates[session_id] = expiration_date
            finally:
                self.unlock(session_id)

    def close_session_in_ee(self, session_id):
        """
        @summary Close session in EE. Subtract session references for GC.
        @param session_id ID of session closing.
        """
        logger.debug('[==DGC==] Closing session %s' % str(session_id))
        self.session_expires_dates[session_id] = datetime.datetime.now()

    def get_retained_references(self):
        """
        @summary Get retained refs by this EE
        @return Retained refs (alias, sessions, ...)
        """
        logger.debug('Getting retained references')
        retained_refs = list()
        retained_refs.extend(self.dataclay_heap_manager.get_object_ids_retained())
        logger.debug('Obtained retained references in memory: %s ' % str(len(retained_refs)))
        now = datetime.datetime.now()
        sessions_to_close = set()
        for oid in list(self.references_hold_by_sessions.keys()):
            sessions_of_obj = self.references_hold_by_sessions.get(oid)
            logger.debug('[==DGC==] Object %s is retained by sessions %s' % (oid, str(sessions_of_obj)))
            for cur_session in list(sessions_of_obj):
                session_expired = False
                expired_date = self.session_expires_dates.get(cur_session)
                print(expired_date)
                if expired_date is not None:
                    if now > expired_date:
                        if cur_session in self.quarantine_sessions:
                            session_expired = True
                            cur_expired_date = self.session_expires_dates.get(cur_session)
                            if cur_expired_date is not None:
                                if now > cur_expired_date:
                                    sessions_to_close.add(cur_session)
                                else:
                                    self.quarantine_sessions.add(cur_session)
                        else:
                            pass
                if expired_date is not None and now < expired_date:
                    if cur_session in self.quarantine_sessions:
                        self.quarantine_sessions.remove(cur_session)
                    if session_expired:
                        sessions_of_obj.remove(cur_session)
                        logger.debug('Session %s expired' % str(cur_session))
                        if not self.dataclay_heap_manager.exists_in_heap(oid):
                            if len(sessions_of_obj) == 0:
                                logger.debug('Removing session reference for oid %s' % str(oid))
                                for oid, oid_ref in self.references_hold_by_sessions.items():
                                    oid_ref.discard(cur_session)

                                print(self.references_hold_by_sessions)
                else:
                    retained_refs.append(oid)

        for session_to_close in sessions_to_close:
            obj_using_session = False
            for sessions_of_obj in self.references_hold_by_sessions.values():
                if session_to_close in sessions_of_obj:
                    obj_using_session = True
                    break

            if not obj_using_session:
                del self.session_expires_dates[session_to_close]

        logger.debug('Retained references %s' % str(retained_refs))
        return retained_refs

    def get_from_sl(self, object_id):
        """ Get from SL associated to this EE. 
        :param object_id: id of the object to get 
        :type object_id: ObjectID 
        :returns: Bytes of object
        :rtype: Byte array
        """
        return self.ready_clients['@STORAGE'].get_from_db(settings.environment_id, object_id)

    def update_to_sl(self, object_id, obj_bytes, dirty):
        """ Update to SL associated to this EE. 
        :param object_id: id of the object  
        :param obj_bytes: bytes to update
        :param dirty: indicates if object is dirty or not
        :returns: None
        :type object_id: ObjectID 
        :type obj_bytes: Byte array 
        :type dirty: Boolean
        :rtype: None
        """
        return self.ready_clients['@STORAGE'].update_to_db(settings.environment_id, object_id, obj_bytes, dirty)