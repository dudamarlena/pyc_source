# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/resource_node_associate.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 21, 2013

@package: support acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processor that associates a resources node with ACL rights.
"""
from acl.right_sevice import StructureRight, StructMethod, StructService, StructCall, RightService
from acl.spec import Filter, RightAcl
from ally.api.operator.container import Call
from ally.api.type import typeFor
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.core.impl.invoker import InvokerCall
from ally.core.spec.resources import Invoker, INodeChildListener, INodeInvokerListener, Path, Node
from ally.design.processor.attribute import defines, requires, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from ally.support.core.util_resources import iterateNodes, pathForNode, METHOD_NODE_ATTRIBUTE, invokerCallOf
from collections import Iterable
from itertools import chain

@injected
@setup(name='structureAssociate')
class StructureAssociate(INodeChildListener, INodeInvokerListener):
    """
    The association structure.
    """
    resourcesRoot = Node
    wire.entity('resourcesRoot')

    def __init__(self):
        assert isinstance(self.resourcesRoot, Node), 'Invalid root node %s' % self.resourcesRoot
        self.callInvokers = {}
        self.resourcesRoot.addStructureListener(self)

    def onChildAdded(self, node, child):
        """
        @see: INodeChildListener.onChildAdded
        """
        self.callInvokers.clear()

    def onInvokerChange(self, node, old, new):
        """
        @see: INodeInvokerListener.onInvokerChange
        """
        self.callInvokers.clear()

    def associate(self, structure):
        """
        Associate the structure with the resource root node.
        
        @param structure: StructureRight
            The structure to associate with.
        @return: StructCallInvokers
            The associated structure with the call invokers.
        """
        assert isinstance(structure, StructureRight), 'Invalid structure %s' % structure
        callInvokers = self.callInvokers.get(structure)
        if not callInvokers:
            callInvokers = self.callInvokers[structure] = StructCallInvokers()
            for node in iterateNodes(self.resourcesRoot):
                assert isinstance(node, Node), 'Invalid node %s' % node
                for method, attr in METHOD_NODE_ATTRIBUTE.items():
                    original = getattr(node, attr)
                    if not original:
                        continue
                    invoker = invokerCallOf(original)
                    if not invoker:
                        continue
                    assert isinstance(invoker, InvokerCall)
                    assert isinstance(invoker.call, Call)
                    structMethod = structure.methods.get(method)
                    if not structMethod:
                        continue
                    assert isinstance(structMethod, StructMethod)
                    structService = structMethod.services.get(typeFor(invoker.implementation))
                    if not structService:
                        continue
                    assert isinstance(structService, StructService)
                    structCall = structService.calls.get(invoker.call.name)
                    if not structCall:
                        continue
                    callInvokers.push(structCall, node, original)

        return callInvokers


class StructCallInvokers:
    """
    The structure for call with invokers.
    """
    __slots__ = ('invokersByCall', )

    def __init__(self):
        """
        Construct the association for call with invokers structure.
        
        @ivar invokersByCall: dictionary{StructCall, StructInvokers}
            The structure invokers indexed by the structure call.
        """
        self.invokersByCall = {}

    def push(self, structCall, node, invoker):
        """
        Pushes the call structure with the node and invoker.
        
        @param structCall: StructCall
            The structure call to push for.
        @param node: Node
            The node to push for.
        @param invoker: Invoker
            The invoker to push for.
        """
        assert isinstance(structCall, StructCall), 'Invalid structure call %s' % structCall
        structInvokers = self.invokersByCall.get(structCall)
        if not structInvokers:
            structInvokers = self.invokersByCall[structCall] = StructInvokers()
        structInvokers.push(node, invoker)


class StructInvokers:
    """
    The structure for node invoker.
    """
    __slots__ = ('invokers', )

    def __init__(self):
        """
        Construct the association for call with invokers structure.
        
        @ivar invokers: dictionary{Node, Invoker}
            The invoker structure indexed by the node.
        """
        self.invokers = {}

    def push(self, node, invoker):
        """
        Pushes the invoker for the node.
        
        @param node: Node
            The node to push for.
        @param invoker: Invoker
            The invoker to push for.
        """
        assert isinstance(node, Node), 'Invalid node %s' % node
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        self.invokers[node] = invoker


class Solicitation(Context):
    """
    The solicitation context.
    """
    method = optional(int, doc='\n    @rtype: integer\n    The method to get the permissions one of (GET, INSERT, UPDATE, DELETE) or a combination of those using the\n    "|" operator, if None then all methods are considered.\n    ')
    rights = requires(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The rights that make the scope of the resource node association, this iterable gets trimmed of all processed rights.\n    ')


class ReplyAvailable(Context):
    """
    The reply context.
    """
    rightsAvailable = defines(Iterable, doc='\n    @rtype: Iterable(RightAcl)\n    The rights that are available.\n    ')


class PermissionResource(Context):
    """
    The permission context.
    """
    method = defines(int, doc='\n    @rtype: integer\n    The method of the permission.\n    ')
    path = defines(Path, doc='\n    @rtype: Path\n    The path of the permission.\n    ')
    invoker = defines(Invoker, doc='\n    @rtype: Invoker\n    The invoker of the permission.\n    ')
    filters = defines(list, doc='\n    @rtype: list[Filter]\n    The filters for the permission.\n    ')


class SolicitationWithPermissions(Solicitation):
    """
    The solicitation context with permissions.
    """
    permissions = defines(Iterable, doc='\n    @rtype: Iterable(Permission)\n    The solicitation permissions.\n    ')


@injected
@setup(Handler, name='checkResourceAvailableRights')
class CheckResourceAvailableRights(HandlerProcessorProceed):
    """
    Provides the handler that filters the rights and keeps only those that have permissions.
    """
    structureAssociate = StructureAssociate
    wire.entity('structureAssociate')

    def __init__(self):
        assert isinstance(self.structureAssociate, StructureAssociate), 'Invalid structure association %s' % self.StructureAssociate
        super().__init__()

    def process(self, solicitation: Solicitation, reply: ReplyAvailable, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Filters the rights with permissions.
        """
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(reply, ReplyAvailable), 'Invalid reply %s' % reply
        assert isinstance(solicitation.rights, Iterable), 'Invalid rights %s' % solicitation.rights
        serviceRights, unprocessed = [], []
        for right in solicitation.rights:
            if isinstance(right, RightService):
                assert isinstance(right, RightService)
                serviceRights.append(right)
            else:
                assert isinstance(right, RightAcl), 'Invalid right %s' % right
                unprocessed.append(right)

        solicitation.rights = unprocessed
        if Solicitation.method in solicitation:
            available = self.iterAvailableRights(serviceRights, solicitation.method)
        else:
            available = self.iterAvailableRights(serviceRights)
        if reply.rightsAvailable is not None:
            reply.rightsAvailable = chain(reply.rightsAvailable, available)
        else:
            reply.rightsAvailable = available
        return

    def iterAvailableRights(self, serviceRights, method=None):
        """
        Iterates the rights that have permissions.
        """
        for right in serviceRights:
            assert isinstance(right, RightService)
            callInvokers = self.structureAssociate.associate(right.structure)
            assert isinstance(callInvokers, StructCallInvokers)
            if not callInvokers.invokersByCall:
                continue
            if method is None:
                yield right
                continue
            assert isinstance(method, int), 'Invalid method %s' % method
            for structCall in callInvokers.invokersByCall:
                assert isinstance(structCall, StructCall)
                if method & structCall.call.method:
                    yield right
                    continue

        return


@injected
@setup(Handler, name='iterateResourcePermissions')
class IterateResourcePermissions(HandlerProcessorProceed):
    """
    Provides the handler that iterates the permissions.
    """
    structureAssociate = StructureAssociate
    wire.entity('structureAssociate')

    def __init__(self):
        assert isinstance(self.structureAssociate, StructureAssociate), 'Invalid structure association %s' % self.StructureAssociate
        super().__init__()

    def process(self, Permission: PermissionResource, solicitation: SolicitationWithPermissions, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Provides the permissions.
        """
        assert issubclass(Permission, PermissionResource), 'Invalid permission class %s' % Permission
        assert isinstance(solicitation, SolicitationWithPermissions), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.rights, Iterable), 'Invalid rights %s' % solicitation.rights
        structures, unprocessed = [], []
        for right in solicitation.rights:
            if isinstance(right, RightService):
                assert isinstance(right, RightService)
                structures.append(right.structure)
            else:
                assert isinstance(right, RightAcl), 'Invalid right %s' % right
                unprocessed.append(right)

        solicitation.rights = unprocessed
        indexed = {}
        for structure in structures:
            callInvokers = self.structureAssociate.associate(structure)
            assert isinstance(callInvokers, StructCallInvokers), 'Invalid call invokers structure %s' % callInvokers
            for structCall, structInvokers in callInvokers.invokersByCall.items():
                assert isinstance(structCall, StructCall)
                assert isinstance(structInvokers, StructInvokers)
                indexedServices = indexed.get(structCall.call.method)
                if indexedServices is None:
                    indexedServices = indexed[structCall.call.method] = {}
                indexedCalls = indexedServices.get(structCall.serviceType)
                if indexedCalls is None:
                    indexedCalls = indexedServices[structCall.serviceType] = {}
                invokersAndFilters = indexedCalls.get(structCall.call.name)
                if invokersAndFilters is None:
                    invokersAndFilters = indexedCalls[structCall.call.name] = ({}, {})
                    isFirst = True
                else:
                    isFirst = False
                indexInvokers, filters = invokersAndFilters
                if Solicitation.method in solicitation and solicitation.method is not None:
                    if not solicitation.method & structCall.call.method:
                        continue
                assert isinstance(structCall.call, Call)
                indexInvokers.update(structInvokers.invokers)
                if structCall.filters:
                    if isFirst:
                        filters.update(structCall.filters)
                    elif filters:
                        oldFilters = dict(filters)
                        filters.clear()
                        for resourceType, structFilter in structCall.filters.items():
                            assert isinstance(structFilter, Filter)
                            resourceFilter = oldFilters.get(resourceType)
                            if not resourceFilter:
                                continue
                            assert isinstance(resourceFilter, Filter)
                            if resourceFilter.priority > structFilter.priority:
                                filters[resourceType] = structFilter
                            else:
                                filters[resourceType] = resourceFilter

                elif filters:
                    filters.clear()
                    continue

        permissions = self.iterPermissions(indexed, Permission)
        if solicitation.permissions is not None:
            solicitation.permissions = chain(solicitation.permissions, permissions)
        else:
            solicitation.permissions = permissions
        return

    def iterPermissions(self, indexed, Permission):
        """
        Iterates the permissions for the provided indexed structure.
        """
        for indexedMethod, indexedServices in indexed.items():
            for indexedCalls in indexedServices.values():
                for indexInvokers, filters in indexedCalls.values():
                    for node, invoker in indexInvokers.items():
                        yield Permission(method=indexedMethod, path=pathForNode(node), invoker=invoker, filters=list(filters.values()))