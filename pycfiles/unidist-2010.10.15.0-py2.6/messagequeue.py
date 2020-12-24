# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/messagequeue.py
# Compiled at: 2010-10-14 14:04:23
"""
messagequeue

Message Queue management

TODO(g): Add auto-deleting options by count or age.  Date tag their arrival
    in a dict so we can track stuff about it, and can maybe skip it.

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
import threadsafedict, threadsafelist
MESSAGE_QUEUES = threadsafedict.ThreadSafeDict()

def QueueExists(queue):
    """Does this queue exist?
  
  Args:
    queue: string, name space for messages
  
  Returns: boolean, True if queue namespace already exists
  """
    global MESSAGE_QUEUES
    if queue not in MESSAGE_QUEUES:
        return False
    else:
        return True


def AddMessage(queue, message):
    """Adds a message to a specified queue.
  
  Args:
    queue: string, name space for messages
    message: any, data to store in queue
  """
    if queue not in MESSAGE_QUEUES:
        MESSAGE_QUEUES[queue] = threadsafelist.ThreadSafeList()
    MESSAGE_QUEUES[queue].append(message)


def GetMessageCount(queue):
    """
  Returns the number of messages in a queue.
  
  Args:
    queue: string, name space for messages
  
  Returns: int, number of messages in specified queue
  """
    if queue not in MESSAGE_QUEUES:
        return None
    else:
        return len(MESSAGE_QUEUES[queue])


def GetMessage_Oldest(queue, remove=True):
    """Returns the oldest message in the queue(0).
  
  Args:
    queue: string, name space for messages
    remove: boolean, remove the message from the queue?
  """
    if queue not in MESSAGE_QUEUES or not MESSAGE_QUEUES[queue]:
        return None
    else:
        message = MESSAGE_QUEUES[queue][0]
        if remove:
            MESSAGE_QUEUES[queue].remove(message)
        return message


def GetMessage_Newest(queue, remove=True):
    """Returns the oldest message in the queue(-1).
  
  Args:
    queue: string, name space for messages
    remove: boolean, remove the message from the queue?
  """
    if queue not in MESSAGE_QUEUES or not MESSAGE_QUEUES[queue]:
        return None
    else:
        message = MESSAGE_QUEUES[queue][(-1)]
        if remove:
            del MESSAGE_QUEUES[queue][-1]
        return message


def GetAllMessages(queue):
    """Returns all the messages in the queue, for inspection purposes.
  
  Args:
    queue: string, name space for messages
  """
    if queue not in MESSAGE_QUEUES or not MESSAGE_QUEUES[queue]:
        return
    else:
        return MESSAGE_QUEUES[queue]
        return


if __name__ == '__main__':
    queue = 'testing'
    print QueueExists(queue)
    AddMessage(queue, 1)
    AddMessage(queue, 2)
    AddMessage(queue, 3)
    print GetMessage_Newest(queue)
    print GetMessage_Oldest(queue)
    print GetMessageCount(queue)