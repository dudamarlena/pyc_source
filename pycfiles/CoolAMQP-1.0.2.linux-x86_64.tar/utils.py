# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python2.7.15/lib/python2.7/site-packages/coolamqp/attaches/utils.py
# Compiled at: 2020-04-03 16:00:47
from __future__ import print_function, absolute_import, division
import functools, logging, threading
logger = logging.getLogger(__name__)

class ConfirmableRejectable(object):
    """
    Protocol for objects put into AtomicTagger. You need not subclass it,
    just support this protocol.
    """
    __slots__ = ()

    def confirm(self):
        """
        This has been ACK'd
        :return: don't care
        """
        pass

    def reject(self):
        """
        This has been REJECT'd/NACK'd
        :return: don't care
        """
        pass


class FutureConfirmableRejectable(ConfirmableRejectable):
    """
    A ConfirmableRejectable that can result a future (with None),
    or Exception it with a message
    """
    __slots__ = ('future', )

    def __init__(self, future):
        self.future = future

    def confirm(self):
        self.future.set_result(None)
        return

    def reject(self):
        self.future.set_exception(Exception())


class AtomicTagger(object):
    """
    This implements a thread-safe dictionary of (integer=>ConfirmableRejectable | None),
    used for processing delivery tags / (negative) acknowledgements.
        - you can requisition a key. This key belongs only to you, and the whole world
          doesn't know you have it.

            delivery_tag_to_use = tagger.get_key()

        - you can deposit a ConfirmableRejectable into the  tagger.

            tagger.deposit(delivery_tag, message)

         After you do so, this tag is subject to be acked/nacked. Read on.

        - you can (multiple)(ack/nack) messages. This coresponds to multiple bit
          used in basic.ack/basic.nack.

          If this is done, your message objects (that MUST implement the
          ConfirmableRejectable protocol) will have respective methods called.
          These methods MUST NOT depend on particular state of locking by this
          object.

    Thread safety is implemented using reentrant locking. The lock object is a
    threading.RLock, and you can access it at atomicTagger.lock.

    Please note that delivery tags are increasing non-negative integer.
    Therefore, X>Y implies that sending/receiving X happened after Y.

    Note that key/delivery_tag of 0 has special meaning of "everything so far".

    This has to be fast for most common cases. Corner cases will be resolved correctly,
    but maybe not fast.
    """
    __slots__ = ('lock', 'next_tag', 'tags')

    def __init__(self):
        self.lock = threading.RLock()
        self.next_tag = 1
        self.tags = []

    def deposit(self, tag, obj):
        """
        Put a tag into the tag list.

        Putting the same tag more than one time will result in undefined behaviour.

        :param tag: non-negative integer
        :param obj: ConfirmableRejectable
                    if you put something that isn't a ConfirmableRejectable, you won't get bitten
                    until you call .ack() or .nack().
        """
        assert tag >= 0
        opt = (tag, obj)
        with self.lock:
            if len(self.tags) == 0:
                self.tags.append(opt)
            elif self.tags[(-1)][0] < tag:
                self.tags.append(opt)
            else:
                i = len(self.tags) - 1
                while i > 0:
                    if self.tags[i][0] > tag:
                        break
                    i -= 1

                self.tags.insert(i, opt)

    def __acknack(self, tag, multiple, ack):
        """
        :param tag: Note that 0 means "everything"
        :param ack: True to ack, False to nack
        """
        with self.lock:
            start = 0
            if tag > 0:
                if multiple:
                    for stop, opt in enumerate(self.tags):
                        if opt[0] == tag:
                            stop += 1
                            break
                        if opt[0] > tag:
                            break
                    else:
                        stop = len(self.tags)

                else:
                    for index, opt in enumerate(self.tags):
                        if opt[0] == tag:
                            stop = index + 1
                            break
                    else:
                        return

                if not multiple:
                    start = stop - 1
            else:
                stop = len(self.tags)
            items = self.tags[start:stop]
            del self.tags[start:stop]
        for tag, cr in items:
            if ack:
                cr.confirm()
            else:
                cr.reject()

    def ack(self, tag, multiple):
        """
        Acknowledge given objects.

        If multiple, objects UP TO AND INCLUDING tag will have .confirm() called.
        If it's false, only this precise objects will have done so.
        It this object does not exist, nothing will happen. Acking same tag more than one time
        is a no-op.

        Things acked/nacked will be evicted from .data
        :param tag: delivery tag to use. Note that 0 means "everything so far"
        """
        self.__acknack(tag, multiple, True)

    def nack(self, tag, multiple):
        """
        Acknowledge given objects.

        If multiple, objects UP TO AND INCLUDING tag will have .confirm() called.
        If it's false, only this precise objects will have done so.
        It this object does not exist, nothing will happen. Acking same tag more than one time
        is a no-op.

        Things acked/nacked will be evicted from .data
        :param tag: delivery tag to use. Note that 0 means "everything so far"
        """
        self.__acknack(tag, multiple, False)

    def get_key(self):
        """
        Return a key. It won't be seen here until you deposit it.

        It's just yours, and you can do whatever you want with it, even drop on the floor.
        :return: a positive integer
        """
        with self.lock:
            self.next_tag += 1
            return self.next_tag - 1


class Synchronized(object):
    """
    I have a lock and can sync on it. Use like:

    class Synced(Synchronized):

        @synchronized
        def mandatorily_a_instance_method(self, ...):
            ...

    """

    def __init__(self):
        self._monitor_lock = threading.Lock()

    def get_monitor_lock(self):
        return self._monitor_lock

    @staticmethod
    def synchronized(fun):

        @functools.wraps(fun)
        def monitored(*args, **kwargs):
            with args[0]._monitor_lock:
                return fun(*args, **kwargs)

        return monitored