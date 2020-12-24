# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/rpc/kernels.py
# Compiled at: 2011-08-30 23:33:15
import os, time, pyopencl
from pyopencl import mem_flags as mf
import numpy as np
GPU_ENGINE = 0
CPU_ENGINE = 1
MEMFLAGS = mf.READ_WRITE | mf.COPY_HOST_PTR
from weakref import WeakValueDictionary

class Engine(object):

    def __init__(self, engine, autoflatten=True):
        self.ctx = pyopencl.Context([pyopencl.get_platforms()[0].get_devices()[engine]])
        self.queue = pyopencl.CommandQueue(self.ctx)
        self.context = WeakValueDictionary()
        self.context_meta = {}
        self.buffers = {}
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.runtime = 0.0
        self.autoflatten = autoflatten

    def build(self, source):
        binary = pyopencl.Program(self.ctx, source)
        program = binary.build(options=['-w'])
        return program

    def purgeBuffers(self):
        """Purges mapped buffers if the Numpy array has been garbage collected"""
        for key in self.buffers.keys():
            if key not in self.context:
                del self.buffers[key]

        for key in self.context_meta.keys():
            if key not in self.context:
                del self.context_meta[key]

    def findBuffer(self, arg, metadata):
        """Finds or allocates an appropriately mapped buffer"""
        self.purgeBuffers()
        argid = id(arg)
        dirflag, param = metadata
        living = self.context.get(argid, None)
        if living is None:
            buf = pyopencl.Buffer(self.ctx, dirflag, hostbuf=self.viewof(arg))
            self.context[argid] = arg
            self.buffers[argid] = buf
            self.context_meta[argid] = metadata
            self.misses += 1
        else:
            buf = self.buffers[argid]
            arg = self.viewof(arg)
            if param[0] != 'resident':
                pyopencl.enqueue_copy(self.queue, buf, arg).wait()
            self.hits += 1
        return buf

    def viewof(self, arg):
        assert hasattr(arg, 'dtype')
        if self.autoflatten and len(arg.shape) > 1:
            tmparg = arg.view()
            tmparg.shape = (arg.size,)
        else:
            tmparg = arg
        return tmparg

    def write(self, arg):
        assert hasattr(arg, 'dtype')
        param = ('resident', arg.dtype, True)
        buf = self.findBuffer(arg, (MEMFLAGS, param))
        arg = self.viewof(arg)
        pyopencl.enqueue_copy(self.queue, buf, arg).wait()
        return buf

    def read(self, arg):
        assert self.context.has_key(id(arg))
        param = ('resident', arg.dtype, True)
        buf = self.findBuffer(arg, (MEMFLAGS, param))
        tmparg = self.viewof(arg)
        pyopencl.enqueue_copy(self.queue, tmparg, buf).wait()
        del tmparg
        return arg


engines = {CPU_ENGINE: Engine(CPU_ENGINE), GPU_ENGINE: Engine(GPU_ENGINE)}

def getEngine(engine):
    """Takes the identifier for an OpenCL engine (CPU_ENGINE, GPU_ENGINE)
    and returns a Engine with buffer management ."""
    return engines[engine]


from mako.template import Template
from mako.lookup import TemplateLookup

def findFile(dirs, subdirs, filename):
    for d in dirs:
        for sd in subdirs:
            pth = os.path.join(d, sd, filename)
            if os.path.exists(pth):
                return pth

    return


directories = [
 '.', 'rpc', 'interfaces']

def renderProgram(filename, **context):
    """
    Takes the basename of a mako template file, and uses context to generate an OpenCL program
    """
    filename += '.mako'
    tfilename = findFile([os.getcwd(), os.path.abspath(os.path.dirname(__file__))], [
     '.', 'rpc', 'interfaces'], filename)
    if not tfilename:
        raise Exception("Can't find template '%s'" % filename)
    mylookup = TemplateLookup(directories=[os.path.dirname(tfilename)])
    t = Template(filename=tfilename, lookup=mylookup)
    return str(t.render(**context))


def renderInterface(source, **context):
    """
    Takes the source for a mako definition of a yapocis.rpc interface and generates
    a parsable definition. Useful when the template can generate multiple parameterized
    routines.
    """
    t = Template(source)
    return str(t.render(**context))


class Kernel:
    """
    Provide a callable interface to an OpenCL kernel function.
    """

    def __init__(self, program, kernel, params, engine):
        self.program = program
        self.kernel = kernel
        self.params = params
        self.ctx = engine.ctx
        self.queue = engine.queue
        self.autoflatten = engine.autoflatten

    def prepareArgs--- This code section failed: ---

 L. 143         0  BUILD_LIST_0          0 
                3  LOAD_FAST             0  'self'
                6  STORE_ATTR            0  'returns'

 L. 144         9  BUILD_LIST_0          0 
               12  STORE_FAST            2  'pargs'

 L. 145        15  LOAD_CONST               0
               18  STORE_FAST            3  'iarg'

 L. 146        21  BUILD_MAP_0           0  None
               24  STORE_FAST            4  'paramdict'

 L. 147        27  LOAD_CONST               0
               30  STORE_FAST            5  'iparam'

 L. 148        33  SETUP_LOOP           76  'to 112'
               36  LOAD_FAST             0  'self'
               39  LOAD_ATTR             1  'params'
               42  GET_ITER         
               43  FOR_ITER             65  'to 111'
               46  UNPACK_SEQUENCE_4     4 
               49  STORE_FAST            6  'bufferHint'
               52  STORE_FAST            7  'dtype'
               55  STORE_FAST            8  'isbuffer'
               58  STORE_FAST            9  'name'

 L. 149        61  LOAD_FAST             6  'bufferHint'
               64  LOAD_CONST               ('outlike', 'sizeof', 'widthof', 'heightof')
               67  COMPARE_OP            7  not-in
               70  POP_JUMP_IF_FALSE    43  'to 43'

 L. 150        73  LOAD_FAST             5  'iparam'
               76  LOAD_FAST             6  'bufferHint'
               79  LOAD_FAST             7  'dtype'
               82  LOAD_FAST             8  'isbuffer'
               85  BUILD_TUPLE_4         4 
               88  LOAD_FAST             4  'paramdict'
               91  LOAD_FAST             9  'name'
               94  STORE_SUBSCR     

 L. 151        95  LOAD_FAST             5  'iparam'
               98  LOAD_CONST               1
              101  INPLACE_ADD      
              102  STORE_FAST            5  'iparam'
              105  JUMP_BACK            43  'to 43'
              108  JUMP_BACK            43  'to 43'
              111  POP_BLOCK        
            112_0  COME_FROM            33  '33'

 L. 152       112  LOAD_GLOBAL           2  'len'
              115  LOAD_FAST             1  'args'
              118  CALL_FUNCTION_1       1  None
              121  LOAD_GLOBAL           2  'len'
              124  LOAD_FAST             4  'paramdict'
              127  CALL_FUNCTION_1       1  None
              130  COMPARE_OP            2  ==
              133  POP_JUMP_IF_TRUE    142  'to 142'
              136  LOAD_ASSERT              AssertionError
              139  RAISE_VARARGS_1       1  None

 L. 153       142  LOAD_CONST               0
              145  STORE_FAST            3  'iarg'

 L. 154       148  SETUP_LOOP          839  'to 990'
              151  LOAD_FAST             0  'self'
              154  LOAD_ATTR             1  'params'
              157  GET_ITER         
              158  FOR_ITER            828  'to 989'
              161  STORE_FAST           10  'param'

 L. 155       164  LOAD_FAST            10  'param'
              167  UNPACK_SEQUENCE_4     4 
              170  STORE_FAST            6  'bufferHint'
              173  STORE_FAST            7  'dtype'
              176  STORE_FAST            8  'isbuffer'
              179  STORE_FAST            9  'name'

 L. 156       182  LOAD_FAST             7  'dtype'
              185  POP_JUMP_IF_FALSE   206  'to 206'

 L. 157       188  LOAD_GLOBAL           4  'getattr'
              191  LOAD_GLOBAL           5  'np'
              194  LOAD_FAST             7  'dtype'
              197  CALL_FUNCTION_2       2  None
              200  STORE_FAST            7  'dtype'
              203  JUMP_FORWARD          6  'to 212'

 L. 159       206  LOAD_CONST               None
              209  STORE_FAST            7  'dtype'
            212_0  COME_FROM           203  '203'

 L. 162       212  LOAD_FAST             8  'isbuffer'
              215  POP_JUMP_IF_TRUE    281  'to 281'

 L. 163       218  LOAD_FAST             1  'args'
              221  LOAD_FAST             3  'iarg'
              224  BINARY_SUBSCR    
              225  STORE_FAST           11  'arg'

 L. 164       228  LOAD_FAST             3  'iarg'
              231  LOAD_CONST               1
              234  INPLACE_ADD      
              235  STORE_FAST            3  'iarg'

 L. 165       238  LOAD_FAST             7  'dtype'
              241  POP_JUMP_IF_TRUE    250  'to 250'
              244  LOAD_ASSERT              AssertionError
              247  RAISE_VARARGS_1       1  None

 L. 166       250  LOAD_FAST             7  'dtype'
              253  LOAD_FAST            11  'arg'
              256  CALL_FUNCTION_1       1  None
              259  STORE_FAST           12  'parg'

 L. 167       262  LOAD_FAST             2  'pargs'
              265  LOAD_ATTR             7  'append'
              268  LOAD_FAST            12  'parg'
              271  CALL_FUNCTION_1       1  None
              274  POP_TOP          

 L. 168       275  CONTINUE            158  'to 158'
              278  JUMP_FORWARD          0  'to 281'
            281_0  COME_FROM           278  '278'

 L. 169       281  LOAD_GLOBAL           8  'mf'
              284  LOAD_ATTR             9  'READ_WRITE'
              287  LOAD_GLOBAL           8  'mf'
              290  LOAD_ATTR            10  'COPY_HOST_PTR'
              293  BINARY_OR        
              294  STORE_FAST           13  'dirflag'

 L. 170       297  LOAD_CONST               None
              300  STORE_FAST           14  'buf'

 L. 171       303  LOAD_FAST             6  'bufferHint'
              306  LOAD_CONST               ('sizeof', 'widthof', 'heightof')
              309  COMPARE_OP            6  in
              312  POP_JUMP_IF_FALSE   550  'to 550'

 L. 172       315  LOAD_FAST             4  'paramdict'
              318  LOAD_FAST             9  'name'
              321  BINARY_SUBSCR    
              322  UNPACK_SEQUENCE_4     4 
              325  STORE_FAST            5  'iparam'
              328  STORE_FAST           15  '_'
              331  STORE_FAST           15  '_'
              334  STORE_FAST           15  '_'

 L. 173       337  LOAD_FAST             1  'args'
              340  LOAD_FAST             5  'iparam'
              343  BINARY_SUBSCR    
              344  STORE_FAST           11  'arg'

 L. 174       347  LOAD_FAST             7  'dtype'
              350  POP_JUMP_IF_TRUE    365  'to 365'

 L. 175       353  LOAD_GLOBAL           5  'np'
              356  LOAD_ATTR            11  'int32'
              359  STORE_FAST            7  'dtype'
              362  JUMP_FORWARD          0  'to 365'
            365_0  COME_FROM           362  '362'

 L. 176       365  LOAD_FAST            11  'arg'
              368  LOAD_ATTR            12  'size'
              371  LOAD_FAST            11  'arg'
              374  LOAD_ATTR            13  'shape'
              377  ROT_TWO          
              378  STORE_FAST           16  'size'
              381  STORE_FAST           17  'shape'

 L. 177       384  LOAD_GLOBAL           2  'len'
              387  LOAD_FAST            17  'shape'
              390  CALL_FUNCTION_1       1  None
              393  LOAD_CONST               1
              396  COMPARE_OP            2  ==
              399  POP_JUMP_IF_FALSE   423  'to 423'

 L. 178       402  LOAD_FAST             6  'bufferHint'
              405  LOAD_CONST               'sizeof'
              408  COMPARE_OP            2  ==
              411  POP_JUMP_IF_TRUE    423  'to 423'
              414  LOAD_ASSERT              AssertionError
              417  RAISE_VARARGS_1       1  None
              420  JUMP_FORWARD          0  'to 423'
            423_0  COME_FROM           420  '420'

 L. 179       423  LOAD_GLOBAL           2  'len'
              426  LOAD_FAST            17  'shape'
              429  CALL_FUNCTION_1       1  None
              432  LOAD_CONST               2
              435  COMPARE_OP            2  ==
              438  POP_JUMP_IF_FALSE   456  'to 456'

 L. 180       441  LOAD_FAST            17  'shape'
              444  UNPACK_SEQUENCE_2     2 
              447  STORE_FAST           18  'width'
              450  STORE_FAST           19  'height'
              453  JUMP_FORWARD          0  'to 456'
            456_0  COME_FROM           453  '453'

 L. 181       456  LOAD_FAST             6  'bufferHint'
              459  LOAD_CONST               'sizeof'
              462  COMPARE_OP            2  ==
              465  POP_JUMP_IF_FALSE   477  'to 477'

 L. 182       468  LOAD_FAST            16  'size'
              471  STORE_FAST           12  'parg'
              474  JUMP_FORWARD         42  'to 519'

 L. 183       477  LOAD_FAST             6  'bufferHint'
              480  LOAD_CONST               'widthof'
              483  COMPARE_OP            2  ==
              486  POP_JUMP_IF_FALSE   498  'to 498'

 L. 184       489  LOAD_FAST            18  'width'
              492  STORE_FAST           12  'parg'
              495  JUMP_FORWARD         21  'to 519'

 L. 185       498  LOAD_FAST             6  'bufferHint'
              501  LOAD_CONST               'heightof'
              504  COMPARE_OP            2  ==
              507  POP_JUMP_IF_FALSE   519  'to 519'

 L. 186       510  LOAD_FAST            19  'height'
              513  STORE_FAST           12  'parg'
              516  JUMP_FORWARD          0  'to 519'
            519_0  COME_FROM           516  '516'
            519_1  COME_FROM           495  '495'
            519_2  COME_FROM           474  '474'

 L. 187       519  LOAD_FAST             7  'dtype'
              522  LOAD_FAST            12  'parg'
              525  CALL_FUNCTION_1       1  None
              528  STORE_FAST           12  'parg'

 L. 188       531  LOAD_FAST             2  'pargs'
              534  LOAD_ATTR             7  'append'
              537  LOAD_FAST            12  'parg'
              540  CALL_FUNCTION_1       1  None
              543  POP_TOP          

 L. 189       544  CONTINUE            158  'to 158'
              547  JUMP_FORWARD        278  'to 828'

 L. 190       550  LOAD_FAST             6  'bufferHint'
              553  LOAD_CONST               'outlike'
              556  COMPARE_OP            2  ==
              559  POP_JUMP_IF_FALSE   636  'to 636'

 L. 191       562  LOAD_FAST             4  'paramdict'
              565  LOAD_FAST             9  'name'
              568  BINARY_SUBSCR    
              569  UNPACK_SEQUENCE_4     4 
              572  STORE_FAST            5  'iparam'
              575  STORE_FAST           15  '_'
              578  STORE_FAST           20  'oldtype'
              581  STORE_FAST           15  '_'

 L. 192       584  LOAD_FAST             7  'dtype'
              587  POP_JUMP_IF_TRUE    608  'to 608'

 L. 193       590  LOAD_GLOBAL           4  'getattr'
              593  LOAD_GLOBAL           5  'np'
              596  LOAD_FAST            20  'oldtype'
              599  CALL_FUNCTION_2       2  None
              602  STORE_FAST            7  'dtype'
              605  JUMP_FORWARD          0  'to 608'
            608_0  COME_FROM           605  '605'

 L. 194       608  LOAD_GLOBAL           5  'np'
              611  LOAD_ATTR            14  'zeros_like'
              614  LOAD_FAST             1  'args'
              617  LOAD_FAST             5  'iparam'
              620  BINARY_SUBSCR    
              621  LOAD_CONST               'dtype'
              624  LOAD_FAST             7  'dtype'
              627  CALL_FUNCTION_257   257  None
              630  STORE_FAST           12  'parg'
              633  JUMP_FORWARD        192  'to 828'

 L. 195       636  LOAD_FAST             6  'bufferHint'
              639  LOAD_CONST               'resident'
              642  COMPARE_OP            2  ==
              645  POP_JUMP_IF_FALSE   719  'to 719'

 L. 196       648  LOAD_FAST             1  'args'
              651  LOAD_FAST             3  'iarg'
              654  BINARY_SUBSCR    
              655  STORE_FAST           11  'arg'

 L. 197       658  LOAD_FAST            11  'arg'
              661  STORE_FAST           12  'parg'

 L. 198       664  LOAD_FAST             3  'iarg'
              667  LOAD_CONST               1
              670  INPLACE_ADD      
              671  STORE_FAST            3  'iarg'

 L. 199       674  LOAD_FAST             0  'self'
              677  LOAD_ATTR            15  'program'
              680  LOAD_ATTR            16  'findBuffer'
              683  LOAD_FAST            12  'parg'
              686  LOAD_FAST            13  'dirflag'
              689  LOAD_FAST            10  'param'
              692  BUILD_TUPLE_2         2 
              695  CALL_FUNCTION_2       2  None
              698  STORE_FAST           14  'buf'

 L. 200       701  LOAD_FAST            14  'buf'
              704  POP_JUMP_IF_TRUE    828  'to 828'
              707  LOAD_ASSERT              AssertionError
              710  LOAD_CONST               'Resident buffer is not present, array have gone out of scope'
              713  RAISE_VARARGS_2       2  None
              716  JUMP_FORWARD        109  'to 828'

 L. 201       719  LOAD_GLOBAL          17  'hasattr'
              722  LOAD_FAST             1  'args'
              725  LOAD_FAST             3  'iarg'
              728  BINARY_SUBSCR    
              729  LOAD_CONST               'dtype'
              732  CALL_FUNCTION_2       2  None
              735  UNARY_NOT        
              736  POP_JUMP_IF_TRUE    758  'to 758'
              739  LOAD_FAST             1  'args'
              742  LOAD_FAST             3  'iarg'
              745  BINARY_SUBSCR    
              746  LOAD_ATTR            18  'dtype'
              749  LOAD_FAST             7  'dtype'
              752  COMPARE_OP            3  !=
            755_0  COME_FROM           736  '736'
              755  POP_JUMP_IF_FALSE   802  'to 802'

 L. 202       758  LOAD_FAST             1  'args'
              761  LOAD_FAST             3  'iarg'
              764  BINARY_SUBSCR    
              765  STORE_FAST           11  'arg'

 L. 203       768  LOAD_GLOBAL           5  'np'
              771  LOAD_ATTR            19  'array'
              774  LOAD_FAST            11  'arg'
              777  LOAD_CONST               'dtype'
              780  LOAD_FAST             7  'dtype'
              783  CALL_FUNCTION_257   257  None
              786  STORE_FAST           12  'parg'

 L. 204       789  LOAD_FAST             3  'iarg'
              792  LOAD_CONST               1
              795  INPLACE_ADD      
              796  STORE_FAST            3  'iarg'
              799  JUMP_FORWARD         26  'to 828'

 L. 206       802  LOAD_FAST             1  'args'
              805  LOAD_FAST             3  'iarg'
              808  BINARY_SUBSCR    
              809  STORE_FAST           11  'arg'

 L. 207       812  LOAD_FAST            11  'arg'
              815  STORE_FAST           12  'parg'

 L. 208       818  LOAD_FAST             3  'iarg'
              821  LOAD_CONST               1
              824  INPLACE_ADD      
              825  STORE_FAST            3  'iarg'
            828_0  COME_FROM           799  '799'
            828_1  COME_FROM           716  '716'
            828_2  COME_FROM           633  '633'
            828_3  COME_FROM           547  '547'

 L. 210       828  LOAD_FAST             0  'self'
              831  LOAD_ATTR            20  'global_size'
              834  LOAD_CONST               None
              837  COMPARE_OP            8  is
              840  POP_JUMP_IF_FALSE   894  'to 894'
              843  LOAD_FAST             6  'bufferHint'
              846  LOAD_CONST               ('in', 'inout', 'resident')
              849  COMPARE_OP            6  in
            852_0  COME_FROM           840  '840'
              852  POP_JUMP_IF_FALSE   894  'to 894'

 L. 211       855  LOAD_FAST             0  'self'
              858  LOAD_ATTR            21  'autoflatten'
              861  POP_JUMP_IF_FALSE   879  'to 879'

 L. 212       864  LOAD_FAST            12  'parg'
              867  LOAD_ATTR            12  'size'
              870  LOAD_FAST             0  'self'
              873  STORE_ATTR           20  'global_size'
              876  JUMP_ABSOLUTE       894  'to 894'

 L. 214       879  LOAD_FAST            12  'parg'
              882  LOAD_ATTR            13  'shape'
              885  LOAD_FAST             0  'self'
              888  STORE_ATTR           20  'global_size'
              891  JUMP_FORWARD          0  'to 894'
            894_0  COME_FROM           891  '891'

 L. 215       894  LOAD_FAST            14  'buf'
              897  LOAD_CONST               None
              900  COMPARE_OP            8  is
              903  POP_JUMP_IF_FALSE   936  'to 936'

 L. 216       906  LOAD_FAST             0  'self'
              909  LOAD_ATTR            15  'program'
              912  LOAD_ATTR            16  'findBuffer'
              915  LOAD_FAST            12  'parg'
              918  LOAD_FAST            13  'dirflag'
              921  LOAD_FAST            10  'param'
              924  BUILD_TUPLE_2         2 
              927  CALL_FUNCTION_2       2  None
              930  STORE_FAST           14  'buf'
              933  JUMP_FORWARD          0  'to 936'
            936_0  COME_FROM           933  '933'

 L. 217       936  LOAD_FAST             6  'bufferHint'
              939  LOAD_CONST               ('out', 'inout', 'outlike')
              942  COMPARE_OP            6  in
              945  POP_JUMP_IF_FALSE   973  'to 973'

 L. 218       948  LOAD_FAST             0  'self'
              951  LOAD_ATTR             0  'returns'
              954  LOAD_ATTR             7  'append'
              957  LOAD_FAST            12  'parg'
              960  LOAD_FAST            14  'buf'
              963  BUILD_TUPLE_2         2 
              966  CALL_FUNCTION_1       1  None
              969  POP_TOP          
              970  JUMP_FORWARD          0  'to 973'
            973_0  COME_FROM           970  '970'

 L. 219       973  LOAD_FAST             2  'pargs'
              976  LOAD_ATTR             7  'append'
              979  LOAD_FAST            14  'buf'
              982  CALL_FUNCTION_1       1  None
              985  POP_TOP          
              986  JUMP_BACK           158  'to 158'
              989  POP_BLOCK        
            990_0  COME_FROM           148  '148'

 L. 220       990  LOAD_FAST             2  'pargs'
              993  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 989

    def __call__(self, *args, **kwargs):
        """Call a kernel, prepare arguments, and track performance"""
        self.program.calls += 1
        t = time.time()
        self.global_size = kwargs.pop('global_size', None)
        self.local_size = kwargs.pop('local_size', None)
        args = self.prepareArgs(args)
        if not isinstance(self.global_size, (tuple, list)):
            self.global_size = (
             self.global_size,)
        self.evt = self.kernel(self.queue, self.global_size, self.local_size, *args)
        self.evt.wait()
        rval = self.prepareReturn()
        self.program.runtime += time.time() - t
        return rval

    def prepareReturn(self):
        """Takes the return value buffers (out and outlike) and prepares proper Numpy arrays"""
        rvals = []
        for arg, buf in self.returns:
            pyopencl.enqueue_copy(self.queue, self.program.viewof(arg), buf).wait()
            rvals.append(arg)

        self.returns = []
        if len(rvals) == 0:
            return None
        else:
            if len(rvals) == 1:
                return rvals[0]
            return tuple(rvals)


class Program:
    """
    Takes a parsed yapocis interface and returns a class/module like structure
    which supports calling into kernel methods of the interface.
    Manages buffers on the OpenCL device to prevent over-allocation.
    """

    def __init__(self, interface, engine, debug=False, **context):
        source = renderProgram(interface.interfacename, **context)
        self.source = source
        if debug:
            print 'Source'
            print source
        mf = pyopencl.mem_flags
        self.engine = getEngine(engine)
        interface.program = self.engine.build(source)
        self.callable = {}
        self.context = self.engine.context
        self.context_meta = self.engine.context_meta
        self.ctx = self.engine.ctx
        self.queue = self.engine.queue
        self.buffers = self.engine.buffers
        self.interface = interface
        program = interface.program
        self.hits = 0
        self.misses = 0
        self.calls = 0
        self.runtime = 0.0
        for kernel in interface.kernels():
            alias = interface.kernelalias(kernel)
            self.callable[kernel] = Kernel(self, getattr(program, alias), interface.kernelparams(kernel), self.engine)

    def __getattr__(self, attr):
        """Any unbound attribute is checked to see if it is a callable"""
        if attr not in self.callable:
            print 'Kernel %s not found, %s available' % (attr, self.callable.keys())
            raise KeyError, attr
        return self.callable[attr]

    def purgeBuffers(self):
        self.engine.purgeBuffers()

    def findBuffer(self, *args):
        return self.engine.findBuffer(*args)

    def read(self, *args):
        return self.engine.read(*args)

    def write(self, *args):
        return self.engine.write(*args)

    def viewof(self, *args):
        return self.engine.viewof(*args)

    def stats(self):
        return dict(calls=self.calls, hits=self.hits, misses=self.misses, buffers=len(self.buffers), runtime=self.runtime)

    def __str__(self):
        self.purgeBuffers()
        return '%s calls:%s hits:%s misses:%s cached:%s time:%s' % (self.interface.interfacename, self.calls, self.hits, self.misses, len(self.buffers), self.runtime)


from interfacecl_parser import getInterfaceCL

def loadProgram(source, engine=CPU_ENGINE, debug=False, **context):
    """
    Primary interface for yapocis.rpc
    Factory returning runnable interface based on a interface specification.
    """
    source = renderInterface(source, **context)
    interface = getInterfaceCL(source)
    interface.source = source
    if debug:
        print 'Interface', interface
    return Program(interface, engine, debug=debug, **context)


from interfaces import *

def test_compiling--- This code section failed: ---

 L. 320         0  LOAD_CONST               6202013264865897877
                3  LOAD_CONST               -8119117248955560468
                6  LOAD_CONST               7139354972159999745
                9  LOAD_CONST               -682776529868236564
               12  LOAD_CONST               1403331523463003145
               15  LOAD_CONST               -7762762614049038277
               18  LOAD_CONST               8451406568839298774
               21  BUILD_LIST_7          7 
               24  STORE_FAST            0  'sourcehashes'

 L. 321        27  LOAD_CONST               6402197007761216735
               30  LOAD_CONST               -110486948446408996
               33  LOAD_CONST               5834752055632543161
               36  LOAD_CONST               -9192547793151607825
               39  LOAD_CONST               6003157927413075666
               42  LOAD_CONST               1424139564779745970
               45  LOAD_CONST               4108900838076230702
               48  BUILD_LIST_7          7 
               51  STORE_FAST            1  'interfacehashes'

 L. 322        54  LOAD_CONST               'Interface search path'
               57  PRINT_ITEM       
               58  LOAD_GLOBAL           0  'directories'
               61  PRINT_ITEM_CONT  
               62  PRINT_NEWLINE_CONT

 L. 323        63  LOAD_GLOBAL           1  'convolve'
               66  LOAD_GLOBAL           2  'dict'
               69  LOAD_CONST               'name'
               72  LOAD_CONST               'convolve'
               75  LOAD_CONST               'conv'
               78  LOAD_CONST               1
               81  LOAD_CONST               2
               84  LOAD_CONST               3
               87  LOAD_CONST               4
               90  LOAD_CONST               3
               93  LOAD_CONST               2
               96  LOAD_CONST               1
               99  BUILD_LIST_7          7 
              102  CALL_FUNCTION_512   512  None
              105  BUILD_TUPLE_2         2 

 L. 324       108  LOAD_GLOBAL           3  'median3x3'
              111  LOAD_GLOBAL           2  'dict'
              114  LOAD_CONST               'steps'
              117  LOAD_CONST               9
              120  BUILD_LIST_1          1 
              123  LOAD_CONST               'width'
              126  LOAD_CONST               9
              129  CALL_FUNCTION_512   512  None
              132  BUILD_TUPLE_2         2 

 L. 325       135  LOAD_GLOBAL           4  'gradient'
              138  BUILD_MAP_0           0  None
              141  BUILD_TUPLE_2         2 

 L. 326       144  LOAD_GLOBAL           5  'hsi'
              147  BUILD_MAP_0           0  None
              150  BUILD_TUPLE_2         2 

 L. 327       153  LOAD_GLOBAL           6  'convolves'
              156  LOAD_GLOBAL           2  'dict'
              159  LOAD_CONST               'convs'
              162  LOAD_CONST               'boxone'
              165  LOAD_CONST               1
              168  LOAD_CONST               1
              171  LOAD_CONST               1
              174  BUILD_LIST_3          3 
              177  BUILD_TUPLE_2         2 
              180  LOAD_CONST               'triangle'
              183  LOAD_CONST               0.5
              186  LOAD_CONST               1
              189  LOAD_CONST               0.5
              192  BUILD_LIST_3          3 
              195  BUILD_TUPLE_2         2 
              198  BUILD_LIST_2          2 
              201  CALL_FUNCTION_256   256  None
              204  BUILD_TUPLE_2         2 

 L. 328       207  LOAD_GLOBAL           7  'mandelbrot'
              210  BUILD_MAP_0           0  None
              213  BUILD_TUPLE_2         2 

 L. 329       216  LOAD_GLOBAL           8  'demo'
              219  BUILD_MAP_0           0  None
              222  BUILD_TUPLE_2         2 
              225  BUILD_LIST_7          7 
              228  STORE_FAST            2  'interfaces'

 L. 331       231  SETUP_LOOP          283  'to 517'
              234  LOAD_GLOBAL           9  'enumerate'
              237  LOAD_FAST             2  'interfaces'
              240  CALL_FUNCTION_1       1  None
              243  GET_ITER         
              244  FOR_ITER            269  'to 516'
              247  UNPACK_SEQUENCE_2     2 
              250  STORE_FAST            3  'itest'
              253  UNPACK_SEQUENCE_2     2 
              256  STORE_FAST            4  'interface'
              259  STORE_FAST            5  'context'

 L. 332       262  LOAD_GLOBAL          10  'loadProgram'
              265  LOAD_FAST             4  'interface'
              268  LOAD_CONST               'engine'
              271  LOAD_GLOBAL          11  'GPU_ENGINE'
              274  LOAD_CONST               'debug'
              277  LOAD_GLOBAL          12  'True'
              280  LOAD_FAST             5  'context'
              283  CALL_FUNCTION_KW_513   513  None
              286  STORE_FAST            6  'program'

 L. 333       289  LOAD_FAST             1  'interfacehashes'
              292  LOAD_FAST             3  'itest'
              295  BINARY_SUBSCR    
              296  LOAD_GLOBAL          13  'hash'
              299  LOAD_FAST             6  'program'
              302  LOAD_ATTR            14  'interface'
              305  LOAD_ATTR            15  'source'
              308  CALL_FUNCTION_1       1  None
              311  COMPARE_OP            2  ==
              314  POP_JUMP_IF_TRUE    344  'to 344'
              317  LOAD_ASSERT              AssertionError
              320  LOAD_FAST             4  'interface'
              323  LOAD_GLOBAL          13  'hash'
              326  LOAD_FAST             6  'program'
              329  LOAD_ATTR            14  'interface'
              332  LOAD_ATTR            15  'source'
              335  CALL_FUNCTION_1       1  None
              338  BUILD_TUPLE_2         2 
              341  RAISE_VARARGS_2       2  None

 L. 334       344  LOAD_FAST             0  'sourcehashes'
              347  LOAD_FAST             3  'itest'
              350  BINARY_SUBSCR    
              351  LOAD_GLOBAL          13  'hash'
              354  LOAD_FAST             6  'program'
              357  LOAD_ATTR            15  'source'
              360  CALL_FUNCTION_1       1  None
              363  COMPARE_OP            2  ==
              366  POP_JUMP_IF_TRUE    387  'to 387'
              369  LOAD_ASSERT              AssertionError
              372  LOAD_GLOBAL          13  'hash'
              375  LOAD_FAST             6  'program'
              378  LOAD_ATTR            15  'source'
              381  CALL_FUNCTION_1       1  None
              384  RAISE_VARARGS_2       2  None

 L. 335       387  LOAD_CONST               'Interface'
              390  PRINT_ITEM       
              391  LOAD_FAST             6  'program'
              394  LOAD_ATTR            14  'interface'
              397  LOAD_ATTR            17  'interfacename'
              400  PRINT_ITEM_CONT  
              401  PRINT_NEWLINE_CONT

 L. 336       402  SETUP_LOOP          107  'to 512'
              405  LOAD_FAST             6  'program'
              408  LOAD_ATTR            14  'interface'
              411  LOAD_ATTR            18  'kernels'
              414  CALL_FUNCTION_0       0  None
              417  GET_ITER         
              418  FOR_ITER             90  'to 511'
              421  STORE_FAST            7  'kernel'

 L. 337       424  LOAD_CONST               'Kernel'
              427  PRINT_ITEM       
              428  LOAD_FAST             7  'kernel'
              431  PRINT_ITEM_CONT  
              432  PRINT_NEWLINE_CONT

 L. 338       433  LOAD_CONST               'Params'
              436  PRINT_ITEM       
              437  LOAD_FAST             6  'program'
              440  LOAD_ATTR            14  'interface'
              443  LOAD_ATTR            19  'kernelparams'
              446  LOAD_FAST             7  'kernel'
              449  CALL_FUNCTION_1       1  None
              452  PRINT_ITEM_CONT  
              453  PRINT_NEWLINE_CONT

 L. 339       454  LOAD_CONST               'OpenCL entry'
              457  PRINT_ITEM       
              458  LOAD_GLOBAL          20  'getattr'
              461  LOAD_FAST             6  'program'
              464  LOAD_ATTR            14  'interface'
              467  LOAD_ATTR            21  'program'
              470  LOAD_FAST             6  'program'
              473  LOAD_ATTR            14  'interface'
              476  LOAD_ATTR            22  'kernelalias'
              479  LOAD_FAST             7  'kernel'
              482  CALL_FUNCTION_1       1  None
              485  CALL_FUNCTION_2       2  None
              488  PRINT_ITEM_CONT  
              489  PRINT_NEWLINE_CONT

 L. 340       490  LOAD_CONST               'Callable'
              493  PRINT_ITEM       
              494  LOAD_GLOBAL          20  'getattr'
              497  LOAD_FAST             6  'program'
              500  LOAD_FAST             7  'kernel'
              503  CALL_FUNCTION_2       2  None
              506  PRINT_ITEM_CONT  
              507  PRINT_NEWLINE_CONT
              508  JUMP_BACK           418  'to 418'
              511  POP_BLOCK        
            512_0  COME_FROM           402  '402'

 L. 341       512  PRINT_NEWLINE    
              513  JUMP_BACK           244  'to 244'
              516  POP_BLOCK        
            517_0  COME_FROM           231  '231'

Parse error at or near `POP_BLOCK' instruction at offset 516


def test_context():
    engine = getEngine(GPU_ENGINE)
    a = np.random.sample((100, )).astype(np.float32)
    b = a.copy()
    engine.write(a)
    a[:] = 0
    engine.read(a)
    diff = np.abs(a - b).sum()
    assert diff == 0.0
    del a
    try:
        engine.read(b)
        print 'Did not fail on unmapped array'
    except AssertionError:
        pass

    assert (engine.hits, engine.misses) == (1, 1)


if __name__ == '__main__':
    test_compiling()
    test_context()
    print 'All is well'