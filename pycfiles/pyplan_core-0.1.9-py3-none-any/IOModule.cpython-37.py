# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/IOModule.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 4940 bytes
import jsonpickle

class IOModule(object):

    def __init__(self, model):
        self.model = model

    def exportModule(self, moduleId, filename):
        res = False
        if self.model.existNode(moduleId):
            toSave = {'modelProp':self.model.modelProp,  'nodeList':[]}
            mainModule = self.model.getNode(moduleId).toObj()
            toSave['nodeList'].append(mainModule)
            mainModel = self.model.getNode(mainModule['moduleId'])
            modelObj = mainModel.toObj()
            modelObj['nodeClass'] = 'model'
            modelObj['moduleId'] = '_model_'
            toSave['nodeList'].append(modelObj)

            def iterateNodes(subModuleId, toSave):
                for node in self.model.findNodes('moduleId', subModuleId):
                    node.system or toSave['nodeList'].append(node.toObj())
                    if node.nodeClass == 'module':
                        iterateNodes(node.identifier, toSave)

            iterateNodes(moduleId, toSave)
            with open(filename, 'w') as (f):
                f.write(jsonpickle.encode(toSave))
                f.close()
            toSave = None
            res = True
        return res

    def importModule(self, moduleId, filename, importType):
        if importType == '0':
            return self.mergeModule(moduleId, filename)
        if importType == '2':
            return self.switchModule(moduleId, filename)
        return False

    def mergeModule(self, moduleId, filename):
        res = False
        if self.model.existNode(moduleId):
            opened = {}
            with open(filename, 'r') as (f):
                opened = jsonpickle.decode(f.read())
                f.close()
            self.model._isLoadingModel = True
            try:
                for nn, obj in enumerate(opened['nodeList']):
                    if obj['nodeClass'] != 'model':
                        if self.model.existNode(obj['identifier']):
                            node = self.model.getNode(obj['identifier'])
                            node.definition = obj['definition']
                            node.title = obj['title']
                            node.description = obj['description']
                            node.units = obj['units']
                            node.color = obj['color']
                            node.x = obj['x']
                            node.y = obj['y']
                            node.w = obj['w']
                            node.h = obj['h']
                            node = None
                        else:
                            if nn == 0:
                                obj['moduleId'] = moduleId
                            node = self.model.createNode((obj['identifier']),
                              moduleId=(obj['moduleId']))
                            node.fromObj(obj)
                            node = None

                [self.model.nodeDic[nod].generateIO() for nod in self.model.nodeDic]
            finally:
                self.model._isLoadingModel = False

            res = True
        else:
            raise ValueError('Module base not found')
        return res

    def switchModule(self, moduleId, filename):
        res = False
        if self.model.existNode(moduleId):
            opened = {}
            with open(filename, 'r') as (f):
                opened = jsonpickle.decode(f.read())
                f.close()
            if len(opened['nodeList']) > 0:
                mainModule = opened['nodeList'][0]
                mainId = mainModule['identifier']
                self.model.deleteNodes([mainId], removeAliasIfNotIn=mainId)
            self.model._isLoadingModel = True
            try:
                for nn, obj in enumerate(opened['nodeList']):
                    if nn == 0:
                        obj['moduleId'] = moduleId
                    if obj['nodeClass'] != 'model':
                        if self.model.existNode(obj['identifier']):
                            node = self.model.getNode(obj['identifier'])
                            node.identifier = node.identifier + '_copy'
                        node = self.model.createNode((obj['identifier']),
                          moduleId=(obj['moduleId']))
                        node.fromObj(obj)
                        node = None

                for nodeId in self.model.nodeDic:
                    self.model.nodeDic[nodeId].generateIO()

            finally:
                self.model._isLoadingModel = False

            res = True
        else:
            raise ValueError('Module base not found')
        return res