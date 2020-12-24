# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/Model.py
# Compiled at: 2020-05-05 18:04:47
# Size of source mod 2**32: 73665 bytes
import datetime, importlib, os, re, subprocess, sys, threading, unicodedata
from shlex import split
from site import getsitepackages
from sys import platform
from time import sleep
import jsonpickle, numpy, pandas, xarray as xr
from pyplan_core import cubepy
import pyplan_core.classes.BaseNode as BaseNode
import pyplan_core.classes.Intellisense as Intellisense
import pyplan_core.classes.IOModule as IOModule
from pyplan_core.classes.PyplanFunctions import Selector, PyplanFunctions
import pyplan_core.classes.evaluators.Evaluator as Evaluator
from pyplan_core.classes.wizards import CalculatedField, DataframeGroupby, DataframeIndex, SelectColumns, SelectRows, sourcecsv

class Model(object):
    DEFAULT_IMPORTS = {'np':numpy, 
     'pd':pandas, 
     'cubepy':cubepy, 
     'xr':xr}

    def __init__(self, WSClass=None):
        self._nodeDic = {}
        self._nodeClassDic = dict()
        self._modelProp = {}
        self._modelNode = None
        self._isLoadingModel = False
        self.initialize()
        self.evaluationVersion = 0
        self.inCyclicEvaluate = False
        self._scenarioDic = dict()
        self._wizard = None
        self._currentProcessingNode = ''
        self._currentInstallProgress = []
        self._customImports = None
        self.company_code = None
        self.session_key = None
        self.ws = None
        self.debugMode = None
        self.WS = WSClass

    @property
    def nodeDic(self):
        return self._nodeDic

    @property
    def modelProp(self):
        return self._modelProp

    @property
    def modelNode(self):
        return self._modelNode

    @property
    def isLoadingModel(self):
        return self._isLoadingModel

    def getPID(self):
        return os.getpid()

    def getDefaultNodeFormat(self, nodeClass):
        if nodeClass in self._nodeClassDic:
            return self._nodeClassDic[nodeClass]
        return

    def getTotalMemory(self):
        res = 0
        for node in self.nodeDic:
            res = res + self.nodeDic[node].usedMemory

        return res

    def getCurrentModelPath(self):
        if self.existNode('current_path'):
            return self.getNode('current_path').result
        return ''

    def setCurrentModelPath(self, value):
        if self.existNode('current_path'):
            self.getNode('current_path').definition = 'result="""' + str(value) + '"""'

    def currentProcessingNode(self, nodeId):
        if nodeId not in ('__evalnode__', 'current_path'):
            self._currentProcessingNode = nodeId

    def initialize(self, modelName=None):
        if modelName is None:
            self._modelNode = self.createNode('new_model', 'model', '_model_')
        else:
            newId = modelName.lower()
            newId = re.sub('[^0-9a-z]+', '_', newId)
            self._modelNode = self.createNode(newId, 'model', '_model_')
            self._modelNode.title = modelName
        self._scenarioDic = dict()
        self._nodeClassDic = dict()
        self._wizard = None

    def setNodeClassDic(self, nodeClassDic):
        """Set nodeclass dic used for create new nodes"""
        self._nodeClassDic = nodeClassDic

    def connectToWS(self, company_code, session_key):
        self.company_code = company_code
        self.session_key = session_key
        if self.WS:
            self.ws = self.WS(company_code=company_code, session_key=session_key)

    def createNode(self, identifier=None, nodeClass=None, moduleId=None, x=None, y=None, toObj=False, originalId=None):
        """Create new node"""
        newNode = BaseNode(model=self, identifier=identifier, nodeClass=nodeClass, moduleId=moduleId,
          x=x,
          y=y,
          originalId=originalId)
        id = newNode.identifier
        self.nodeDic[id] = newNode
        newNode = None
        if toObj:
            return self.nodeDic[id].toObj()
        return self.nodeDic[id]

    def deleteNodes(self, nodes, removeAliasIfNotIn=None):
        """Delete nodes by node id"""
        if nodes is not None:
            for nodeId in nodes:
                if self.existNode(nodeId):
                    if nodeId != '_model_':
                        if self.getNode(nodeId).nodeClass == 'module':
                            childs = self.findNodes('moduleId', nodeId)
                            childsIds = [c.identifier for c in childs]
                            self.deleteNodes(childsIds, removeAliasIfNotIn)
                        aliases = []
                        aliases = self.findNodes('originalId', nodeId)
                        if aliases:
                            aliasesId = [a.identifier for a in aliases]
                            if removeAliasIfNotIn:
                                _auxAliases = []
                                for _aliasId in aliasesId:
                                    if self.isIn(_aliasId, removeAliasIfNotIn):
                                        _auxAliases.append(_aliasId)

                                if len(_auxAliases) > 0:
                                    self.deleteNodes(_auxAliases, removeAliasIfNotIn)
                            else:
                                self.deleteNodes(aliasesId, removeAliasIfNotIn)
                    self.nodeDic[nodeId].preDelete()
                    self.nodeDic[nodeId].release()
                    self.nodeDic[nodeId] = None
                    del self.nodeDic[nodeId]

    def existNode(self, nodeId):
        """Return True if node exists in model"""
        nodeId = self.clearId(nodeId)
        if (nodeId is not None) & (nodeId in self.nodeDic):
            return True
        return False

    def getNode(self, nodeId):
        """Renor node from node dictionary"""
        if self.existNode(nodeId):
            return self.nodeDic[nodeId]

    def isChild(self, nodeId, modulesId):
        """Return true if nodeid or one of your parents is in any of modulesId modules"""
        res = False
        if self.existNode(nodeId):
            aux = self.getNode(nodeId).moduleId
            nChance = 20
            while res == False and aux != '_model_' and nChance > 0:
                res = aux in modulesId
                node = self.getNode(aux)
                if node:
                    aux = node.moduleId
                else:
                    nChance = 0
                nChance -= 1

        return res

    def isNodeInScenario(self, nodeId):
        if nodeId in self._scenarioDic:
            return True
        return False

    def evaluateNode(self, nodeId, dims=None, rows=None, columns=None, summaryBy='sum', bottomTotal=False, rightTotal=False, fromRow=0, toRow=0, resultType=''):
        """Evaluate node. Call evaluator class for implement diferent evaluators."""
        if self.existNode(nodeId):
            result = None
            if nodeId in self._scenarioDic:
                result = self._scenarioDic[nodeId]
            else:
                result = self.nodeDic[nodeId].result
            if result is not None:
                self.evaluationVersion += 1
                evaluator = Evaluator.createInstance(result)
                if not evaluator.checkStructure(result, resultType):
                    raise ValueError('bad_node_structure')
                return evaluator.evaluateNode(result, self.nodeDic, nodeId, dims, rows, columns, summaryBy, bottomTotal, rightTotal, fromRow, toRow)
        return ''

    def executeButton(self, nodeId):
        """Execute node of class button"""
        if self.existNode(nodeId):
            self.nodeDic[nodeId].invalidate()
            toReturn = self.nodeDic[nodeId].result
            if toReturn is None:
                toReturn = ''
            return toReturn
        return ''

    def previewNode(self, nodeId, debugMode=''):
        """Perform preview of a node"""
        try:
            result = None
            if self.existNode(nodeId):
                if debugMode:
                    self.debugMode = debugMode
                    if debugMode == 'node':
                        self.nodeDic[nodeId].silentInvalidate()
                    else:
                        if debugMode == 'model':
                            for node_key in self.nodeDic:
                                self.nodeDic[node_key].silentInvalidate()

                else:
                    if self.nodeDic[nodeId].originalId is not None:
                        nodeId = self.nodeDic[nodeId].originalId
                    if self.nodeDic[nodeId].nodeClass in ('button', 'module', 'text'):
                        self.evaluationVersion += 1
                        _dummy = self.nodeDic[nodeId].result
                    else:
                        if self.nodeDic[nodeId].result is not None:
                            self.evaluationVersion += 1
                            evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
                            result = evaluator.previewNode(self.nodeDic, nodeId)
            if result is None:
                evaluator = Evaluator.createInstance(None)
                result = evaluator.generateEmptyPreviewResponse(self.nodeDic, nodeId)
            return result
        finally:
            if self.debugMode:
                if self.ws:
                    self.ws.sendDebugInfo('endPreview', '', 'endPreview')
            self.debugMode = None

    def getCubeValues(self, query):
        """Evaluate node. Used for pivotgrid"""
        nodeId = query['cube']
        if self.existNode(nodeId):
            result = None
            if nodeId in self._scenarioDic:
                result = self._scenarioDic[nodeId]
            else:
                result = self.nodeDic[nodeId].result
            if result is not None:
                evaluator = Evaluator.createInstance(result)
                return evaluator.getCubeValues(result, self.nodeDic, nodeId, query)

    def getCubeDimensionValues(self, query):
        """Return the values of a dimension of node. Used from pivotgrid"""
        nodeId = query['cube']
        if self.existNode(nodeId):
            result = None
            if nodeId in self._scenarioDic:
                result = self._scenarioDic[nodeId]
            else:
                result = self.nodeDic[nodeId].result
            if result is not None:
                evaluator = Evaluator.createInstance(result)
                return evaluator.getCubeDimensionValues(result, self.nodeDic, nodeId, query)

    def getCubeMetadata(self, nodeId, resultType=''):
        """Return metadata of cube. Used from pivotgrid"""
        if self.existNode(nodeId):
            result = None
            if nodeId in self._scenarioDic:
                result = self._scenarioDic[nodeId]
            else:
                result = self.nodeDic[nodeId].result
            if result is not None:
                evaluator = Evaluator.createInstance(result)
                if resultType:
                    if not evaluator.checkStructure(result, resultType):
                        raise ValueError('bad_node_structure')
                return evaluator.getCubeMetadata(result, self.nodeDic, nodeId)

    def setNodeValueChanges(self, changes):
        """Set values for node using filters"""
        nodeId = changes['node']
        if self.existNode(nodeId):
            if self.nodeDic[nodeId].nodeClass == 'formnode':
                nodeId = self.nodeDic[nodeId].originalId
                evaluator = Evaluator.createInstance(None)
                return evaluator.setNodeValueChanges(self.nodeDic, nodeId, changes)
            if self.nodeDic[nodeId].originalId is not None:
                nodeId = self.nodeDic[nodeId].originalId
            if self.nodeDic[nodeId].result is not None:
                evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
                return evaluator.setNodeValueChanges(self.nodeDic, nodeId, changes)

    def getDiagram(self, moduleId=None):
        """Get diagram"""
        if moduleId is None:
            moduleId = self.modelNode.identifier
        moduleId = self.clearId(moduleId)
        res = {'moduleId':moduleId, 
         'arrows':[],  'nodes':[],  'breadcrumb':self.getBreadcrumb(moduleId)}
        nodeList = self.findNodes('moduleId', moduleId)
        nodeList.sort(key=(lambda x: int(x.z)))
        for node in nodeList:
            res['nodes'].append(node.toObj(exceptions=[
             'definition'],
              fillDefaultProperties=True))

        return res

    def getBreadcrumb(self, moduleId=None):
        """Get breadcrumb"""
        if moduleId is None:
            moduleId = self.modelNode.identifier
        moduleId = self.clearId(moduleId)
        res = []
        aux = moduleId
        while aux != self.modelNode.identifier and self.existNode(aux):
            res.append({'identifier':aux, 
             'title':self.getNode(aux).title or aux})
            aux = self.getNode(aux).moduleId

        res.append({'identifier':self.modelNode.identifier,  'title':self.modelNode.title or 'Main'})
        return res

    def isIn(self, nodeId, moduleId):
        """ Return true if nodeId is in moduleId. Search for parents"""
        res = False
        aux = nodeId
        _secure = 1
        while aux != self.modelNode.identifier and self.existNode(aux) and _secure < 100:
            if aux == moduleId:
                res = True
                break
            aux = self.getNode(aux).moduleId
            _secure += 1

        return res

    def isSelector(self, nodeId):
        """Return True if nodeId is of type Selector"""
        if self.existNode(nodeId):
            return isinstance(self.getNode(nodeId).result, Selector)
        return False

    def getSelector(self, nodeId):
        """Return selector data if node is of type selector"""
        if self.isSelector(nodeId):
            return self.getNode(nodeId).result.toObj()

    def setSelectorValue(self, nodeId, value):
        """Set selector value if node is of type selector"""
        if self.isSelector(nodeId):
            node = self.getNode(nodeId)
            selector = node.result
            if not selector.isSameValue(value):
                definition = node.definition
                new_definition = selector.generateDefinition(definition, value)
                if new_definition:
                    node.definition = new_definition

    def release(self):
        """Release model. Free all resources """
        if self._modelNode is not None:
            self._modelNode.release()
        (xx.release() for xx in self.nodeDic)
        keys = [x for x in self.nodeDic]
        for key in keys:
            del self.nodeDic[key]

        self._nodeDic = {}
        self._modelProp = {}
        self._modelNode = None
        self._scenarioDic = dict()
        self._nodeClassDic = dict()
        self._wizard = None
        self._customImports = None

    def getNextIdentifier(self, prefix):
        """Get next free identifier of node"""
        reg = '(\\d+$)'
        matches = re.findall(reg, prefix)
        start_at = 1
        if len(matches) > 0:
            num = matches[0]
            start_at = int(num) + 1
            if start_at > 100000000:
                prefix += '_'
                start_at = 1
            else:
                prefix = prefix[:-len(num)]
        for num in range(start_at, 100000000):
            key = prefix + str(num)
            if key not in self.nodeDic:
                return key

    def clearId(self, nodeId):
        """DEPRECATED"""
        return nodeId

    def updateNodeIdInDic(self, oldNodeId, newNodeId):
        """Update node identifier on all dictionary."""
        if self.existNode(oldNodeId):
            newNodeId = self.clearId(newNodeId)
            self.nodeDic[newNodeId] = self.nodeDic[oldNodeId]
            for node in self.findNodes('moduleId', oldNodeId):
                node.moduleId = newNodeId

            for node in self.findNodes('originalId', oldNodeId):
                node.originalId = newNodeId
                node._definition = 'result = ' + str(newNodeId)

            del self.nodeDic[oldNodeId]
            return True
        return False

    def setNodeProperties(self, nodeId, properties):
        """Update properties of a node"""
        nodeId = self.clearId(nodeId)
        if self.existNode(nodeId):
            _node = self.getNode(nodeId)
            for prop in properties:
                if '.' in prop['name']:
                    nodeProp, objProp = prop['name'].split('.')
                    setattr(getattr(_node, nodeProp), objProp, prop['value'])
                else:
                    setattr(_node, prop['name'], prop['value'])

    def getNodeProperties(self, nodeProperties):
        """Get properties of a node"""
        if nodeProperties is not None:
            if nodeProperties['node'] != '':
                nodeId = self.clearId(nodeProperties['node'])
                if self.existNode(nodeId):
                    _node = self.getNode(nodeId)
                    for prop in nodeProperties['properties']:
                        if hasattr(_node, prop['name']):
                            prop['value'] = getattr(_node, prop['name'])

                    return nodeProperties

    def setModelProperties(self, properties):
        """Update properties of model"""
        for key in properties:
            if key == 'modelId':
                continue
            elif key in ('identifier', 'title'):
                setattr(self.modelNode, key, properties[key])
            else:
                self.modelProp[key] = properties[key]

    def getModelProperties(self):
        """Get model propierties"""
        res = dict()
        res['identifier'] = self.modelNode.identifier
        res['title'] = self.modelNode.title
        for key in self.modelProp:
            res[key] = self.modelProp[key]

        return res

    def getIndexes(self, nodeId):
        """Return indexes of a node"""
        if self.existNode(nodeId):
            if nodeId in self._scenarioDic:
                evaluator = Evaluator.createInstance(self._scenarioDic[nodeId])
                return evaluator.getIndexes(self.nodeDic[nodeId], self._scenarioDic[nodeId])
            _node = self.getNode(nodeId)
            return _node.indexes

    def getIndexValues(self, data):
        """Return values of a index node."""
        tmpNodeId = data.index_id if (data.node_id is None or data.node_id == '') else (data.node_id)
        if self.existNode(tmpNodeId):
            result = self.nodeDic[tmpNodeId].result
            if data.node_id in self._scenarioDic:
                result = self._scenarioDic[data.node_id]
            evaluator = Evaluator.createInstance(result)
            return evaluator.getIndexValues(self.nodeDic, data, result)

    def getIndexType(self, nodeId, indexId):
        """Return index type"""
        tmpNodeId = indexId if (nodeId is None or nodeId == '') else nodeId
        if self.existNode(tmpNodeId):
            evaluator = Evaluator.createInstance(self.nodeDic[tmpNodeId].result)
            return evaluator.getIndexType(self.nodeDic, nodeId, indexId)

    def getIndexesWithLevels(self, nodeId):
        """Return indexes of a node"""
        if self.existNode(nodeId):
            if nodeId in self._scenarioDic:
                evaluator = Evaluator.createInstance(self._scenarioDic[nodeId])
                return evaluator.getIndexesWithLevels(self.nodeDic[nodeId], self._scenarioDic[nodeId])
            evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
            return evaluator.getIndexesWithLevels(self.nodeDic[nodeId])

    def isTable(self, nodeId):
        """return true if node is a table"""
        res = '0'
        if self.existNode(nodeId):
            evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
            res = evaluator.isTable(self.getNode(nodeId))
        return res

    def getArrows(self, moduleId):
        """Return all arrows of moduleId"""
        res = []
        modulesInLevel = []
        inputsInOtherLevel = []
        outputsInOtherLevel = []
        thisLevel = self.findNodes('moduleId', moduleId)
        thisIds = [node.identifier for node in thisLevel]
        for node in thisLevel:
            if node.nodeClass == 'module':
                modulesInLevel.append(node.identifier)

        for node in thisLevel:
            if node.nodeClass not in ('module', 'text'):
                for outputNodeId in node.outputs:
                    fullOutputs = []
                    fullOutputs = self.findNodes('originalId', outputNodeId)
                    fullOutputs.append(self.getNode(outputNodeId))
                    for o in fullOutputs:
                        if o is not None:
                            element = {'from':node.identifier, 
                             'to':o.identifier}
                            if o.identifier in thisIds:
                                if node.nodeInfo.showOutputs:
                                    if o.nodeInfo.showInputs:
                                        if self.existArrow(element['from'], element['to'], res) == False:
                                            res.append(element)
                            elif o.identifier not in thisIds and self.existArrow(element['from'], element['to'], outputsInOtherLevel) == False:
                                len(self.getAliasInLevel(o.identifier, moduleId)) > 0 or outputsInOtherLevel.append(element)

                for inputNodeId in node.inputs:
                    fullInputs = []
                    fullInputs = self.findNodes('originalId', inputNodeId)
                    fullInputs.append(self.getNode(inputNodeId))
                    for i in fullInputs:
                        if i is not None:
                            element = {'from':i.identifier, 
                             'to':node.identifier}
                            if i.identifier in thisIds:
                                if i.nodeInfo.showOutputs and node.nodeInfo.showInputs and self.existArrow(element['from'], element['to'], res) == False:
                                    res.append(element)
                            elif i.identifier not in thisIds:
                                if self.existArrow(element['from'], element['to'], inputsInOtherLevel) == False:
                                    len(self.getAliasInLevel(i.identifier, moduleId)) > 0 or inputsInOtherLevel.append(element)

        if outputsInOtherLevel:
            for d in outputsInOtherLevel:
                newTo = []
                nodeFrom = d['from']
                nodeTo = d['to']
                if self.getNode(nodeTo).isin in self.nodeDic:
                    newTo = self.getParentModule(nodeTo, modulesInLevel)
                if newTo:
                    element = {'from':nodeFrom, 
                     'to':newTo}
                    if self.getNode(nodeFrom).nodeInfo.showOutputs and self.getNode(newTo).nodeInfo.showInputs and self.existArrow(element['from'], element['to'], res) == False:
                        res.append(element)

        if inputsInOtherLevel:
            for d in inputsInOtherLevel:
                newFrom = []
                nodeFrom = d['from']
                nodeTo = d['to']
                if self.getNode(nodeFrom).isin in self.nodeDic:
                    newFrom = self.getParentModule(nodeFrom, modulesInLevel)
                if newFrom:
                    element = {'from':newFrom, 
                     'to':nodeTo}
                    if self.getNode(newFrom).nodeInfo.showOutputs and self.getNode(nodeTo).nodeInfo.showInputs and self.existArrow(element['from'], element['to'], res) == False:
                        res.append(element)

        modulesComplete = []
        for mod in modulesInLevel:
            modulesComplete.append({'module':mod, 
             'nodes':self.getNodesInModule(mod, [])})

        for mod in modulesComplete:
            for node in mod['nodes']:
                if self.getNode(mod['module']).nodeInfo.showOutputs:
                    tempOutputs = node.outputs
                    if tempOutputs:
                        for output in tempOutputs:
                            for auxModule in modulesComplete:
                                if mod['module'] != auxModule['module'] and self.getNode(auxModule['module']).nodeInfo.showInputs and self.getNode(output) in auxModule['nodes']:
                                    element = {'from':mod['module'],  'to':auxModule['module']}
                                    if self.existArrow(element['from'], element['to'], res) == False:
                                        res.append(element)

        return res

    def existArrow(self, aFrom, aTo, arrowsList):
        """Return true if exists de arrow from-to"""
        if arrowsList:
            for arrow in arrowsList:
                if arrow['from'] == aFrom and arrow['to'] == aTo:
                    return True

        return False

    def getAliasInLevel(self, nodeIdentifier, levelId):
        """Returns the aliases in the level"""
        res = []
        aliasNodes = self.findNodes('originalId', nodeIdentifier)
        if aliasNodes is not None:
            for alias in aliasNodes:
                if alias.moduleId == levelId:
                    res.append(alias)
                    break

        return res

    def getParentModulesWithAlias(self, moduleId, modulesArray):
        """Return the parent module with alias"""
        if moduleId != '_model_':
            if moduleId not in modulesArray:
                modulesArray.append(moduleId)
            alias = []
            alias = self.findNodes('originalId', moduleId)
            if alias:
                for a in alias:
                    if a.identifier not in modulesArray:
                        modulesArray.append(a.identifier)

            if self.getNode(moduleId).isin in self.nodeDic:
                return self.getParentModulesWithAlias(self.getNode(moduleId).isin, modulesArray)
            return modulesArray
        else:
            return modulesArray

    def getParentModule(self, moduleId, modulesInLevel):
        """Return parent module"""
        if moduleId == '_model_':
            return
        if moduleId in modulesInLevel:
            return moduleId
        if self.getNode(moduleId).isin in self.nodeDic:
            return self.getParentModule(self.getNode(moduleId).isin, modulesInLevel)
        return

    def getNodesInModule(self, moduleId, nodesInSubLevels):
        """Return nodes un module"""
        subLevelNodes = []
        modulesInSubLevels = []
        subLevelNodes = self.findNodes('moduleId', moduleId)
        if subLevelNodes:
            for node in subLevelNodes:
                if node.nodeClass == 'module':
                    modulesInSubLevels.append(node)

            if modulesInSubLevels:
                for module in modulesInSubLevels:
                    self.getNodesInModule(module.identifier, nodesInSubLevels)

        return nodesInSubLevels

    def findNodes(self, prop, value):
        """Finds nodes by property/value"""
        res = []
        for k, v in self.nodeDic.items():
            if getattr(v, prop) == value:
                v.system or res.append(self.nodeDic[k])

        return res

    def searchNodes(self, filterOptions):
        """Search nodes using filter options """
        res = []
        res = Intellisense().search(self, filterOptions)
        return res

    def getInputs(self, nodeId):
        res = []
        if self.existNode(nodeId):
            for nodeInput in self.getNode(nodeId).inputs:
                if self.existNode(nodeInput):
                    inp = self.getNode(nodeInput)
                    res.append({'id':nodeInput, 
                     'name':inp.title if inp.title is not None else nodeInput, 
                     'nodeClass':inp.nodeClass, 
                     'moduleId':inp.moduleId})

        return res

    def getOutputs(self, nodeId):
        """Get output list of a node"""
        res = []
        if self.existNode(nodeId):
            for nodeOutput in self.getNode(nodeId).outputs:
                if self.existNode(nodeOutput):
                    out = self.getNode(nodeOutput)
                    res.append({'id':nodeOutput, 
                     'name':out.title if out.title is not None else nodeOutput, 
                     'nodeClass':out.nodeClass, 
                     'moduleId':out.moduleId})

        return res

    def moveNodes(self, nodeList, moduleId):
        """Move nodes to other moduleId"""
        res = []
        moduleId = self.clearId(moduleId)
        if self.existNode(moduleId):
            for nodeId in nodeList:
                if self.existNode(nodeId):
                    self.getNode(nodeId).moduleId = moduleId
                    res.append(nodeId)

        return res

    def copyNodes(self, nodeList, moduleId):
        """Copy nodes"""
        res = []
        if self.existNode(moduleId):
            try:
                self._isLoadingModel = True
                rx = '(\'[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*\'|\\"[^\\"\\\\]*(?:\\\\.[^\\"\\\\]*)*\\")|\\b{0}\\b'
                newNodesDic = dict()

                def nodeCreator(_nodeList, _moduleId):
                    for nodeId in _nodeList:
                        nodeId = self.clearId(nodeId)
                        if self.existNode(nodeId):
                            obj = self.getNode(nodeId).toObj()
                            newId = self.getNextIdentifier(f"{obj['identifier']}")
                            newNodesDic[obj['identifier']] = newId
                            obj['identifier'] = newId
                            if obj['moduleId'] == _moduleId:
                                obj['x'] = int(obj['x']) + 10
                                obj['y'] = int(obj['y']) + 10
                            else:
                                obj['moduleId'] = _moduleId
                            nodeObj = self.createNode((obj['identifier']),
                              moduleId=_moduleId)
                            nodeObj.fromObj(obj)
                            res.append(nodeObj.identifier)
                            if nodeObj.nodeClass == 'module':
                                _childrens = [node.identifier for node in self.findNodes('moduleId', nodeId)]
                                nodeCreator(_childrens, newId)

                nodeCreator(nodeList, moduleId)
                for sourceNode, targetNode in newNodesDic.items():
                    newNode = self.getNode(targetNode)
                    currentDef = newNode.definition
                    if currentDef is not None:
                        if currentDef != '':
                            tmpCode = newNode.compileDef(currentDef)
                            if tmpCode is not None:
                                names = newNode.parseNames(tmpCode)
                                for node in names:
                                    if node in newNodesDic:
                                        newRelatedId = newNodesDic[node]
                                        currentDef = re.sub(rx.format(node), lambda m:                                         if m.group(1):
m.group(1) # Avoid dead code: newRelatedId, currentDef, 0, re.IGNORECASE)

                                newNode.definition = currentDef
                    if newNode.originalId is not None:
                        if newNode.originalId in newNodesDic:
                            newNode.originalId = newNodesDic[newNode.originalId]
                    newNode.generateIO()

            finally:
                self._isLoadingModel = False

        return res

    def copyAsValues(self, nodeId, asNewNode=False):
        """ Copy node as values """
        if self.existNode(nodeId):
            node = self.nodeDic[nodeId]
            if node.originalId:
                return self.copyAsValues(node.originalId, asNewNode)
            result = node.result
            if asNewNode:
                newNode = self.createNode(moduleId=(node.moduleId), nodeClass=(node.nodeClass), x=(int(node.x) + 40),
                  y=(int(node.y) + 60))
                newNode.w = node.w
                newNode.h = node.h
                newNode.definition = node.definition
                node = newNode
            evaluator = Evaluator.createInstance(result)
            return evaluator.copyAsValues(result, self.nodeDic, node.identifier)
        return False

    def createInputNodes(self, nodeList):
        """Create input nodes"""
        res = []
        if nodeList is not None:
            for nodeId in nodeList:
                if self.existNode(nodeId):
                    firstNode = self.getNode(nodeId)
                    nodeOrig = self.getOriginalNode(nodeId)
                    inputNode = self.createNode(moduleId=(firstNode.moduleId), nodeClass='formnode', x=(int(firstNode.x) - 70),
                      y=(int(firstNode.y) + 70),
                      originalId=(nodeOrig.identifier))
                    inputNode.w = 240
                    inputNode.h = 36
                    inputNode.color = nodeOrig.color
                    inputNode.definition = 'result = ' + str(nodeOrig.identifier)
                    res.append(inputNode.identifier)

        return res

    def createAlias(self, nodeList):
        """Create node alias"""
        res = []
        if nodeList is not None:
            for nodeId in nodeList:
                if self.existNode(nodeId):
                    firstNode = self.getNode(nodeId)
                    nodeOrig = self.getOriginalNode(nodeId)
                    aliasNode = self.createNode(moduleId=(firstNode.moduleId), nodeClass='alias', x=(int(firstNode.x) + 30),
                      y=(int(firstNode.y) + 30),
                      originalId=(nodeOrig.identifier))
                    aliasNode.w = int(nodeOrig.w)
                    aliasNode.h = int(nodeOrig.h)
                    aliasNode.definition = 'result = ' + str(nodeOrig.identifier)
                    aliasNode.color = BaseNode.getDefaultColor(nodeOrig.nodeClass) if nodeOrig.color is None else nodeOrig.color
                    res.append(aliasNode.identifier)

        return res

    def getOriginalNode(self, nodeId):
        """Get original node from an alias or input node"""
        if self.existNode(nodeId):
            nodeOrig = self.getNode(nodeId)
            if nodeOrig.originalId is None:
                return nodeOrig
            return self.getOriginalNode(nodeOrig.originalId)

    def isCalcNodes(self, nodeList):
        """Return list of Booleans. True for node is calculated otherwise False"""
        res = []
        if nodeList is not None:
            for nodeId in nodeList:
                isCalc = False
                if self.existNode(nodeId):
                    isCalc = self.getNode(nodeId).isCalc
                res.append(isCalc)

        return res

    def exportModule(self, moduleId, filename):
        """Export module to file"""
        _moduleIOEngine = IOModule(self)
        return _moduleIOEngine.exportModule(moduleId, filename)

    def importModule(self, moduleId, filename, importType):
        """Import module from file"""
        _moduleIOEngine = IOModule(self)
        return _moduleIOEngine.importModule(moduleId, filename, importType)

    def exportFlatNode(self, nodeId, numberFormat, columnFormat, fileName):
        """Export node values in flat format"""
        if self.existNode(nodeId):
            evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
            return evaluator.exportFlatNode(self.nodeDic, nodeId, numberFormat, columnFormat, fileName)
        return False

    def dumpNodeToFile(self, nodeId, fileName):
        """Dump current node value to file"""
        if self.existNode(nodeId):
            evaluator = Evaluator.createInstance(self.nodeDic[nodeId].result)
            return evaluator.dumpNodeToFile(self.nodeDic, nodeId, fileName)
        return False

    def saveModel(self, fileName=None):
        """Save model. If fileName is specified, then save to fileName, else return string of ppl """
        self.modelProp['libs'] = self._get_used_libraries()
        toSave = {'modelProp':self.modelProp, 
         'nodeList':[]}
        for k, v in self.nodeDic.items():
            if not v.system:
                toSave['nodeList'].append(v.toObj())

        if fileName:
            if os.path.isfile(fileName):
                filename_to_save = f"{fileName}.tmp#"
                filename_old = f"{fileName}.old#"
                if os.path.isfile(filename_to_save):
                    os.remove(filename_to_save)
                if os.path.isfile(filename_old):
                    os.remove(filename_old)
                with open(filename_to_save, 'w') as (f):
                    f.write(jsonpickle.encode(toSave))
                    f.close()
                os.rename(fileName, filename_old)
                os.rename(filename_to_save, fileName)
                if os.path.isfile(filename_old):
                    new_size = os.path.getsize(fileName)
                    old_size = os.path.getsize(filename_old)
                    if new_size / old_size > 0.8:
                        os.remove(filename_old)
                    else:
                        os.rename(filename_old, f"{fileName}-{datetime.datetime.today().strftime('%Y%m%d-%H%M%S')}.old")
            else:
                with open(fileName, 'w') as (f):
                    f.write(jsonpickle.encode(toSave))
                    f.close()
        return jsonpickle.encode(toSave)

    def openModel(self, fileName=None, textModel=None):
        """Open model.
        If fileName is especified then open from fileName, else open from textModel text """
        self.release()
        opened = {}
        if textModel:
            opened = jsonpickle.decode(textModel)
        else:
            with open(fileName, 'r') as (f):
                opened = jsonpickle.decode(f.read())
                f.close()
        self._modelProp = opened['modelProp']
        self._isLoadingModel = True
        multiplier = 1
        hasBaseNode = False
        for obj in opened['nodeList']:
            if obj['moduleId'] == '_model_':
                node = self.createNode((obj['identifier']), moduleId='_model_')
                if obj['w'] == 50:
                    if obj['h'] == 25:
                        multiplier = 2
                obj['w'] = str(int(obj['w']) * multiplier)
                obj['h'] = str(int(obj['h']) * multiplier)
                node.fromObj(obj)
                self._modelNode = node
                hasBaseNode = True
                break

        if not hasBaseNode:
            self.initialize()
        self.createSystemNodes(fileName)
        rootModelId = self.modelNode.identifier
        for obj in opened['nodeList']:
            if obj['moduleId'] != '_model_':
                if obj['identifier']:
                    if obj['nodeClass'] in ('alias', 'formnode'):
                        if hasattr(obj, 'originalId'):
                            node = self.createNode((obj['identifier']),
                              moduleId=rootModelId, originalId=(obj['originalId']))
                        else:
                            index = obj['definition'].find('=')
                            originalId = obj['definition'][index + 1:].strip()
                            node = self.createNode((obj['identifier']),
                              moduleId=rootModelId, originalId=originalId)
                    else:
                        node = self.createNode((obj['identifier']),
                          moduleId=rootModelId)
                obj['w'] = str(int(obj['w']) * multiplier)
                obj['h'] = str(int(obj['h']) * multiplier)
                node.fromObj(obj)
                node = None

        self.createDefaultNodes()
        [self.nodeDic[nod].generateIO() for nod in self.nodeDic]
        opened = None
        self._isLoadingModel = False
        self.ensureModelLibraries()
        try:
            for key in self.nodeDic:
                if self.nodeDic[key] and self.nodeDic[key].evaluateOnStart:
                    _dummy = self.nodeDic[key].result

        except Exception as ex:
            try:
                print(str(ex))
            finally:
                ex = None
                del ex

        return True

    def closeModel(self):
        """Close model"""
        self.release()

    def getCustomImports(self):
        """Return object with custom imported python modules."""
        if self._customImports is None:
            self._buildCustomImports()
        return self._customImports

    def _buildCustomImports(self):
        """Build custom imports"""
        self._customImports = Model.DEFAULT_IMPORTS.copy()
        self._customImports['pp'] = PyplanFunctions(self)
        self._customImports['selector'] = self._customImports['pp'].selector
        if self.existNode('imports'):
            import_node = self.getNode('imports')
            import_dic = import_node.result
            for key in import_dic:
                if key not in self._customImports:
                    self._customImports[key] = import_dic[key]

    def createSystemNodes(self, fileName):
        """Create system nodes"""
        systemPathNode = self.createNode(identifier='current_path',
          moduleId=(self.modelNode.identifier))
        path = os.path.abspath(fileName[0:fileName.rfind(os.path.sep)]) + os.path.sep
        if self.isLinux():
            path = fileName[:fileName.rfind('/')] + '/'
            self.createSymlinks(path)
        else:
            path = path.replace('\\', '\\\\')
        systemPathNode.system = True
        systemPathNode.definition = 'result="""' + str(path) + '"""'
        os.chdir(str(path))
        node = self.createNode(identifier='pyplan_user', moduleId=(self.modelNode.identifier))
        node.system = True
        node = self.createNode(identifier='cub_refresh', moduleId=(self.modelNode.identifier))
        node.system = True
        node = self.createNode(identifier='pyplan_refresh', moduleId=(self.modelNode.identifier))
        node.system = True
        node = self.createNode(identifier='_scenario_',
          moduleId=(self.modelNode.identifier),
          nodeClass='index')
        node.system = True
        node.title = 'Scenario'
        node.definition = "result = pp.index(['Current'])"
        node = self.createNode(identifier='task_log_endpoint', moduleId=(self.modelNode.identifier),
          nodeClass='variable')
        node.system = True
        node.title = 'TaskLog endpoint'
        node.definition = "result = ''"

    def createSymlinks(self, path):
        if os.getenv('PYPLAN_IDE', '0') != '1':
            if os.getenv('ENGINE_MODE', '') not in ('fixed', 'local'):
                pos = path.index('/', path.index('/', path.index('/', path.index('/', path.index('/') + 1) + 1) + 1) + 1)
                python_folder = f"python{sys.version[:3]}"
                try:
                    folder_list = os.listdir(os.path.join(path[:pos], '.venv', 'lib'))
                    python_folder = folder_list[(len(folder_list) - 1)]
                except Exception as ex:
                    try:
                        pass
                    finally:
                        ex = None
                        del ex

                user_lib_path = os.path.join(path[:pos], '.venv', 'lib', python_folder, 'site-packages')
                venv_path = os.path.join('/venv', 'lib', 'python3.7', 'site-packages')
                if not os.path.isdir(user_lib_path):
                    os.makedirs(user_lib_path, exist_ok=True)
                os.system(f"cp -r -u {venv_path}-bkp/* {user_lib_path}")
                os.system(f"rm -rf {venv_path}")
                os.system(f"ln -s -f {user_lib_path} {venv_path}")

    def createDefaultNodes(self):
        """ Create default nodes as pyplan library, etc """
        if not self.existNode('pyplan_library'):
            pyplan_library_node = self.createNode(identifier='pyplan_library',
              moduleId=(self.modelNode.identifier),
              x=50,
              y=500,
              nodeClass='module')
            pyplan_library_node.title = 'Pyplan library'
            pyplan_library_node.color = '#9fc5e8'
            pyplan_library_node.nodeInfo['showInputs'] = 0
            pyplan_library_node.nodeInfo['showOutputs'] = 0

    def isLinux(self):
        if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
            return True
        return False

    def profileNode(self, nodeId):
        """Perform profile of an node"""
        if self.getNode(nodeId).originalId is not None:
            nodeId = self.getNode(nodeId).originalId
        profile = self.getNode(nodeId).profileNode([], [], self.getNode(nodeId).evaluationVersion, nodeId)
        for node in profile:
            node['calcTime'] = node['evaluationTime'] if node['evaluationTime'] > 0 else 0

        total_time = 0
        for nn in reversed(range(len(profile))):
            node = profile[nn]
            total_time = total_time + node['calcTime']
            node['evaluationTime'] = total_time

        return jsonpickle.encode(profile)

    def evaluate(self, definition, params=None, returnEvaluateTime=False):
        """Evaluate expression"""
        res = None
        evalNode = BaseNode(model=self,
          identifier='__evalnode__',
          nodeClass='variable')
        evalNode._definition = definition
        evalNode.calculate(params)
        res = evalNode.result
        evaluateTime = evalNode.lastEvaluationTime
        evalNode.release()
        evalNode = None
        if returnEvaluateTime:
            return (
             res, evaluateTime)
        return res

    def callFunction(self, nodeId, params=None):
        """Call node function with params"""
        res = None
        if self.existNode(nodeId):
            nodeFn = self.getNode(nodeId).result
            if params is None:
                res = nodeFn()
            else:
                res = nodeFn(**params)
        return res

    def getIdentifierByNode(self, result):
        """Return Identifier of node searching by your result"""
        res = ''
        for nodeId in self.nodeDic:
            if self.nodeDic[nodeId].isCalc and self.nodeDic[nodeId].result is result:
                res = nodeId
                break

        return res

    def loadScenario(self, nodeId, scenarioData):
        """ Load and fill scenarioDic """
        res = False
        if scenarioData is not None:
            if self.existNode(nodeId):
                scenarioResult = []
                scenarioNames = []
                scenList = str(scenarioData).split('##')
                for scenItem in scenList:
                    arr = str(scenItem).split('||')
                    if len(arr) == 3:
                        scenarioName = arr[1]
                        fileName = arr[2]
                        _result = None
                        if arr[0] == '-1':
                            _result = self.getNode(nodeId).result
                        else:
                            nodeDef = ''
                            with open(fileName, 'r') as (f):
                                nodeDef = f.read()
                                f.close()
                            _result = self.evaluate(nodeDef)
                        scenarioResult.append(_result)
                        scenarioNames.append(scenarioName)

                scenarioIndex = self.getNode('_scenario_')
                scenarioIndex.definition = "result = pp.index(['" + "','".join(scenarioNames) + "'])"
                if len(scenarioResult) > 0:
                    finalResult = None
                    if isinstance(scenarioResult[0], xr.DataArray):
                        finalResult = xr.concat(scenarioResult, scenarioIndex.result.dataArray)
                    else:
                        finalResult = xr.DataArray(scenarioResult, scenarioIndex.result.coord)
                    self._scenarioDic[nodeId] = finalResult
                    res = True
        return res

    def unloadScenario(self):
        """Unload all scenarios and clean calculated nodes in the scenario """
        for key in self._scenarioDic:
            self._scenarioDic[key] = None

        self._scenarioDic = dict()
        scenarioIndex = self.getNode('_scenario_')
        scenarioIndex.definition = "result = pp.index(['Current'])"

    def geoUnclusterData(self, nodeId, rowIndex, attIndex, latField='latitude', lngField='longitude', geoField='geoField', labelField='labelField', sizeField='sizeField', colorField='colorField', iconField='iconField'):
        """get unclusted data for geo representation."""
        if self.existNode(nodeId):
            result = self.nodeDic[nodeId].result
            if result is not None:
                self.evaluationVersion += 1
                evaluator = Evaluator.createInstance(result)
                return evaluator.geoUnclusterData(result, self.nodeDic, nodeId, rowIndex, attIndex, latField, lngField, geoField, labelField, sizeField, colorField, iconField)
        else:
            return ''

    def callWizard(self, param):
        """ Start and call wizard toolbar """
        obj = jsonpickle.decode(param)
        key = obj['wizard']
        action = obj['action']
        params = obj['params']
        if self._wizard is None or self._wizard.code != key:
            self._wizard = self._getWizzard(key)
        toCall = getattr(self._wizard, action)
        return toCall(self, params)

    def createNewModel(self, modelFile=None, modelName=None):
        self.release()
        self._modelProp = {}
        self._isLoadingModel = True
        self.initialize(modelName)
        self.createSystemNodes(modelFile)
        self._isLoadingModel = False
        if modelFile:
            self.saveModel(modelFile)
        return True

    def _getWizzard(self, key):
        key = key.lower()
        if key == 'calculatedfield':
            return CalculatedField.Wizard()
        if key == 'selectcolumns':
            return SelectColumns.Wizard()
        if key == 'selectrows':
            return SelectRows.Wizard()
        if key == 'sourcecsv':
            return sourcecsv.Wizard()
        if key == 'dataframeindex':
            return DataframeIndex.Wizard()
        if key == 'dataframegroupby':
            return DataframeGroupby.Wizard()

    def getSystemResources(self, onlyMemory=False):
        """Return current system resources"""

        def _read_int(file):
            data = 0
            with open(file, 'r') as (f):
                data = int(f.read())
                f.close()
            return data

        def _read_cache():
            data = 0
            with open('/sys/fs/cgroup/memory/memory.stat', 'r') as (f):
                line = f.readline()
                data = int(str(line).split(' ')[1])
                f.close()
            return data

        mem_limit = _read_int('/sys/fs/cgroup/memory/memory.limit_in_bytes') / 1024 / 1024 / 1024
        if mem_limit > 200:
            total_host = ''
            with open('/proc/meminfo', 'r') as (f):
                line1 = f.readline()
                total_host = str(line1).split(' ')[-2:-1][0]
                mem_limit = int(total_host) / 1024 / 1024
        mem_used = (_read_int('/sys/fs/cgroup/memory/memory.usage_in_bytes') - _read_cache()) / 1024 / 1024 / 1024
        if onlyMemory:
            return {'totalMemory':mem_limit,  'usedMemory':mem_used}
        time_1 = datetime.datetime.now()
        cpu_time_1 = _read_int('/sys/fs/cgroup/cpu/cpuacct.usage')
        sleep(0.3)
        time_2 = datetime.datetime.now()
        cpu_time_2 = _read_int('/sys/fs/cgroup/cpu/cpuacct.usage')
        delta_time = (time_2 - time_1).microseconds * 10
        used_cpu = (cpu_time_2 - cpu_time_1) / delta_time
        used_cpu = used_cpu if used_cpu < 100 else 100
        current_node = self._currentProcessingNode
        if self.existNode(current_node):
            node = self.getNode(current_node)
            if node.title:
                current_node = f"{node.title} ({current_node})"
        return {'totalMemory':mem_limit,  'usedMemory':mem_used, 
         'usedCPU':used_cpu, 
         'pid':self.getPID(), 
         'currentNode':current_node}

    def ensureModelLibraries(self):
        """Ensure that all model libs are installed"""
        try:
            if 'libs' not in self.modelProp:
                self.modelProp['libs'] = []
            modelLibs = self.modelProp['libs']
            installed_libs_str = self.listInstalledLibraries()
            installed_libs = jsonpickle.decode(installed_libs_str)
            installed_libs_dic = dict()
            for installed_lib in installed_libs:
                installed_libs_dic[installed_lib['name']] = installed_lib['version']

            to_install = ''
            for lib in modelLibs:
                if lib['name'] not in installed_libs_dic:
                    to_install += f" {lib['name']}=={lib['version']}"

            if to_install != '':
                self._installLibrary(to_install)
        except Exception as ex:
            try:
                print(f"Error checking libraries. {ex}")
            finally:
                ex = None
                del ex

    def _installLibrary(self, lib):
        cmd = f"pip install {lib}"
        http_proxy = os.getenv('PYPLAN_HTTP_PROXY')
        https_proxy = os.getenv('PYPLAN_HTTPS_PROXY')
        if http_proxy:
            cmd += f" --proxy {http_proxy}"
        else:
            if https_proxy:
                cmd += f" --proxy {https_proxy}"
        p = subprocess.Popen((split(cmd)), stdout=(subprocess.PIPE), stderr=(subprocess.PIPE),
          universal_newlines=True)
        nn = 0
        while p.stdout is not None and nn < 240:
            line = p.stdout.readline()
            if not line:
                p.stdout.flush()
                aa, err = p.communicate()
                if err:
                    self._currentInstallProgress.append(err.rstrip('\n'))
                break
            sleep(1)
            nn += 1
            self._currentInstallProgress.append(line.rstrip('\n'))

        importlib.invalidate_caches()

    def installLibrary(self, lib, target):
        """install python library"""
        self._currentInstallProgress = []
        thread = threading.Thread(target=(self._installLibrary), args=(lib,))
        thread.start()
        return 'ok'

    def _get_used_libraries--- This code section failed: ---

 L.1649       0_2  SETUP_EXCEPT        624  'to 624'

 L.1650         4  LOAD_GLOBAL              re
                6  LOAD_METHOD              compile
                8  LOAD_STR                 '(^import\\s.*)|(^from\\s.*)'
               10  LOAD_GLOBAL              re
               12  LOAD_ATTR                M
               14  CALL_METHOD_2         2  '2 positional arguments'
               16  STORE_FAST               '_regex'

 L.1651        18  BUILD_LIST_0          0 
               20  STORE_FAST               '_temp_imports'

 L.1652        22  LOAD_GLOBAL              dict
               24  CALL_FUNCTION_0       0  '0 positional arguments'
               26  STORE_FAST               '_imports'

 L.1653        28  BUILD_LIST_0          0 
               30  STORE_FAST               '_used_libraries'

 L.1656        32  SETUP_LOOP          116  'to 116'
               34  LOAD_FAST                'self'
               36  LOAD_ATTR                nodeDic
               38  GET_ITER         
             40_0  COME_FROM            58  '58'
               40  FOR_ITER            114  'to 114'
               42  STORE_FAST               'node_id'

 L.1657        44  LOAD_FAST                'self'
               46  LOAD_ATTR                nodeDic
               48  LOAD_FAST                'node_id'
               50  BINARY_SUBSCR    
               52  LOAD_ATTR                definition
               54  STORE_FAST               '_def'

 L.1658        56  LOAD_FAST                '_def'
               58  POP_JUMP_IF_FALSE    40  'to 40'

 L.1659        60  LOAD_GLOBAL              re
               62  LOAD_METHOD              finditer
               64  LOAD_FAST                '_regex'
               66  LOAD_FAST                '_def'
               68  CALL_METHOD_2         2  '2 positional arguments'
               70  STORE_FAST               '_finditer'

 L.1660        72  SETUP_LOOP          112  'to 112'
               74  LOAD_FAST                '_finditer'
               76  GET_ITER         
             78_0  COME_FROM            92  '92'
               78  FOR_ITER            110  'to 110'
               80  STORE_FAST               'match'

 L.1661        82  LOAD_FAST                'match'
               84  LOAD_METHOD              group
               86  CALL_METHOD_0         0  '0 positional arguments'
               88  LOAD_FAST                '_temp_imports'
               90  COMPARE_OP               not-in
               92  POP_JUMP_IF_FALSE    78  'to 78'

 L.1662        94  LOAD_FAST                '_temp_imports'
               96  LOAD_METHOD              append
               98  LOAD_FAST                'match'
              100  LOAD_METHOD              group
              102  CALL_METHOD_0         0  '0 positional arguments'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  POP_TOP          
              108  JUMP_BACK            78  'to 78'
              110  POP_BLOCK        
            112_0  COME_FROM_LOOP       72  '72'
              112  JUMP_BACK            40  'to 40'
              114  POP_BLOCK        
            116_0  COME_FROM_LOOP       32  '32'

 L.1666   116_118  SETUP_LOOP          508  'to 508'
              120  LOAD_FAST                '_temp_imports'
              122  GET_ITER         
            124_0  COME_FROM           488  '488'
          124_126  FOR_ITER            506  'to 506'
              128  STORE_FAST               '_element'

 L.1667       130  LOAD_FAST                '_element'
              132  LOAD_CONST               None
              134  LOAD_CONST               6
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  LOAD_STR                 'import'
              142  COMPARE_OP               ==
          144_146  POP_JUMP_IF_FALSE   364  'to 364'

 L.1669       148  LOAD_FAST                '_element'
              150  LOAD_CONST               7
              152  LOAD_CONST               None
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              find
              160  LOAD_STR                 ','
              162  CALL_METHOD_1         1  '1 positional argument'
              164  LOAD_CONST               -1
              166  COMPARE_OP               !=
              168  POP_JUMP_IF_FALSE   238  'to 238'

 L.1671       170  SETUP_LOOP          362  'to 362'
              172  LOAD_FAST                '_element'
              174  LOAD_CONST               7
              176  LOAD_CONST               None
              178  BUILD_SLICE_2         2 
              180  BINARY_SUBSCR    
              182  LOAD_METHOD              split
              184  LOAD_STR                 ','
              186  CALL_METHOD_1         1  '1 positional argument'
              188  GET_ITER         
              190  FOR_ITER            234  'to 234'
              192  STORE_FAST               '_el'

 L.1672       194  LOAD_FAST                'self'
              196  LOAD_METHOD              _check_import_function

 L.1673       198  LOAD_FAST                '_el'
              200  LOAD_METHOD              strip
              202  CALL_METHOD_0         0  '0 positional arguments'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  LOAD_STR                 'import'
              208  LOAD_CONST               None
              210  LOAD_CONST               None
              212  LOAD_CONST               ('import_name', 'import_type', 'name', 'version')
              214  BUILD_CONST_KEY_MAP_4     4 
              216  LOAD_FAST                '_imports'
              218  LOAD_FAST                'self'
              220  LOAD_METHOD              _check_import_function
              222  LOAD_FAST                '_el'
              224  LOAD_METHOD              strip
              226  CALL_METHOD_0         0  '0 positional arguments'
              228  CALL_METHOD_1         1  '1 positional argument'
              230  STORE_SUBSCR     
              232  JUMP_BACK           190  'to 190'
              234  POP_BLOCK        
              236  JUMP_FORWARD        362  'to 362'
            238_0  COME_FROM           168  '168'

 L.1674       238  LOAD_FAST                '_element'
              240  LOAD_CONST               7
              242  LOAD_CONST               None
              244  BUILD_SLICE_2         2 
              246  BINARY_SUBSCR    
              248  LOAD_METHOD              find
              250  LOAD_STR                 ' as '
              252  CALL_METHOD_1         1  '1 positional argument'
              254  LOAD_CONST               -1
              256  COMPARE_OP               !=
          258_260  POP_JUMP_IF_FALSE   316  'to 316'

 L.1676       262  LOAD_FAST                '_element'
              264  LOAD_CONST               7
              266  LOAD_FAST                '_element'
              268  LOAD_METHOD              find
              270  LOAD_STR                 ' as '
              272  CALL_METHOD_1         1  '1 positional argument'
              274  BUILD_SLICE_2         2 
              276  BINARY_SUBSCR    
              278  LOAD_METHOD              strip
              280  CALL_METHOD_0         0  '0 positional arguments'
              282  STORE_FAST               '_el'

 L.1677       284  LOAD_FAST                'self'
              286  LOAD_METHOD              _check_import_function

 L.1678       288  LOAD_FAST                '_el'
              290  CALL_METHOD_1         1  '1 positional argument'
              292  LOAD_STR                 'import'
              294  LOAD_CONST               None
              296  LOAD_CONST               None
              298  LOAD_CONST               ('import_name', 'import_type', 'name', 'version')
              300  BUILD_CONST_KEY_MAP_4     4 
              302  LOAD_FAST                '_imports'
              304  LOAD_FAST                'self'
              306  LOAD_METHOD              _check_import_function
              308  LOAD_FAST                '_el'
              310  CALL_METHOD_1         1  '1 positional argument'
              312  STORE_SUBSCR     
              314  JUMP_FORWARD        362  'to 362'
            316_0  COME_FROM           258  '258'

 L.1681       316  LOAD_FAST                '_element'
              318  LOAD_CONST               7
              320  LOAD_CONST               None
              322  BUILD_SLICE_2         2 
              324  BINARY_SUBSCR    
              326  LOAD_METHOD              strip
              328  CALL_METHOD_0         0  '0 positional arguments'
              330  STORE_FAST               '_el'

 L.1682       332  LOAD_FAST                'self'
              334  LOAD_METHOD              _check_import_function

 L.1683       336  LOAD_FAST                '_el'
              338  CALL_METHOD_1         1  '1 positional argument'
              340  LOAD_STR                 'import'
              342  LOAD_CONST               None
              344  LOAD_CONST               None
              346  LOAD_CONST               ('import_name', 'import_type', 'name', 'version')
              348  BUILD_CONST_KEY_MAP_4     4 
              350  LOAD_FAST                '_imports'
              352  LOAD_FAST                'self'
              354  LOAD_METHOD              _check_import_function
              356  LOAD_FAST                '_el'
              358  CALL_METHOD_1         1  '1 positional argument'
              360  STORE_SUBSCR     
            362_0  COME_FROM           314  '314'
            362_1  COME_FROM           236  '236'
            362_2  COME_FROM_LOOP      170  '170'
              362  JUMP_BACK           124  'to 124'
            364_0  COME_FROM           144  '144'

 L.1684       364  LOAD_FAST                '_element'
              366  LOAD_CONST               None
              368  LOAD_CONST               4
              370  BUILD_SLICE_2         2 
              372  BINARY_SUBSCR    
              374  LOAD_STR                 'from'
              376  COMPARE_OP               ==
          378_380  POP_JUMP_IF_FALSE   484  'to 484'

 L.1686       382  LOAD_FAST                '_element'
              384  LOAD_CONST               5
              386  LOAD_CONST               None
              388  BUILD_SLICE_2         2 
              390  BINARY_SUBSCR    
              392  LOAD_METHOD              find
              394  LOAD_STR                 ' import '
              396  CALL_METHOD_1         1  '1 positional argument'
              398  LOAD_CONST               -1
              400  COMPARE_OP               !=
          402_404  POP_JUMP_IF_FALSE   460  'to 460'

 L.1687       406  LOAD_FAST                '_element'
              408  LOAD_CONST               5
              410  LOAD_FAST                '_element'
              412  LOAD_METHOD              find
              414  LOAD_STR                 ' import '
              416  CALL_METHOD_1         1  '1 positional argument'
              418  BUILD_SLICE_2         2 
              420  BINARY_SUBSCR    
              422  LOAD_METHOD              strip
              424  CALL_METHOD_0         0  '0 positional arguments'
              426  STORE_FAST               '_el'

 L.1688       428  LOAD_FAST                'self'
              430  LOAD_METHOD              _check_import_function

 L.1689       432  LOAD_FAST                '_el'
              434  CALL_METHOD_1         1  '1 positional argument'
              436  LOAD_STR                 'from'
              438  LOAD_CONST               None
              440  LOAD_CONST               None
              442  LOAD_CONST               ('import_name', 'import_type', 'name', 'version')
              444  BUILD_CONST_KEY_MAP_4     4 
              446  LOAD_FAST                '_imports'
              448  LOAD_FAST                'self'
              450  LOAD_METHOD              _check_import_function
              452  LOAD_FAST                '_el'
              454  CALL_METHOD_1         1  '1 positional argument'
              456  STORE_SUBSCR     
              458  JUMP_FORWARD        482  'to 482'
            460_0  COME_FROM           402  '402'

 L.1690       460  LOAD_FAST                'self'
              462  LOAD_ATTR                ws
          464_466  POP_JUMP_IF_FALSE   504  'to 504'

 L.1691       468  LOAD_FAST                'self'
              470  LOAD_ATTR                ws
              472  LOAD_METHOD              sendMsg
              474  LOAD_FAST                '_element'
              476  LOAD_STR                 'Could not find import from'
              478  CALL_METHOD_2         2  '2 positional arguments'
              480  POP_TOP          
            482_0  COME_FROM           458  '458'
              482  JUMP_BACK           124  'to 124'
            484_0  COME_FROM           378  '378'

 L.1692       484  LOAD_FAST                'self'
              486  LOAD_ATTR                ws
              488  POP_JUMP_IF_FALSE   124  'to 124'

 L.1693       490  LOAD_FAST                'self'
              492  LOAD_ATTR                ws
              494  LOAD_METHOD              sendMsg
              496  LOAD_FAST                '_element'
              498  LOAD_STR                 'Element not recognized'
              500  CALL_METHOD_2         2  '2 positional arguments'
              502  POP_TOP          
            504_0  COME_FROM           464  '464'
              504  JUMP_BACK           124  'to 124'
              506  POP_BLOCK        
            508_0  COME_FROM_LOOP      116  '116'

 L.1695       508  LOAD_FAST                'self'
              510  LOAD_METHOD              _check_installed_libraries
              512  CALL_METHOD_0         0  '0 positional arguments'
              514  STORE_FAST               '_installed_libs'

 L.1696       516  SETUP_LOOP          620  'to 620'
              518  LOAD_FAST                '_imports'
              520  LOAD_METHOD              keys
              522  CALL_METHOD_0         0  '0 positional arguments'
              524  GET_ITER         
            526_0  COME_FROM           596  '596'
              526  FOR_ITER            618  'to 618'
              528  STORE_FAST               'key'

 L.1697       530  SETUP_LOOP          582  'to 582'
              532  LOAD_FAST                '_installed_libs'
              534  GET_ITER         
            536_0  COME_FROM           554  '554'
              536  FOR_ITER            580  'to 580'
              538  STORE_FAST               'lib'

 L.1698       540  LOAD_FAST                'lib'
              542  LOAD_FAST                '_imports'
              544  LOAD_FAST                'key'
              546  BINARY_SUBSCR    
              548  LOAD_STR                 'import_name'
              550  BINARY_SUBSCR    
              552  COMPARE_OP               ==
          554_556  POP_JUMP_IF_FALSE   536  'to 536'

 L.1699       558  LOAD_FAST                '_imports'
              560  LOAD_FAST                'key'
              562  BINARY_SUBSCR    
              564  LOAD_METHOD              update
              566  LOAD_FAST                '_installed_libs'
              568  LOAD_FAST                'lib'
              570  BINARY_SUBSCR    
              572  CALL_METHOD_1         1  '1 positional argument'
              574  POP_TOP          
          576_578  JUMP_BACK           536  'to 536'
              580  POP_BLOCK        
            582_0  COME_FROM_LOOP      530  '530'

 L.1700       582  LOAD_FAST                '_imports'
              584  LOAD_FAST                'key'
              586  BINARY_SUBSCR    
              588  LOAD_STR                 'name'
              590  BINARY_SUBSCR    
              592  LOAD_CONST               None
              594  COMPARE_OP               !=
          596_598  POP_JUMP_IF_FALSE   526  'to 526'

 L.1701       600  LOAD_FAST                '_used_libraries'
              602  LOAD_METHOD              append
              604  LOAD_FAST                '_imports'
              606  LOAD_FAST                'key'
              608  BINARY_SUBSCR    
              610  CALL_METHOD_1         1  '1 positional argument'
              612  POP_TOP          
          614_616  JUMP_BACK           526  'to 526'
              618  POP_BLOCK        
            620_0  COME_FROM_LOOP      516  '516'

 L.1703       620  LOAD_FAST                '_used_libraries'
              622  RETURN_VALUE     
            624_0  COME_FROM_EXCEPT      0  '0'

 L.1704       624  DUP_TOP          
              626  LOAD_GLOBAL              Exception
              628  COMPARE_OP               exception-match
          630_632  POP_JUMP_IF_FALSE   684  'to 684'
              634  POP_TOP          
              636  STORE_FAST               'ex'
              638  POP_TOP          
              640  SETUP_FINALLY       672  'to 672'

 L.1705       642  LOAD_FAST                'self'
              644  LOAD_ATTR                ws
          646_648  POP_JUMP_IF_FALSE   668  'to 668'

 L.1706       650  LOAD_FAST                'self'
              652  LOAD_ATTR                ws
              654  LOAD_METHOD              sendMsg
              656  LOAD_GLOBAL              str
              658  LOAD_FAST                'ex'
              660  CALL_FUNCTION_1       1  '1 positional argument'
              662  LOAD_STR                 'Error getting used libraries'
              664  CALL_METHOD_2         2  '2 positional arguments'
              666  POP_TOP          
            668_0  COME_FROM           646  '646'

 L.1707       668  BUILD_LIST_0          0 
              670  RETURN_VALUE     
            672_0  COME_FROM_FINALLY   640  '640'
              672  LOAD_CONST               None
              674  STORE_FAST               'ex'
              676  DELETE_FAST              'ex'
              678  END_FINALLY      
              680  POP_EXCEPT       
              682  JUMP_FORWARD        686  'to 686'
            684_0  COME_FROM           630  '630'
              684  END_FINALLY      
            686_0  COME_FROM           682  '682'

Parse error at or near `POP_BLOCK' instruction at offset 506

    def _check_import_function(self, _element):
        if _element.find('.') != -1:
            return _element[:_element.find('.')].strip()
        return _element

    def _check_installed_libraries(self):
        try:
            installed_libraries = dict()
            dirs = sys.path if os.getenv('PYPLAN_IDE') else [
             '/venv/lib64/python3.7/site-packages/']
            for _dir in dirs:
                installed_modules = dict()
                if '.zip' not in _dir:
                    for folder in os.listdir(_dir):
                        if not '.dist-info' in folder:
                            if '.egg-info' in folder:
                                top_level_file = os.path.join(_dir, folder, 'top_level.txt')
                                if os.path.isfile(top_level_file):
                                    top_level = str(open(top_level_file).read()).replace('\n', '')
                                    metadata_file = os.path.join(_dir, folder, 'METADATA' if '.dist-info' in folder else 'PKG-INFO')
                                    if os.path.isfile(metadata_file):
                                        metadata = str(open(metadata_file).read())
                                        metadata_arr = metadata.split('\n')
                                        for metadata_item in metadata_arr:
                                            if str(metadata_item).startswith('Name: '):
                                                pypi_name = str(metadata_item).split(' ')[1]

                            installed_modules[top_level] = {'name':pypi_name, 
                             'version':pypi_version}

                installed_libraries.update(installed_modules)

            return installed_libraries
        except Exception as ex:
            try:
                if self.ws:
                    self.ws.sendMsg(str(ex), 'Error checking installed libraries')
                return {}
            finally:
                ex = None
                del ex

    def listInstalledLibraries(self):
        cmd = 'pip list -v --disable-pip-version-check --format=json'
        popen = subprocess.Popen((split(cmd)),
          stdout=(subprocess.PIPE), universal_newlines=True)
        stdout, stderr = popen.communicate()
        if stderr:
            raise ValueError(f"Error listing installed libraries: {str(stderr)}")
        return stdout

    def uninstallLibrary(self, lib, target):
        """Uninstall python library"""
        cmd = f"find {target} -name '*{lib.replace('-', '_')}*' -exec rm -rf {{}} \\;"
        popen = subprocess.Popen((split(cmd)),
          stdout=(subprocess.PIPE), universal_newlines=True)
        stdout, stderr = popen.communicate()
        importlib.invalidate_caches()
        if stderr:
            raise ValueError(f"Error uninstalling library: {str(stderr)}")
        return stdout

    def getInstallProgress(self, from_line):
        """Return install library progress"""
        from_line = int(from_line)
        if len(self._currentInstallProgress) == 0 or from_line > len(self._currentInstallProgress):
            return []
        return self._currentInstallProgress[from_line:]

    def setNodeIdFromTitle(self, node_id):
        """Generate node id from node identifier """
        res = {'node_id': node_id}
        model_props = self.getModelProperties()
        if 'changeIdentifier' not in model_props or model_props['changeIdentifier'] == '1':
            if self.existNode(node_id):
                node = self.nodeDic[node_id]
                new_id = ''
                try:
                    if node.title:
                        new_id = self._removeDiacritics(node.title)
                except Exception as ex:
                    try:
                        raise ValueError(f"Error finding node title: {str(ex)}")
                    finally:
                        ex = None
                        del ex

                if new_id:
                    if self.existNode(new_id):
                        new_id = self.getNextIdentifier(new_id)
                    node.identifier = new_id
                    res['node_id'] = new_id
        return res

    def _removeDiacritics(self, text):
        """Removes all diacritic marks from the given string"""
        norm_txt = unicodedata.normalize('NFD', text)
        shaved = ''.join((c for c in norm_txt if not unicodedata.combining(c)))
        no_spaces = unicodedata.normalize('NFC', shaved).lower().replace(' ', '_')
        final_text = no_spaces
        p = re.compile('[a-z0-9_]+')
        for i in range(0, len(no_spaces)):
            if not p.match(no_spaces[i]):
                final_text = final_text[:i] + '_' + final_text[i + 1:]

        p2 = re.compile('[a-z]+')
        if not p2.match(final_text[0]):
            final_text = 'a' + final_text[1:]
        return final_text