# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_newlogger.py
# Compiled at: 2011-05-11 16:11:59
import os, re, cPickle, numpy, die, avio, gpkmisc as GM, dictops, load_mod, mcmc_indexclass as IC
HUGE = 1e+30

def ok(x):
    return -HUGE < x < HUGE


assert ok(1.0)
assert not ok(2 * HUGE)

class WildNumber(ValueError):

    def __init__(self, *s):
        ValueError.__init__(self, *s)


BadFormatError = avio.BadFormatError

class logger_base(object):

    def __init__(self, fd):
        self.writer = avio.writer(fd)

    def flush(self):
        self.writer.flush()

    def close(self):
        self.writer.close()

    def header(self, k, v):
        self.writer.header(k, v)
        self.writer.flush()

    def headers(self, hdict):
        kvl = list(hdict.items())
        kvl.sort()
        for k, v in kvl:
            self.header(k, v)

    def comment(self, comment):
        self.writer.comment(comment)
        self.writer.flush()


def _fmt(x):
    return IC.index_base._fmt(x)


class DBGlogger(logger_base):

    def __init__(self, fd):
        logger_base.__init__(self, fd)

    def add(self, uid, prms, map, logp, iter, extra=None, reason=None):
        """Adds parameters to the log file.
                uid -- which subset of parameters,
                prms -- a vector of the actual numbers,
                map -- a dictionary mapping from parameter names to an index into the prms array.
                logp -- how good is the fit?  log(probability)
                iter -- an integer to keep track of the number of iterations
                """
        if extra is not None:
            tmp = extra.copy()
        else:
            tmp = {}
        if reason is not None:
            tmp['why_logged'] = reason
        tmp.update({'uid': uid, 'iter': iter, 'logp': '%.1f' % logp})
        for nm, i in map.items():
            tmp[_fmt(nm)] = '%.2f' % prms[i]

        self.writer.datum(tmp)
        self.writer.flush()
        return


class logger(logger_base):

    def __init__(self, fd, huge=1e+30):
        """Create a data log.
                @param fd: Where to log the results
                @type fd: file
                @param huge: sets a threshold for throwing L{WildNumber}.
                        If the absolute value of any parameter gets bigger than huge,
                        something is assumed to be wrong.
                @type huge: normally float, but could be numpy.ndarray
                """
        logger_base.__init__(self, fd)
        self.nmmap = {}
        self.HUGE = huge

    def add(self, uid, prms, map, logp, iter, extra=None, reason=None):
        """Adds a set of parameters to the log file.
                @param uid: which subset of parameters,
                @type uid: string
                @param prms: a vector of the actual numbers,
                @type prms: numpy.ndarray
                @param map: a dictionary mapping from parameter names to an index into the prms array.
                @type map: dict
                @param logp: how good is the fit?  log(probability)
                @type logp: float
                @param iter: which iteration is it?
                @type iter: int
                @param extra: any extra information desired.
                @type extra: None or a dictionary.
                """
        deltanm = []
        for nm, i in map.items():
            k = (
             uid, i)
            if k not in self.nmmap or self.nmmap[k] != nm:
                self.nmmap[k] = nm
                deltanm.append((i, nm))

        if extra:
            tmp = extra.copy()
        else:
            tmp = {}
        if reason is not None:
            tmp['why_logged'] = reason
        tmp['uid'] = uid
        tmp['iter'] = iter
        wild = []
        if logp is None or ok(logp):
            tmp['logp'] = '%.2f' % logp
        else:
            wild.append('logp=%s' % str(logp))
        okprm = numpy.greater_equal(self.HUGE, prms) * numpy.greater_equal(prms, -self.HUGE)
        if not okprm.all():
            rmap = dictops.rev1to1(map)
            for i, isok in enumerate(okprm):
                if not isok:
                    wild.append('p%d(%s)=%s' % (i, _fmt(rmap[i]), prms[i]))

        tmp['prms'] = cPickle.dumps(prms, protocol=0)
        tmp['deltanm'] = cPickle.dumps(deltanm, protocol=0)
        self.writer.datum(tmp)
        self.writer.flush()
        if wild:
            raise WildNumber, ('; ').join(wild)
        return


class NoDataError(ValueError):
    """There is not a complete set of data in the log file:
        data from the outer optimizer and at least one full set of inner optimizer
        results.
        """

    def __init__(self, *s):
        ValueError.__init__(self, *s)


class logline(object):
    """This holds the information from one line of a log file.
        For efficiency reasons, some of the data may be stored pickled,
        and should be accessed through C{prms()} or C{logp()}.
        """
    __slots__ = [
     'uid', 'iter', '_logp', '_prms', 'names']

    def __init__(self, uid, iter, logp, prms, names):
        self.uid = uid
        self.iter = int(iter)
        self._logp = logp
        self._prms = prms
        self.names = names

    def prms(self):
        tmp = cPickle.loads(self._prms)
        if len(tmp) != len(self.names):
            raise ValueError, 'Problem unpickling logline: len=%d, should be %d' % (len(tmp), len(self.names))
        return tmp

    def logp(self):
        return float(self._logp)


def readiter(logfd, trigger=None):
    """Reads in one line at a time from a log file.
        This is an iterator.   At every non-comment line, it yields an output.
        @param logfd: a L{file} descriptor for a log file produced by this module.
        @param trigger: this is None or a regular expression that specifies when to start paying
                attention to the data.  If C{trigger} is not None, body
                lines before C{trigger} matches are ignored.   Note that C{trigger}
                is matched to a line with trailing whitespace stripped away.
        @return: (Yields) C{(hdr, x)} where C{hdr} is a dictionary of the header information current
                at that point in the file and C{x} is a L{logline} class containing the current line's
                data.
        @except BadFormatError: ???
        @except KeyError: ???
        """
    if trigger is not None:
        die.info('# Trigger="%s"' % trigger)
        trigger = re.compile('^#\\s*' + trigger)
    hdr = {}
    nmmap = {}
    lineno = 0
    try:
        for line in logfd:
            lineno += 1
            if not line.endswith('\n'):
                break
            line = line.rstrip()
            if line == '':
                continue
            if trigger is not None:
                if trigger.match(line):
                    die.info('Trigger match')
                    trigger = None
            if line.startswith('#'):
                if '=' in line:
                    k, v = line[1:].split('=', 1)
                    hdr[k.strip()] = avio.back(v.strip())
                continue
            a = avio.parse(line)
            uid = a['uid']
            deltanm = cPickle.loads(a['deltanm'])
            try:
                names = nmmap[uid]
            except KeyError:
                names = []
                nmmap[uid] = names

            if len(deltanm) > 0:
                olen = len(names)
                lmax = olen + len(deltanm)
                for i, nm in deltanm:
                    if not 0 <= i < lmax:
                        raise BadFormatError, 'Bad index for deltanm: old=%d i=%d len(names)=%d' % (olen, i, len(names))
                    elif i < len(names):
                        if names[i] is None:
                            names[i] = nm
                        elif names[i] != nm:
                            raise BadFormatError, 'Inconsistent names in slot %d: %s and %s' % (i, names[i], nm)
                    else:
                        names.extend([None] * (1 + i - len(names)))
                        names[i] = nm

                if None in names[olen:]:
                    raise BadFormatError, 'A name is none: %s' % names
                nmmap[uid] = names
            if trigger is None:
                yield (
                 hdr,
                 logline(uid, a['iter'], a['logp'], a['prms'], names))

    except KeyError as x:
        raise BadFormatError, 'Missing key: %s on line %d of %s' % (x, lineno, getattr(logfd, 'name', '?'))
    except BadFormatError as x:
        raise BadFormatError, 'file %s line %d: %s' % (getattr(logfd, 'name', '?'), lineno, str(x))

    if trigger is not None:
        die.warn('Trigger set but never fired: %s' % getattr(logfd, 'name', '???'))
    return


def read_raw(logfd):
    """Read log information in raw line-by-line form."""
    data = []
    allhdrs = None
    for hdr, datum in readiter(logfd):
        data.append(datum)
        allhdrs = hdr

    return (
     allhdrs, data)


def _find_longest_suboptimizer(clidx):
    n = 0
    for k, v in clidx.items():
        lp = len(v.prms())
        if lp > n:
            n = lp

    return n


def _read_currentlist(fname, trigger):
    """Starting from a file name, read in a log file.
        @param fname: name of a (possibly compressed) log file.
        @type fname: str
        @param trigger: where to start in the log file.  See L{readiter}.
        @rtype: C{(list(dict(str:X)), dict(str:str))} where C{X} is a
                L{logline} class containing the data from one line of the log file.
        @return: a list of data groups and header information.
                A data group is a dictionary of information, all from the same iteration.
                For simple optimizations, there is one item in a data group,
                conventionally under the key "UID".
        """
    current = {}
    currentlist = []
    lastiter = -1
    lasthdr = None
    n_in_current = 0
    for hdr, d in readiter(GM.open_compressed(fname), trigger=trigger):
        if d.iter != lastiter and current:
            if lastiter >= 0:
                currentlist.append(current)
                current = {}
            lastiter = d.iter
        current[d.uid] = d
        n_in_current = max(n_in_current, len(current))
        lasthdr = hdr

    if n_in_current > 0 and len(current) == n_in_current:
        currentlist.append(current)
    return (
     currentlist, lasthdr)


def read_log--- This code section failed: ---

 L. 362         0  LOAD_CODE                <code_object sumlogp>
                3  MAKE_FUNCTION_0       0  None
                6  STORE_FAST            2  'sumlogp'

 L. 368         9  LOAD_GLOBAL           0  '_read_currentlist'
               12  LOAD_FAST             0  'fname'
               15  LOAD_CONST               None
               18  CALL_FUNCTION_2       2  None
               21  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST            3  'currentlist'
               27  STORE_FAST            4  'lasthdr'

 L. 370        30  LOAD_GLOBAL           2  'len'
               33  LOAD_FAST             3  'currentlist'
               36  CALL_FUNCTION_1       1  None
               39  LOAD_CONST               0
               42  COMPARE_OP            2  ==
               45  POP_JUMP_IF_FALSE    60  'to 60'

 L. 371        48  LOAD_GLOBAL           3  'NoDataError'
               51  LOAD_FAST             0  'fname'
               54  RAISE_VARARGS_2       2  None
               57  JUMP_FORWARD          0  'to 60'
             60_0  COME_FROM            57  '57'

 L. 373        60  LOAD_FAST             1  'which'
               63  LOAD_CONST               'last'
               66  COMPARE_OP            2  ==
               69  POP_JUMP_IF_FALSE    91  'to 91'

 L. 374        72  LOAD_GLOBAL           2  'len'
               75  LOAD_FAST             3  'currentlist'
               78  CALL_FUNCTION_1       1  None
               81  LOAD_CONST               1
               84  BINARY_SUBTRACT  
               85  STORE_FAST            5  'idx'
               88  JUMP_FORWARD        345  'to 436'

 L. 375        91  LOAD_FAST             1  'which'
               94  LOAD_CONST               'best'
               97  COMPARE_OP            2  ==
              100  POP_JUMP_IF_FALSE   190  'to 190'

 L. 377       103  LOAD_CONST               0
              106  STORE_FAST            5  'idx'

 L. 378       109  LOAD_FAST             2  'sumlogp'
              112  LOAD_FAST             3  'currentlist'
              115  LOAD_FAST             5  'idx'
              118  BINARY_SUBSCR    
              119  CALL_FUNCTION_1       1  None
              122  STORE_FAST            6  'slp'

 L. 379       125  SETUP_LOOP          308  'to 436'
              128  LOAD_GLOBAL           4  'enumerate'
              131  LOAD_FAST             3  'currentlist'
              134  CALL_FUNCTION_1       1  None
              137  GET_ITER         
              138  FOR_ITER             45  'to 186'
              141  UNPACK_SEQUENCE_2     2 
              144  STORE_FAST            7  'i'
              147  STORE_FAST            8  'current'

 L. 380       150  LOAD_FAST             2  'sumlogp'
              153  LOAD_FAST             8  'current'
              156  CALL_FUNCTION_1       1  None
              159  STORE_FAST            9  'tmp'

 L. 381       162  LOAD_FAST             9  'tmp'
              165  LOAD_FAST             6  'slp'
              168  COMPARE_OP            4  >
              171  POP_JUMP_IF_FALSE   138  'to 138'

 L. 382       174  LOAD_FAST             7  'i'
              177  STORE_FAST            5  'idx'
              180  JUMP_BACK           138  'to 138'
              183  JUMP_BACK           138  'to 138'
              186  POP_BLOCK        
            187_0  COME_FROM           125  '125'
              187  JUMP_FORWARD        246  'to 436'

 L. 383       190  LOAD_FAST             1  'which'
              193  LOAD_ATTR             5  'startswith'
              196  LOAD_CONST               'frac'
              199  CALL_FUNCTION_1       1  None
              202  POP_JUMP_IF_FALSE   298  'to 298'

 L. 384       205  LOAD_GLOBAL           6  'float'
              208  LOAD_GLOBAL           7  'GM'
              211  LOAD_ATTR             8  'dropfront'
              214  LOAD_CONST               'frac'
              217  LOAD_FAST             1  'which'
              220  CALL_FUNCTION_2       2  None
              223  CALL_FUNCTION_1       1  None
              226  STORE_FAST           10  'frac'

 L. 385       229  LOAD_CONST               0
              232  LOAD_FAST            10  'frac'
              235  DUP_TOP          
              236  ROT_THREE        
              237  COMPARE_OP            1  <=
              240  JUMP_IF_FALSE_OR_POP   252  'to 252'
              243  LOAD_CONST               1.0
              246  COMPARE_OP            1  <=
              249  JUMP_FORWARD          2  'to 254'
            252_0  COME_FROM           240  '240'
              252  ROT_TWO          
              253  POP_TOP          
            254_0  COME_FROM           249  '249'
              254  POP_JUMP_IF_TRUE    273  'to 273'

 L. 386       257  LOAD_GLOBAL           9  'ValueError'
              260  LOAD_CONST               'Requires 0 <= (frac=%g) <= 1.0'
              263  LOAD_FAST            10  'frac'
              266  BINARY_MODULO    
              267  RAISE_VARARGS_2       2  None
              270  JUMP_FORWARD          0  'to 273'
            273_0  COME_FROM           270  '270'

 L. 387       273  LOAD_GLOBAL          10  'int'
              276  LOAD_GLOBAL           2  'len'
              279  LOAD_FAST             3  'currentlist'
              282  CALL_FUNCTION_1       1  None
              285  LOAD_FAST            10  'frac'
              288  BINARY_MULTIPLY  
              289  CALL_FUNCTION_1       1  None
              292  STORE_FAST            5  'idx'
              295  JUMP_FORWARD        138  'to 436'

 L. 388       298  LOAD_FAST             1  'which'
              301  LOAD_ATTR             5  'startswith'
              304  LOAD_CONST               'index'
              307  CALL_FUNCTION_1       1  None
              310  POP_JUMP_IF_FALSE   423  'to 423'

 L. 389       313  LOAD_GLOBAL          10  'int'
              316  LOAD_GLOBAL           7  'GM'
              319  LOAD_ATTR             8  'dropfront'
              322  LOAD_CONST               'index'
              325  LOAD_FAST             1  'which'
              328  CALL_FUNCTION_2       2  None
              331  CALL_FUNCTION_1       1  None
              334  STORE_FAST            5  'idx'

 L. 390       337  LOAD_GLOBAL          11  'abs'
              340  LOAD_FAST             5  'idx'
              343  CALL_FUNCTION_1       1  None
              346  LOAD_GLOBAL           2  'len'
              349  LOAD_FAST             3  'currentlist'
              352  CALL_FUNCTION_1       1  None
              355  COMPARE_OP            1  <=
              358  POP_JUMP_IF_TRUE    389  'to 389'

 L. 391       361  LOAD_GLOBAL           9  'ValueError'
              364  LOAD_CONST               'Requires abs(idx=%d) <= len(log_items)=%d'
              367  LOAD_FAST             5  'idx'
              370  LOAD_GLOBAL           2  'len'
              373  LOAD_FAST             3  'currentlist'
              376  CALL_FUNCTION_1       1  None
              379  BUILD_TUPLE_2         2 
              382  BINARY_MODULO    
              383  RAISE_VARARGS_2       2  None
              386  JUMP_FORWARD          0  'to 389'
            389_0  COME_FROM           386  '386'

 L. 392       389  LOAD_FAST             5  'idx'
              392  LOAD_CONST               0
              395  COMPARE_OP            0  <
              398  POP_JUMP_IF_FALSE   436  'to 436'

 L. 393       401  LOAD_GLOBAL           2  'len'
              404  LOAD_FAST             3  'currentlist'
              407  CALL_FUNCTION_1       1  None
              410  LOAD_FAST             5  'idx'
              413  BINARY_ADD       
              414  STORE_FAST            5  'idx'
              417  JUMP_ABSOLUTE       436  'to 436'
              420  JUMP_FORWARD         13  'to 436'

 L. 395       423  LOAD_GLOBAL           9  'ValueError'
              426  LOAD_CONST               'Bad choice of which=%s'
              429  LOAD_FAST             1  'which'
              432  BINARY_MODULO    
              433  RAISE_VARARGS_2       2  None
            436_0  COME_FROM           125  '125'
            436_1  COME_FROM           125  '125'
            436_2  COME_FROM           125  '125'
            436_3  COME_FROM            88  '88'

 L. 397       436  LOAD_GLOBAL          12  '_find_longest_suboptimizer'
              439  LOAD_FAST             3  'currentlist'
              442  LOAD_FAST             5  'idx'
              445  BINARY_SUBSCR    
              446  CALL_FUNCTION_1       1  None
              449  LOAD_CONST               1
              452  BINARY_ADD       
              453  STORE_FAST           11  'n'

 L. 399       456  BUILD_MAP_0           0  None
              459  STORE_FAST           12  'logps'

 L. 400       462  BUILD_MAP_0           0  None
              465  STORE_FAST           13  'vlists'

 L. 401       468  BUILD_MAP_0           0  None
              471  STORE_FAST           14  'stepperstate'

 L. 402       474  LOAD_GLOBAL           2  'len'
              477  LOAD_FAST             3  'currentlist'
              480  CALL_FUNCTION_1       1  None
              483  STORE_FAST           15  'lc'

 L. 403       486  LOAD_FAST            15  'lc'
              489  LOAD_CONST               0
              492  COMPARE_OP            4  >
              495  POP_JUMP_IF_TRUE    504  'to 504'
              498  LOAD_ASSERT              AssertionError
              501  RAISE_VARARGS_1       1  None

 L. 404       504  SETUP_LOOP          348  'to 855'
              507  LOAD_FAST             3  'currentlist'
              510  LOAD_FAST             5  'idx'
              513  BINARY_SUBSCR    
              514  LOAD_ATTR            14  'items'
              517  CALL_FUNCTION_0       0  None
              520  GET_ITER         
              521  FOR_ITER            330  'to 854'
              524  UNPACK_SEQUENCE_2     2 
              527  STORE_FAST           16  'k'
              530  STORE_FAST           17  'v'

 L. 407       533  LOAD_GLOBAL          10  'int'
              536  LOAD_GLOBAL          15  'round'
              539  LOAD_FAST             5  'idx'
              542  LOAD_GLOBAL           6  'float'
              545  LOAD_GLOBAL          16  'max'
              548  LOAD_CONST               0
              551  LOAD_FAST            15  'lc'
              554  LOAD_FAST            11  'n'
              557  BINARY_SUBTRACT  
              558  CALL_FUNCTION_2       2  None
              561  CALL_FUNCTION_1       1  None
              564  BINARY_MULTIPLY  
              565  LOAD_GLOBAL           6  'float'
              568  LOAD_FAST            15  'lc'
              571  CALL_FUNCTION_1       1  None
              574  BINARY_DIVIDE    
              575  CALL_FUNCTION_1       1  None
              578  CALL_FUNCTION_1       1  None
              581  STORE_FAST           18  'lo'

 L. 408       584  LOAD_CONST               0
              587  LOAD_FAST            18  'lo'
              590  DUP_TOP          
              591  ROT_THREE        
              592  COMPARE_OP            1  <=
              595  JUMP_IF_FALSE_OR_POP   607  'to 607'
              598  LOAD_FAST            15  'lc'
              601  COMPARE_OP            0  <
              604  JUMP_FORWARD          2  'to 609'
            607_0  COME_FROM           595  '595'
              607  ROT_TWO          
              608  POP_TOP          
            609_0  COME_FROM           604  '604'
              609  POP_JUMP_IF_TRUE    618  'to 618'
              612  LOAD_ASSERT              AssertionError
              615  RAISE_VARARGS_1       1  None

 L. 409       618  LOAD_GLOBAL          17  'min'
              621  LOAD_CONST               2
              624  LOAD_FAST            11  'n'
              627  BINARY_MULTIPLY  
              628  LOAD_FAST            18  'lo'
              631  BINARY_ADD       
              632  LOAD_FAST            15  'lc'
              635  CALL_FUNCTION_2       2  None
              638  STORE_FAST           19  'high'

 L. 410       641  LOAD_FAST            18  'lo'
              644  LOAD_FAST            19  'high'
              647  DUP_TOP          
              648  ROT_THREE        
              649  COMPARE_OP            0  <
              652  JUMP_IF_FALSE_OR_POP   664  'to 664'
              655  LOAD_FAST            15  'lc'
              658  COMPARE_OP            1  <=
              661  JUMP_FORWARD          2  'to 666'
            664_0  COME_FROM           652  '652'
              664  ROT_TWO          
              665  POP_TOP          
            666_0  COME_FROM           661  '661'
              666  POP_JUMP_IF_TRUE    694  'to 694'
              669  LOAD_ASSERT              AssertionError
              672  LOAD_CONST               'lc=%d, lo=%d, idx=%d, n=%d'
              675  LOAD_FAST            15  'lc'
              678  LOAD_FAST            18  'lo'
              681  LOAD_FAST             5  'idx'
              684  LOAD_FAST            11  'n'
              687  BUILD_TUPLE_4         4 
              690  BINARY_MODULO    
              691  RAISE_VARARGS_2       2  None

 L. 411       694  LOAD_GLOBAL          18  'dict'
              697  BUILD_LIST_0          0 
              700  LOAD_GLOBAL           4  'enumerate'
              703  LOAD_FAST            17  'v'
              706  LOAD_ATTR            19  'names'
              709  CALL_FUNCTION_1       1  None
              712  GET_ITER         
              713  FOR_ITER             24  'to 740'
              716  UNPACK_SEQUENCE_2     2 
              719  STORE_FAST            7  'i'
              722  STORE_FAST           20  'key'
              725  LOAD_FAST            20  'key'
              728  LOAD_FAST             7  'i'
              731  BUILD_TUPLE_2         2 
              734  LIST_APPEND           2  None
              737  JUMP_BACK           713  'to 713'
              740  CALL_FUNCTION_1       1  None
              743  STORE_FAST           21  'keymap'

 L. 412       746  LOAD_GLOBAL          20  'IC'
              749  LOAD_ATTR            21  'index'
              752  LOAD_FAST            21  'keymap'
              755  LOAD_CONST               'p'
              758  LOAD_FAST            17  'v'
              761  LOAD_ATTR            22  'prms'
              764  CALL_FUNCTION_0       0  None
              767  LOAD_CONST               'name'
              770  LOAD_GLOBAL          23  'str'
              773  LOAD_FAST            16  'k'
              776  CALL_FUNCTION_1       1  None
              779  CALL_FUNCTION_513   513  None
              782  LOAD_FAST            14  'stepperstate'
              785  LOAD_FAST            16  'k'
              788  STORE_SUBSCR     

 L. 413       789  BUILD_LIST_0          0 
              792  LOAD_FAST             3  'currentlist'
              795  LOAD_FAST            18  'lo'
              798  LOAD_FAST            19  'high'
              801  SLICE+3          
              802  GET_ITER         
              803  FOR_ITER             22  'to 828'
              806  STORE_FAST           22  'c'
              809  LOAD_FAST            22  'c'
              812  LOAD_FAST            16  'k'
              815  BINARY_SUBSCR    
              816  LOAD_ATTR            22  'prms'
              819  CALL_FUNCTION_0       0  None
              822  LIST_APPEND           2  None
              825  JUMP_BACK           803  'to 803'
              828  LOAD_FAST            13  'vlists'
              831  LOAD_FAST            16  'k'
              834  STORE_SUBSCR     

 L. 414       835  LOAD_FAST            17  'v'
              838  LOAD_ATTR            24  'logp'
              841  CALL_FUNCTION_0       0  None
              844  LOAD_FAST            12  'logps'
              847  LOAD_FAST            16  'k'
              850  STORE_SUBSCR     
              851  JUMP_BACK           521  'to 521'
              854  POP_BLOCK        
            855_0  COME_FROM           504  '504'

 L. 415       855  LOAD_FAST             4  'lasthdr'
              858  LOAD_FAST            14  'stepperstate'
              861  LOAD_FAST            13  'vlists'
              864  LOAD_FAST            12  'logps'
              867  BUILD_TUPLE_4         4 
              870  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 854


def read_multilog(fname, Nsamp=10, tail=0.5):
    """Read in a log file, producing a sample of stepperstate information.
        @param tail: Where to start in the file?
                C{tail=0} means that you start at the trigger or beginning.
                C{tail=1-epsilon} means you take just the last tiny bit of the file.
        """
    currentlist, lasthdr = _read_currentlist(fname, None)
    if len(currentlist) == 0:
        raise NoDataError, fname
    lc = len(currentlist)
    stepperstates = []
    nsamp = min(Nsamp, int(lc * (1.0 - tail)))
    assert nsamp > 0
    for i in range(nsamp):
        f = float(i) / float(nsamp)
        aCurrent = currentlist[int((tail + (1.0 - tail) * f) * lc)]
        stepperstate = {}
        lc = len(currentlist)
        assert lc > 0
        for k, v in aCurrent.items():
            keymap = dict([ (key, i) for i, key in enumerate(v.names) ])
            stepperstate[k] = IC.index(keymap, p=v.prms(), name=str(k))

        stepperstates.append(stepperstate)

    return (
     lasthdr, stepperstates)


def read_multi_uid(fname, uid, Nsamp=10, tail=0.0, trigger=None):
    """Read in a log file, selecting information only for a particular UID.
        This *doesn't* read in multiple UIDs, no matter what the name says:
        the "multi" refers to the fact that it gives you multiple samples
        from the log.   In other words, it provides a time-series of the changes
        to the parameters.

        @param Nsamp: the maximum number of samples to extract (or None, or -1).
                None means "as many as are available"; -1 means "as many samples as there are parameters."
        @type Nsamp: L{int} or L{None}.
        @param tail: Where to start in the file?
                C{tail=0} means that you start at the trigger or beginning.
                C{tail=1-epsilon} means you take just the last tiny bit of the file.
        @except NoDataError: When the log file is empty or a trigger is set but not triggered.
        """
    currentlist, lasthdr = _read_currentlist(fname, trigger)
    if len(currentlist) == 0:
        raise NoDataError, fname
    lc = len(currentlist)
    tail = min(tail, 1.0 - 0.5 / lc)
    indexers = []
    nsamp = lc - int(lc * tail)
    if Nsamp is not None and Nsamp == -1:
        Nsamp = currentlist[0][uid].prms().shape[0]
        assert Nsamp > 0
        if Nsamp < nsamp:
            nsamp = Nsamp
    else:
        if Nsamp is not None and Nsamp < nsamp:
            nsamp = Nsamp
        print '# len(currentlist)=', len(currentlist), 'tail=', tail, 'nsamp=', nsamp
        assert nsamp > 0
        logps = numpy.zeros((nsamp,))
        for i in range(nsamp):
            f = float(i) / float(nsamp)
            aCurrent = currentlist[int((tail + (1.0 - tail) * f) * lc)]
            assert len(currentlist) > 0
            keymap = dict([ (key, j) for j, key in enumerate(aCurrent[uid].names) ])
            indexers.append(IC.index(keymap, p=aCurrent[uid].prms(), name=uid))
            logps.itemset(i, aCurrent[uid].logp())

    return (
     lasthdr, indexers, logps)


def read_human_fmt(fname):
    """This reads a more human-readable format, as produced by L{print_log}.
        It can easily be modified with a text editor to change parameters.
        """
    statedict = {}
    logps = {}
    hdr = {}
    lnum = 0
    uid = None
    map = {}
    prms = []
    for line in open(fname, 'r'):
        if not line.endswith('\n'):
            die.warn('Incomplete line - no newline: %d' % (lnum + 1))
            continue
        lnum += 1
        line = line.strip()
        if line == '':
            continue
        elif line.startswith('#'):
            tmp = avio.parse(line[1:])
            if 'uid' in tmp:
                if uid is not None:
                    statedict[uid] = IC.index(map, p=numpy.array(prms, numpy.float), name=uid)
                    map = {}
                    prms = []
                uid = tmp['uid']
                if uid in statedict:
                    raise BadFormatError, 'human format: duplicate uid=%s' % uid
                if 'logP' in tmp:
                    logps[uid] = float(tmp['logP'])
            else:
                hdr.update(tmp)
        else:
            cols = line.strip().split(None, 1)
            print 'line=', line, 'cols=', cols
            if len(cols) != 2:
                raise BadFormatError, 'human format: needs two columns line %d' % lnum
            map[IC.index_base._unfmt(cols[1])] = len(prms)
            try:
                prms.append(float(cols[0]))
            except ValueError:
                raise BadFormatError, 'human format: need number in first column line %d: %s' % (lnum, cols[0])

    statedict[uid] = IC.index(map, p=numpy.array(prms, numpy.float), name=uid)
    return (
     hdr, statedict, logps)


def load_module(phdr):
    try:
        m = load_mod.load_named(os.path.splitext(phdr['model_file'])[0])
    except ImportError:
        m = None

    if m is None:
        m = load_mod.load_named(phdr['model_name'])
    return m


def print_log(fname, which):
    try:
        hdr, stepperstate, vlists, logps = read_log(fname, which)
    except BadFormatError as x:
        die.info('Not main log format: %s' % str(x))
        hdr, stepperstate, logps = read_human_fmt(fname)
        vlists = None

    for k, v in sorted(hdr.items()):
        print '#', avio.concoct({k: v})

    for uid, v in sorted(stepperstate.items()):
        print '#', avio.concoct({'uid': uid, 'logP': logps[uid]})
        for i, pkey, p in sorted(v.i_k_val()):
            print p, v._fmt(pkey)

        print

    return


if __name__ == '__main__':
    import sys
    which = 'last'
    arglist = sys.argv[1:]
    while arglist and arglist[0].startswith('-'):
        arg = arglist.pop(0)
        if arg == '--':
            break
        elif arg == '-last':
            which = 'last'
        elif arg == '-best':
            which = 'best'
        elif arg == '-frac':
            which = 'frac%f' % float(arglist.pop(0))
        elif arg == '-index':
            which = 'index%d' % int(arglist.pop(0))
        else:
            die.die('Unrecognized arg: %s' % arg)

    assert len(arglist) == 1
    fname = arglist.pop(0)
    print_log(fname, which)