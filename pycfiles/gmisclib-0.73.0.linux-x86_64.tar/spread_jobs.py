# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/spread_jobs.py
# Compiled at: 2011-05-12 11:57:48
"""
A module that starts a bunch of subprocesses and distributes
work amongst them, then collects the results.

Subprocesses must follow a protocol: they must listen for commands
on the standard input (commands are encoded with C{cPickle}),
and they must produce C{cPickle}d tuples on their standard output.
NOTE: THEY CANNOT PRINT ANYTHING ELSE!  (But it's OK for subprocesses
to produce stuff on the standard error output.)

PROTOCOL:

        1. Execcing state: C{spread_jobs} execs a group of subprocesses.  You have
        full control of the argument list.

        2. Preparation state: C{spread_jobs} will send a list of C{cPickled} things,
        one at a time to the subprocess.   No explicit terminator
        is added, so the subprocess must either know how many things
        are coming or the list should contain some terminator.
        (E.g. the last item of the list could be L{None}, and the
        subprocess would wait for it.)
        In this state, the subprocess must not produce anything on
        the standard output.

        3. Running state: C{spread_jobs} will send one C{cPickled} thing to the
        subprocess and then wait for a C{cPickled} C{tuple} to come
        back.

        The request to the subprocess is a C{tuple(int, arbitrary)}.
        The L{int} is a task-ID number which must be returned with the answer.
        The C{arbitrary} is whatever information the subprocess needs to do its job.

        The subprocess responds with a 3-L{tuple}.   The first element of the
        tuple is either:
        
                - An instance of L{TooBusy}.  This causes the main process to
                        put the task back on the queue and ignore this subprocess for
                        a while.  The second element is printed; the third is ignored.
                - An instance of L{RemoteException}.   This leads to termination of
                        the job and causes an exception to be raised on the main thread.
                        The other two elements of the tuple are printed.
                - Anything else.   In that case, the first element is returned on the
                        output list and the other two elements are printed.

        The subprocess loops in the running state.
        Normally, it should terminate when its standard input is closed.
        (It can terminate itself if it wishes by simply closing the standard output and exiting.)

        4. Shutdown state: The subprocess can produce anything it wants.   This will
        be collected up and returned to the caller of C{spread_jobs.main}.

        You can use this to run certain normal linux commands by not sending anything
        in the preparatory state or the running state.  You will then be handed
        the standard output as a list of strings.

Normally, the action happens in the running state.

Normally, the subprocess looks much like this::

        import cPickle
        while True:
                try:
                        control = cPickle.load(stdin)
                except EOFError:
                        break
                d, so, se = compute(control)
                cPickle.dump((d, so, se), stdout, CP.HIGHEST_PROTOCOL)
                stdout.flush()
        stdout.close()

@sort: main, replace, Replace, append
"""
from __future__ import with_statement
import re, sys, math, time, random, cPickle as CP, threading, subprocess, StringIO
from gmisclib import die
from gmisclib import gpkmisc
from gmisclib import dictops
from gyropy import g_mailbox as MB

class notComputed(object):
    """A singleton marker for values that haven't been computed."""
    pass


class NoResponse(RuntimeError):

    def __init__(self, *s):
        RuntimeError.__init__(self, *s)


class RemoteException(Exception):
    """An exception that corresponds to one raised by a subprocess.
        This is raised in the parent process.
        """

    def __init__(self, *s):
        Exception.__init__(self, *s)
        self.index = ''
        self.comment = ''

    def __repr__(self):
        return '<%s.RemoteException: %s>' % (__name__, repr(self.args))

    def raise_me(self):
        raise self


class TooBusy(object):

    def __init__(self, delay):
        self.delay = delay


class PastPerformance(dictops.dict_of_averages):

    def __init__(self):
        dictops.dict_of_averages.__init__(self)

    def add_many(self, kvpairs):
        for k, v in kvpairs:
            self.add(k, v)

    def __call__(self, x):
        s = 0.5
        n = 1
        for t in x:
            try:
                sm, wts = self.get_both(str(t))
            except KeyError:
                sm, wts = (0.5, 1.0)

            n += wts
            s += sm

        return -s / n


class Connection(object):
    """This class represents a connection from the master process down to one of the slaves.
        It also keeps track of how often the slave reports that it is too busy to work.
        """

    def __init__(self, arglist):
        """
                @param arglist: an argument list to execute to start a subprocess.
                @type arglist: a sequence of anything that can be converted to strings.
                @note: This is where the arglist is finally converted to a list of strings.
                @except OSError: when connection cannot be set up.
                """
        self.arglist = [ str(q) for q in arglist ]
        self.OSError = OSError
        self.EOFError = EOFError
        self.SendError = (IOError, ValueError)
        self.lock = threading.Lock()
        self.uness = 1.0

    def send(self, todo):
        """@except IOError: Trouble sending."""
        raise RuntimeError, 'Virtual Method'

    def get(self):
        """@return: (answer, standard_output, standard_error) or None.
                @except EOFError: No data available from slave.
                """
        raise RuntimeError, 'Virtual Method'

    def close(self):
        """Closes the channel to the slave."""
        raise RuntimeError, 'Virtual Method'

    def wait(self):
        """Waits for the slave to terminate and closes the channel from the slave.
                @return: any final output.
                @rtype: list(str)
                """
        raise RuntimeError, 'Virtual Method'

    def argstring(self):
        return (' ').join(self.arglist)

    BUSYFAC1 = 0.85
    BUSY3 = 0.01
    BUSYFAC2 = (1 - BUSYFAC1) / (1 + BUSY3)

    def usefulness(self):
        with self.lock:
            assert 0 <= self.uness <= 1.0
            return self.uness

    def I_am_working(self, now):
        with self.lock:
            self.uness = self.uness * self.BUSYFAC1 + self.BUSYFAC2 * (now + self.BUSY3)

    def mystate(self, state):
        if state != 'running':
            with self.lock:
                self.uness = 0.0

    def performance(self):
        u = self.usefulness()
        for arg in self.arglist:
            yield (
             arg, u)


class Connection_subprocess(Connection):
    """This is a L{Connection} via stdin/stdout to a subprocess."""

    def __init__(self, arglist):
        Connection.__init__(self, arglist)
        self.p = subprocess.Popen(self.arglist, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=sys.stderr, close_fds=True)

    def send(self, todo):
        CP.dump(todo, self.p.stdin)
        self.p.stdin.flush()

    def get(self):
        while True:
            try:
                rv = CP.load(self.p.stdout)
                return rv
            except CP.UnpicklingError as y:
                die.warn('spread_jobs: Junk response: %s' % repr(y))
                die.info('spread_jobs: Junk remainder: %s' % self.p.stdout.readline())
                die.info('spread_jobs: Junk arglist: %s' % self.argstring())
                raise

        return

    def close1(self):
        self.p.stdin.close()

    def close2(self):
        tmp = self.p.stdout.readlines()
        self.p.stdout.close()
        self.p.wait()
        return tmp


def delay_sanitize(x):
    return max(0.01, min(1000.0, float(x)))


class _ThreadJob(threading.Thread):

    def __init__(self, iqueue, oqueue, p, stdin, solock, wss):
        """@param stdin: something to send at the start of the subprocess
                        to get it going.   This is before the main processing starts.
                @type stdin: any iterable that yields something that can be
                        given to L{cPickle.dumps}.
                @param p: The process to run.   It's already been started,
                        but no input/output has occurred.
                @type p: L{Connection}
                @param solock: a lock to serialize the standard output
                @type solock: threading.Lock
                """
        threading.Thread.__init__(self, name='spread_jobs%s' % id(self))
        self.iqueue = iqueue
        self.oqueue = oqueue
        self.wss = wss
        assert isinstance(p, Connection)
        self.p = p
        self.solock = solock
        try:
            for x in stdin:
                self.p.send(x)

        except self.p.SendError as x:
            die.info('I/O error in thread start-up: %s' % str(x))
            self.p.close1()

    def want_shutdown(self):
        na, nlive = self.wss.num_active()
        return na > 3 + 2 * (len(self.iqueue) + 1) and nlive * self.p.usefulness() < na

    def compute_delay(self, qdelay, delta_t):
        """The reason we have the dependence on nw and nq is that we want to
                shorten delays as the queue empties.   Basically, we don't want any
                processes sleeping when the queue is empty.   That would just waste
                time to no purpose.
        
                The reason we have the dependence on delta_t is that we want to limit
                the number of CPU cycles that are wasted in polling other machines to
                see if they are too busy.
                """
        nw = self.wss.num_active()[0]
        nq = len(self.iqueue)
        delay = delay_sanitize(qdelay) * random.uniform(0.8, 1.4)
        delay1 = math.exp(1.0 - self.p.usefulness())
        delay2 = max(0.1, float(nq + 1) / float(nw))
        delay *= min(delay1, delay2)
        return math.sqrt(10 * delta_t * delay) + delay

    def run(self):
        self.p.mystate('running')
        while True:
            try:
                i, todo = self.iqueue.get()
            except MB.EOF:
                self.p.mystate('iqueue EOF')
                break

            t0 = time.time()
            try:
                self.p.send(todo)
            except self.p.SendError as x:
                die.warn('IO Error on send task %d to worker: %s' % (i, str(x)))
                self.iqueue.put((i, todo))
                self.p.mystate('SendError')
                break

            try:
                q, so, se = self.p.get()
            except (self.p.EOFError, CP.UnpicklingError, ValueError) as x:
                die.warn('Exception %s when trying to read worker %s' % (x, self.p.argstring()))
                self.iqueue.put((i, todo))
                self.p.mystate('BadRead')
                break

            t2 = time.time()
            if isinstance(q, TooBusy):
                self.iqueue.put((i, todo))
                if self.want_shutdown():
                    die.info('TooBusy: giving up on %s' % str(so))
                    self.p.mystate('giving up')
                    break
                else:
                    tsleep = self.compute_delay(q.delay, t2 - t0)
                    die.info('TooBusy: sleeping %.3f for %s' % (tsleep, str(so)))
                    self.p.I_am_working(0)
                    time.sleep(tsleep)
                continue
            self.p.I_am_working(1)
            self.oqueue.put((i, t0, t2, q))
            with self.solock:
                if so:
                    sys.stdout.writelines('#slot so%d ------\n' % i)
                    sys.stdout.writelines(so)
                    sys.stdout.flush()
                if se:
                    sys.stderr.writelines('#slot se%d ------\n' % i)
                    sys.stderr.writelines(se)
                    sys.stderr.flush()
            if isinstance(q, RemoteException):
                die.info('Remote Exception info: %s' % str(q.args))
                die.warn('Exception from remote job (index=%d): %s' % (i, str(q)))
                q.index = 'index=%d' % i
                q.comment = 'so=%s # se=%s' % (gpkmisc.truncate((';').join(so), 40),
                 gpkmisc.truncate((';').join(se), 40))
                while True:
                    try:
                        j, todo = self.iqueue.get()
                    except MB.EOF:
                        self.p.mystate('RemoteException')
                        break

                    self.oqueue.put((j, t0, t2, notComputed))

        self.p.close1()

    def join(self, timeout=None):
        tmp = self.p.close2()
        threading.Thread.join(self, timeout=timeout)
        self.wss = None
        return tmp


_past_performance = PastPerformance()

def main(todo, list_of_args, connection_factory=Connection_subprocess, stdin=None, verbose=False, timing_callback=None, tail_callback=None, past_performance=_past_performance):
    """Pass a bunch of work to other processes.
        @param stdin: a list of stuff to send to the other processes before the computation is
                properly commenced.
        @type stdin: list(whatever)
        @param todo: a sequence of tasks to do
        @type todo: sequence(whatever)
        @param list_of_args:
        @type list_of_args:  list(list(str))
        @param past_performance: a L{PastPerformance} object if you want the system to remember which
                machines were more/less successful last time and to start jobs on the more successful
                machines first.    L{None} if you don't want any memory.  The default is to have memory.
        @type past_performance: None or L{PastPerformance}.
        @rtype: C{tuple(list(whatever), list(list(str)))}
        @return: A 2-tuple.   The first item is
                a list of the results produced by the other processes.
                Items in the returned list correspond to items in the todo list.
                These are the stuff that comes out, pickled, on the standard
                output after each chunk of data is fed into the standard input.
                The second item is a list of the remaining outputs, as read
                by file.readlines(); these are one per process.
        """
    if stdin is None:
        stdin = []
    solock = threading.Lock()
    iqueue = MB.maillist(enumerate(todo))
    ntodo = len(iqueue)
    oqueue = MB.mailbox()
    ths = workers_c(connection_factory, list_of_args, iqueue, oqueue, stdin, solock, tail_callback=tail_callback, verbose=verbose, past_performance=past_performance)
    if verbose:
        die.info('%d jobs started' % len(ths))
    if not ths:
        raise RuntimeError, 'No subprocesses started.'
    oi = 0
    rv = [notComputed] * ntodo
    while oi < ntodo:
        try:
            i, ts, te, ans = oqueue.get()
        except MB.EOF:
            raise RuntimeError, 'whoops'

        if timing_callback:
            timing_callback(ts, te)
        assert rv[i] is notComputed
        rv[i] = ans
        oi += 1

    iqueue.putclose()
    oqueue.putclose()
    if verbose:
        die.info('Joining %d jobs' % len(ths))
    ths.join()
    if past_performance is not None:
        ths.pass_performance(past_performance)
    return rv


class workers_c(object):
    """This creates a group of worker threads that take tasks from the iqueue and put the
        answers on the oqueue.
        """

    def __init__(self, connection_factory, list_of_args, iqueue, oqueue, stdin, solock, verbose=False, tail_callback=None, past_performance=None):
        self.tail_callback = tail_callback
        self.args = list_of_args
        self.ths = []
        self.verbose = verbose
        for args in sorted(list_of_args, key=past_performance):
            if self.verbose:
                die.info('Args= %s' % str(args))
            try:
                p = connection_factory(args)
            except p.OSError as x:
                die.warn('Cannot execute subprocess: %s on %s' % (x, args))
                continue

            t = _ThreadJob(iqueue, oqueue, p, stdin, solock, self)
            self.ths.append(t)
            t.start()

    def join(self):
        nj = len(self.ths)
        for t in self.ths:
            oo = t.join()
            if self.tail_callback:
                self.tail_callback(t.arglist, oo)

        if self.verbose:
            die.info('Joined %d jobs' % nj)

    def pass_performance(self, x):
        x.clear()
        for t in self.ths:
            x.add_many(t.p.performance())

    def __len__(self):
        return len(self.ths)

    def num_active(self):
        """@return: total usefulness of all workers and the number of live workers
                @rtype: (float, int)
                """
        na = 0.0
        nlive = 0
        for t in self.ths:
            tmp = t.p.usefulness()
            if tmp > 0.0:
                na += tmp
                nlive += 1

        return (
         na, nlive)


def test_worker(x):
    if x > 0 and random.random() < 0.3:
        sys.exit(random.randrange(2))
    sys.stderr.write('test_worker starting\n')
    while True:
        sys.stderr.write('test_worker loop\n')
        try:
            txt = CP.load(sys.stdin)
        except EOFError:
            sys.stderr.write('test_worker got EOF\n')
            break

        if random.random() < 0.1:
            sys.stderr.write('Sending TooBusy')
            CP.dump((TooBusy(0.1), None, None), sys.stdout, CP.HIGHEST_PROTOCOL)
            sys.stdout.flush()
            continue
        if random.random() < 0.5:
            time.sleep(random.expovariate(30.0))
        sys.stderr.write('test worker control=%s\n' % txt)
        if txt is None:
            sys.stderr.write('test_worker got stop\n')
            break
        sys.stderr.write('test_worker dump %s\n' % txt)
        CP.dump((txt, ['stdout:%s\n' % txt], ['stderr\n']), sys.stdout, CP.HIGHEST_PROTOCOL)
        sys.stdout.flush()

    sys.stderr.write('test_worker finished\n')
    sys.stdout.close()
    return


def test(script):
    for np in range(1, 5):
        print 'NP=%d' % np
        for i in range(1, 6):
            print 'ntasks=%d' % (i * 5)
            x = ['a', 'b', 'c', 'd', 'e'] * i
            arglist = [ ['python', script, 'worker', str(j)] for j in range(np) ]
            y = list(main(x, arglist, verbose=True))
            assert x == y


class unpickled_pseudofile(StringIO.StringIO):
    """For testing.
        """

    def __init__(self):
        StringIO.StringIO.__init__(self)

    def close(self):
        self.seek(0, 0)
        while True:
            try:
                d, so, se = CP.load(self)
            except EOFError:
                break

            sys.stdout.write('STDOUT:\n')
            sys.stdout.writelines(so)
            sys.stdout.write('STDERR:\n')
            sys.stdout.writelines(se)
            sys.stdout.write('d=%s\n' % str(d))
            sys.stdout.flush()


def one_shot_test(input):
    stdin = StringIO.StringIO()
    CP.dump(input, stdin)
    stdin.flush()
    stdin.seek(0, 0)
    stdout = unpickled_pseudofile()
    return (stdin, stdout)


def replace--- This code section failed: ---

 L. 612         0  BUILD_LIST_0          0 
                3  STORE_FAST            2  'frc'

 L. 613         6  SETUP_LOOP           56  'to 65'
                9  LOAD_FAST             1  'fr'
               12  POP_JUMP_IF_FALSE    64  'to 64'

 L. 614        15  LOAD_FAST             2  'frc'
               18  LOAD_ATTR             0  'append'
               21  LOAD_GLOBAL           1  're'
               24  LOAD_ATTR             2  'compile'
               27  LOAD_FAST             1  'fr'
               30  LOAD_CONST               0
               33  BINARY_SUBSCR    
               34  CALL_FUNCTION_1       1  None
               37  LOAD_FAST             1  'fr'
               40  LOAD_CONST               1
               43  BINARY_SUBSCR    
               44  BUILD_TUPLE_2         2 
               47  CALL_FUNCTION_1       1  None
               50  POP_TOP          

 L. 615        51  LOAD_FAST             1  'fr'
               54  LOAD_CONST               2
               57  SLICE+1          
               58  STORE_FAST            1  'fr'
               61  JUMP_BACK             9  'to 9'
               64  POP_BLOCK        
             65_0  COME_FROM             6  '6'

 L. 616        65  BUILD_LIST_0          0 
               68  STORE_FAST            3  'o'

 L. 617        71  SETUP_LOOP          184  'to 258'
               74  LOAD_FAST             0  'list_of_lists'
               77  GET_ITER         
               78  FOR_ITER            176  'to 257'
               81  STORE_FAST            4  'l'

 L. 618        84  LOAD_GLOBAL           3  'isinstance'
               87  LOAD_FAST             4  'l'
               90  LOAD_GLOBAL           4  'tuple'
               93  LOAD_GLOBAL           5  'list'
               96  BUILD_TUPLE_2         2 
               99  CALL_FUNCTION_2       2  None
              102  POP_JUMP_IF_TRUE    130  'to 130'
              105  LOAD_ASSERT              AssertionError
              108  LOAD_CONST               'List of lists contains %s within %s'
              111  LOAD_GLOBAL           7  'repr'
              114  LOAD_FAST             4  'l'
              117  CALL_FUNCTION_1       1  None
              120  LOAD_FAST             0  'list_of_lists'
              123  BUILD_TUPLE_2         2 
              126  BINARY_MODULO    
              127  RAISE_VARARGS_2       2  None

 L. 619       130  BUILD_LIST_0          0 
              133  STORE_FAST            5  'tmp'

 L. 620       136  SETUP_LOOP          102  'to 241'
              139  LOAD_FAST             4  'l'
              142  GET_ITER         
              143  FOR_ITER             94  'to 240'
              146  STORE_FAST            6  't'

 L. 621       149  SETUP_LOOP           72  'to 224'
              152  LOAD_FAST             2  'frc'
              155  GET_ITER         
              156  FOR_ITER             64  'to 223'
              159  UNPACK_SEQUENCE_2     2 
              162  STORE_FAST            7  'find'
              165  STORE_FAST            8  'repl'

 L. 622       168  LOAD_GLOBAL           3  'isinstance'
              171  LOAD_FAST             6  't'
              174  LOAD_GLOBAL           8  'str'
              177  CALL_FUNCTION_2       2  None
              180  POP_JUMP_IF_TRUE    202  'to 202'
              183  LOAD_ASSERT              AssertionError
              186  LOAD_CONST               'whoops! t=%s'
              189  LOAD_GLOBAL           8  'str'
              192  LOAD_FAST             6  't'
              195  CALL_FUNCTION_1       1  None
              198  BINARY_MODULO    
              199  RAISE_VARARGS_2       2  None

 L. 623       202  LOAD_FAST             7  'find'
              205  LOAD_ATTR             9  'sub'
              208  LOAD_FAST             8  'repl'
              211  LOAD_FAST             6  't'
              214  CALL_FUNCTION_2       2  None
              217  STORE_FAST            6  't'
              220  JUMP_BACK           156  'to 156'
              223  POP_BLOCK        
            224_0  COME_FROM           149  '149'

 L. 624       224  LOAD_FAST             5  'tmp'
              227  LOAD_ATTR             0  'append'
              230  LOAD_FAST             6  't'
              233  CALL_FUNCTION_1       1  None
              236  POP_TOP          
              237  JUMP_BACK           143  'to 143'
              240  POP_BLOCK        
            241_0  COME_FROM           136  '136'

 L. 625       241  LOAD_FAST             3  'o'
              244  LOAD_ATTR             0  'append'
              247  LOAD_FAST             5  'tmp'
              250  CALL_FUNCTION_1       1  None
              253  POP_TOP          
              254  JUMP_BACK            78  'to 78'
              257  POP_BLOCK        
            258_0  COME_FROM            71  '71'

 L. 626       258  LOAD_FAST             3  'o'
              261  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 223


def Replace--- This code section failed: ---

 L. 630         0  LOAD_GLOBAL           0  'isinstance'
                3  LOAD_FAST             3  'replacement'
                6  LOAD_GLOBAL           1  'list'
                9  CALL_FUNCTION_2       2  None
               12  POP_JUMP_IF_TRUE     21  'to 21'
               15  LOAD_ASSERT              AssertionError
               18  RAISE_VARARGS_1       1  None

 L. 631        21  LOAD_FAST             2  'length'
               24  LOAD_CONST               0
               27  COMPARE_OP            4  >
               30  POP_JUMP_IF_TRUE     39  'to 39'
               33  LOAD_ASSERT              AssertionError
               36  RAISE_VARARGS_1       1  None

 L. 632        39  LOAD_GLOBAL           3  're'
               42  LOAD_ATTR             4  'compile'
               45  LOAD_FAST             1  'pat'
               48  CALL_FUNCTION_1       1  None
               51  STORE_FAST            4  'cpat'

 L. 633        54  BUILD_LIST_0          0 
               57  STORE_FAST            5  'o'

 L. 634        60  SETUP_LOOP          197  'to 260'
               63  LOAD_FAST             0  'list_of_lists'
               66  GET_ITER         
               67  FOR_ITER            189  'to 259'
               70  STORE_FAST            6  'l'

 L. 635        73  LOAD_GLOBAL           0  'isinstance'
               76  LOAD_FAST             6  'l'
               79  LOAD_GLOBAL           5  'tuple'
               82  LOAD_GLOBAL           1  'list'
               85  BUILD_TUPLE_2         2 
               88  CALL_FUNCTION_2       2  None
               91  POP_JUMP_IF_TRUE    119  'to 119'
               94  LOAD_ASSERT              AssertionError
               97  LOAD_CONST               'List of lists contains %s within %s'
              100  LOAD_GLOBAL           6  'repr'
              103  LOAD_FAST             6  'l'
              106  CALL_FUNCTION_1       1  None
              109  LOAD_FAST             0  'list_of_lists'
              112  BUILD_TUPLE_2         2 
              115  BINARY_MODULO    
              116  RAISE_VARARGS_2       2  None

 L. 636       119  LOAD_GLOBAL           1  'list'
              122  LOAD_FAST             6  'l'
              125  CALL_FUNCTION_1       1  None
              128  STORE_FAST            7  'tmp'

 L. 637       131  SETUP_LOOP          109  'to 243'
              134  LOAD_FAST             7  'tmp'
              137  POP_JUMP_IF_FALSE   242  'to 242'

 L. 638       140  LOAD_CONST               None
              143  STORE_FAST            8  'found'

 L. 639       146  SETUP_LOOP           51  'to 200'
              149  LOAD_GLOBAL           8  'enumerate'
              152  LOAD_FAST             7  'tmp'
              155  CALL_FUNCTION_1       1  None
              158  GET_ITER         
              159  FOR_ITER             37  'to 199'
              162  UNPACK_SEQUENCE_2     2 
              165  STORE_FAST            9  'i'
              168  STORE_FAST           10  't'

 L. 640       171  LOAD_FAST             4  'cpat'
              174  LOAD_ATTR             9  'match'
              177  LOAD_FAST            10  't'
              180  CALL_FUNCTION_1       1  None
              183  POP_JUMP_IF_FALSE   159  'to 159'

 L. 641       186  LOAD_FAST             9  'i'
              189  STORE_FAST            8  'found'

 L. 642       192  BREAK_LOOP       
              193  JUMP_BACK           159  'to 159'
              196  JUMP_BACK           159  'to 159'
              199  POP_BLOCK        
            200_0  COME_FROM           146  '146'

 L. 643       200  LOAD_FAST             8  'found'
              203  LOAD_CONST               None
              206  COMPARE_OP            9  is-not
              209  POP_JUMP_IF_FALSE   238  'to 238'

 L. 644       212  LOAD_GLOBAL           1  'list'
              215  LOAD_FAST             3  'replacement'
              218  CALL_FUNCTION_1       1  None
              221  LOAD_FAST             7  'tmp'
              224  LOAD_FAST             9  'i'
              227  LOAD_FAST             9  'i'
              230  LOAD_FAST             2  'length'
              233  BINARY_ADD       
              234  STORE_SLICE+3    
              235  JUMP_BACK           134  'to 134'

 L. 646       238  BREAK_LOOP       
              239  JUMP_BACK           134  'to 134'
              242  POP_BLOCK        
            243_0  COME_FROM           131  '131'

 L. 647       243  LOAD_FAST             5  'o'
              246  LOAD_ATTR            10  'append'
              249  LOAD_FAST             7  'tmp'
              252  CALL_FUNCTION_1       1  None
              255  POP_TOP          
              256  JUMP_BACK            67  'to 67'
              259  POP_BLOCK        
            260_0  COME_FROM            60  '60'

 L. 648       260  LOAD_FAST             5  'o'
              263  RETURN_VALUE     

Parse error at or near `POP_BLOCK' instruction at offset 259


def append(list_of_lists, *a):
    o = []
    for l in list_of_lists:
        tmp = tuple(l) + a
        o.append(tmp)

    return o


if __name__ == '__main__':
    if len(sys.argv) == 3 and sys.argv[1] == 'worker':
        test_worker(int(sys.argv[2]))
    else:
        test(sys.argv[0])