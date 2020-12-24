# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/resource_model_filter.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 27, 2013

@package: support acl
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Processors that processes on the permissions the model filters.
"""
from acl.spec import Filter
from ally.api.config import UPDATE, INSERT
from ally.api.operator.container import Model
from ally.api.operator.type import TypeModel, TypeModelProperty, TypeProperty
from ally.api.type import Input
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.core.spec.resources import Node, Invoker, INodeInvokerListener, Path
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from ally.support.core.util_resources import propertyTypesOf
from collections import Iterable
from weakref import WeakKeyDictionary
import logging
log = logging.getLogger(__name__)

class PermissionResource(Context):
    """
    The permission context.
    """
    method = requires(int)
    path = requires(Path)
    invoker = requires(Invoker)
    filters = requires(list)


class PermissionWithAuthenticated(PermissionResource):
    """
    The permission context.
    """
    modelsAuthenticated = defines(set, doc='\n    @rtype: set(TypeProperty)\n    The filter models set containing the authenticated property type for the filters.\n    ')


class PermissionWithModelFilters(PermissionResource):
    """
    The permission context.
    """
    filtersModels = defines(list, doc='\n    @rtype: list[ModelFilter]\n    A list with the model filters.\n    ')


class ModelFilterResource(Context):
    """
    The model filter context.
    """
    inputName = defines(str, doc='\n    @rtype: string\n    The input name where the model is found.\n    ')
    propertyName = defines(str, doc='\n    @rtype: string\n    The resource property name to be filtered and on the last position the filter to be used.\n    ')
    filters = defines(list, doc='\n    @rtype: string\n    The filters to be used.\n    ')


class Solicitation(Context):
    """
    The solicitation context.
    """
    permissions = requires(Iterable)


@injected
@setup(name='processorModelFilters')
class ProcessorModelFilters:
    """
    Processor that provides the model filters on the resources permissions.
    """

    def __init__(self):
        """
        Construct the persistence invoker service.
        """
        self.structure = Strucutre()

    def processPermissions(self, permissions, ModelFilter=None):
        """
        Process the permissions filter models.
        """
        for permission in permissions:
            assert isinstance(permission, PermissionResource), 'Invalid permission %s' % permission
            assert isinstance(permission.path, Path), 'Invalid path %s' % permission.path
            assert isinstance(permission.invoker, Invoker), 'Invalid invoker %s' % permission.invoker
            if not permission.filters:
                yield permission
                continue
            data = self.structure.process(permission.path.node, permission.invoker)
            if data is None:
                yield permission
                continue
            typesPath, typesModel, locations = data
            k = 0
            while k < len(permission.filters):
                rfilter = permission.filters[k]
                k += 1
                assert isinstance(rfilter, Filter), 'Invalid filter %s' % rfilter
                assert isinstance(rfilter.resource, TypeModelProperty), 'Invalid resource property %s' % rfilter.resource
                assert isinstance(rfilter.resource.container, Model), 'Invalid model %s' % rfilter.resource.container
                occModel = typesModel.count(rfilter.resource)
                if occModel == 0:
                    continue
                if occModel > 1:
                    log.error("Ambiguous resource filter type '%s', has to many occurrences in model types: %s", rfilter.resource, ', '.join(str(typ) for typ in typesModel))
                    continue
                occPath = typesPath.count(rfilter.resource)
                if occPath > 0:
                    if permission.invoker.method != UPDATE:
                        log.error("Ambiguous resource filter type '%s', has to many occurrences in path types: %s and model types: %s", rfilter.resource, ', '.join(str(typ) for typ in typesPath), ', '.join(str(typ) for typ in typesModel))
                    continue
                if permission.invoker.method == INSERT and rfilter.resource.container.propertyId == rfilter.resource.property:
                    continue
                k -= 1
                del permission.filters[k]
                if ModelFilter is None:
                    self.processAuthenticated(permission, rfilter)
                else:
                    self.processModelFilters(permission, rfilter, ModelFilter, *locations[typesModel.index(rfilter.resource)])

            yield permission

        return

    def processAuthenticated(self, permission, rfilter):
        """
        Process the permission with authenticated.
        """
        assert isinstance(permission, PermissionWithAuthenticated), 'Invalid permission %s' % permission
        assert isinstance(rfilter, Filter), 'Invalid filter %s' % rfilter
        if permission.modelsAuthenticated is None:
            permission.modelsAuthenticated = set()
        permission.modelsAuthenticated.add(rfilter.authenticated)
        return

    def processModelFilters(self, permission, rfilter, ModelFilter, inputName, propertyName):
        """
        Process the permission with model filters.
        """
        assert isinstance(permission, PermissionWithModelFilters), 'Invalid permission %s' % permission
        assert isinstance(rfilter, Filter), 'Invalid filter %s' % rfilter
        processed = False
        if permission.filtersModels is None:
            permission.filtersModels = []
        else:
            assert isinstance(permission.filtersModels, list), 'Invalid model filters %s' % permission.filtersModels
            for modelFilter in permission.filtersModels:
                assert isinstance(modelFilter, ModelFilterResource), 'Invalid model filter %s' % modelFilter
                if modelFilter.inputName == inputName and modelFilter.propertyName == propertyName:
                    assert isinstance(modelFilter.filters, list), 'Invalid filters %s' % modelFilter.filters
                    modelFilter.filters.append(rfilter)
                    processed = True
                    break

        if not processed:
            permission.filtersModels.append(ModelFilter(inputName=inputName, propertyName=propertyName, filters=[rfilter]))
        return


@injected
@setup(Handler, name='authenticatedForPermissions')
class AuthenticatedForPermissions(HandlerProcessorProceed):
    """
    Processor that provides the authenticated model filters on the resources permissions.
    """
    processorModelFilters = ProcessorModelFilters
    wire.entity('processorModelFilters')

    def __init__(self):
        """
        Construct the persistence invoker service.
        """
        assert isinstance(self.processorModelFilters, ProcessorModelFilters), 'Invalid model filters processor %s' % self.processorModelFilters
        super().__init__()

    def process(self, Permission: PermissionWithAuthenticated, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process permission model fitler.
        """
        assert issubclass(Permission, PermissionResource), 'Invalid permission class %s' % Permission
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.permissions, Iterable), 'Invalid permissions %s' % solicitation.permissions
        solicitation.permissions = self.processorModelFilters.processPermissions(solicitation.permissions)


@injected
@setup(Handler, name='modelFiltersForPermissions')
class ModelFiltersForPermissions(HandlerProcessorProceed):
    """
    Processor that provides the model filters on the resources permissions.
    """
    processorModelFilters = ProcessorModelFilters
    wire.entity('processorModelFilters')

    def __init__(self):
        """
        Construct the persistence invoker service.
        """
        assert isinstance(self.processorModelFilters, ProcessorModelFilters), 'Invalid model filters processor %s' % self.processorModelFilters
        super().__init__()

    def process(self, Permission: PermissionWithModelFilters, ModelFilter: ModelFilterResource, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Process permission model fitler.
        """
        assert issubclass(Permission, PermissionResource), 'Invalid permission class %s' % Permission
        assert issubclass(ModelFilter, ModelFilterResource), 'Invalid model filter class %s' % ModelFilter
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.permissions, Iterable), 'Invalid permissions %s' % solicitation.permissions
        solicitation.permissions = self.processorModelFilters.processPermissions(solicitation.permissions, ModelFilter)


class Strucutre(INodeInvokerListener):
    """
    The general structure.
    """
    __slots__ = ('structNodes', 'typesPaths')

    def __init__(self):
        """
        Construct the structure.
        """
        self.structNodes = WeakKeyDictionary()
        self.typesPaths = WeakKeyDictionary()

    def onInvokerChange(self, node, old, new):
        """
        @see: INodeInvokerListener.onInvokerChange
        """
        self.structNodes.pop(node, None)
        self.typesPaths.pop(node, None)
        return

    def process(self, node, invoker):
        """
        Process the structure for the provided node and invoker.
        
        @param node: Node
            The node to process for.
        @param invoker: Invoker
            The invoker to process.
        @return: tuple(list[TypeProperty], @see: StructNode.process)|None
            The list of path property types.
        """
        assert isinstance(node, Node), 'Invalid node %s' % node
        structNode = self.structNodes.get(node)
        if structNode is None:
            structNode = self.structNodes[node] = StructNode()
        assert isinstance(structNode, StructNode)
        data = structNode.process(invoker)
        if data is None:
            return
        else:
            typesPath = self.typesPaths.get(node)
            if typesPath is None:
                typesPath = self.typesPaths[node] = (
                 propertyTypesOf(node, invoker),)
            return typesPath + data


class StructNode:
    """
    The structure for node.
    """
    __slots__ = ('typesModels', )

    def __init__(self):
        """
        Construct the structure for the provided node.
        """
        self.typesModels = {}

    def process(self, invoker):
        """
        Process the invoker.
        
        @param invoker: Invoker
            The invoker to process.
        @return: tuple(list[TypeProperty], list[tuple(string, string)])|None
            The list of invokers models properties types, ([models properties], [locations of model properties]).
        """
        assert isinstance(invoker, Invoker), 'Invalid invoker %s' % invoker
        if invoker not in self.typesModels:
            typesModel, locations = [], []
            for inp in invoker.inputs:
                assert isinstance(inp, Input), 'Invalid input %s' % inp
                if isinstance(inp.type, TypeModel):
                    assert isinstance(inp.type, TypeModel)
                    for typeProperty in inp.type.propertyTypes():
                        assert isinstance(typeProperty, TypeProperty), 'Invalid property type %s' % typeProperty
                        typesModel.append(typeProperty)
                        locations.append((inp.name, typeProperty.property))

                    continue

            if not typesModel:
                self.typesModels[invoker] = None
            else:
                self.typesModels[invoker] = (
                 typesModel, locations)
        return self.typesModels.get(invoker)