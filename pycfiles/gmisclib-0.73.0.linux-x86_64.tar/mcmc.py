# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc.py
# Compiled at: 2011-05-13 03:19:24
"""Adaptive Markov-Chain Monte-Carlo algorithm.
This can be used to generate samples from a probability distribution,
or also as a simulated annealing algorithm for maximization.
This can be imported and its functions and classes can be used.

The central interfaces are the L{mcmc.BootStepper} class, and within
it, the C{step()} method is used iteratively to take a Markov step.

The algorithm is described in Kochanski and Rosner 2010,
and earlier versions have been used in ZZZ.
It evolved originally from amoeba_anneal (in Numerical Recipes, Press et al.).
The essential feature is that it keeps a large archive of previous positions
(possibly many times more than C{N} of them). It samples two positions
from the archive and subtracts them to generate candidate steps.
This has the nice property that when sampling from a multivariate
Gaussian distribution, the candidate steps match the distribution nicely.

It can be operated in two modes (or set to automatically switch).
One is optimization mode where it heads for the maximum of the probability
distribution.   The other mode is sampling mode, where it
asymptotically follows a Markov sampling procedure and has the
proper statistical properties.
"""
from __future__ import with_statement
import math, types, random, bisect, threading, numpy, die, gpkmisc, g_implements, multivariate_normal as MVN
Debug = 0
MEMORYS_WORTH_OF_PARAMETERS = 100000000.0

class problem_definition(object):
    """This class implements the problem to be solved.
        It's overall function in life is to compute the probability that a given
        parameter vector is acceptable.    Mcmc.py then uses that to run a
        Markov-Chain Monte-Carlo sampling.
        You may want to derive a class from this and override all the functions defined here,
        or implement your own class with the same functions.
        (Of course, in that case, it can contain extra functions also.)
        
        For instance, it can be a good idea to define a function
        "model" that computes the model that you are fitting to data
        (if that is your plan).   Then logp() can be something
        like -numpy.sum((self.model()-self.data)**2).
        Also, it can be good to define a "guess" function that computes
        a reasonable initial guess to the parameters, somehow.
        """

    @g_implements.make_optional
    @g_implements.make_varargs
    def __init__(self):
        pass

    def logp(self, x):
        """Compute the log of the probability density at C{x}.
                @param x:a parameter vector
                @type x: numpy.ndarray
                @return: The log of the probability that the model assigns to parameters x.
                @rtype: float
                @raise NotGoodPosition: This exception is used to indicate that the position
                        x is not valid.   This is equivalent to returning an extremely negative
                        logp.
                """
        raise RuntimeError, 'Virtual method'

    def fixer(self, x):
        """This is called on each candidate position
                vector.    Generally, it is used to restrict the possible
                solution space by folding position vectors that escape outside the solution space back into
                the solution space.    It can also allow for symmetries in equations.

                Formally, it defines a convex region.   All vectors outside the region are mapped
                into the region, but the mapping must be continuous at the boundary.
                (More precisely, logp(fixer(x)) must be continuous everywhere that logp(x) is continuous,
                including the boundary.)   For instance, mapping x[0] into abs(x[0]) defines a convex region
                (the positive half-space), and the mapping is continuous near x[0]=0.

                Additionally, it may re-normalize parameters at will subject to the restriction
                that logp(fixer(x))==logp(x).
                For instance, it can implement a constraint that sum(x)==0 by mapping
                x into x-average(x), so long as the value of logp() is unaffected by that
                substitution.
                other folds can sometimes lead to problems.

                @param x:a parameter vector
                @type x: numpy.ndarray
                @return: a (possibly modified) parameter vector.
                @rtype: numpy.ndarray
                @attention: Within a convex region (presumably one that contains the optimal x),
                        fixer must *not* change the value of logp(): logp(fixer(x)) == logp(x).

                @raise NotGoodPosition: This exception is used to indicate that the position
                        x is not valid.   Fixer has the option of either
                        mapping invalid parameter vectors into valid ones
                        or raising this exception.
                """
        raise RuntimeError, 'Virtual method'

    @g_implements.make_optional
    def log(self, p, i):
        """Some code calls this function every iteration
                to log the current state of the MCMC process.
                @param p: the current parameter vector, and
                @param i: an integer iteration counter.
                @return: nothing.
                """
        raise RuntimeError, 'Virtual method'


class problem_definition_F(problem_definition):

    @g_implements.make_optional
    @g_implements.make_varargs
    def __init__(self, logp_fcn, c, fixer=None):
        problem_definition.__init__(self)
        self.c = c
        self._fixer = fixer
        assert callable(logp_fcn)
        self.lpf = logp_fcn

    def logp(self, x):
        return self.lpf(x, self.c)

    logp.__doc__ = problem_definition.logp.__doc__

    def fixer(self, x):
        if self._fixer is not None:
            return self._fixer(x, self.c)
        else:
            return x

    fixer.__doc__ = problem_definition.fixer.__doc__


_Ntype = type(numpy.zeros((1,), numpy.float))

class position_base(object):
    """This class is used internally in the MCMC sampling process to
        represent a position.   It stores a parameter vector, a reference to
        the problem definition, and (optionally) caches computed values
        of log(P).
        """

    @g_implements.make_optional
    def __init__--- This code section failed: ---

 L. 176         0  LOAD_GLOBAL           0  'g_implements'
                3  LOAD_ATTR             1  'check'
                6  LOAD_FAST             2  'problem_def'
                9  LOAD_GLOBAL           2  'problem_definition'
               12  CALL_FUNCTION_2       2  None
               15  POP_TOP          

 L. 177        16  LOAD_FAST             2  'problem_def'
               19  LOAD_FAST             0  'self'
               22  STORE_ATTR            3  'pd'

 L. 179        25  LOAD_GLOBAL           4  'numpy'
               28  LOAD_ATTR             5  'array'
               31  LOAD_FAST             1  'x'
               34  LOAD_GLOBAL           4  'numpy'
               37  LOAD_ATTR             6  'float'
               40  LOAD_CONST               'copy'
               43  LOAD_GLOBAL           7  'True'
               46  CALL_FUNCTION_258   258  None
               49  STORE_FAST            3  'tmp'

 L. 180        52  LOAD_FAST             0  'self'
               55  LOAD_ATTR             3  'pd'
               58  LOAD_ATTR             8  'fixer'
               61  LOAD_FAST             3  'tmp'
               64  CALL_FUNCTION_1       1  None
               67  STORE_FAST            3  'tmp'

 L. 181        70  LOAD_GLOBAL           9  'isinstance'
               73  LOAD_FAST             3  'tmp'
               76  LOAD_GLOBAL          10  '_Ntype'
               79  CALL_FUNCTION_2       2  None
               82  POP_JUMP_IF_TRUE     94  'to 94'
               85  LOAD_ASSERT              AssertionError
               88  LOAD_CONST               'Output of fixer() is not numpy array.'
               91  RAISE_VARARGS_2       2  None

 L. 182        94  LOAD_FAST             3  'tmp'
               97  LOAD_ATTR            12  'shape'
              100  LOAD_FAST             1  'x'
              103  LOAD_ATTR            12  'shape'
              106  COMPARE_OP            2  ==
              109  POP_JUMP_IF_TRUE    149  'to 149'
              112  LOAD_ASSERT              AssertionError
              115  LOAD_CONST               'Fixer output[%s] must match shape of input[%s].'
              118  LOAD_GLOBAL          13  'str'
              121  LOAD_FAST             3  'tmp'
              124  LOAD_ATTR            12  'shape'
              127  CALL_FUNCTION_1       1  None
              130  LOAD_GLOBAL          13  'str'
              133  LOAD_FAST             1  'x'
              136  LOAD_ATTR            12  'shape'
              139  CALL_FUNCTION_1       1  None
              142  BUILD_TUPLE_2         2 
              145  BINARY_MODULO    
              146  RAISE_VARARGS_2       2  None

 L. 184       149  LOAD_FAST             3  'tmp'
              152  LOAD_FAST             0  'self'
              155  STORE_ATTR           14  'x'

 L. 185       158  LOAD_GLOBAL          15  'hash'
              161  LOAD_FAST             0  'self'
              164  LOAD_ATTR            16  'vec'
              167  CALL_FUNCTION_0       0  None
              170  LOAD_ATTR            17  'tostring'
              173  CALL_FUNCTION_0       0  None
              176  CALL_FUNCTION_1       1  None
              179  LOAD_FAST             0  'self'
              182  STORE_ATTR           18  '_uid'

Parse error at or near `LOAD_FAST' instruction at offset 179

    def logp(self):
        """Compute the log of the probability for the position.
                """
        raise RuntimeError, 'Virtual Function'

    def logp_nocompute(self):
        """Shows a recent logp value.  It does not compute
                a value unless none has ever been computed.
                """
        raise RuntimeError, 'Virtual Function'

    def new(self, shift, logp=None):
        """Returns a new position, shifted by the specified amount.
                @param shift: How much of a move to make to the new position.
                @type shift: numpy.ndarray
                @param logp: (optional)  If this is supplied, is is used to set the
                        log(P) value for the newly created position structure.
                @type logp: float or None
                @return: a new position
                @rtype: L{position_base} or a subclass
                """
        raise RuntimeError, 'Virtual Function'

    def prms(self):
        """The result of this function is to be handed to problem_definition.logp().
                This result must contain all the information specifying the position.
                Normally, this is a vector of floats, but concievably, you could include other information.
                """
        return self.x

    def vec(self):
        """Returns a numpy vector, for mathematical purposes.
                The result should contain all the information specifying the position;
                if not all, it should at least contain all the information that can be
                usefully expressed as a vector of floating point numbers.

                Normally, self.vec() and self.prms() are identical.
                """
        return self.x

    @g_implements.make_optional
    def __repr__(self):
        return '<POSbase %s>' % str(self.x)

    def __cmp__(self, other):
        """This is used when the archive is sorted."""
        dd = 0
        try:
            a = self.logp_nocompute()
        except NotGoodPosition:
            dd -= 2
            a = 0.0

        try:
            b = other.logp_nocompute()
        except NotGoodPosition:
            dd += 2
            b = 0.0

        return dd or cmp(a, b)

    def uid(self):
        return self._uid


class position_repeatable(position_base):
    """This is for the common case where logp is a well-behaved
        function of its arguments.   It caches positions and their corresponding
        values of log(P).
        """
    EPS = 1e-07
    HUGE = 1e+38
    CACHE_LIFE = 50
    FIXER_CHECK = 100

    @g_implements.make_optional
    def __init__(self, x, problem_def, logp=None):
        """
                @param x: 
                @type x: numpy.ndarray
                @type problem_def: L{problem_definition} or a subclass thereof.
                @type logp: float or None
                @param logp: the value of C{log(P)} at C{x}, or None to indicate that it
                        hasn't been computed yet.
                @except ValueError: if sanity check is failed.
                @except NotGoodPosition: from inside L{problem_definition.logp}.
                """
        position_base.__init__(self, x, problem_def)
        if logp is not None and not logp < self.HUGE:
            raise ValueError('Absurdly large value of logP', logp, self.x)
        self.cache = logp
        if logp is None:
            self.cache_valid = -1
        else:
            self.cache_valid = self.CACHE_LIFE
        if random.random() * self.FIXER_CHECK < 1.0:
            tmp = position_repeatable(self.x, problem_def)
            tlp = tmp.logp()
            slp = self.logp()
            if abs(tlp - slp) > 0.1 + self.EPS * abs(tlp + slp):
                raise ValueError, 'Fixer is not idempotent.  Logp changes from %s to %s.' % (self.logp(), tmp.logp())
        return

    def invalidate_cache(self):
        """This can be called when the mapping between parameters (x)
                and value changes.   You might use it if you wanted to
                change the probability distribution (i.e. C{log(P)}).
                """
        self.cache_valid = -1

    def logp(self):
        if self.cache_valid <= 0:
            try:
                logp = self.pd.logp(self.prms())
            except NotGoodPosition:
                logp = None

            if logp is not None and not logp < self.HUGE:
                raise ValueError('Absurdly large value of logP', logp, self.x)
            if self.cache_valid == 0 and ((self.cache is None) != (logp is None) or abs(logp - self.cache) > 0.1 + 1e-08 * (abs(logp) + abs(self.cache))):
                raise ValueError, 'Recomputing position cache; found mismatch %s to %s' % (self.cache, logp)
            self.cache = logp
            self.cache_valid = self.CACHE_LIFE
        self.cache_valid -= 1
        if self.cache is None:
            raise NotGoodPosition
        return self.cache

    def logp_nocompute(self):
        if self.cache_valid < 0:
            return self.logp()
        else:
            if self.cache is None:
                raise NotGoodPosition
            return self.cache

    def new(self, shift, logp=None):
        """Returns a new position, shifted by the specified amount."""
        return position_repeatable(self.vec() + shift, self.pd, logp=logp)

    def __repr__(self):
        if self.cache_valid > 0:
            s = str(self.cache)
        elif self.cache_valid == 0:
            s = '<cache expired>'
        else:
            s = '<uncomputed>'
        return '<POSr %s -> %s>' % (str(self.prms()), s)


class position_nonrepeatable(position_base):
    """This is for the (unfortunately common) case where logp
        is an indpendent random function of its arguments.  It does
        not cache as much as L{position_repeatable}.
        Arguments are analogous to L{position_repeatable}.
        """
    HUGE = 1e+38

    @g_implements.make_optional
    def __init__(self, x, problem_def, logp=None):
        position_base.__init__(self, x, problem_def)
        if logp is None:
            self.cache = []
        else:
            if not logp < self.HUGE:
                raise ValueError('Absurdly large value of logP', logp, self.x)
            self.cache = [
             logp]
        self.CSIZE = 5
        return

    def logp(self):
        if random.random() > self.CSIZE / float(self.CSIZE + len(self.cache)):
            logp = random.choice(self.cache)
        else:
            try:
                logp = self.pd.logp(self.prms())
            except NotGoodPosition:
                logp = None

            if not (logp is None or logp < self.HUGE):
                raise ValueError('Absurdly large value of logP', logp, self.x)
            self.cache.append(logp)
        if logp is None:
            raise NotGoodPosition
        return logp

    def logp_nocompute(self):
        if self.cache:
            tmp = random.choice(self.cache)
            if tmp is None:
                raise NotGoodPosition
        else:
            tmp = self.logp()
        return tmp

    def new(self, shift, logp=None):
        """Returns a new position, shifted by the specified amount."""
        return position_nonrepeatable(self.vec() + shift, self.pd, logp=logp)

    def __repr__(self):
        if len(self.cache):
            s1 = ''
            mn = None
            mx = None
            for q in self.cache:
                if q is None:
                    s1 = 'BAD or'
                else:
                    if mx is None or q > mx:
                        mx = q
                    if mn is None or q < mx:
                        mn = q

            s = '%s%g to %g' % (s1, mn, mx)
        else:
            s = '<uncomputed>'
        return '<POSnr %s -> %s>' % (str(self.prms()), s)


class _empty(object):
    """Just a singleton marker."""
    pass


class position_history_dependent(position_base):
    """This is for the case where logp is a history-dependent
        function of its arguments.   This is the most general, most
        expensive case.
        """
    EMPTY = _empty
    HUGE = 1e+38

    @g_implements.make_optional
    def __init__(self, x, problem_def, logp=None):
        position_base.__init__(self, x, problem_def)
        if logp is None:
            self.cache = self.EMPTY
        else:
            if not logp < self.HUGE:
                raise ValueError('Absurdly large value of logP', logp, self.x)
            self.cache = logp
        return

    def logp(self):
        logp = self.pd.logp(self.prms())
        if not (logp is None or logp < self.HUGE):
            raise ValueError('Absurdly large value of logP', logp, self.x)
        self.cache = logp
        if logp is None:
            return NotGoodPosition
        else:
            return logp

    def logp_nocompute(self):
        if self.cache is self.EMPTY:
            return self.logp()
        else:
            if self.cache is None:
                return NotGoodPosition
            return self.cache

    def new(self, shift, logp=None):
        """Returns a new position, shifted by the specified amount."""
        return position_history_dependent(self.vec() + shift, self.pd, logp=logp)

    def __repr__(self):
        if self.cache is self.EMPTY:
            s = '<uncomputed>'
        else:
            s = str(self.cache)
        return '<POSr %s -> %s>' % (str(self.prms()), s)


class T_acceptor(object):
    """This class implements a normal Metropolis-Hastings
        acceptance of steps.
        """

    def __init__(self, T=1.0):
        """You can change the temperature to do simulated annealing.
                @param T: temperature
                @type T: float
                """
        assert T >= 0.0
        self._T = T

    def T(self):
        """@return: the system temperature.
                @rtype: L{float}
                """
        return self._T

    def __call__(self, delta):
        """Accept a step or not?
                @param delta: The proposed step gives C{delta} as the change in
                        C{log(probability)}.
                @type delta: float
                @return: should it be accepted or not?
                @rtype: C{bool}
                """
        return delta > -self._T * random.expovariate(1.0)


class stepper(object):
    """This is your basic stepper class that incrementally will
        give you a Markov-Chain Monte-Carlo series of samples from
        a probability distribution.
        """

    @g_implements.make_varargs
    def __init__(self):
        self.since_last_rst = 0
        self.resetid = 0
        self.last_reset = None
        self.last_failed = None
        self.lock = threading.RLock()
        self.acceptable = T_acceptor(1.0)
        return

    def step(self):
        """In subclasses, this takes a step and returns 0 or 1,
                depending on whether the step was accepted or not."""
        self.since_last_rst += 1
        return

    def prms(self):
        """@return: The current parameters
                @rtype: C{numpy.ndarray}
                """
        return self.current().prms()

    def status(self):
        """Provides some printable status information in a=v; format."""
        raise RuntimeError, 'Virtual Function'

    def reset(self):
        """Called internally to mark when the optimization
                has found a new minimum.   [NOTE: You might also call it
                if the function you are minimizing changes.]
                """
        with self.lock:
            self.since_last_rst = 0
            self.resetid += 1

    def reset_id(self):
        """Use this to tell if the stepper has been reset since you last
                looked at it.
                """
        return self.resetid

    def needs_a_reset(self):
        """Decides if we we need a reset.    This checks
                to see if we have a new record logP that exceeds
                the old record.   It keeps track of the necessary
                paperwork.
                """
        current = self.current()
        with self.lock:
            if self.last_reset is None:
                self.last_reset = current
                rst = False
            else:
                rst = current.logp_nocompute() > self.last_reset.logp_nocompute() + self.acceptable.T() * 0.5
                if rst:
                    self.last_reset = current
        if rst and Debug > 1:
            print '# RESET: logp=', current.logp_nocompute()
        return rst

    def _set_failed(self, f):
        with self.lock:
            self.last_failed = f

    def current(self):
        """@return: the current position.
                @rtype: L{position_base}
                """
        with self.lock:
            return self._current

    def _set_current(self, newcurrent):
        """@raise NotGoodPosition: if newcurrent doesn't have a finite logp() value.
                """
        with self.lock:
            newcurrent.logp_nocompute()
            self._current = newcurrent


class adjuster(object):
    Z0 = 1.5
    DZ = 0.3
    TOL = 0.2
    STABEXP = 1.0

    def __init__(self, F, vscale, vse=0.0, vsmax=1e+30):
        assert 0.0 < F < 1.0
        self.lock = threading.Lock()
        self.vscale = vscale
        self.F = F
        self.state = 0
        self.vse = vse
        self.reset()
        self.vsmax = vsmax

    def reset(self):
        with self.lock:
            self.z = self.Z0
            self.since_reset = 0
            self.ncheck = self._calc_ncheck()
            self.blocknacc = 0
            self.blockntry = 0

    def _calc_ncheck(self):
        """This estimates when to make the next check for statistically significant
                deviations from the correct step acceptance rate.
                """
        assert self.z >= self.Z0
        ss = max(-self.z / math.log(1 - self.f()), -self.z / math.log(self.f()))
        assert ss > 3.0
        return min(100, int(math.ceil(ss)))

    def f(self):
        """This allows the desired fraction of accepted steps to
                depend on self.vscale.
                @note: This method should only be called with C{self.vse != 0}
                        where self.vscale can normally be expected to be fairly close to unity,
                        and where small values of C{self.vse} indicate trouble.
                        In the L{mcmc.Bootstepper.step_boot} case this is true.
                """
        return self.F * min(1.0, self.vscale ** self.vse)

    def inctry(self, accepted):
        with self.lock:
            self.since_reset += 1
            self.blockntry += 1
            self.blocknacc += accepted
            if self.blockntry > self.ncheck:
                self._inctry_guts()

    def _inctry_guts(self):
        """Called under lock!
                We check that the observed fraction of accepted
                steps is consistent with a Binomial distribution.
                If not, we try updating self.vscale.
                """
        EPS = 1e-06
        Flow = self.f() * (1.0 - self.TOL)
        Fhi = self.f() * (1.0 + self.TOL)
        lPH0low = self.blocknacc * math.log(Flow) + (self.blockntry - self.blocknacc) * math.log(1 - Flow)
        lPH0hi = self.blocknacc * math.log(Fhi) + (self.blockntry - self.blocknacc) * math.log(1 - Fhi)
        Phat = (self.blocknacc + EPS) / (self.blockntry + 2 * EPS)
        sigmaP = math.sqrt(self.f() * (1 - self.f()) / self.blockntry)
        lPH1 = self.blocknacc * math.log(Phat) + (self.blockntry - self.blocknacc) * math.log(1 - Phat)
        if Phat > Fhi and lPH1 - lPH0hi > self.z or Phat < Flow and lPH1 - lPH0low > self.z:
            delta = math.log(Phat / self.f())
            delta = min(max(delta, -self.TOL), self.TOL)
            self.vscale *= math.exp(delta * self.STABEXP)
            if self.vscale > self.vsmax:
                self.vscale = self.vsmax
            if Debug > 2:
                print '#NCHECK step acceptance rate is %.2f vs. %.2f:' % (Phat, self.f()), 'changing vscale to', self.vscale
                print '#NCHECK ADJ vscale=', self.vscale, self.z, self.blocknacc, self.blockntry, delta
            self.blockntry = 0
            self.blocknacc = 0
            self.state = -1
            self.ncheck = self._calc_ncheck()
        elif Phat > Flow and Phat < Fhi and 2.0 * sigmaP / self.f() < self.TOL:
            self.blockntry = 0
            self.blocknacc = 0
            self.state = 1
            self.ncheck = self._calc_ncheck()
        else:
            self.z += self.DZ
            self.state = 0
            self.ncheck = self.blockntry + self._calc_ncheck()

    def vs(self):
        """We stick in the factor of random.lognormvariate()
                so that all sizes of move are possible and thus we
                can prove that we can random-walk to any point in
                a connected region.   This makes the proof of
                ergodicity simpler.
                """
        assert type(self.vscale) == types.FloatType
        return random.lognormvariate(0.0, self.TOL / 2.0) * self.vscale

    def status(self):
        with self.lock:
            tmp = (
             self.blocknacc, self.blockntry, self.state)
        return tmp


def start_is_list_a(start):
    """Is the argument a sequence of numpy arrays?
        """
    for i, tmp in enumerate(start):
        if not isinstance(tmp, _Ntype):
            if i > 0:
                raise TypeError, 'Sequence is not all the same type'
            return False

    return len(start) > 0


def start_is_list_p(start):
    """Is the argument a sequence of position_base objects?
        """
    for i, tmp in enumerate(start):
        if not g_implements.impl(tmp, position_base):
            if i > 0:
                raise TypeError, 'Sequence is not all the same type'
            return False

    return len(start) > 0


class NoBoot(ValueError):

    def __init__(self, *s):
        ValueError.__init__(self, *s)


class NotGoodPosition(ValueError):

    def __init__(self, *s):
        ValueError.__init__(self, *s)


def make_list_of_positions--- This code section failed: ---

 L. 831         0  BUILD_LIST_0          0 
                3  STORE_FAST            3  'o'

 L. 832         6  LOAD_GLOBAL           0  'start_is_list_a'
                9  LOAD_FAST             0  'x'
               12  CALL_FUNCTION_1       1  None
               15  POP_JUMP_IF_FALSE   224  'to 224'

 L. 833        18  LOAD_GLOBAL           1  'len'
               21  LOAD_FAST             0  'x'
               24  CALL_FUNCTION_1       1  None
               27  LOAD_CONST               0
               30  COMPARE_OP            4  >
               33  POP_JUMP_IF_TRUE     45  'to 45'
               36  LOAD_ASSERT              AssertionError
               39  LOAD_CONST               'Zero length list of arrays.'
               42  RAISE_VARARGS_2       2  None

 L. 834        45  SETUP_LOOP          541  'to 589'
               48  LOAD_FAST             0  'x'
               51  GET_ITER         
               52  FOR_ITER            165  'to 220'
               55  STORE_FAST            4  't'

 L. 835        58  LOAD_GLOBAL           1  'len'
               61  LOAD_FAST             3  'o'
               64  CALL_FUNCTION_1       1  None
               67  LOAD_CONST               0
               70  COMPARE_OP            4  >
               73  POP_JUMP_IF_FALSE   120  'to 120'

 L. 836        76  LOAD_FAST             4  't'
               79  LOAD_ATTR             3  'shape'
               82  LOAD_FAST             3  'o'
               85  LOAD_CONST               0
               88  BINARY_SUBSCR    
               89  LOAD_ATTR             4  'vec'
               92  CALL_FUNCTION_0       0  None
               95  LOAD_ATTR             3  'shape'
               98  LOAD_CONST               0
              101  BINARY_SUBSCR    
              102  BUILD_TUPLE_1         1 
              105  COMPARE_OP            2  ==
              108  POP_JUMP_IF_TRUE    120  'to 120'
              111  LOAD_ASSERT              AssertionError
              114  RAISE_VARARGS_1       1  None
              117  JUMP_FORWARD          0  'to 120'
            120_0  COME_FROM           117  '117'

 L. 841       120  LOAD_GLOBAL           1  'len'
              123  LOAD_FAST             3  'o'
              126  CALL_FUNCTION_1       1  None
              129  LOAD_CONST               0
              132  COMPARE_OP            4  >
              135  POP_JUMP_IF_FALSE   195  'to 195'
              138  LOAD_GLOBAL           5  'numpy'
              141  LOAD_ATTR             6  'alltrue'
              144  LOAD_GLOBAL           5  'numpy'
              147  LOAD_ATTR             7  'equal'
              150  LOAD_FAST             3  'o'
              153  LOAD_CONST               -1
              156  BINARY_SUBSCR    
              157  LOAD_ATTR             4  'vec'
              160  CALL_FUNCTION_0       0  None
              163  LOAD_FAST             4  't'
              166  CALL_FUNCTION_2       2  None
              169  CALL_FUNCTION_1       1  None
            172_0  COME_FROM           135  '135'
              172  POP_JUMP_IF_FALSE   195  'to 195'

 L. 843       175  LOAD_FAST             3  'o'
              178  LOAD_ATTR             8  'append'
              181  LOAD_FAST             3  'o'
              184  LOAD_CONST               -1
              187  BINARY_SUBSCR    
              188  CALL_FUNCTION_1       1  None
              191  POP_TOP          
              192  JUMP_BACK            52  'to 52'

 L. 846       195  LOAD_FAST             3  'o'
              198  LOAD_ATTR             8  'append'
              201  LOAD_FAST             1  'PositionClass'
              204  LOAD_FAST             4  't'
              207  LOAD_FAST             2  'problem_def'
              210  CALL_FUNCTION_2       2  None
              213  CALL_FUNCTION_1       1  None
              216  POP_TOP          
              217  JUMP_BACK            52  'to 52'
              220  POP_BLOCK        
            221_0  COME_FROM            45  '45'
              221  JUMP_FORWARD        365  'to 589'

 L. 847       224  LOAD_GLOBAL           9  'start_is_list_p'
              227  LOAD_FAST             0  'x'
              230  CALL_FUNCTION_1       1  None
              233  POP_JUMP_IF_FALSE   471  'to 471'

 L. 848       236  LOAD_GLOBAL           1  'len'
              239  LOAD_FAST             0  'x'
              242  CALL_FUNCTION_1       1  None
              245  LOAD_CONST               0
              248  COMPARE_OP            4  >
              251  POP_JUMP_IF_TRUE    263  'to 263'
              254  LOAD_ASSERT              AssertionError
              257  LOAD_CONST               'Zero length list of positions.'
              260  RAISE_VARARGS_2       2  None

 L. 849       263  BUILD_LIST_0          0 
              266  STORE_FAST            3  'o'

 L. 850       269  SETUP_LOOP          317  'to 589'
              272  LOAD_FAST             0  'x'
              275  GET_ITER         
              276  FOR_ITER            188  'to 467'
              279  STORE_FAST            4  't'

 L. 851       282  LOAD_GLOBAL          10  'g_implements'
              285  LOAD_ATTR            11  'check'
              288  LOAD_FAST             4  't'
              291  LOAD_FAST             1  'PositionClass'
              294  CALL_FUNCTION_2       2  None
              297  POP_TOP          

 L. 852       298  LOAD_GLOBAL           1  'len'
              301  LOAD_FAST             3  'o'
              304  CALL_FUNCTION_1       1  None
              307  LOAD_CONST               0
              310  COMPARE_OP            4  >
              313  POP_JUMP_IF_FALSE   370  'to 370'

 L. 853       316  LOAD_FAST             4  't'
              319  LOAD_ATTR             4  'vec'
              322  CALL_FUNCTION_0       0  None
              325  LOAD_ATTR             3  'shape'
              328  LOAD_CONST               0
              331  BINARY_SUBSCR    
              332  LOAD_FAST             3  'o'
              335  LOAD_CONST               0
              338  BINARY_SUBSCR    
              339  LOAD_ATTR             4  'vec'
              342  CALL_FUNCTION_0       0  None
              345  LOAD_ATTR             3  'shape'
              348  LOAD_CONST               0
              351  BINARY_SUBSCR    
              352  BUILD_TUPLE_1         1 
              355  COMPARE_OP            2  ==
              358  POP_JUMP_IF_TRUE    370  'to 370'
              361  LOAD_ASSERT              AssertionError
              364  RAISE_VARARGS_1       1  None
              367  JUMP_FORWARD          0  'to 370'
            370_0  COME_FROM           367  '367'

 L. 854       370  LOAD_GLOBAL           1  'len'
              373  LOAD_FAST             3  'o'
              376  CALL_FUNCTION_1       1  None
              379  LOAD_CONST               0
              382  COMPARE_OP            4  >
              385  POP_JUMP_IF_FALSE   451  'to 451'
              388  LOAD_GLOBAL           5  'numpy'
              391  LOAD_ATTR             6  'alltrue'
              394  LOAD_GLOBAL           5  'numpy'
              397  LOAD_ATTR             7  'equal'
              400  LOAD_FAST             4  't'
              403  LOAD_ATTR             4  'vec'
              406  CALL_FUNCTION_0       0  None
              409  LOAD_FAST             3  'o'
              412  LOAD_CONST               -1
              415  BINARY_SUBSCR    
              416  LOAD_ATTR             4  'vec'
              419  CALL_FUNCTION_0       0  None
              422  CALL_FUNCTION_2       2  None
              425  CALL_FUNCTION_1       1  None
            428_0  COME_FROM           385  '385'
              428  POP_JUMP_IF_FALSE   451  'to 451'

 L. 855       431  LOAD_FAST             3  'o'
              434  LOAD_ATTR             8  'append'
              437  LOAD_FAST             3  'o'
              440  LOAD_CONST               -1
              443  BINARY_SUBSCR    
              444  CALL_FUNCTION_1       1  None
              447  POP_TOP          
              448  JUMP_BACK           276  'to 276'

 L. 858       451  LOAD_FAST             3  'o'
              454  LOAD_ATTR             8  'append'
              457  LOAD_FAST             4  't'
              460  CALL_FUNCTION_1       1  None
              463  POP_TOP          
              464  JUMP_BACK           276  'to 276'
              467  POP_BLOCK        
            468_0  COME_FROM           269  '269'
              468  JUMP_FORWARD        118  'to 589'

 L. 859       471  LOAD_GLOBAL          10  'g_implements'
              474  LOAD_ATTR            12  'impl'
              477  LOAD_FAST             0  'x'
              480  LOAD_FAST             1  'PositionClass'
              483  CALL_FUNCTION_2       2  None
              486  POP_JUMP_IF_FALSE   501  'to 501'

 L. 860       489  LOAD_FAST             0  'x'
              492  BUILD_LIST_1          1 
              495  STORE_FAST            3  'o'
              498  JUMP_FORWARD         88  'to 589'

 L. 861       501  LOAD_GLOBAL          13  'isinstance'
              504  LOAD_FAST             0  'x'
              507  LOAD_GLOBAL          14  '_Ntype'
              510  CALL_FUNCTION_2       2  None
              513  POP_JUMP_IF_FALSE   558  'to 558'
              516  LOAD_GLOBAL           1  'len'
              519  LOAD_FAST             0  'x'
              522  LOAD_ATTR             3  'shape'
              525  CALL_FUNCTION_1       1  None
              528  LOAD_CONST               1
              531  COMPARE_OP            2  ==
            534_0  COME_FROM           513  '513'
              534  POP_JUMP_IF_FALSE   558  'to 558'

 L. 862       537  LOAD_FAST             1  'PositionClass'
              540  LOAD_FAST             0  'x'
              543  LOAD_FAST             2  'problem_def'
              546  CALL_FUNCTION_2       2  None
              549  BUILD_LIST_1          1 
              552  STORE_FAST            3  'o'
              555  JUMP_FORWARD         31  'to 589'

 L. 864       558  LOAD_GLOBAL          15  'TypeError'
              561  LOAD_CONST               'Cannot handle type=%s for x.  Must implement %s or be a 1-dimensional numpy array.'
              564  LOAD_GLOBAL          16  'type'
              567  LOAD_FAST             0  'x'
              570  CALL_FUNCTION_1       1  None
              573  LOAD_GLOBAL          17  'repr'
              576  LOAD_FAST             1  'PositionClass'
              579  CALL_FUNCTION_1       1  None
              582  BUILD_TUPLE_2         2 
              585  BINARY_MODULO    
              586  RAISE_VARARGS_2       2  None
            589_0  COME_FROM           269  '269'
            589_1  COME_FROM           269  '269'
            589_2  COME_FROM           269  '269'
            589_3  COME_FROM            45  '45'

 L. 865       589  LOAD_FAST             3  'o'
              592  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 592


def _check_list_of_positions(x):
    if not isinstance(x, list):
        raise TypeError, 'Not a List (should be a list of positions)'
    for i, t in enumerate(x):
        failure = g_implements.why(t, position_base)
        if failure is not None:
            raise TypeError, 'x[%d] does not implement position_base: %s' % (i, failure)

    return


class hashcounter_c(dict):

    def incr(self, x):
        try:
            self[x] += 1
        except KeyError:
            self[x] = 1

    def decr(self, x):
        tmp = self[x]
        if tmp == 1:
            del self[x]
        elif tmp < 1:
            raise ValueError('More decrements than increments', x)
        else:
            self[x] = tmp - 1


class Archive(object):
    """This maintains a list of all the recent accepted positions."""
    SUPHILL = 'hillclimb'
    SSAMPLE = 'sample'
    SANNEAL = 'intermediate'

    def __init__(self, lop, np_eff, strategy=SANNEAL, maxArchSize=None, alpha=None):
        assert strategy in (self.SSAMPLE, self.SANNEAL, self.SUPHILL)
        assert len(lop) > 0
        self.xlop = []
        self.lop = lop
        self.strategy = strategy
        self.sorted = False
        if self.strategy == self.SANNEAL:
            self.sort()
            self.sorted = True
        self.np_eff = np_eff
        self.since_last_rst = 0
        self.lock = threading.Lock()
        self._hashes = hashcounter_c()
        for p in self.lop:
            self._hashes.incr(p.uid())

        if maxArchSize is None:
            maxArchSize = MEMORYS_WORTH_OF_PARAMETERS // self.np_eff
        self.min_l = self.np_eff + int(round(2 * math.sqrt(self.np_eff))) + 3
        if maxArchSize < self.min_l:
            raise ValueError, 'maxArchSize is too small for trustworthy operation: %d < min_l=%d (npeff=%d)' % (maxArchSize, self.min_l, self.np_eff)
        self.max_l = maxArchSize
        self.alpha = alpha
        self.n_prmlist = self.min_l
        return

    def distinct_count(self):
        """How many distinct values of the parameters are there in the archive?"""
        with self.lock:
            return len(self._hashes)

    def prmlist(self, n):
        assert n > 0
        with self.lock:
            self.n_prmlist = n
            rv = self.xlop + self.lop
            return rv[max(0, len(rv) - n):]

    def sort(self):
        """Called under lock. Sort the archive into order of C{logp}."""
        if self.sorted or self.strategy == self.SSAMPLE:
            return
        if Debug:
            die.info('# Sorting archive')
        self.lop.sort()
        self.sorted = True

    def reset(self):
        """We sort the archive to speed the convergence to
                the best solution.   After all, if you've just
                gotten a reset, it is likely that you're not at the
                bottom yet, so statistical properties of the distribution
                are likely to be irrelevant.
                """
        with self.lock:
            self.sort()
            self.truncate(self.min_l)
            self.since_last_rst = 0

    def __len__(self):
        with self.lock:
            return len(self.lop)

    def choose(self):
        with self.lock:
            return random.choice(self.lop)

    def truncate(self, desired_length):
        """Shortens the archive and updates the various counters and statistics.
                @param desired_length: Measured in terms of the number of distinct positions.
                @note: Must be called under lock.
                """
        assert len(self.lop) > 0
        assert len(self._hashes) <= len(self.lop)
        assert (len(self._hashes) > 0) == (len(self.lop) > 0)
        j = 0
        while len(self._hashes) > desired_length:
            self._hashes.decr(self.lop[j].uid())
            j += 1

        assert j <= len(self.lop)
        if j > 0:
            self.truncate_hook(self.lop[:j])
            self.xlop.extend(self.lop[:j])
            if len(self.xlop) > self.n_prmlist:
                self.xlop = self.xlop[len(self.xlop) - self.n_prmlist:]
            self.lop = self.lop[j:]
            if Debug > 1:
                die.info('Truncating archive from %d by %d' % (len(self.lop), j))
        elif Debug > 1:
            die.info('Truncate: max=%d, len=%d, nothing done' % (desired_length, len(self.lop)))
        assert len(self._hashes) <= len(self.lop)

    Sfac = {SUPHILL: 100, SANNEAL: 5, SSAMPLE: 2}

    def append(self, x, maxdups):
        """Adds stuff to the archive, possibly sorting the
                new information into place.   It updates all kinds of
                counters and summary statistics.

                @param x: A position to (possibly) add to the archive.
                @type x: L{position_base}
                @return: A one-letter code indicating what happened.  'f' if x
                        is a duplicate and duplicates are forbidden.
                        'd' if it is a duplicate and there have been
                        too many duplicates lately.
                        'a' otherwise -- x has been added to the archive.
                @rtype: str
                """
        F = 0.25
        with self.lock:
            self.since_last_rst += 1
            assert len(self._hashes) <= len(self.lop)
            uid = x.uid()
            if self.strategy != self.SSAMPLE and maxdups > 0 and self._hashes.get(uid, 0) > maxdups:
                return 'f'
            self._hashes.incr(uid)
            if not self.sorted or self.strategy == self.SSAMPLE:
                self.lop.append(x)
                self.sorted = False
            else:
                bisect.insort_right(self.lop, x)
                if self.since_last_rst > self.Sfac[self.strategy] * self.np_eff / F:
                    self.sorted = False
                    if Debug:
                        die.info('# Archive sorting is now off')
            self.append_hook(x)
            if Debug > 1:
                die.info('Archive length=%d' % len(self.lop))
            assert len(self._hashes) <= len(self.lop)
            self.truncate(min(int(self.min_l + self.alpha * self.since_last_rst), self.max_l))
        return 'a'

    def append_hook(self, x):
        pass

    def truncate_hook(self, to_be_dropped):
        pass


class ContPrmArchive(Archive):

    def __init__(self, lop, np_eff, strategy=Archive.SANNEAL, maxArchSize=None, alpha=None):
        """Append_hook() is called for every element of the archive.
                That function can be replaced in a sub-class to accumulate
                some kind of summary.  Here, it is used to keep track of parameter
                means and standard deviations.
                """
        Archive.__init__(self, lop, np_eff, strategy=strategy, maxArchSize=maxArchSize, alpha=alpha)
        self.p0 = lop[(-1)].vec()
        self.s = numpy.zeros(self.p0.shape, numpy.float)
        self.ss = numpy.zeros(self.p0.shape, numpy.float)
        for a in lop:
            self.append_hook(a)

    def append_hook(self, x):
        """This accumulates parameter means and standard deviations.
                """
        tmp = x.vec() - self.p0
        numpy.add(self.s, tmp, self.s)
        numpy.add(self.ss, numpy.square(tmp), self.ss)

    def truncate_hook(self, to_be_dropped):
        if len(to_be_dropped) > len(self.lop):
            self.p0 = self.s / (len(to_be_dropped) + len(self.lop))
            self.s = numpy.zeros(self.p0.shape)
            self.ss = numpy.zeros(self.p0.shape)
            for prms in self.lop:
                self.append_hook(prms)

        else:
            for prms in to_be_dropped:
                tmp = prms.vec() - self.p0
                numpy.subtract(self.s, tmp, self.s)
                numpy.subtract(self.ss, numpy.square(tmp), self.ss)

    def variance(self):
        with self.lock:
            n = len(self.lop)
            core = self.ss - self.s * self.s / n
            if not numpy.alltrue(numpy.greater(core, 0.0)):
                self.ss -= numpy.minimum(0.0, core)
                if Debug > 0:
                    die.warn('Zero stdev in archive.stdev for p=%s' % (',').join([ '%d' % q for q in numpy.nonzero(numpy.less_equal(core, 0.0))[0]
                                                                                 ]))
                return numpy.ones(self.s.shape, numpy.float)
        assert n > 1
        assert numpy.alltrue(numpy.greater(core, 0.0))
        return core / (n - 1)


class BootStepper(stepper):
    F = 0.234
    alpha = 0.1
    PBootLim = 0.9
    SSAMPLE = ContPrmArchive.SSAMPLE
    SUPHILL = ContPrmArchive.SUPHILL
    SANNEAL = ContPrmArchive.SANNEAL
    SSAUTO = SANNEAL
    SSNEVER = SSAMPLE
    SSLOW = SANNEAL
    SSALWAYS = SUPHILL

    def __init__(self, lop, v, strategy=SANNEAL, maxArchSize=None, parallelSizeDiv=1):
        """@param maxArchSize: How many position vectors can be stored.  This is
                        normally used to (loosely) enforce a memory limitation for large
                        jobs.
                @param parallelSizeDiv: For use when there are several cooperating MCMC
                        processes that share data.  When >1, this allows each process
                        to have smaller stored lists.   Normally, parallelSizeDiv is
                        between 1 and the number of cooperating processes.
                """
        stepper.__init__(self)
        _check_list_of_positions(lop)
        stepper._set_current(self, lop[(-1)])
        self.np = lop[0].vec().shape[0]
        self.np_eff = (self.np + parallelSizeDiv - 1) // parallelSizeDiv
        self.archive = ContPrmArchive(lop, self.np_eff, strategy=strategy, maxArchSize=maxArchSize, alpha=self.alpha)
        self.maxdups = int(round(4.0 / self.F))
        if not self.np > 0:
            raise ValueError, 'Np=%d; it must be positive.' % self.np
        if v.shape != (self.np, self.np):
            raise ValueError, 'v must be square, with side equal to the number of parameters. Vs=%s, np=%d.' % (str(v.shape), self.np)
        self.v = numpy.array(v, numpy.float, copy=True)
        self.V = MVN.multivariate_normal(numpy.zeros(v.shape[0], numpy.float), v)
        self.aB = adjuster(self.F, vscale=0.5, vse=0.5, vsmax=1.3)
        self.aV = adjuster(self.F, vscale=1.0)
        self.steptype = None
        return

    def step(self):
        stepper.step(self)
        WBoot = max(self.archive.distinct_count() - 1, 0)
        WV = self.np_eff
        P = min(self.PBootLim, WBoot / float(WBoot + WV))
        if random.random() < P:
            try:
                accepted = self.step_boot()
            except NoBoot:
                accepted = self.stepV()

        else:
            accepted = self.stepV()
        return accepted

    def status(self):
        with self.lock:
            o = [
             'a0vs=%g' % self.aB.vscale,
             'a0acc=%g; a0try=%g; a0state=%d' % self.aB.status(),
             'a1vs=%g' % self.aV.vscale,
             'a1acc=%g;  a1try=%g; a1state=%d' % self.aV.status(),
             'nboot=%d' % len(self.archive),
             'logP=%g' % self.current().logp_nocompute(),
             'type=%s' % self.steptype]
        return ('; ').join(o) + ';'

    def stepV(self):
        self.steptype = 'stepV'
        vs1 = self.aV.vs()
        move = self.V.sample() * vs1
        if hasattr(self.archive, 'variance') and self.archive.distinct_count() >= min(5, self.np):
            move *= (self.archive.variance() / self.v.diagonal()) ** 0.25
        try:
            tmp = self.current().new(move)
            delta = tmp.logp() - self.current().logp()
        except ValueError as x:
            die.warn('Cache trouble!: %s' % str(x))
            print 'current=', self.current()
            raise
        except NotGoodPosition as x:
            if Debug > 2:
                die.warn('StepV: %s' % str(x))
            return 0

        if self.acceptable(delta):
            accepted = 1
            if Debug > 2:
                die.info('StepV: Accepted logp=%g' % tmp.logp_nocompute())
            self._set_current(tmp)
            self.aV.inctry(accepted)
        else:
            self._set_failed(tmp)
            accepted = 0
            if Debug > 2:
                die.info('StepV: Rejected logp=%g vs. %g, T=%g' % (
                 tmp.logp_nocompute(), self.current().logp_nocompute(), self.acceptable.T()))
            self.aV.inctry(accepted)
            self._set_current(self.current())
        return accepted

    def step_boot--- This code section failed: ---

 L.1276         0  LOAD_CONST               'step_boot'
                3  LOAD_FAST             0  'self'
                6  STORE_ATTR            0  'steptype'

 L.1277         9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             1  'aB'
               15  LOAD_ATTR             2  'vs'
               18  CALL_FUNCTION_0       0  None
               21  STORE_FAST            1  'vs0'

 L.1278        24  LOAD_FAST             1  'vs0'
               27  LOAD_CONST               10.0
               30  COMPARE_OP            0  <
               33  POP_JUMP_IF_TRUE     55  'to 55'
               36  LOAD_ASSERT              AssertionError
               39  LOAD_CONST               'Vs0 too big!=%s'
               42  LOAD_GLOBAL           4  'str'
               45  LOAD_FAST             1  'vs0'
               48  CALL_FUNCTION_1       1  None
               51  BINARY_MODULO    
               52  RAISE_VARARGS_2       2  None

 L.1279        55  LOAD_GLOBAL           5  'Debug'
               58  LOAD_CONST               3
               61  COMPARE_OP            4  >
               64  POP_JUMP_IF_FALSE    86  'to 86'

 L.1280        67  LOAD_GLOBAL           6  'die'
               70  LOAD_ATTR             7  'note'
               73  LOAD_CONST               'VsB'
               76  LOAD_FAST             1  'vs0'
               79  CALL_FUNCTION_2       2  None
               82  POP_TOP          
               83  JUMP_FORWARD          0  'to 86'
             86_0  COME_FROM            83  '83'

 L.1282        86  LOAD_GLOBAL           8  'len'
               89  LOAD_FAST             0  'self'
               92  LOAD_ATTR             9  'archive'
               95  CALL_FUNCTION_1       1  None
               98  LOAD_CONST               2
              101  COMPARE_OP            1  <=
              104  POP_JUMP_IF_FALSE   119  'to 119'

 L.1284       107  LOAD_GLOBAL          10  'NoBoot'
              110  LOAD_CONST               'Cannot find bootstrap points'
              113  RAISE_VARARGS_2       2  None
              116  JUMP_FORWARD          0  'to 119'
            119_0  COME_FROM           116  '116'

 L.1285       119  LOAD_FAST             0  'self'
              122  LOAD_ATTR             9  'archive'
              125  LOAD_ATTR            11  'choose'
              128  CALL_FUNCTION_0       0  None
              131  STORE_FAST            2  'p1'

 L.1286       134  LOAD_FAST             0  'self'
              137  LOAD_ATTR             9  'archive'
              140  LOAD_ATTR            11  'choose'
              143  CALL_FUNCTION_0       0  None
              146  STORE_FAST            3  'p2'

 L.1288       149  LOAD_FAST             2  'p1'
              152  LOAD_ATTR            12  'uid'
              155  CALL_FUNCTION_0       0  None
              158  LOAD_FAST             3  'p2'
              161  LOAD_ATTR            12  'uid'
              164  CALL_FUNCTION_0       0  None
              167  COMPARE_OP            2  ==
              170  POP_JUMP_IF_FALSE   185  'to 185'

 L.1290       173  LOAD_GLOBAL          10  'NoBoot'
              176  LOAD_CONST               'Bootstrap: Duplicate uid'
              179  RAISE_VARARGS_2       2  None
              182  JUMP_FORWARD          0  'to 185'
            185_0  COME_FROM           182  '182'

 L.1294       185  LOAD_FAST             2  'p1'
              188  LOAD_ATTR            13  'vec'
              191  CALL_FUNCTION_0       0  None
              194  LOAD_FAST             3  'p2'
              197  LOAD_ATTR            13  'vec'
              200  CALL_FUNCTION_0       0  None
              203  BINARY_SUBTRACT  
              204  LOAD_FAST             1  'vs0'
              207  BINARY_MULTIPLY  
              208  STORE_FAST            4  'move'

 L.1297       211  SETUP_EXCEPT         53  'to 267'

 L.1298       214  LOAD_FAST             0  'self'
              217  LOAD_ATTR            14  'current'
              220  CALL_FUNCTION_0       0  None
              223  LOAD_ATTR            15  'new'
              226  LOAD_FAST             4  'move'
              229  CALL_FUNCTION_1       1  None
              232  STORE_FAST            5  'tmp'

 L.1299       235  LOAD_FAST             5  'tmp'
              238  LOAD_ATTR            16  'logp'
              241  CALL_FUNCTION_0       0  None
              244  LOAD_FAST             0  'self'
              247  LOAD_ATTR            14  'current'
              250  CALL_FUNCTION_0       0  None
              253  LOAD_ATTR            16  'logp'
              256  CALL_FUNCTION_0       0  None
              259  BINARY_SUBTRACT  
              260  STORE_FAST            6  'delta'
              263  POP_BLOCK        
              264  JUMP_FORWARD        105  'to 372'
            267_0  COME_FROM           211  '211'

 L.1300       267  DUP_TOP          
              268  LOAD_GLOBAL          17  'ValueError'
              271  COMPARE_OP           10  exception-match
              274  POP_JUMP_IF_FALSE   326  'to 326'
              277  POP_TOP          
              278  STORE_FAST            7  'x'
              281  POP_TOP          

 L.1301       282  LOAD_GLOBAL           6  'die'
              285  LOAD_ATTR            18  'warn'
              288  LOAD_CONST               'Cache trouble!: %s'
              291  LOAD_GLOBAL           4  'str'
              294  LOAD_FAST             7  'x'
              297  CALL_FUNCTION_1       1  None
              300  BINARY_MODULO    
              301  CALL_FUNCTION_1       1  None
              304  POP_TOP          

 L.1302       305  LOAD_CONST               'current='
              308  PRINT_ITEM       
              309  LOAD_FAST             0  'self'
              312  LOAD_ATTR            14  'current'
              315  CALL_FUNCTION_0       0  None
              318  PRINT_ITEM_CONT  
              319  PRINT_NEWLINE_CONT

 L.1303       320  RAISE_VARARGS_0       0  None
              323  JUMP_FORWARD         46  'to 372'

 L.1304       326  DUP_TOP          
              327  LOAD_GLOBAL          19  'NotGoodPosition'
              330  COMPARE_OP           10  exception-match
              333  POP_JUMP_IF_FALSE   371  'to 371'
              336  POP_TOP          
              337  POP_TOP          
              338  POP_TOP          

 L.1305       339  LOAD_GLOBAL           5  'Debug'
              342  LOAD_CONST               2
              345  COMPARE_OP            4  >
              348  POP_JUMP_IF_FALSE   367  'to 367'

 L.1306       351  LOAD_GLOBAL           6  'die'
              354  LOAD_ATTR            18  'warn'
              357  LOAD_CONST               'StepBoot: Nogood position'
              360  CALL_FUNCTION_1       1  None
              363  POP_TOP          
              364  JUMP_FORWARD          0  'to 367'
            367_0  COME_FROM           364  '364'

 L.1307       367  LOAD_CONST               0
              370  RETURN_VALUE     
              371  END_FINALLY      
            372_0  COME_FROM           371  '371'
            372_1  COME_FROM           264  '264'

 L.1308       372  LOAD_FAST             0  'self'
              375  LOAD_ATTR            20  'acceptable'
              378  LOAD_FAST             6  'delta'
              381  CALL_FUNCTION_1       1  None
              384  POP_JUMP_IF_FALSE   463  'to 463'

 L.1309       387  LOAD_CONST               1
              390  STORE_FAST            8  'accepted'

 L.1310       393  LOAD_GLOBAL           5  'Debug'
              396  LOAD_CONST               2
              399  COMPARE_OP            4  >
              402  POP_JUMP_IF_FALSE   431  'to 431'

 L.1311       405  LOAD_GLOBAL           6  'die'
              408  LOAD_ATTR            21  'info'
              411  LOAD_CONST               'StepBoot: Accepted logp=%g'
              414  LOAD_FAST             5  'tmp'
              417  LOAD_ATTR            22  'logp_nocompute'
              420  CALL_FUNCTION_0       0  None
              423  BINARY_MODULO    
              424  CALL_FUNCTION_1       1  None
              427  POP_TOP          
              428  JUMP_FORWARD          0  'to 431'
            431_0  COME_FROM           428  '428'

 L.1312       431  LOAD_FAST             0  'self'
              434  LOAD_ATTR            23  '_set_current'
              437  LOAD_FAST             5  'tmp'
              440  CALL_FUNCTION_1       1  None
              443  POP_TOP          

 L.1313       444  LOAD_FAST             0  'self'
              447  LOAD_ATTR             1  'aB'
              450  LOAD_ATTR            24  'inctry'
              453  LOAD_FAST             8  'accepted'
              456  CALL_FUNCTION_1       1  None
              459  POP_TOP          
              460  JUMP_FORWARD        122  'to 585'

 L.1315       463  LOAD_FAST             0  'self'
              466  LOAD_ATTR            25  '_set_failed'
              469  LOAD_FAST             5  'tmp'
              472  CALL_FUNCTION_1       1  None
              475  POP_TOP          

 L.1316       476  LOAD_CONST               0
              479  STORE_FAST            8  'accepted'

 L.1317       482  LOAD_GLOBAL           5  'Debug'
              485  LOAD_CONST               2
              488  COMPARE_OP            4  >
              491  POP_JUMP_IF_FALSE   550  'to 550'

 L.1318       494  LOAD_GLOBAL           6  'die'
              497  LOAD_ATTR            21  'info'
              500  LOAD_CONST               'StepBoot: Rejected logp=%g vs. %g, T=%g'

 L.1319       503  LOAD_FAST             5  'tmp'
              506  LOAD_ATTR            22  'logp_nocompute'
              509  CALL_FUNCTION_0       0  None
              512  LOAD_FAST             0  'self'
              515  LOAD_ATTR            14  'current'
              518  CALL_FUNCTION_0       0  None
              521  LOAD_ATTR            22  'logp_nocompute'
              524  CALL_FUNCTION_0       0  None
              527  LOAD_FAST             0  'self'
              530  LOAD_ATTR            20  'acceptable'
              533  LOAD_ATTR            26  'T'
              536  CALL_FUNCTION_0       0  None
              539  BUILD_TUPLE_3         3 
              542  BINARY_MODULO    
              543  CALL_FUNCTION_1       1  None
              546  POP_TOP          
              547  JUMP_FORWARD          0  'to 550'
            550_0  COME_FROM           547  '547'

 L.1320       550  LOAD_FAST             0  'self'
              553  LOAD_ATTR             1  'aB'
              556  LOAD_ATTR            24  'inctry'
              559  LOAD_FAST             8  'accepted'
              562  CALL_FUNCTION_1       1  None
              565  POP_TOP          

 L.1321       566  LOAD_FAST             0  'self'
              569  LOAD_ATTR            23  '_set_current'
              572  LOAD_FAST             0  'self'
              575  LOAD_ATTR            14  'current'
              578  CALL_FUNCTION_0       0  None
              581  CALL_FUNCTION_1       1  None
              584  POP_TOP          
            585_0  COME_FROM           460  '460'

 L.1322       585  LOAD_FAST             8  'accepted'
              588  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 588

    def _set_current(self, newcurrent):
        """@raise NotGoodPosition: if newcurrent doesn't have a finite logp() value.
                """
        g_implements.check(newcurrent, position_base)
        stepper._set_current(self, newcurrent)
        out = []
        with self.lock:
            maxdups = self.maxdups if self.since_last_rst < self.np_eff else -1
            q = self.archive.append(newcurrent, maxdups=maxdups)
            out.append(q)
            if self.needs_a_reset():
                self.reset_adjusters()
                self.archive.reset()
                self.reset()
                out.append('r')
        return ('').join(out)

    def _set_failed(self, f):
        """We remember this failure for error reporting purposes.
                But, just because a step failed doesn't mean it is awful.   If the archive is
                sorted (i.e. we are in optimization mode, not sampling mode) and
                if the failed step is better than most of the archive, then remember it.
                """
        stepper._set_failed(self, f)
        with self.lock:
            refPos = len(self.archive) // 4
            try:
                if f is not None and self.archive.sorted and f.logp_nocompute() > self.archive.lop[refPos].logp_nocompute():
                    self.archive.append(f, 1)
            except NotGoodPosition:
                pass

        return

    def reset_adjusters(self):
        self.aB.reset()
        self.aV.reset()

    def ergodic(self):
        """A crude measure of how ergodic the MCMC is.
                @return: The inverse of how many steps it takes to cross the
                        minimum in the slowest direction.  Or zero, if it is too
                        soon after some major violation of the MCMC assumptions.
                """
        if self.since_last_rst * self.aB.f() < 3 * self.np_eff:
            return 0.0
        if self.aB.state < 0:
            return 0.0
        vsbar = 1.7 / math.sqrt(self.np)
        vs = self.aB.vscale
        return self.F * min(1.0, vs / vsbar) ** 2

    def set_strategy(self, ss):
        tmp = self.archive.strategy
        self.archive.strategy = ss
        return tmp

    set_sort_strategy = set_strategy


def bootstepper(logp, x, v, c=None, strategy=BootStepper.SANNEAL, fixer=None, repeatable=True):
    """This is (essentially) another interface to the class constructor.
        It's really there for backwards compatibility.
        """
    pd = problem_definition_F(logp_fcn=logp, c=c, fixer=fixer)
    position_constructor = [position_nonrepeatable, position_repeatable][repeatable]
    return BootStepper(make_list_of_positions(x, position_constructor, pd), v, strategy=strategy)


def _logp1(x, c):
    return -numpy.sum(x * x * c * c)


def _logp2(x, c):
    r = numpy.identity(x.vec().shape[0], numpy.float)
    r[(0, 0)] = 0.707107
    r[(0, 1)] = 0.707107
    r[(1, 0)] = -0.707107
    r[(1, 1)] = 0.707107
    xt = numpy.dot(x, r)
    return _logp1(xt, c)


def test--- This code section failed: ---

 L.1441         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'dictops'
                9  STORE_FAST            1  'dictops'

 L.1442        12  LOAD_GLOBAL           1  'numpy'
               15  LOAD_ATTR             2  'array'
               18  LOAD_CONST               1.0
               21  LOAD_CONST               2.0
               24  LOAD_CONST               2
               27  LOAD_CONST               9
               30  LOAD_CONST               1
               33  BUILD_LIST_5          5 
               36  CALL_FUNCTION_1       1  None
               39  STORE_FAST            2  'start'

 L.1443        42  LOAD_GLOBAL           1  'numpy'
               45  LOAD_ATTR             2  'array'
               48  LOAD_CONST               100.0
               51  LOAD_CONST               30.0
               54  LOAD_CONST               10.0
               57  LOAD_CONST               3.0
               60  LOAD_CONST               0.1
               63  BUILD_LIST_5          5 
               66  CALL_FUNCTION_1       1  None
               69  STORE_FAST            3  'c'

 L.1444        72  LOAD_GLOBAL           1  'numpy'
               75  LOAD_ATTR             3  'identity'
               78  LOAD_GLOBAL           4  'len'
               81  LOAD_FAST             3  'c'
               84  CALL_FUNCTION_1       1  None
               87  LOAD_GLOBAL           1  'numpy'
               90  LOAD_ATTR             5  'float'
               93  CALL_FUNCTION_2       2  None
               96  STORE_FAST            4  'V'

 L.1447        99  LOAD_FAST             0  'stepper'
              102  LOAD_GLOBAL           6  '_logp1'
              105  LOAD_FAST             2  'start'
              108  LOAD_FAST             4  'V'
              111  LOAD_CONST               'c'
              114  LOAD_FAST             3  'c'
              117  CALL_FUNCTION_259   259  None
              120  STORE_FAST            5  'x'

 L.1448       123  LOAD_GLOBAL           1  'numpy'
              126  LOAD_ATTR             7  'zeros'
              129  LOAD_FAST             5  'x'
              132  LOAD_ATTR             8  'np'
              135  LOAD_FAST             5  'x'
              138  LOAD_ATTR             8  'np'
              141  BUILD_TUPLE_2         2 
              144  CALL_FUNCTION_1       1  None
              147  STORE_FAST            6  'v'

 L.1449       150  LOAD_FAST             1  'dictops'
              153  LOAD_ATTR             9  'dict_of_averages'
              156  CALL_FUNCTION_0       0  None
              159  STORE_FAST            7  'n_per_steptype'

 L.1450       162  SETUP_LOOP           51  'to 216'
              165  LOAD_GLOBAL          10  'range'
              168  LOAD_CONST               1000
              171  CALL_FUNCTION_1       1  None
              174  GET_ITER         
              175  FOR_ITER             37  'to 215'
              178  STORE_FAST            8  'i'

 L.1451       181  LOAD_FAST             5  'x'
              184  LOAD_ATTR            11  'step'
              187  CALL_FUNCTION_0       0  None
              190  STORE_FAST            9  'accepted'

 L.1452       193  LOAD_FAST             7  'n_per_steptype'
              196  LOAD_ATTR            12  'add'
              199  LOAD_FAST             5  'x'
              202  LOAD_ATTR            13  'steptype'
              205  LOAD_FAST             9  'accepted'
              208  CALL_FUNCTION_2       2  None
              211  POP_TOP          
              212  JUMP_BACK           175  'to 175'
              215  POP_BLOCK        
            216_0  COME_FROM           162  '162'

 L.1453       216  LOAD_CONST               0.0
              219  STORE_FAST           10  'lpsum'

 L.1454       222  LOAD_CONST               0.0
              225  STORE_FAST           11  'lps2'

 L.1455       228  LOAD_CONST               0
              231  STORE_FAST           12  'na'

 L.1456       234  LOAD_GLOBAL           1  'numpy'
              237  LOAD_ATTR             7  'zeros'
              240  LOAD_FAST             5  'x'
              243  LOAD_ATTR             8  'np'
              246  BUILD_TUPLE_1         1 
              249  CALL_FUNCTION_1       1  None
              252  STORE_FAST           13  'psum'

 L.1457       255  LOAD_CONST               30000
              258  STORE_FAST           14  'N'

 L.1458       261  LOAD_CONST               0
              264  STORE_FAST           15  'nreset'

 L.1459       267  LOAD_CONST               0
              270  STORE_FAST           16  'nsorted'

 L.1460       273  LOAD_FAST             5  'x'
              276  LOAD_ATTR            14  'reset_id'
              279  CALL_FUNCTION_0       0  None
              282  STORE_FAST           17  'rid'

 L.1461       285  SETUP_LOOP          221  'to 509'
              288  LOAD_GLOBAL          10  'range'
              291  LOAD_FAST            14  'N'
              294  CALL_FUNCTION_1       1  None
              297  GET_ITER         
              298  FOR_ITER            207  'to 508'
              301  STORE_FAST            8  'i'

 L.1462       304  LOAD_FAST             5  'x'
              307  LOAD_ATTR            11  'step'
              310  CALL_FUNCTION_0       0  None
              313  STORE_FAST            9  'accepted'

 L.1463       316  LOAD_FAST            12  'na'
              319  LOAD_FAST             9  'accepted'
              322  INPLACE_ADD      
              323  STORE_FAST           12  'na'

 L.1464       326  LOAD_FAST             7  'n_per_steptype'
              329  LOAD_ATTR            12  'add'
              332  LOAD_FAST             5  'x'
              335  LOAD_ATTR            13  'steptype'
              338  LOAD_FAST             9  'accepted'
              341  CALL_FUNCTION_2       2  None
              344  POP_TOP          

 L.1465       345  LOAD_FAST            16  'nsorted'
              348  LOAD_FAST             5  'x'
              351  LOAD_ATTR            15  'archive'
              354  LOAD_ATTR            16  'sorted'
              357  INPLACE_ADD      
              358  STORE_FAST           16  'nsorted'

 L.1466       361  LOAD_FAST             5  'x'
              364  LOAD_ATTR            14  'reset_id'
              367  CALL_FUNCTION_0       0  None
              370  LOAD_FAST            17  'rid'
              373  COMPARE_OP            3  !=
              376  POP_JUMP_IF_FALSE   404  'to 404'

 L.1467       379  LOAD_FAST             5  'x'
              382  LOAD_ATTR            14  'reset_id'
              385  CALL_FUNCTION_0       0  None
              388  STORE_FAST           17  'rid'

 L.1468       391  LOAD_FAST            15  'nreset'
              394  LOAD_CONST               1
              397  INPLACE_ADD      
              398  STORE_FAST           15  'nreset'
              401  JUMP_FORWARD          0  'to 404'
            404_0  COME_FROM           401  '401'

 L.1469       404  LOAD_FAST             5  'x'
              407  LOAD_ATTR            17  'current'
              410  CALL_FUNCTION_0       0  None
              413  LOAD_ATTR            18  'logp'
              416  CALL_FUNCTION_0       0  None
              419  STORE_FAST           18  'lp'

 L.1470       422  LOAD_FAST            10  'lpsum'
              425  LOAD_FAST            18  'lp'
              428  INPLACE_ADD      
              429  STORE_FAST           10  'lpsum'

 L.1471       432  LOAD_FAST            11  'lps2'
              435  LOAD_FAST            18  'lp'
              438  LOAD_CONST               2
              441  BINARY_POWER     
              442  INPLACE_ADD      
              443  STORE_FAST           11  'lps2'

 L.1472       446  LOAD_FAST             5  'x'
              449  LOAD_ATTR            17  'current'
              452  CALL_FUNCTION_0       0  None
              455  LOAD_ATTR            19  'vec'
              458  CALL_FUNCTION_0       0  None
              461  STORE_FAST           19  'p'

 L.1473       464  LOAD_GLOBAL           1  'numpy'
              467  LOAD_ATTR            12  'add'
              470  LOAD_FAST            13  'psum'
              473  LOAD_FAST            19  'p'
              476  LOAD_FAST            13  'psum'
              479  CALL_FUNCTION_3       3  None
              482  POP_TOP          

 L.1474       483  LOAD_FAST             6  'v'
              486  LOAD_GLOBAL           1  'numpy'
              489  LOAD_ATTR            20  'outer'
              492  LOAD_FAST            19  'p'
              495  LOAD_FAST            19  'p'
              498  CALL_FUNCTION_2       2  None
              501  INPLACE_ADD      
              502  STORE_FAST            6  'v'
              505  JUMP_BACK           298  'to 298'
              508  POP_BLOCK        
            509_0  COME_FROM           285  '285'

 L.1475       509  SETUP_LOOP           76  'to 588'
              512  LOAD_FAST             7  'n_per_steptype'
              515  LOAD_ATTR            21  'keys'
              518  CALL_FUNCTION_0       0  None
              521  GET_ITER         
              522  FOR_ITER             62  'to 587'
              525  STORE_FAST           20  'steptype'

 L.1476       528  LOAD_CONST               'Step %s has %.0f successes out of %.0f trials: %.2f'

 L.1477       531  LOAD_FAST            20  'steptype'
              534  LOAD_FAST             7  'n_per_steptype'
              537  LOAD_ATTR            22  'get_both'
              540  LOAD_FAST            20  'steptype'
              543  CALL_FUNCTION_1       1  None
              546  LOAD_CONST               0
              549  BINARY_SUBSCR    

 L.1478       550  LOAD_FAST             7  'n_per_steptype'
              553  LOAD_ATTR            22  'get_both'
              556  LOAD_FAST            20  'steptype'
              559  CALL_FUNCTION_1       1  None
              562  LOAD_CONST               1
              565  BINARY_SUBSCR    

 L.1479       566  LOAD_FAST             7  'n_per_steptype'
              569  LOAD_ATTR            23  'get_avg'
              572  LOAD_FAST            20  'steptype'
              575  CALL_FUNCTION_1       1  None
              578  BUILD_TUPLE_4         4 
              581  BINARY_MODULO    
              582  PRINT_ITEM       
              583  PRINT_NEWLINE_CONT
              584  JUMP_BACK           522  'to 522'
              587  POP_BLOCK        
            588_0  COME_FROM           509  '509'

 L.1482       588  LOAD_FAST            16  'nsorted'
              591  LOAD_FAST            14  'N'
              594  LOAD_CONST               30
              597  BINARY_FLOOR_DIVIDE
              598  COMPARE_OP            0  <
              601  POP_JUMP_IF_TRUE    610  'to 610'
              604  LOAD_ASSERT              AssertionError
              607  RAISE_VARARGS_1       1  None

 L.1483       610  LOAD_FAST            14  'N'
              613  LOAD_CONST               8
              616  BINARY_FLOOR_DIVIDE
              617  LOAD_FAST            12  'na'
              620  DUP_TOP          
              621  ROT_THREE        
              622  COMPARE_OP            0  <
              625  JUMP_IF_FALSE_OR_POP   641  'to 641'
              628  LOAD_FAST            14  'N'
              631  LOAD_CONST               2
              634  BINARY_FLOOR_DIVIDE
              635  COMPARE_OP            0  <
              638  JUMP_FORWARD          2  'to 643'
            641_0  COME_FROM           625  '625'
              641  ROT_TWO          
              642  POP_TOP          
            643_0  COME_FROM           638  '638'
              643  POP_JUMP_IF_TRUE    652  'to 652'
              646  LOAD_ASSERT              AssertionError
              649  RAISE_VARARGS_1       1  None

 L.1484       652  LOAD_FAST            15  'nreset'
              655  LOAD_CONST               3
              658  COMPARE_OP            0  <
              661  POP_JUMP_IF_TRUE    670  'to 670'
              664  LOAD_ASSERT              AssertionError
              667  RAISE_VARARGS_1       1  None

 L.1485       670  LOAD_FAST            10  'lpsum'
              673  LOAD_FAST            14  'N'
              676  INPLACE_DIVIDE   
              677  STORE_FAST           10  'lpsum'

 L.1486       680  LOAD_GLOBAL          25  'abs'
              683  LOAD_FAST            10  'lpsum'
              686  LOAD_CONST               0.5
              689  LOAD_FAST             5  'x'
              692  LOAD_ATTR             8  'np'
              695  BINARY_MULTIPLY  
              696  BINARY_ADD       
              697  CALL_FUNCTION_1       1  None
              700  LOAD_CONST               0.15
              703  COMPARE_OP            0  <
              706  POP_JUMP_IF_TRUE    735  'to 735'
              709  LOAD_ASSERT              AssertionError
              712  LOAD_CONST               'Lpsum=%g, expected value=%g'
              715  LOAD_FAST            10  'lpsum'
              718  LOAD_CONST               -0.5
              721  LOAD_FAST             5  'x'
              724  LOAD_ATTR             8  'np'
              727  BINARY_MULTIPLY  
              728  BUILD_TUPLE_2         2 
              731  BINARY_MODULO    
              732  RAISE_VARARGS_2       2  None

 L.1487       735  LOAD_FAST            11  'lps2'
              738  LOAD_FAST            14  'N'
              741  LOAD_CONST               1
              744  BINARY_SUBTRACT  
              745  INPLACE_DIVIDE   
              746  STORE_FAST           11  'lps2'

 L.1488       749  LOAD_FAST            11  'lps2'
              752  LOAD_FAST            10  'lpsum'
              755  LOAD_CONST               2
              758  BINARY_POWER     
              759  BINARY_SUBTRACT  
              760  STORE_FAST           21  'lpvar'

 L.1489       763  LOAD_GLOBAL          25  'abs'
              766  LOAD_FAST            21  'lpvar'
              769  LOAD_CONST               0.5
              772  LOAD_FAST             5  'x'
              775  LOAD_ATTR             8  'np'
              778  BINARY_MULTIPLY  
              779  BINARY_SUBTRACT  
              780  CALL_FUNCTION_1       1  None
              783  LOAD_CONST               1.0
              786  COMPARE_OP            0  <
              789  POP_JUMP_IF_TRUE    798  'to 798'
              792  LOAD_ASSERT              AssertionError
              795  RAISE_VARARGS_1       1  None

 L.1490       798  LOAD_GLOBAL           1  'numpy'
              801  LOAD_ATTR            26  'divide'
              804  LOAD_FAST            13  'psum'
              807  LOAD_FAST            14  'N'
              810  LOAD_FAST            13  'psum'
              813  CALL_FUNCTION_3       3  None
              816  POP_TOP          

 L.1491       817  LOAD_GLOBAL           1  'numpy'
              820  LOAD_ATTR            27  'alltrue'
              823  LOAD_GLOBAL           1  'numpy'
              826  LOAD_ATTR            28  'less'
              829  LOAD_GLOBAL           1  'numpy'
              832  LOAD_ATTR            29  'absolute'
              835  LOAD_FAST            13  'psum'
              838  CALL_FUNCTION_1       1  None
              841  LOAD_CONST               6.0
              844  LOAD_GLOBAL           1  'numpy'
              847  LOAD_ATTR            30  'sqrt'
              850  LOAD_FAST             3  'c'
              853  CALL_FUNCTION_1       1  None
              856  BINARY_DIVIDE    
              857  CALL_FUNCTION_2       2  None
              860  CALL_FUNCTION_1       1  None
              863  POP_JUMP_IF_TRUE    872  'to 872'
              866  LOAD_ASSERT              AssertionError
              869  RAISE_VARARGS_1       1  None

 L.1492       872  LOAD_GLOBAL           1  'numpy'
              875  LOAD_ATTR            26  'divide'
              878  LOAD_FAST             6  'v'
              881  LOAD_FAST            14  'N'
              884  LOAD_CONST               1
              887  BINARY_SUBTRACT  
              888  LOAD_FAST             6  'v'
              891  CALL_FUNCTION_3       3  None
              894  POP_TOP          

 L.1493       895  SETUP_LOOP          177  'to 1075'
              898  LOAD_GLOBAL          10  'range'
              901  LOAD_FAST             5  'x'
              904  LOAD_ATTR             8  'np'
              907  CALL_FUNCTION_1       1  None
              910  GET_ITER         
              911  FOR_ITER            160  'to 1074'
              914  STORE_FAST            8  'i'

 L.1494       917  SETUP_LOOP          151  'to 1071'
              920  LOAD_GLOBAL          10  'range'
              923  LOAD_FAST             5  'x'
              926  LOAD_ATTR             8  'np'
              929  CALL_FUNCTION_1       1  None
              932  GET_ITER         
              933  FOR_ITER            134  'to 1070'
              936  STORE_FAST           22  'j'

 L.1495       939  LOAD_FAST             8  'i'
              942  LOAD_FAST            22  'j'
              945  COMPARE_OP            2  ==
              948  POP_JUMP_IF_FALSE  1017  'to 1017'

 L.1497       951  LOAD_GLOBAL          25  'abs'
              954  LOAD_GLOBAL          31  'math'
              957  LOAD_ATTR            32  'log'
              960  LOAD_CONST               2
              963  LOAD_FAST             6  'v'
              966  LOAD_FAST             8  'i'
              969  LOAD_FAST            22  'j'
              972  BUILD_TUPLE_2         2 
              975  BINARY_SUBSCR    
              976  BINARY_MULTIPLY  
              977  LOAD_FAST             3  'c'
              980  LOAD_FAST             8  'i'
              983  BINARY_SUBSCR    
              984  BINARY_MULTIPLY  
              985  LOAD_FAST             3  'c'
              988  LOAD_FAST            22  'j'
              991  BINARY_SUBSCR    
              992  BINARY_MULTIPLY  
              993  CALL_FUNCTION_1       1  None
              996  CALL_FUNCTION_1       1  None
              999  LOAD_CONST               0.1
             1002  COMPARE_OP            0  <
             1005  POP_JUMP_IF_TRUE   1067  'to 1067'
             1008  LOAD_ASSERT              AssertionError
             1011  RAISE_VARARGS_1       1  None
             1014  JUMP_BACK           933  'to 933'

 L.1499      1017  LOAD_GLOBAL          25  'abs'
             1020  LOAD_FAST             6  'v'
             1023  LOAD_FAST             8  'i'
             1026  LOAD_FAST            22  'j'
             1029  BUILD_TUPLE_2         2 
             1032  BINARY_SUBSCR    
             1033  CALL_FUNCTION_1       1  None
             1036  LOAD_CONST               20
             1039  LOAD_FAST             3  'c'
             1042  LOAD_FAST             8  'i'
             1045  BINARY_SUBSCR    
             1046  LOAD_FAST             3  'c'
             1049  LOAD_FAST            22  'j'
             1052  BINARY_SUBSCR    
             1053  BINARY_MULTIPLY  
             1054  BINARY_DIVIDE    
             1055  COMPARE_OP            0  <
             1058  POP_JUMP_IF_TRUE    933  'to 933'
             1061  LOAD_ASSERT              AssertionError
             1064  RAISE_VARARGS_1       1  None
             1067  JUMP_BACK           933  'to 933'
             1070  POP_BLOCK        
           1071_0  COME_FROM           917  '917'
             1071  JUMP_BACK           911  'to 911'
             1074  POP_BLOCK        
           1075_0  COME_FROM           895  '895'

Parse error at or near `POP_BLOCK' instruction at offset 1074


def diag_variance(start):
    """Hand this a list of vectors and it will compute
        the variance of each component, then return a diagonal
        covariance matrix.
        """
    tmp = gpkmisc.vec_variance(start)
    if not numpy.alltrue(numpy.greater(tmp, 0.0)):
        raise ValueError, 'Zero variance for components %s' % (',').join([ '%d' % q for q in numpy.nonzero(1 - numpy.greater(tmp, 0.0))[0]
                                                                         ])
    return gpkmisc.make_diag(tmp)


if __name__ == '__main__':
    test(stepper=bootstepper)