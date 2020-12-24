# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/BaseNode.py
# Compiled at: 2020-05-07 09:53:16
# Size of source mod 2**32: 32054 bytes
import datetime as dt, io, re, uuid
from contextlib import redirect_stdout
from sys import exc_info, getsizeof
from types import CodeType
import numpy as np
import pyplan_core.classes.evaluators.Evaluator as Evaluator
import pyplan_core.classes.dynamics.BaseDynamic as BaseDynamic
import pyplan_core.classes.dynamics.FactoryDynamic as FactoryDynamic
import pyplan_core.cubepy.Helpers as Helpers
import pyplan_core.classes.IOEngine as IOEngine
import pyplan_core.classes.NodeInfo as NodeInfo
from pyplan_core.classes.PyplanFunctions import Selector

class BaseNode(object):
    SERIALIZABLE_PROPERTIES = [
     'identifier', 'definition', 'title', 'nodeClass', 'moduleId', 'x', 'y', 'z', 'w', 'h',
     'description', 'units', 'color', 'errorInDef', 'nodeInfo', 'nodeFont', 'numberFormat', 'originalId', 'extraData', 'picture', 'evaluateOnStart']
    FORMNODE_TYPE_CHECKBOX = 0
    FORMNODE_TYPE_COMBOBOX = 1
    FORMNODE_TYPE_SCALAR = 2
    FORMNODE_TYPE_BUTTON = 3

    def __init__(self, model, identifier=None, nodeClass=None, moduleId=None, x=None, y=None, originalId=None):
        self._model = model
        self._originalId = originalId
        self._result = None
        self._isCalc = False
        self._title = None
        self._description = None
        self.units = None
        self.numberFormat = None
        self.color = None
        self.errorInDef = False
        self.nodeClass = nodeClass if nodeClass is not None else 'variable'
        self._definition = self.getDefaultDefinitionByClass(self.nodeClass)
        self.nodeInfo = self.getDefaultNodeinfoByClass(self.nodeClass)
        self.moduleId = moduleId if moduleId is not None else self._model.modelNode.identifier
        self.x = int(x) if x is not None else 100
        self.y = int(y) if y is not None else 100
        self.z = 1
        if nodeClass == 'text':
            self.z = -1
        else:
            self.w = 100
            self.h = 50
            self._ioEngine = IOEngine(self)
            self._resultMemory = 0
            self.system = False
            self.lastEvaluationTime = 0
            self.lastEvaluationConsole = ''
            self.lastLazyTime = 0
            self.evaluationVersion = 0
            self.profileParent = None
            self.nodeFont = None
            self._bypassCircularEvaluator = False
            self.extraData = None
            self.dynamicEvaluator = None
            self.picture = None
            self._hierarchy_parents = None
            self._hierarchy_maps = None
            self._releaseMemory = False
            self._evaluateOnStart = False
            nodeFormat = model.getDefaultNodeFormat(self.nodeClass)
            if identifier is None:
                if nodeClass is not None:
                    if nodeClass == 'alias' or nodeClass == 'formnode' or nodeClass == 'text':
                        self._identifier = 'a' + str(uuid.uuid4().hex).lower()
            elif nodeClass == 'index':
                self._identifier = model.getNextIdentifier('index')
            else:
                self._identifier = model.getNextIdentifier('node')
            if nodeFormat is not None:
                if nodeFormat['nodeClass'] is not None:
                    if not nodeFormat['nodeClass'] == 'alias':
                        if nodeFormat['nodeClass'] == 'formnode' or nodeFormat['nodeClass'] == 'text':
                            self._identifier = 'a' + str(uuid.uuid4().hex).lower()
                    elif nodeFormat['nodeClass'] == 'index':
                        self._identifier = model.getNextIdentifier('index')
                    else:
                        self._identifier = model.getNextIdentifier('node')
                else:
                    self._identifier = identifier
        if nodeFormat is not None:
            self.fromObj(nodeFormat)

    def __del__(self):
        self.release()

    def release(self):
        """Release object"""
        self._model = None
        self._result = None
        self._identifier = None
        self._definition = None
        self.moduleId = None
        self.dynamicEvaluator = None
        if self.ioEngine is not None:
            self.ioEngine.release()
            self._ioEngine = None

    def toObj(self, exceptions=None, properties=None, fillDefaultProperties=False):
        """Convert node to dictionary"""
        res = {}
        if properties is not None:
            for k in properties:
                if k in BaseNode.SERIALIZABLE_PROPERTIES and hasattr(self, k):
                    res[k] = getattr(self, k)

        else:
            for k in BaseNode.SERIALIZABLE_PROPERTIES:
                if exceptions is None or k not in exceptions:
                    if hasattr(self, k):
                        res[k] = getattr(self, k)

        if fillDefaultProperties:
            if 'color' not in res or res['color'] is None:
                res['color'] = BaseNode.getDefaultColor(self.nodeClass)
            res['hasPicture'] = self.hasPicture
            if self.nodeClass in ('formnode', 'alias'):
                res['originalId'] = self.originalId
                res['originalClass'] = self.originalClass
                if self.nodeClass == 'formnode':
                    res['formNodeType'] = self.formNodeType
                    res['formNodeExtraValue'] = self.formNodeExtraValue
                    try:
                        res['formNodeValue'] = self.formNodeValue
                    except TypeError as ex:
                        try:
                            res['formNodeValue'] = str(ex)
                            res['formNodeType'] = self.FORMNODE_TYPE_SCALAR
                        finally:
                            ex = None
                            del ex

        return res

    def fromObj(self, obj):
        """Convert dictionary to basenode object"""
        for k in BaseNode.SERIALIZABLE_PROPERTIES:
            if k in obj:
                if k == 'nodeInfo':
                    if isinstance(obj[k], dict):
                        obj[k] = NodeInfo(obj[k]['showInputs'], obj[k]['showOutputs'], obj[k]['showLabel'], obj[k]['showBorder'], obj[k]['fill'], obj[k]['useNodeFont'])
                setattr(self, k, obj[k])

    @property
    def node(self):
        return self

    @property
    def model(self):
        return self._model

    @property
    def result(self):
        try:
            self.calculate()
        except Exception as e:
            try:
                err = str(e)
                if 'Error evaluating' not in err:
                    title = self.title
                    if title is None:
                        title = ''
                    else:
                        title = title + ' '
                    title = title + '(' + self.identifier + ') '
                    err = 'Error evaluating ' + title + ': ' + err
                raise ValueError(err)
            finally:
                e = None
                del e

        try:
            return self._result
        finally:
            if self.releaseMemory:
                self._isCalc = False
                self.profileParent = None
                self._result = None
                self._resultMemory = 0

    @property
    def isCalc(self):
        return self._isCalc

    @property
    def releaseMemory(self):
        return self._releaseMemory

    @releaseMemory.setter
    def releaseMemory(self, value):
        self._releaseMemory = value

    @property
    def evaluateOnStart(self):
        return self._evaluateOnStart

    @evaluateOnStart.setter
    def evaluateOnStart(self, value):
        self._evaluateOnStart = value

    @property
    def resultType(self):
        if self._isCalc:
            return str(type(self.result))
        return ''

    @property
    def usedMemory(self):
        return (getsizeof(self.definition) + self._resultMemory) / 1024 / 1024

    @property
    def hasPicture(self):
        if self.picture:
            return True
        return False

    @property
    def title(self):
        if self.originalId is not None:
            if self.model.existNode(self.originalId):
                return self.model.getNode(self.originalId).title
            return self._title
        else:
            return self._title

    @title.setter
    def title(self, value):
        self._title = value
        if self.isCalc:
            self.postCalculate()

    @property
    def description(self):
        if self.originalId is not None:
            if self.model.existNode(self.originalId):
                return self.model.getNode(self.originalId).description
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def definition(self):
        return self._definition

    @definition.setter
    def definition(self, value):
        if not self.model.isLoadingModel:
            value = self.sanitizeDefinition(value)
        self._definition = value
        if not self.model.isLoadingModel:
            self.invalidate()
            self.generateIO()
        self._isCalc = False

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        if value != self._identifier:
            if self._model.existNode(value):
                raise ValueError("'The id '" + value + "' already exists")
            if self._model.updateNodeIdInDic(self._identifier, value):
                self.ioEngine.updateNodeId(self._identifier, value)
                self._identifier = value
                if self.isCalc:
                    self.invalidate()

    @property
    def isIndexed(self):
        raise ValueError('TODO: Mover isIndexed a clase BaseEvaluator')
        return False

    @property
    def indexes(self):
        res = []
        self.calculate()
        if self._result is not None:
            evaluator = Evaluator.createInstance(self._result)
            return evaluator.getIndexes(self)

    @property
    def ioEngine(self):
        return self._ioEngine

    @property
    def inputs(self):
        return self.ioEngine.inputs

    @property
    def outputs(self):
        return self.ioEngine.outputs

    @property
    def originalId(self):
        return self._originalId

    @originalId.setter
    def originalId(self, value):
        self._originalId = value

    @property
    def originalClass(self):
        if self._originalId is not None:
            if self.model.existNode(self._originalId):
                return self.model.getNode(self._originalId).nodeClass

    @property
    def formNodeType--- This code section failed: ---

 L. 341         0  LOAD_FAST                'self'
                2  LOAD_ATTR                originalId
                4  LOAD_CONST               None
                6  COMPARE_OP               is-not
                8  POP_JUMP_IF_FALSE   168  'to 168'

 L. 342        10  SETUP_EXCEPT        138  'to 138'

 L. 343        12  LOAD_FAST                'self'
               14  LOAD_ATTR                model
               16  LOAD_METHOD              getNode
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                originalId
               22  CALL_METHOD_1         1  '1 positional argument'
               24  STORE_FAST               'originalNode'

 L. 344        26  LOAD_FAST                'originalNode'
               28  LOAD_CONST               None
               30  COMPARE_OP               is-not
               32  POP_JUMP_IF_FALSE   134  'to 134'

 L. 345        34  LOAD_STR                 'choice('
               36  LOAD_FAST                'originalNode'
               38  LOAD_ATTR                definition
               40  COMPARE_OP               in
               42  POP_JUMP_IF_TRUE     54  'to 54'
               44  LOAD_STR                 'selector('
               46  LOAD_FAST                'originalNode'
               48  LOAD_ATTR                definition
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    60  'to 60'
             54_0  COME_FROM            42  '42'

 L. 346        54  LOAD_FAST                'self'
               56  LOAD_ATTR                FORMNODE_TYPE_COMBOBOX
               58  RETURN_VALUE     
             60_0  COME_FROM            52  '52'

 L. 347        60  LOAD_GLOBAL              str
               62  LOAD_FAST                'originalNode'
               64  LOAD_ATTR                result
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  LOAD_METHOD              isnumeric
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  POP_JUMP_IF_TRUE    110  'to 110'
               74  LOAD_GLOBAL              isinstance
               76  LOAD_FAST                'originalNode'
               78  LOAD_ATTR                result
               80  LOAD_GLOBAL              str
               82  CALL_FUNCTION_2       2  '2 positional arguments'
               84  POP_JUMP_IF_TRUE    110  'to 110'
               86  LOAD_GLOBAL              isinstance
               88  LOAD_FAST                'originalNode'
               90  LOAD_ATTR                result
               92  LOAD_GLOBAL              float
               94  CALL_FUNCTION_2       2  '2 positional arguments'
               96  POP_JUMP_IF_TRUE    110  'to 110'
               98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'originalNode'
              102  LOAD_ATTR                result
              104  LOAD_GLOBAL              int
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_JUMP_IF_FALSE   116  'to 116'
            110_0  COME_FROM            96  '96'
            110_1  COME_FROM            84  '84'
            110_2  COME_FROM            72  '72'

 L. 348       110  LOAD_FAST                'self'
              112  LOAD_ATTR                FORMNODE_TYPE_SCALAR
              114  RETURN_VALUE     
            116_0  COME_FROM           108  '108'

 L. 349       116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'originalNode'
              120  LOAD_ATTR                result
              122  LOAD_GLOBAL              bool
              124  CALL_FUNCTION_2       2  '2 positional arguments'
              126  POP_JUMP_IF_FALSE   134  'to 134'

 L. 350       128  LOAD_FAST                'self'
              130  LOAD_ATTR                FORMNODE_TYPE_CHECKBOX
              132  RETURN_VALUE     
            134_0  COME_FROM           126  '126'
            134_1  COME_FROM            32  '32'
              134  POP_BLOCK        
              136  JUMP_FORWARD        168  'to 168'
            138_0  COME_FROM_EXCEPT     10  '10'

 L. 352       138  DUP_TOP          
              140  LOAD_GLOBAL              RuntimeError
              142  LOAD_GLOBAL              TypeError
              144  LOAD_GLOBAL              NameError
              146  LOAD_GLOBAL              ValueError
              148  LOAD_GLOBAL              SyntaxError
              150  BUILD_TUPLE_5         5 
              152  COMPARE_OP               exception-match
              154  POP_JUMP_IF_FALSE   166  'to 166'
              156  POP_TOP          
              158  POP_TOP          
              160  POP_TOP          

 L. 353       162  POP_EXCEPT       
              164  JUMP_FORWARD        168  'to 168'
            166_0  COME_FROM           154  '154'
              166  END_FINALLY      
            168_0  COME_FROM           164  '164'
            168_1  COME_FROM           136  '136'
            168_2  COME_FROM             8  '8'

 L. 355       168  LOAD_FAST                'self'
              170  LOAD_ATTR                FORMNODE_TYPE_BUTTON
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 134

    @property
    def formNodeValue(self):
        if self.formNodeType == self.FORMNODE_TYPE_SCALAR or self.formNodeType == self.FORMNODE_TYPE_CHECKBOX or self.formNodeType == self.FORMNODE_TYPE_COMBOBOX:
            try:
                res = self.model.getNode(self.originalId).result
                if isinstance(res, Selector):
                    if 'numpy.' in str(type(res.value)):
                        return res.value.item()
                    return res.value
                else:
                    return res
            except Exception as e:
                try:
                    self.errorInDef = True
                finally:
                    e = None
                    del e

    @property
    def formNodeExtraValue(self):
        if self.formNodeType == self.FORMNODE_TYPE_SCALAR or self.formNodeType == self.FORMNODE_TYPE_CHECKBOX:
            try:
                if isinstance(self.result, str):
                    return f'"{self.result}"'
                return self.result
            except (RuntimeError, TypeError, NameError, ValueError, SyntaxError):
                pass

        else:
            if self.formNodeType == self.FORMNODE_TYPE_COMBOBOX:
                originalNode = self.model.getNode(self.originalId)
                return originalNode.definition

    @property
    def hierarchy_parents(self):
        return self._hierarchy_parents

    @property
    def hierarchy_maps(self):
        return self._hierarchy_maps

    @property
    def isin(self):
        return self.moduleId

    def preDelete(self):
        self.invalidate()
        self.ioEngine.updateOnDeleteNode()

    def silentInvalidate(self):
        self._isCalc = False
        self.profileParent = None
        self._result = None
        self._resultMemory = 0

    def invalidate(self, fromCircularNode=False):
        """Invalidate node result"""
        self._isCalc = False
        self.profileParent = None
        self._result = None
        self._resultMemory = 0
        if self.isCircular():
            if not fromCircularNode:
                circularNodes = self.getSortedCyclicDependencies()
                for node in circularNodes:
                    if node != self.identifier and self._model.existNode(node):
                        self._model.getNode(node).invalidate(fromCircularNode=True)

        self.invalidateOutputs()

    def invalidateOutputs(self):
        """Invalidate outputs of this node"""
        isCircular = self.isCircular()
        for node in self.ioEngine.outputs:
            if node is not None:
                if self._model.existNode(node):
                    if isCircular:
                        if self._model.getNode(node).isCircular():
                            if self.identifier in self._model.getNode(node).getSortedCyclicDependencies():
                                continue
                if self._model.getNode(node).isCalc:
                    self._model.getNode(node).invalidate()

    def generateIO(self):
        """Generate inputs and outputs"""
        if self.nodeClass not in ('alias', 'formnode'):
            tmpCode = None
            try:
                tmpCode = self.compileDef(self._definition)
            except SyntaxError:
                aa = 1

            if tmpCode is not None:
                nameList = self.parseNames(tmpCode)
                finalList = []
                for item in nameList:
                    if item and self.model.existNode(item):
                        rxText = '[^!.a-zA-Z_]\\b(###)\\b(?!={1}(?!={1}))'.replace('###', item)
                        rx = re.compile(rxText)
                        if len(re.findall(rx, self.definition)) > 0:
                            finalList.append(item)

                self.ioEngine.updateInputs(finalList)

    def compileDef(self, definition):
        """Compile definition"""
        try:
            self.errorInDef = False
            tmpCode = compile(str(definition), '<string>', 'exec')
            return tmpCode
        except SyntaxError:
            self.errorInDef = True

    def _getCalcNode(self, node):
        lazy_start_time = dt.datetime.now()
        try:
            return self._model.getNode(node).result
        finally:
            lazy_end_time = dt.datetime.now()
            if self.identifier != node:
                self.lastLazyTime = self.lastLazyTime + (lazy_end_time - lazy_start_time).total_seconds()

    def calculate(self, extraParams=None):
        """Calculate result of the node"""
        if not self.isCalc or self.nodeClass == 'button' or self.nodeClass == 'formnode':
            nodeIsCircular = self.isCircular()
            if not self._bypassCircularEvaluator:
                if nodeIsCircular:
                    circularNodes = self.getSortedCyclicDependencies()
                    if self.dynamicEvaluator is None:
                        self.dynamicEvaluator = FactoryDynamic.createInstance(circularNodes, self)
                    params = self.dynamicEvaluator.generateCircularParameters(self, circularNodes)
                    if params['dynamicIndex'] is None:
                        raise ValueError('Cyclic dependency detected between nodes: ' + ','.join(circularNodes) + ".\nPlease use the 'dynamic' function")
                    self.dynamicEvaluator.circularEval(self, params)
            else:
                from_circular_evaluator = self._bypassCircularEvaluator
                self.sendStartCalcNode(from_circular_evaluator)
                self.model.currentProcessingNode(self.identifier)
                self._bypassCircularEvaluator = False
                startTime = dt.datetime.now()
                finalDef = str(self._definition)
                self.lastLazyTime = 0
                if nodeIsCircular:
                    finalDef = BaseDynamic.clearAllCircularDependency(finalDef)
                tmpCode = self.compileDef(finalDef)
                if tmpCode is not None:
                    names = self.parseNames(tmpCode)
                    rx = '(\'[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*\'|\\"[^\\"\\\\]*(?:\\\\.[^\\"\\\\]*)*\\")|\\b{0}\\b'
                    for node in names:
                        if self._model.existNode(self._model.clearId(node)):
                            finalDef = re.sub(rx.format(node), lambda m:                             if m.group(1):
m.group(1) # Avoid dead code:                             if m.endpos > m.regs[0][1] + 5:
                                if m.string[m.regs[0][1]:m.regs[0][1] + 5] == '.node' or m.string[m.regs[0][1]:m.regs[0][1] + 8] == '.timeit(':
"getNode('" + node + "')" # Avoid dead code:                             if m.string[m.regs[0][0] - 1:m.regs[0][0] + len(node)] == '.' + node:
node # Avoid dead code: "getCalcNode('" + node + "')", finalDef, 0, re.IGNORECASE)

                localRes = {'getNode':self._model.getNode, 
                 'getCalcNode':self._getCalcNode, 
                 'cp':Helpers(self)}
                if extraParams is not None:
                    for keyParam in extraParams:
                        localRes[keyParam] = extraParams[keyParam]

                if self.identifier == 'imports':
                    if ', cubepy,' in finalDef:
                        finalDef = finalDef.replace(', cubepy,', ', pyplan_core.cubepy as cubepy,')
                    else:
                        customImports = self.model.getCustomImports()
                        if customImports:
                            for keyParam in customImports:
                                localRes[keyParam] = customImports[keyParam]

                        try:
                            memoryIO = io.StringIO()
                            try:
                                with redirect_stdout(memoryIO):
                                    exec(compile(finalDef, '<string>', 'exec'), localRes)
                            except Exception as ex:
                                try:
                                    if '_io.StringIO' in str(ex):
                                        exec(compile(finalDef, '<string>', 'exec'), localRes)
                                    else:
                                        raise ex
                                finally:
                                    ex = None
                                    del ex

                            self.lastEvaluationConsole = memoryIO.getvalue()
                            memoryIO = None
                            if self.nodeClass not in ('button', 'module', 'text'):
                                if 'this' in localRes:
                                    self._result = localRes['this']
                                    self._resultMemory = Helpers.getResultSize(self._result)
                                else:
                                    if 'result' in localRes:
                                        self._result = localRes['result']
                                        self._resultMemory = Helpers.getResultSize(self._result)
                                    else:
                                        self._result = None
                                        if self.lastEvaluationConsole != '':
                                            self._result = str(self.lastEvaluationConsole)
                                        else:
                                            raise ValueError("The result was not found. Did you forget to include the text 'result =' ?")
                            self._isCalc = self.nodeClass != 'button'
                            self.postCalculate()
                            endTime = dt.datetime.now()
                            self.lastEvaluationTime = (endTime - startTime).total_seconds() - self.lastLazyTime
                            if self.lastEvaluationTime < 0:
                                self.lastEvaluationTime = 0
                            self.evaluationVersion = self.model.evaluationVersion
                        finally:
                            localRes['cp'].release()
                            localRes = None
                            self.sendEndCalcNode(from_circular_evaluator)

                else:
                    self._bypassCircularEvaluator = False

    def postCalculate(self):
        evaluator = Evaluator.createInstance(self._result)
        evaluator.postCalculate(self, self._result)

    def parseNames(self, compiledCode):
        """Parse names used in node definition"""
        res = []
        if compiledCode is not None:
            res = compiledCode.co_names
            for co in compiledCode.co_consts:
                if co is not None and isinstance(co, CodeType):
                    res += co.co_names

        return res

    def updateDefinitionForChangeId(self, oldId, newId):
        """ Search and replace on this node definition the oldId for the newId
        """
        rx = re.compile('((?<!\\w)(?<!\\d)(?<!\\.)' + re.escape(oldId) + '(?!\\d)(?!\\w))(?=(?:[^"]|["][^"]*["])*$)')
        newDef = re.sub(rx, newId, self.definition)
        self.definition = newDef

    def isCircular(self):
        """ Checks if the node is part of a cycle
        """
        _id = self.identifier if self.originalId is None else self.originalId
        _inputNodes = [_id]
        nn = 0
        while nn < len(_inputNodes):
            _node = _inputNodes[nn]
            if self.model.existNode(_node):
                for _inputId in self.model.getNode(_node).ioEngine.inputs:
                    if _inputId == _id:
                        return True
                        if _inputId not in _inputNodes:
                            _inputNodes.append(_inputId)

            nn += 1

        return False

    def getFullInputs(self):
        """
        Return list of all node inputs and inputs of inputs
        """
        res = [
         self.identifier if self.originalId is None else self.originalId]
        nn = 0
        while nn < len(res):
            _node = res[nn]
            if self.model.existNode(_node):
                if self.model.getNode(_node).ioEngine.inputs:
                    for _inputId in self.model.getNode(_node).ioEngine.inputs:
                        input_node = self.model.getNode(_inputId)
                        if _inputId not in res:
                            res.append(_inputId)

            nn += 1

        return res

    def getSortedCyclicDependencies(self):
        """
        Return list of nodes in circular dependencyes, sortered by execution order
        """
        res = []
        if self.isCircular():
            res = [
             self.identifier if self.originalId is None else self.originalId]
            nn = 0
            while nn < len(res):
                _node = res[nn]
                for _inputId in self.model.getNode(_node).ioEngine.inputs:
                    input_node = self.model.getNode(_inputId)
                    if _inputId not in res and input_node.isCircular() and _node in input_node.getFullInputs():
                        res.append(_inputId)

                nn += 1

        return res

    def profileNode(self, evaluated, response, evaluationVersion, profileParentId):
        """Perform node profile"""
        if evaluated is not None:
            if self.identifier in evaluated:
                return response
            evaluated.append(self.identifier)
            if self.evaluationVersion == evaluationVersion:
                if self.profileParent is None:
                    self.profileParent = profileParentId
                auxVal = ({'nodeId':self.identifier, 
                  'title':self.identifier if self.model.getNode(self.identifier).title is None else self.model.getNode(self.identifier).title,  'moduleId':self.model.getNode(self.identifier).moduleId, 
                  'evaluationTime':self.model.getNode(self.identifier).lastEvaluationTime,  'usedMemory':self.model.getNode(self.identifier).usedMemory,  'calcTime':0.0},)
                response.extend(auxVal)
            if response is not None:
                for nodeInputId in self.inputs:
                    if nodeInputId not in evaluated:
                        response = self.model.getNode(nodeInputId).profileNode(evaluated, response, evaluationVersion, self.identifier)

        return response

    def sanitizeDefinition(self, value):
        """
        Sanitize from current front (Ade to py)
        """
        if str(value).isnumeric():
            value = 'result = ' + str(value)
        return value

    def getDefaultDefinitionByClass(self, nodeClass):
        """Return default definition by node class"""
        if nodeClass == 'module':
            return ''
        if nodeClass == 'index':
            return "result = cp.index(['Item 1', 'Item 2', 'Item 3'])"
        if nodeClass == 'button':
            return ''
        return 'result = 0'

    def getDefaultNodeinfoByClass(self, nodeClass):
        """
            Default nodeinfo by class. 
            Positions are:
                showInputs = 0
                showOutputs = 1
                showLabel = 2
                showBorder = 3
                fill = 4
                useNodeFont = 5
        """
        if nodeClass == 'text':
            return NodeInfo(0, 0, 1, 0, 0, 0)
        if nodeClass == 'alias':
            return NodeInfo(0, 0, 1, 1, 1, 0)
        if nodeClass == 'index':
            return NodeInfo(0, 0, 1, 1, 1, 0)
        if nodeClass == 'function':
            return NodeInfo(0, 0, 1, 1, 1, 0)
        if nodeClass == 'button':
            return NodeInfo(0, 0, 1, 1, 1, 0)
        return NodeInfo(1, 1, 1, 1, 1, 0)

    def timeit(self, repeat=1):
        """ Get stats after evaluate "repeat" times this node
        """
        import timeit

        def _testNode_():
            self.invalidate()
            self.node.result

        _locals_ = {'_testNode_': _testNode_}
        _res = timeit.repeat('_testNode_() ', repeat=repeat, number=1,
          globals=_locals_)
        return str({'average':float(str(round(np.mean(_res), 3))), 
         'best':float(str(round(np.min(_res), 3))), 
         'max':float(str(round(np.max(_res), 3)))})

    def set_hierarchy(self, parents, maps):
        self._hierarchy_parents = parents
        self._hierarchy_maps = maps

    def sendStartCalcNode(self, fromCircularEvaluator=False, fromDynamic=False):
        if self.model.debugMode:
            if self.identifier not in ('__evalnode__', 'dynamic'):
                if not fromCircularEvaluator:
                    if self._model.ws:
                        self._model.ws.sendDebugInfo((self.identifier),
                          (self.title if self.title else ''), 'startCalc', fromDynamic=fromDynamic)

    def sendEndCalcNode(self, fromCircularEvaluator=False, fromDynamic=False):
        if self.model.debugMode:
            if self.identifier not in ('__evalnode__', 'dynamic'):
                if not fromCircularEvaluator:
                    if self._model.ws:
                        resources = None
                        try:
                            resources = self.model.getSystemResources(onlyMemory=True)
                        except:
                            resources = {'usedMemory':0, 
                             'totalMemory':0}

                        self._model.ws.sendDebugInfo((self.identifier),
                          (self.title if self.title else ''), 'endCalc', (self.lastEvaluationTime), (resources['usedMemory']), (resources['totalMemory']), fromDynamic=fromDynamic)

    def bypassCircularEvaluator(self):
        """Mark node for bypass circular evaluator"""
        self._bypassCircularEvaluator = True
        return self

    @staticmethod
    def getDefaultColor(nodeClass):
        dic = {'variable':'#4CBCFF', 
         'button':'#a6a6a6', 
         'decision':'#4cffa6', 
         'constant':'#ff794c', 
         'module':'#4c83ff', 
         'function':'#cc99ff', 
         'chance':'#49E4F7', 
         'determ':'#076CBC', 
         'objective':'#ff4c97', 
         'index':'#9999ff', 
         'library':'#076CBC', 
         'form':'#076CBC', 
         'text':'#FEFEFE', 
         'picture':'#FEFEFE', 
         'formnode':'#076CBC', 
         'constraint':'#f2e340'}
        if str(nodeClass).lower() in dic:
            return dic[str(nodeClass).lower()]
        return '#6699FF'