# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/sharedcounter.py
# Compiled at: 2010-10-14 14:04:23
"""
sharedcounter

Shared Counter module.  Get access to shared counters.  Numeric values, which
can be atomically get/set, or atomically incremented.

TODO(g): Implement serialization, archiving, snapshotting, and replication to
sharestate.  This will allow us flexibility in many things.  This is not
necessarily going to be the best scaling solution, but it will work and provide
a way to keep state and distribute.  Name spaces should have this specified
individually.  If not specified, state will not be archived, serialized,
snapshotted or replicated.

  * Use the "archive" and "snapshot" modules for this, so archival and
      snapshotting is universal.  Ensure a process restart will do the right
      thing in attempting to restore from snapshot, then archive, if present.
      
      TODO(g): Merge achive and snapshot.  They are the same technology.  If we
          really want to keep state, then we must archive each transactions and
          snapshot to avoid having to replay too many archives.
"""
import threading, threadsafedict
SHARED_COUNTERS = threadsafedict.ThreadSafeDict()
SHARED_COUNTER_LOCKS = threadsafedict.ThreadSafeDict_IgnoreOverwrites()

class CounterDoesntExist(Exception):
    """This counter does not exist, so it cannot by returned."""
    pass


def _LockCounter(name):
    """Lock a counter for operations.
  
  Args:
    name: string, name of the counter
  """
    global SHARED_COUNTER_LOCKS
    if name not in SHARED_COUNTER_LOCKS:
        SHARED_COUNTER_LOCKS[name] = threading.Lock()
    SHARED_COUNTER_LOCKS[name].acquire()


def _UnlockCounter(name):
    """Unlock a counter after operations.
  
  Args:
    name: string, name of the counter
  """
    if name not in SHARED_COUNTER_LOCKS:
        raise CounterDoesntExist('Not found: %s' % name)
    SHARED_COUNTER_LOCKS[name].release()


def Get(name):
    """Returns the value of this counter, or CounterDoesntExist class.
  
  If named counter does not exist, starts counter value at zero.
  
  Args:
    name: string, name of the counter
  """
    global SHARED_COUNTERS
    if name not in SHARED_COUNTERS:
        Set(name, 0)
        return 0
    else:
        value = SHARED_COUNTERS[name]
        return value


def Set(name, value):
    """Sets the named counter to this value.  Should be numeric, but is not tested.
  
  
  Args:
    name: string, name of the counter
    value: int, value to set this counter.  This is using the counter as a
        numeric state, not a real counter, but it's here for functionality not
        being strictly semantic about what a counter is.
  
  Returns: int, value after setting (for consistency between other functions).
  """
    try:
        _LockCounter(name)
        SHARED_COUNTERS[name] = value
        return SHARED_COUNTERS[name]
    finally:
        _UnlockCounter(name)


def GetSet(name, value):
    """Sets the named counter to this value.  Returns the previous value.
  
  Args:
    name: string, name of the counter
    value: int, value to set this counter.  This is using the counter as a
        numeric state, not a real counter, but it's here for functionality not
        being strictly semantic about what a counter is.
  
  Returns: int, value of the counter, before the new value was set
  """
    try:
        _LockCounter(name)
        if name not in SHARED_COUNTERS:
            previous_value = 0
        else:
            previous_value = SHARED_COUNTERS[name]
        SHARED_COUNTERS[name] = value
        return previous_value
    finally:
        _UnlockCounter(name)


def GetIncrement(name, value=1):
    """Increments the named counter to this value.  Returns the previous value.
  
  If named counter does not exist, starts counter value at zero.
  
  Args:
    name: string, name of the counter
    value: int (optional), value to increment this counter by.  Default is 1.
  
  Returns: int, value of counter before it was incremented.
  """
    try:
        _LockCounter(name)
        if name not in SHARED_COUNTERS:
            previous_value = 0
        else:
            previous_value = SHARED_COUNTERS[name]
        SHARED_COUNTERS[name] = previous_value + value
        return previous_value
    finally:
        _UnlockCounter(name)


def Increment(name, value=1):
    """Increments the named counter by value (default is 1).  Returns the new
  value.
  
  If named counter does not exist, starts counter value at zero.
  
  Args:
    name: string, name of the counter
    value: int (optional), value to increment this counter by.  Default is 1.
  
  Returns: int, value of the counter after it has been incremented
  """
    try:
        _LockCounter(name)
        if name not in SHARED_COUNTERS:
            previous_value = 0
        else:
            previous_value = SHARED_COUNTERS[name]
        SHARED_COUNTERS[name] = previous_value + value
        return SHARED_COUNTERS[name]
    finally:
        _UnlockCounter(name)


def GetAllCounters():
    """Returns a dict (copy) of all the counters we have."""
    counters = dict(SHARED_COUNTERS)
    return counters


if __name__ == '__main__':
    print Get('bongo')
    print Set('bongo', 5)
    print GetSet('bongo', 10)
    print GetSet('bongo', 15)
    print GetIncrement('bongo')
    print GetIncrement('bongo')
    print Increment('bongo')
    print Increment('bongo')
    print Increment('bongo', 5)