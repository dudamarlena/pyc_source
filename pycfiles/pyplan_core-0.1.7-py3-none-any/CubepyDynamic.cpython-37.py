# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/dynamics/CubepyDynamic.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 10263 bytes
import pyplan_core.classes.dynamics.BaseDynamic as BaseDynamic
import pyplan_core.cubepy.Helpers as Helpers
import numpy as np
import pyplan_core.cubepy as cubepy
import datetime as dt, re

class CubepyDynamic(BaseDynamic):

    def circularEval(self, node, params):
        """
        Used for execute nodes with circular reference (dynamic)
        """
        dynamicVars = params['dynamicVars']
        dynamicIndex = params['dynamicIndex']
        nodesInCyclic = params['nodesInCyclic']
        initialValues = params['initialValues']
        shift = params['shift']
        startTime = dt.datetime.now()
        evaluate = node.model.evaluate
        cyclicNodes = []
        try:
            try:
                node.model.inCyclicEvaluate = True
                for nodeId in nodesInCyclic:
                    _nodeObj = node.model.getNode(nodeId)
                    cyclicNodes.append({'node':_nodeObj, 
                     'initialize':self.generateInitDef(node, _nodeObj.bypassCircularEvaluator().result, dynamicIndex), 
                     'loopDefinition':self.generateLoopDef(node, _nodeObj.definition, nodesInCyclic)})

            except Exception as e:
                try:
                    raise e
                finally:
                    e = None
                    del e

        finally:
            node.model.inCyclicEvaluate = False

        cyclicDic = {}
        for _node in cyclicNodes:
            _id = _node['node'].identifier
            cyclicDic[_id] = evaluate(_node['initialize'])
            if initialValues is not None and _id in initialValues:
                cyclicDic[_id] = cyclicDic[_id] + evaluate(initialValues[_id])

        for _var in dynamicVars:
            _key = '__' + _var + '_t'
            cyclicDic[_key] = cyclicDic[_var].sum(dynamicIndex) * 0

        cyclicParams = None
        theRange = range(0, len(dynamicIndex))
        initialCount = shift * -1
        reverseMode = False
        if shift > 0:
            theRange = range(len(dynamicIndex) - 1, -1, -1)
            initialCount = len(dynamicIndex) - 1 - shift
            reverseMode = True
        for nn in theRange:
            item = dynamicIndex[nn]
            cyclicParams = {'item':item, 
             'cyclicDic':cyclicDic}
            _CubepyDynamic__initialValues = None
            for _node in cyclicNodes:
                _id = _node['node'].identifier
                node.model.currentProcessingNode(_id)
                cyclicParams['cyclicDic'] = cyclicDic
                if _id in initialValues:
                    if not nn < initialCount or reverseMode:
                        if not nn > initialCount or reverseMode:
                            _CubepyDynamic__resultNode = evaluate(_node['loopDefinition'], cyclicParams)
                            _CubepyDynamic__initialValues = evaluate(initialValues[_id])
                            if isinstance(_CubepyDynamic__initialValues, cubepy.Cube):
                                _CubepyDynamic__finalNode = _CubepyDynamic__initialValues.tryFilter(item).squeeze() + _CubepyDynamic__resultNode.tryFilter(item).squeeze()
                            else:
                                _CubepyDynamic__finalNode = _CubepyDynamic__resultNode.tryFilter(item).squeeze() + _CubepyDynamic__initialValues
                            cyclicDic[_id].set_data(item, _CubepyDynamic__finalNode.values)
                else:
                    _CubepyDynamic__resultNode = evaluate(_node['loopDefinition'], cyclicParams)
                    cyclicDic[_id].set_data(item, _CubepyDynamic__resultNode.tryFilter(item).squeeze().values)

            if not reverseMode:
                if nn + 1 < initialCount or reverseMode:
                    if nn - 1 > initialCount:
                        continue
                else:
                    for _var in dynamicVars:
                        _key = '__' + _var + '_t'
                        if reverseMode:
                            cyclicDic[_key] = cyclicDic[_var].tryFilter(dynamicIndex[(nn + shift - 1)]).squeeze()
                        else:
                            cyclicDic[_key] = cyclicDic[_var].tryFilter(dynamicIndex[(nn - initialCount + 1)]).squeeze()

        endTime = dt.datetime.now()
        for _node in cyclicNodes:
            _id = _node['node'].identifier
            _node['node']._result = cyclicDic[_id]
            _node['node']._CubepyDynamic__resultMemory = Helpers.getResultSize(_node['node']._result)
            _node['node']._isCalc = True
            _node['node'].lastEvaluationTime = (endTime - startTime).total_seconds()
            _node['node'].evaluationVersion = node.model.evaluationVersion
            _node['node']._bypassCircularEvaluator = False

        evaluate = None
        model = None
        cyclicDic = None
        cyclicParams = None
        return 'ok'

    def generateLoopDef(self, node, nodeDefinition, cyclicVariables):
        """
        Return definition used for circular evaluator
        """
        _def = self.clearCircularDependency(nodeDefinition, "cyclicDic['__##node##_t']")
        finalDef = _def
        tmpCode = compile(_def, '<string>', 'exec')
        names = node.parseNames(tmpCode)
        rx = '(\'[^\'\\\\]*(?:\\\\.[^\'\\\\]*)*\'|\\"[^\\"\\\\]*(?:\\\\.[^\\"\\\\]*)*\\")|\\b{0}\\b'
        for nodeId in names:
            if node._model.existNode(node._model.clearId(nodeId)) and nodeId in cyclicVariables:
                finalDef = re.sub(rx.format(nodeId), lambda m:                 if m.group(1):
m.group(1) # Avoid dead code:                 if m.endpos > m.regs[0][1] + 5:
                    if m.string[m.regs[0][1]:m.regs[0][1] + 5] == '.node' or m.string[m.regs[0][1]:m.regs[0][1] + 8] == '.timeit(':
"cyclicDic['" + nodeId + "']" # Avoid dead code:                 if m.string[m.regs[0][0] - 1:m.regs[0][0] + len(nodeId)] == '.' + nodeId:
nodeId # Avoid dead code: "cyclicDic['" + nodeId + "'].tryFilter(item).squeeze() ", finalDef, 0, re.IGNORECASE)

        return finalDef

    def generateInitDef(self, node, nodeCube, dynamicIndex):
        """
        Return definition used for initialice vars in circular evaluator
        """
        if isinstance(nodeCube, cubepy.Cube):
            _list = nodeCube.dims[:]
            if dynamicIndex.name not in _list:
                _list.append(dynamicIndex.name)
            _dims = ','.join(_list)
            _def = 'result = cp.cube([' + _dims + '])'
            return _def
        return 'result = cp.cube([' + dynamicIndex.name + '])'

    def generateCircularParameters(self, node, nodeList):
        """
        Generate paremters for call to circularEval
        """
        dynamicVars = []
        dynamicIndex = None
        nodesInCyclic = []
        initialValues = {}
        shift = -1
        for _nodeId in nodeList:
            if node.model.existNode(_nodeId):
                _def = node.model.getNode(_nodeId).definition
                if 'cp.dynamic' in _def:
                    _startPos = _def.find('cp.dynamic(') + 11
                    _endPos = _def.find(')', _startPos)
                    _arr = str(_def[_startPos:_endPos]).split(',')
                    _vart_1 = _arr[0].strip()
                    if _vart_1 not in dynamicVars:
                        dynamicVars.append(_vart_1)
                    dynamicIndex = node.model.getNode(_arr[1].strip()).result
                    shift = int(_arr[2])
                    if len(_arr) > 3:
                        initialValues[_nodeId] = 'result = ' + _arr[3].strip()

        _graph = {}
        for _nodeId in nodeList:
            if node.model.existNode(_nodeId):
                _graph[_nodeId] = []
                for _outputId in node.model.getNode(_nodeId).ioEngine.outputs:
                    if _outputId in nodeList and 'cp.dynamic(' + _nodeId + ',' not in str(node.model.getNode(_outputId).definition).replace(' ', ''):
                        _graph[_nodeId].append(_outputId)

        nodesInCyclic = Helpers.dfs_topsort(_graph)
        return {'dynamicVars':dynamicVars, 
         'dynamicIndex':dynamicIndex, 
         'nodesInCyclic':nodesInCyclic, 
         'initialValues':initialValues, 
         'shift':shift}

    def clearCircularDependency(self, stringDef, replaceWith='0'):
        """ Replaces cp.dynamic(x,y,z) for the desired replaceWith param
        """
        response = stringDef
        initialIndex = -1
        startIndex = -1
        finalIndex = -1
        toReplace = ''
        initialIndex = stringDef.find('cp.dynamic(')
        if initialIndex != -1:
            startIndex = initialIndex
            initialIndex = initialIndex + len('cp.dynamic(')
            if len(stringDef) > initialIndex:
                finalIndex = stringDef[initialIndex + 1:].find(')')
        elif initialIndex != -1 and finalIndex != -1:
            toReplace = stringDef[startIndex:initialIndex + finalIndex + 2]
            if 'cyclicDic' in replaceWith:
                nodeInT1 = toReplace.split(',')[0]
                nodeInT1 = nodeInT1[nodeInT1.find('(') + 1:]
                replaceWith = replaceWith.replace('##node##', nodeInT1.strip())
            response = stringDef.replace(toReplace, replaceWith)
        return response