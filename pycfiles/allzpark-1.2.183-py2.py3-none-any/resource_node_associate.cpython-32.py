# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/resource_node_associate.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 21, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that associates a resources node with ACL rights.\n'
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

    def process--- This code section failed: ---

 L. 309         0  LOAD_GLOBAL              issubclass
                3  LOAD_FAST                'Permission'
                6  LOAD_GLOBAL              PermissionResource
                9  CALL_FUNCTION_2       2  '2 positional, 0 named'
               12  POP_JUMP_IF_TRUE     31  'to 31'
               15  LOAD_ASSERT              AssertionError
               18  LOAD_STR                 'Invalid permission class %s'
               21  LOAD_FAST                'Permission'
               24  BINARY_MODULO    
               25  CALL_FUNCTION_1       1  '1 positional, 0 named'
               28  RAISE_VARARGS_1       1  ''
             31_0  COME_FROM            12  '12'

 L. 310        31  LOAD_GLOBAL              isinstance
               34  LOAD_FAST                'solicitation'
               37  LOAD_GLOBAL              SolicitationWithPermissions
               40  CALL_FUNCTION_2       2  '2 positional, 0 named'
               43  POP_JUMP_IF_TRUE     62  'to 62'
               46  LOAD_ASSERT              AssertionError
               49  LOAD_STR                 'Invalid solicitation %s'
               52  LOAD_FAST                'solicitation'
               55  BINARY_MODULO    
               56  CALL_FUNCTION_1       1  '1 positional, 0 named'
               59  RAISE_VARARGS_1       1  ''
             62_0  COME_FROM            43  '43'

 L. 311        62  LOAD_GLOBAL              isinstance
               65  LOAD_FAST                'solicitation'
               68  LOAD_ATTR                rights
               71  LOAD_GLOBAL              Iterable
               74  CALL_FUNCTION_2       2  '2 positional, 0 named'
               77  POP_JUMP_IF_TRUE     99  'to 99'
               80  LOAD_ASSERT              AssertionError
               83  LOAD_STR                 'Invalid rights %s'
               86  LOAD_FAST                'solicitation'
               89  LOAD_ATTR                rights
               92  BINARY_MODULO    
               93  CALL_FUNCTION_1       1  '1 positional, 0 named'
               96  RAISE_VARARGS_1       1  ''
             99_0  COME_FROM            77  '77'

 L. 313        99  BUILD_LIST_0          0 
              102  BUILD_LIST_0          0 
              105  ROT_TWO          
              106  STORE_FAST               'structures'
              109  STORE_FAST               'unprocessed'

 L. 314       112  SETUP_LOOP          231  'to 231'
              115  LOAD_FAST                'solicitation'
              118  LOAD_ATTR                rights
              121  GET_ITER         
              122  FOR_ITER            230  'to 230'
              125  STORE_FAST               'right'

 L. 315       128  LOAD_GLOBAL              isinstance
              131  LOAD_FAST                'right'
              134  LOAD_GLOBAL              RightService
              137  CALL_FUNCTION_2       2  '2 positional, 0 named'
              140  POP_JUMP_IF_FALSE   183  'to 183'

 L. 316       143  LOAD_GLOBAL              isinstance
              146  LOAD_FAST                'right'
              149  LOAD_GLOBAL              RightService
              152  CALL_FUNCTION_2       2  '2 positional, 0 named'
              155  POP_JUMP_IF_TRUE    164  'to 164'
              158  LOAD_ASSERT              AssertionError
              161  RAISE_VARARGS_1       1  ''
            164_0  COME_FROM           155  '155'

 L. 317       164  LOAD_FAST                'structures'
              167  LOAD_ATTR                append
              170  LOAD_FAST                'right'
              173  LOAD_ATTR                structure
              176  CALL_FUNCTION_1       1  '1 positional, 0 named'
              179  POP_TOP          
              180  JUMP_BACK           122  'to 122'

 L. 319       183  LOAD_GLOBAL              isinstance
              186  LOAD_FAST                'right'
              189  LOAD_GLOBAL              RightAcl
              192  CALL_FUNCTION_2       2  '2 positional, 0 named'
              195  POP_JUMP_IF_TRUE    214  'to 214'
              198  LOAD_ASSERT              AssertionError
              201  LOAD_STR                 'Invalid right %s'
              204  LOAD_FAST                'right'
              207  BINARY_MODULO    
              208  CALL_FUNCTION_1       1  '1 positional, 0 named'
              211  RAISE_VARARGS_1       1  ''
            214_0  COME_FROM           195  '195'

 L. 320       214  LOAD_FAST                'unprocessed'
              217  LOAD_ATTR                append
              220  LOAD_FAST                'right'
              223  CALL_FUNCTION_1       1  '1 positional, 0 named'
              226  POP_TOP          
              227  JUMP_BACK           122  'to 122'
              230  POP_BLOCK        
            231_0  COME_FROM_LOOP      112  '112'

 L. 322       231  LOAD_FAST                'unprocessed'
              234  LOAD_FAST                'solicitation'
              237  STORE_ATTR               rights

 L. 325       240  BUILD_MAP_0           0  ''
              243  STORE_FAST               'indexed'

 L. 326       246  SETUP_LOOP          905  'to 905'
              249  LOAD_FAST                'structures'
              252  GET_ITER         
              253  FOR_ITER            904  'to 904'
              256  STORE_FAST               'structure'

 L. 327       259  LOAD_FAST                'self'
              262  LOAD_ATTR                structureAssociate
              265  LOAD_ATTR                associate
              268  LOAD_FAST                'structure'
              271  CALL_FUNCTION_1       1  '1 positional, 0 named'
              274  STORE_FAST               'callInvokers'

 L. 328       277  LOAD_GLOBAL              isinstance
              280  LOAD_FAST                'callInvokers'
              283  LOAD_GLOBAL              StructCallInvokers
              286  CALL_FUNCTION_2       2  '2 positional, 0 named'
              289  POP_JUMP_IF_TRUE    308  'to 308'
              292  LOAD_ASSERT              AssertionError
              295  LOAD_STR                 'Invalid call invokers structure %s'
              298  LOAD_FAST                'callInvokers'
              301  BINARY_MODULO    
              302  CALL_FUNCTION_1       1  '1 positional, 0 named'
              305  RAISE_VARARGS_1       1  ''
            308_0  COME_FROM           289  '289'

 L. 329       308  SETUP_LOOP          901  'to 901'
              311  LOAD_FAST                'callInvokers'
              314  LOAD_ATTR                invokersByCall
              317  LOAD_ATTR                items
              320  CALL_FUNCTION_0       0  '0 positional, 0 named'
              323  GET_ITER         
              324  FOR_ITER            900  'to 900'
              327  UNPACK_SEQUENCE_2     2 
              330  STORE_FAST               'structCall'
              333  STORE_FAST               'structInvokers'

 L. 330       336  LOAD_GLOBAL              isinstance
              339  LOAD_FAST                'structCall'
              342  LOAD_GLOBAL              StructCall
              345  CALL_FUNCTION_2       2  '2 positional, 0 named'
              348  POP_JUMP_IF_TRUE    357  'to 357'
              351  LOAD_ASSERT              AssertionError
              354  RAISE_VARARGS_1       1  ''
            357_0  COME_FROM           348  '348'

 L. 331       357  LOAD_GLOBAL              isinstance
              360  LOAD_FAST                'structInvokers'
              363  LOAD_GLOBAL              StructInvokers
              366  CALL_FUNCTION_2       2  '2 positional, 0 named'
              369  POP_JUMP_IF_TRUE    378  'to 378'
              372  LOAD_ASSERT              AssertionError
              375  RAISE_VARARGS_1       1  ''
            378_0  COME_FROM           369  '369'

 L. 334       378  LOAD_FAST                'indexed'
              381  LOAD_ATTR                get
              384  LOAD_FAST                'structCall'
              387  LOAD_ATTR                call
              390  LOAD_ATTR                method
              393  CALL_FUNCTION_1       1  '1 positional, 0 named'
              396  STORE_FAST               'indexedServices'

 L. 335       399  LOAD_FAST                'indexedServices'
              402  LOAD_CONST               None
              405  COMPARE_OP               is
              408  POP_JUMP_IF_FALSE   434  'to 434'
              411  BUILD_MAP_0           0  ''
              414  DUP_TOP          
              415  STORE_FAST               'indexedServices'
              418  LOAD_FAST                'indexed'
              421  LOAD_FAST                'structCall'
              424  LOAD_ATTR                call
              427  LOAD_ATTR                method
              430  STORE_SUBSCR     
              431  JUMP_FORWARD        434  'to 434'
            434_0  COME_FROM           431  '431'

 L. 337       434  LOAD_FAST                'indexedServices'
              437  LOAD_ATTR                get
              440  LOAD_FAST                'structCall'
              443  LOAD_ATTR                serviceType
              446  CALL_FUNCTION_1       1  '1 positional, 0 named'
              449  STORE_FAST               'indexedCalls'

 L. 338       452  LOAD_FAST                'indexedCalls'
              455  LOAD_CONST               None
              458  COMPARE_OP               is
              461  POP_JUMP_IF_FALSE   484  'to 484'
              464  BUILD_MAP_0           0  ''
              467  DUP_TOP          
              468  STORE_FAST               'indexedCalls'
              471  LOAD_FAST                'indexedServices'
              474  LOAD_FAST                'structCall'
              477  LOAD_ATTR                serviceType
              480  STORE_SUBSCR     
              481  JUMP_FORWARD        484  'to 484'
            484_0  COME_FROM           481  '481'

 L. 340       484  LOAD_FAST                'indexedCalls'
              487  LOAD_ATTR                get
              490  LOAD_FAST                'structCall'
              493  LOAD_ATTR                call
              496  LOAD_ATTR                name
              499  CALL_FUNCTION_1       1  '1 positional, 0 named'
              502  STORE_FAST               'invokersAndFilters'

 L. 341       505  LOAD_FAST                'invokersAndFilters'
              508  LOAD_CONST               None
              511  COMPARE_OP               is
              514  POP_JUMP_IF_FALSE   552  'to 552'

 L. 342       517  BUILD_MAP_0           0  ''
              520  BUILD_MAP_0           0  ''
              523  BUILD_TUPLE_2         2 
              526  DUP_TOP          
              527  STORE_FAST               'invokersAndFilters'
              530  LOAD_FAST                'indexedCalls'
              533  LOAD_FAST                'structCall'
              536  LOAD_ATTR                call
              539  LOAD_ATTR                name
              542  STORE_SUBSCR     

 L. 343       543  LOAD_CONST               True
              546  STORE_FAST               'isFirst'
              549  JUMP_FORWARD        558  'to 558'
              552  ELSE                     '558'

 L. 344       552  LOAD_CONST               False
              555  STORE_FAST               'isFirst'
            558_0  COME_FROM           549  '549'

 L. 345       558  LOAD_FAST                'invokersAndFilters'
              561  UNPACK_SEQUENCE_2     2 
              564  STORE_FAST               'indexInvokers'
              567  STORE_FAST               'filters'

 L. 347       570  LOAD_GLOBAL              Solicitation
              573  LOAD_ATTR                method
              576  LOAD_FAST                'solicitation'
              579  COMPARE_OP               in
              582  POP_JUMP_IF_FALSE   628  'to 628'
              585  LOAD_FAST                'solicitation'
              588  LOAD_ATTR                method
              591  LOAD_CONST               None
              594  COMPARE_OP               is-not
            597_0  COME_FROM           582  '582'
              597  POP_JUMP_IF_FALSE   628  'to 628'

 L. 348       600  LOAD_FAST                'solicitation'
              603  LOAD_ATTR                method
              606  LOAD_FAST                'structCall'
              609  LOAD_ATTR                call
              612  LOAD_ATTR                method
              615  BINARY_AND       
              616  POP_JUMP_IF_TRUE    628  'to 628'
              619  JUMP_BACK           324  'to 324'
              622  JUMP_ABSOLUTE       628  'to 628'
              625  JUMP_FORWARD        628  'to 628'
            628_0  COME_FROM           625  '625'

 L. 349       628  LOAD_GLOBAL              isinstance
              631  LOAD_FAST                'structCall'
              634  LOAD_ATTR                call
              637  LOAD_GLOBAL              Call
              640  CALL_FUNCTION_2       2  '2 positional, 0 named'
              643  POP_JUMP_IF_TRUE    652  'to 652'
              646  LOAD_ASSERT              AssertionError
              649  RAISE_VARARGS_1       1  ''
            652_0  COME_FROM           643  '643'

 L. 350       652  LOAD_FAST                'indexInvokers'
              655  LOAD_ATTR                update
              658  LOAD_FAST                'structInvokers'
              661  LOAD_ATTR                invokers
              664  CALL_FUNCTION_1       1  '1 positional, 0 named'
              667  POP_TOP          

 L. 353       668  LOAD_FAST                'structCall'
              671  LOAD_ATTR                filters
              674  POP_JUMP_IF_FALSE   878  'to 878'

 L. 354       677  LOAD_FAST                'isFirst'
              680  POP_JUMP_IF_FALSE   702  'to 702'
              683  LOAD_FAST                'filters'
              686  LOAD_ATTR                update
              689  LOAD_FAST                'structCall'
              692  LOAD_ATTR                filters
              695  CALL_FUNCTION_1       1  '1 positional, 0 named'
              698  POP_TOP          
              699  JUMP_ABSOLUTE       897  'to 897'
              702  ELSE                     '875'

 L. 355       702  LOAD_FAST                'filters'
              705  POP_JUMP_IF_FALSE   897  'to 897'

 L. 356       708  LOAD_GLOBAL              dict
              711  LOAD_FAST                'filters'
              714  CALL_FUNCTION_1       1  '1 positional, 0 named'
              717  STORE_FAST               'oldFilters'

 L. 357       720  LOAD_FAST                'filters'
              723  LOAD_ATTR                clear
              726  CALL_FUNCTION_0       0  '0 positional, 0 named'
              729  POP_TOP          

 L. 358       730  SETUP_LOOP          875  'to 875'
              733  LOAD_FAST                'structCall'
              736  LOAD_ATTR                filters
              739  LOAD_ATTR                items
              742  CALL_FUNCTION_0       0  '0 positional, 0 named'
              745  GET_ITER         
              746  FOR_ITER            871  'to 871'
              749  UNPACK_SEQUENCE_2     2 
              752  STORE_FAST               'resourceType'
              755  STORE_FAST               'structFilter'

 L. 359       758  LOAD_GLOBAL              isinstance
              761  LOAD_FAST                'structFilter'
              764  LOAD_GLOBAL              Filter
              767  CALL_FUNCTION_2       2  '2 positional, 0 named'
              770  POP_JUMP_IF_TRUE    779  'to 779'
              773  LOAD_ASSERT              AssertionError
              776  RAISE_VARARGS_1       1  ''
            779_0  COME_FROM           770  '770'

 L. 360       779  LOAD_FAST                'oldFilters'
              782  LOAD_ATTR                get
              785  LOAD_FAST                'resourceType'
              788  CALL_FUNCTION_1       1  '1 positional, 0 named'
              791  STORE_FAST               'resourceFilter'

 L. 361       794  LOAD_FAST                'resourceFilter'
              797  POP_JUMP_IF_TRUE    806  'to 806'
              800  CONTINUE            746  'to 746'
              803  JUMP_FORWARD        806  'to 806'
            806_0  COME_FROM           803  '803'

 L. 362       806  LOAD_GLOBAL              isinstance
              809  LOAD_FAST                'resourceFilter'
              812  LOAD_GLOBAL              Filter
              815  CALL_FUNCTION_2       2  '2 positional, 0 named'
              818  POP_JUMP_IF_TRUE    827  'to 827'
              821  LOAD_ASSERT              AssertionError
              824  RAISE_VARARGS_1       1  ''
            827_0  COME_FROM           818  '818'

 L. 364       827  LOAD_FAST                'resourceFilter'
              830  LOAD_ATTR                priority
              833  LOAD_FAST                'structFilter'
              836  LOAD_ATTR                priority
              839  COMPARE_OP               >
              842  POP_JUMP_IF_FALSE   858  'to 858'
              845  LOAD_FAST                'structFilter'
              848  LOAD_FAST                'filters'
              851  LOAD_FAST                'resourceType'
              854  STORE_SUBSCR     
              855  JUMP_BACK           746  'to 746'

 L. 365       858  LOAD_FAST                'resourceFilter'
              861  LOAD_FAST                'filters'
              864  LOAD_FAST                'resourceType'
              867  STORE_SUBSCR     
              868  JUMP_BACK           746  'to 746'
              871  POP_BLOCK        
            872_0  COME_FROM_LOOP      730  '730'
              872  JUMP_ABSOLUTE       897  'to 897'
              875  JUMP_BACK           324  'to 324'

 L. 366       878  LOAD_FAST                'filters'
              881  POP_JUMP_IF_FALSE   324  'to 324'
              884  LOAD_FAST                'filters'
              887  LOAD_ATTR                clear
              890  CALL_FUNCTION_0       0  '0 positional, 0 named'
              893  POP_TOP          
              894  CONTINUE            324  'to 324'
              897  JUMP_BACK           324  'to 324'
              900  POP_BLOCK        
            901_0  COME_FROM_LOOP      308  '308'
              901  JUMP_BACK           253  'to 253'
              904  POP_BLOCK        
            905_0  COME_FROM_LOOP      246  '246'

 L. 368       905  LOAD_FAST                'self'
              908  LOAD_ATTR                iterPermissions
              911  LOAD_FAST                'indexed'
              914  LOAD_FAST                'Permission'
              917  CALL_FUNCTION_2       2  '2 positional, 0 named'
              920  STORE_FAST               'permissions'

 L. 370       923  LOAD_FAST                'solicitation'
              926  LOAD_ATTR                permissions
              929  LOAD_CONST               None
              932  COMPARE_OP               is-not
              935  POP_JUMP_IF_FALSE   962  'to 962'
              938  LOAD_GLOBAL              chain
              941  LOAD_FAST                'solicitation'
              944  LOAD_ATTR                permissions
              947  LOAD_FAST                'permissions'
              950  CALL_FUNCTION_2       2  '2 positional, 0 named'
              953  LOAD_FAST                'solicitation'
              956  STORE_ATTR               permissions
              959  JUMP_FORWARD        971  'to 971'
              962  ELSE                     '971'

 L. 371       962  LOAD_FAST                'permissions'
              965  LOAD_FAST                'solicitation'
              968  STORE_ATTR               permissions
            971_0  COME_FROM           959  '959'
              971  LOAD_CONST               None
              974  RETURN_VALUE     

Parse error at or near `JUMP_FORWARD' instruction at offset 625

    def iterPermissions(self, indexed, Permission):
        """
        Iterates the permissions for the provided indexed structure.
        """
        for indexedMethod, indexedServices in indexed.items():
            for indexedCalls in indexedServices.values():
                for indexInvokers, filters in indexedCalls.values():
                    for node, invoker in indexInvokers.items():
                        yield Permission(method=indexedMethod, path=pathForNode(node), invoker=invoker, filters=list(filters.values()))