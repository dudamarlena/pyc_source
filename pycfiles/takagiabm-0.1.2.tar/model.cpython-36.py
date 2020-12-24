# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/hzy/程序/novalide/forgitcommit/NovalIDE/plugins/takagi/takagiabm/model.py
# Compiled at: 2020-04-18 09:27:50
# Size of source mod 2**32: 8760 bytes
from takagiabm.grid import Grid
from takagiabm.datacounter import DataCounter
from takagiabm.agent import GridAgent, BaseAgent
from takagiabm.activation import Activator
import time
from takagiabm import TakTimeCounter

class BaseModel:
    dataCounters = []

    def __init__(self):
        self.agentSet = set()
        self.currentStep = 0
        self.agentUpdateList = []
        self.activator = Activator(self)
        self.timeCounter = TakTimeCounter(self)

    def countAgentData(self):
        for counter in self.dataCounters:
            if 'agent' in counter.targets:
                counter.count(list(self.agentSet), self.currentStep)

    def startTiming(self, timerName):
        self.timeCounter.startTiming(timerName)

    def endTiming(self, timerName):
        self.timeCounter.endTiming(timerName, time.time())

    def addAgent(self, agent):
        if not isinstance(agent, BaseAgent):
            raise TypeError('添加的Agent类型应为Agent类型，你添加的是%s类型。' % type(agent))
        agent.model = self
        self.agentSet.add(agent)

    def removeAgent(self, agent):
        self.agentSet.remove(agent)

    def stepRoutine(func):
        """
        每一次step发生时都要发生一遍的事情,作为装饰器.
        """

        def wrapper(self, *args, **kwargs):
            self.currentStep += 1
            return func(self, *args, **kwargs)

        return wrapper

    @stepRoutine
    def step(self):
        pass


class GridModel(BaseModel):
    stepRoutine = BaseModel.stepRoutine
    width = 0
    height = 0
    lastStep = 0
    wrapPolicy = None
    agentActivationPolicy = 'random'
    cellActivationPolicy = 'random'
    agentActivationAction = None
    cellActivationAction = None

    def __init__(self):
        super().__init__()
        self.currentStep = 0
        self.grid = Grid(model=self, width=(self.width), height=(self.height))
        self.updateWrapAction()
        self.updateActivationAction()
        self.initAgents()

    def timeIt(self, func, *args, **kwargs):
        return (self.timeCounter.timeIt)(func, *args, **kwargs)

    def countCellData(self):
        cellList = list(self.grid.getAllCells())
        for counter in self.dataCounters:
            if 'cell' in counter.targets:
                counter.count(cellList, self.currentStep)

    def setProperties(self):
        pass

    def initAgents(self):
        pass

    def agentsUpdateProperties(self):
        """
        刷新setTraitLater生成的刷新队列。
        """
        for agent, propertyName, property in self.agentUpdateList:
            agent.properties[propertyName] = property

        self.agentUpdateList = []

    def addAgent(self, agent, randomPlace=False):
        """
        向网格中添加代理人对象.randomPlace调用时，将把agent随机放在某个点上。
        """
        if randomPlace == True:
            agent.pos[0] = np.random.randint(0, self.width)
            agent.pos[1] = np.random.randint(0, self.height)
        super().addAgent(agent)
        self.grid.placeAgent(agent)

    def removeAgent(self, agent):
        """
        移除代理人对象。
        """
        if agent in self.agentSet:
            self.agentSet.remove(agent)
            self.grid.removeAgent(agent)
            agent.removed = True

    def updateWrapAction(self) -> None:
        """
        设置回绕方式,有四种：vcylinder，hcylinder,box和torus。默认为torus.
        系统默认的结构是环面(torus)，即在水平和垂直方向边界都进行回绕(rewind)，
        形成闭合的有限无界空间，当agent超越一个边界时则会在对应另一边界上出现。
        box在两个方向都不回绕，因此上下左右均有边界，agent移动时无法超越边界。
        柱面只在一个方向回绕，垂直柱面的左右边界连接在一起，而水平柱面的上下边界连接在一起。
        以上内容摘自对netlogo的介绍，网址：http://blog.sina.com.cn/s/blog_66efa5fb0100hew6.html
        """
        wrapPolicy = self.wrapPolicy
        if wrapPolicy != None:
            self.grid.setWrapAction(wrapPolicy)
        else:
            self.grid.setWrapAction('torus')

    def updateActivationAction(self):
        d = {'random':self.activator.randomActivation,  'casual':self.activator.casualActivation,  'none':None}
        if self.agentActivationPolicy in d.keys():
            self.agentActivationAction = d[self.agentActivationPolicy]
        else:
            raise Exception('未知的代理人激活策略：%s.所有可用的激活策略为：%s' % (self.agentActivationPolicy, str(d.keys())))
        if self.cellActivationPolicy in d.keys():
            self.cellActivationAction = d[self.cellActivationPolicy]
        else:
            raise Exception('未知的单元格激活策略：%s.所有可用的激活策略为：%s' % (self.cellActivationPolicy, str(d.keys())))

    @stepRoutine
    def step(self):
        t0 = time.time()
        if self.cellActivationAction != None:
            l = list(self.grid.getAllCells())
            self.cellActivationAction(l)
        if self.agentActivationAction != None:
            self.agentActivationAction(list(self.agentSet))
        t1 = time.time()
        self.agentsUpdateProperties()
        self.timeCounter.flush()
        t2 = time.time()
        self.countAgentData()
        self.countCellData()
        t3 = time.time()
        print('模型单步执行时间：', t2 - t0, t2 - t1, t3 - t2)
        print('agentNum', len(list(self.agentSet)))


import numpy as np

class MatGridModel(GridModel):
    agentList = []
    stoDic = {'pos':np.zeros((10, 2)), 
     'speed':np.zeros((10, 2))}
    agentNum = 0
    stoSpace = 0

    def __init__(self):
        super().__init__()
        self.agentArrayLenIni = 10

    def extendStorageSpace(self):
        for k in self.stoDic.keys():
            if (k != 'pos') & (k != 'speed'):
                self.stoDic[k] = np.r_[(self.stoDic[k], np.zeros(self.agentNum))]
            else:
                self.stoDic[k] = np.r_[(self.stoDic[k], np.zeros((self.agentNum, 2)))]

        self.stoSpace = len(self.stoDic['pos'])

    def moveLastAgentTo(self, newid):
        self.agentList[newid] = self.agentList[(self.agentNum - 1)]
        self.moveAgentPropertyTo(self.agentNum - 1, newid)
        self.agentList[newid].id = newid

    def moveAgentPropertyTo(self, lastid, newid):
        for k in self.stoDic.keys():
            self.stoDic[k][newid] = self.stoDic[k][lastid]

    def addAgent(self, agent):
        if self.agentNum >= self.stoSpace * 0.9:
            self.extendStorageSpace()
        self.agentSet.add(agent)
        self.grid.placeAgent(agent)
        self.agentList.append(agent)
        self.agentNum = len(self.agentList)
        agent.id = self.agentNum - 1
        agent.model = self
        self.stoDic['pos'][agent.id] = agent.pos
        self.stoDic['speed'][agent.id] = agent.speed

    def removeAgent(self, agent):
        self.agentSet.remove(agent)
        id = agent.id
        self.grid.removeAgent(agent)
        self.moveLastAgentTo(id)
        self.agentList.pop()
        self.agentNum = len(self.agentList)

    def createArrStorage(self, name, var):
        if type(var) == type(1):
            mat = np.zeros((self.width, self.height), dtype=(np.int))
        else:
            if type(var) == type(1.0):
                mat = np.zeros((self.width, self.height), dtype=(np.float))
            else:
                if type(var) == type(True):
                    mat = np.zeros((self.width, self.height), dtype=(np.bool))
                else:
                    raise Exception('错误：矩阵存储不支持此数据类型、')
        self.stoDic[name] = mat


if __name__ == '__main__':
    MatGridModel.width = 3
    MatGridModel.height = 3
    model = MatGridModel()
    from takagiabm.agent import MatGridAgent
    for i in range(3):
        a = MatGridAgent(np.array([i, 2]))
        model.addAgent(a)

    print(model.agentSet)
    a = model.agentList[1]
    print(a.pos)
    a.move(np.array([0, -1]))
    print(a.pos)
    print(model.stoDic)