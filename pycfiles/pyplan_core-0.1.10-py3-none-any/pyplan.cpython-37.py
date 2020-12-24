# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/pyplan.py
# Compiled at: 2020-05-04 09:09:15
# Size of source mod 2**32: 3380 bytes
import pyplan_core.classes.Model as Model
import pandas as pd
from multiprocessing import Lock
import os
os.environ['ENGINE_MODE'] = 'local'

class Pyplan(object):
    __doc__ = 'Main class to interact with the pyplan model'

    @property
    def sample_models(self):
        return PyplanSampleModels

    def __init__(self):
        self.model = Model()
        self.lastUpdated = -1
        self.currentFilename = ''
        self.lock = Lock()

    def openModel(self, filename):
        """Open Pyplan model"""
        try:
            self._lock_acquire()
            self.currentFilename = filename
            self.lastUpdated = os.path.getmtime(filename)
            self.model.openModel(filename)
        finally:
            self._lock_release()

    def closeModel(self):
        """Close current model"""
        try:
            self._lock_acquire()
            self.model.closeModel()
        finally:
            self._lock_release()

    def getResult(self, node_id):
        """Return result of the node"""
        try:
            self._lock_acquire()
            if self.model.existNode(node_id):
                return self.model.getNode(node_id).result
            raise ValueError(f"The node '{node_id}' was not found in the model")
        finally:
            self._lock_release()

    def setSelectorValue(self, node_id, value):
        """Set value of a selector node"""
        try:
            self._lock_acquire()
            if self.model.existNode(node_id):
                self.model.setSelectorValue(node_id, value)
            else:
                raise ValueError(f"The node '{node_id}' was not found in the model")
        finally:
            self._lock_release()

    def checkForReloadModel(self):
        """Check and reolad model if the last update time has changed"""
        if os.path.getmtime(self.currentFilename) != self.lastUpdated:
            self.openModel(self.currentFilename)

    def getNodeList(self, module_id=None):
        """Return dataframe with the nodes in Pyplan model"""
        arr = []
        if not module_id:
            module_id = self.model.modelNode.identifier
        for node in self.model.findNodes('moduleId', module_id):
            if node.nodeClass not in ('text', 'alias', 'inputnode') and node.identifier not in ('pyplan_library', ):
                arr.append([node.identifier, node.title, node.nodeClass, node.moduleId])

        df = pd.DataFrame(arr, columns=['node_id', 'title', 'class', 'module_id'])
        return df

    def getNode(self, node_id):
        """Return Node from Pyplan model"""
        try:
            self._lock_acquire()
            if self.model.existNode(node_id):
                return self.model.getNode(node_id)
            raise ValueError(f"The node '{node_id}' was not found in the model")
        finally:
            self._lock_release()

    def _lock_acquire(self):
        if self.lock is not None:
            return self.lock.acquire()
        return False

    def _lock_release(self):
        if self.lock is not None:
            try:
                self.lock.release()
            except:
                pass


class PyplanSampleModels(object):
    __doc__ = 'Class for read internal sample models'

    @staticmethod
    def use_of_pyplan_core():
        return os.path.dirname(os.path.abspath(__file__)) + '/sample_models/Sample for Pyplan Core.ppl'