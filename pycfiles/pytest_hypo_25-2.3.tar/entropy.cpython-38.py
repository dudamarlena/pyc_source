# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\entropy.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 3775 bytes
import contextlib, random, sys
from hypothesis.errors import InvalidArgument
RANDOMS_TO_MANAGE = [
 random]

class NumpyRandomWrapper:

    def __init__(self):
        assert 'numpy' in sys.modules
        import numpy.random
        self.seed = numpy.random.seed
        self.getstate = numpy.random.get_state
        self.setstate = numpy.random.set_state


def register_random(r: random.Random) -> None:
    """Register the given Random instance for management by Hypothesis.

    You can pass ``random.Random`` instances (or other objects with seed,
    getstate, and setstate methods) to ``register_random(r)`` to have their
    states seeded and restored in the same way as the global PRNGs from the
    ``random`` and ``numpy.random`` modules.

    All global PRNGs, from e.g. simulation or scheduling frameworks, should
    be registered to prevent flaky tests.  Hypothesis will ensure that the
    PRNG state is consistent for all test runs, or reproducibly varied if you
    choose to use the :func:`~hypothesis.strategies.random_module` strategy.
    """
    if not (hasattr(r, 'seed') and hasattr(r, 'getstate') and hasattr(r, 'setstate')):
        raise InvalidArgument('r=%r does not have all the required methods' % (r,))
    if r not in RANDOMS_TO_MANAGE:
        RANDOMS_TO_MANAGE.append(r)


def get_seeder_and_restorer--- This code section failed: ---

 L.  66         0  LOAD_GLOBAL              isinstance
                2  LOAD_DEREF               'seed'
                4  LOAD_GLOBAL              int
                6  CALL_FUNCTION_2       2  ''
                8  POP_JUMP_IF_FALSE    32  'to 32'
               10  LOAD_CONST               0
               12  LOAD_DEREF               'seed'
               14  DUP_TOP          
               16  ROT_THREE        
               18  COMPARE_OP               <=
               20  POP_JUMP_IF_FALSE    30  'to 30'
               22  LOAD_CONST               4294967296
               24  COMPARE_OP               <
               26  POP_JUMP_IF_TRUE     36  'to 36'
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            20  '20'
               30  POP_TOP          
             32_0  COME_FROM            28  '28'
             32_1  COME_FROM             8  '8'
               32  LOAD_GLOBAL              AssertionError
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.  67        36  BUILD_LIST_0          0 
               38  STORE_DEREF              'states'

 L.  69        40  LOAD_STR                 'numpy'
               42  LOAD_GLOBAL              sys
               44  LOAD_ATTR                modules
               46  COMPARE_OP               in
               48  POP_JUMP_IF_FALSE    80  'to 80'
               50  LOAD_GLOBAL              any
               52  LOAD_GENEXPR             '<code_object <genexpr>>'
               54  LOAD_STR                 'get_seeder_and_restorer.<locals>.<genexpr>'
               56  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L.  70        58  LOAD_GLOBAL              RANDOMS_TO_MANAGE

 L.  69        60  GET_ITER         
               62  CALL_FUNCTION_1       1  ''
               64  CALL_FUNCTION_1       1  ''
               66  POP_JUMP_IF_TRUE     80  'to 80'

 L.  72        68  LOAD_GLOBAL              RANDOMS_TO_MANAGE
               70  LOAD_METHOD              append
               72  LOAD_GLOBAL              NumpyRandomWrapper
               74  CALL_FUNCTION_0       0  ''
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
             80_0  COME_FROM            66  '66'
             80_1  COME_FROM            48  '48'

 L.  74        80  LOAD_CLOSURE             'seed'
               82  LOAD_CLOSURE             'states'
               84  BUILD_TUPLE_2         2 
               86  LOAD_CODE                <code_object seed_all>
               88  LOAD_STR                 'get_seeder_and_restorer.<locals>.seed_all'
               90  MAKE_FUNCTION_8          'closure'
               92  STORE_FAST               'seed_all'

 L.  80        94  LOAD_CLOSURE             'states'
               96  BUILD_TUPLE_1         1 
               98  LOAD_CODE                <code_object restore_all>
              100  LOAD_STR                 'get_seeder_and_restorer.<locals>.restore_all'
              102  MAKE_FUNCTION_8          'closure'
              104  STORE_FAST               'restore_all'

 L.  86       106  LOAD_FAST                'seed_all'
              108  LOAD_FAST                'restore_all'
              110  BUILD_TUPLE_2         2 
              112  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 112


@contextlib.contextmanager
def deterministic_PRNG(seed=0):
    """Context manager that handles random.seed without polluting global state.

    See issue #1255 and PR #1295 for details and motivation - in short,
    leaving the global pseudo-random number generator (PRNG) seeded is a very
    bad idea in principle, and breaks all kinds of independence assumptions
    in practice.
    """
    seed_all, restore_all = get_seeder_and_restorer(seed)
    seed_all
    try:
        yield
    finally:
        restore_all