# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataclay/heap/ExecutionEnvironmentHeapManager.py
# Compiled at: 2019-10-28 11:50:26
# Size of source mod 2**32: 21443 bytes
""" Class description goes here. """
import sys
from weakref import WeakValueDictionary
import logging, time, gc, traceback
try:
    import tracemalloc
except ImportError:
    tracemalloc = None

import psutil
import dataclay.heap.HeapManager as HeapManager
from dataclay.serialization.lib.SerializationLibUtils import SerializationLibUtilsSingleton
from dataclay.serialization.lib.DeserializationLibUtils import DeserializationLibUtilsSingleton
from dataclay.DataClayObjProperties import DCLAY_PROPERTY_PREFIX
from dataclay.util import Configuration

class ExecutionEnvironmentHeapManager(HeapManager):
    __doc__ = "\n    @summary: This class is intended to manage all dataClay objects in EE runtime's memory.\n    "

    def __init__(self, theruntime):
        """
        @postcondition: Constructor of the object 
        @param theruntime: Runtime being managed 
        """
        HeapManager.__init__(self, theruntime)
        self.TIME_WAIT_FOR_GC_TO_FINISH = 1
        self.exec_env = None
        self.retained_objects = list()
        self.retained_objects_id = set()
        self.is_flushing_all = False
        self.is_processing_gc = False
        self.exec_env = theruntime.get_execution_environment()
        self.logger.debug('EE HEAP MANAGER created for EE %s', self.exec_env.ee_name)

    def get_object_ids_retained(self):
        """
        @postcondition: get ids of objects retained in memory
        @return ids of objects retained in memory 
        """
        return self.inmemory_objects.keys()

    def add_to_heap(self, dc_object):
        """
        @postcondition: the object is added to dataClay's heap
        @param dc_object: object to add to the heap 
        """
        self._add_to_inmemory_map(dc_object)
        self.retain_in_heap(dc_object)

    def retain_in_heap(self, dc_object):
        """
        @postcondition: Add a new Hard reference to the object provided. All code in stubs/exec classes using objects in dataClayheap are
        using weak references. In order to avoid objects to be GC without a flush in DB, HeapManager has hard-references to
        them and is the only one able to release them. This function creates the hard-reference.
        @param dc_object: Object to retain. 
        """
        if dc_object.get_object_id() not in self.retained_objects_id:
            self.retained_objects_id.add(dc_object.get_object_id())
            self.retained_objects.append(dc_object)

    def release_from_heap(self, dc_obj):
        """ 
        @postcondition: Release hard reference to object provided. Without hard reference, the object can be Garbage collected
        @param dc_obj: object to release
        """
        self.logger.debug('[==GC==] Releasing object with id %s from retained map. ', dc_obj.get_object_id())
        try:
            self.retained_objects_id.remove(dc_obj.get_object_id())
            self.retained_objects.remove(dc_obj)
        except Exception as e:
            try:
                self.logger.debug('[==GC==] ERROR Releasing object with id %s ', dc_obj.get_object_id())
            finally:
                e = None
                del e

    def __check_memory_pressure(self):
        """
        @postcondition: Check if memory is under pressure 
        @return TRUE if memory is under pressure. FALSE otherwise. 
        """
        virtual_mem = psutil.virtual_memory()
        self.logger.trace('[==GC==] Memory: %s', virtual_mem)
        return float(virtual_mem.percent) > Configuration.MEMMGMT_PRESSURE_FRACTION * 100

    def __check_memory_ease(self):
        """
        @postcondition: Check if memory is at ease
        @return TRUE if memory is at ease. FALSE otherwise.
        """
        virtual_mem = psutil.virtual_memory()
        self.logger.trace('[==GC==] Memory: %s', virtual_mem)
        return float(virtual_mem.percent) < Configuration.MEMMGMT_EASE_FRACTION * 100

    def __nullify_object(self, dc_object):
        """
        @postcondition: Set all fields to none to allow GC action 
        """
        metaclass = dc_object.get_class_extradata()
        self.logger.debug('[==GC==] Going to clean object %r', dc_object)
        if self.logger.isEnabledFor(logging.DEBUG):
            held_objects = WeakValueDictionary()
            o = None
            prop_name_list = metaclass.properties.keys()
            self.logger.debug('The following attributes will be nullified from object %r: %s', dc_object, ', '.join(prop_name_list))
            for prop_name in prop_name_list:
                real_prop_name = '%s%s' % (DCLAY_PROPERTY_PREFIX, prop_name)
                try:
                    o = object.__getattribute__(dc_object, real_prop_name)
                    held_objects[prop_name] = o
                except TypeError:
                    self.logger.trace('Ignoring attribute %s of type %s', prop_name, type(o))

            del o
        else:
            for prop_name in metaclass.properties.keys():
                real_prop_name = '%s%s' % (DCLAY_PROPERTY_PREFIX, prop_name)
                object.__setattr__(dc_object, real_prop_name, None)

            if self.logger.isEnabledFor(logging.DEBUG):
                held_attr_names = held_objects.keys()
                if held_attr_names:
                    self.logger.debug('The following attributes of object %r still have a backref active: %s', dc_object, ', '.join(held_attr_names))
                else:
                    self.logger.debug('The garbage collector seems to have cleaned all the nullified attributes on %r', dc_object)

    def __clean_object(self, dc_object):
        """
        @postcondition: Clean object (except if not loaded or being used). Cleaning means set all fields to None to allow
        GC to work.
        @param dc_object: Object to clean.
        """
        object_id = dc_object.get_object_id()
        self.runtime.lock(object_id)
        try:
            is_loaded = dc_object.is_loaded()
            if not is_loaded:
                self.logger.trace('[==GC==] Not collecting since not loaded.')
                return
            self.logger.debug('[==GC==] Setting loaded to false from gc %s' % str(object_id))
            dc_object.set_loaded(False)
            if dc_object.is_dirty() or dc_object.is_pending_to_register():
                self.logger.debug('[==GC==] Updating object %s ', dc_object.get_object_id())
                self.gc_collect_internal(dc_object)
            self.logger.debug('[==GC==] Cleaning object %s', dc_object.get_object_id())
            self._ExecutionEnvironmentHeapManager__nullify_object(dc_object)
            dc_object.set_dirty(False)
            self.release_from_heap(dc_object)
        finally:
            self.runtime.unlock(object_id)

    def gc_collect_internal(self, object_to_update):
        """
        @postcondition: Update object in db or store it if volatile (and register in LM)
        @param object_to_update: object to update
        """
        try:
            self.logger.debug('[==GCUpdate==] Updating object %s', object_to_update.get_object_id())
            if object_to_update.is_pending_to_register():
                obj_bytes = SerializationLibUtilsSingleton.serialize_for_db_gc(object_to_update, False, None)
                self.logger.debug('[==GCUpdate==] Pending to register in LM ')
                self.exec_env.register_and_store_pending(object_to_update, obj_bytes, True)
            else:
                if object_to_update.is_dirty():
                    obj_bytes = SerializationLibUtilsSingleton.serialize_for_db_gc(object_to_update, False, None)
                    self.logger.debug('[==GCUpdate==] Updated dirty object %s ', object_to_update.get_object_id())
                    self.runtime.update_to_sl(object_to_update.get_object_id(), obj_bytes, True)
                else:
                    obj_bytes = SerializationLibUtilsSingleton.serialize_for_db_gc_not_dirty(object_to_update, False, None)
                    if obj_bytes is not None:
                        ref_counting_bytes = DeserializationLibUtilsSingleton.extract_reference_counting(obj_bytes)
                        self.runtime.update_to_sl(object_to_update.get_object_id(), ref_counting_bytes, False)
        except:
            traceback.print_exc()

    def run_task(self):
        """
        @postcondition: Check Python VM's memory pressure and clean if necessary. Cleaning means flushing objects, setting 
        all fields to none (to allow GC to work better) and remove from retained references. If volatile or pending to register,
        we remove it once registered.
        """
        if not self.is_flushing_all:
            if self.is_processing_gc:
                self.logger.debug('[==GC==] Not running since is being processed or flush all is being done')
                return
            self.is_processing_gc = True
            self.logger.trace('[==GC==] Running GC')
            self.exec_env.prepareThread()
            is_pressure = self._ExecutionEnvironmentHeapManager__check_memory_pressure()
            if is_pressure:
                self.logger.verbose('System memory is under pressure, proceeding to clean up objects')
                if self.logger.isEnabledFor(logging.DEBUG):
                    if tracemalloc is not None:
                        if tracemalloc.is_tracing():
                            self.logger.debug('Doing a snapshot...')
                            snapshot = tracemalloc.take_snapshot()
                            top_stats = snapshot.statistics('lineno')
                            print('[ Top 10 ]')
                            for stat in top_stats[:10]:
                                print(stat)

                retained_objects_copy = self.retained_objects[:]
                self.logger.debug('Starting iteration with #%d retained objects', len(self.retained_objects))
                while 1:
                    if retained_objects_copy:
                        dc_obj = retained_objects_copy.pop()
                        if dc_obj.get_memory_pinned():
                            self.logger.trace('Object %r is memory pinned, ignoring it', dc_obj)
                            continue
                        self._ExecutionEnvironmentHeapManager__clean_object(dc_obj)
                        del dc_obj
                        n = gc.collect()
                        if self.logger.isEnabledFor(logging.DEBUG):
                            if n > 0:
                                self.logger.debug('[==GC==] Collected %d', n)
                            else:
                                self.logger.trace('[==GC==] No objects collected')
                            if gc.garbage:
                                self.logger.debug('[==GC==] Uncollectable: %s', gc.garbage)
                            else:
                                self.logger.trace('[==GC==] No uncollectable objects')
                        at_ease = self._ExecutionEnvironmentHeapManager__check_memory_ease()
                        if at_ease:
                            self.logger.trace("[==GC==] Not collecting since memory is 'at ease' now")
                            break
                        if self.is_flushing_all:
                            self.logger.debug('[==GC==] Interrupted due to flush all.')
                            break
                else:
                    self.logger.warning('I did my best and ended up cleaning all retained_objects. This typically means that there is a huge global memory pressure. Problematic.')

                self.logger.debug('Finishing iteration with #%d retained objects', len(self.retained_objects))
                self.cleanReferencesAndLockers()
                n = gc.collect()
                if self.logger.isEnabledFor(logging.DEBUG):
                    if retained_objects_copy:
                        self.logger.debug('There are #%d remaining objects after Garbage Collection', len(retained_objects_copy))
                    elif n > 0:
                        self.logger.debug('[==GC==] Finally Collected %d', n)
                    else:
                        self.logger.trace('[==GC==] No objects collected')
                    if gc.garbage:
                        self.logger.debug('[==GC==] Uncollectable: %s', gc.garbage)
        else:
            self.logger.trace('[==GC==] No uncollectable objects')
        del retained_objects_copy
        if self.logger.isEnabledFor(logging.DEBUG):
            if tracemalloc is not None:
                if tracemalloc.is_tracing():
                    self.logger.debug('Doing a snapshot...')
                    snapshot2 = tracemalloc.take_snapshot()
                    top_stats = snapshot2.compare_to(snapshot, 'lineno')
                    print('[ Top 10 differences ]')
                    for stat in top_stats[:10]:
                        print(stat)

        self.is_processing_gc = False

    def flush_all(self):
        """
        @postcondition: Stores all objects in memory into disk. This function is usually called at shutdown of the 
        execution environment. 
        """
        if self.is_flushing_all:
            return
        self.is_flushing_all = True
        while self.is_processing_gc:
            time.sleep(self.TIME_WAIT_FOR_GC_TO_FINISH)

        self.logger.debug('[==FlushAll==] Number of objects in Heap: %s', self.heap_size())
        for object_to_update in self.retained_objects:
            self.gc_collect_internal(object_to_update)