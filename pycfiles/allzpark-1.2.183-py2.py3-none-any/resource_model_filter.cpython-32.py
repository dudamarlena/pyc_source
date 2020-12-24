# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/resource_model_filter.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 27, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessors that processes on the permissions the model filters.\n'
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

    def processPermissions--- This code section failed: ---

 L. 109         0  SETUP_LOOP          738  'to 738'
                3  LOAD_FAST                'permissions'
                6  GET_ITER         
                7  FOR_ITER            737  'to 737'
               10  STORE_FAST               'permission'

 L. 110        13  LOAD_GLOBAL              isinstance
               16  LOAD_FAST                'permission'
               19  LOAD_GLOBAL              PermissionResource
               22  CALL_FUNCTION_2       2  '2 positional, 0 named'
               25  POP_JUMP_IF_TRUE     44  'to 44'
               28  LOAD_ASSERT              AssertionError
               31  LOAD_STR                 'Invalid permission %s'
               34  LOAD_FAST                'permission'
               37  BINARY_MODULO    
               38  CALL_FUNCTION_1       1  '1 positional, 0 named'
               41  RAISE_VARARGS_1       1  ''
             44_0  COME_FROM            25  '25'

 L. 111        44  LOAD_GLOBAL              isinstance
               47  LOAD_FAST                'permission'
               50  LOAD_ATTR                path
               53  LOAD_GLOBAL              Path
               56  CALL_FUNCTION_2       2  '2 positional, 0 named'
               59  POP_JUMP_IF_TRUE     81  'to 81'
               62  LOAD_ASSERT              AssertionError
               65  LOAD_STR                 'Invalid path %s'
               68  LOAD_FAST                'permission'
               71  LOAD_ATTR                path
               74  BINARY_MODULO    
               75  CALL_FUNCTION_1       1  '1 positional, 0 named'
               78  RAISE_VARARGS_1       1  ''
             81_0  COME_FROM            59  '59'

 L. 112        81  LOAD_GLOBAL              isinstance
               84  LOAD_FAST                'permission'
               87  LOAD_ATTR                invoker
               90  LOAD_GLOBAL              Invoker
               93  CALL_FUNCTION_2       2  '2 positional, 0 named'
               96  POP_JUMP_IF_TRUE    118  'to 118'
               99  LOAD_ASSERT              AssertionError
              102  LOAD_STR                 'Invalid invoker %s'
              105  LOAD_FAST                'permission'
              108  LOAD_ATTR                invoker
              111  BINARY_MODULO    
              112  CALL_FUNCTION_1       1  '1 positional, 0 named'
              115  RAISE_VARARGS_1       1  ''
            118_0  COME_FROM            96  '96'

 L. 114       118  LOAD_FAST                'permission'
              121  LOAD_ATTR                filters
              124  POP_JUMP_IF_TRUE    138  'to 138'

 L. 115       127  LOAD_FAST                'permission'
              130  YIELD_VALUE      
              131  POP_TOP          

 L. 116       132  CONTINUE              7  'to 7'
              135  JUMP_FORWARD        138  'to 138'
            138_0  COME_FROM           135  '135'

 L. 118       138  LOAD_FAST                'self'
              141  LOAD_ATTR                structure
              144  LOAD_ATTR                process
              147  LOAD_FAST                'permission'
              150  LOAD_ATTR                path
              153  LOAD_ATTR                node
              156  LOAD_FAST                'permission'
              159  LOAD_ATTR                invoker
              162  CALL_FUNCTION_2       2  '2 positional, 0 named'
              165  STORE_FAST               'data'

 L. 119       168  LOAD_FAST                'data'
              171  LOAD_CONST               None
              174  COMPARE_OP               is
              177  POP_JUMP_IF_FALSE   191  'to 191'

 L. 120       180  LOAD_FAST                'permission'
              183  YIELD_VALUE      
              184  POP_TOP          

 L. 121       185  CONTINUE              7  'to 7'
              188  JUMP_FORWARD        191  'to 191'
            191_0  COME_FROM           188  '188'

 L. 123       191  LOAD_FAST                'data'
              194  UNPACK_SEQUENCE_3     3 
              197  STORE_FAST               'typesPath'
              200  STORE_FAST               'typesModel'
              203  STORE_FAST               'locations'

 L. 125       206  LOAD_CONST               0
              209  STORE_FAST               'k'

 L. 126       212  SETUP_LOOP          729  'to 729'
              215  LOAD_FAST                'k'
              218  LOAD_GLOBAL              len
              221  LOAD_FAST                'permission'
              224  LOAD_ATTR                filters
              227  CALL_FUNCTION_1       1  '1 positional, 0 named'
              230  COMPARE_OP               <
              233  POP_JUMP_IF_FALSE   728  'to 728'

 L. 127       236  LOAD_FAST                'permission'
              239  LOAD_ATTR                filters
              242  LOAD_FAST                'k'
              245  BINARY_SUBSCR    
              246  STORE_FAST               'rfilter'

 L. 128       249  LOAD_FAST                'k'
              252  LOAD_CONST               1
              255  INPLACE_ADD      
              256  STORE_FAST               'k'

 L. 129       259  LOAD_GLOBAL              isinstance
              262  LOAD_FAST                'rfilter'
              265  LOAD_GLOBAL              Filter
              268  CALL_FUNCTION_2       2  '2 positional, 0 named'
              271  POP_JUMP_IF_TRUE    290  'to 290'
              274  LOAD_ASSERT              AssertionError
              277  LOAD_STR                 'Invalid filter %s'
              280  LOAD_FAST                'rfilter'
              283  BINARY_MODULO    
              284  CALL_FUNCTION_1       1  '1 positional, 0 named'
              287  RAISE_VARARGS_1       1  ''
            290_0  COME_FROM           271  '271'

 L. 130       290  LOAD_GLOBAL              isinstance
              293  LOAD_FAST                'rfilter'
              296  LOAD_ATTR                resource
              299  LOAD_GLOBAL              TypeModelProperty
              302  CALL_FUNCTION_2       2  '2 positional, 0 named'
              305  POP_JUMP_IF_TRUE    327  'to 327'
              308  LOAD_ASSERT              AssertionError
              311  LOAD_STR                 'Invalid resource property %s'
              314  LOAD_FAST                'rfilter'
              317  LOAD_ATTR                resource
              320  BINARY_MODULO    
              321  CALL_FUNCTION_1       1  '1 positional, 0 named'
              324  RAISE_VARARGS_1       1  ''
            327_0  COME_FROM           305  '305'

 L. 131       327  LOAD_GLOBAL              isinstance
              330  LOAD_FAST                'rfilter'
              333  LOAD_ATTR                resource
              336  LOAD_ATTR                container
              339  LOAD_GLOBAL              Model
              342  CALL_FUNCTION_2       2  '2 positional, 0 named'
              345  POP_JUMP_IF_TRUE    370  'to 370'
              348  LOAD_ASSERT              AssertionError
              351  LOAD_STR                 'Invalid model %s'
              354  LOAD_FAST                'rfilter'
              357  LOAD_ATTR                resource
              360  LOAD_ATTR                container
              363  BINARY_MODULO    
              364  CALL_FUNCTION_1       1  '1 positional, 0 named'
              367  RAISE_VARARGS_1       1  ''
            370_0  COME_FROM           345  '345'

 L. 132       370  LOAD_FAST                'typesModel'
              373  LOAD_ATTR                count
              376  LOAD_FAST                'rfilter'
              379  LOAD_ATTR                resource
              382  CALL_FUNCTION_1       1  '1 positional, 0 named'
              385  STORE_FAST               'occModel'

 L. 133       388  LOAD_FAST                'occModel'
              391  LOAD_CONST               0
              394  COMPARE_OP               ==
              397  POP_JUMP_IF_FALSE   406  'to 406'
              400  JUMP_BACK           215  'to 215'
              403  JUMP_FORWARD        406  'to 406'
            406_0  COME_FROM           403  '403'

 L. 134       406  LOAD_FAST                'occModel'
              409  LOAD_CONST               1
              412  COMPARE_OP               >
              415  POP_JUMP_IF_FALSE   465  'to 465'

 L. 135       418  LOAD_GLOBAL              log
              421  LOAD_ATTR                error
              424  LOAD_STR                 "Ambiguous resource filter type '%s', has to many occurrences in model types: %s"

 L. 136       427  LOAD_FAST                'rfilter'
              430  LOAD_ATTR                resource
              433  LOAD_STR                 ', '
              436  LOAD_ATTR                join
              439  LOAD_GENEXPR             '<code_object <genexpr>>'
              442  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              445  LOAD_FAST                'typesModel'
              448  GET_ITER         
              449  CALL_FUNCTION_1       1  '1 positional, 0 named'
              452  CALL_FUNCTION_1       1  '1 positional, 0 named'
              455  CALL_FUNCTION_3       3  '3 positional, 0 named'
              458  POP_TOP          

 L. 137       459  CONTINUE            215  'to 215'
              462  JUMP_FORWARD        465  'to 465'
            465_0  COME_FROM           462  '462'

 L. 138       465  LOAD_FAST                'typesPath'
              468  LOAD_ATTR                count
              471  LOAD_FAST                'rfilter'
              474  LOAD_ATTR                resource
              477  CALL_FUNCTION_1       1  '1 positional, 0 named'
              480  STORE_FAST               'occPath'

 L. 139       483  LOAD_FAST                'occPath'
              486  LOAD_CONST               0
              489  COMPARE_OP               >
              492  POP_JUMP_IF_FALSE   585  'to 585'

 L. 141       495  LOAD_FAST                'permission'
              498  LOAD_ATTR                invoker
              501  LOAD_ATTR                method
              504  LOAD_GLOBAL              UPDATE
              507  COMPARE_OP               !=
              510  POP_JUMP_IF_FALSE   215  'to 215'

 L. 142       513  LOAD_GLOBAL              log
              516  LOAD_ATTR                error
              519  LOAD_STR                 "Ambiguous resource filter type '%s', has to many occurrences in path types: %s and model types: %s"

 L. 143       522  LOAD_FAST                'rfilter'
              525  LOAD_ATTR                resource
              528  LOAD_STR                 ', '
              531  LOAD_ATTR                join
              534  LOAD_GENEXPR             '<code_object <genexpr>>'
              537  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              540  LOAD_FAST                'typesPath'
              543  GET_ITER         
              544  CALL_FUNCTION_1       1  '1 positional, 0 named'
              547  CALL_FUNCTION_1       1  '1 positional, 0 named'

 L. 144       550  LOAD_STR                 ', '
              553  LOAD_ATTR                join
              556  LOAD_GENEXPR             '<code_object <genexpr>>'
              559  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              562  LOAD_FAST                'typesModel'
              565  GET_ITER         
              566  CALL_FUNCTION_1       1  '1 positional, 0 named'
              569  CALL_FUNCTION_1       1  '1 positional, 0 named'
              572  CALL_FUNCTION_4       4  '4 positional, 0 named'
              575  POP_TOP          
              576  JUMP_BACK           215  'to 215'

 L. 145       579  CONTINUE            215  'to 215'
              582  JUMP_FORWARD        585  'to 585'
            585_0  COME_FROM           582  '582'

 L. 147       585  LOAD_FAST                'permission'
              588  LOAD_ATTR                invoker
              591  LOAD_ATTR                method
              594  LOAD_GLOBAL              INSERT
              597  COMPARE_OP               ==
              600  POP_JUMP_IF_FALSE   636  'to 636'
              603  LOAD_FAST                'rfilter'
              606  LOAD_ATTR                resource
              609  LOAD_ATTR                container
              612  LOAD_ATTR                propertyId
              615  LOAD_FAST                'rfilter'
              618  LOAD_ATTR                resource
              621  LOAD_ATTR                property
              624  COMPARE_OP               ==
            627_0  COME_FROM           600  '600'
              627  POP_JUMP_IF_FALSE   636  'to 636'

 L. 149       630  CONTINUE            215  'to 215'
              633  JUMP_FORWARD        636  'to 636'
            636_0  COME_FROM           633  '633'

 L. 152       636  LOAD_FAST                'k'
              639  LOAD_CONST               1
              642  INPLACE_SUBTRACT 
              643  STORE_FAST               'k'

 L. 153       646  LOAD_FAST                'permission'
              649  LOAD_ATTR                filters
              652  LOAD_FAST                'k'
              655  DELETE_SUBSCR    

 L. 155       656  LOAD_FAST                'ModelFilter'
              659  LOAD_CONST               None
              662  COMPARE_OP               is
              665  POP_JUMP_IF_FALSE   687  'to 687'
              668  LOAD_FAST                'self'
              671  LOAD_ATTR                processAuthenticated
              674  LOAD_FAST                'permission'
              677  LOAD_FAST                'rfilter'
              680  CALL_FUNCTION_2       2  '2 positional, 0 named'
              683  POP_TOP          
              684  JUMP_BACK           215  'to 215'

 L. 156       687  LOAD_FAST                'self'
              690  LOAD_ATTR                processModelFilters
              693  LOAD_FAST                'permission'
              696  LOAD_FAST                'rfilter'
              699  LOAD_FAST                'ModelFilter'
              702  LOAD_FAST                'locations'
              705  LOAD_FAST                'typesModel'
              708  LOAD_ATTR                index
              711  LOAD_FAST                'rfilter'
              714  LOAD_ATTR                resource
              717  CALL_FUNCTION_1       1  '1 positional, 0 named'
              720  BINARY_SUBSCR    
              721  CALL_FUNCTION_VAR_3     3  '3 positional, 0 named'
              724  POP_TOP          
              725  JUMP_BACK           215  'to 215'
              728  POP_BLOCK        
            729_0  COME_FROM_LOOP      212  '212'

 L. 158       729  LOAD_FAST                'permission'
              732  YIELD_VALUE      
              733  POP_TOP          
              734  JUMP_BACK             7  'to 7'
              737  POP_BLOCK        
            738_0  COME_FROM_LOOP        0  '0'
              738  LOAD_CONST               None
              741  RETURN_VALUE     

Parse error at or near `JUMP_BACK' instruction at offset 684

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
                typesPath = self.typesPaths[node] = (propertyTypesOf(node, invoker),)
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