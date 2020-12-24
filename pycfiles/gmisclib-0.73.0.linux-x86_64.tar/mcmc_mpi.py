# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_mpi.py
# Compiled at: 2011-05-11 15:13:41
"""This is a helper module to make use of mcmc.py and mcmc_big.py.
It allows you to conveniently run a Monte-Carlo simulation of any
kind until it converges (L{stepper.run_to_bottom}) or until it
has explored a large chunk of parameter space (L{stepper.run_to_ergodic}).

It also helps you with logging the process.

When run in parallel, each processor does its thing more-or-less
independently.   However, every few steps, they exchange notes on
their current progress.   If one finds an improved vertex, it will be
passed on to other processors via MPI.
"""
import sys, mpi, random, numpy
from gmisclib import die
from gmisclib import mcmc
from gmisclib import mcmc_helper as MCH
Debug = 0
from gmisclib.mcmc_helper import TooManyLoops, warnevery, logger_template, test
from gmisclib.mcmc_helper import step_acceptor, make_stepper_from_lov

class stepper(MCH.stepper):

    def __init__(self, x, maxloops=-1, logger=None, share=None):
        die.info('# mpi stepper rank=%d size=%d' % (rank(), size()))
        assert maxloops == -1
        MCH.stepper.__init__(self, x, maxloops, logger)

    def reset_loops(self, maxloops=-1):
        assert maxloops == -1
        MCH.stepper.reset_loops(self, maxloops)

    def communicate_hook--- This code section failed: ---

 L.  41         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'note'
                6  LOAD_CONST               'chook iter=%d'
                9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             1  'iter'
               15  BINARY_MODULO    
               16  LOAD_CONST               4
               19  CALL_FUNCTION_2       2  None
               22  POP_TOP          

 L.  42        23  LOAD_GLOBAL           2  'size'
               26  CALL_FUNCTION_0       0  None
               29  LOAD_CONST               1
               32  COMPARE_OP            4  >
               35  POP_JUMP_IF_FALSE   541  'to 541'

 L.  43        38  LOAD_FAST             0  'self'
               41  LOAD_ATTR             0  'note'
               44  LOAD_CONST               'chook active iter=%d'
               47  LOAD_FAST             0  'self'
               50  LOAD_ATTR             1  'iter'
               53  BINARY_MODULO    
               54  LOAD_CONST               3
               57  CALL_FUNCTION_2       2  None
               60  POP_TOP          

 L.  44        61  LOAD_GLOBAL           3  'mpi'
               64  LOAD_ATTR             4  'irecv'
               67  LOAD_CONST               'tag'
               70  LOAD_FAST             0  'self'
               73  LOAD_ATTR             5  'MPIID'
               76  CALL_FUNCTION_256   256  None
               79  STORE_FAST            2  'handle'

 L.  45        82  LOAD_FAST             0  'self'
               85  LOAD_ATTR             6  'x'
               88  LOAD_ATTR             7  'current'
               91  CALL_FUNCTION_0       0  None
               94  STORE_FAST            3  'c'

 L.  46        97  LOAD_FAST             3  'c'
              100  LOAD_ATTR             8  'vec'
              103  CALL_FUNCTION_0       0  None
              106  STORE_FAST            4  'v'

 L.  47       109  LOAD_FAST             3  'c'
              112  LOAD_ATTR             9  'logp'
              115  CALL_FUNCTION_0       0  None
              118  STORE_FAST            5  'lp'

 L.  48       121  LOAD_GLOBAL           3  'mpi'
              124  LOAD_ATTR            10  'send'
              127  LOAD_FAST             4  'v'
              130  LOAD_FAST             5  'lp'
              133  LOAD_FAST             1  'id'
              136  BUILD_TUPLE_3         3 
              139  LOAD_GLOBAL           3  'mpi'
              142  LOAD_ATTR            11  'rank'
              145  LOAD_CONST               1
              148  BINARY_ADD       
              149  LOAD_GLOBAL           3  'mpi'
              152  LOAD_ATTR             2  'size'
              155  BINARY_MODULO    
              156  LOAD_CONST               'tag'
              159  LOAD_FAST             0  'self'
              162  LOAD_ATTR             5  'MPIID'
              165  CALL_FUNCTION_258   258  None
              168  POP_TOP          

 L.  49       169  LOAD_FAST             2  'handle'
              172  LOAD_ATTR            12  'wait'
              175  CALL_FUNCTION_0       0  None
              178  POP_TOP          

 L.  50       179  LOAD_FAST             2  'handle'
              182  LOAD_ATTR            13  'message'
              185  UNPACK_SEQUENCE_3     3 
              188  STORE_FAST            6  'nv'
              191  STORE_FAST            7  'nlp'
              194  STORE_FAST            8  'nid'

 L.  51       197  LOAD_FAST             8  'nid'
              200  LOAD_FAST             1  'id'
              203  COMPARE_OP            2  ==
              206  POP_JUMP_IF_TRUE    228  'to 228'
              209  LOAD_ASSERT              AssertionError
              212  LOAD_CONST               'ID mismatch: %d/%d or %s/%s'
              215  LOAD_FAST             1  'id'
              218  LOAD_FAST             8  'nid'
              221  BUILD_TUPLE_2         2 
              224  BINARY_MODULO    
              225  RAISE_VARARGS_2       2  None

 L.  53       228  LOAD_GLOBAL          11  'rank'
              231  CALL_FUNCTION_0       0  None
              234  STORE_FAST            9  'r'

 L.  54       237  LOAD_GLOBAL           2  'size'
              240  CALL_FUNCTION_0       0  None
              243  STORE_FAST           10  's'

 L.  55       246  LOAD_FAST             0  'self'
              249  LOAD_ATTR             0  'note'
              252  LOAD_CONST               'sendrecv from %d to %d'
              255  LOAD_FAST             9  'r'
              258  LOAD_FAST             9  'r'
              261  LOAD_CONST               1
              264  BINARY_ADD       
              265  LOAD_FAST            10  's'
              268  BINARY_MODULO    
              269  BUILD_TUPLE_2         2 
              272  BINARY_MODULO    
              273  LOAD_CONST               5
              276  CALL_FUNCTION_2       2  None
              279  POP_TOP          

 L.  56       280  LOAD_GLOBAL           3  'mpi'
              283  LOAD_ATTR            15  'sendrecv'
              286  LOAD_CONST               'sendobj'
              289  LOAD_FAST             4  'v'
              292  LOAD_FAST             5  'lp'
              295  LOAD_FAST             1  'id'
              298  BUILD_TUPLE_3         3 
              301  LOAD_CONST               'dest'

 L.  57       304  LOAD_FAST             9  'r'
              307  LOAD_CONST               1
              310  BINARY_ADD       
              311  LOAD_FAST            10  's'
              314  BINARY_MODULO    
              315  LOAD_CONST               'sendtag'
              318  LOAD_FAST             0  'self'
              321  LOAD_ATTR             5  'MPIID'
              324  LOAD_CONST               'source'

 L.  58       327  LOAD_FAST             9  'r'
              330  LOAD_FAST            10  's'
              333  BINARY_ADD       
              334  LOAD_CONST               1
              337  BINARY_SUBTRACT  
              338  LOAD_FAST            10  's'
              341  BINARY_MODULO    
              342  LOAD_CONST               'recvtag'

 L.  59       345  LOAD_FAST             0  'self'
              348  LOAD_ATTR             5  'MPIID'
              351  CALL_FUNCTION_1280  1280  None
              354  UNPACK_SEQUENCE_3     3 
              357  STORE_FAST            6  'nv'
              360  STORE_FAST            7  'nlp'
              363  STORE_FAST            8  'nid'

 L.  62       366  LOAD_FAST             0  'self'
              369  LOAD_ATTR             0  'note'
              372  LOAD_CONST               'communicate succeeded from %s'
              375  LOAD_FAST             8  'nid'
              378  BINARY_MODULO    
              379  LOAD_CONST               1
              382  CALL_FUNCTION_2       2  None
              385  POP_TOP          

 L.  63       386  LOAD_FAST             7  'nlp'
              389  LOAD_FAST             5  'lp'
              392  BINARY_SUBTRACT  
              393  STORE_FAST           11  'delta'

 L.  64       396  LOAD_FAST             0  'self'
              399  LOAD_ATTR             6  'x'
              402  LOAD_ATTR            16  'acceptable'
              405  LOAD_FAST            11  'delta'
              408  CALL_FUNCTION_1       1  None
              411  POP_JUMP_IF_FALSE   474  'to 474'

 L.  65       414  LOAD_FAST             0  'self'
              417  LOAD_ATTR             6  'x'
              420  LOAD_ATTR            17  '_set_current'
              423  LOAD_FAST             3  'c'
              426  LOAD_ATTR            18  'new'
              429  LOAD_FAST             6  'nv'
              432  LOAD_FAST             4  'v'
              435  BINARY_SUBTRACT  
              436  LOAD_CONST               'logp'
              439  LOAD_FAST             7  'nlp'
              442  CALL_FUNCTION_257   257  None
              445  CALL_FUNCTION_1       1  None
              448  STORE_FAST           12  'q'

 L.  66       451  LOAD_FAST             0  'self'
              454  LOAD_ATTR             0  'note'
              457  LOAD_CONST               'communicate accepted: %s'
              460  LOAD_FAST            12  'q'
              463  BINARY_MODULO    
              464  LOAD_CONST               1
              467  CALL_FUNCTION_2       2  None
              470  POP_TOP          
              471  JUMP_FORWARD         51  'to 525'

 L.  68       474  LOAD_FAST             0  'self'
              477  LOAD_ATTR             0  'note'
              480  LOAD_CONST               'communicate not accepted %g vs %g'
              483  LOAD_FAST             7  'nlp'
              486  LOAD_FAST             5  'lp'
              489  BUILD_TUPLE_2         2 
              492  BINARY_MODULO    
              493  LOAD_CONST               1
              496  CALL_FUNCTION_2       2  None
              499  POP_TOP          

 L.  69       500  LOAD_FAST             0  'self'
              503  LOAD_ATTR             6  'x'
              506  LOAD_ATTR            17  '_set_current'
              509  LOAD_FAST             0  'self'
              512  LOAD_ATTR             6  'x'
              515  LOAD_ATTR             7  'current'
              518  CALL_FUNCTION_0       0  None
              521  CALL_FUNCTION_1       1  None
              524  POP_TOP          
            525_0  COME_FROM           471  '471'

 L.  70       525  LOAD_GLOBAL          19  'sys'
              528  LOAD_ATTR            20  'stdout'
              531  LOAD_ATTR            21  'flush'
              534  CALL_FUNCTION_0       0  None
              537  POP_TOP          
              538  JUMP_FORWARD          0  'to 541'
            541_0  COME_FROM           538  '538'

Parse error at or near `JUMP_FORWARD' instruction at offset 538

    MPIID = 1241

    def _nc_get_hook(self, nc):
        self.note('_nye pre', 5)
        ncsum = mpi.allreduce(float(nc), mpi.SUM)
        self.note('_nye post', 5)
        return ncsum / float(size())

    def _not_at_bottom(self, xchanged, nchg, es, dotchanged, ndot):
        mytmp = numpy.sometrue(numpy.less(xchanged, nchg)) or es < 1.0 or dotchanged < ndot or self.x.acceptable.T() > 1.5
        self.note('_nab pre', 5)
        ntrue = mpi.allreduce(int(mytmp), mpi.SUM)
        self.note('_nab post', 5)
        return ntrue * 4 >= mpi.size

    def synchronize_start(self, id):
        self.synchronize('start ' + id)

    def synchronize_end(self, id):
        self.synchronize('end ' + id)

    def synchronize_abort(self, id):
        raise RuntimeError, 'MPI cannot handle an abort.'

    def synchronize(self, id):
        self.note('pre join %s' % id, 5)
        rootid = mpi.bcast(id)
        assert rootid == id
        self.note('post join %s' % id, 5)

    def note(self, s, lvl):
        if Debug >= lvl:
            sys.stderr.writelines('# %s, rank=%d\n' % (s, rank()))
            sys.stderr.flush()

    def size(self):
        return mpi.Get_size()

    def rank(self):
        return mpi.Get_rank()


def precompute_logp(lop):
    """Does a parallel evaluation of logp for all items in lop.
        """
    nper = len(lop) // mpi.size
    r = rank()
    mychunk = lop[r * nper:(r + 1) * nper]
    for p in mychunk:
        q = p.logp()
        print 'logp=', q, 'for rank', r

    for r in range(size()):
        nc = mpi.bcast(mychunk, r)
        lop[(r * nper):((r + 1) * nper)] = nc

    mpi.barrier()


def test():

    def test_logp(x, c):
        return -(x[0] - x[1] ** 2) ** 2 + 0.001 * x[1] ** 2

    x = mcmc.bootstepper(test_logp, numpy.array([0.0, 2.0]), numpy.array([[1.0, 0], [0, 2.0]]))
    print 'TEST: rank=', rank()
    thr = stepper(x)
    for i in range(2):
        print 'RTC'
        thr.run_to_change(2)
        print 'RTE'
        thr.run_to_ergodic(1.0)
        print 'DONE'

    thr.close()


if __name__ == '__main__':
    test()