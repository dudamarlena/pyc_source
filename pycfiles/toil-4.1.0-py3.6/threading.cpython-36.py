# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/threading.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 20001 bytes
from __future__ import absolute_import
from future.utils import raise_
from builtins import range
import atexit, fcntl, logging, math, os, sys, tempfile, threading, traceback
from contextlib import contextmanager
from threading import BoundedSemaphore
import psutil
from toil.lib.misc import mkdir_p, robust_rmtree
log = logging.getLogger(__name__)

class BoundedEmptySemaphore(BoundedSemaphore):
    __doc__ = '\n    A bounded semaphore that is initially empty.\n    '

    def __init__(self, value=1, verbose=None):
        super(BoundedEmptySemaphore, self).__init__(value, verbose)
        for i in range(value):
            assert self.acquire(blocking=False)


class ExceptionalThread(threading.Thread):
    __doc__ = '\n    A thread whose join() method re-raises exceptions raised during run(). While join() is\n    idempotent, the exception is only during the first invocation of join() that successfully\n    joined the thread. If join() times out, no exception will be re reraised even though an\n    exception might already have occured in run().\n\n    When subclassing this thread, override tryRun() instead of run().\n\n    >>> def f():\n    ...     assert 0\n    >>> t = ExceptionalThread(target=f)\n    >>> t.start()\n    >>> t.join()\n    Traceback (most recent call last):\n    ...\n    AssertionError\n\n    >>> class MyThread(ExceptionalThread):\n    ...     def tryRun( self ):\n    ...         assert 0\n    >>> t = MyThread()\n    >>> t.start()\n    >>> t.join()\n    Traceback (most recent call last):\n    ...\n    AssertionError\n\n    '
    exc_info = None

    def run(self):
        try:
            self.tryRun()
        except:
            self.exc_info = sys.exc_info()
            raise

    def tryRun(self):
        super(ExceptionalThread, self).run()

    def join(self, *args, **kwargs):
        (super(ExceptionalThread, self).join)(*args, **kwargs)
        if not self.is_alive():
            if self.exc_info is not None:
                type, value, traceback = self.exc_info
                self.exc_info = None
                raise_(type, value, traceback)


class defaultlocal(threading.local):
    __doc__ = '\n    Thread local storage with default values for each field in each thread\n\n    >>>\n    >>> l = defaultlocal( foo=42 )\n    >>> def f(): print(l.foo)\n    >>> t = threading.Thread(target=f)\n    >>> t.start() ; t.join()\n    42\n    '

    def __init__(self, **kwargs):
        super(defaultlocal, self).__init__()
        self.__dict__.update(kwargs)


def cpu_count():
    """
    Get the rounded-up integer number of whole CPUs available.

    Counts hyperthreads as CPUs.

    Uses the system's actual CPU count, or the current v1 cgroup's quota per
    period, if the quota is set.

    Ignores the cgroup's cpu shares value, because it's extremely difficult to
    interpret. See https://github.com/kubernetes/kubernetes/issues/81021.

    Caches result for efficiency.

    :return: Integer count of available CPUs, minimum 1.
    :rtype: int
    """
    cached = getattr(cpu_count, 'result', None)
    if cached is not None:
        return cached
    else:
        total_machine_size = psutil.cpu_count(logical=True)
        log.debug('Total machine size: %d cores', total_machine_size)
        try:
            with open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us', 'r') as (stream):
                quota = int(stream.read())
            log.debug('CPU quota: %d', quota)
            if quota == -1:
                return total_machine_size
            with open('/sys/fs/cgroup/cpu/cpu.cfs_period_us', 'r') as (stream):
                period = int(stream.read())
            log.debug('CPU quota period: %d', period)
            cgroup_size = int(math.ceil(float(quota) / float(period)))
            log.debug('Cgroup size in cores: %d', cgroup_size)
        except:
            log.debug('Could not inspect cgroup: %s', traceback.format_exc())
            cgroup_size = float('inf')

        result = max(1, min(cgroup_size, total_machine_size))
        log.debug('cpu_count: %s', str(result))
        setattr(cpu_count, 'result', result)
        return result


current_process_name_lock = threading.Lock()
current_process_name_for = {}

def collect_process_name_garbage():
    """
    Delete all the process names that point to files that don't exist anymore
    (because the work directory was temporary and got cleaned up). This is
    known to happen during the tests, which get their own temp directories.

    Caller must hold current_process_name_lock.
    """
    global current_process_name_for
    missing = []
    for workDir, name in current_process_name_for.items():
        if not os.path.exists(os.path.join(workDir, name)):
            missing.append(workDir)

    for workDir in missing:
        del current_process_name_for[workDir]


def destroy_all_process_names():
    """
    Delete all our process name files because our process is going away.

    We let all our FDs get closed by the process death.

    We assume there is nobody else using the system during exit to race with.
    """
    for workDir, name in current_process_name_for.items():
        robust_rmtree(os.path.join(workDir, name))


atexit.register(destroy_all_process_names)

def get_process_name(workDir):
    """
    Return the name of the current process. Like a PID but visible between
    containers on what to Toil appears to be a node.

    :param str workDir: The Toil work directory. Defines the shared namespace.
    :return: Process's assigned name
    :rtype: str
    """
    global current_process_name_lock
    with current_process_name_lock:
        collect_process_name_garbage()
        if workDir in current_process_name_for:
            return current_process_name_for[workDir]
        else:
            nameFD, nameFileName = tempfile.mkstemp(dir=workDir)
            try:
                fcntl.lockf(nameFD, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except IOError as e:
                raise RuntimeError('Could not lock process name file %s: %s' % (nameFileName, str(e)))

            current_process_name_for[workDir] = os.path.basename(nameFileName)
            return current_process_name_for[workDir]


def process_name_exists(workDir, name):
    """
    Return true if the process named by the given name (from process_name) exists, and false otherwise.

    Can see across container boundaries using the given node workflow directory.

    :param str workDir: The Toil work directory. Defines the shared namespace.
    :param str name: Process's name to poll
    :return: True if the named process is still alive, and False otherwise.
    :rtype: bool
    """
    with current_process_name_lock:
        if current_process_name_for.get(workDir, None) == name:
            return True
    nameFileName = os.path.join(workDir, name)
    if not os.path.exists(nameFileName):
        return False
    nameFD = None
    try:
        nameFD = os.open(nameFileName, os.O_RDONLY)
        try:
            fcntl.lockf(nameFD, fcntl.LOCK_SH | fcntl.LOCK_NB)
        except IOError as e:
            return True
        else:
            try:
                os.remove(nameFileName)
            except:
                pass

            fcntl.lockf(nameFD, fcntl.LOCK_UN)
            return False
    finally:
        if nameFD is not None:
            try:
                os.close(nameFD)
            except:
                pass


@contextmanager
def global_mutex(workDir, mutex):
    """
    Context manager that locks a mutex. The mutex is identified by the given
    name, and scoped to the given directory. Works across all containers that
    have access to the given diectory. Mutexes held by dead processes are
    automatically released.
    
    Only works between processes, NOT between threads.
    
    :param str workDir: The Toil work directory. Defines the shared namespace.
    :param str mutex: Mutex to lock. Must be a permissible path component.
    """
    lock_filename = os.path.join(workDir, 'toil-mutex-' + mutex)
    log.debug('PID %d acquiring mutex %s', os.getpid(), lock_filename)
    while True:
        fd = os.open(lock_filename, os.O_CREAT | os.O_WRONLY)
        fcntl.lockf(fd, fcntl.LOCK_EX)
        fd_stats = os.fstat(fd)
        try:
            path_stats = os.stat(lock_filename)
        except FileNotFoundError:
            path_stats = None

        if path_stats is None or fd_stats.st_dev != path_stats.st_dev or fd_stats.st_ino != path_stats.st_ino:
            fcntl.lockf(fd, fcntl.LOCK_UN)
            os.close(fd)
            continue
        else:
            break

    try:
        log.debug('PID %d now holds mutex %s', os.getpid(), lock_filename)
        yield
    finally:
        log.debug('PID %d releasing mutex %s', os.getpid(), lock_filename)
        os.unlink(lock_filename)
        fcntl.lockf(fd, fcntl.LOCK_UN)
        os.close(fd)


class LastProcessStandingArena:
    __doc__ = '\n    Class that lets a bunch of processes detect and elect a last process\n    standing.\n    \n    Process enter and leave (sometimes due to sudden existence failure). We\n    guarantee that the last process to leave, if it leaves properly, will get a\n    chance to do some cleanup. If new processes try to enter during the\n    cleanup, they will be delayed until after the cleanup has happened and the\n    previous "last" process has finished leaving.\n    \n    The user is responsible for making sure you always leave if you enter!\n    Consider using a try/finally; this class is not a context manager.\n    '

    def __init__(self, workDir, name):
        """
        Connect to the arena specified by the given workDir and name.
        
        Any process that can access workDir, in any container, can connect to
        the arena. Many arenas can be active with different names.
        
        Doesn't enter or leave the arena.
        
        :param str workDir: The Toil work directory. Defines the shared namespace.
        :param str name: Name of the arena. Must be a permissible path component.
        """
        self.workDir = workDir
        self.mutex = name + '-arena-lock'
        self.lockfileDir = os.path.join(workDir, name + '-arena-members')
        self.lockfileFD = None
        self.lockfileName = None

    def enter(self):
        """
        This process is entering the arena. If cleanup is in progress, blocks
        until it is finished.
        
        You may not enter the arena again before leaving it.
        """
        log.debug('Joining arena %s', self.lockfileDir)
        if not self.lockfileName is None:
            raise AssertionError
        elif not self.lockfileFD is None:
            raise AssertionError
        with global_mutex(self.workDir, self.mutex):
            try:
                os.mkdir(self.lockfileDir)
            except FileExistsError:
                pass

            self.lockfileFD, self.lockfileName = tempfile.mkstemp(dir=(self.lockfileDir))
            fcntl.lockf(self.lockfileFD, fcntl.LOCK_EX)
        log.debug('Now in arena %s', self.lockfileDir)

    def leave(self):
        """
        This process is leaving the arena. If this process happens to be the
        last process standing, yields something, with other processes blocked
        from joining the arena until the loop body completes and the process
        has finished leaving. Otherwise, does not yield anything.
        
        Should be used in a loop:
        
            for _ in arena.leave():
                # If we get here, we were the last process. Do the cleanup
                pass
        """
        if not self.lockfileName is not None:
            raise AssertionError
        elif not self.lockfileFD is not None:
            raise AssertionError
        log.debug('Leaving arena %s', self.lockfileDir)
        with global_mutex(self.workDir, self.mutex):
            try:
                os.unlink(self.lockfileName)
            except:
                pass

            self.lockfileName = None
            fcntl.lockf(self.lockfileFD, fcntl.LOCK_UN)
            os.close(self.lockfileFD)
            self.lockfileFD = None
            for item in os.listdir(self.lockfileDir):
                full_path = os.path.join(self.lockfileDir, item)
                fd = os.open(full_path, os.O_RDONLY)
                try:
                    fcntl.lockf(fd, fcntl.LOCK_SH | fcntl.LOCK_NB)
                except IOError as e:
                    break
                else:
                    try:
                        os.remove(full_path)
                    except:
                        pass

                    fcntl.lockf(fd, fcntl.LOCK_UN)
            else:
                log.debug('We are the Last Process Standing in arena %s', self.lockfileDir)
                yield True
                try:
                    os.rmdir(self.lockfileDir)
                except:
                    log.warning('Could not clean up arena %s completely: %s', self.lockfileDir, traceback.format_exc())

        log.debug('Now out of arena %s', self.lockfileDir)