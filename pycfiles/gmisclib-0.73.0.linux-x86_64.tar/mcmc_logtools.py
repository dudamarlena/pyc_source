# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_logtools.py
# Compiled at: 2011-05-11 16:12:11
import math, numpy, die, Numeric_gpk as NG, mcmc_logger, mcmc_newlogger as LG
FILE_DROP_FAC = 0.2
TRIGGER = 'run_to_bottom finished'

def read_many_files(fnames, uid, Nsamp, tail, trigger):
    """
        @return: a dictionary mapping filenames onto "data" and header information.
                Header information is from the last file read.
                The "data" are L{onelog} class instances that encapsulate
                log information from one log file.
        @rtype: tuple(dict(str:onelog), dict(str:str))
        """
    hdr = {}
    per_fn = {}
    if uid is None:
        for fname in fnames:
            hdr, indexers, logps = mcmc_logger.read_multisample(fname, Nsamp=Nsamp, tail=tail, trigger=trigger)
            per_fn[fname] = onelog(logps, indexers, fname)

    else:
        for fname in fnames:
            try:
                hdr, indexers, logps = LG.read_multi_uid(fname, uid, Nsamp=Nsamp, tail=tail, trigger=trigger)
            except LG.BadFormatError as x:
                try:
                    hdr, statedict, logps = LG.read_human_fmt(fname)
                except LG.BadFormatError as y:
                    raise LG.BadFormatError, 'Unreadable in either format: {%s} or {%s}' % (x, y)

                try:
                    indexers = [
                     statedict[uid]]
                    logps = [logps[uid]]
                except KeyError:
                    raise LG.BadFormatError, 'human format: uid=%s not found' % uid
                else:
                    per_fn[fname] = onelog(logps, indexers, fname)

            except LG.NoDataError as x:
                die.warn('No data in %s: %s' % (fname, x))
            else:
                per_fn[fname] = onelog(logps, indexers, fname)

    return (
     per_fn, hdr)


def get_pmap(per_fn):
    for ol in per_fn.values():
        return ol.indexers[0].map

    raise ValueError, 'No data - cannot get_pmap.'


def indexer_covar(per_fn, sample_selector):
    idxr_map = get_pmap(per_fn)
    ndim = len(idxr_map)
    sum = numpy.zeros((ndim,))
    sw = 0
    for ol, i in sample_selector(per_fn):
        idxr = ol.indexers[i]
        numpy.add(sum, idxr.get_prms(), sum)
        sw += 1

    assert sw > 0
    m = sum / sw
    sum = numpy.zeros((ndim, ndim))
    for ol, i in sample_selector(per_fn):
        idxr = ol.indexers[i]
        delta = idxr.get_prms() - m
        assert len(delta.shape) == 1
        delta2 = numpy.outer(delta, delta)
        assert len(delta2.shape) == 2
        numpy.add(sum, delta2, sum)

    if sw > 1:
        var = sum / (sw - 1)
    else:
        var = None
    return (
     m, var, sw, idxr_map)


def logp_stdev--- This code section failed: ---

 L.  93         0  LOAD_CONST               0
                3  STORE_FAST            2  'sw'

 L.  94         6  LOAD_CONST               0.0
                9  STORE_FAST            3  'slp'

 L.  95        12  SETUP_LOOP           58  'to 73'
               15  LOAD_FAST             1  'sample_selector'
               18  LOAD_FAST             0  'per_fn'
               21  CALL_FUNCTION_1       1  None
               24  GET_ITER         
               25  FOR_ITER             44  'to 72'
               28  UNPACK_SEQUENCE_2     2 
               31  STORE_FAST            4  'ol'
               34  STORE_FAST            5  'i'

 L.  96        37  LOAD_FAST             3  'slp'
               40  LOAD_FAST             4  'ol'
               43  LOAD_ATTR             0  'logps'
               46  LOAD_ATTR             1  'item'
               49  LOAD_FAST             5  'i'
               52  CALL_FUNCTION_1       1  None
               55  INPLACE_ADD      
               56  STORE_FAST            3  'slp'

 L.  97        59  LOAD_FAST             2  'sw'
               62  LOAD_CONST               1
               65  INPLACE_ADD      
               66  STORE_FAST            2  'sw'
               69  JUMP_BACK            25  'to 25'
               72  POP_BLOCK        
             73_0  COME_FROM            12  '12'

 L.  98        73  LOAD_FAST             2  'sw'
               76  LOAD_CONST               0
               79  COMPARE_OP            4  >
               82  POP_JUMP_IF_TRUE     94  'to 94'
               85  LOAD_ASSERT              AssertionError
               88  LOAD_CONST               'No data in average in logp_stdev'
               91  RAISE_VARARGS_2       2  None

 L.  99        94  LOAD_FAST             3  'slp'
               97  LOAD_FAST             2  'sw'
              100  BINARY_DIVIDE    
              101  STORE_FAST            6  'lpavg'

 L. 100       104  LOAD_FAST             2  'sw'
              107  STORE_FAST            7  'n'

 L. 101       110  LOAD_CONST               0.0
              113  STORE_FAST            8  'svar'

 L. 102       116  SETUP_LOOP           56  'to 175'
              119  LOAD_FAST             1  'sample_selector'
              122  LOAD_FAST             0  'per_fn'
              125  CALL_FUNCTION_1       1  None
              128  GET_ITER         
              129  FOR_ITER             42  'to 174'
              132  UNPACK_SEQUENCE_2     2 
              135  STORE_FAST            4  'ol'
              138  STORE_FAST            5  'i'

 L. 103       141  LOAD_FAST             8  'svar'
              144  LOAD_FAST             4  'ol'
              147  LOAD_ATTR             0  'logps'
              150  LOAD_ATTR             1  'item'
              153  LOAD_FAST             5  'i'
              156  CALL_FUNCTION_1       1  None
              159  LOAD_FAST             6  'lpavg'
              162  BINARY_SUBTRACT  
              163  LOAD_CONST               2
              166  BINARY_POWER     
              167  INPLACE_ADD      
              168  STORE_FAST            8  'svar'
              171  JUMP_BACK           129  'to 129'
              174  POP_BLOCK        
            175_0  COME_FROM           116  '116'

 L. 104       175  LOAD_FAST             2  'sw'
              178  LOAD_CONST               1
              181  COMPARE_OP            4  >
              184  POP_JUMP_IF_FALSE   237  'to 237'

 L. 105       187  LOAD_CONST               ('logp',)
              190  LOAD_FAST             6  'lpavg'
              193  LOAD_GLOBAL           3  'math'
              196  LOAD_ATTR             4  'sqrt'
              199  LOAD_FAST             8  'svar'
              202  LOAD_FAST             2  'sw'
              205  BINARY_DIVIDE    
              206  LOAD_GLOBAL           5  'float'
              209  LOAD_FAST             7  'n'
              212  CALL_FUNCTION_1       1  None
              215  BINARY_MULTIPLY  
              216  LOAD_GLOBAL           5  'float'
              219  LOAD_FAST             7  'n'
              222  LOAD_CONST               1
              225  BINARY_SUBTRACT  
              226  CALL_FUNCTION_1       1  None
              229  BINARY_DIVIDE    
              230  CALL_FUNCTION_1       1  None
              233  BUILD_TUPLE_3         3 
              236  RETURN_END_IF    
            237_0  COME_FROM           184  '184'

 L. 106       237  LOAD_CONST               ('logp',)
              240  LOAD_FAST             6  'lpavg'
              243  LOAD_CONST               None
              246  BUILD_TUPLE_3         3 
              249  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_3' instruction at offset 246


def after_convergence(per_fn):
    """This selects which measurements will be used."""
    for ol in per_fn.values():
        if ol.convergence is not None:
            for i in range(ol.convergence, len(ol.indexers)):
                yield (
                 ol, i)

    return


def some_after_convergence(per_fn):
    """This selects which measurements will be used.
        It looks after convergence, then throws out optimizations that haven't
        converged.
        """
    maxes = []
    for ol in per_fn.values():
        if ol.convergence is not None:
            maxes.append(NG.N_maximum(ol.logps[ol.convergence:]))

    ndim = len(get_pmap(per_fn))
    assert ndim > 0
    tol = 6 * math.sqrt(ndim)
    threshold = max(maxes) - tol
    for ol in per_fn.values():
        if ol.convergence is not None:
            for i in range(ol.convergence, len(ol.indexers)):
                if ol.logps.item(i) > threshold:
                    yield (
                     ol, i)

    return


def near_each_max(per_fn):
    """This selects which measurements will be used.
        It looks after convergence, then gives you the best few
        results from each run.
        """
    ndim = len(get_pmap(per_fn))
    assert ndim > 0
    tol = 6 * math.sqrt(ndim)
    for ol in per_fn.values():
        if ol.convergence is not None:
            themax = NG.N_maximum(ol.logps[ol.convergence:])
            threshold = themax - tol
            for i in range(ol.convergence, len(ol.indexers)):
                if ol.logps.item(i) > threshold:
                    yield (
                     ol, i)

    return


def all(per_fn):
    """This selects which measurements will be used."""
    for ol in per_fn.values():
        for i in range(len(ol.indexers)):
            yield (
             ol, i)


def last(per_fn):
    """This selects which measurements will be used."""
    for ol in per_fn.values():
        assert isinstance(ol, onelog)
        yield (ol, len(ol.indexers) - 1)


def each_best(per_fn):
    """This selects which measurements will be used."""
    for ol in per_fn.values():
        if ol.convergence is not None:
            bi = numpy.argmax(ol.logps[ol.convergence:]) + ol.convergence
            yield (ol, bi)

    return


def overall_best(per_fn):
    """This selects which measurements will be used."""
    blp = None
    bol = None
    bi = None
    for ol, i in each_best(per_fn):
        if blp is None or ol.logps.item(i) > blp:
            blp = ol.logps.item(i)
            bol = ol
            bi = i

    yield (
     bol, bi)
    return


def indexer_stdev(per_fn, selector):
    """Return a summary of the properties of the last indexer in each file."""
    mean, covar, n, idxr_map = indexer_covar(per_fn, selector)
    o = []
    for nm, i in idxr_map.items():
        if covar is None:
            std = None
        else:
            std = math.sqrt(covar[(i, i)])
        o.append((nm, mean[i], std))

    return o


def print_index_error(ke):
    print 'Cannot find key= %s in index.' % str(ke.args[0])
    idxr = ke.args[1]
    kl = sorted(idxr.map.keys())
    print 'The index has these keys:'
    for k in kl:
        print 'Key=', idxr._fmt(k)


class onelog:

    def __init__(self, logps, indexers, fname):
        assert len(indexers) == len(logps)
        assert isinstance(logps, numpy.ndarray)
        assert isinstance(indexers, list)
        self.logps = logps
        self.indexers = indexers
        self.fname = fname
        self.convergence = None
        return


def estimate_convergence(per_fn, FileDropFac, Trim=None, Stretch=None):
    mxvs = []
    for k, ol in per_fn.items():
        mxvs.append((max(ol.logps), k))

    mxvs.sort()
    for lp, kk in mxvs:
        print '# max(%s) = %g' % (kk, lp)

    ndrop = int(math.floor(FileDropFac * len(per_fn)))
    keep = [ k for mxlogp, k in mxvs[ndrop:] ]
    for kk in keep:
        per_fn[kk].convergence = 0


def ascii_cmp(a, b):
    """Compares the ASCII form of keys, for sorting purposes.   Does a good
        attempt at ASCII ordering for strings and numeric ordering for numbers.
        """
    asp = a.split(',')
    bsp = b.split(',')
    return key_cmp(asp, bsp)


def key_cmp(a, b):
    """Compares the tuple form of keys, for sorting purposes.   Does a good
        attempt at ASCII ordering for strings and numeric ordering for numbers.
        """
    for aa, bb in zip(a, b):
        for fcn in [float, str]:
            try:
                c = cmp(fcn(aa), fcn(bb))
                if c != 0:
                    return c
                break
            except ValueError:
                pass

    return 0