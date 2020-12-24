# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/admin/introspection/impl/memory_status.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Oct 11, 2011

@package: introspection request
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides a Node on the resource manager with an invoker that presents the memory status.
"""
from ally.api.config import GET
from ally.api.type import Input, Integer, typeFor, String, Non
from ally.container import wire
from ally.container.ioc import injected
from ally.core.impl.invoker import InvokerFunction
from ally.core.impl.node import NodePath
from ally.core.spec.resources import Node
from ally.support.util_sys import fullyQName
from collections import OrderedDict
from inspect import isclass
import gc, sys

@injected
class MemoryStatusPresenter:
    """
    Class providing the memory status presentation.
    """
    resourcesRoot = Node
    wire.entity('resourcesRoot')

    def __init__(self):
        assert isinstance(self.resourcesRoot, Node), 'Invalid root node %s' % self.resourcesRoot
        node = NodePath(self.resourcesRoot, True, 'MemoryStatus')
        node.get = InvokerFunction(GET, self.present, typeFor(Non), [
         Input('limit', typeFor(Integer), True, None),
         Input('include', typeFor(String), True, None),
         Input('exclude', typeFor(String), True, None)], {})
        return

    def present(self, limit, include=None, exclude=None):
        """
        Provides the dictionary structure presenting the memory.
        Attention this will also call the garbage collection.
        
        @return: dictionary
            The dictionary containing the memory status.
        """
        if not limit:
            limit = 10
        gc.collect()
        total, referencess = self.getRefcounts(limit, include, exclude)
        return {'References': {'Total': total,  'Class': referencess}}

    def getRefcounts(self, limit, prefixInclude, prefixExclude):
        counts = {}
        total = 0
        for m in sys.modules.values():
            for sym in dir(m):
                o = getattr(m, sym)
                typ = type(o)
                if isclass(typ):
                    name = fullyQName(typ)
                    if name not in counts:
                        count = sys.getrefcount(o)
                        counts[name] = count
                        total += count
                    else:
                        continue

        counts = [(name, count) for name, count in counts.items()]
        counts.sort(key=lambda pack: pack[1], reverse=True)
        d = OrderedDict()
        k = 0
        for className, count in counts:
            add = True
            if prefixInclude:
                add = className.startswith(prefixInclude)
            if prefixExclude:
                add = not className.startswith(prefixExclude)
            if add:
                d[className] = str(count)
            if k >= limit:
                break
            k += 1

        return (
         str(total), d)