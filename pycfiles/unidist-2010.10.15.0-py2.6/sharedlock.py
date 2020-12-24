# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/sharedlock.py
# Compiled at: 2010-10-14 14:04:22
"""
sharedlock

Shared Locking module.  Get access to shared locks for any program using
this procblock module's state.

NOTE(g): Locks are never stored for process restarts.  If a process goes down,
    assume all locks are lost and must be restored.  There is no way to
    determine the effect that the process restarting will have on a lock, so
    the assumption must be made that the locks have been lost.
    
    Only distributed locking can solve this, so that any given nodes loss of
    locks means nothing, because a quorum (N/2+1) must be reached before a
    new lock will be acquired, and so the restart of this lock databes node
    means nothing in itself, as a minimum of 3 nodes must be present for a
    quorum to decide on a lock.
    
    An individual node's code will restart as well, so the code will proceed
    as if no locks are already set, and start requesting locks.  This appears
    to be the right way to handle this.

TODO(g): Allow quorum-locking for multi-region locks.  This isn't about
    implementation in this module, it's about creating the method for how to
    link a number of locks together so that inside an entire system the first
    to get the (N/2)+1 locks is the victor, and all other locks are undone and
    given to the victor.  Other lock attempts must block until the quorum
    releases the lock and allows another (N/2)+1 locks to be made.
    
    Distributed lock systems allow flexibility on lock servers coming and going
    for large scale systems.  No system can be the master in this environment
    and a majority quorum must be met to enforce any lock.  Each lock server
    should attempt to gain the quorum lock before locking itself.
    
    There is a dual-layer of locking here.  The attempt-lock and the actual-lock.
    The attempt lock is this node only, the actual-lock is when a quorum has
    been reached.  Attempt locks are blocked by actual locks.
    
    All distributed locks must have a timeout specified so that the network does
    not come to a halt.
    
    To avoid dead-locks, locks must have a unique priority, so a lock name
    must register it's unique priority.  To get a lower lock, you must attain
    higher locks first, and only go from low to high.  This allows dead-locks
    to be avoided by design.  Locks must be designed as a priority so a high
    lock is never requested before a low-lock.
    
    This can be enforced by using credentials for locks, so a node request
    sessions has a crendential, and the credentials are tracked, and any
    requests from that credential must come in order, or will be rejected
    due to creating a possible dead-lock scenario.
"""
import threading, time
from log import log
import threadsafedict, sharedstate
SHARED_LOCK_CONTROL = threading.Lock()
SHARED_LOCKS = threadsafedict.ThreadSafeDict()
TIMEOUT_SLEEP_SECONDS = 0.1

class LockDoesntExist(Exception):
    """This lock does not exist, so it cant be released."""
    pass


def SharedControl_Lock():
    """Lock the shared control access to locks.  This way we can safely acquire
  an individual lock or create a new lock without a race condition.
  """
    global SHARED_LOCK_CONTROL
    SHARED_LOCK_CONTROL.acquire()


def SharedControl_Release():
    """Lock the shared control access to locks.  This way we can safely acquire
  an individual lock or create a new lock without a race condition.
  """
    SHARED_LOCK_CONTROL.release()


def LockedTimeoutRemaining(name):
    """Returns the seconds (float) until this lock times out, None if N/A."""
    global SHARED_LOCKS
    if name not in SHARED_LOCKS:
        return
    else:
        lock = SHARED_LOCKS[name]
        data = sharedstate.Get('__locks', name)
        if data and lock.locked() and data['max_duration'] != None:
            duration = time.time() - data['acquired_time']
            remaining = data['max_duration'] - duration
            return remaining
        return
        return


def IsLocked(name):
    """Returns boolean if this named lock is locked.  If doesnt exist, still False
  
  Args:
    name: string, name of lock
  """
    if name not in SHARED_LOCKS:
        return False
    else:
        lock = SHARED_LOCKS[name]
        remaining = LockedTimeoutRemaining(name)
        if remaining != None and remaining <= 0.0:
            log('Lock max_duration has timed out: %s  Releasing: %s' % (name, remaining))
            lock.release()
        locked = lock.locked()
        return locked
        return


def Acquire(name, timeout=None, save=False, max_duration=None, instantly=False):
    """Acquire the lock.
  
  Args:
    name: string, name of the lock.  Use naming convertion like:
        "top.middle.bottom" or other layered naming convertion to be able to
        maintain specific resource locks.
    timeout: float or None (optional), if float, number of seconds until timeout
    save: boolean, if True this lock will be saved to disk on restart, so
        the resource is still locked or unlocked after sharedlock's module
        has been reloaded
        TODO(g): Use state and not module, or maybe in addition to module...
    instantly: boolean, if True and timeout==None, then if this is already
        locked, we will not wait, and will fail instantly
  
  Returns: boolean, success of lock (only False if timeout is set and exceeded)
  """
    time_start = time.time()
    if name not in SHARED_LOCKS:
        SharedControl_Lock()
        if name not in SHARED_LOCKS:
            SHARED_LOCKS[name] = threading.Lock()
            data = {'max_duration': max_duration, 'acquired_time': time.time()}
            sharedstate.Set('__locks', name, data)
        SharedControl_Release()
    if timeout == None:
        if instantly == False:
            SHARED_LOCKS[name].acquire()
            data = {'max_duration': max_duration, 'acquired_time': time.time()}
            sharedstate.Set('__locks', name, data)
            return True
        else:
            success = SHARED_LOCKS[name].acquire(0)
            if success:
                data = {'max_duration': max_duration, 'acquired_time': time.time()}
                sharedstate.Set('__locks', name, data)
                return True
            return False
    else:
        while True:
            success = SHARED_LOCKS[name].acquire(0)
            duration = time.time() - time_start
            if success:
                data = {'max_duration': max_duration, 'acquired_time': time.time()}
                sharedstate.Set('__locks', name, data)
                return success
            if duration > timeout or timeout == 0:
                return success

        return


def Release(name):
    """Acquire the lock.
  
  TODO(g): Could have optional secret to enforce who can release this lock...
  
  Args:
    name: string, name of the lock.  Use naming convertion like:
        "top.middle.bottom" or other layered naming convertion to be able to
        maintain specific resource locks.
    time: float or None (optional), if float, number of seconds until timeout
  """
    if name not in SHARED_LOCKS:
        raise LockDoesntExist(name)
    sharedstate.Set('__locks', name, None)
    SHARED_LOCKS[name].release()
    return


def FindAllLocked():
    """Returns a list of strings, for the names of all the locks currentl locked."""
    all_locks = []
    keys = SHARED_LOCKS.keys()
    for key in keys:
        if IsLocked(key):
            all_locks.append(key)

    all_locks.sort()
    return all_locks


if __name__ == '__main__':
    Acquire('one')
    Acquire('two')
    print 'Currently locked locks: %s' % FindAllLocked()
    success = Acquire('one', 2)
    IsLocked('two')
    Release('two')
    IsLocked('two')
    Release('one')
    Acquire('one')
    print 'Currently locked locks: %s' % FindAllLocked()