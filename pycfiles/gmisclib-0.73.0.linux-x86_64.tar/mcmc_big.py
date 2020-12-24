# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_big.py
# Compiled at: 2011-05-11 15:13:04
"""An extension of mcmc that includes new stepping algorithms.
"""
from __future__ import with_statement
import math, random, numpy, die, mcmc, avio
from mcmc import Debug
import gpk_lsq
SIGFAC = 2.0
NotGoodPosition = mcmc.NotGoodPosition

def N_maximum(a):
    return a[numpy.argmax(a)].item()


def _parab_interp_guts(x0, y0, x1, y1, x2, y2):
    xx01 = x0 ** 2 - x1 ** 2
    x01 = x0 - x1
    y01 = y0 - y1
    xx21 = x2 ** 2 - x1 ** 2
    x21 = x2 - x1
    y21 = y2 - y1
    b = (y01 * xx21 - y21 * xx01) / (xx21 * x01 - xx01 * x21)
    a = (y01 - b * x01) / xx01
    c = y0 - a * x0 ** 2 - b * x0
    return (a, b, c)


def pairmax(*xy):
    """Finds the (x,y) pair which has the largest y."""
    bestx, besty = xy[0]
    for x, y in xy[1:]:
        if y > besty:
            besty = y
            bestx = x

    return (
     bestx, besty)


def _parab_interp(x0, y0, x1, y1, x2, y2):
    xctr = (x0 + x1 + x2) / 3.0
    x0 -= xctr
    x1 -= xctr
    x2 -= xctr
    a, b, c = _parab_interp_guts(x0, y0, x1, y1, x2, y2)
    mn = min(x0, x1, x2)
    mx = max(x0, x1, x2)
    w = mx - mn
    if a >= 0.0:
        raise mcmc.NoBoot, 'parab: positive curvature'
    else:
        xmin = -b / (2 * a)
        sigma = math.sqrt(-SIGFAC / (2 * a))
    TOOCLOSE = 0.02
    TOOFAR = 2.0
    if xmin < -TOOFAR * w:
        xmin = -TOOFAR * w
    elif xmin > TOOFAR * w:
        xmin = TOOFAR * w
    if sigma > TOOFAR * w:
        sigma = TOOFAR * w
    else:
        if sigma < 2 * TOOCLOSE * w:
            sigma = 2 * TOOCLOSE * w
        xtmp = random.normalvariate(xmin, sigma)
        while min(abs(xtmp - x0), abs(xtmp - x1), abs(xtmp - x2)) < TOOCLOSE * w:
            xtmp = random.normalvariate(xtmp, sigma)

    return xctr + xtmp


def test():
    a, b, c = _parab_interp_guts(0.0, 1.0, 1.0, 0.0, 2.0, 1.0)
    assert abs(a - 1.0) < 0.001
    assert abs(-b / (2 * a) - 1.0) < 0.001
    assert abs(c - 1.0) < 0.001


def find_closest_p(v, *vp):
    """Searches a list of (v,p) pairs and finds the one whose v
        is closest to the first argument.   Returns
        (v,p) of the closest pair.
        """
    assert len(vp) > 0
    vc, pc = vp[0]
    for vi, pi in vp[1:]:
        if abs(vi - v) < abs(vc - v):
            vc = vi
            pc = pi

    return (
     vc, pc)


def _fast_adjust(moveB, moveV, VFAC, aV, aB, accepted):
    """@note: this breaks the Markov assumption."""
    if numpy.greater(numpy.absolute(moveB), numpy.absolute(moveV)).all():
        aB.inctry(accepted)
    SLOP = 5.0
    if numpy.greater(numpy.absolute(moveB), SLOP * numpy.absolute(moveV) / VFAC).all():
        aV.inctry(0)
    if numpy.greater(numpy.absolute(moveV) / VFAC, SLOP * numpy.absolute(moveB)).all():
        if random.random():
            aV.inctry(1)


class BootStepper(mcmc.BootStepper):

    def __init__(self, lop, v, strategy=mcmc.BootStepper.SSAUTO, maxArchSize=None, parallelSizeDiv=1):
        mcmc.BootStepper.__init__(self, lop, v, strategy=strategy, maxArchSize=maxArchSize, parallelSizeDiv=parallelSizeDiv)

    def step(self):
        mcmc.stepper.step(self)
        Wboot = max(self.archive.distinct_count() - 2, 0)
        WV = self.np
        Wmixed = math.sqrt(Wboot * WV)
        die.info('STEP: sorted=%s strategy=%s' % (self.archive.sorted, self.archive.strategy))
        if self.archive.sorted:
            Wparab = max(self.archive.distinct_count() - 2, 0)
        else:
            Wparab = 0
        if self.np < 30 and (self.archive.sorted or self.archive.strategy != self.SSAMPLE):
            WmultiD = math.sqrt(max(self.archive.distinct_count() - (self.np + 1), 0) * WV)
        else:
            WmultiD = 0
        W = float(Wboot + Wmixed + Wparab + WV + WmultiD)
        Pboot = Wboot / W
        Pmixed = Pboot + Wmixed / W
        Pparab = Pmixed + Wparab / W
        PmultiD = Pparab + WmultiD / W
        again = True
        while again:
            P = random.random()
            try:
                if P < Pboot:
                    accepted = self.step_boot()
                elif P < Pmixed:
                    accepted = self.step_mixed()
                elif P < Pparab:
                    accepted = self.step_parab()
                elif P < PmultiD:
                    accepted = self.step_multiD()
                else:
                    accepted = self.stepV()
            except mcmc.NoBoot as x:
                die.info('NoBoot: %s' % str(x))
                again = True
            else:
                again = False

        return accepted

    def step_mixed(self):
        VFAC = 0.01
        self.steptype = 'step_mixed'
        if len(self.archive) <= 2:
            raise mcmc.NoBoot, 'mixed short archive'
        p1 = self.archive.choose()
        p2 = self.archive.choose()
        if p1.uid() == p2.uid():
            raise mcmc.NoBoot, 'mixed duplicate'
        vsV = self.aV.vs() * VFAC
        if self.archive.distinct_count() >= min(5, self.np_eff):
            vsV *= (self.archive.variance() / self.v.diagonal()) ** (1.0 / 4.0)
        moveB = (p1.vec() - p2.vec()) * self.aB.vs()
        moveV = vsV * VFAC * self.V.sample()
        move = moveB + moveV
        try:
            tmp = self.current().new(move)
            delta = tmp.logp() - self.current().logp()
        except mcmc.NotGoodPosition:
            die.warn('NotGoodPosition')
            return 0

        if self.acceptable(delta):
            accepted = 1
            self._set_current(tmp)
            if Debug > 2:
                die.info('StepMixed: Accepted logp=%g' % tmp.logp_nocompute())
        else:
            self._set_failed(tmp)
            accepted = 0
            self._set_current(self.current())
            if Debug > 2:
                die.info('StepMixed: Rejected logp=%g vs. %g, T=%g' % (
                 tmp.logp_nocompute(), self.current().logp_nocompute(), self.acceptable.T()))
        if self.archive.sorted:
            _fast_adjust(moveB, moveV, VFAC, self.aV, self.aB, accepted)
        return accepted

    def step_parab(self):
        VFAC = 0.01
        self.steptype = 'step_parab'
        if len(self.archive) <= 2:
            raise mcmc.NoBoot, 'parab short archive'
        vsB = self.aB.vs()
        while True:
            vs0 = random.normalvariate(0.0, vsB)
            if abs(vs0) > vsB / 4.0 and abs(vs0 - 1) > vsB / 4.0:
                break

        p1 = self.current()
        p2 = self.archive.choose()
        if p1.uid() == p2.uid():
            raise mcmc.NoBoot, 'parab duplicate'
        vbase, pbase = find_closest_p(vs0, (0.0, p1), (1.0, p2))
        move = (p2.vec() - p1.vec()) * (vs0 - vbase)
        try:
            tmp = pbase.new(move)
            delta = tmp.logp() - self.current().logp()
        except mcmc.NotGoodPosition:
            die.warn('NotGoodPosition2a at %.3f' % vs0)
            return 0

        if self.acceptable(delta):
            if Debug > 2:
                die.info('StepParab Accepted1 at %.3f, logp=%g' % (vs0, tmp.logp_nocompute()))
            self._set_current(tmp)
        else:
            self._set_failed(tmp)
            self._set_current(self.current())
        try:
            vsnew = _parab_interp(0.0, p1.logp(), 1.0, p2.logp(), vs0, tmp.logp())
        except mcmc.NotGoodPosition:
            die.warn('NotGoodPosition preparing for _parab_interp().')
            return 0

        vbase, pbase = find_closest_p(vsnew, (0.0, p1), (1.0, p2), (vs0, tmp))
        moveP = (p2.vec() - p1.vec()) * (vsnew - vbase)
        if random.random() < 0.5:
            moveV = self.aV.vs() * VFAC * self.V.sample()
            move = moveP + moveV
        else:
            move = moveP
            moveV = None
        try:
            tmp = pbase.new(move)
            delta = tmp.logp() - self.current().logp()
        except mcmc.NotGoodPosition:
            die.warn('NotGoodPosition')
            accepted = 0

        if self.acceptable(delta):
            if Debug > 2:
                die.info('StepParab Accepted2 at %.3f, logp=%g' % (vsnew, tmp.logp_nocompute()))
            accepted = 1
            self._set_current(tmp)
        else:
            self._set_failed(tmp)
            accepted = 0
            self._set_current(self.current())
            if Debug > 2:
                die.info('StepParab: Rejected logp=%g vs. %g, T=%g' % (
                 tmp.logp_nocompute(), self.current().logp_nocompute(), self.acceptable.T()))
        return accepted

    def step_multiD(self):
        self.steptype = 'step_multiD'
        if self.archive.distinct_count() <= self.np + 2:
            raise mcmc.NoBoot, 'multiD: archive length too small: %d vs np=%d' % (len(self.archive), self.np)
        n_w_distinct = 2 * self.np
        lop = self.archive.prmlist(n_w_distinct)
        n = 0
        lolp = []
        lop2 = []
        z0 = self.current().logp()
        x0 = self.current().vec()
        vs = numpy.zeros(lop[0].vec().shape)
        n = 0
        lolp = []
        lop2 = []
        for p in lop:
            try:
                lolp.append(p.logp())
                numpy.add(vs, (p.vec() - x0) ** 2, vs)
                lop2.append(p.vec())
                n += 1
            except mcmc.NotGoodPosition:
                pass

        sigx = numpy.sqrt(vs / (n - 1))
        if numpy.less(sigx, 1e-30).any():
            raise mcmc.NoBoot, 'multiD: sigx too small = %s' % str(sigx)
        sz = 0.0
        for lp in lolp:
            sz += abs(z0 - lp)

        sigz = sz / (n - 1)
        if sigz < 0.25 * self.acceptable.T():
            raise mcmc.NoBoot, 'multiD: sigz too small = %g' % sigz
        width = 1 + self.np + self.np * (1 + self.np) // 2
        y = numpy.zeros((len(lolp), 1))
        a = numpy.zeros((len(lolp), width))
        for i, (p, lp) in enumerate(zip(lop2, lolp)):
            y[(i, 0)] = z0 - lp
            pt = (p - x0) / sigx
            a[(i, 0)] = 1.0
            a[i, 1:1 + self.np] = pt
            _unfold(pt, a[i, 1 + self.np:])

        rfactors = None
        nbe = None
        for tries in range(5):
            nbe = None
            try:
                move, rfactors = self._compute_move(a, y, width, x0, sigx)
            except mcmc.NoBoot as nbe:
                pass
            else:
                break

        if nbe:
            raise nbe
        die.info('stepMultiD: plausible step on try %d' % tries)
        try:
            tmp = self.current().new(move)
            delta = tmp.logp() - self.current().logp()
        except mcmc.NotGoodPosition:
            die.warn('NotGoodPosition')
            return 0

        if self.acceptable(delta):
            accepted = 1
            self._set_current(tmp)
            if Debug > 2:
                die.info('StepMultiD: Accepted logp=%g; %s' % (tmp.logp_nocompute(), avio.concoct(rfactors)))
        else:
            self._set_failed(tmp)
            accepted = 0
            self._set_current(self.current())
            if Debug > 2:
                die.info('StepMultiD: Rejected logp=%g; was=%g; T=%g; %s' % (
                 tmp.logp_nocompute(), self.current().logp_nocompute(), self.acceptable.T(),
                 avio.concoct(rfactors)))
        return accepted

    def _compute_move--- This code section failed: ---

 L. 423         0  LOAD_CONST               4.0
                3  STORE_FAST            6  'FARSTEP'

 L. 424         6  LOAD_GLOBAL           0  'math'
                9  LOAD_ATTR             1  'exp'
               12  LOAD_GLOBAL           2  'random'
               15  LOAD_ATTR             3  'expovariate'
               18  LOAD_CONST               0.2
               21  CALL_FUNCTION_1       1  None
               24  UNARY_NEGATIVE   
               25  CALL_FUNCTION_1       1  None
               28  STORE_FAST            7  'rscale'

 L. 425        31  LOAD_GLOBAL           4  '_regularize'
               34  LOAD_FAST             0  'self'
               37  LOAD_ATTR             5  'np'
               40  CALL_FUNCTION_1       1  None
               43  UNPACK_SEQUENCE_3     3 
               46  STORE_FAST            8  'regstr'
               49  STORE_FAST            9  'regtgt'
               52  STORE_FAST           10  'rfactors'

 L. 426        55  LOAD_FAST             7  'rscale'
               58  LOAD_FAST            10  'rfactors'
               61  LOAD_CONST               'rscale'
               64  STORE_SUBSCR     

 L. 427        65  LOAD_GLOBAL           6  'gpk_lsq'
               68  LOAD_ATTR             7  'reg_linear_least_squares'
               71  LOAD_FAST             1  'a'
               74  LOAD_FAST             2  'y'
               77  LOAD_CONST               'regstr'
               80  LOAD_FAST             8  'regstr'
               83  LOAD_CONST               'regtgt'
               86  LOAD_FAST             9  'regtgt'
               89  LOAD_CONST               'rscale'
               92  LOAD_FAST             7  'rscale'
               95  LOAD_CONST               'copy'
               98  LOAD_GLOBAL           8  'False'
              101  CALL_FUNCTION_1026  1026  None
              104  STORE_FAST           11  'lls'

 L. 428       107  SETUP_EXCEPT         28  'to 138'

 L. 429       110  LOAD_FAST            11  'lls'
              113  LOAD_ATTR             9  'sv_reg'
              116  CALL_FUNCTION_0       0  None
              119  STORE_FAST           12  'sv'

 L. 430       122  LOAD_FAST            11  'lls'
              125  LOAD_ATTR            10  'x'
              128  CALL_FUNCTION_0       0  None
              131  STORE_FAST           13  'x'
              134  POP_BLOCK        
              135  JUMP_FORWARD         50  'to 188'
            138_0  COME_FROM           107  '107'

 L. 431       138  DUP_TOP          
              139  LOAD_GLOBAL          11  'numpy'
              142  LOAD_ATTR            12  'linalg'
              145  LOAD_ATTR            12  'linalg'
              148  LOAD_ATTR            13  'LinAlgError'
              151  COMPARE_OP           10  exception-match
              154  POP_JUMP_IF_FALSE   187  'to 187'
              157  POP_TOP          
              158  STORE_FAST           14  'ex'
              161  POP_TOP          

 L. 432       162  LOAD_GLOBAL          14  'mcmc'
              165  LOAD_ATTR            15  'NoBoot'
              168  LOAD_CONST               'multiD: %s in _compute_move'
              171  LOAD_GLOBAL          16  'str'
              174  LOAD_FAST            14  'ex'
              177  CALL_FUNCTION_1       1  None
              180  BINARY_MODULO    
              181  RAISE_VARARGS_2       2  None
              184  JUMP_FORWARD          1  'to 188'
              187  END_FINALLY      
            188_0  COME_FROM           187  '187'
            188_1  COME_FROM           135  '135'

 L. 433       188  LOAD_FAST            13  'x'
              191  LOAD_ATTR            17  'shape'
              194  LOAD_FAST             3  'width'
              197  LOAD_CONST               1
              200  BUILD_TUPLE_2         2 
              203  COMPARE_OP            2  ==
              206  POP_JUMP_IF_TRUE    231  'to 231'
              209  LOAD_ASSERT              AssertionError
              212  LOAD_CONST               'shape=%s'
              215  LOAD_GLOBAL          16  'str'
              218  LOAD_FAST            13  'x'
              221  LOAD_ATTR            17  'shape'
              224  CALL_FUNCTION_1       1  None
              227  BINARY_MODULO    
              228  RAISE_VARARGS_2       2  None

 L. 434       231  LOAD_FAST            13  'x'
              234  LOAD_CONST               1
              237  LOAD_CONST               1
              240  LOAD_FAST             0  'self'
              243  LOAD_ATTR             5  'np'
              246  BINARY_ADD       
              247  BUILD_SLICE_2         2 
              250  LOAD_CONST               0
              253  BUILD_TUPLE_2         2 
              256  BINARY_SUBSCR    
              257  STORE_FAST           15  'c'

 L. 435       260  LOAD_GLOBAL          19  '_refold'
              263  LOAD_FAST            13  'x'
              266  LOAD_CONST               1
              269  LOAD_FAST             0  'self'
              272  LOAD_ATTR             5  'np'
              275  BINARY_ADD       
              276  LOAD_CONST               None
              279  BUILD_SLICE_2         2 
              282  LOAD_CONST               0
              285  BUILD_TUPLE_2         2 
              288  BINARY_SUBSCR    
              289  LOAD_FAST             0  'self'
              292  LOAD_ATTR             5  'np'
              295  CALL_FUNCTION_2       2  None
              298  STORE_FAST           16  'cc'

 L. 438       301  LOAD_FAST            12  'sv'
              304  LOAD_CONST               -1
              307  BINARY_SUBSCR    
              308  LOAD_CONST               1e-06
              311  LOAD_FAST            12  'sv'
              314  LOAD_CONST               0
              317  BINARY_SUBSCR    
              318  BINARY_MULTIPLY  
              319  COMPARE_OP            0  <
              322  POP_JUMP_IF_FALSE   358  'to 358'

 L. 439       325  LOAD_GLOBAL          14  'mcmc'
              328  LOAD_ATTR            15  'NoBoot'
              331  LOAD_CONST               'Sv ratio too extreme: %g/%g'
              334  LOAD_FAST            12  'sv'
              337  LOAD_CONST               -1
              340  BINARY_SUBSCR    
              341  LOAD_FAST            12  'sv'
              344  LOAD_CONST               0
              347  BINARY_SUBSCR    
              348  BUILD_TUPLE_2         2 
              351  BINARY_MODULO    
              352  RAISE_VARARGS_2       2  None
              355  JUMP_FORWARD          0  'to 358'
            358_0  COME_FROM           355  '355'

 L. 440       358  LOAD_GLOBAL          20  '_pick_min'
              361  LOAD_FAST            15  'c'
              364  LOAD_FAST            16  'cc'
              367  LOAD_FAST             0  'self'
              370  LOAD_ATTR            21  'acceptable'
              373  LOAD_ATTR            22  'T'
              376  CALL_FUNCTION_0       0  None
              379  CALL_FUNCTION_3       3  None
              382  LOAD_FAST             5  'sigx'
              385  BINARY_MULTIPLY  
              386  LOAD_FAST             4  'x0'
              389  BINARY_ADD       
              390  LOAD_FAST             0  'self'
              393  LOAD_ATTR            23  'current'
              396  CALL_FUNCTION_0       0  None
              399  LOAD_ATTR            24  'vec'
              402  CALL_FUNCTION_0       0  None
              405  BINARY_SUBTRACT  
              406  STORE_FAST           17  'move'

 L. 441       409  LOAD_GLOBAL          25  'N_maximum'
              412  LOAD_GLOBAL          11  'numpy'
              415  LOAD_ATTR            26  'absolute'
              418  LOAD_FAST            17  'move'
              421  CALL_FUNCTION_1       1  None
              424  LOAD_FAST             5  'sigx'
              427  BINARY_DIVIDE    
              428  CALL_FUNCTION_1       1  None
              431  STORE_FAST           18  'r'

 L. 442       434  LOAD_GLOBAL          27  'die'
              437  LOAD_ATTR            28  'info'
              440  LOAD_CONST               'multiD move= %s (r=%.3f) from %s'
              443  LOAD_FAST            17  'move'
              446  LOAD_FAST            18  'r'
              449  LOAD_FAST             0  'self'
              452  LOAD_ATTR            23  'current'
              455  CALL_FUNCTION_0       0  None
              458  LOAD_ATTR            24  'vec'
              461  CALL_FUNCTION_0       0  None
              464  BUILD_TUPLE_3         3 
              467  BINARY_MODULO    
              468  CALL_FUNCTION_1       1  None
              471  POP_TOP          

 L. 443       472  LOAD_FAST            18  'r'
              475  LOAD_FAST             6  'FARSTEP'
              478  LOAD_CONST               2
              481  BINARY_POWER     
              482  COMPARE_OP            4  >
              485  POP_JUMP_IF_FALSE   507  'to 507'

 L. 444       488  LOAD_GLOBAL          14  'mcmc'
              491  LOAD_ATTR            15  'NoBoot'
              494  LOAD_CONST               'multiD: unreasonably large step: r=%g'
              497  LOAD_FAST            18  'r'
              500  BINARY_MODULO    
              501  RAISE_VARARGS_2       2  None
              504  JUMP_FORWARD         42  'to 549'

 L. 445       507  LOAD_FAST            18  'r'
              510  LOAD_FAST             6  'FARSTEP'
              513  COMPARE_OP            4  >
              516  POP_JUMP_IF_FALSE   549  'to 549'

 L. 446       519  LOAD_GLOBAL          11  'numpy'
              522  LOAD_ATTR            29  'multiply'
              525  LOAD_FAST            17  'move'
              528  LOAD_FAST             6  'FARSTEP'
              531  LOAD_FAST            18  'r'
              534  BINARY_DIVIDE    
              535  LOAD_CONST               2
              538  BINARY_POWER     
              539  LOAD_FAST            17  'move'
              542  CALL_FUNCTION_3       3  None
              545  POP_TOP          
              546  JUMP_FORWARD          0  'to 549'
            549_0  COME_FROM           546  '546'
            549_1  COME_FROM           504  '504'

 L. 447       549  LOAD_FAST            17  'move'
              552  LOAD_FAST            10  'rfactors'
              555  BUILD_TUPLE_2         2 
              558  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 558


def _unfold(p, rv):
    n = p.shape[0] * (p.shape[0] + 1) // 2
    assert rv.shape == (n,)
    k = 0
    for i in range(p.shape[0]):
        for j in range(p.shape[0]):
            if i <= j:
                rv[k] = p[i] * p[j]
                k += 1

    assert k == n


def _refold(m, n):
    assert len(m.shape) == 1
    assert n * (n + 1) // 2 == m.shape[0]
    rv = numpy.zeros((n, n))
    k = 0
    for i in range(n):
        for j in range(n):
            if i <= j:
                rv[(i, j)] = m[k]
                rv[(j, i)] = m[k]
                k += 1

    return rv


def _regularize(n):
    """This weakly constrains the diagonal elements (the curvatures) to be equal,
        and it more strongly constrains the off-diagonal elements to be zero.
        """
    FORCE_SIMILAR = math.exp(random.normalvariate(-4.0, 3.0))
    m = n * (n + 1) // 2
    sz = 1 + n + m
    regtgt = numpy.zeros((sz, 1))
    regstr = numpy.zeros((sz, sz))
    diag = []
    k = 1 + n
    for i in range(n):
        for j in range(n):
            if i <= j:
                if i == j:
                    regstr[(k, k)] = FORCE_SIMILAR
                    diag.append(k)
                else:
                    regstr[(k, k)] = 1.0
                k += 1

    lmbda = math.exp(random.expovariate(2.0))
    for k1 in diag:
        regtgt[(k1, 0)] = lmbda
        for k2 in diag:
            regstr[(k1, k2)] = -FORCE_SIMILAR
            regstr[(k2, k1)] = -FORCE_SIMILAR

    return (
     regstr, regtgt, {'FORCE_SIMILAR': FORCE_SIMILAR, 'lmbda': lmbda})


def _pick_min(c, cc, T):
    rv = -0.5 * numpy.linalg.tensorsolve(cc, c)
    dzds = numpy.dot(c, rv)
    curv = numpy.dot(numpy.dot(rv, cc), rv)
    if curv <= 0:
        raise mcmc.NoBoot, 'multiD: Negative curvature'
    assert abs(-dzds / (2 * curv) - 1) < 0.01
    sigma = math.sqrt(SIGFAC * T / (2 * curv))
    rv *= random.normalvariate(1.0, sigma)
    return rv


def bootstepper(logp, x, v, c=None, strategy=BootStepper.SSAUTO, fixer=None, repeatable=True):
    """This is (essentially) another interface to the class constructor.
        It's really there for backwards compatibility.
        """
    pd = mcmc.problem_definition_F(logp_fcn=logp, c=c, fixer=fixer)
    position_constructor = [mcmc.position_nonrepeatable, mcmc.position_repeatable][repeatable]
    return BootStepper(mcmc.make_list_of_positions(x, position_constructor, pd), v, strategy=strategy)


diag_variance = mcmc.diag_variance
stepper = mcmc.stepper
problem_definition = mcmc.problem_definition
problem_definition_F = mcmc.problem_definition_F
problem_definition = mcmc.problem_definition
position_repeatable = mcmc.position_repeatable
position_nonrepeatable = mcmc.position_nonrepeatable
position_history_dependent = mcmc.position_history_dependent

def test2d(stepper):
    import dictops
    start = numpy.array([9, 1])
    c = numpy.array([1.0, 0.1])
    V = numpy.identity(len(c), numpy.float)
    x = stepper(mcmc._logp1, start, V, c=c)
    v = numpy.zeros((x.np, x.np))
    n_per_steptype = dictops.dict_of_averages()
    for i in range(1000):
        accepted = x.step()
        n_per_steptype.add(x.steptype, accepted)

    lpsum = 0.0
    lps2 = 0.0
    na = 0
    psum = numpy.zeros((x.np,))
    N = 30000
    nreset = 0
    nsorted = 0
    rid = x.reset_id()
    for i in range(N):
        accepted = x.step()
        na += accepted
        n_per_steptype.add(x.steptype, accepted)
        nsorted += x.archive.sorted
        if x.reset_id() != rid:
            rid = x.reset_id()
            nreset += 1
        lp = x.current().logp()
        lpsum += lp
        lps2 += lp ** 2
        p = x.current().vec()
        numpy.add(psum, p, psum)
        v += numpy.outer(p, p)

    for steptype in n_per_steptype.keys():
        print 'Step %s has %.0f successes out of %.0f trials: %.2f' % (
         steptype, n_per_steptype.get_both(steptype)[0],
         n_per_steptype.get_both(steptype)[1],
         n_per_steptype.get_avg(steptype))

    assert nsorted < N // 30
    assert N // 8 < na < N // 2
    assert nreset < 30
    lpsum /= N
    assert abs(lpsum + 0.5 * x.np) < 0.15
    lps2 /= N - 1
    lpvar = lps2 - lpsum ** 2
    assert abs(lpvar - 0.5 * x.np) < 1.0
    numpy.divide(psum, N, psum)
    assert numpy.alltrue(numpy.less(numpy.absolute(psum), 6.0 / numpy.sqrt(c)))
    numpy.divide(v, N - 1, v)
    for i in range(x.np):
        for j in range(x.np):
            if i == j:
                assert abs(math.log(2 * v[(i, j)] * c[i] * c[j])) < 0.1
            elif not abs(v[(i, j)]) < 20 / (c[i] * c[j]):
                raise AssertionError


if __name__ == '__main__':
    Debug = 3
    mcmc.test(stepper=bootstepper)