# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\arrayjob.py
# Compiled at: 2013-01-14 06:47:43
"""
Simple wrapper for PBS array jobs. See test_arrayjob.py for a working example.

Usage:

#. Import the arrayjob module, usually with ``from utils.arrayjob import *``
#. Set the number of tasks that are going to split the work.
#. Define one function per stage of computation.
#. Call ``arun(stage0, par(stage1), ...)`` where ``par()`` marks stages to run 
   in parallel.

The arrayjob module senses which mode it is running in, by examining the 
environment variables PBS_ARRAYID and STAGE_ID.

* Regular execution: arun() will submit one job per stage.
* Serial job: single instance will execute stage STAGE_ID.
* Parallel job: parallel instances will execute stage STAGE_ID.

If STAGE_ID is not set, the script is executing for the first time, and 
arun() will submit a batch job for each stage, with dependencies between stages.
Parallel stages use the PBS "array job" facility. Also, Stallo won't put 
multiple jobs on the same node. We work around this by using MPI without 
actually passing any messages, just -lnodes=1:ppn=8 and running with mpirun.

If PBS_ARRAYID exists, the variable ID is set to ``PBS_ARRAYID * size + rank``, 
where size and rank are taken from MPI (if OMPI_COMM_WORLD_RANK exists), 
otherwise size, rank = 1, 0.

Example:

>>> from cgp.utils.arrayjob import *
>>> set_NID(16)                                                 # doctest: +SKIP

Next, define one function per stage of computation.
Finally, specify the sequence of stages, and which of them should run in 
parallel (as an "array job").

>>> arun(stage0, par(stage1), ...)                              # doctest: +SKIP

Importing ``* from arrayjob`` defines the following:

* :func:`arun` : Run a multi-stage job, 
  submitting parallel stages as array jobs.
* :func:`presub` : Indicate that first stage should run on login node 
  rather than batch.
* :func:`par` : Indicate that a stage should execute in parallel.
* :data:`ID` : Array job index ID (in the sequence 0, 1, ..., NID-1).
* :func:`get_NID` : Get the number of array jobs to submit, 
  or that have been submitted.
* :func:`set_NID` : Set number of array jobs to submit. 
  You should call set_NID() exactly once.
* :func:`qopt` : Decorator to pass job parameters for an individual stage
* :data:`alog` : Logger object for the arrayjob module.
* :func:`wait` : Do-nothing stage used to separate parallel stages if required.
* :func:`memmap_chunk` : Read-write memmap to chunk ID out of NID.

Calling ``set_NID(n+1)`` is equivalent to::

    qsub -t 0-n <jobscript>

or the jobscript directive ::

    #PBS -t 0-n <jobscript>

(The :func:`reset_NID` below prepares for other doctests by forgetting 
that we have called :func:`set_NID`.)

>>> reset_NID()
"""
import sys, os
from os import environ as e
from cgp.utils.commands import getstatusoutput
import logging
from collections import defaultdict
import numpy as np
from cgp.utils.ordereddict import OrderedDict
from cgp.utils.rec2dict import dict2rec
from cgp.utils.dotdict import Dotdict
__all__ = ('arun presub par ID get_NID set_NID reset_NID\n             qopt alog wait memmap_chunk Mmapdict Timing').split()
ID = NID = ppn = rank = size = STAGE_ID = None
if 'STAGE_ID' in e:
    STAGE_ID = int(e['STAGE_ID'])
if 'PBS_ARRAYID' in e:
    AID = int(e['PBS_ARRAYID'])
    if 'OMPI_COMM_WORLD_RANK' in e:
        from mpi4py import MPI
        size = MPI.COMM_WORLD.Get_size()
        rank = MPI.COMM_WORLD.Get_rank()
    else:
        size, rank = (1, 0)
    ID = int(AID) * size + rank
keys = 'asctime levelname name lineno process message'
fmt = '%(' + (')s\t%(').join(keys.split()) + ')s'
logging.basicConfig(level=logging.INFO, format=fmt)
alog = logging.getLogger('arrayjob')
jobscript = os.path.realpath(sys.argv[0])

class QsubException(Exception):
    """Exception in queue submission."""

    def __init__(self, status, output, cmd):
        super(QsubException, self).__init__()
        self.status = status
        self.output = output
        self.cmd = cmd

    def __str__(self):
        classname = self.__class__.__name__
        return '%s%s' % (classname, (self.status, self.output, self.cmd))


def set_NID--- This code section failed: ---

 L. 143         0  LOAD_FAST             1  'n'
                3  STORE_GLOBAL          0  'ppn'

 L. 144         6  LOAD_GLOBAL           1  'NID'
                9  LOAD_CONST               None
               12  COMPARE_OP            8  is
               15  POP_JUMP_IF_TRUE     27  'to 27'
               18  LOAD_ASSERT              AssertionError
               21  LOAD_CONST               'Attempting to call set_NID() more than once'
               24  RAISE_VARARGS_2       2  None

 L. 145        27  LOAD_CONST               'NID (%s) must be an even multiple of # processors per node (%s)'
               30  STORE_FAST            2  'msg'

 L. 146        33  LOAD_FAST             0  'i'
               36  LOAD_GLOBAL           0  'ppn'
               39  BINARY_MODULO    
               40  LOAD_CONST               0
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     68  'to 68'
               49  LOAD_ASSERT              AssertionError
               52  LOAD_FAST             2  'msg'
               55  LOAD_FAST             0  'i'
               58  LOAD_GLOBAL           0  'ppn'
               61  BUILD_TUPLE_2         2 
               64  BINARY_MODULO    
               65  RAISE_VARARGS_2       2  None

 L. 147        68  LOAD_FAST             0  'i'
               71  STORE_GLOBAL          1  'NID'
               74  LOAD_CONST               None
               77  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 74


def reset_NID():
    """
    Reset NID to None, so ``assert NID is None`` does not fail when debugging.
    """
    global NID
    NID = None
    return


def get_NID():
    """Get the number of array jobs to submit, or that have been submitted."""
    return NID


class Qopt(defaultdict):
    """Dict to record queue options."""

    @staticmethod
    def key(func):
        """Return func, or its wrapped function if decorated."""
        if hasattr(func, '__func__'):
            return func.__func__
        return func

    def __getitem__(self, func):
        return super(Qopt, self).__getitem__(key(func))

    def __setitem__(self, func, value):
        super(Qopt, self).__setitem__(key(func), value)


opt = dict(par=set(), presub=set(), qopt=Qopt(list))

def par(func):
    """
    Indicate that a stage should execute in parallel.
    
    Wrapping a function in :func:`par` adds it to the set of functions that the 
    arrayjob module knows should be executed as array jobs.
    
    >>> def f(): pass
    >>> is_par(par(f))
    True
    
    It can be used as a decorator.
    
    >>> @par
    ... def h(): pass
    >>> is_par(h)
    True
    """
    opt['par'].add(key(func))
    return func


def is_par(func):
    """
    Return ``True`` if a function has been marked by par(stage).
    
    >>> def f(): pass
    >>> is_par(f)
    False
    >>> is_par(par(f))
    True
    """
    return key(func) in opt['par']


def presub(func):
    """
    Indicate that first stage should run on login node rather than as batch job.
    
    Cheap initialization can run on the login node without waiting in queue, 
    saving some time.
    
    Typical usage, assuming setup(), work() and wrapup() have been defined.
    
    >>> arun(presub(setup), par(work), wrapup)                  # doctest: +SKIP
    
    >>> def f(): pass
    >>> is_presub(presub(f))
    True
    
    It can be used as a decorator.
    
    >>> @presub
    ... def h(): pass
    >>> is_presub(h)
    True
    
    Instance methods are OK, whether bound or unbound.
    
    >>> class A(object):
    ...     @presub
    ...     def test(self):
    ...         pass
    >>> a = A()
    >>> is_presub(a.test)
    True
    >>> is_presub(A.test)
    True
    
    This example shows that presub(f) is executed immediately by arun.
    (Here, no jobs are submitted because there are no regular stages.)
    
    >>> set_NID(8)
    >>> def f():
    ...     print "Testing"
    >>> arun(presub(f))
    Testing
    >>> reset_NID() # undo effects of the doctest
    """
    opt['presub'].add(key(func))
    return func


def is_presub(func):
    """
    Return True if a function has been marked by presub(stage).
    
    >>> def f(): pass
    >>> is_presub(f)
    False
    >>> is_presub(presub(f))
    True
    """
    return key(func) in opt['presub']


def key(func):
    """
    Common basis for comparison of functions, bound and unbound methods.
    
    >>> class A(object):
    ...     def test():
    ...         pass
    >>> a = A()
    >>> a.test, A.test
    (<bound method A.test of <...A object at 0x...>>, 
     <unbound method A.test>)
    >>> key(a.test), key(A.test)
    (<function test at 0x...>, <function test at 0x...>)
    >>> a.test == A.test
    False
    >>> key(a.test) == key(A.test)
    True
    """
    if hasattr(func, '__func__'):
        return func.__func__
    return func


def qopt(*args):
    """
    Decorator to associate queueing options with a stage function.
    
    >>> @qopt("-l walltime=00:01:00", "-j oe")
    ... def f():
    ...     pass
    
    The options are stored internally in a list.
    
    >>> opt["qopt"][f]
    ['-l walltime=00:01:00', '-j oe']
    
    This works with any callable, including instance methods.
    
    >>> class A(object):
    ...     @qopt("-j oe")
    ...     def test(self):
    ...         pass
    >>> a = A()
    >>> opt["qopt"][key(a.test)]
    ['-j oe']
    
    Can be applied multiple times. The outermost option is added last.
    
    >>> @qopt("-j oe")
    ... @qopt("-l walltime=00:01:00")
    ... def g():
    ...     pass
    >>> opt["qopt"][g]
    ['-l walltime=00:01:00', '-j oe']
    """

    def wrapper(func):
        opt['qopt'][key(func)].extend(args)
        return func

    return wrapper


def wait():
    """Do nothing. Used to separate parallel stages if required."""
    pass


def array_opt(NID):
    """
    PBS array job option.
    
    >>> array_opt(3)
    '-t 0-2'
    """
    return '-t 0-%s' % (NID - 1)


def submit(STAGE_ID, *options):
    """
    Submit the jobscript as an array job, passing any *options to qsub.
    
    This is equivalent to running::
    
        qsub -v STAGE_ID=2 -t 0-2 -W depend=afterok:123 arrayjob.py
    
    >>> submit(2, array_opt(3), "-W depend=afterok:123")        # doctest: +SKIP
    
    submit() returns the job ID assigned by the queue system.
    """
    if any([ opt.startswith('-t') for opt in options ]):
        wrapper = 'qsubwrapmpi'
    else:
        wrapper = 'qsubwrap'
    options = (' ').join(options)
    cmd = '%s -v STAGE_ID=%s %s %s' % (wrapper, STAGE_ID, options, jobscript)
    status, output = getstatusoutput(cmd)
    result = output
    alog.info('Submitted (status, output, cmd): %s', (status, output, cmd))
    if status != 0:
        raise QsubException(status, output, cmd)
    return result.split('.', 1)[0]


def arun--- This code section failed: ---

 L. 427         0  LOAD_FAST             1  'kwargs'
                3  LOAD_ATTR             0  'pop'
                6  LOAD_CONST               'loglevel'
                9  LOAD_CONST               'INFO'
               12  CALL_FUNCTION_2       2  None
               15  STORE_FAST            2  'loglevel'

 L. 428        18  LOAD_GLOBAL           1  'alog'
               21  LOAD_ATTR             2  'setLevel'
               24  LOAD_GLOBAL           3  'getattr'
               27  LOAD_GLOBAL           4  'logging'
               30  LOAD_FAST             2  'loglevel'
               33  CALL_FUNCTION_2       2  None
               36  CALL_FUNCTION_1       1  None
               39  POP_TOP          

 L. 429        40  LOAD_GLOBAL           5  'os'
               43  LOAD_ATTR             6  'environ'
               46  LOAD_ATTR             7  'get'
               49  LOAD_CONST               'STAGE_ID'
               52  CALL_FUNCTION_1       1  None
               55  STORE_DEREF           0  'STAGE_ID'

 L. 431        58  LOAD_CLOSURE          0  'STAGE_ID'
               64  LOAD_CODE                <code_object run_presub>
               67  MAKE_CLOSURE_0        0  None
               70  STORE_FAST            3  'run_presub'

 L. 446        73  LOAD_FAST             1  'kwargs'
               76  LOAD_ATTR             0  'pop'
               79  LOAD_CONST               'testID'
               82  LOAD_CONST               None
               85  CALL_FUNCTION_2       2  None
               88  STORE_FAST            4  'testID'

 L. 447        91  LOAD_FAST             4  'testID'
               94  LOAD_CONST               None
               97  COMPARE_OP            9  is-not
              100  POP_JUMP_IF_FALSE   200  'to 200'

 L. 448       103  LOAD_GLOBAL           1  'alog'
              106  LOAD_ATTR             9  'info'
              109  LOAD_CONST               'Calling arun() with testID=%s'
              112  LOAD_FAST             4  'testID'
              115  CALL_FUNCTION_2       2  None
              118  POP_TOP          

 L. 449       119  LOAD_FAST             3  'run_presub'
              122  LOAD_FAST             0  'stages'
              125  CALL_FUNCTION_1       1  None
              128  STORE_FAST            0  'stages'

 L. 450       131  LOAD_FAST             4  'testID'
              134  STORE_GLOBAL         10  'ID'

 L. 451       137  SETUP_LOOP           56  'to 196'
              140  LOAD_GLOBAL          11  'range'
              143  LOAD_GLOBAL          12  'len'
              146  LOAD_FAST             0  'stages'
              149  CALL_FUNCTION_1       1  None
              152  CALL_FUNCTION_1       1  None
              155  GET_ITER         
              156  FOR_ITER             36  'to 195'
              159  STORE_DEREF           0  'STAGE_ID'

 L. 452       162  LOAD_GLOBAL          13  'str'
              165  LOAD_DEREF            0  'STAGE_ID'
              168  CALL_FUNCTION_1       1  None
              171  LOAD_GLOBAL           5  'os'
              174  LOAD_ATTR             6  'environ'
              177  LOAD_CONST               'STAGE_ID'
              180  STORE_SUBSCR     

 L. 453       181  LOAD_FAST             0  'stages'
              184  LOAD_DEREF            0  'STAGE_ID'
              187  BINARY_SUBSCR    
              188  CALL_FUNCTION_0       0  None
              191  POP_TOP          
              192  JUMP_BACK           156  'to 156'
              195  POP_BLOCK        
            196_0  COME_FROM           137  '137'

 L. 455       196  LOAD_CONST               None
              199  RETURN_VALUE     
            200_0  COME_FROM           100  '100'

 L. 457       200  LOAD_GLOBAL           1  'alog'
              203  LOAD_ATTR            14  'debug'
              206  LOAD_CONST               'ID=%s, STAGE_ID=%s'
              209  LOAD_GLOBAL          10  'ID'
              212  LOAD_DEREF            0  'STAGE_ID'
              215  CALL_FUNCTION_3       3  None
              218  POP_TOP          

 L. 458       219  LOAD_FAST             1  'kwargs'
              222  UNARY_NOT        
              223  POP_JUMP_IF_TRUE    239  'to 239'
              226  LOAD_ASSERT              AssertionError
              229  LOAD_CONST               'Undefined keyword arguments: %s'
              232  LOAD_FAST             1  'kwargs'
              235  BINARY_MODULO    
              236  RAISE_VARARGS_2       2  None

 L. 459       239  LOAD_GLOBAL          16  'NID'
              242  LOAD_CONST               None
              245  COMPARE_OP            9  is-not
              248  POP_JUMP_IF_TRUE    260  'to 260'
              251  LOAD_ASSERT              AssertionError
              254  LOAD_CONST               'Need to call set_NID() before arun()'
              257  RAISE_VARARGS_2       2  None

 L. 460       260  LOAD_FAST             3  'run_presub'
              263  LOAD_FAST             0  'stages'
              266  CALL_FUNCTION_1       1  None
              269  STORE_FAST            0  'stages'

 L. 462       272  LOAD_FAST             0  'stages'
              275  POP_JUMP_IF_TRUE    282  'to 282'

 L. 463       278  LOAD_CONST               None
              281  RETURN_END_IF    
            282_0  COME_FROM           275  '275'

 L. 464       282  LOAD_DEREF            0  'STAGE_ID'
              285  LOAD_CONST               None
              288  COMPARE_OP            8  is
              291  POP_JUMP_IF_FALSE   805  'to 805'

 L. 465       294  SETUP_LOOP          108  'to 405'
              297  LOAD_GLOBAL          17  'zip'
              300  LOAD_FAST             0  'stages'
              303  LOAD_FAST             0  'stages'
              306  LOAD_CONST               1
              309  SLICE+1          
              310  CALL_FUNCTION_2       2  None
              313  GET_ITER         
              314  FOR_ITER             87  'to 404'
              317  UNPACK_SEQUENCE_2     2 
              320  STORE_FAST            5  'this'
              323  STORE_FAST            6  'next_'

 L. 466       326  LOAD_GLOBAL          18  'is_par'
              329  LOAD_FAST             5  'this'
              332  CALL_FUNCTION_1       1  None
              335  POP_JUMP_IF_FALSE   314  'to 314'
              338  LOAD_GLOBAL          18  'is_par'
              341  LOAD_FAST             6  'next_'
              344  CALL_FUNCTION_1       1  None
            347_0  COME_FROM           335  '335'
              347  POP_JUMP_IF_FALSE   314  'to 314'

 L. 467       350  LOAD_CONST               'Consecutive stages %s and %s are both parallel.'
              353  STORE_FAST            7  'msg'

 L. 468       356  LOAD_FAST             7  'msg'
              359  LOAD_CONST               ' qsub dependencies cannot handle this case.'
              362  INPLACE_ADD      
              363  STORE_FAST            7  'msg'

 L. 469       366  LOAD_FAST             7  'msg'
              369  LOAD_CONST               ' Workaround: insert a serial arrayjob.wait.'
              372  INPLACE_ADD      
              373  STORE_FAST            7  'msg'

 L. 470       376  LOAD_GLOBAL          15  'AssertionError'
              379  LOAD_FAST             7  'msg'
              382  LOAD_FAST             5  'this'
              385  LOAD_FAST             6  'next_'
              388  BUILD_TUPLE_2         2 
              391  BINARY_MODULO    
              392  CALL_FUNCTION_1       1  None
              395  RAISE_VARARGS_1       1  None
              398  JUMP_BACK           314  'to 314'
              401  JUMP_BACK           314  'to 314'
              404  POP_BLOCK        
            405_0  COME_FROM           294  '294'

 L. 471       405  LOAD_CONST               '-W depend=on:%s'
              408  LOAD_GLOBAL          16  'NID'
              411  LOAD_GLOBAL          19  'ppn'
              414  BINARY_DIVIDE    
              415  BINARY_MODULO    
              416  STORE_FAST            8  'on_opt'

 L. 472       419  BUILD_MAP_0           0  None
              422  STORE_FAST            9  'jobid'

 L. 473       425  LOAD_GLOBAL          20  'defaultdict'
              428  LOAD_GLOBAL          21  'list'
              431  CALL_FUNCTION_1       1  None
              434  STORE_FAST           10  'jobdep'

 L. 475       437  LOAD_GLOBAL          22  'np'
              440  LOAD_ATTR            23  'array'
              443  BUILD_LIST_0          0 

 L. 476       446  LOAD_GLOBAL          24  'enumerate'
              449  LOAD_FAST             0  'stages'
              452  CALL_FUNCTION_1       1  None
              455  GET_ITER         
              456  FOR_ITER             44  'to 503'
              459  UNPACK_SEQUENCE_2     2 
              462  STORE_DEREF           0  'STAGE_ID'
              465  STORE_FAST           11  'stage'
              468  LOAD_DEREF            0  'STAGE_ID'
              471  LOAD_CONST               0
              474  COMPARE_OP            4  >
              477  JUMP_IF_FALSE_OR_POP   497  'to 497'
              480  LOAD_GLOBAL          18  'is_par'
              483  LOAD_FAST             0  'stages'
              486  LOAD_DEREF            0  'STAGE_ID'
              489  LOAD_CONST               1
              492  BINARY_SUBTRACT  
              493  BINARY_SUBSCR    
              494  CALL_FUNCTION_1       1  None
            497_0  COME_FROM           477  '477'
              497  LIST_APPEND           2  None
              500  JUMP_BACK           456  'to 456'
              503  CALL_FUNCTION_1       1  None
              506  STORE_FAST           12  'afterpar'

 L. 478       509  LOAD_GLOBAL          22  'np'
              512  LOAD_ATTR            23  'array'
              515  LOAD_GLOBAL          21  'list'
              518  LOAD_GLOBAL          24  'enumerate'
              521  LOAD_FAST             0  'stages'
              524  CALL_FUNCTION_1       1  None
              527  CALL_FUNCTION_1       1  None
              530  CALL_FUNCTION_1       1  None
              533  STORE_FAST           13  'istage'

 L. 479       536  SETUP_LOOP           83  'to 622'
              539  LOAD_FAST            13  'istage'
              542  LOAD_FAST            12  'afterpar'
              545  BINARY_SUBSCR    
              546  GET_ITER         
              547  FOR_ITER             71  'to 621'
              550  UNPACK_SEQUENCE_2     2 
              553  STORE_DEREF           0  'STAGE_ID'
              556  STORE_FAST           11  'stage'

 L. 481       559  LOAD_GLOBAL          25  'submit'
              562  LOAD_DEREF            0  'STAGE_ID'
              565  LOAD_FAST             8  'on_opt'
              568  LOAD_GLOBAL          26  'opt'
              571  LOAD_CONST               'qopt'
              574  BINARY_SUBSCR    
              575  LOAD_FAST            11  'stage'
              578  BINARY_SUBSCR    
              579  CALL_FUNCTION_VAR_2     2  None
              582  LOAD_FAST             9  'jobid'
              585  LOAD_DEREF            0  'STAGE_ID'
              588  STORE_SUBSCR     

 L. 483       589  LOAD_FAST            10  'jobdep'
              592  LOAD_DEREF            0  'STAGE_ID'
              595  LOAD_CONST               1
              598  BINARY_SUBTRACT  
              599  BINARY_SUBSCR    
              600  LOAD_ATTR            27  'append'
              603  LOAD_CONST               'beforeok:%s'
              606  LOAD_FAST             9  'jobid'
              609  LOAD_DEREF            0  'STAGE_ID'
              612  BINARY_SUBSCR    
              613  BINARY_MODULO    
              614  CALL_FUNCTION_1       1  None
              617  POP_TOP          
              618  JUMP_BACK           547  'to 547'
              621  POP_BLOCK        
            622_0  COME_FROM           536  '536'

 L. 484       622  SETUP_LOOP          235  'to 860'
              625  LOAD_FAST            13  'istage'
              628  LOAD_FAST            12  'afterpar'
              631  UNARY_INVERT     
              632  BINARY_SUBSCR    
              633  GET_ITER         
              634  FOR_ITER            164  'to 801'
              637  UNPACK_SEQUENCE_2     2 
              640  STORE_DEREF           0  'STAGE_ID'
              643  STORE_FAST           11  'stage'

 L. 486       646  LOAD_DEREF            0  'STAGE_ID'
              649  LOAD_CONST               0
              652  COMPARE_OP            4  >
              655  POP_JUMP_IF_FALSE   690  'to 690'

 L. 488       658  LOAD_FAST            10  'jobdep'
              661  LOAD_DEREF            0  'STAGE_ID'
              664  BINARY_SUBSCR    
              665  LOAD_ATTR            27  'append'
              668  LOAD_CONST               'afterok:%s'
              671  LOAD_FAST             9  'jobid'
              674  LOAD_DEREF            0  'STAGE_ID'
              677  LOAD_CONST               1
              680  BINARY_SUBTRACT  
              681  BINARY_SUBSCR    
              682  BINARY_MODULO    
              683  CALL_FUNCTION_1       1  None
              686  POP_TOP          
              687  JUMP_FORWARD          0  'to 690'
            690_0  COME_FROM           687  '687'

 L. 489       690  LOAD_FAST            10  'jobdep'
              693  LOAD_DEREF            0  'STAGE_ID'
              696  BINARY_SUBSCR    
              697  STORE_FAST           14  'dep'

 L. 490       700  LOAD_FAST            14  'dep'
              703  POP_JUMP_IF_FALSE   725  'to 725'
              706  LOAD_CONST               '-W depend='
              709  LOAD_CONST               ','
              712  LOAD_ATTR            28  'join'
              715  LOAD_FAST            14  'dep'
              718  CALL_FUNCTION_1       1  None
              721  BINARY_ADD       
              722  JUMP_FORWARD          3  'to 728'
              725  LOAD_CONST               ''
            728_0  COME_FROM           722  '722'
              728  STORE_FAST           15  'dep_opt'

 L. 491       731  LOAD_GLOBAL          18  'is_par'
              734  LOAD_FAST            11  'stage'
              737  CALL_FUNCTION_1       1  None
              740  POP_JUMP_IF_FALSE   759  'to 759'
              743  LOAD_GLOBAL          29  'array_opt'
              746  LOAD_GLOBAL          16  'NID'
              749  LOAD_GLOBAL          19  'ppn'
              752  BINARY_DIVIDE    
              753  CALL_FUNCTION_1       1  None
              756  JUMP_FORWARD          3  'to 762'
              759  LOAD_CONST               ''
            762_0  COME_FROM           756  '756'
              762  STORE_FAST           16  'arr_opt'

 L. 492       765  LOAD_GLOBAL          25  'submit'
              768  LOAD_DEREF            0  'STAGE_ID'
              771  LOAD_FAST            15  'dep_opt'
              774  LOAD_FAST            16  'arr_opt'

 L. 493       777  LOAD_GLOBAL          26  'opt'
              780  LOAD_CONST               'qopt'
              783  BINARY_SUBSCR    
              784  LOAD_FAST            11  'stage'
              787  BINARY_SUBSCR    
              788  CALL_FUNCTION_VAR_3     3  None
              791  LOAD_FAST             9  'jobid'
              794  LOAD_DEREF            0  'STAGE_ID'
              797  STORE_SUBSCR     
              798  JUMP_BACK           634  'to 634'
              801  POP_BLOCK        
            802_0  COME_FROM           622  '622'
              802  JUMP_FORWARD         55  'to 860'

 L. 495       805  LOAD_FAST             0  'stages'
              808  LOAD_GLOBAL          30  'int'
              811  LOAD_DEREF            0  'STAGE_ID'
              814  CALL_FUNCTION_1       1  None
              817  BINARY_SUBSCR    
              818  STORE_FAST           11  'stage'

 L. 496       821  LOAD_GLOBAL           1  'alog'
              824  LOAD_ATTR             9  'info'
              827  LOAD_CONST               'Stage starting: %s'
              830  LOAD_FAST            11  'stage'
              833  CALL_FUNCTION_2       2  None
              836  POP_TOP          

 L. 497       837  LOAD_FAST            11  'stage'
              840  CALL_FUNCTION_0       0  None
              843  POP_TOP          

 L. 498       844  LOAD_GLOBAL           1  'alog'
              847  LOAD_ATTR             9  'info'
              850  LOAD_CONST               'Stage done: %s'
              853  LOAD_FAST            11  'stage'
              856  CALL_FUNCTION_2       2  None
              859  POP_TOP          
            860_0  COME_FROM           622  '622'
              860  LOAD_CONST               None
              863  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 860


def memmap_chunk(filename, mode='r+', **kwargs):
    """
    Read-write memmap to chunk ID out of NID.
    
    ID and NID are normally taken from arrayjob.get_ID() and arrayjob.get_NID(), 
    but can be specified as keyword arguments for testing.
    
    Assuming a Numpy array has already been saved to file.
    
    >>> np.save("test.npy", np.arange(10))
    
    Return chunk 1 out of [0, 1, 2], [3, 4, 5], [6, 7], [8, 9].
    
    >>> c = memmap_chunk("test.npy", ID=1, NID=4)
    >>> c
    memmap([3, 4, 5])
    
    The offset attribute is the original index of the first item in the chunk.
    
    >>> c.offset
    3
    
    Clean up after the test.
    
    >>> del c
    >>> os.remove("test.npy")
    """
    global ID
    myID = kwargs.get('ID', ID)
    myNID = kwargs.get('NID', NID)
    from cgp.utils.load_memmap_offset import open_memmap, memmap_chunk_ind
    r = open_memmap(filename, 'r')
    n = r.shape[0]
    i = np.array_split(range(n), myNID)[myID]
    if len(i) > 0:
        result, offset = memmap_chunk_ind(filename, i, mode=mode)
        result.offset = offset
        return result
    else:
        return np.empty(0, r.dtype)


class Mmapdict(Dotdict):
    """
    Dictionary that memory-maps an existing {key}.npy on first lookup of d[key].
    
    Attribute access ``d.key`` works too.
    
    >>> import tempfile, shutil
    >>> dtemp = tempfile.mkdtemp()
    >>> try:
    ...     np.save("%s/a.npy" % dtemp, np.arange(3))
    ...     md = Mmapdict(pardir=dtemp, mode="r")
    ...     print repr(md["a"])
    ...     print repr(md.a)
    ...     del md
    ...     # It can be useful to pass shape and offset to Mmapdict()
    ...     np.save("%s/b.npy" % dtemp, np.arange(4))
    ...     md = Mmapdict(pardir=dtemp, mode="r+", shape=(2,), offset=1)
    ...     print repr(md["b"])
    ...     md["b"][:] = 10 + np.arange(len(md["b"]))
    ...     del md
    ...     # The memory-mapped part is modified
    ...     np.load("%s/b.npy" % dtemp)
    ... finally:
    ...     shutil.rmtree(dtemp)
    memmap([0, 1, 2])
    memmap([0, 1, 2])
    memmap([1, 2])
    array([ 0, 10, 11,  3])
    """

    def __init__(self, pardir=os.curdir, **kwargs):
        """
        Mmapdict constructor. Create pardir if not exists.
        
        :param str pardir: parent directory of preexisting .npy files to be memory-mapped.
        :param: ``**kwargs`` : passed to :func:`open_memmap`.
        """
        super(Mmapdict, self).__init__()
        if not os.path.exists(pardir):
            os.makedirs(pardir)
        self.pardir = pardir
        self.kwargs = kwargs

    def __missing__(self, key):
        """Memory-map existing {key}.npy on first lookup of key."""
        from cgp.utils.load_memmap_offset import open_memmap
        return open_memmap(('%s/%s.npy' % (self.pardir, key)), **self.kwargs)


class Timing(OrderedDict):
    """
    :class:`OrderedDict` for timings.
    
    >>> Timing(attempts=1)
    Timing([('attempts', 1), ('waiting', nan), ('started', nan), 
        ('finished', nan), ('error', nan), ('seconds', nan)])
    """
    _fields = ('attempts waiting started finished error seconds').split()
    _default = OrderedDict((k, np.nan) for k in _fields)
    _default['attempts'] = np.int64(0)

    def __init__(self, **kwargs):
        """
        Constructor for :class:`Timing`. Keyword arguments override default (0, NaN, ...)
        
        Overriding defaults.
        
        >>> Timing(attempts=1)
        Timing([('attempts', 1), ('waiting', nan), ('started', nan), 
            ('finished', nan), ('error', nan), ('seconds', nan)])
        """
        super(Timing, self).__init__()
        for k, v in self._default.items():
            self[k] = v

        for k, v in kwargs.items():
            self[k] = v

    def __array__(self):
        """
        Convert timing to record array.
        
        >>> np.array(Timing())  # ...ellipsis to allow 0 or 0L
        array([(0..., nan, nan, nan, nan, nan)],
            dtype=[('attempts', '<i8'), ('waiting', '<f8'), ('started', '<f8'), 
            ('finished', '<f8'), ('error', '<f8'), ('seconds', '<f8')])
        """
        return dict2rec(self)

    def item(self):
        """
        Emulate .item() method of np.recarray.
        
        >>> Timing().item()  # ...ellipsis to allow 0 or 0L
        (0..., nan, nan, nan, nan, nan)
        """
        return np.array(self).item()


d = os.environ.get('PBS_O_WORKDIR')
if d:
    alog.info('Changing to PBS_O_WORKDIR directory: %s' % d)
    os.chdir(d)
if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
# global ppn ## Warning: Unused global