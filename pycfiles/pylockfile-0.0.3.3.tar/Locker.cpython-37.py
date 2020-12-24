# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pylocker/Locker.py
# Compiled at: 2020-01-09 17:07:19
# Size of source mod 2**32: 24883 bytes
from __future__ import print_function
import os, sys, time, atexit, signal, threading, uuid
try:
    basestring
except:
    basestring = str

try:
    from psutil import pid_exists
except:
    if os.name == 'posix':
        import errno

        def pid_exists(pid):
            if pid < 0:
                return False
                if pid == 0:
                    raise ValueError('invalid PID 0')
            else:
                try:
                    os.kill(pid, 0)
                except OSError as err:
                    try:
                        if err.errno == errno.ESRCH:
                            return False
                        if err.errno == errno.EPERM:
                            return True
                        raise
                    finally:
                        err = None
                        del err

                else:
                    return True


    else:
        import ctypes

        def pid_exists(pid):
            processHandle = ctypes.windll.kernel32.OpenProcess(4096, 0, pid)
            if processHandle == 0:
                return False
            ctypes.windll.kernel32.CloseHandle(processHandle)
            return True


VERBOSE = False
RAISE_ERROR = False

class Locker(object):
    """Locker"""

    def __init__(self, filePath, lockPass, mode='ab', lockPath=None, timeout=60, wait=0, deadLock=120):
        self._Locker__fd = None
        self._Locker__pid = str(os.getpid())
        self._Locker__uniqueID = str(uuid.uuid1()) + '_' + self._Locker__pid
        self.set_file_path(filePath)
        self.set_mode(mode)
        self.set_lock_pass(lockPass)
        self.set_lock_path(lockPath)
        self.set_wait(wait)
        self.set_timeout(timeout)
        self.set_dead_lock(deadLock)
        atexit.register(self.release_lock)
        if threading.current_thread().__class__.__name__ == '_MainThread':
            signal.signal(signal.SIGINT, self._Locker__signal_handler)

    def __enter__(self):
        acquired, code = self.acquire_lock()
        if acquired and self._Locker__filePath is not None:
            self._Locker__fd = open(self._Locker__filePath, self._Locker__mode)
        else:
            self._Locker__fd = None
        return (acquired, code, self._Locker__fd)

    def __exit__(self, type, value, traceback):
        self.release_lock()

    def __del__(self):
        self.release_lock()

    def __signal_handler(self, signal, frame):
        self.release_lock()
        sys.exit(0)

    @property
    def filePath(self):
        """locker file path"""
        return self._Locker__filePath

    @property
    def lockPass(self):
        """locker pass"""
        return self._Locker__lockPass

    @property
    def lockPath(self):
        """locker lock path"""
        return self._Locker__lockPath

    @property
    def timeout(self):
        """locker timeout in seconds"""
        return self._Locker__timeout

    @property
    def wait(self):
        """locker wait in seconds"""
        return self._Locker__wait

    @property
    def deadLock(self):
        """locker deadLock in seconds"""
        return self._Locker__deadLock

    def set_mode(self, mode):
        """
        Set file opening mode.

        :Parameters:
            #. mode (string): This is file opening mode and it can be any of
               r , r+ , w , w+ , a , a+ . If filePath is None, this argument
               will be discarded.

               *  r : Open text file for reading.  The stream is positioned at the
                  beginning of the file.

               *  r+ : Open for reading and writing.  The stream is positioned at the
                  beginning of the file.

               *  w : Truncate file to zero length or create text file for writing.
                  The stream is positioned at the beginning of the file.

               *  w+ : Open for reading and writing.  The file is created if it does not
                  exist, otherwise it is truncated.  The stream is positioned at
                  the beginning of the file.

               *  a : Open for writing.  The file is created if it does not exist.  The
                  stream is positioned at the end of the file.  Subsequent writes
                  to the file will always end up at the then current end of file,
                  irrespective of any intervening fseek(3) or similar.

               *  a+ : Open for reading and writing.  The file is created if it does not
                  exist. The stream is positioned at the end of the file.  Subsequent
                  writes to the file will always end up at the then current
                  end of file, irrespective of any intervening fseek(3) or similar.
        """
        assert mode in ('r', 'rb', 'r+', 'rb+', 'w', 'wb', 'w+', 'wb', 'wb+', 'a',
                        'ab', 'a+', 'ab+'), "mode must be any of 'r','rb','r+','rb+','w','wb','w+','wb','wb+','a','ab','a+','ab+' '%s' is given" % mode
        self._Locker__mode = mode

    def set_file_path(self, filePath):
        """
        Set the file path that needs to be locked.

        :Parameters:
            #. filePath (None, path): The file that needs to be locked. When given and a lock
               is acquired, the file will be automatically opened for writing or reading
               depending on the given mode. If None is given, the locker can always be used
               for its general purpose as shown in the examples.
        """
        if filePath is not None:
            assert isinstance(filePath, basestring), 'filePath must be None or string'
            filePath = str(filePath)
        self._Locker__filePath = filePath

    def set_lock_pass(self, lockPass):
        """
        Set the locking pass

        :Parameters:
            #. lockPass (string): The locking pass.
        """
        assert isinstance(lockPass, basestring), 'lockPass must be string'
        lockPass = str(lockPass)
        assert '\n' not in lockPass, 'lockPass must be not contain a new line'
        self._Locker__lockPass = lockPass

    def set_lock_path(self, lockPath):
        """
        Set the managing lock file path.

        :Parameters:
            #. lockPath (None, path): The locking file path. If None is given the locking file
               will be automatically created to '.lock' in the filePath directory. If
               filePath is None, '.lock' will be created in the current working directory.
        """
        if lockPath is not None:
            assert isinstance(lockPath, basestring), 'lockPath must be None or string'
            lockPath = str(lockPath)
        else:
            self._Locker__lockPath = lockPath
            if self._Locker__lockPath is None:
                if self._Locker__filePath is None:
                    self._Locker__lockPath = os.path.join(os.getcwd(), '.lock')
                else:
                    self._Locker__lockPath = os.path.join(os.path.dirname(self._Locker__filePath), '.lock')

    def set_timeout(self, timeout):
        """
        set the timeout limit.

        :Parameters:
            #. timeout (number): The maximum delay or time allowed to successfully set the
               lock. When timeout is exhausted before successfully setting the lock,
               the lock ends up not acquired.
        """
        try:
            timeout = float(timeout)
            assert timeout >= 0
            assert timeout >= self._Locker__wait
        except:
            raise Exception('timeout must be a positive number bigger than wait')

        self._Locker__timeout = timeout

    def set_wait(self, wait):
        """
        set the waiting time.

        :Parameters:
            #. wait (number): The time delay between each attempt to lock. By default it's
               set to 0 to keeping the aquiring mechanism trying to acquire the lock without
               losing any time waiting. Setting wait to a higher value suchs as 0.05 seconds
               or higher can be very useful in special cases when many processes are trying
               to acquire the lock and one of them needs to hold it a release it at a higher
               frequency or rate.
        """
        try:
            wait = float(wait)
            assert wait >= 0
        except:
            raise Exception('wait must be a positive number')

        self._Locker__wait = wait

    def set_dead_lock(self, deadLock):
        """
        Set the dead lock time.

        :Parameters:
            #. deadLock (number): The time delay judging if the lock was left out mistakenly
               after a system crash or other unexpected reasons. Normally Locker is stable
               and takes care of not leaving any locking file hanging even it crashes or it
               is forced to stop by a user signal.
        """
        try:
            deadLock = float(deadLock)
            assert deadLock >= 0
        except:
            raise Exception('deadLock must be a positive number')

        self._Locker__deadLock = deadLock

    def acquire_lock(self, verbose=VERBOSE, raiseError=RAISE_ERROR):
        """
        Try to acquire the lock.

        :Parameters:
            #. verbose (bool): Whether to be verbose about errors when encountered
            #. raiseError (bool): Whether to raise error exception when encountered

        :Returns:
            #. result (boolean): Whether the lock is succesfully acquired.
            #. code (integer, Exception): Integer code indicating the reason how the
               lock was successfully set or unsuccessfully acquired. When setting the
               lock generates an error, this will be caught and returned in a message
               Exception code.

               *  0: Lock is successfully set for normal reasons, In this case result
                  is True.
               *  1: Lock was already set, no need to set it again. In this case result
                  is True.
               *  2: Old and forgotten lock is found and removed. New lock is
                  successfully set, In this case result is True.
               *  3: Lock was not successfully set before timeout. In this case result
                  is False.
               *  Exception: Lock was not successfully set because of an unexpected error.
                  The error is caught and returned in this Exception. In this case
                  result is False.
        """
        code = 0
        acquired = False
        t0 = t1 = time.time()
        LP = self._Locker__lockPass + '\n'
        bytesLP = LP.encode()
        _lockingText = LP + '%.6f' + '\n%s' % self._Locker__pid
        _timeout = self._Locker__timeout
        while t1 - t0 <= _timeout:
            try:
                while not acquired:
                    if t1 - t0 <= _timeout:
                        if os.path.isfile(self._Locker__lockPath):
                            try:
                                with open(self._Locker__lockPath, 'rb') as (fd):
                                    lock = fd.readlines()
                            except:
                                pass
                            else:
                                if len(lock) != 3:
                                    code = 0
                                    acquired = True
                                    break
                                if lock[0] == bytesLP:
                                    code = 1
                                    acquired = True
                                    break
                                if t1 - float(lock[1]) > self._Locker__deadLock:
                                    acquired = True
                                    code = 2
                                    break
                                if not pid_exists(int(lock[2])):
                                    acquired = True
                                    code = 2
                                    break
                                if self._Locker__wait:
                                    time.sleep(self._Locker__wait)
                                t1 = time.time()
                        else:
                            acquired = True
                            break

            except Exception as err:
                try:
                    code = Exception('Failed to check the lock (%s)' % (str(err),))
                    acquired = False
                    if verbose:
                        print(str(code))
                    if raiseError:
                        raise code
                finally:
                    err = None
                    del err

            if not acquired:
                break
            try:
                tic = time.time()
                tmpFile = self._Locker__lockPath
                if os.name == 'posix':
                    tmpFile = '%s_%s' % (self._Locker__lockPath, self._Locker__uniqueID)
                with open(tmpFile, 'wb') as (fd):
                    fd.write(str(_lockingText % t1).encode())
                    fd.flush()
                    os.fsync(fd.fileno())
                if os.name == 'posix':
                    os.rename(tmpFile, self._Locker__lockPath)
                toc = time.time()
                if toc - tic > 1:
                    print("PID '%s' writing '%s' is delayed by os for %s seconds. Lock timeout adjusted. MUST FIND A WAY TO FIX THAT" % (self._Locker__pid, self._Locker__lockPath, str(toc - tic)))
                    _timeout += toc - tic
            except Exception as err:
                try:
                    code = Exception('Failed to write the lock (%s)' % (str(err),))
                    acquired = False
                    if verbose:
                        print(str(code))
                    if raiseError:
                        raise code
                    break
                finally:
                    err = None
                    del err

            s = max([toc - tic, 0.0001])
            time.sleep(s)
            try:
                with open(self._Locker__lockPath, 'rb') as (fd):
                    lock = fd.readlines()
            except:
                lock = []

            if len(lock) >= 1:
                if lock[0] == bytesLP:
                    acquired = True
                    break
                else:
                    acquired = False
                    t1 = time.time()
                    continue
            else:
                acquired = False
                t1 = time.time()
                continue

        if not acquired:
            if not code:
                code = 3
        return (
         acquired, code)

    def release_lock(self, verbose=VERBOSE, raiseError=RAISE_ERROR):
        """
        Release the lock when set and close file descriptor if opened.

        :Parameters:
            #. verbose (bool): Whether to be verbose about errors when encountered
            #. raiseError (bool): Whether to raise error exception when encountered

        :Returns:
            #. result (boolean): Whether the lock is succesfully released.
            #. code (integer, Exception): Integer code indicating the reason how the
               lock was successfully or unsuccessfully released. When releasing the
               lock generates an error, this will be caught and returned in a message
               Exception code.

               *  0: Lock is not found, therefore successfully released
               *  1: Lock is found empty, therefore successfully released
               *  2: Lock is found owned by this locker and successfully released
               *  3: Lock is found owned by this locker and successfully released and locked file descriptor was successfully closed
               *  4: Lock is found owned by another locker, this locker has no permission to release it. Therefore unsuccessfully released
               *  Exception: Lock was not successfully released because of an unexpected error.
                  The error is caught and returned in this Exception. In this case
                  result is False.

        """
        if not os.path.isfile(self._Locker__lockPath):
            released = True
            code = 0
        else:
            try:
                with open(self._Locker__lockPath, 'rb') as (fd):
                    lock = fd.readlines()
            except Exception as err:
                try:
                    code = Exception("Unable to read release lock file '%s' (%s)" % (self._Locker__lockPath, str(err)))
                    released = False
                    if verbose:
                        print(str(code))
                    if raiseError:
                        raise code
                finally:
                    err = None
                    del err

            else:
                if not len(lock):
                    code = 1
                    released = True
                elif lock[0].rstrip() == self._Locker__lockPass.encode():
                    try:
                        with open(self._Locker__lockPath, 'wb') as (f):
                            f.write(''.encode())
                            f.flush()
                            os.fsync(f.fileno())
                    except Exception as err:
                        try:
                            released = False
                            code = Exception("Unable to write release lock file '%s' (%s)" % (self._Locker__lockPath, str(err)))
                            if verbose:
                                print(str(code))
                            if raiseError:
                                raise code
                        finally:
                            err = None
                            del err

                    else:
                        released = True
                        code = 2
                else:
                    code = 4
                    released = False
        if released:
            if self._Locker__fd is not None:
                try:
                    if not self._Locker__fd.closed:
                        self._Locker__fd.flush()
                        os.fsync(self._Locker__fd.fileno())
                        self._Locker__fd.close()
                except Exception as err:
                    try:
                        code = Exception("Unable to close file descriptor of locked file '%s' (%s)" % (self._Locker__filePath, str(err)))
                        if verbose:
                            print(str(code))
                        if raiseError:
                            raise code
                    finally:
                        err = None
                        del err

                else:
                    code = 3
        return (
         released, code)

    def acquire(self, *args, **kwargs):
        """Alias to acquire_lock"""
        return (self.acquire_lock)(*args, **kwargs)

    def release(self, *args, **kwargs):
        """Alias to release_lock"""
        return (self.release_lock)(*args, **kwargs)