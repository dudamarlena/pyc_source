# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fabian/devs/novix/python/pyplan-core/pyplan_core/classes/dynamics/PureXArrayDynamic.py
# Compiled at: 2020-04-29 16:08:41
# Size of source mod 2**32: 14354 bytes
import pyplan_core.classes.dynamics.BaseDynamic as BaseDynamic
import pyplan_core.cubepy.Helpers as Helpers
import numpy as np, re, xarray as xr, datetime as dt

class PureXArrayDynamic(BaseDynamic):

    def circularEval(self, node, params):
        """
        Used for execute nodes with circular reference (pp.dynamic)
        """
        dynamicVars = params['dynamicVars']
        dynamicIndex = params['dynamicIndex']
        nodesInCyclic = params['nodesInCyclic']
        initialValues = params['initialValues']
        shift = params['shift']
        evaluate = node.model.evaluate
        if node.model.debugMode:
            for circular_node_id in nodesInCyclic:
                circular_node = node.model.getNode(circular_node_id)
                if circular_node is not None:
                    circular_node.sendStartCalcNode(fromDynamic=True)

        cyclicNodes = []
        try:
            try:
                node.model.inCyclicEvaluate = True
                for nodeId in nodesInCyclic:
                    _nodeObj = node.model.getNode(nodeId)
                    cyclic_item = {'node':_nodeObj, 
                     'initialize':self.generateInitDef(node, _nodeObj.bypassCircularEvaluator().result, dynamicIndex), 
                     'calcTime':_nodeObj.lastEvaluationTime}
                    startTime = dt.datetime.now()
                    cyclic_item['loopDefinition'] = self.generateLoopDef(node, _nodeObj.definition, nodesInCyclic)
                    endTime = dt.datetime.now()
                    cyclic_item['calcTime'] += (endTime - startTime).total_seconds()
                    cyclicNodes.append(cyclic_item)

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
            evaluate_node_time = 0
            evaluate_initial_params_time = 0
            cyclicDic[_id], evaluate_node_time = evaluate((_node['initialize']),
              returnEvaluateTime=True)
            if initialValues is not None:
                if _id in initialValues:
                    initial_result, evaluate_initial_params_time = evaluate((initialValues[_id]),
                      returnEvaluateTime=True)
                    cyclicDic[_id] = cyclicDic[_id] + initial_result
            if cyclicDic[_id].dims[0] != dynamicIndex.name:
                list_dims = list(cyclicDic[_id].dims)
                list_dims.remove(dynamicIndex.name)
                new_tuple = (dynamicIndex.name,) + tuple(list_dims)
                cyclicDic[_id] = (cyclicDic[_id].transpose)(*new_tuple, **{'transpose_coords': True})
            _node['calcTime'] = _node['calcTime'] + evaluate_node_time + evaluate_initial_params_time

        for _var in dynamicVars:
            _key = '__' + _var + '_t'
            cyclicDic[_key] = cyclicDic[_var].sum(dynamicIndex.name) * 0

        cyclicParams = None
        theRange = range(0, len(dynamicIndex.values))
        initialCount = shift * -1
        reverseMode = False
        if shift > 0:
            theRange = range(len(dynamicIndex.values) - 1, -1, -1)
            initialCount = len(dynamicIndex.values) - 1 - shift
            reverseMode = True
        for nn in theRange:
            item = dynamicIndex.values[nn]
            cyclicParams = {'item':item, 
             'cyclicDic':cyclicDic, 
             'dynamicIndex':dynamicIndex, 
             'self':self}
            _PureXArrayDynamic__initialValues = None
            for _node in cyclicNodes:
                _id = _node['node'].identifier
                node.model.currentProcessingNode(_id)
                cyclicParams['cyclicDic'] = cyclicDic
                evaluate_node_time = 0
                evaluate_initial_params_time = 0
                start_extra_process_time = None
                if _id in initialValues:
                    if not nn < initialCount or reverseMode:
                        if not nn > initialCount or reverseMode:
                            _resultNode, evaluate_node_time = evaluate(_node['loopDefinition'], cyclicParams, True)
                            _initialValues, evaluate_initial_params_time = evaluate((initialValues[_id]),
                              returnEvaluateTime=True)
                            _finalNode = None
                            start_extra_process_time = dt.datetime.now()
                            if isinstance(_initialValues, xr.DataArray):
                                _finalNode = self._tryFilter(_resultNode, dynamicIndex, item) + self._tryFilter(_initialValues, dynamicIndex, item)
                            else:
                                _finalNode = self._tryFilter(_resultNode, dynamicIndex, item) + _initialValues
                            try:
                                cyclicDic[_id].loc[{dynamicIndex.name: slice(item, item)}] = _finalNode.values
                            except Exception as ex:
                                try:
                                    list_dims = list(cyclicDic[_id].dims)
                                    list_dims.remove(dynamicIndex.name)
                                    cyclicDic[_id].loc[{dynamicIndex.name: slice(item, item)}] = (_finalNode.transpose)(*list_dims, **{'transpose_coords': True}).values
                                finally:
                                    ex = None
                                    del ex

                        else:
                            _resultNode, evaluate_node_time = evaluate(_node['loopDefinition'], cyclicParams, True)
                            _finalNode = self._tryFilter(_resultNode, dynamicIndex, item)
                            start_extra_process_time = dt.datetime.now()
                            try:
                                cyclicDic[_id].loc[{dynamicIndex.name: slice(item, item)}] = _finalNode.values
                            except Exception as ex:
                                try:
                                    list_dims = list(cyclicDic[_id].dims)
                                    list_dims.remove(dynamicIndex.name)
                                    cyclicDic[_id].loc[{dynamicIndex.name: slice(item, item)}] = (_finalNode.transpose)(*list_dims, **{'transpose_coords': True}).values
                                finally:
                                    ex = None
                                    del ex

                            _node['calcTime'] += evaluate_node_time + evaluate_initial_params_time
                        if start_extra_process_time is not None:
                            end_extra_process_time = dt.datetime.now()
                            _node['calcTime'] += (end_extra_process_time - start_extra_process_time).total_seconds()

            if not reverseMode:
                if nn + 1 < initialCount or :
                    if nn - 1 > initialCount:
                        continue
                else:
                    for _var in dynamicVars:
                        _key = '__' + _var + '_t'
                        if reverseMode:
                            cyclicDic[_key] = self._tryFilter(cyclicDic[_var], dynamicIndex, dynamicIndex.values[(nn + shift - 1)])
                        else:
                            cyclicDic[_key] = self._tryFilter(cyclicDic[_var], dynamicIndex, dynamicIndex.values[(nn - initialCount + 1)])

        for _node in cyclicNodes:
            _id = _node['node'].identifier
            _node['node']._result = cyclicDic[_id]
            _node['node']._PureXArrayDynamic__resultMemory = Helpers.getResultSize(_node['node']._result)
            _node['node']._isCalc = True
            _node['node'].lastEvaluationTime = _node['calcTime']
            _node['node'].evaluationVersion = node.model.evaluationVersion

        if node.model.debugMode:
            for circular_node_id in nodesInCyclic:
                circular_node = node.model.getNode(circular_node_id)
                if circular_node is not None:
                    circular_node.sendEndCalcNode(fromDynamic=True)

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
nodeId # Avoid dead code: "self._tryFilter( cyclicDic['" + nodeId + "'],dynamicIndex,item) ", finalDef, 0, re.IGNORECASE)

        return finalDef

    def generateInitDef(self, node, nodeCube, dynamicIndex):
        """
        Return definition used for initialice vars in circular evaluator
        """
        if isinstance(nodeCube, xr.DataArray):
            _list = list(nodeCube.dims[:])
            if dynamicIndex.name not in _list:
                _list.append(dynamicIndex.name)
            _dims = ','.join(_list)
            _def = f"result = create_dataarray(0.,[{_dims}])"
            return _def
        return f"result = create_dataarray(0.,[{dynamicIndex.name}])"

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
                if 'dynamic(' in _def:
                    _startPos = _def.find('dynamic(') + 8
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
                    if _outputId in nodeList and 'dynamic(' + _nodeId + ',' not in str(node.model.getNode(_outputId).definition).replace(' ', ''):
                        _graph[_nodeId].append(_outputId)

        nodesInCyclic = Helpers.dfs_topsort(_graph)
        return {'dynamicVars':dynamicVars, 
         'dynamicIndex':dynamicIndex, 
         'nodesInCyclic':nodesInCyclic, 
         'initialValues':initialValues, 
         'shift':shift}

    def clearCircularDependency(self, stringDef, replaceWith='0'):
        """ Replaces pp.dynamic(x,y,z) for the desired replaceWith param
        """
        response = stringDef
        initialIndex = -1
        startIndex = -1
        finalIndex = -1
        toReplace = ''
        initialIndex = stringDef.find('dynamic(')
        if initialIndex != -1:
            startIndex = initialIndex
            initialIndex = initialIndex + len('dynamic(')
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

    def _tryFilter(self, array, dim, value):
        try:
            _dic = {dim.name: value}
            return array.sel(_dic, drop=True)
        except Exception as ex:
            try:
                return array
            finally:
                ex = None
                del ex