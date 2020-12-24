# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/hzy/程序/novalide/forgitcommit/NovalIDE/plugins/takagi/takagiabm/activation.py
# Compiled at: 2020-04-18 00:46:43
# Size of source mod 2**32: 3505 bytes
import random, time, numpy as np
from multiprocessing import Process, Queue
from takagiabm.agent import GridAgent
from multiprocessing.managers import BaseManager
import multiprocessing

class MyManager(BaseManager):
    pass


MyManager.register('GridAgent', GridAgent)
inQueue = Queue(50)

class Activator:

    def __init__(self, model):
        self.agentSet = model.agentSet

    def casualActivation(self, agentList):
        """
        随意地激活,不是随机的.意思是将所有元素简单的按照哈希表的顺序激活.
        """
        for agent in agentList:
            agent.step()

    def randomActivation(self, agentList: list, activatePortion=1) -> None:
        t0 = time.time()
        if (activatePortion < -1e-09) | (activatePortion > 1.000000001):
            raise Exception('Invalid activatePortion.激活比例须在[0,1]闭区间以内.')
        agentNum = len(agentList)
        agentNumToActivate = int(agentNum * activatePortion)
        agentIndexArray = np.arange(agentNumToActivate)
        np.random.shuffle(agentIndexArray)
        for index in agentIndexArray:
            if agentList[index].removed == False:
                agentList[index].step()

    def parallelActivation(self, agentList, activatePortion=1):
        t0 = time.time()
        if (activatePortion < -1e-09) | (activatePortion > 1.000000001):
            raise Exception('Invalid activatePortion.激活比例须在[0,1]闭区间以内.')
        agentNum = len(agentList)
        agentNumToActivate = int(agentNum * activatePortion)
        agentIndexArray = np.arange(agentNumToActivate)
        t1 = time.time()
        np.random.shuffle(agentIndexArray)
        t2 = time.time()
        from pathos.pools import ProcessPool
        self.pool = ProcessPool(nodes=1)
        try:
            print(id(agentList[0]))
        except:
            pass

        self.pool.map(process, agentList)
        t3 = time.time()
        print('tttfggggg', time.time() - t0)


class ParallelProcessor:

    def __init__(self):
        self.processList = []
        for i in range(1):
            self.processList.append(Process(target=process, args=lock))
            self.processList[i].daemon = True
            self.processList[i].start()


def process(a):
    print('id', id(a))
    print(a.properties['color'])
    a.properties['color'] = '#aaaaaa'
    print(2, a.properties['color'])
    a.step()


# global inQueue ## Warning: Unused global