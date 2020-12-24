# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/acl/core/impl/processor/resource_alternate.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 28, 2013\n\n@package: support acl\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProcessor that creates alternate Gateway objects for resources that are not allowed. The purpose of this is to facilitate\nthe client side implementation since they can use the same resources but the gateway will automatically provide a filtered\nresource that is allowed by permissions.\n'
from acl.right_sevice import Alternate
from acl.support.core.util_resources import processPath
from ally.api.operator.type import TypeModel
from ally.api.type import typeFor
from ally.container import wire
from ally.container.ioc import injected
from ally.container.support import setup
from ally.core.impl.invoker import InvokerCall
from ally.core.spec.resources import Node, Path, INodeChildListener, INodeInvokerListener, Invoker
from ally.design.processor.attribute import requires, definesIf, optional
from ally.design.processor.context import Context
from ally.design.processor.handler import HandlerProcessorProceed, Handler
from ally.http.spec.server import IEncoderPath
from ally.support.core.util_resources import propertyTypesOf, iterateNodes, METHOD_NODE_ATTRIBUTE, invokerCallOf, pathForNode
from collections import Iterable
import logging
log = logging.getLogger(__name__)

class PermissionResource(Context):
    """
    The permission context.
    """
    navigate = definesIf(str, doc='\n    @rtype: string\n    The permission navigation.\n    ')
    method = requires(int)
    path = requires(Path)
    invoker = requires(Invoker)
    filters = requires(list)
    values = requires(dict)


class Solicitation(Context):
    """
    The solicitation context.
    """
    encoderPath = optional(IEncoderPath)
    permissions = requires(Iterable)


@injected
@setup(Handler, name='alternateNavigationPermissions')
class AlternateNavigationPermissions(HandlerProcessorProceed, INodeChildListener, INodeInvokerListener):
    """
    Provides the handler that creates alternate gateways based on resource permissions.
    """
    resourcesRoot = Node
    wire.entity('resourcesRoot')
    alternate = Alternate
    wire.entity('alternate')

    def __init__(self):
        assert isinstance(self.resourcesRoot, Node), 'Invalid root node %s' % self.resourcesRoot
        assert isinstance(self.alternate, Alternate), 'Invalid alternate repository %s' % self.alternate
        super().__init__()
        self._alternates = None
        self.resourcesRoot.addStructureListener(self)
        return

    def process(self, Permission: PermissionResource, solicitation: Solicitation, **keyargs):
        """
        @see: HandlerProcessorProceed.process
        
        Construct the alternate gateways for permissions.
        """
        assert issubclass(Permission, PermissionResource), 'Invalid permission class %s' % Permission
        assert isinstance(solicitation, Solicitation), 'Invalid solicitation %s' % solicitation
        assert isinstance(solicitation.permissions, Iterable), 'Invalid permissions %s' % solicitation.permissions
        if Solicitation.encoderPath in solicitation:
            encoder = solicitation.encoderPath
        else:
            encoder = None
        solicitation.permissions = self.processPermissions(solicitation.permissions, Permission, encoder)
        return

    def onChildAdded(self, node, child):
        """
        @see: INodeChildListener.onChildAdded
        """
        self._alternates = None
        return

    def onInvokerChange(self, node, old, new):
        """
        @see: INodeInvokerListener.onInvokerChange
        """
        self._alternates = None
        return

    def processPermissions(self, permissions, Permission, encoder):
        """
        Process the permissions alternate navigation.
        
        @param encoder: IEncoderPath|None
            The encoder path to be used for the gateways resource paths and patterns.
        """
        for permission in permissions:
            assert isinstance(permission, PermissionResource), 'Invalid permission %s' % permission
            yield permission
            if not permission.values:
                continue
            assert isinstance(permission.path, Path), 'Invalid path %s' % permission.path
            alternates = self.alternates().get((permission.path.node, permission.invoker))
            if not alternates:
                continue
            for node, invoker, required in alternates:
                assert isinstance(required, set)
                if required.issubset(permission.values):
                    permissionAlt = Permission()
                    assert isinstance(permissionAlt, PermissionResource)
                    permissionAlt.method = permission.method
                    permissionAlt.path = pathForNode(node)
                    permissionAlt.invoker = invoker
                    permissionAlt.filters = permission.filters
                    permissionAlt.values = permission.values
                    if PermissionResource.navigate in permissionAlt:
                        assert isinstance(encoder, IEncoderPath), 'Invalid encoder path %s' % encoder
                        path, _types = processPath(permission.path, permission.invoker, encoder, permission.values)
                        permissionAlt.navigate = path
                    yield permissionAlt
                    continue

    def alternates--- This code section failed: ---

 L. 161         0  LOAD_FAST                'self'
                3  LOAD_ATTR                _alternates
                6  LOAD_CONST               None
                9  COMPARE_OP               is
               12  POP_JUMP_IF_FALSE   991  'to 991'

 L. 162        15  BUILD_MAP_0           0  ''
               18  LOAD_FAST                'self'
               21  STORE_ATTR               _alternates

 L. 163        24  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               27  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'

 L. 164        30  LOAD_FAST                'self'
               33  LOAD_ATTR                alternate
               36  LOAD_ATTR                iterate
               39  CALL_FUNCTION_0       0  '0 positional, 0 named'
               42  GET_ITER         
               43  CALL_FUNCTION_1       1  '1 positional, 0 named'
               46  STORE_FAST               'alternatesRepository'

 L. 166        49  BUILD_LIST_0          0 
               52  STORE_FAST               'keys'

 L. 167        55  SETUP_LOOP          156  'to 156'
               58  LOAD_GLOBAL              iterateNodes
               61  LOAD_FAST                'self'
               64  LOAD_ATTR                resourcesRoot
               67  CALL_FUNCTION_1       1  '1 positional, 0 named'
               70  GET_ITER         
               71  FOR_ITER            155  'to 155'
               74  STORE_FAST               'node'

 L. 168        77  SETUP_LOOP          152  'to 152'
               80  LOAD_GLOBAL              METHOD_NODE_ATTRIBUTE
               83  LOAD_ATTR                items
               86  CALL_FUNCTION_0       0  '0 positional, 0 named'
               89  GET_ITER         
               90  FOR_ITER            151  'to 151'
               93  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               '_method'
               99  STORE_FAST               'attr'

 L. 169       102  LOAD_GLOBAL              getattr
              105  LOAD_FAST                'node'
              108  LOAD_FAST                'attr'
              111  CALL_FUNCTION_2       2  '2 positional, 0 named'
              114  STORE_FAST               'invoker'

 L. 170       117  LOAD_FAST                'invoker'
              120  POP_JUMP_IF_TRUE    129  'to 129'
              123  CONTINUE             90  'to 90'
              126  JUMP_FORWARD        129  'to 129'
            129_0  COME_FROM           126  '126'

 L. 172       129  LOAD_FAST                'keys'
              132  LOAD_ATTR                append
              135  LOAD_FAST                'node'
              138  LOAD_FAST                'invoker'
              141  BUILD_TUPLE_2         2 
              144  CALL_FUNCTION_1       1  '1 positional, 0 named'
              147  POP_TOP          
              148  JUMP_BACK            90  'to 90'
              151  POP_BLOCK        
            152_0  COME_FROM_LOOP       77  '77'
              152  JUMP_BACK            71  'to 71'
              155  POP_BLOCK        
            156_0  COME_FROM_LOOP       55  '55'

 L. 175       156  BUILD_MAP_0           0  ''
              159  BUILD_MAP_0           0  ''
              162  ROT_TWO          
              163  STORE_FAST               'pathTypesByKey'
              166  STORE_FAST               'modelTypesByKey'

 L. 176       169  SETUP_LOOP          891  'to 891'
              172  LOAD_FAST                'keys'
              175  GET_ITER         
              176  FOR_ITER            890  'to 890'
              179  STORE_FAST               'key'

 L. 177       182  LOAD_FAST                'key'
              185  UNPACK_SEQUENCE_2     2 
              188  STORE_FAST               'node'
              191  STORE_FAST               'invoker'

 L. 178       194  LOAD_GLOBAL              isinstance
              197  LOAD_FAST                'node'
              200  LOAD_GLOBAL              Node
              203  CALL_FUNCTION_2       2  '2 positional, 0 named'
              206  POP_JUMP_IF_TRUE    225  'to 225'
              209  LOAD_ASSERT              AssertionError
              212  LOAD_STR                 'Invalid node %s'
              215  LOAD_FAST                'node'
              218  BINARY_MODULO    
              219  CALL_FUNCTION_1       1  '1 positional, 0 named'
              222  RAISE_VARARGS_1       1  ''
            225_0  COME_FROM           206  '206'

 L. 179       225  LOAD_GLOBAL              isinstance
              228  LOAD_FAST                'invoker'
              231  LOAD_GLOBAL              Invoker
              234  CALL_FUNCTION_2       2  '2 positional, 0 named'
              237  POP_JUMP_IF_TRUE    256  'to 256'
              240  LOAD_ASSERT              AssertionError
              243  LOAD_STR                 'Invalid invoker %s'
              246  LOAD_FAST                'invoker'
              249  BINARY_MODULO    
              250  CALL_FUNCTION_1       1  '1 positional, 0 named'
              253  RAISE_VARARGS_1       1  ''
            256_0  COME_FROM           237  '237'

 L. 181       256  SETUP_LOOP          887  'to 887'
              259  LOAD_FAST                'keys'
              262  GET_ITER         
              263  FOR_ITER            886  'to 886'
              266  STORE_FAST               'keyAlt'

 L. 182       269  LOAD_FAST                'keyAlt'
              272  UNPACK_SEQUENCE_2     2 
              275  STORE_FAST               'nodeAlt'
              278  STORE_FAST               'invokerAlt'

 L. 183       281  LOAD_GLOBAL              isinstance
              284  LOAD_FAST                'nodeAlt'
              287  LOAD_GLOBAL              Node
              290  CALL_FUNCTION_2       2  '2 positional, 0 named'
              293  POP_JUMP_IF_TRUE    312  'to 312'
              296  LOAD_ASSERT              AssertionError
              299  LOAD_STR                 'Invalid node %s'
              302  LOAD_FAST                'nodeAlt'
              305  BINARY_MODULO    
              306  CALL_FUNCTION_1       1  '1 positional, 0 named'
              309  RAISE_VARARGS_1       1  ''
            312_0  COME_FROM           293  '293'

 L. 184       312  LOAD_GLOBAL              isinstance
              315  LOAD_FAST                'invokerAlt'
              318  LOAD_GLOBAL              Invoker
              321  CALL_FUNCTION_2       2  '2 positional, 0 named'
              324  POP_JUMP_IF_TRUE    343  'to 343'
              327  LOAD_ASSERT              AssertionError
              330  LOAD_STR                 'Invalid invoker %s'
              333  LOAD_FAST                'invokerAlt'
              336  BINARY_MODULO    
              337  CALL_FUNCTION_1       1  '1 positional, 0 named'
              340  RAISE_VARARGS_1       1  ''
            343_0  COME_FROM           324  '324'

 L. 186       343  LOAD_FAST                'node'
              346  LOAD_FAST                'nodeAlt'
              349  COMPARE_OP               ==
              352  POP_JUMP_IF_FALSE   361  'to 361'
              355  CONTINUE            263  'to 263'
              358  JUMP_FORWARD        361  'to 361'
            361_0  COME_FROM           358  '358'

 L. 187       361  LOAD_FAST                'invoker'
              364  LOAD_FAST                'invokerAlt'
              367  COMPARE_OP               !=
              370  POP_JUMP_IF_FALSE   424  'to 424'

 L. 188       373  LOAD_FAST                'invoker'
              376  LOAD_ATTR                method
              379  LOAD_FAST                'invokerAlt'
              382  LOAD_ATTR                method
              385  COMPARE_OP               !=
              388  POP_JUMP_IF_FALSE   397  'to 397'
              391  CONTINUE            263  'to 263'
              394  JUMP_FORWARD        397  'to 397'
            397_0  COME_FROM           394  '394'

 L. 189       397  LOAD_FAST                'invoker'
              400  LOAD_ATTR                output
              403  LOAD_FAST                'invokerAlt'
              406  LOAD_ATTR                output
              409  COMPARE_OP               !=
              412  POP_JUMP_IF_FALSE   424  'to 424'
              415  JUMP_BACK           263  'to 263'
              418  JUMP_ABSOLUTE       424  'to 424'
              421  JUMP_FORWARD        424  'to 424'
            424_0  COME_FROM           421  '421'

 L. 191       424  LOAD_FAST                'modelTypesByKey'
              427  LOAD_ATTR                get
              430  LOAD_FAST                'key'
              433  CALL_FUNCTION_1       1  '1 positional, 0 named'
              436  STORE_FAST               'modelTypes'

 L. 192       439  LOAD_FAST                'modelTypes'
              442  LOAD_CONST               None
              445  COMPARE_OP               is
              448  POP_JUMP_IF_FALSE   483  'to 483'

 L. 193       451  LOAD_LISTCOMP            '<code_object <listcomp>>'
              454  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              457  LOAD_FAST                'invoker'
              460  LOAD_ATTR                inputs
              463  GET_ITER         
              464  CALL_FUNCTION_1       1  '1 positional, 0 named'
              467  STORE_FAST               'modelTypes'

 L. 194       470  LOAD_FAST                'modelTypes'
              473  LOAD_FAST                'modelTypesByKey'
              476  LOAD_FAST                'key'
              479  STORE_SUBSCR     
              480  JUMP_FORWARD        483  'to 483'
            483_0  COME_FROM           480  '480'

 L. 196       483  LOAD_FAST                'modelTypesByKey'
              486  LOAD_ATTR                get
              489  LOAD_FAST                'keyAlt'
              492  CALL_FUNCTION_1       1  '1 positional, 0 named'
              495  STORE_FAST               'modelTypesAlt'

 L. 197       498  LOAD_FAST                'modelTypesAlt'
              501  LOAD_CONST               None
              504  COMPARE_OP               is
              507  POP_JUMP_IF_FALSE   542  'to 542'

 L. 198       510  LOAD_LISTCOMP            '<code_object <listcomp>>'
              513  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              516  LOAD_FAST                'invokerAlt'
              519  LOAD_ATTR                inputs
              522  GET_ITER         
              523  CALL_FUNCTION_1       1  '1 positional, 0 named'
              526  STORE_FAST               'modelTypesAlt'

 L. 199       529  LOAD_FAST                'modelTypesAlt'
              532  LOAD_FAST                'modelTypesByKey'
              535  LOAD_FAST                'keyAlt'
              538  STORE_SUBSCR     
              539  JUMP_FORWARD        542  'to 542'
            542_0  COME_FROM           539  '539'

 L. 201       542  LOAD_FAST                'modelTypes'
              545  LOAD_FAST                'modelTypesAlt'
              548  COMPARE_OP               !=
              551  POP_JUMP_IF_FALSE   560  'to 560'
              554  CONTINUE            263  'to 263'
              557  JUMP_FORWARD        560  'to 560'
            560_0  COME_FROM           557  '557'

 L. 203       560  LOAD_FAST                'pathTypesByKey'
              563  LOAD_ATTR                get
              566  LOAD_FAST                'key'
              569  CALL_FUNCTION_1       1  '1 positional, 0 named'
              572  STORE_FAST               'pathTypes'

 L. 204       575  LOAD_FAST                'pathTypes'
              578  LOAD_CONST               None
              581  COMPARE_OP               is
              584  POP_JUMP_IF_FALSE   613  'to 613'
              587  LOAD_GLOBAL              propertyTypesOf
              590  LOAD_FAST                'node'
              593  LOAD_FAST                'invoker'
              596  CALL_FUNCTION_2       2  '2 positional, 0 named'
              599  DUP_TOP          
              600  STORE_FAST               'pathTypes'
              603  LOAD_FAST                'pathTypesByKey'
              606  LOAD_FAST                'key'
              609  STORE_SUBSCR     
              610  JUMP_FORWARD        613  'to 613'
            613_0  COME_FROM           610  '610'

 L. 205       613  LOAD_FAST                'pathTypesByKey'
              616  LOAD_ATTR                get
              619  LOAD_FAST                'keyAlt'
              622  CALL_FUNCTION_1       1  '1 positional, 0 named'
              625  STORE_FAST               'pathTypesAlt'

 L. 206       628  LOAD_FAST                'pathTypesAlt'
              631  LOAD_CONST               None
              634  COMPARE_OP               is
              637  POP_JUMP_IF_FALSE   666  'to 666'
              640  LOAD_GLOBAL              propertyTypesOf
              643  LOAD_FAST                'nodeAlt'
              646  LOAD_FAST                'invokerAlt'
              649  CALL_FUNCTION_2       2  '2 positional, 0 named'
              652  DUP_TOP          
              653  STORE_FAST               'pathTypesAlt'
              656  LOAD_FAST                'pathTypesByKey'
              659  LOAD_FAST                'keyAlt'
              662  STORE_SUBSCR     
              663  JUMP_FORWARD        666  'to 666'
            666_0  COME_FROM           663  '663'

 L. 208       666  LOAD_GLOBAL              set
              669  LOAD_FAST                'pathTypes'
              672  CALL_FUNCTION_1       1  '1 positional, 0 named'
              675  STORE_FAST               'required'

 L. 209       678  SETUP_LOOP          744  'to 744'
              681  LOAD_FAST                'pathTypesAlt'
              684  GET_ITER         
              685  FOR_ITER            743  'to 743'
              688  STORE_FAST               'pathType'

 L. 210       691  SETUP_EXCEPT        711  'to 711'
              694  LOAD_FAST                'required'
              697  LOAD_ATTR                remove
              700  LOAD_FAST                'pathType'
              703  CALL_FUNCTION_1       1  '1 positional, 0 named'
              706  POP_TOP          
              707  POP_BLOCK        
              708  JUMP_BACK           685  'to 685'
            711_0  COME_FROM_EXCEPT    691  '691'

 L. 211       711  DUP_TOP          
              712  LOAD_GLOBAL              KeyError
              715  COMPARE_OP               exception-match
              718  POP_JUMP_IF_FALSE   739  'to 739'
              721  POP_TOP          
              722  POP_TOP          
              723  POP_TOP          

 L. 212       724  LOAD_FAST                'required'
              727  LOAD_ATTR                clear
              730  CALL_FUNCTION_0       0  '0 positional, 0 named'
              733  POP_TOP          

 L. 213       734  BREAK_LOOP       
              735  POP_EXCEPT       
              736  JUMP_BACK           685  'to 685'
              739  END_FINALLY      
              740  JUMP_BACK           685  'to 685'
              743  POP_BLOCK        
            744_0  COME_FROM_LOOP      678  '678'

 L. 214       744  LOAD_FAST                'required'
              747  POP_JUMP_IF_TRUE    756  'to 756'
              750  CONTINUE            263  'to 263'
              753  JUMP_FORWARD        756  'to 756'
            756_0  COME_FROM           753  '753'

 L. 217       756  LOAD_FAST                'self'
              759  LOAD_ATTR                processWithRepository
              762  LOAD_FAST                'alternatesRepository'
              765  LOAD_FAST                'invoker'
              768  LOAD_FAST                'invokerAlt'
              771  CALL_FUNCTION_3       3  '3 positional, 0 named'
              774  POP_JUMP_IF_FALSE   263  'to 263'

 L. 218       777  LOAD_FAST                'self'
              780  LOAD_ATTR                _alternates
              783  LOAD_ATTR                get
              786  LOAD_FAST                'key'
              789  CALL_FUNCTION_1       1  '1 positional, 0 named'
              792  STORE_FAST               'alternates'

 L. 219       795  LOAD_FAST                'alternates'
              798  LOAD_CONST               None
              801  COMPARE_OP               is
              804  POP_JUMP_IF_FALSE   827  'to 827'
              807  BUILD_LIST_0          0 
              810  DUP_TOP          
              811  STORE_FAST               'alternates'
              814  LOAD_FAST                'self'
              817  LOAD_ATTR                _alternates
              820  LOAD_FAST                'key'
              823  STORE_SUBSCR     
              824  JUMP_FORWARD        827  'to 827'
            827_0  COME_FROM           824  '824'

 L. 220       827  LOAD_FAST                'alternates'
              830  LOAD_ATTR                append
              833  LOAD_FAST                'keyAlt'
              836  LOAD_FAST                'required'
              839  BUILD_TUPLE_1         1 
              842  BINARY_ADD       
              843  CALL_FUNCTION_1       1  '1 positional, 0 named'
              846  POP_TOP          

 L. 221       847  LOAD_GLOBAL              log
              850  LOAD_ATTR                debug
              853  LOAD_STR                 'Added alternate on %s for %s'
              856  LOAD_FAST                'invoker'
              859  LOAD_FAST                'invokerAlt'
              862  CALL_FUNCTION_3       3  '3 positional, 0 named'
              865  POP_JUMP_IF_TRUE    883  'to 883'
              868  LOAD_CONST               True
              871  POP_JUMP_IF_TRUE    883  'to 883'
              874  LOAD_GLOBAL              AssertionError
              877  RAISE_VARARGS_1       1  ''
            880_0  COME_FROM           871  '871'
            880_1  COME_FROM           865  '865'
              880  CONTINUE            263  'to 263'
              883  JUMP_BACK           263  'to 263'
              886  POP_BLOCK        
            887_0  COME_FROM_LOOP      256  '256'
              887  JUMP_BACK           176  'to 176'
              890  POP_BLOCK        
            891_0  COME_FROM_LOOP      169  '169'

 L. 223       891  SETUP_LOOP          991  'to 991'
              894  LOAD_FAST                'alternatesRepository'
              897  LOAD_ATTR                items
              900  CALL_FUNCTION_0       0  '0 positional, 0 named'
              903  GET_ITER         
              904  FOR_ITER            987  'to 987'
              907  UNPACK_SEQUENCE_2     2 
              910  STORE_FAST               'serviceCall'
              913  STORE_FAST               'alternates'

 L. 224       916  LOAD_FAST                'alternates'
              919  POP_JUMP_IF_FALSE   904  'to 904'

 L. 225       922  LOAD_GENEXPR             '<code_object <genexpr>>'
              925  MAKE_FUNCTION_0          '0 positional, 0 keyword only, 0 annotated'
              928  LOAD_FAST                'alternates'
              931  GET_ITER         
              932  CALL_FUNCTION_1       1  '1 positional, 0 named'
              935  STORE_FAST               'alternates'

 L. 226       938  LOAD_FAST                'serviceCall'
              941  UNPACK_SEQUENCE_2     2 
              944  STORE_FAST               'service'
              947  STORE_FAST               'call'

 L. 227       950  LOAD_GLOBAL              log
              953  LOAD_ATTR                error
              956  LOAD_STR                 'Invalid alternate configuration on %s for %s with:\n%s\n'
              959  LOAD_FAST                'service'
              962  LOAD_FAST                'call'
              965  LOAD_STR                 '\n'
              968  LOAD_ATTR                join
              971  LOAD_FAST                'alternates'
              974  CALL_FUNCTION_1       1  '1 positional, 0 named'
              977  CALL_FUNCTION_4       4  '4 positional, 0 named'
              980  POP_TOP          
              981  CONTINUE            904  'to 904'
              984  JUMP_BACK           904  'to 904'
              987  POP_BLOCK        
            988_0  COME_FROM_LOOP      891  '891'
              988  JUMP_FORWARD        991  'to 991'
            991_0  COME_FROM           988  '988'

 L. 229       991  LOAD_FAST                'self'
              994  LOAD_ATTR                _alternates
              997  RETURN_VALUE     

Parse error at or near `JUMP_FORWARD' instruction at offset 421

    def processWithRepository(self, alternatesRepository, invoker, invokerAlt):
        """
        Process the invoker and alternate invoker against the alternates repository.
        
        @return: boolean
            True if the invoker and alternate invoker are configured in the repository.
        """
        assert isinstance(alternatesRepository, dict), 'Invalid alternates repository %s' % alternatesRepository
        if invoker == invokerAlt:
            return True
        invokerCall, invokerCallAlt = invokerCallOf(invoker), invokerCallOf(invokerAlt)
        if not invoker or not invokerCallAlt:
            return False
        else:
            assert isinstance(invokerCall, InvokerCall)
            assert isinstance(invokerCallAlt, InvokerCall)
            alternates = alternatesRepository.get((typeFor(invokerCallAlt.implementation), invokerCallAlt.call))
            if alternates is None:
                return False
            try:
                alternates.remove((typeFor(invokerCall.implementation), invokerCall.call))
            except KeyError:
                return False

            return True