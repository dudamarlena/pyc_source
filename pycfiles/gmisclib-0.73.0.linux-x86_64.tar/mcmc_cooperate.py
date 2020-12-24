# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/mcmc_cooperate.py
# Compiled at: 2011-05-11 15:13:41
import socket, random, hashlib, cPickle, g_encode

class Barrier(object):

    def __init__(self, *x):
        """Constructs a barrier from a list of integers.
                """
        if len(x) == 1 and isinstance(x[0], str):
            self.x = tuple([ int(q) for q in x[0].split('.') ])
        else:
            self.x = tuple(x)
        for tmp in self.x:
            if not tmp >= 0:
                raise ValueError, 'Nonpositive component of Barrier: %s' % tmp

    def __cmp__(self, other):
        return cmp(self.x, other.x)

    def __iadd__(self, other):
        if len(other.x) > len(self.x):
            xl = list(other.x)
            for i, x in enumerate(self.x):
                xl[i] += x

        else:
            xl = list(self.x)
            for i, x in enumerate(other.x):
                xl[i] += x

        self.x = tuple(xl)
        return self

    def __repr__(self):
        return ('.').join([ str(q) for q in self.x ])

    def deepen(self, v):
        return Barrier(*(self.x + (v,)))


assert Barrier(12) == Barrier(12)
assert Barrier(11) > Barrier(10)
assert Barrier(1, 3) > Barrier(1, 1)
assert Barrier(1, 3) > Barrier(1)
assert Barrier(2) > Barrier(1, 3)
assert Barrier(2, 1) > Barrier(1, 3)

class Oops(Exception):

    def __init__(self, *s):
        Exception.__init__(self, *s)


class LateToBarrier(Oops):

    def __init__(self, *s):
        Oops.__init__(self, *s)


encoder = g_encode.encoder(regex='[^a-zA-Z0-9<>?,./:";\'{}[\\]!@$^&*()_+=|\\\\-]')

class connection(object):
    e = encoder

    def __init__(self, host, port, Key, jobid):
        self.my_id = None
        self.host = host
        self.port = port
        self.jobid = jobid
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.sock.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, True)
        seed = hash(open('/dev/urandom', 'r').read(16))
        x = hashlib.sha1('%s:%s:%s' % (Key, self.jobid, seed)).hexdigest()
        self.sf = self.sock.makefile('w', 4096)
        self.rf = self.sock.makefile('r', 4096)
        assert self.version()[1] == __version__
        self.send('connect', jobid, seed, x)
        self.flush()
        self.my_id = self.recv()[1]
        return

    def send(self, *s):
        assert s
        self.sf.write((' ').join([ self.e.fwd(str(q)) for q in s ]) + '\n')

    def flush(self):
        self.sf.flush()

    def recv(self):
        tmp = [ self.e.back(q) for q in self.rf.readline().strip().split() ]
        if not tmp:
            raise Oops('Empty response')
        if tmp[0] == 'Fail':
            raise Oops(*tmp[1:])
        return tmp

    def list_ops(self):
        self.send('list_ops', self.jobid, self.my_id)
        self.flush()
        return self.recv()[1:]

    def version(self):
        self.send('version')
        self.flush()
        return [ Barrier(q) for q in self.recv()[1:] ]

    def rank(self):
        """@return: number_of_processes, rank_of_this_process
                @rtype: (int, int)
                """
        self.send('rank', self.jobid, self.my_id)
        self.flush()
        a = self.recv()
        return (int(a[1]), int(a[2]))

    def close(self):
        self.send('leave', self.jobid, self.my_id)
        self.flush()
        self.recv()
        self.my_id = None
        return

    def __del__(self):
        if self.my_id is not None:
            self.close()
        return

    def barrier(self, b, nmin=0, exc=True):
        self.send('barrier', self.jobid, self.my_id, b, nmin)
        self.flush()
        x = self.recv()
        if exc and x[0] != 'OK':
            raise LateToBarrier(x[1])
        if x[0] == 'OK':
            return None
        else:
            return Barrier(x[1])

    def swap_vec(self, logp, v):
        """@return: (logp, vector)
                """
        size = v.shape[0]
        self.send('*set_vector', self.jobid, self.my_id, size, logp, cPickle.dumps(v))
        self.send('get_vector', self.jobid, self.my_id)
        self.flush()
        lp, v = self.recv()[1:]
        return (float(lp), cPickle.loads(v))

    def set(self, *kv):
        assert len(kv) >= 2 and len(kv) % 2 == 0
        self.send('set_info', self.jobid, self.my_id, *kv)
        self.flush()
        self.recv()

    def get_list(self, key):
        self.send('get_info_list', self.jobid, self.my_id, key)
        self.flush()
        return self.recv()[1:]

    def get_combined(self, key, operation):
        self.send('get_info_combined', self.jobid, self.my_id, key, operation)
        self.flush()
        return Unpack[operation](self.recv()[1])

    def spread(self, key, value, barrier, nmin=0):
        self.send('*barrier', self.jobid, self.my_id, barrier.deepen(0), nmin)
        self.send('*set_info', self.jobid, self.my_id, key, value)
        self.send('*barrier', self.jobid, self.my_id, barrier.deepen(1), nmin)
        self.send('get_info_list', self.jobid, self.my_id, key)
        self.flush()
        tmp = self.recv()
        return tmp[1:]

    def get_consensus(self, key, value, barrier, operation, nmin=0):
        self.send('*barrier', self.jobid, self.my_id, barrier.deepen(0), nmin)
        self.send('*set_info', self.jobid, self.my_id, key, value)
        self.send('*barrier', self.jobid, self.my_id, barrier.deepen(1), nmin)
        self.send('get_info_combined', self.jobid, self.my_id, key, operation)
        self.flush()
        return self.recv()[1]


def test0():
    import time
    test = connection(*test_args)
    test.set('a', 'A')
    time.sleep(random.expovariate(1.0))
    test.set('a', 'B')
    time.sleep(random.expovariate(1.0))
    test.barrier(Barrier(2))
    time.sleep(random.expovariate(1.0))
    for x in test.get_list('a'):
        assert x == 'B'

    time.sleep(random.expovariate(1.0))
    test.barrier(Barrier(3))
    test.barrier(Barrier(4))
    test.set('a', 'C')
    test.close()
    print 'Test0 OK'


def test0s():
    import time
    test = connection(*test_args)
    test.set('a', 'A')
    time.sleep(random.expovariate(1.0))
    test.barrier(Barrier(1))
    print 'Barrier 1s'
    time.sleep(random.expovariate(1.0))
    test.barrier(Barrier(1, 3))
    print 'Barrier1.3s'
    time.sleep(random.expovariate(1.0))
    tmp = test.spread('a', 'x', Barrier(1, 3))
    print 'test.spread 0s tmp=', tmp
    for x in test.get_list('a'):
        assert x == 'x'

    time.sleep(random.expovariate(1.0))
    test.barrier(Barrier(3))
    test.set('a', 'B')
    test.close()
    print 'Test0s OK'


def test1--- This code section failed: ---

 L. 227         0  LOAD_CONST               -1
                3  LOAD_CONST               None
                6  IMPORT_NAME           0  'time'
                9  STORE_FAST            0  'time'

 L. 228        12  LOAD_GLOBAL           1  'connection'
               15  LOAD_GLOBAL           2  'test_args'
               18  CALL_FUNCTION_VAR_0     0  None
               21  STORE_FAST            1  'test'

 L. 229        24  LOAD_CONST               'rank='
               27  PRINT_ITEM       
               28  LOAD_FAST             1  'test'
               31  LOAD_ATTR             3  'rank'
               34  CALL_FUNCTION_0       0  None
               37  PRINT_ITEM_CONT  
               38  PRINT_NEWLINE_CONT

 L. 230        39  LOAD_FAST             1  'test'
               42  LOAD_ATTR             4  'set'
               45  LOAD_CONST               'key'
               48  LOAD_CONST               'value'
               51  CALL_FUNCTION_2       2  None
               54  POP_TOP          

 L. 231        55  LOAD_CONST               'value'
               58  LOAD_FAST             1  'test'
               61  LOAD_ATTR             5  'get_list'
               64  LOAD_CONST               'key'
               67  CALL_FUNCTION_1       1  None
               70  COMPARE_OP            6  in
               73  POP_JUMP_IF_TRUE     82  'to 82'
               76  LOAD_ASSERT              AssertionError
               79  RAISE_VARARGS_1       1  None

 L. 232        82  LOAD_FAST             0  'time'
               85  LOAD_ATTR             7  'sleep'
               88  LOAD_GLOBAL           8  'random'
               91  LOAD_ATTR             9  'expovariate'
               94  LOAD_CONST               100.0
               97  CALL_FUNCTION_1       1  None
              100  CALL_FUNCTION_1       1  None
              103  POP_TOP          

 L. 233       104  LOAD_FAST             1  'test'
              107  LOAD_ATTR             4  'set'
              110  LOAD_CONST               'k2'
              113  LOAD_CONST               '2'
              116  LOAD_CONST               'k'
              119  LOAD_CONST               'wahoonie'
              122  CALL_FUNCTION_4       4  None
              125  POP_TOP          

 L. 234       126  LOAD_FAST             1  'test'
              129  LOAD_ATTR            10  'barrier'
              132  LOAD_GLOBAL          11  'Barrier'
              135  LOAD_CONST               1
              138  CALL_FUNCTION_1       1  None
              141  CALL_FUNCTION_1       1  None
              144  POP_TOP          

 L. 235       145  LOAD_CONST               'Barrier 1'
              148  PRINT_ITEM       
              149  PRINT_NEWLINE_CONT

 L. 236       150  LOAD_FAST             0  'time'
              153  LOAD_ATTR             7  'sleep'
              156  LOAD_GLOBAL           8  'random'
              159  LOAD_ATTR             9  'expovariate'
              162  LOAD_CONST               100.0
              165  CALL_FUNCTION_1       1  None
              168  CALL_FUNCTION_1       1  None
              171  POP_TOP          

 L. 237       172  LOAD_FAST             1  'test'
              175  LOAD_ATTR            10  'barrier'
              178  LOAD_GLOBAL          11  'Barrier'
              181  LOAD_CONST               1
              184  LOAD_CONST               1
              187  CALL_FUNCTION_2       2  None
              190  CALL_FUNCTION_1       1  None
              193  POP_TOP          

 L. 238       194  LOAD_FAST             0  'time'
              197  LOAD_ATTR             7  'sleep'
              200  LOAD_GLOBAL           8  'random'
              203  LOAD_ATTR             9  'expovariate'
              206  LOAD_CONST               100.0
              209  CALL_FUNCTION_1       1  None
              212  CALL_FUNCTION_1       1  None
              215  POP_TOP          

 L. 239       216  LOAD_FAST             1  'test'
              219  LOAD_ATTR             4  'set'
              222  LOAD_CONST               'k2'
              225  LOAD_CONST               '1'
              228  LOAD_CONST               'k'
              231  LOAD_CONST               'no_value'
              234  CALL_FUNCTION_4       4  None
              237  POP_TOP          

 L. 240       238  LOAD_FAST             1  'test'
              241  LOAD_ATTR            10  'barrier'
              244  LOAD_GLOBAL          11  'Barrier'
              247  LOAD_CONST               2
              250  CALL_FUNCTION_1       1  None
              253  CALL_FUNCTION_1       1  None
              256  POP_TOP          

 L. 241       257  LOAD_CONST               'Barrier 2'
              260  PRINT_ITEM       
              261  PRINT_NEWLINE_CONT

 L. 242       262  LOAD_FAST             0  'time'
              265  LOAD_ATTR             7  'sleep'
              268  LOAD_GLOBAL           8  'random'
              271  LOAD_ATTR             9  'expovariate'
              274  LOAD_CONST               100.0
              277  CALL_FUNCTION_1       1  None
              280  CALL_FUNCTION_1       1  None
              283  POP_TOP          

 L. 243       284  LOAD_FAST             1  'test'
              287  LOAD_ATTR            10  'barrier'
              290  LOAD_GLOBAL          11  'Barrier'
              293  LOAD_CONST               2
              296  LOAD_CONST               0
              299  LOAD_CONST               1
              302  CALL_FUNCTION_3       3  None
              305  CALL_FUNCTION_1       1  None
              308  POP_TOP          

 L. 244       309  LOAD_FAST             1  'test'
              312  LOAD_ATTR             5  'get_list'
              315  LOAD_CONST               'k2'
              318  CALL_FUNCTION_1       1  None
              321  STORE_FAST            2  'tmp'

 L. 245       324  LOAD_FAST             2  'tmp'
              327  LOAD_CONST               0
              330  BINARY_SUBSCR    
              331  LOAD_CONST               '1'
              334  COMPARE_OP            2  ==
              337  POP_JUMP_IF_TRUE    353  'to 353'
              340  LOAD_ASSERT              AssertionError
              343  LOAD_CONST               'tmp=%s'
              346  LOAD_FAST             2  'tmp'
              349  BINARY_MODULO    
              350  RAISE_VARARGS_2       2  None

 L. 246       353  LOAD_FAST             1  'test'
              356  LOAD_ATTR            10  'barrier'
              359  LOAD_GLOBAL          11  'Barrier'
              362  LOAD_CONST               2
              365  LOAD_CONST               1
              368  CALL_FUNCTION_2       2  None
              371  CALL_FUNCTION_1       1  None
              374  POP_TOP          

 L. 247       375  LOAD_CONST               'Barrier 2.1'
              378  PRINT_ITEM       
              379  PRINT_NEWLINE_CONT

 L. 248       380  LOAD_FAST             1  'test'
              383  LOAD_ATTR             4  'set'
              386  LOAD_CONST               'k2'
              389  LOAD_CONST               '2'
              392  LOAD_CONST               'k'
              395  LOAD_CONST               'wahoonie'
              398  CALL_FUNCTION_4       4  None
              401  POP_TOP          

 L. 249       402  LOAD_FAST             0  'time'
              405  LOAD_ATTR             7  'sleep'
              408  LOAD_GLOBAL           8  'random'
              411  LOAD_ATTR             9  'expovariate'
              414  LOAD_CONST               100.0
              417  CALL_FUNCTION_1       1  None
              420  CALL_FUNCTION_1       1  None
              423  POP_TOP          

 L. 250       424  LOAD_FAST             1  'test'
              427  LOAD_ATTR            10  'barrier'
              430  LOAD_GLOBAL          11  'Barrier'
              433  LOAD_CONST               2
              436  LOAD_CONST               1
              439  LOAD_CONST               1
              442  CALL_FUNCTION_3       3  None
              445  CALL_FUNCTION_1       1  None
              448  POP_TOP          

 L. 251       449  LOAD_FAST             1  'test'
              452  LOAD_ATTR             5  'get_list'
              455  LOAD_CONST               'k'
              458  CALL_FUNCTION_1       1  None
              461  STORE_FAST            2  'tmp'

 L. 252       464  LOAD_FAST             2  'tmp'
              467  LOAD_CONST               0
              470  BINARY_SUBSCR    
              471  LOAD_CONST               'wahoonie'
              474  COMPARE_OP            2  ==
              477  POP_JUMP_IF_TRUE    493  'to 493'
              480  LOAD_ASSERT              AssertionError
              483  LOAD_CONST               'tmp=%s'
              486  LOAD_FAST             2  'tmp'
              489  BINARY_MODULO    
              490  RAISE_VARARGS_2       2  None

 L. 253       493  LOAD_FAST             1  'test'
              496  LOAD_ATTR             4  'set'
              499  LOAD_CONST               'k3'
              502  LOAD_CONST               'x y'
              505  CALL_FUNCTION_2       2  None
              508  POP_TOP          

 L. 254       509  LOAD_CONST               'x y'
              512  LOAD_FAST             1  'test'
              515  LOAD_ATTR             5  'get_list'
              518  LOAD_CONST               'k3'
              521  CALL_FUNCTION_1       1  None
              524  COMPARE_OP            6  in
              527  POP_JUMP_IF_TRUE    536  'to 536'
              530  LOAD_ASSERT              AssertionError
              533  RAISE_VARARGS_1       1  None

 L. 255       536  LOAD_FAST             0  'time'
              539  LOAD_ATTR             7  'sleep'
              542  LOAD_GLOBAL           8  'random'
              545  LOAD_ATTR             9  'expovariate'
              548  LOAD_CONST               100.0
              551  CALL_FUNCTION_1       1  None
              554  CALL_FUNCTION_1       1  None
              557  POP_TOP          

 L. 256       558  LOAD_FAST             1  'test'
              561  LOAD_ATTR            12  'get_combined'
              564  LOAD_CONST               'k2'
              567  LOAD_CONST               'float_median'
              570  CALL_FUNCTION_2       2  None
              573  LOAD_CONST               2.0
              576  COMPARE_OP            2  ==
              579  POP_JUMP_IF_TRUE    588  'to 588'
              582  LOAD_ASSERT              AssertionError
              585  RAISE_VARARGS_1       1  None

 L. 257       588  LOAD_FAST             1  'test'
              591  LOAD_ATTR            10  'barrier'
              594  LOAD_GLOBAL          11  'Barrier'
              597  LOAD_CONST               3
              600  CALL_FUNCTION_1       1  None
              603  CALL_FUNCTION_1       1  None
              606  POP_TOP          

 L. 258       607  LOAD_FAST             0  'time'
              610  LOAD_ATTR             7  'sleep'
              613  LOAD_GLOBAL           8  'random'
              616  LOAD_ATTR             9  'expovariate'
              619  LOAD_CONST               100.0
              622  CALL_FUNCTION_1       1  None
              625  CALL_FUNCTION_1       1  None
              628  POP_TOP          

 L. 259       629  LOAD_FAST             1  'test'
              632  LOAD_ATTR            10  'barrier'
              635  LOAD_GLOBAL          11  'Barrier'
              638  LOAD_CONST               3
              641  CALL_FUNCTION_1       1  None
              644  CALL_FUNCTION_1       1  None
              647  POP_TOP          

 L. 260       648  LOAD_FAST             0  'time'
              651  LOAD_ATTR             7  'sleep'
              654  LOAD_GLOBAL           8  'random'
              657  LOAD_ATTR             9  'expovariate'
              660  LOAD_CONST               100.0
              663  CALL_FUNCTION_1       1  None
              666  CALL_FUNCTION_1       1  None
              669  POP_TOP          

 L. 261       670  LOAD_FAST             1  'test'
              673  LOAD_ATTR            10  'barrier'
              676  LOAD_GLOBAL          11  'Barrier'
              679  LOAD_CONST               2
              682  CALL_FUNCTION_1       1  None
              685  LOAD_CONST               'exc'
              688  LOAD_GLOBAL          13  'False'
              691  CALL_FUNCTION_257   257  None
              694  LOAD_GLOBAL          11  'Barrier'
              697  LOAD_CONST               3
              700  CALL_FUNCTION_1       1  None
              703  COMPARE_OP            2  ==
              706  POP_JUMP_IF_TRUE    715  'to 715'
              709  LOAD_ASSERT              AssertionError
              712  RAISE_VARARGS_1       1  None

 L. 262       715  LOAD_FAST             0  'time'
              718  LOAD_ATTR             7  'sleep'
              721  LOAD_GLOBAL           8  'random'
              724  LOAD_ATTR             9  'expovariate'
              727  LOAD_CONST               100.0
              730  CALL_FUNCTION_1       1  None
              733  CALL_FUNCTION_1       1  None
              736  POP_TOP          

 L. 263       737  LOAD_FAST             1  'test'
              740  LOAD_ATTR            10  'barrier'
              743  LOAD_GLOBAL          11  'Barrier'
              746  LOAD_CONST               1
              749  CALL_FUNCTION_1       1  None
              752  LOAD_CONST               'exc'
              755  LOAD_GLOBAL          13  'False'
              758  CALL_FUNCTION_257   257  None
              761  LOAD_GLOBAL          11  'Barrier'
              764  LOAD_CONST               3
              767  CALL_FUNCTION_1       1  None
              770  COMPARE_OP            2  ==
              773  POP_JUMP_IF_TRUE    782  'to 782'
              776  LOAD_ASSERT              AssertionError
              779  RAISE_VARARGS_1       1  None

 L. 264       782  LOAD_FAST             0  'time'
              785  LOAD_ATTR             7  'sleep'
              788  LOAD_GLOBAL           8  'random'
              791  LOAD_ATTR             9  'expovariate'
              794  LOAD_CONST               100.0
              797  CALL_FUNCTION_1       1  None
              800  CALL_FUNCTION_1       1  None
              803  POP_TOP          

 L. 265       804  LOAD_FAST             1  'test'
              807  LOAD_ATTR            10  'barrier'
              810  LOAD_GLOBAL          11  'Barrier'
              813  LOAD_CONST               3
              816  CALL_FUNCTION_1       1  None
              819  CALL_FUNCTION_1       1  None
              822  LOAD_CONST               None
              825  COMPARE_OP            8  is
              828  POP_JUMP_IF_TRUE    837  'to 837'
              831  LOAD_ASSERT              AssertionError
              834  RAISE_VARARGS_1       1  None

 L. 266       837  LOAD_FAST             0  'time'
              840  LOAD_ATTR             7  'sleep'
              843  LOAD_GLOBAL           8  'random'
              846  LOAD_ATTR             9  'expovariate'
              849  LOAD_CONST               100.0
              852  CALL_FUNCTION_1       1  None
              855  CALL_FUNCTION_1       1  None
              858  POP_TOP          

 L. 267       859  LOAD_FAST             1  'test'
              862  LOAD_ATTR            10  'barrier'
              865  LOAD_GLOBAL          11  'Barrier'
              868  LOAD_CONST               4
              871  CALL_FUNCTION_1       1  None
              874  CALL_FUNCTION_1       1  None
              877  LOAD_CONST               None
              880  COMPARE_OP            8  is
              883  POP_JUMP_IF_TRUE    892  'to 892'
              886  LOAD_ASSERT              AssertionError
              889  RAISE_VARARGS_1       1  None

 L. 268       892  LOAD_FAST             1  'test'
              895  LOAD_ATTR            15  'spread'
              898  LOAD_CONST               'k3'
              901  LOAD_CONST               'x'
              904  LOAD_GLOBAL          11  'Barrier'
              907  LOAD_CONST               6
              910  CALL_FUNCTION_1       1  None
              913  CALL_FUNCTION_3       3  None
              916  LOAD_CONST               0
              919  BINARY_SUBSCR    
              920  LOAD_CONST               'x'
              923  COMPARE_OP            2  ==
              926  POP_JUMP_IF_TRUE    935  'to 935'
              929  LOAD_ASSERT              AssertionError
              932  RAISE_VARARGS_1       1  None

 L. 269       935  LOAD_FAST             0  'time'
              938  LOAD_ATTR             7  'sleep'
              941  LOAD_GLOBAL           8  'random'
              944  LOAD_ATTR             9  'expovariate'
              947  LOAD_CONST               100.0
              950  CALL_FUNCTION_1       1  None
              953  CALL_FUNCTION_1       1  None
              956  POP_TOP          

 L. 270       957  LOAD_FAST             1  'test'
              960  LOAD_ATTR            16  'get_consensus'
              963  LOAD_CONST               'k3'
              966  LOAD_CONST               'a'
              969  LOAD_GLOBAL          11  'Barrier'
              972  LOAD_CONST               6
              975  LOAD_CONST               3
              978  CALL_FUNCTION_2       2  None
              981  LOAD_CONST               'string_median'
              984  CALL_FUNCTION_4       4  None
              987  LOAD_CONST               'a'
              990  COMPARE_OP            2  ==
              993  POP_JUMP_IF_TRUE   1002  'to 1002'
              996  LOAD_ASSERT              AssertionError
              999  RAISE_VARARGS_1       1  None

 L. 271      1002  LOAD_FAST             1  'test'
             1005  LOAD_ATTR            10  'barrier'
             1008  LOAD_GLOBAL          11  'Barrier'
             1011  LOAD_CONST               7
             1014  CALL_FUNCTION_1       1  None
             1017  CALL_FUNCTION_1       1  None
             1020  POP_TOP          

 L. 272      1021  LOAD_CONST               'barrier 7'
             1024  PRINT_ITEM       
             1025  PRINT_NEWLINE_CONT

 L. 273      1026  LOAD_FAST             1  'test'
             1029  LOAD_ATTR            15  'spread'
             1032  LOAD_CONST               'k3'
             1035  LOAD_CONST               'x'
             1038  LOAD_GLOBAL          11  'Barrier'
             1041  LOAD_CONST               7
             1044  LOAD_CONST               3
             1047  CALL_FUNCTION_2       2  None
             1050  CALL_FUNCTION_3       3  None
             1053  STORE_FAST            2  'tmp'

 L. 274      1056  LOAD_FAST             2  'tmp'
             1059  LOAD_CONST               0
             1062  BINARY_SUBSCR    
             1063  LOAD_CONST               'x'
             1066  COMPARE_OP            2  ==
             1069  POP_JUMP_IF_TRUE   1085  'to 1085'
             1072  LOAD_ASSERT              AssertionError
             1075  LOAD_CONST               'tmp= %s'
             1078  LOAD_FAST             2  'tmp'
             1081  BINARY_MODULO    
             1082  RAISE_VARARGS_2       2  None

 L. 275      1085  LOAD_FAST             0  'time'
             1088  LOAD_ATTR             7  'sleep'
             1091  LOAD_GLOBAL           8  'random'
             1094  LOAD_ATTR             9  'expovariate'
             1097  LOAD_CONST               100.0
             1100  CALL_FUNCTION_1       1  None
             1103  CALL_FUNCTION_1       1  None
             1106  POP_TOP          

 L. 276      1107  LOAD_FAST             1  'test'
             1110  LOAD_ATTR            17  'close'
             1113  CALL_FUNCTION_0       0  None
             1116  POP_TOP          
             1117  LOAD_CONST               None
             1120  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 1117


def test_many(n, fcn):
    import threading
    t = []
    for i in range(n):
        t.append(threading.Thread(target=fcn))

    for tt in t:
        tt.start()

    for tt in t:
        tt.join()


__version__ = Barrier(0, 1, 0)

def op_string_median(tmp):
    tmp.sort()
    n = len(tmp)
    if n % 2 == 1:
        return [tmp[(n // 2)]]
    return [
     random.choice([tmp[((n - 1) // 2)], tmp[(n // 2)]])]


def op_float_median(tmp):
    try:
        tmp = sorted([ float(q) for q in tmp ])
    except ValueError as x:
        return 'Bad data: %s' % str(x)

    n = len(tmp)
    if n % 2 == 1:
        return [tmp[(n // 2)]]
    return [
     0.5 * (tmp[((n - 1) // 2)] + tmp[(n // 2)])]


Ops = {'string_median': op_string_median, 'float_median': op_float_median}
Unpack = {'float_median': float, 'string_median': str}
test_args = ('localhost', 8487, 'K', 'job')
if __name__ == '__main__':
    test_many(2, test0s)
    test_many(2, test0)
    test1()
    print 'Test1 OK'
    test_many(2, test1)
    test_many(11, test0s)
    test_many(11, test0)
    test_many(11, test1)