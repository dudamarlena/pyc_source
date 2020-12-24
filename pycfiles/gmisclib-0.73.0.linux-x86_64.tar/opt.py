# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/opt.py
# Compiled at: 2011-05-13 03:22:43
"""This module is a Levenberg-Marquardt optimizer with
stem-size control for numeric differentiation.
It just needs a function that produces residuals.
It is multi-threaded, so calculations of residuals can
be farmed out to many processors.

UPDATED 12/2009 GPK:   NOT TESTED!
"""
import os, sys, math, random, traceback, threading
from gmisclib import die
from gmisclib import avio
from gmisclib import gpkmisc
from gmisclib import Num
RA = Num.RA
LA = Num.LA

class OptError(RuntimeError):

    def __init__(self, s=None):
        RuntimeError.__init__(self, s)


class NoDownhill(OptError):

    def __init__(self, s=None):
        OptError.__init__(self, s)


class NoDerivative(OptError):

    def __init__(self, s=None):
        OptError.__init__(self, s)


class BadParamError(ValueError):
    """Raised when you give and opt instance some invalid control parameter."""

    def __init__(self, s=None):
        ValueError.__init__(self, s)


class BadResult(OptError):
    """The function to be optimized returns some illegal result.
                For instance, an array of the wrong size or type,
                or it returns None for the initial evaluation."""

    def __init__(self, s=None):
        OptError.__init__(self, s)


def vec_equal(a, b):
    """Check that two Numeric vectors are exactly equal."""
    return Num.alltrue(Num.equal(a, b))


def sumsq(a):
    """This is the overall error measure."""
    return Num.sum(Num.sort(a ** 2))


def maxabs(a):
    """This is used as a measure of how much the function changed as a
        result of a parameter change."""
    absa = Num.absolute(a)
    return absa[Num.argmax(absa)]


def wtf(r_dz, delta, quantum):
    """This shows how important different measurements are to
        the final derivitive estimate.    The weight must be small
        when the change of a parameter is smaller than the quantum
        (i.e. when r_delta < quantum).  It must also be small when
        the change in z is much larger than T (r_dz>>1).
        It is largest when r_dz is about 1.
        """
    z_term = abs(r_dz) / (1.0 + r_dz ** 2)
    if quantum > 0:
        r_delta = delta / quantum
        return r_delta ** 2 / (1.0 + r_delta ** 2) * z_term
    return z_term


def near_duplicate(guess, tmp, quantum):
    for delt, dz in tmp:
        if abs(delt - guess) < 0.5 * quantum:
            return True

    return False


def symmetry_point(tmp, T, quantum):
    """Given a list of (delta, z) in a differentiation,
        pick one more point that makes the differentiation more symmetric.
        This is done by picking a new delta that brings
        sum{delta_i * wtf()} closer to zero,
        where wtf() is the weight given to
        each point in the differentiation.
        """
    sumwd, sumd, sumdzsize, sumwt = (0.0, 0.0, 0.0, 0.0)
    for delt, dz in tmp:
        if dz is not None and delt != 0.0:
            dzsize = maxabs(dz)
            wt = wtf(dzsize / T, delt, quantum)
            sumwt += wt
            sumwd += delt * wt
            sumdzsize += dzsize
            sumd += abs(delt)

    if sumwt <= 0.0:
        return
    else:
        asymmetry = sumwd / sumwt
        dzsize_vs_delt = sumdzsize / sumd
        best = None
        best_asym_after_guess = abs(asymmetry)
        for q in (-0.2, -0.4, -0.5, -0.6, -0.7, -0.8, -0.9, -1.0, -1.1, -1.2, -1.35,
                  -1.5, -1.75, -2, -2.5, -3):
            guess = q * asymmetry
            if near_duplicate(guess, tmp, quantum):
                continue
            wt_guess = wtf(dzsize_vs_delt * guess / T, guess, quantum)
            asym_after_guess = abs(sumwd + guess * wt_guess) / (sumwt + wt_guess)
            if asym_after_guess < best_asym_after_guess:
                best_asym_after_guess = asym_after_guess
                best = q * asymmetry

        return best


def scale_est(tmp, T):
    if len(tmp) < 2:
        die.warn('len(tmp)<2 in scale_est')
        return
    else:
        sumd, sumsts = (0.0, 0.0)
        for delt, dz in tmp:
            if dz is not None:
                sumsts += maxabs(dz)
                sumd += abs(delt)

        if abs(sumsts) < 1e-10:
            die.warn('sumsts is small (%g/%g) in scale_est' % (sumsts, sumd))
        if sumsts == 0.0:
            return 'HUGE'
        s_vs_delt = sumsts / sumd
        return T / s_vs_delt


def explored_region(tmp):
    sumad = 0.0
    for delt, dz in tmp:
        sumad += abs(delt)

    return sumad / len(tmp)


def clz_point(qq, T, quantum):
    """Given a list of (delta, z) tuples in a differentiation attempt,
        find another delta that (a) fills a gap in the sequence,
        (b) is preferably has a sign opposite most of the {delta} values,
        and (c) has a large wtf().
        Points outside the sequence are also considered.
        """
    if len(qq) == 1:
        return
    else:
        FUDGEFACTOR = 2.0
        tmp = qq[:]
        tmp.sort()
        sumd = 0.0
        for delt, dz in tmp:
            if dz is not None:
                wt = wtf(maxabs(dz) / T, delt, quantum)
                sumd += delt * wt

        top = None
        bot = None
        possibilities = []
        for i in range(1, len(tmp)):
            delti, dzi = tmp[i]
            deltim, dzim = tmp[(i - 1)]
            if dzi is None and dzim is None:
                continue
            if dzi is None:
                top = True
                dzc = dzim
            elif dzim is None:
                bot = True
                dzc = dzi
            else:
                dzc = 0.5 * (dzi + dzim)
            ctr = 0.5 * (delti + deltim)
            if not near_duplicate(ctr, tmp, quantum):
                gap = (delti - deltim) / (abs(delti) + abs(deltim) + quantum)
                wtc = wtf(maxabs(dzc) / T, ctr, quantum)
                gap *= math.sqrt(wtc)
                if ctr * sumd < 0:
                    gap *= FUDGEFACTOR
                possibilities.append((gap, ctr))

        if not top and len(tmp) > 1:
            delti, dzi = tmp[(-1)]
            if not dzi is not None:
                raise AssertionError
                deltim, dzim = tmp[(-2)]
                ctr = delti + 0.5 * (delti - deltim)
                if not near_duplicate(ctr, tmp, quantum):
                    gap = (delti - deltim) / (abs(delti) + abs(deltim) + quantum)
                    if abs(delti) > abs(deltim):
                        dzc = dzi * (ctr / delti)
                    else:
                        dzc = dzim * (ctr / deltim)
                    wtc = wtf(maxabs(dzc) / T, ctr, quantum)
                    gap *= math.sqrt(wtc)
                    if ctr * sumd < 0:
                        gap *= FUDGEFACTOR
                    possibilities.append((gap, ctr))
            if not bot and len(tmp) > 1:
                delti, dzi = tmp[0]
                assert dzi is not None
                deltip, dzip = tmp[1]
                ctr = delti - 0.5 * (deltip - delti)
                gap = near_duplicate(ctr, tmp, quantum) or (deltip - delti) / (abs(delti) + abs(deltip) + quantum)
                if abs(delti) > abs(deltip):
                    dzc = dzi * (ctr / delti)
                else:
                    dzc = dzip * (ctr / deltip)
                wtc = wtf(maxabs(dzc) / T, ctr, quantum)
                gap *= math.sqrt(wtc)
                if ctr * sumd < 0:
                    gap *= FUDGEFACTOR
                possibilities.append((gap, ctr))
        if len(possibilities) == 0:
            return
        possibilities.sort()
        return possibilities[(-1)][1]


def deriv_estimate--- This code section failed: ---

 L. 250         0  LOAD_GLOBAL           0  'len'
                3  LOAD_FAST             0  'tmp'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_CONST               2
               12  COMPARE_OP            0  <
               15  POP_JUMP_IF_FALSE    27  'to 27'

 L. 251        18  LOAD_GLOBAL           1  'NoDerivative'
               21  RAISE_VARARGS_1       1  None
               24  JUMP_FORWARD          0  'to 27'
             27_0  COME_FROM            24  '24'

 L. 252        27  LOAD_GLOBAL           2  'Num'
               30  LOAD_ATTR             3  'zeros'
               33  LOAD_FAST             0  'tmp'
               36  LOAD_CONST               0
               39  BINARY_SUBSCR    
               40  LOAD_CONST               1
               43  BINARY_SUBSCR    
               44  LOAD_ATTR             4  'shape'
               47  LOAD_GLOBAL           2  'Num'
               50  LOAD_ATTR             5  'Float'
               53  CALL_FUNCTION_2       2  None
               56  STORE_FAST            3  'sumd'

 L. 253        59  LOAD_CONST               0.0
               62  STORE_FAST            4  'sumwt'

 L. 254        65  SETUP_LOOP          111  'to 179'
               68  LOAD_FAST             0  'tmp'
               71  GET_ITER         
               72  FOR_ITER            103  'to 178'
               75  UNPACK_SEQUENCE_2     2 
               78  STORE_FAST            5  'delt'
               81  STORE_FAST            6  'dz'

 L. 255        84  LOAD_GLOBAL           6  'wtf'
               87  LOAD_GLOBAL           7  'maxabs'
               90  LOAD_FAST             6  'dz'
               93  CALL_FUNCTION_1       1  None
               96  LOAD_FAST             1  'T'
               99  BINARY_DIVIDE    
              100  LOAD_FAST             5  'delt'
              103  LOAD_FAST             2  'quantum'
              106  CALL_FUNCTION_3       3  None
              109  STORE_FAST            7  'wt'

 L. 257       112  LOAD_FAST             6  'dz'
              115  LOAD_FAST             5  'delt'
              118  LOAD_FAST             7  'wt'
              121  BINARY_MULTIPLY  
              122  BINARY_MULTIPLY  
              123  LOAD_ATTR             8  'astype'
              126  LOAD_GLOBAL           2  'Num'
              129  LOAD_ATTR             5  'Float'
              132  CALL_FUNCTION_1       1  None
              135  STORE_FAST            8  'increment'

 L. 258       138  LOAD_GLOBAL           2  'Num'
              141  LOAD_ATTR             9  'add'
              144  LOAD_FAST             3  'sumd'
              147  LOAD_FAST             8  'increment'
              150  LOAD_FAST             3  'sumd'
              153  CALL_FUNCTION_3       3  None
              156  POP_TOP          

 L. 259       157  LOAD_FAST             4  'sumwt'
              160  LOAD_FAST             5  'delt'
              163  LOAD_FAST             5  'delt'
              166  BINARY_MULTIPLY  
              167  LOAD_FAST             7  'wt'
              170  BINARY_MULTIPLY  
              171  INPLACE_ADD      
              172  STORE_FAST            4  'sumwt'
              175  JUMP_BACK            72  'to 72'
              178  POP_BLOCK        
            179_0  COME_FROM            65  '65'

 L. 260       179  LOAD_FAST             4  'sumwt'
              182  LOAD_CONST               0
              185  COMPARE_OP            4  >
              188  POP_JUMP_IF_TRUE    200  'to 200'
              191  LOAD_ASSERT              AssertionError
              194  LOAD_CONST               'Whoops!'
              197  RAISE_VARARGS_2       2  None

 L. 262       200  LOAD_FAST             3  'sumd'
              203  LOAD_FAST             4  'sumwt'
              206  BINARY_DIVIDE    
              207  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 207


def need_more_diff_pts(tmp, T, quantum):
    n = 0
    nT = 0
    nq = 0
    nTl = 0
    for delt, dz in tmp:
        if dz is not None:
            n += 1
            if 0.5 * T < maxabs(dz) < 2 * T:
                nT += 1
            if 0.2 * T < maxabs(dz) < 5 * T:
                nTl += 1
            if abs(delt) > 0.9 * quantum:
                nq += 1

    return n < 3 or nT < 1 or nq < 2 or nTl < 2


def diff_one(x, i, sem):
    """Differentiate z with respect to parameter i.
        We enter this function with the semaphore 'sem' already acquired.
        """
    die.note('differentiating', i)
    z = x.z()
    zraw = x.p.zraw()
    assert z is not None
    delta = x.scale[i]
    v = Num.zeros((x.np,), Num.Float)
    v[i] = 1.0
    tmp = [
     (
      0.0, Num.zeros(z.shape, Num.Float))]
    quantum = x.deriv_quantum[i]
    non_None = 0
    for sign in (-1, 1, -0.5, 0.5, -0.25, 0.25, -0.125, 0.125, -0.0625, 0.0625):
        delta = sign * max(x.scale[i], quantum)
        if near_duplicate(delta, tmp, quantum):
            continue
        q = x.constrain(x.p.p, x.p.p + delta * v, x.args)
        if q is None or vec_equal(q, x.p.p):
            die.warn('Constraint complains: delta=%g' % delta)
            continue
        z1 = prms(q, x.fn, x.args, (sem.id, x.steps), diffparam=i, diffctr=zraw).z()
        if z1 is not None:
            if z1.shape != z.shape:
                sem.release()
                raise BadResult, 'Size mismatch: %s vs. %s' % (str(z1.shape),
                 str(z.shape))
            try:
                delta_z = z1 - z
                non_None += 1
            except OverflowError:
                die.warn('Overflow in differentiation attempt')
                delta_z = None

        tmp.append((delta, delta_z))
        if non_None > 0:
            break

    if len(tmp) < 2:
        sem.release()
        raise NoDerivative, 'len(tmp)<2, initial'
    parity = True
    while need_more_diff_pts(tmp, x.Td(), quantum):
        if parity:
            delta = clz_point(tmp, x.Td(), quantum)
            if delta is None:
                delta = symmetry_point(tmp, x.Td(), quantum)
            else:
                parity = not parity
        else:
            delta = symmetry_point(tmp, x.Td(), quantum)
            if delta is None:
                delta = clz_point(tmp, x.Td(), quantum)
            else:
                parity = not parity
        if delta is None:
            die.warn('Neither symmetry_point nor clz_point')
            break
        q = x.constrain(x.p.p, x.p.p + delta * v, x.args)
        if q is not None and not vec_equal(q, x.p.p):
            z1 = prms(q, x.fn, x.args, (sem.id, x.steps), diffparam=i, diffctr=zraw).z()
            tmp.append((delta, z1 - z))
        else:
            die.warn('Constrain complains 2')

    x.diff[i, :] = deriv_estimate(tmp, x.Td(), quantum)
    newscale = scale_est(tmp, x.Td())
    if newscale == 'HUGE':
        die.info('scale_est is huge on %d %g %s' % (i, x.scale[i], str(tmp)))
        x.newscale[i] = 3.0 * x.scale[i]
    elif newscale is not None:
        x.newscale[i] = gpkmisc.limit(x.scale[i] * 0.1, gpkmisc.geo_mean(x.scale[i], newscale), x.scale[i] * 10.0)
    else:
        die.info('scale_est is None on %d %g %s' % (i, x.scale[i], str(tmp)))
        x.newscale[i] = x.scale[i]
    x.newscale[i] = max(x.newscale[i], quantum)
    x.explored[i] = explored_region(tmp)
    sys.stderr.flush()
    sys.stdout.flush()
    sem.release()
    return


def eval_lambda(processor, a, b, startp, lamb, out, opt):
    rmat = RA.standard_normal(a.shape)
    rsq = Num.matrixmultiply(rmat, Num.transpose(rmat)) / a.shape[0]
    aa = a + rsq * lamb
    try:
        s = LA.solve(aa, b) * opt.scale
    except LA.LinAlgError:
        processor.release()
        return

    newp = opt.constrain(startp.p, startp.p - s, opt.args)
    if newp is None:
        die.warn('eval_lambda: Step outside of valid region')
        pnew = None
    else:
        pnew = prms(newp, opt.fn, opt.args, (processor.id, opt.steps))
        pnew.sumsq()
    out.append((lamb, pnew, rsq))
    processor.release()
    return


def lamb_correct(newscale, scale):
    assert len(newscale.shape) == 1
    assert newscale.shape == scale.shape
    return math.exp(2 * Num.sum(Num.log(newscale / scale)) / newscale.shape[0])


class mysem():
    """This is a semaphore that is automatically released when
                        it is de-allocated.   It also contains a processor ID."""

    def __init__(self, id, sem):
        self.id = id
        self.sem = sem

    def release(self):
        self.sem._release(self.id)
        self.sem = None
        return

    def __del__(self):
        if self.sem:
            self.release()


class semclass():
    """This is a semaphore to control the number of
                        simultaneous computations.  It hands out a
                        mysem class which is used to release the semaphore."""

    def __init__(self, n):
        self.s = threading.Semaphore(n)
        self.p_list = range(n)
        self.nthreads = n

    def acquire(self):
        self.s.acquire()
        tmp = self.p_list.pop(-1)
        return mysem(tmp, self)

    def _release(self, id):
        self.p_list.append(id)
        self.s.release()


_NumType = type(Num.array([1], Num.Float))
_tupletype = type(())
_sequenceType = type([])
_floatType = type(1.0)

def _zarray--- This code section failed: ---

 L. 466         0  LOAD_GLOBAL           0  'type'
                3  LOAD_FAST             0  'z'
                6  CALL_FUNCTION_1       1  None
                9  LOAD_GLOBAL           1  '_NumType'
               12  COMPARE_OP            2  ==
               15  POP_JUMP_IF_FALSE    31  'to 31'

 L. 467        18  LOAD_GLOBAL           2  'Num'
               21  LOAD_ATTR             3  'ravel'
               24  LOAD_FAST             0  'z'
               27  CALL_FUNCTION_1       1  None
               30  RETURN_END_IF    
             31_0  COME_FROM            15  '15'

 L. 468        31  LOAD_GLOBAL           0  'type'
               34  LOAD_FAST             0  'z'
               37  CALL_FUNCTION_1       1  None
               40  LOAD_GLOBAL           4  '_floatType'
               43  COMPARE_OP            2  ==
               46  POP_JUMP_IF_TRUE     58  'to 58'
               49  LOAD_ASSERT              AssertionError
               52  LOAD_CONST               'Opt needs an array of mixed floats and Num arrays'
               55  RAISE_VARARGS_2       2  None

 L. 469        58  LOAD_GLOBAL           2  'Num'
               61  LOAD_ATTR             6  'array'
               64  LOAD_FAST             0  'z'
               67  BUILD_LIST_1          1 
               70  LOAD_GLOBAL           2  'Num'
               73  LOAD_ATTR             7  'Float'
               76  CALL_FUNCTION_2       2  None
               79  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 79


class prms():
    """This class records parameters and caches function evaluations.
                All function evaluations happen here."""

    def __init__(self, p, fn, args, processor, diffparam=None, diffctr=None):
        assert len(p.shape) == 1
        self.p = p
        self.lock = threading.RLock()
        self.fn = fn
        self.args = args
        self.processor = processor
        self.diffparam = diffparam
        self.diffctr = diffctr

    def zraw(self):
        self.lock.acquire()
        if not hasattr(self, 'zr_cache'):
            try:
                self.zr_cache = self.fn(self.p, self.args, self.diffparam, self.diffctr, self.processor)
            except:
                traceback.print_exc(file=sys.stdout)
                die.die('Uncaught exception in self.fn')

        self.lock.release()
        return self.zr_cache

    def z(self):
        self.lock.acquire()
        if not hasattr(self, 'z_cache'):
            z = self.zraw()
            ztype = type(z)
            if z is None:
                self.z_cache = None
            elif ztype == _NumType:
                self.z_cache = Num.ravel(z)
            elif ztype == _sequenceType or ztype == _tupletype:
                self.z_cache = Num.concatenate(map(_zarray, z))
            else:
                raise BadResult, 'Unknown type(%s) returned from function' % repr(type(z))
        self.lock.release()
        return self.z_cache

    def sumsq(self):
        self.lock.acquire()
        if not hasattr(self, 'sumsq_cache'):
            z = self.z()
            if z is None:
                self.sumsq_cache = None
            else:
                self.sumsq_cache = sumsq(z)
        self.lock.release()
        return self.sumsq_cache

    def __len__(self):
        return self.p.shape[0]

    def __str__(self):
        return str(self.p)

    def __repr__(self):
        return repr(self.p)


class LockedList():

    def __init__(self, start=None):
        if start is None:
            self.x = []
        else:
            self.x = start
        self.l = threading.Lock()
        return

    def append(self, x):
        self.l.acquire()
        self.x.append(x)
        self.l.release()

    def __len__(self):
        return len(self.x)

    def pop(self, i=-1):
        self.l.acquire()
        try:
            tmp = self.x.pop(i)
        except:
            self.l.release()
            raise

        self.l.release()
        return tmp

    def items(self):
        self.l.acquire()
        tmp = self.x
        self.l.release()
        return tmp


def _dE(T):
    return random.expovariate(1.0) * T


def anneal_guts(p, rv, T, lamb, sem, opt):
    ossq = p.sumsq()
    if ossq is None:
        die.warn('anneal_guts: ossq=None')
        sem.release()
        return
    else:
        np = len(p)
        eval, evec = LA.eigh(opt.curv)
        r = RA.standard_normal((np,)) * math.sqrt(2 * T / np)
        e = 1.0 / Num.sqrt(eval + lamb)
        s = Num.matrixmultiply(r * e, evec) * opt.curv_scale * opt.active
        q = opt.constrain(p.p, p.p + s, opt.args)
        if q is None:
            die.warn('anneal_guts: started outside constraint region')
            sem.release()
            return
        p = prms(q, opt.fn, opt.args, (sem.id, opt.steps))
        ssq = p.sumsq()
        if ssq is None:
            die.warn('anneal_guts: ssq=None')
            sem.release()
            return
        prediction = sumsq(r)
        if opt.verbose:
            print 'AGUTS: ssq-ossq=', ssq - ossq, 'quad_predict=', prediction, 'lambda=', lamb
        if ssq < ossq + 2 * _dE(T):
            rv.append((p, lamb))
        sys.stdout.flush()
        sem.release()
        return


def _evec_write(log_fd, a_vec, a_val, note):
    Nlim = 500
    o = ['note=%s' % note, 'eigenvalue=%g' % a_val]
    try:
        sq = Num.absolute(a_vec) ** 2
    except OverflowError:
        die.info('note=' + note)
        die.info('a=' + str(a_vec))
        raise

    idx = Num.argsort(sq)
    total = Num.sum(sq)
    ssq = 0.0
    n = 0
    for i in range(idx.shape[0] - 1, -1, -1):
        j = idx[i]
        o.append('c%d=%.3f' % (j, a_vec[j]))
        ssq += sq[j]
        n += 1
        if ssq > total * (1 - n / Nlim):
            break

    log_fd.write('#Evec: ' + ('; ').join(o) + '\n')


def _opt_eval(maybe_fcn, arg):
    if callable(maybe_fcn):
        return maybe_fcn(arg)
    return float(maybe_fcn)


class opt():
    """A class that implements a optimizer.  """

    def __init__(self, p, T, fcn, args=None):
        """Create an optimizer object.
                You can also set the following variables between calls to self.step():
                C{scale}, C{deriv_quantum}, C{T}, C{active}, C{sem}, C{constrain}
                
                @param p: initial parameter vector.
                @param T: temperature for simulated annealing and numeric differentiation.
                @param fcn: fcn(p, args, diffparam, diffctr, processor), where
                        C{p} = parameters,
                        C{args} = arbitrary reference passed to function,
                        C{diffparam} = L{None} (unless differentiating),
                        C{diffctr} = L{None} (unless differentiating),
                        C{processor} = (proc_id, i_steps),
                        where proc_id is in C{range(self.nthreads)}
                        and specifies which processor ought
                        to be assigned to the task, and
                        C{i_steps} is the number of steps the
                        optimization has gone through.
                        The function is assumed to return either a Num Python array
                        or a sequence of arrays and floats, mixed.
                @ivar scale: estimate of the step size to use in differentiation.
                @ivar deriv_quantum: minimum step size used in differentiation.
                @ivar T: simulated annealing temperature.
                @ivar active: vector of which parameters to optimize.  Only the active
                                parameters change their value.
                @ivar sem: a semaphore to control the number of threads to use
                        (if you want to set the # of threads do self.sem = semclass(nnn)).
                @ivar constrain: a function that constrains the step.
                        You can use it to do a constrained fit by having it project
                        the proposed step back into the legal volume.
                        Called as self.constrain(old_prms, proposed_prms, self.args).
                        It returns the constrained step, or None if there isn't any.
                """
        self.fn = fcn
        self.args = args
        self.steps = 0
        if isinstance(p, prms):
            self.p = p
        else:
            self.p = prms(Num.array(p, Num.Float, copy=True), self.fn, self.args, (0, self.steps))
        self.last_p = self.p
        self.np = len(self.p.p)
        self.scale = Num.ones((self.np,), Num.Float)
        self.deriv_quantum = None
        self.T = T
        self.active = Num.ones((self.np,), Num.Int)
        try:
            nthreads = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, AttributeError):
            nthreads = 1

        self.lamb = 1.0
        self.sem = semclass(nthreads)
        self.verbose = 1
        self.constrain = lambda x, y, args: y
        return

    def set_nthreads(self, n):
        """Set the number of simultaneous threads to be allowed.
                Calculations of the residuals are farmed out to threads.
                """
        self.sem = semclass(min(self.np, max(0, n)))

    def z(self):
        """What is the current residual?"""
        return self.p.z()

    def sumsq(self):
        """What is the current error?"""
        return self.p.sumsq()

    def _differentiate(self, prms_to_measure=None):
        """Sets self.diff to the Jacobian matrix.  Jacobian is in real units, with
                no parameter scaling.  Also sets self.scale.

                The differentials with respect to unmeasured parameters are left unchanged
                from whatever they were.  This is good under some circumstances, where
                you might be optimizing just a single (of many) local parameter which only
                affects the solution locally, and you have some global parameters which
                you don't expect to change much as the local parameter changes.
                However, sometimes you might want to zero out self.diff to get rid of
                old information.
                """
        sys.stderr.flush()
        sys.stdout.flush()
        if self.deriv_quantum is None:
            self.deriv_quantum = Num.zeros((self.np,), Num.Float)
        if prms_to_measure is None:
            prms_to_measure = self.active
        zctr = self.z()
        if zctr is None:
            raise BadResult, 'Function returns None at starting point.'
        no = zctr.shape[0]
        self.explored = Num.ones((self.np,), Num.Float)
        self.newscale = Num.ones((self.np,), Num.Float)
        if not hasattr(self, 'diff') or self.diff is None or self.diff.shape != (self.np, no):
            self.diff = None
            self.diff = Num.zeros((self.np, no), Num.Float)
        threads = []
        for i in range(self.np):
            if prms_to_measure[i]:
                processor = self.sem.acquire()
                thr = threading.Thread(target=diff_one, args=(
                 self, i, processor))
                threads.append(thr)
                thr.start()

        for thr in threads:
            thr.join()

        return

    def _diff_update(self, oldp, newp):
        """Adjust the derivitive matrix to match a newly recorded newp.z()
                value.   This is a secant update."""
        if self.verbose:
            print '# diff_update'
        step = newp.p - oldp.p
        step2 = sumsq(step / self.curv_scale)
        if step2 < 1e-10:
            return 0
        chg = newp.z() - oldp.z()
        chg_sz = sumsq(chg)
        ex = Num.matrixmultiply(step, self.diff)
        ex_sz = sumsq(ex)
        cor_sz = sumsq(chg - ex)
        f = chg_sz / (chg_sz + 0.5 * self.Td())
        f *= ex_sz / (ex_sz + cor_sz) * (chg_sz / (chg_sz + cor_sz))
        if self.verbose:
            print '\tf=', f
        if self.verbose:
            print '\tchange in z=', chg_sz, 'expected=', ex_sz, 'correction=', cor_sz
        correction = Num.outerproduct(step, chg - ex) * (f / step2)
        Num.add(self.diff, correction, self.diff)
        del correction
        self.calc_curv()
        return 1

    def _curv_update(self, oldp, newp):
        """Adjust the curvature matrix to match a newly recorded newp.sumsq()
                value.   This is a secant update."""
        if self.verbose:
            print '# curv_update'
        step = (newp.p - oldp.p) / self.curv_scale
        step2 = sumsq(step)
        EPS = 1e-10
        if step2 < EPS:
            return 0.0
        step_chg = sumsq(newp.z() - oldp.z())
        f = step_chg / (step_chg + 10 * self.Td())
        b = Num.matrixmultiply(self.diff, oldp.z())
        parab = Num.dot(step, Num.matrixmultiply(self.curv, step))
        if self.verbose:
            print '#\tparabolic part:', parab
            print '#\tdownhill part:', 2 * Num.matrixmultiply(step * self.curv_scale, b)
        ex = 2 * Num.matrixmultiply(step * self.curv_scale, b) + parab
        if self.verbose:
            print '#\texpect a change of', ex, 'get', newp.sumsq() - oldp.sumsq()
        delta = newp.sumsq() - oldp.sumsq() - ex
        if delta <= 0:
            return 0.0
            print '#\tdelta=', delta
        correction = Num.outerproduct(step, step) * (f * delta / step2)
        Num.add(self.curv, correction, self.curv)
        return delta

    LOG_NAME = 'a.tmp'

    def _log(self):
        if not hasattr(self, 'log_fd'):
            self.log_fd = open(self.LOG_NAME, 'w')
        return self.log_fd

    def print_ev_diag(self, misc={}, vectors=0):
        log_fd = self._log()
        a = self.curv
        if vectors:
            eval, evec = LA.eigh(a)
        else:
            eval = LA.eigh(a)
            evec = None
        mx_e = gpkmisc.N_maximum(eval)
        o = misc.copy()
        o['Max_EV'] = mx_e
        o['Min_EV'] = gpkmisc.N_minimum(eval)
        lg_thr = mx_e / 10.0
        sm_thr = mx_e / 1000000.0
        o['N_large_ev'] = Num.sum(Num.greater(eval, lg_thr))
        o['large_thr'] = lg_thr
        o['N_small_ev'] = Num.sum(Num.less(eval, sm_thr))
        o['small_thr'] = sm_thr
        o['Median_EV'] = gpkmisc.N_median(eval)
        o['N_sm_lambda'] = Num.sum(Num.less(eval, self.lamb))
        o['lambda'] = self.lamb
        log_fd.write('#EV: ' + avio.concoct(o) + '\n')
        if vectors:
            n = eval.shape[0]
            for i in range(n):
                if eval[i] > lg_thr:
                    _evec_write(log_fd, evec[i, :], eval[i], 'L')
                if eval[i] < sm_thr:
                    _evec_write(log_fd, evec[i, :], eval[i], 'S')

        log_fd.flush()
        return

    def Td(self):
        """This allows the differentiation temperature to be dynamically set."""
        if callable(self.T):
            return self.T(self)
        return float(self.T)

    def dE(self):
        return _dE(self.Td())

    def quick_lambda(self, a, b, startp, lamb, ntries=10):
        if self.verbose:
            print '# quick lambda: lamb=', lamb
        attempt = 0
        bestp, bestl, bestrsq = (None, 0.0, None)
        NTRIES = 3 + int(round(math.sqrt(self.np))) * self.sem.nthreads
        EPS = 1e-13
        ev_sum = Num.trace(a)
        lamb = min(lamb / 5.0, ev_sum * 5.0) * math.exp(-self.sem.nthreads * 0.2)
        rv = LockedList()
        while attempt < NTRIES:
            processor = self.sem.acquire()
            tmp = threading.Thread(target=eval_lambda, args=(
             processor, a, b, startp, lamb, rv, self))
            tmp.start()
            processor = self.sem.acquire()
            while len(rv) > 0:
                bestl1, bestp1, bestrsq1 = rv.pop(0)
                if bestp1 is None:
                    continue
                if bestp1.z() is None:
                    continue
                if bestp is None or bestp1.sumsq() < bestp.sumsq():
                    bestp, bestl, bestrsq = bestp1, bestl1, bestrsq1
                if bestp1.sumsq() < startp.sumsq() + self.dE():
                    attempt = NTRIES
                elif sumsq(bestp1.z() - startp.z()) < 0.2 * self.Td():
                    attempt = NTRIES

            processor.release()
            attempt += 1
            lamb = lamb * 2.0 * math.pow(10.0, 1.0 / self.sem.nthreads) + EPS * ev_sum

        return (
         bestl, bestp, bestrsq)

    def search_with_update(self, lamb, newp):
        if self.verbose:
            print 'search with update: lamb=', lamb, 'ssq=', newp.sumsq()
        self._diff_update(self.p, newp)
        prm_per_proc = float(self.np) / float(self.sem.nthreads)
        tthresh = 2 * int(math.ceil(math.sqrt(prm_per_proc / 7.0)))
        impthresh = newp.sumsq() / prm_per_proc
        tries = 0
        improvement = 0.0
        bestp = newp
        while tries < tthresh:
            if self.verbose:
                print '\tswu: tries=', tries
            b = self.scale * Num.matrixmultiply(self.diff, bestp.z())
            bestl, bestp1, bestrsq1 = self.quick_lambda(self.curv, b, bestp, lamb, 3)
            lamb = max(1e-10, bestl)
            if bestp1 is None:
                if self.verbose:
                    print '\tNone'
                break
            if self.verbose:
                print '\tbestp1=', bestp1.sumsq(), 'bestp=', bestp.sumsq(), 'T=', self.Td()
            if bestp1.sumsq() <= bestp.sumsq():
                self._diff_update(self.p, newp)
                improvement = bestp.sumsq() - bestp1.sumsq()
                if self.verbose:
                    print '\timprovement=', improvement, 'impthresh=', impthresh
                bestp = bestp1
            else:
                improvement = 0.0
            if improvement < self.Td():
                if self.verbose:
                    print '\tNot much better'
                break
            elif improvement <= impthresh:
                tries += 1

        return (
         bestp, bestrsq1)

    def calc_curv(self):
        if self.verbose:
            print 'scale=', self.scale
        a = self.scale[:, Num.NewAxis] * Num.matrixmultiply(self.diff, Num.transpose(self.diff)) * self.scale[Num.NewAxis, :]
        assert a.shape == (self.np, self.np)
        ev_avg = Num.trace(a) / Num.sum(self.active)
        for i in Num.nonzero(1 - self.active):
            a[(i, i)] += ev_avg

        self.curv = a
        self.curv_scale = self.scale

    def measure(self):
        """If you decrease the number of active parameters, it might behoove
                you to set self.diff=None, before you call this function,
                so that old derivitives get flushed.
                """
        self._differentiate()
        self.calc_curv()
        self.last = 'measure'

    def step(self):
        """A minimization step."""
        if not self.Td() > 0:
            raise BadParamError, 'Temperature must be positive.'
        if self.verbose:
            print 'BEGIN STEP'
        self.measure()
        b = self.scale * Num.matrixmultiply(self.diff, self.z())
        self.lamb, bestp, bestrsq = self.quick_lambda(self.curv, b, self.p, self.lamb)
        if bestp is None or bestp.sumsq() is None:
            die.warn('No Downhill, quick_lambda. Will anneal.')
            self.one_anneal(self.Td())
            return
        else:
            if not bestp.sumsq() < self.sumsq():
                die.warn('No downhill after quick_lambda: sumsq %g -> %g' % (
                 self.sumsq(), bestp.sumsq()))
            bestp1, bestrsq1 = self.search_with_update(self.lamb, bestp)
            if bestp is None or bestp1 is not None and bestp1.sumsq() < bestp.sumsq():
                bestp = bestp1
                bestrsq = bestrsq1
            sys.stderr.flush()
            sys.stdout.flush()
            if bestp.sumsq() < self.sumsq() + self.dE():
                self.p = bestp
                self.lambdir = bestrsq
                self.lamb = max(self.lamb * lamb_correct(self.newscale, self.scale), 1e-10)
                self.scale = self.newscale
                self.steps += 1
                self.last = 'step'
            else:
                die.warn('No Downhill, search. Will anneal.')
                self.one_anneal(self.Td())
            return

    def predicted_sumsq_delta(self, last_p):
        """The energy change of a step, assuming you're at the minimum."""
        p_step = self.p.p - last_p.p
        ps = p_step / self.curv_scale
        return Num.dot(ps, Num.matrixmultiply(self.curv, ps))

    def one_anneal(self, T):
        """Take one simulated annealing step, as fast as possible.
                We send all the processors in random directions, and the one
                that reports an acceptable step first is returned.
                Returns 1 on success, 0 if no good step could be found
                in a reasonable number of tries.
                The temperature can also be a function of one argument
                (as an alternative to a float), in which case, the temperature
                is calculated as T(self)."""
        Ta = _opt_eval(T, self)
        attempt = 0
        NTRIES = 3 + int(round(math.sqrt(self.np))) * self.sem.nthreads
        EPS = 1e-13
        lamb = self.lamb / 30.0 + EPS * Num.trace(self.curv)
        rv = LockedList()
        self.last = 'anneal'
        while attempt < NTRIES:
            processor = self.sem.acquire()
            tmp = threading.Thread(target=anneal_guts, args=(
             self.p, rv, Ta, lamb, processor, self))
            tmp.start()
            processor = self.sem.acquire()
            if len(rv) > 0:
                processor.release()
                self.p, rlamb = rv.pop(0)
                self.lamb = math.sqrt(rlamb * self.lamb)
                return 1
            processor.release()
            attempt += 1
            lamb *= math.pow(3.0, 1.0 / self.sem.nthreads)

        die.warn('simulated annealing fails after %d attempts' % attempt)
        return 0

    def terminate(self):
        """Returns number between 0 and 1 if the optimization seems finished.
                Returns -1 if it's clearly not done yet.
                This is designed to be called after step(),
                so that both self.p and self.last_p refer to the results
                of downhill steps.
                """
        p_step = self.p.p - self.last_p.p
        step_to_explored = Num.sum(Num.absolute(p_step / self.explored)) / p_step.shape[0]
        small1 = 1.0 / (1 + math.sqrt(step_to_explored))
        if self.verbose:
            print 'TERM: step_to_explored=', step_to_explored
        delta_E = self.last_p.sumsq() - self.sumsq()
        small2 = delta_E < self.Td() / math.sqrt((self.steps + 1) * self.np)
        if self.verbose:
            print 'TERM: last_sumsq=', self.last_p.sumsq(),
            print 'sumsq=', self.sumsq(),
            print 'diff=', self.last_p.sumsq() - self.sumsq()
        predicted = self.predicted_sumsq_delta(self.last_p)
        small3 = predicted < 10 * self.Td()
        if self.verbose:
            print 'TERM: predicted improvement=', predicted, 'T=', self.Td()
            print 'TERM: tests:', small1, small2, small3
        self.last_p = self.p
        if small2 and small3:
            return small1
        return -1.0

    def covariance_under(self):
        """This is an underestimate of covariance.
                Adding in the self.lamb term means that it attempts to
                correct for the nonlinearity of the problem,
                at least along the direction of search.
                """
        c = LA.inv(self.curv + self.lamb * self.lambdir)
        return self.curv_scale[:, Num.NewAxis] * c * self.curv_scale[Num.NewAxis, :]

    def covariance(self):
        """Covariance estimate."""
        try:
            c = LA.inv(self.curv)
        except LA.LinAlgError:
            die.warn('Singular covariance matrix')
            return

        return self.curv_scale[:, Num.NewAxis] * c * self.curv_scale[Num.NewAxis, :]

    def run(self, maxsteps=None, misc={}, Ta=None):
        """This is the normal top-level routine.
                You should feel free to make your own, though."""
        if Ta is None:
            Ta = self.Td()
        term = 0.0
        while term < 3 and (maxsteps is None or self.steps < maxsteps):
            self.step()
            self.print_ev_diag(vectors=1)
            ttmp = self.terminate()
            if ttmp < 0:
                term = term / 2.0
            else:
                term += self.terminate()
            self.print_at(misc=misc)
            if Ta > 0:
                self.one_anneal(Ta)
                self.print_at(misc=misc)

        return

    def print_errbar(self):
        log_fd = self._log()
        c = self.covariance()
        assert c.shape[0] == c.shape[1]
        log_fd.write('#var:')
        for i in range(c.shape[0]):
            log_fd.write(' %6g' % c[(i, i)])

        log_fd.write('\n')
        log_fd.flush()

    def sim_anneal(self, nsteps, Ta=None, misc={}):
        """A top-level simulated annealing routine."""
        if Ta is None:
            Ta = self.Td()
        self.measure()
        self.steps = 0
        no = 1 + self.np / 2
        while nsteps is None or self.steps < nsteps:
            if self.steps % self.np == self.np - 1:
                self.measure()
                self.print_errbar()
                self.print_ev_diag(vectors=1)
            if self.steps % no == no - 1:
                self.print_at(misc=misc)
            self.one_anneal(Ta)
            self.steps += 1

        self.print_at(misc=misc)
        return

    def print_at(self, misc={}):
        """Prints a file to match the old C++ optimizer output."""
        log_fd = self._log()
        log_fd.write('#move:')
        p_step = self.p.p - self.last_p.p
        for i in range(p_step.shape[0]):
            log_fd.write(' %6g' % p_step[i])

        log_fd.write('\n')
        o = misc.copy()
        o['E'] = self.sumsq()
        o['iter'] = self.steps
        o['lambda'] = self.lamb
        o['last'] = self.last
        log_fd.write('# ' + avio.concoct(o) + '\n')
        for i in range(self.p.p.shape[0]):
            log_fd.write(' %g' % self.p.p[i])

        log_fd.write('\n')
        log_fd.flush()


def test1_fcn(p, args, *d):
    return p * (1 + Num.arrayrange(p.shape[0]))


def test1():
    """Linear."""
    p = Num.array([1, 99, -1, 2, 3, 4, 5, 0, 0, -45, 3, 4, 5, 2, 2, 1, 2], Num.Float)
    o = opt(p, 0.0001, test1_fcn)
    o.set_nthreads(1)
    o.scale = Num.ones(p.shape) * 0.1
    o.run()
    print 'p=', o.p
    print 'cov=', o.covariance()


def test1a_fcn(p, args, *d):
    pp = Num.array([p])
    x = Num.matrixmultiply(pp, args)
    assert x.shape[0] == 1
    return x[0]


def _errsize(a, b):
    q = a - b
    n = Num.sum(Num.ravel(a) ** 2) + Num.sum(Num.ravel(b) ** 2)
    s = Num.sum(Num.ravel(q) ** 2) / (0.5 * n)
    return math.sqrt(s)


def test1a():
    """Linear."""
    p = Num.array([-0.2222, 0.1, 0.5, -1, 5, -0.3], Num.Float)
    q = RA.standard_normal((p.shape[0], p.shape[0]))
    qq = Num.matrixmultiply(q, Num.transpose(q))
    o = opt(p, 0.0001, test1a_fcn, args=q)
    o.scale = Num.exp(RA.standard_normal((p.shape[0],)))
    o.set_nthreads(1)
    o.run()
    print 'p=', o.p
    print 'cov=', o.covariance()
    print 'cov_under=', o.covariance_under()
    print 'Inv cov=', LA.inv(o.covariance())
    print 'qq=', qq
    print 'Inv qq=', LA.inv(qq)
    print 'Inv cov_under=', LA.inv(o.covariance_under())
    print 'cov error=', _errsize(o.covariance(), LA.inv(qq))
    print 'curv error=', _errsize(LA.inv(o.covariance()), qq)
    ce = o.covariance_under() - LA.inv(qq)
    print 'ce=', ce
    print 'cov_under error=', _errsize(o.covariance_under(), LA.inv(qq))
    print 'curv_under error=', _errsize(LA.inv(o.covariance_under()), qq)


def test2_fcn(p, args, *d):
    return Num.sin(p) - Num.cos(p)


def test2():
    """Nonlinear"""
    p = Num.array([0, 0.2, 0.4, 0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.77, 0.76, 0.33, 0.01], Num.Float)
    o = opt(p, 0.0001, test2_fcn)
    o.scale = Num.ones(p.shape) * 0.1
    o.run()
    print 'p=', o.p


def test3_fcn(p, args, *d):
    o = Num.zeros(p.shape, Num.Float)
    for i in range(p.shape[0]):
        s = 0.0
        for j in range(i):
            s += p[i] - p[j] * (j + 1)

        o[i] = s + p[i]

    return o


def test3():
    """Linear, but correlated"""
    p = Num.array([0, 0.2, 0.4, 0.1, 0.3, 0.5, 0.6, 0.7, 0.8, 0.77, 0.76, 0.33, 0.01], Num.Float)
    o = opt(p, 0.0001, test3_fcn)
    o.scale = Num.ones(p.shape) * 0.1
    o.run()
    print 'steps=', o.steps
    print 'p=', o.p


def test4_fcn(p, args, *d):
    if p[0] < 0 or p[1] < 0:
        return None
    return [
     (p[0] - p[1]) * 100 + p[0], p[1]]


def test4():
    """Linear, but with a constraint"""
    p = Num.array([1, 0.1], Num.Float)
    o = opt(p, 0.0001, test4_fcn)
    o.set_nthreads(1)
    o.run()
    print 'steps=', o.steps
    print 'p=', o.p


def test5_fcn(p, args, *d):
    o = Num.zeros(p.shape, Num.Float)
    for i in range(p.shape[0]):
        s = 0.0
        for j in range(i):
            s += p[i] - p[j] * (j + 1)

        o[i] = s + p[i]

    if gpkmisc.N_maximum(o) > 30 or gpkmisc.N_minimum(o) < -30:
        return None
    return Num.exp(o) - 1


def test5():
    """Very Nonlinear"""
    p = Num.array([0, 4.2, 1.4, 0.1, 0.8, -1.77, 0.01], Num.Float)
    o = opt(p, 0.0001, test5_fcn)
    o.set_nthreads(1)
    o.verbose = 1
    o.scale = Num.ones(p.shape) * 0.1
    try:
        o.run()
    except NoDownhill as q:
        die.warn('No downhill step:' + str(q))
    except:
        raise

    print 'p=', o.p


def test6_fcn(p, args, *d):
    o = Num.zeros((3, ), Num.Float)
    v = p[0] - p[1] * p[1]
    o[0] = v + 0.001 * p[0]
    o[1] = v + 0.001 * p[1]
    o[2] = v - 0.001 * p[1]
    print 'test_fcn: p=', p, 'o=', o
    return o


def test6():
    """Curved valley."""
    p = Num.array([1, 8], Num.Float)
    o = opt(p, 0.001, test6_fcn)
    o.set_nthreads(1)
    o.scale = Num.ones(p.shape) * 0.1
    try:
        o.run()
    except NoDownhill as q:
        die.warn('No downhill step:' + str(q))
    except:
        raise

    print 'p=', o.p


def _test7_fcn(p, args, *d):
    if p[0] < 0 or p[1] < 0:
        return None
    return [
     (p[0] - p[1]) * 100, p[1] + 1]


def linconst_min(nparam, param, min):
    """Generate a linear constraint to be added onto a list and passed
        to linear_constraint().   This constraint expresses that p[param]>=min."""
    vec = Num.zeros(nparam)
    vec[param] = 1.0
    shift = -1.0 * min
    return (vec, shift)


def linconst_max(nparam, param, max):
    """Generate a linear constraint to be added onto a list and passed
        to linear_constraint().   This constraint expresses that p[param]<=max."""
    vec = Num.zeros(nparam)
    vec[param] = -1.0
    shift = 1.0 * max
    return (vec, shift)


def linear_constraint--- This code section failed: ---

 L.1453         0  LOAD_FAST             1  'np'
                3  LOAD_FAST             0  'op'
                6  BINARY_SUBTRACT  
                7  STORE_FAST            3  'dir'

 L.1454        10  LOAD_FAST             2  'list_of_constraints'
               13  SLICE+0          
               14  STORE_FAST            4  'possibles'

 L.1455        17  SETUP_LOOP          357  'to 377'
               20  LOAD_GLOBAL           0  'len'
               23  LOAD_FAST             4  'possibles'
               26  CALL_FUNCTION_1       1  None
               29  LOAD_CONST               0
               32  COMPARE_OP            4  >
               35  POP_JUMP_IF_FALSE   376  'to 376'

 L.1457        38  LOAD_CONST               None
               41  STORE_FAST            5  'eta'

 L.1458        44  LOAD_CONST               None
               47  STORE_FAST            6  'whichc'

 L.1459        50  SETUP_LOOP          184  'to 237'
               53  LOAD_GLOBAL           2  'range'
               56  LOAD_GLOBAL           0  'len'
               59  LOAD_FAST             4  'possibles'
               62  CALL_FUNCTION_1       1  None
               65  CALL_FUNCTION_1       1  None
               68  GET_ITER         
               69  FOR_ITER            164  'to 236'
               72  STORE_FAST            7  'i'

 L.1460        75  LOAD_FAST             4  'possibles'
               78  LOAD_FAST             7  'i'
               81  BINARY_SUBSCR    
               82  UNPACK_SEQUENCE_2     2 
               85  STORE_FAST            8  'cdir'
               88  STORE_FAST            9  'cdist'

 L.1461        91  LOAD_GLOBAL           3  'Num'
               94  LOAD_ATTR             4  'dot'
               97  LOAD_FAST             0  'op'
              100  LOAD_FAST             8  'cdir'
              103  CALL_FUNCTION_2       2  None
              106  LOAD_FAST             9  'cdist'
              109  BINARY_ADD       
              110  STORE_FAST           10  'distance'

 L.1462       113  LOAD_FAST            10  'distance'
              116  LOAD_CONST               0
              119  COMPARE_OP            0  <
              122  POP_JUMP_IF_FALSE   129  'to 129'

 L.1463       125  LOAD_CONST               None
              128  RETURN_END_IF    
            129_0  COME_FROM           122  '122'

 L.1464       129  LOAD_GLOBAL           3  'Num'
              132  LOAD_ATTR             4  'dot'
              135  LOAD_FAST             8  'cdir'
              138  LOAD_FAST             3  'dir'
              141  CALL_FUNCTION_2       2  None
              144  STORE_FAST           11  'progress'

 L.1465       147  LOAD_FAST            11  'progress'
              150  LOAD_CONST               0
              153  COMPARE_OP            5  >=
              156  POP_JUMP_IF_FALSE   165  'to 165'

 L.1467       159  CONTINUE             69  'to 69'
              162  JUMP_FORWARD          0  'to 165'
            165_0  COME_FROM           162  '162'

 L.1468       165  LOAD_FAST            10  'distance'
              168  UNARY_NEGATIVE   
              169  LOAD_FAST            11  'progress'
              172  BINARY_DIVIDE    
              173  STORE_FAST           12  'new_eta'

 L.1470       176  LOAD_FAST            12  'new_eta'
              179  LOAD_CONST               1
              182  COMPARE_OP            4  >
              185  POP_JUMP_IF_FALSE   194  'to 194'

 L.1472       188  CONTINUE             69  'to 69'
              191  JUMP_FORWARD          0  'to 194'
            194_0  COME_FROM           191  '191'

 L.1473       194  LOAD_FAST             5  'eta'
              197  LOAD_CONST               None
              200  COMPARE_OP            8  is
              203  POP_JUMP_IF_TRUE    218  'to 218'
              206  LOAD_FAST             5  'eta'
              209  LOAD_FAST            12  'new_eta'
              212  COMPARE_OP            4  >
            215_0  COME_FROM           203  '203'
              215  POP_JUMP_IF_FALSE    69  'to 69'

 L.1474       218  LOAD_FAST            12  'new_eta'
              221  STORE_FAST            5  'eta'

 L.1475       224  LOAD_FAST             7  'i'
              227  STORE_FAST            6  'whichc'
              230  JUMP_BACK            69  'to 69'
              233  JUMP_BACK            69  'to 69'
              236  POP_BLOCK        
            237_0  COME_FROM            50  '50'

 L.1476       237  LOAD_FAST             6  'whichc'
              240  LOAD_CONST               None
              243  COMPARE_OP            8  is
              246  POP_JUMP_IF_FALSE   253  'to 253'

 L.1478       249  LOAD_FAST             1  'np'
              252  RETURN_END_IF    
            253_0  COME_FROM           246  '246'

 L.1479       253  LOAD_FAST             4  'possibles'
              256  LOAD_ATTR             5  'pop'
              259  LOAD_FAST             6  'whichc'
              262  CALL_FUNCTION_1       1  None
              265  UNPACK_SEQUENCE_2     2 
              268  STORE_FAST            8  'cdir'
              271  STORE_FAST            9  'cdist'

 L.1481       274  LOAD_FAST             0  'op'
              277  LOAD_FAST             3  'dir'
              280  LOAD_FAST             5  'eta'
              283  BINARY_MULTIPLY  
              284  BINARY_ADD       
              285  STORE_FAST            1  'np'

 L.1483       288  LOAD_GLOBAL           6  'abs'
              291  LOAD_GLOBAL           3  'Num'
              294  LOAD_ATTR             4  'dot'
              297  LOAD_FAST             1  'np'
              300  LOAD_FAST             8  'cdir'
              303  CALL_FUNCTION_2       2  None
              306  LOAD_FAST             9  'cdist'
              309  BINARY_ADD       
              310  CALL_FUNCTION_1       1  None
              313  LOAD_CONST               1e-06
              316  COMPARE_OP            0  <
              319  POP_JUMP_IF_TRUE    331  'to 331'
              322  LOAD_ASSERT              AssertionError
              325  LOAD_CONST               'Should go to edge'
              328  RAISE_VARARGS_2       2  None

 L.1485       331  LOAD_FAST             3  'dir'
              334  LOAD_FAST             8  'cdir'
              337  LOAD_GLOBAL           3  'Num'
              340  LOAD_ATTR             4  'dot'
              343  LOAD_FAST             3  'dir'
              346  LOAD_FAST             8  'cdir'
              349  CALL_FUNCTION_2       2  None
              352  BINARY_MULTIPLY  
              353  LOAD_GLOBAL           3  'Num'
              356  LOAD_ATTR             4  'dot'
              359  LOAD_FAST             8  'cdir'
              362  LOAD_FAST             8  'cdir'
              365  CALL_FUNCTION_2       2  None
              368  BINARY_DIVIDE    
              369  INPLACE_SUBTRACT 
              370  STORE_FAST            3  'dir'
              373  JUMP_BACK            20  'to 20'
              376  POP_BLOCK        
            377_0  COME_FROM            17  '17'

 L.1487       377  LOAD_FAST             1  'np'
              380  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 376


def test7():
    """Constraint."""
    c = [
     (
      Num.array((1, 0), Num.Float), 0), (Num.array((0, 1), Num.Float), 0)]
    p = Num.array([1, 8], Num.Float)
    o = opt(p, 0.001, _test7_fcn)
    o.set_nthreads(1)
    o.constrain = lambda op, np, args, loc=c: linear_constraint(op, np, loc)
    o.run()
    print 'p=', o.p


if __name__ == '__main__':
    test1a()