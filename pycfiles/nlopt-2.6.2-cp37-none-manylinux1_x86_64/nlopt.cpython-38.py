# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Projects\nlopt-python\nlopt\nlopt.py
# Compiled at: 2019-11-24 22:38:29
# Size of source mod 2**32: 17467 bytes
"""
NLopt is a multi-language library for nonlinear optimization (local or
global, with or without derivatives, and supporting nonlinear
constraints).  Complete documentation, including a Python tutorial,
can be found at the NLopt web page: http://ab-initio.mit.edu/nlopt
"""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):

    def swig_import_helper--- This code section failed: ---

 L.  18         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              importlib
                6  STORE_FAST               'importlib'

 L.  19         8  LOAD_GLOBAL              __name__
               10  LOAD_METHOD              rpartition
               12  LOAD_STR                 '.'
               14  CALL_METHOD_1         1  ''
               16  LOAD_CONST               0
               18  BINARY_SUBSCR    
               20  STORE_FAST               'pkg'

 L.  20        22  LOAD_STR                 '.'
               24  LOAD_METHOD              join
               26  LOAD_FAST                'pkg'
               28  LOAD_STR                 '_nlopt'
               30  BUILD_TUPLE_2         2 
               32  CALL_METHOD_1         1  ''
               34  LOAD_METHOD              lstrip
               36  LOAD_STR                 '.'
               38  CALL_METHOD_1         1  ''
               40  STORE_FAST               'mname'

 L.  21        42  SETUP_FINALLY        56  'to 56'

 L.  22        44  LOAD_FAST                'importlib'
               46  LOAD_METHOD              import_module
               48  LOAD_FAST                'mname'
               50  CALL_METHOD_1         1  ''
               52  POP_BLOCK        
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY    42  '42'

 L.  23        56  DUP_TOP          
               58  LOAD_GLOBAL              ImportError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    84  'to 84'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L.  24        70  LOAD_FAST                'importlib'
               72  LOAD_METHOD              import_module
               74  LOAD_STR                 '_nlopt'
               76  CALL_METHOD_1         1  ''
               78  ROT_FOUR         
               80  POP_EXCEPT       
               82  RETURN_VALUE     
             84_0  COME_FROM            62  '62'
               84  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 66


    _nlopt = swig_import_helper()
    del swig_import_helper
else:
    if _swig_python_version_info >= (2, 6, 0):

        def swig_import_helper():
            from os.path import dirname
            import imp
            fp = None
            try:
                fp, pathname, description = imp.find_module('_nlopt', [dirname(__file__)])
            except ImportError:
                import _nlopt
                return _nlopt
            else:
                try:
                    _mod = imp.load_module('_nlopt', fp, pathname, description)
                finally:
                    if fp is not None:
                        fp.close()

                return _mod


        _nlopt = swig_import_helper()
        del swig_import_helper
    else:
        import _nlopt
del _swig_python_version_info
try:
    _swig_property = property
except NameError:
    pass

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__
else:

    def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
        if name == 'thisown':
            return self.this.ownvalue
        else:
            if name == 'this':
                if type(value).__name__ == 'SwigPyObject':
                    self.__dict__[name] = value
                    return
            method = class_type.__swig_setmethods__.get(name, None)
            if method:
                return method(self, value)
                if not static:
                    if _newclass:
                        object.__setattr__(self, name, value)
                    else:
                        self.__dict__[name] = value
            else:
                raise AttributeError('You cannot add attributes to %s' % self)


    def _swig_setattr(self, class_type, name, value):
        return _swig_setattr_nondynamic(self, class_type, name, value, 0)


    def _swig_getattr(self, class_type, name):
        if name == 'thisown':
            return self.this.own()
        method = class_type.__swig_getmethods__.get(name, None)
        if method:
            return method(self)
        raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


    def _swig_repr(self):
        try:
            strthis = 'proxy of ' + self.this.__repr__()
        except __builtin__.Exception:
            strthis = ''
        else:
            return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


    try:
        _object = object
        _newclass = 1
    except __builtin__.Exception:

        class _object:
            pass


        _newclass = 0
    else:

        class SwigPyIterator(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)

            def __init__(self, *args, **kwargs):
                raise AttributeError('No constructor defined - class is abstract')

            __repr__ = _swig_repr
            __swig_destroy__ = _nlopt.delete_SwigPyIterator
            __del__ = lambda self: None

            def value(self):
                return _nlopt.SwigPyIterator_valueself

            def incr(self, n=1):
                return _nlopt.SwigPyIterator_incr(self, n)

            def decr(self, n=1):
                return _nlopt.SwigPyIterator_decr(self, n)

            def distance(self, x):
                return _nlopt.SwigPyIterator_distance(self, x)

            def equal(self, x):
                return _nlopt.SwigPyIterator_equal(self, x)

            def copy(self):
                return _nlopt.SwigPyIterator_copyself

            def next(self):
                return _nlopt.SwigPyIterator_nextself

            def __next__(self):
                return _nlopt.SwigPyIterator___next__self

            def previous(self):
                return _nlopt.SwigPyIterator_previousself

            def advance(self, n):
                return _nlopt.SwigPyIterator_advance(self, n)

            def __eq__(self, x):
                return _nlopt.SwigPyIterator___eq__(self, x)

            def __ne__(self, x):
                return _nlopt.SwigPyIterator___ne__(self, x)

            def __iadd__(self, n):
                return _nlopt.SwigPyIterator___iadd__(self, n)

            def __isub__(self, n):
                return _nlopt.SwigPyIterator___isub__(self, n)

            def __add__(self, n):
                return _nlopt.SwigPyIterator___add__(self, n)

            def __sub__(self, *args):
                return (_nlopt.SwigPyIterator___sub__)(self, *args)

            def __iter__(self):
                return self


        SwigPyIterator_swigregister = _nlopt.SwigPyIterator_swigregister
        SwigPyIterator_swigregister(SwigPyIterator)

        class nlopt_doublevector(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, nlopt_doublevector, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, nlopt_doublevector, name)
            __repr__ = _swig_repr

            def iterator(self):
                return _nlopt.nlopt_doublevector_iteratorself

            def __iter__(self):
                return self.iterator()

            def __nonzero__(self):
                return _nlopt.nlopt_doublevector___nonzero__self

            def __bool__(self):
                return _nlopt.nlopt_doublevector___bool__self

            def __len__(self):
                return _nlopt.nlopt_doublevector___len__self

            def __getslice__(self, i, j):
                return _nlopt.nlopt_doublevector___getslice__(self, i, j)

            def __setslice__(self, *args):
                return (_nlopt.nlopt_doublevector___setslice__)(self, *args)

            def __delslice__(self, i, j):
                return _nlopt.nlopt_doublevector___delslice__(self, i, j)

            def __delitem__(self, *args):
                return (_nlopt.nlopt_doublevector___delitem__)(self, *args)

            def __getitem__(self, *args):
                return (_nlopt.nlopt_doublevector___getitem__)(self, *args)

            def __setitem__(self, *args):
                return (_nlopt.nlopt_doublevector___setitem__)(self, *args)

            def pop(self):
                return _nlopt.nlopt_doublevector_popself

            def append(self, x):
                return _nlopt.nlopt_doublevector_append(self, x)

            def empty(self):
                return _nlopt.nlopt_doublevector_emptyself

            def size(self):
                return _nlopt.nlopt_doublevector_sizeself

            def swap(self, v):
                return _nlopt.nlopt_doublevector_swap(self, v)

            def begin(self):
                return _nlopt.nlopt_doublevector_beginself

            def end(self):
                return _nlopt.nlopt_doublevector_endself

            def rbegin(self):
                return _nlopt.nlopt_doublevector_rbeginself

            def rend(self):
                return _nlopt.nlopt_doublevector_rendself

            def clear(self):
                return _nlopt.nlopt_doublevector_clearself

            def get_allocator(self):
                return _nlopt.nlopt_doublevector_get_allocatorself

            def pop_back(self):
                return _nlopt.nlopt_doublevector_pop_backself

            def erase(self, *args):
                return (_nlopt.nlopt_doublevector_erase)(self, *args)

            def __init__(self, *args):
                this = (_nlopt.new_nlopt_doublevector)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def push_back(self, x):
                return _nlopt.nlopt_doublevector_push_back(self, x)

            def front(self):
                return _nlopt.nlopt_doublevector_frontself

            def back(self):
                return _nlopt.nlopt_doublevector_backself

            def assign(self, n, x):
                return _nlopt.nlopt_doublevector_assign(self, n, x)

            def resize(self, *args):
                return (_nlopt.nlopt_doublevector_resize)(self, *args)

            def insert(self, *args):
                return (_nlopt.nlopt_doublevector_insert)(self, *args)

            def reserve(self, n):
                return _nlopt.nlopt_doublevector_reserve(self, n)

            def capacity(self):
                return _nlopt.nlopt_doublevector_capacityself

            __swig_destroy__ = _nlopt.delete_nlopt_doublevector
            __del__ = lambda self: None


        nlopt_doublevector_swigregister = _nlopt.nlopt_doublevector_swigregister
        nlopt_doublevector_swigregister(nlopt_doublevector)
        ForcedStop = _nlopt.ForcedStop
        RoundoffLimited = _nlopt.RoundoffLimited
        __version__ = str(_nlopt.version_major()) + '.' + str(_nlopt.version_minor()) + '.' + str(_nlopt.version_bugfix())

        def nlopt_get_initial_step(opt, dx):
            return _nlopt.nlopt_get_initial_step(opt, dx)


        nlopt_get_initial_step = _nlopt.nlopt_get_initial_step
        GN_DIRECT = _nlopt.GN_DIRECT
        GN_DIRECT_L = _nlopt.GN_DIRECT_L
        GN_DIRECT_L_RAND = _nlopt.GN_DIRECT_L_RAND
        GN_DIRECT_NOSCAL = _nlopt.GN_DIRECT_NOSCAL
        GN_DIRECT_L_NOSCAL = _nlopt.GN_DIRECT_L_NOSCAL
        GN_DIRECT_L_RAND_NOSCAL = _nlopt.GN_DIRECT_L_RAND_NOSCAL
        GN_ORIG_DIRECT = _nlopt.GN_ORIG_DIRECT
        GN_ORIG_DIRECT_L = _nlopt.GN_ORIG_DIRECT_L
        GD_STOGO = _nlopt.GD_STOGO
        GD_STOGO_RAND = _nlopt.GD_STOGO_RAND
        LD_LBFGS_NOCEDAL = _nlopt.LD_LBFGS_NOCEDAL
        LD_LBFGS = _nlopt.LD_LBFGS
        LN_PRAXIS = _nlopt.LN_PRAXIS
        LD_VAR1 = _nlopt.LD_VAR1
        LD_VAR2 = _nlopt.LD_VAR2
        LD_TNEWTON = _nlopt.LD_TNEWTON
        LD_TNEWTON_RESTART = _nlopt.LD_TNEWTON_RESTART
        LD_TNEWTON_PRECOND = _nlopt.LD_TNEWTON_PRECOND
        LD_TNEWTON_PRECOND_RESTART = _nlopt.LD_TNEWTON_PRECOND_RESTART
        GN_CRS2_LM = _nlopt.GN_CRS2_LM
        GN_MLSL = _nlopt.GN_MLSL
        GD_MLSL = _nlopt.GD_MLSL
        GN_MLSL_LDS = _nlopt.GN_MLSL_LDS
        GD_MLSL_LDS = _nlopt.GD_MLSL_LDS
        LD_MMA = _nlopt.LD_MMA
        LN_COBYLA = _nlopt.LN_COBYLA
        LN_NEWUOA = _nlopt.LN_NEWUOA
        LN_NEWUOA_BOUND = _nlopt.LN_NEWUOA_BOUND
        LN_NELDERMEAD = _nlopt.LN_NELDERMEAD
        LN_SBPLX = _nlopt.LN_SBPLX
        LN_AUGLAG = _nlopt.LN_AUGLAG
        LD_AUGLAG = _nlopt.LD_AUGLAG
        LN_AUGLAG_EQ = _nlopt.LN_AUGLAG_EQ
        LD_AUGLAG_EQ = _nlopt.LD_AUGLAG_EQ
        LN_BOBYQA = _nlopt.LN_BOBYQA
        GN_ISRES = _nlopt.GN_ISRES
        AUGLAG = _nlopt.AUGLAG
        AUGLAG_EQ = _nlopt.AUGLAG_EQ
        G_MLSL = _nlopt.G_MLSL
        G_MLSL_LDS = _nlopt.G_MLSL_LDS
        LD_SLSQP = _nlopt.LD_SLSQP
        LD_CCSAQ = _nlopt.LD_CCSAQ
        GN_ESCH = _nlopt.GN_ESCH
        GN_AGS = _nlopt.GN_AGS
        NUM_ALGORITHMS = _nlopt.NUM_ALGORITHMS
        FAILURE = _nlopt.FAILURE
        INVALID_ARGS = _nlopt.INVALID_ARGS
        OUT_OF_MEMORY = _nlopt.OUT_OF_MEMORY
        ROUNDOFF_LIMITED = _nlopt.ROUNDOFF_LIMITED
        FORCED_STOP = _nlopt.FORCED_STOP
        SUCCESS = _nlopt.SUCCESS
        STOPVAL_REACHED = _nlopt.STOPVAL_REACHED
        FTOL_REACHED = _nlopt.FTOL_REACHED
        XTOL_REACHED = _nlopt.XTOL_REACHED
        MAXEVAL_REACHED = _nlopt.MAXEVAL_REACHED
        MAXTIME_REACHED = _nlopt.MAXTIME_REACHED

        class roundoff_limited(Exception):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, roundoff_limited, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, roundoff_limited, name)
            __repr__ = _swig_repr

            def __init__(self):
                this = _nlopt.new_roundoff_limited()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _nlopt.delete_roundoff_limited
            __del__ = lambda self: None


        roundoff_limited_swigregister = _nlopt.roundoff_limited_swigregister
        roundoff_limited_swigregister(roundoff_limited)

        class forced_stop(Exception):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, forced_stop, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, forced_stop, name)
            __repr__ = _swig_repr

            def __init__(self):
                this = _nlopt.new_forced_stop()
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            __swig_destroy__ = _nlopt.delete_forced_stop
            __del__ = lambda self: None


        forced_stop_swigregister = _nlopt.forced_stop_swigregister
        forced_stop_swigregister(forced_stop)

        class opt(_object):
            __swig_setmethods__ = {}
            __setattr__ = lambda self, name, value: _swig_setattr(self, opt, name, value)
            __swig_getmethods__ = {}
            __getattr__ = lambda self, name: _swig_getattr(self, opt, name)
            __repr__ = _swig_repr
            __swig_destroy__ = _nlopt.delete_opt
            __del__ = lambda self: None

            def __init__(self, *args):
                this = (_nlopt.new_opt)(*args)
                try:
                    self.this.appendthis
                except __builtin__.Exception:
                    self.this = this

            def optimize(self, *args):
                return (_nlopt.opt_optimize)(self, *args)

            def last_optimize_result(self):
                return _nlopt.opt_last_optimize_resultself

            def last_optimum_value(self):
                return _nlopt.opt_last_optimum_valueself

            def get_algorithm(self):
                return _nlopt.opt_get_algorithmself

            def get_algorithm_name(self):
                return _nlopt.opt_get_algorithm_nameself

            def get_dimension(self):
                return _nlopt.opt_get_dimensionself

            def set_min_objective(self, *args):
                return (_nlopt.opt_set_min_objective)(self, *args)

            def set_max_objective(self, *args):
                return (_nlopt.opt_set_max_objective)(self, *args)

            def remove_inequality_constraints(self):
                return _nlopt.opt_remove_inequality_constraintsself

            def remove_equality_constraints(self):
                return _nlopt.opt_remove_equality_constraintsself

            def add_inequality_constraint(self, *args):
                return (_nlopt.opt_add_inequality_constraint)(self, *args)

            def add_equality_constraint(self, *args):
                return (_nlopt.opt_add_equality_constraint)(self, *args)

            def add_inequality_mconstraint(self, *args):
                return (_nlopt.opt_add_inequality_mconstraint)(self, *args)

            def add_equality_mconstraint(self, *args):
                return (_nlopt.opt_add_equality_mconstraint)(self, *args)

            def get_lower_bounds(self, *args):
                return (_nlopt.opt_get_lower_bounds)(self, *args)

            def set_lower_bounds(self, *args):
                return (_nlopt.opt_set_lower_bounds)(self, *args)

            def get_upper_bounds(self, *args):
                return (_nlopt.opt_get_upper_bounds)(self, *args)

            def set_upper_bounds(self, *args):
                return (_nlopt.opt_set_upper_bounds)(self, *args)

            def get_stopval(self):
                return _nlopt.opt_get_stopvalself

            def set_stopval(self, stopval):
                return _nlopt.opt_set_stopval(self, stopval)

            def get_ftol_rel(self):
                return _nlopt.opt_get_ftol_relself

            def set_ftol_rel(self, ftol_rel):
                return _nlopt.opt_set_ftol_rel(self, ftol_rel)

            def get_ftol_abs(self):
                return _nlopt.opt_get_ftol_absself

            def set_ftol_abs(self, ftol_abs):
                return _nlopt.opt_set_ftol_abs(self, ftol_abs)

            def get_xtol_rel(self):
                return _nlopt.opt_get_xtol_relself

            def set_xtol_rel(self, xtol_rel):
                return _nlopt.opt_set_xtol_rel(self, xtol_rel)

            def get_xtol_abs(self, *args):
                return (_nlopt.opt_get_xtol_abs)(self, *args)

            def set_xtol_abs(self, *args):
                return (_nlopt.opt_set_xtol_abs)(self, *args)

            def get_maxeval(self):
                return _nlopt.opt_get_maxevalself

            def set_maxeval(self, maxeval):
                return _nlopt.opt_set_maxeval(self, maxeval)

            def get_numevals(self):
                return _nlopt.opt_get_numevalsself

            def get_maxtime(self):
                return _nlopt.opt_get_maxtimeself

            def set_maxtime(self, maxtime):
                return _nlopt.opt_set_maxtime(self, maxtime)

            def get_force_stop(self):
                return _nlopt.opt_get_force_stopself

            def set_force_stop(self, force_stop):
                return _nlopt.opt_set_force_stop(self, force_stop)

            def force_stop(self):
                return _nlopt.opt_force_stopself

            def get_errmsg(self):
                return _nlopt.opt_get_errmsgself

            def set_local_optimizer(self, lo):
                return _nlopt.opt_set_local_optimizer(self, lo)

            def get_population(self):
                return _nlopt.opt_get_populationself

            def set_population(self, population):
                return _nlopt.opt_set_population(self, population)

            def get_vector_storage(self):
                return _nlopt.opt_get_vector_storageself

            def set_vector_storage(self, vector_storage):
                return _nlopt.opt_set_vector_storage(self, vector_storage)

            def set_initial_step(self, *args):
                return (_nlopt.opt_set_initial_step)(self, *args)

            def set_default_initial_step(self, x):
                return _nlopt.opt_set_default_initial_step(self, x)

            def get_initial_step(self, *args):
                return (_nlopt.opt_get_initial_step)(self, *args)

            def get_initial_step_(self, x):
                return _nlopt.opt_get_initial_step_(self, x)


        opt_swigregister = _nlopt.opt_swigregister
        opt_swigregister(opt)

        def srand(seed):
            return _nlopt.srandseed


        srand = _nlopt.srand

        def srand_time():
            return _nlopt.srand_time()


        srand_time = _nlopt.srand_time

        def version(major, minor, bugfix):
            return _nlopt.version(major, minor, bugfix)


        version = _nlopt.version

        def version_major():
            return _nlopt.version_major()


        version_major = _nlopt.version_major

        def version_minor():
            return _nlopt.version_minor()


        version_minor = _nlopt.version_minor

        def version_bugfix():
            return _nlopt.version_bugfix()


        version_bugfix = _nlopt.version_bugfix

        def algorithm_name(a):
            return _nlopt.algorithm_namea


        algorithm_name = _nlopt.algorithm_name