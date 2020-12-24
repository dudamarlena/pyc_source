# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/serialization/lib/DeserializationLibUtils.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 16657 bytes
""" Class description goes here. """
from io import BytesIO
import logging
from dataclay.exceptions.exceptions import InvalidPythonSignature
import dataclay.serialization.python.lang.IntegerWrapper as IntegerWrapper
import dataclay.serialization.python.lang.VLQIntegerWrapper as VLQIntegerWrapper
import dataclay.serialization.python.util.PyTypeWildcardWrapper as PyTypeWildcardWrapper
import dataclay.communication.grpc.messages.common.common_messages_pb2 as common_messages
from dataclay.communication.grpc.Utils import get_metadata
__author__ = 'Alex Barcelo <alex.barcelo@bsc.es>'
__copyright__ = '2015 Barcelona Supercomputing Center (BSC-CNS)'
logger = logging.getLogger(__name__)

class DeserializationLibUtils(object):

    def deserialize_params(self, serialized_params_or_return, iface_bitmaps, param_specs, params_order, runtime):
        return self.deserialize_params_or_return(serialized_params_or_return, iface_bitmaps, param_specs, params_order, runtime)

    def _create_buffer_and_deserialize(self, obj_bytes, instance, ifacebitmaps, metadata, cur_deser_python_objs):
        """
        @postcondition: Create buffer and deserialize
        @param obj_bytes: bytes to deserialize
        @param instance: Instance to deserialize
        @param ifacebitmaps: Map of bitmaps representing the interfaces to use
        @param metadata: object metadata
        @param cur_deser_python_objs: Currently deserialized Java objects
        """
        instance.deserialize(obj_bytes, ifacebitmaps, metadata, cur_deser_python_objs)

    def deserialize_grpc_message_from_db(self, obj_bytes):
        """
        @postcondition: Deserialize grpc message from DB
        @param obj_bytes: object bytes
        @return grpc msg stored in db
        """
        msg = common_messages.PersistentObjectInDB()
        msg.ParseFromString(obj_bytes)
        return msg

    def deserialize_object_from_db(self, object_to_fill, object_bytes, runtime):
        """
        @postcondition: Deserialize object from bytes
        @param object_to_fill: object to fill
        @param object_bytes: Object bytes
        @param runtime: runtime
        """
        msg = self.deserialize_grpc_message_from_db(object_bytes)
        metadata = get_metadata(msg.metadata)
        self.deserialize_object_from_db_bytes_aux(object_to_fill, metadata, msg.data, runtime)

    def deserialize_object_from_db_bytes_aux(self, object_to_fill, metadata, data, runtime):
        """
        @postcondition: Deserialize object from bytes into instance provided
        @param metadata: object metadata
        @param data: Object data
        @param runtime: runtime
        """
        cur_deser_python_objs = dict()
        obj_bytes = BytesIO(data)
        object_to_fill.set_loaded(True)
        object_to_fill.set_persistent(True)
        self._create_buffer_and_deserialize(obj_bytes, object_to_fill, None, metadata, cur_deser_python_objs)
        runtime.add_to_heap(object_to_fill)

    def deserialize_objbytes_from_db_into_obj_data(self, object_id, obj_bytes_from_db, runtime):
        """
        @postcondition: Deserialize object from bytes into ObjectData and return it.
        @param object_id: ID of object
        @param obj_bytes_from_db: Object bytes
        @param runtime: Runtime to use
        @return object data (to send) of this object
        """
        logger.debug('OBJECT_ID %s, OBJ_BYTES %s', object_id, obj_bytes_from_db)
        msg = self.deserialize_grpc_message_from_db(obj_bytes_from_db)
        metadata = get_metadata(msg.metadata)
        obj_bytes = BytesIO(msg.data)
        logger.debug('METADATA %s and METADATA CLASS_ID %s', metadata, metadata[1][0])
        return (
         object_id, metadata[1][0], metadata, obj_bytes)

    def deserialize_metadata_from_db(self, obj_bytes_from_db):
        """
        @postcondition: deserialize metadata from db (just metadata)
        @param obj_bytes_from_db: object bytes from db
        @return metadata of the object
        """
        msg = common_messages.PersistentObjectInDB()
        msg.ParseFromString(obj_bytes_from_db)
        metadata = get_metadata(msg.metadata)
        return metadata

    def deserialize_object_with_data_in_client(self, param_or_ret, instance, ifacebitmpas, runtime, owner_session_id):
        """
        @postcondition: Deserialize object into a memory instance. ALSO called from executeImplementation in case of 'executions during
        deserialization'. THIS FUNCTION SHOULD NEVER BE CALLED FROM CLIENT SIDE.
        @param param_or_ret: Param/return bytes and metadata
        @param instance: Object in which to deserialize data
        @param ifacebitmaps: Interface bitmaps
        @param runtime: the runtime
        @param owner_session_id: Can be None. ID of owner session of the object. Used for volatiles pending to register.
        """
        runtime.lock(instance.get_object_id())
        try:
            metadata = param_or_ret[2]
            obj_bytes = BytesIO(param_or_ret[3])
            cur_deser_python_objs = dict()
            self._create_buffer_and_deserialize(obj_bytes, instance, None, metadata, cur_deser_python_objs)
            instance.set_persistent(False)
            instance.set_hint(None)
        finally:
            runtime.unlock(instance.get_object_id())

    def deserialize_object_with_data(self, param_or_ret, instance, ifacebitmpas, runtime, owner_session_id, force_deserialization):
        """
        @postcondition: Deserialize object into a memory instance. ALSO called from executeImplementation in case of 'executions during
        deserialization'. THIS FUNCTION SHOULD NEVER BE CALLED FROM CLIENT SIDE.
        @param param_or_ret: Param/return bytes and metadata
        @param instance: Object in which to deserialize data
        @param ifacebitmaps: Interface bitmaps
        @param runtime: the runtime
        @param owner_session_id: Can be None. ID of owner session of the object. Used for volatiles pending to register.
        @param force_deserialization: Check if the object is loaded or not. If FALSE and loaded, then no deserialization is happening. If TRUE, then
        deserialization is forced.
        """
        runtime.lock(instance.get_object_id())
        try:
            if not (force_deserialization or instance.is_loaded()):
                metadata = param_or_ret[2]
                obj_bytes = BytesIO(param_or_ret[3])
                cur_deser_python_objs = dict()
                self._create_buffer_and_deserialize(obj_bytes, instance, None, metadata, cur_deser_python_objs)
                instance.set_loaded(True)
                instance.set_persistent(True)
                if owner_session_id is not None:
                    instance.set_owner_session_id(owner_session_id)
        finally:
            runtime.unlock(instance.get_object_id())

    def deserialize_return(self, serialized_params_or_return, iface_bitmaps, return_type, runtime):
        if serialized_params_or_return[0] == 0:
            logger.verbose('No return to deserialize: returning None')
            return
        return self.deserialize_params_or_return(serialized_params_or_return, iface_bitmaps, {'0': return_type}, [
         '0'], runtime)[0]

    def deserialize_params_or_return(self, serialized_params_or_return, iface_bitmaps, param_specs, params_order, runtime):
        """
        Deserialize parameters or return of an execution
        :param serialized_params_or_return: serialized parameters or return
        :param iface_bitmaps: interface bitmaps
        :param param_specs: specifications of parameters
        :param params_order: order of parameters
        :param runtime: runtime being used
        """
        num_params = serialized_params_or_return[0]
        params = [None] * num_params
        first_volatile = True
        for i, serialized_param in serialized_params_or_return[3].items():
            object_id = serialized_param[0]
            class_id = serialized_param[1]
            logger.verbose('Deserializing volatile with object ID %s' % str(object_id))
            if first_volatile:
                runtime.add_volatiles_under_deserialization(serialized_params_or_return[3])
                first_volatile = False
            deserialized_param = runtime.get_or_new_volatile_instance_and_load(object_id, class_id, runtime.get_hint(), serialized_param, iface_bitmaps)
            runtime.add_session_reference(deserialized_param.get_object_id())
            if i < num_params:
                params[i] = deserialized_param

        for i, serialized_param in serialized_params_or_return[2].items():
            logger.verbose('Deserializing language type at index %s' % str(i))
            obj_bytes = BytesIO(serialized_param[1])
            params[i] = self.deserialize_language(obj_bytes, param_specs[params_order[i]])

        for i, serialized_param in serialized_params_or_return[1].items():
            logger.verbose('Deserializing immutable type at index %s' % str(i))
            obj_bytes = BytesIO(serialized_param)
            params[i] = self.deserialize_immutable(obj_bytes, param_specs[params_order[i]])

        for i, serialized_param in serialized_params_or_return[4].items():
            object_id = serialized_param[0]
            hint = serialized_param[1]
            class_id = serialized_param[2]
            logger.verbose('Deserializing persistent object with object ID %s' % str(object_id))
            deserialized_param = runtime.get_or_new_persistent_instance(object_id, class_id, hint)
            deserialized_param.set_persistent(True)
            if i < num_params:
                params[i] = deserialized_param

        if not first_volatile:
            runtime.remove_volatiles_under_deserialization()
        return params

    def deserialize_association(self, io_file, iface_bitmaps, metadata, cur_deserialized_objs, runtime):
        """
        @postcondition: deserialize association
        @param io_file: bytes of the object containing the association
        @param iface_bitmaps: interface bitmaps
        @param metadata: metadata of the object
        @param cur_deserialized_objs: current deserialized objects
        @param runtime: the runtime
        """
        tag = VLQIntegerWrapper().read(io_file)
        logger.debug('Deserializing association for tag: %d', tag)
        logger.debug('Metadata OIDs: %s', metadata[0])
        object_id = metadata[0][tag]
        logger.debug('Metadata ClassIDs: %s', metadata[1])
        metaclass_id = metadata[1][tag]
        hint = None
        try:
            logger.info('Metadata Hints: %s', metadata[2])
            hint = metadata[2][tag]
        except KeyError:
            pass

        logger.debug('Deserializing association to object: %s', str(object_id))
        obj = runtime.get_or_new_persistent_instance(object_id, metaclass_id, hint)
        cur_deserialized_objs[tag] = obj
        return obj

    def deserialize_immutable(self, io_file, type_):
        try:
            ptw = PyTypeWildcardWrapper(type_.signature)
        except InvalidPythonSignature:
            raise NotImplementedError('Only Java primitive types are understood in Python.')

        return ptw.read(io_file)

    def deserialize_language(self, io_file, type_):
        try:
            ptw = PyTypeWildcardWrapper(type_.signature)
        except InvalidPythonSignature:
            raise NotImplementedError('In fact, InvalidPythonSignature was not even implemented, seems somebody is raising it without implementing logic.')

        return ptw.read(io_file)

    def extract_reference_counting(self, io_file):
        io_file.seek(0)
        ref_counting_pos = IntegerWrapper().read(io_file)
        io_file.seek(ref_counting_pos)
        return io_file.read()


DeserializationLibUtilsSingleton = DeserializationLibUtils()

class PersistentLoadPicklerHelper(object):
    __doc__ = 'Helper to solve deserialization of associations inside Pickled structures.\n\n    See https://docs.python.org/2.7/library/pickle.html#pickling-and-unpickling-external-objects\n    for more information of what this is doing.\n\n    The `__call__` method is being called by Pickle for persistent ids, i.e.,\n    objects that have been serialized by PersistentIdPicklerHelper and thus\n    are associations (DataClayObjects).\n\n    The code is very close to the deserialize association.\n    '

    def __init__(self, metadata, cur_deserialized_objs, runtime):
        self._metadata = metadata
        self._runtime = runtime
        self._cur_deserialized_objs = cur_deserialized_objs

    def __call__(self, str_tag):
        tag = int(str_tag)
        logger.verbose('Deserializing association for tag: %d', tag)
        logger.debug('Metadata OIDs: %s', self._metadata[0])
        object_id = self._metadata[0][tag]
        logger.debug('Metadata ClassIDs: %s', self._metadata[1])
        metaclass_id = self._metadata[1][tag]
        hint = None
        try:
            logger.debug('Metadata Hints: %s', self._metadata[2])
            hint = self._metadata[2][tag]
        except KeyError:
            logger.debug('No Metadata Hints')

        logger.debug('Deserializing association to object: %s', str(object_id))
        obj = self._runtime.get_or_new_persistent_instance(object_id, metaclass_id, hint)
        self._cur_deserialized_objs[tag] = obj
        return obj