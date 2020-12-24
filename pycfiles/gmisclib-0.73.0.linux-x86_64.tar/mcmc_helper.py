# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_helper.py
# Compiled at: 2011-05-11 15:13:41
"""This is a helper module to make use of mcmc.py and mcmc_big.py.
It allows you to conveniently run a Monte-Carlo simulation of any
kind until it converges (L{stepper.run_to_bottom}) or until it
has explored a large chunk of parameter space (L{stepper.run_to_ergodic}).

It also helps you with logging the process.
"""
from __future__ import with_statement
import sys, random, thread as Thr, numpy, g_implements, mcmc, die
Debug = 0
_NumpyType = type(numpy.zeros((1, )))

class TooManyLoops(Exception):

    def __init__(self, *s):
        Exception.__init__(self, *s)


class warnevery(object):

    def __init__(self, interval):
        self.c = 0
        self.interval = interval
        self.lwc = 0

    def inc(self, incr=1):
        self.c += incr
        if self.c > self.lwc + self.interval:
            self.lwc = self.c
            return 1
        return 0

    def count(self):
        return self.c


class _counter(object):

    def __init__(self):
        self.lock = Thr.allocate_lock()
        self.count = 0

    def update(self, accepted):
        with self.lock:
            self.count += accepted

    def get(self):
        with self.lock:
            return self.count


class logger_template(object):

    def add(self, stepperInstance, iter):
        pass

    def close(self):
        pass

    def reset(self):
        pass


def _sign(x):
    if x > 0.0:
        return 1
    if x < 0.0:
        return -1
    return 0


class stepper(object):

    def __init__(self, x, maxloops=-1, logger=None, share=None):
        self.logger = None
        self.iter = 0
        self.last_resetid = -1
        self.maxloops = maxloops
        g_implements.check(x, mcmc.stepper)
        self.x = x
        if logger is None:
            self.logger = logger_template()
        else:
            g_implements.check(logger, logger_template)
            self.logger = logger
        return

    def reset_loops(self, maxloops=-1):
        self.maxloops = maxloops

    def run_to_change--- This code section failed: ---

 L. 111         0  LOAD_FAST             3  'update_T'
                3  UNARY_NOT        
                4  POP_JUMP_IF_TRUE     16  'to 16'
                7  LOAD_ASSERT              AssertionError
               10  LOAD_CONST               'Obsolete!'
               13  RAISE_VARARGS_2       2  None

 L. 112        16  LOAD_FAST             2  'acceptable_step'
               19  LOAD_CONST               None
               22  COMPARE_OP            9  is-not
               25  POP_JUMP_IF_FALSE    43  'to 43'

 L. 113        28  LOAD_FAST             2  'acceptable_step'
               31  LOAD_FAST             0  'self'
               34  LOAD_ATTR             2  'x'
               37  STORE_ATTR            3  'acceptable'
               40  JUMP_FORWARD          0  'to 43'
             43_0  COME_FROM            40  '40'

 L. 114        43  LOAD_FAST             0  'self'
               46  LOAD_ATTR             2  'x'
               49  LOAD_ATTR             3  'acceptable'
               52  STORE_FAST            4  'old_acceptable'

 L. 115        55  LOAD_CONST               0
               58  STORE_FAST            5  'n'

 L. 116        61  LOAD_FAST             0  'self'
               64  LOAD_ATTR             4  'synchronize_start'
               67  LOAD_CONST               'rtc'
               70  CALL_FUNCTION_1       1  None
               73  POP_TOP          

 L. 117        74  LOAD_FAST             0  'self'
               77  LOAD_ATTR             5  'communicate_hook'
               80  LOAD_CONST               'RTC:%d'
               83  LOAD_FAST             1  'ncw'
               86  BINARY_MODULO    
               87  CALL_FUNCTION_1       1  None
               90  POP_TOP          

 L. 118        91  SETUP_FINALLY       117  'to 211'

 L. 119        94  SETUP_LOOP          110  'to 207'
               97  LOAD_FAST             5  'n'
              100  LOAD_FAST             1  'ncw'
              103  COMPARE_OP            0  <
              106  POP_JUMP_IF_FALSE   206  'to 206'

 L. 120       109  LOAD_FAST             5  'n'
              112  LOAD_FAST             0  'self'
              115  LOAD_ATTR             2  'x'
              118  LOAD_ATTR             6  'step'
              121  CALL_FUNCTION_0       0  None
              124  INPLACE_ADD      
              125  STORE_FAST            5  'n'

 L. 121       128  LOAD_FAST             0  'self'
              131  LOAD_ATTR             7  'maxloops'
              134  LOAD_CONST               0
              137  COMPARE_OP            4  >
              140  POP_JUMP_IF_FALSE   161  'to 161'

 L. 122       143  LOAD_FAST             0  'self'
              146  DUP_TOP          
              147  LOAD_ATTR             7  'maxloops'
              150  LOAD_CONST               1
              153  INPLACE_SUBTRACT 
              154  ROT_TWO          
              155  STORE_ATTR            7  'maxloops'
              158  JUMP_FORWARD          0  'to 161'
            161_0  COME_FROM           158  '158'

 L. 123       161  LOAD_FAST             0  'self'
              164  LOAD_ATTR             7  'maxloops'
              167  LOAD_CONST               0
              170  COMPARE_OP            2  ==
              173  POP_JUMP_IF_FALSE   188  'to 188'

 L. 124       176  LOAD_GLOBAL           8  'TooManyLoops'
              179  LOAD_CONST               'run_to_change'
              182  RAISE_VARARGS_2       2  None
              185  JUMP_FORWARD          0  'to 188'
            188_0  COME_FROM           185  '185'

 L. 125       188  LOAD_FAST             0  'self'
              191  DUP_TOP          
              192  LOAD_ATTR             9  'iter'
              195  LOAD_CONST               1
              198  INPLACE_ADD      
              199  ROT_TWO          
              200  STORE_ATTR            9  'iter'
              203  JUMP_BACK            97  'to 97'
              206  POP_BLOCK        
            207_0  COME_FROM            94  '94'
              207  POP_BLOCK        
              208  LOAD_CONST               None
            211_0  COME_FROM_FINALLY    91  '91'

 L. 127       211  LOAD_FAST             4  'old_acceptable'
              214  LOAD_FAST             0  'self'
              217  LOAD_ATTR             2  'x'
              220  STORE_ATTR           10  'acceptable_step'

 L. 128       223  LOAD_FAST             0  'self'
              226  LOAD_ATTR            11  'synchronize_end'
              229  LOAD_CONST               'rtc'
              232  CALL_FUNCTION_1       1  None
              235  POP_TOP          
              236  END_FINALLY      

 L. 129       237  LOAD_FAST             0  'self'
              240  LOAD_ATTR             2  'x'
              243  LOAD_ATTR            12  'current'
              246  CALL_FUNCTION_0       0  None
              249  RETURN_VALUE     

Parse error at or near `CALL_FUNCTION_0' instruction at offset 246

    def communicate_hook(self, id):
        pass

    def close(self):
        """After calling close(), it is no longer legal
                to call run_to_change(), run_to_ergodic(), or
                run_to_bottom().    Logging is shut down, but the
                contents of the stepper are still available for
                inspection.
                """
        if self.logger is not None:
            self.logger.close()
            self.logger = None
        return

    def _nc_get_hook(self, nc):
        return nc

    def run_to_ergodic(self, ncw=1, T=1.0):
        """Run the stepper until it has explored all of parameter space
                C{ncw} times (as best as we can estimate).   Note that this
                is a pretty careful routine.   If the stepper finds a better
                region of parameter space so that log(P) improves part way
                through the process, the routine will reset itself and begin
                again.

                NOTE: this sets C{T} and C{sortstrategy} for the L{stepper<mcmc.BootStepper>}.

                @param ncw: how many times (or what fraction) of an ergodic
                        exploration to make.
                @type ncw: int.
                @param T: temperature at which to run the Monte-Carlo process.
                        This is normally 1.0.   If it is C{None}, then the
                        current temperature is not modified.
                @type T: C{float} or C{None}.
                @return: a L{position<mcmc.position_base>} at the end of the process.
                """
        ISSMAX = 20
        self.synchronize_start('rte')
        if T is not None:
            acceptable_step = mcmc.T_acceptor(T)
        else:
            acceptable_step = None
        ss = self.x.set_strategy(self.x.SSAMPLE)
        nc = 0.0
        try:
            iss = 1
            while True:
                ncg = self._nc_get_hook(nc)
                if ncg >= ncw:
                    break
                elif ncg < 0.5 * ncw and iss < ISSMAX:
                    iss += 1
                self.run_to_change(ncw=iss, acceptable_step=acceptable_step)
                nc += self.x.ergodic() * iss
                if self.x.reset_id() != self.last_resetid:
                    self.last_resetid = self.x.reset_id()
                    nc = 0.0
                    self.logger.reset()
                else:
                    e = self.x.ergodic()
                    nc += e * iss
                    if e > 0.0:
                        self.logger.add(self.x, self.iter)

        finally:
            self.x.set_strategy(ss)

        self.synchronize_end('rte')
        return self.x.current()

    def _not_at_bottom(self, xchanged, nchg, es, dotchanged, ndot):
        return numpy.sometrue(numpy.less(xchanged, nchg)) or es < 0.5 or dotchanged < ndot or self.x.acceptable.T() > 1.5

    def run_to_bottom(self, ns=3, acceptable_step=None):
        """Run the X{Markov Chain Monte-Carlo} until it converges
                near a minimum.

                The general idea of the termination condition is that
                it keeps track of the angle between successive sequences of steps,
                where each sequence contains C{ns} steps.
                If the angle is less than 90 degrees, it is evidence that the
                solution is still drifting in some consistent direction and therefore
                not yet at the maximum.  Angles of greater than 90 degrees
                suggest that the optimization is wandering aimlessly near
                a minimum. It will run until a sufficient number
                of large angles are seen since the last BMCMC reset.    
                A similar check is made on individual components of the
                parameter vector.

                @param ns: This controls how carefully if checks that
                        it has really found a minimum.   Large values
                        will take longer but will assure more accurate
                        convergence.
                @type ns: L{int}
                @param acceptable_step: A callable object (i.e. class or function) that returns C{True} or C{False},
                        depending on whether a proposed step is acceptable.
                        See L{mcmc.T_acceptor} for an example.
                @except TooManyLoops: ?
                """
        assert ns > 0
        m = self.x.np
        if acceptable_step is None:
            acceptable_step = step_acceptor(n=m, T0=10.0, T=1.0, ooze=0.5)
        assert acceptable_step is not None
        nchg = 1 + m // 2 + ns
        ndot = 1 + m // 2 + ns
        for i in range(2 + m // 2):
            self.run_to_change(5, acceptable_step=acceptable_step)
            self.logger.add(self.x, self.iter)

        before = self.run_to_change(ns, acceptable_step=acceptable_step)
        self.logger.add(self.x, self.iter)
        mid = self.run_to_change(ns, acceptable_step=acceptable_step)
        self.logger.add(self.x, self.iter)
        es = 0.0
        lock = Thr.allocate_lock()
        xchanged = numpy.zeros(m, numpy.int)
        dotchanged = 0
        last_resetid = self.x.reset_id()
        self.synchronize_start('rtb')
        while self._not_at_bottom(xchanged, nchg, es, dotchanged, ndot):
            try:
                after = self.run_to_change(ns, acceptable_step=acceptable_step)
            except TooManyLoops as x:
                self.synchronize_abort('rtb')
                raise TooManyLoops, ('run_to_bottom: s' % x, self.iter, es, dotchanged, m,
                 numpy.sum(numpy.less(xchanged, nchg)),
                 self.x.current().prms())

            self.logger.add(self.x, self.iter)
            numpy.subtract(xchanged, numpy.sign((after.vec() - mid.vec()) * (mid.vec() - before.vec())), xchanged)
            dotchanged -= _sign(numpy.dot(after.vec() - mid.vec(), mid.vec() - before.vec()))
            es += self.x.ergodic() * ns ** 0.5
            lock.acquire()
            if self.x.reset_id() != last_resetid:
                last_resetid = self.x.reset_id()
                lock.release()
                self.logger.reset()
                es = 0.0
                xchanged[:] = 0
                dotchanged = 0
                self.note('run_to_bottom: Reset: T=%g' % acceptable_step.T(), 1)
            else:
                lock.release()
                self.note('run_to_bottom: T=%g' % acceptable_step.T(), 3)
            before = mid
            mid = after

        self.synchronize_end('rtb')
        return self.iter

    def synchronize_start(self, id):
        pass

    def synchronize_end(self, id):
        pass

    def synchronize_abort(self, id):
        pass

    def note(self, s, lvl):
        if Debug >= lvl:
            print s
            sys.stdout.flush()


class step_acceptor(object):
    """This class defines the annealing schedule when L{mcmc} is used
        as an optimizer.  It corresponds to C{n} extra degrees of freedom
        that exchange probability (i.e. `energy') with each other,  and
        the system to be optimized.
        Over time, the excess log(probability) gradually oozes away.
        """

    def __init__(self, n, T0, ooze, T=1.0, maxT=None):
        """Create a step_acceptor and define it's properties.
                @param n: How many degrees of freedom should the step
                        acceptor store?
                @type n: L{int}
                @param T: What's the temperature of the heat bath?
                        This is the final temperature that the annealing
                        schedule will eventually approach.  Default: C{1.0}.
                @type T: L{float}
                @param ooze: When a step is accepted, one of the degrees of freedom
                        is oozed toward C{T}.  This specifies how far.
                        After C{n/(1-ooze)} steps, these degrees of freedom will
                        have lost most of their excess probability and the temperature
                        will be approaching C{T}.
                @type ooze: L{float}
                @param T0: The starting temperature.
                @type T0: L{float}
                @param maxT: In optimization mode, it's normal for the system being
                        optimized to increase it's log(P).  That dumps log(P) or
                        `energy' into the L{step_acceptor}'s degrees of freedom
                        and raises its temperature.  This parameter lets you define
                        an approximate maximum temperature.   Setting this 
                        may speed up convergence, though there is a corresponding risk
                        of getting trapped in a local minimum.
                @type maxT: L{float} or L{None}
                """
        ooze = float(ooze)
        assert 0.0 <= ooze < 1.0
        T = float(T)
        assert T > 0 and T0 > 0
        assert n > 0
        self._T = T
        self.ooze = ooze
        self.E = [ random.expovariate(1.0) * T0 for i in range(n + 1) ]
        if maxT is not None:
            assert maxT > max(T, T0)
            self.maxT = maxT
        else:
            self.maxT = T0
        return

    def T(self):
        """@return: the current effective temperature.
                @rtype: float
                """
        Tsum = 0.0
        for e in self.E:
            Tsum += e

        return Tsum / len(self.E)

    def __call__(self, delta):
        """@param delta: How much did the candidate step change C{log(P)}?
                @type delta: L{float}
                @return: Whether to accept the candidate step or not.
                @rtype: L{bool}
                """
        n = len(self.E)
        i = random.randrange(n)
        ok = delta > -self.E[i]
        if not ok:
            j = random.randrange(n)
            if j != i:
                Esum = self.E[i] + self.E[j]
                f = random.random()
                self.E[i] = f * Esum
                self.E[j] = Esum - self.E[i]
            return False
        self.E[i] = min((delta + self.E[i]) * self.ooze + self._T * random.expovariate(1.0) * (1.0 - self.ooze), 2 * self.maxT)
        return True

    def __repr__(self):
        return '<step_acceptor(T=%g o=%g) %s>' % (self._T, self.ooze, str(self.E))

    def is_root(self):
        """This is a stub for compatibility with MPI code."""
        return self.rank() == 0

    def size(self):
        """This is a stub for compatibility with MPI code."""
        return 1

    def rank(self):
        """This is a stub for compatibility with MPI code."""
        return 0


def make_stepper_from_lov--- This code section failed: ---

 L. 437         0  BUILD_LIST_0          0 
                3  STORE_FAST            5  'lop'

 L. 438         6  BUILD_LIST_0          0 
                9  STORE_FAST            6  'lov'

 L. 439        12  SETUP_LOOP          231  'to 246'
               15  LOAD_FAST             1  'vector_generator'
               18  GET_ITER         
               19  FOR_ITER            223  'to 245'
               22  STORE_FAST            7  'x'

 L. 440        25  LOAD_GLOBAL           0  'type'
               28  LOAD_FAST             7  'x'
               31  CALL_FUNCTION_1       1  None
               34  LOAD_GLOBAL           1  '_NumpyType'
               37  COMPARE_OP            2  ==
               40  POP_JUMP_IF_TRUE     89  'to 89'
               43  LOAD_ASSERT              AssertionError
               46  LOAD_CONST               'Whoops: type=%s vs %s x=%s'
               49  LOAD_GLOBAL           3  'str'
               52  LOAD_GLOBAL           0  'type'
               55  LOAD_FAST             7  'x'
               58  CALL_FUNCTION_1       1  None
               61  CALL_FUNCTION_1       1  None
               64  LOAD_GLOBAL           3  'str'
               67  LOAD_GLOBAL           4  '_NumPyType'
               70  CALL_FUNCTION_1       1  None
               73  LOAD_GLOBAL           3  'str'
               76  LOAD_FAST             7  'x'
               79  CALL_FUNCTION_1       1  None
               82  BUILD_TUPLE_3         3 
               85  BINARY_MODULO    
               86  RAISE_VARARGS_2       2  None

 L. 441        89  SETUP_EXCEPT         39  'to 131'

 L. 442        92  LOAD_FAST             5  'lop'
               95  LOAD_ATTR             5  'append'
               98  LOAD_FAST             3  'posn_class'
              101  LOAD_FAST             7  'x'
              104  LOAD_FAST             0  'problem_def'
              107  CALL_FUNCTION_2       2  None
              110  CALL_FUNCTION_1       1  None
              113  POP_TOP          

 L. 443       114  LOAD_FAST             6  'lov'
              117  LOAD_ATTR             5  'append'
              120  LOAD_FAST             7  'x'
              123  CALL_FUNCTION_1       1  None
              126  POP_TOP          
              127  POP_BLOCK        
              128  JUMP_FORWARD         39  'to 170'
            131_0  COME_FROM            89  '89'

 L. 444       131  DUP_TOP          
              132  LOAD_GLOBAL           6  'mcmc'
              135  LOAD_ATTR             7  'NotGoodPosition'
              138  COMPARE_OP           10  exception-match
              141  POP_JUMP_IF_FALSE   169  'to 169'
              144  POP_TOP          
              145  STORE_FAST            8  'xcpt'
              148  POP_TOP          

 L. 445       149  LOAD_GLOBAL           8  'die'
              152  LOAD_ATTR             9  'warn'
              155  LOAD_CONST               'Bad initial position for guess: %s'
              158  LOAD_FAST             8  'xcpt'
              161  BINARY_MODULO    
              162  CALL_FUNCTION_1       1  None
              165  POP_TOP          
              166  JUMP_FORWARD          1  'to 170'
              169  END_FINALLY      
            170_0  COME_FROM           169  '169'
            170_1  COME_FROM           128  '128'

 L. 446       170  LOAD_CONST               2
              173  LOAD_FAST             7  'x'
              176  LOAD_ATTR            10  'shape'
              179  LOAD_CONST               0
              182  BINARY_SUBSCR    
              183  BINARY_ADD       
              184  STORE_FAST            9  'nwp'

 L. 447       187  LOAD_FAST             4  'n'
              190  LOAD_CONST               None
              193  COMPARE_OP            8  is
              196  POP_JUMP_IF_TRUE    211  'to 211'
              199  LOAD_FAST             4  'n'
              202  LOAD_FAST             9  'nwp'
              205  COMPARE_OP            0  <
            208_0  COME_FROM           196  '196'
              208  POP_JUMP_IF_FALSE   220  'to 220'

 L. 448       211  LOAD_FAST             9  'nwp'
              214  STORE_FAST            4  'n'
              217  JUMP_FORWARD          0  'to 220'
            220_0  COME_FROM           217  '217'

 L. 449       220  LOAD_GLOBAL          12  'len'
              223  LOAD_FAST             5  'lop'
              226  CALL_FUNCTION_1       1  None
              229  LOAD_FAST             4  'n'
              232  COMPARE_OP            5  >=
              235  POP_JUMP_IF_FALSE    19  'to 19'

 L. 450       238  BREAK_LOOP       
              239  JUMP_BACK            19  'to 19'
              242  JUMP_BACK            19  'to 19'
              245  POP_BLOCK        
            246_0  COME_FROM            12  '12'

 L. 452       246  LOAD_GLOBAL          12  'len'
              249  LOAD_FAST             6  'lov'
              252  CALL_FUNCTION_1       1  None
              255  LOAD_CONST               2
              258  COMPARE_OP            0  <
              261  POP_JUMP_IF_FALSE   289  'to 289'

 L. 453       264  LOAD_GLOBAL           8  'die'
              267  LOAD_ATTR             9  'warn'
              270  LOAD_CONST               'Not enough data'
              273  CALL_FUNCTION_1       1  None
              276  POP_TOP          

 L. 454       277  LOAD_GLOBAL          13  'ValueError'
              280  LOAD_CONST               'Not enough vectors that are good positions.'
              283  RAISE_VARARGS_2       2  None
              286  JUMP_FORWARD          0  'to 289'
            289_0  COME_FROM           286  '286'

 L. 455       289  LOAD_GLOBAL           6  'mcmc'
              292  LOAD_ATTR            14  'diag_variance'
              295  LOAD_FAST             6  'lov'
              298  CALL_FUNCTION_1       1  None
              301  STORE_FAST           10  'v'

 L. 456       304  LOAD_FAST             2  'mcmc_mod'
              307  LOAD_ATTR            15  'BootStepper'
              310  LOAD_FAST             5  'lop'
              313  LOAD_FAST            10  'v'
              316  CALL_FUNCTION_2       2  None
              319  STORE_FAST           11  'st'

 L. 457       322  LOAD_FAST            11  'st'
              325  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 245


def test():

    def test_logp(x, c):
        return -(x[0] - x[1] ** 2) ** 2 + 0.001 * x[1] ** 2

    x = mcmc.bootstepper(test_logp, numpy.array([0.0, 2.0]), numpy.array([[1.0, 0], [0, 2.0]]))
    thr = stepper(x)
    nsteps = thr.run_to_bottom(acceptable_step=step_acceptor(x.np, T0=5.0, T=1.0, ooze=0.5))
    print '#nsteps', nsteps, 'lopg=', x.current().logp_nocompute()
    assert 0 >= x.current().logp_nocompute() > -10
    assert nsteps < 1200
    for i in range(2):
        print 'RTC'
        thr.run_to_change(2)
        print 'RTE'
        thr.run_to_ergodic(1.0)
        print 'DONE'

    thr.close()


if __name__ == '__main__':
    test()