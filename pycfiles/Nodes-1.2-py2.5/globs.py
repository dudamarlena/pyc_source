# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/nodes/globs.py
# Compiled at: 2009-10-19 11:25:39
"""Globs, or syntactic sugar."""
from core import Synaps, ones
from stacker.connect import connect as sconnect
from stacker.types import Type
import random, twist

def typconnect(nod1, nod2, type=None, w1=1.0, w2=1.0):
    type = type or Type('')
    (ind1, ind2) = sconnect(nod1, nod2, type)
    return connect(nod1, nod2, ind1, ind2, w1, w2)


def connect(nod1, nod2, ind1=-1, ind2=-1, w1=1.0, w2=1.0):
    """Connects two Nodes."""
    synaps = Synaps()
    synaps.bind(nod1, ind1, nod2, ind2)
    nod1.output_weights[ind1] = w1
    nod2.input_weights[ind2] = w2
    return synaps


class Glob:

    def __init__(self, nodes=(), shape=(), inputs=(), outputs=(), heart=None, name='', cache=False):
        self.nodes = {}
        self.sysname = name or 'Glob:' + repr(id(self))
        self.doubly = True
        if cache:
            self.cache = {}
        else:
            self.cache = None
        if nodes:
            self.make_shape(nodes, shape)
            self.inputs = [ self.nodes[x] for x in inputs ]
            self.outputs = [ self.nodes[x] for x in outputs ]
            if heart:
                self.heart = self.nodes[heart]
            else:
                self.heart = None
        return

    def _new(self, nodclass, iN, oN, name):
        return nodclass([None] * iN, [None] * oN, ones(iN), ones(oN), sysname=self.sysname + '.' + name)

    def make_shape(self, nodes, edges):
        nodict = {}
        for (name, class_) in nodes:
            (iN, oN) = class_.__shape__
            if iN and iN[(-1)] is None:
                iN = iN[:-1]
            if oN and oN[(-1)] is None:
                oN = oN[:-1]
            nodict[name] = self._new(class_, len(iN), len(oN), name)

        for edge in edges:
            (from_, to) = edge[:2]
            from_ = nodict[from_]
            to = nodict[to]
            edge = (from_, to) + edge[2:]
            if len(edge) == 2 or not isinstance(edge[2], int):
                synaps = typconnect(*edge)
            else:
                synaps = connect(*edge)
            if self.cache is not None:
                if len(edge) == 2 or not isinstance(edge[2], int):
                    key = edge[:3]
                else:
                    key = edge[:4]
                self.cache[key] = synaps

        self.nodes.update(nodict)
        return

    def add(self, name, nodclass, input_edges, output_edges):
        iN = len(input_edges)
        oN = len(output_edges)
        nod = self._new(nodclass, iN, oN, name)
        for edge in input_edges:
            thenod = self.nodes[edge[0]]
            edge = [thenod, nod] + edge[1:]
            connect(*edge)

        for edge in output_edges:
            thenod = self.nodes[edge[0]]
            edge = [nod, thenod] + edge[1:]
            connect(*edge)

        return nod

    def addInput(self, name, nodclass, input_edges, output_edges):
        nod = self.add(name, nodclass, input_edges, output_edges)
        self.inputs.append(nod)
        return nod

    def addOutput(self, name, nodclass, input_edges, output_edges):
        nod = self.add(name, nodclass, input_edges, output_edges)
        self.outputs.append(nod)

    def calculate(self, values=None, dfr=None, callback=None, *pargs):
        self.reset()
        if values:
            self._put(values)
        dfr = dfr or self.satisfaction()
        initcalls = [ x.calc for x in self.inputs ]
        for call in initcalls:
            twist.asyncall(call)

        dfr.addCallback(twist.nodummy(self._get))
        if callback is not None:
            dfr.addCallback(callback, *pargs)
        return dfr

    def satisfaction(self):
        satisfaction = twist.deferred.Deferred()
        satisfaction.list = self.outputs[:]

        def _oneMore(nod_self):
            if nod_self in satisfaction.list:
                satisfaction.list.remove(nod_self)
                if not satisfaction.list:
                    for callID in twist.reactor.getDelayedCalls():
                        callID.cancel()

                    satisfaction.callback(self.outputs[:])

        def _ifError(the_fail):
            satisfaction.errback(the_fail)

        for nod in satisfaction.list:
            nod.deferred.addCallbacks(_oneMore, _ifError)

        return satisfaction

    def _put(self, values):
        if values is None:
            return
        for (nod, val) in zip(self.inputs, values):
            print nod, val
            nod.set(val)

        return

    def _get(self):
        return [ nod.get() for nod in self.outputs ]

    def compute(self, values=None, doubly=False):
        """Layered calculating algorhytm."""
        self._put(values)
        for nod in self.inputs:
            nod.compute()

        stage = 0
        nodes = self.nodes.values()
        syns = set()
        for nod in nodes:
            syns |= set(nod.inputs + nod.outputs)

        selfconnected = set((syn.innode.layer for syn in syns if syn.direction == 0))
        backconnected = set((syn.innode.layer for syn in syns if syn.direction < 0))
        maxstage = len(selfconnected) + len(backconnected) - len(selfconnected & backconnected) / 2
        if maxstage < 2:
            return self.calculate()
        last = None
        while 1:
            for nod in nodes:
                nod.reset()

            (i, o) = self._randselect()
            o.compute()
            if doubly:
                i.compute()
            res = self._get()
            if res == last:
                break
            last = res
            stage += 1
            if stage > maxstage + 1:
                break

        return res

    def print_self(self):
        print 'Glob', self.sysname
        print '\nNet state:'
        for nam in self.nodes:
            print '%4s: %s %s' % (nam, self.nodes[nam].ivalues,
             self.nodes[nam].ovalues)

        print '\nWeights:'
        for nam in self.nodes:
            print '%4s: %s %s' % (nam, self.nodes[nam].input_weights,
             self.nodes[nam].output_weights)
            print

    def teach(self, result):
        if self.heart is not None:
            self.heart.teach_feed(result)
        else:
            random.choice(self.nodes.values()).teach_feed(result)
        return

    def reset(self):
        for nod in self.nodes.values():
            nod.reset()