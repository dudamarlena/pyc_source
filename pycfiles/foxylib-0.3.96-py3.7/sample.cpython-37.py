# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/async/tests/sample.py
# Compiled at: 2020-01-06 01:07:42
# Size of source mod 2**32: 3484 bytes
import datetime, heapq, types, time

class Task:
    __doc__ = "Represent how long a coroutine should wait before starting again.\n\n    Comparison operators are implemented for use by heapq. Two-item\n    tuples unfortunately don't work because when the datetime.datetime\n    instances are equal, comparison falls to the coroutine and they don't\n    implement comparison methods, triggering an exception.\n\n    Think of this as being like asyncio.Task/curio.Task.\n    "

    def __init__(self, wait_until, coro):
        self.coro = coro
        self.waiting_until = wait_until

    def __eq__(self, other):
        return self.waiting_until == other.waiting_until

    def __lt__(self, other):
        return self.waiting_until < other.waiting_until


class SleepingLoop:
    __doc__ = 'An event loop focused on delaying execution of coroutines.\n\n    Think of this as being like asyncio.BaseEventLoop/curio.Kernel.\n    '

    def __init__(self, *coros):
        self._new = coros
        self._waiting = []

    def run_until_complete(self):
        for coro in self._new:
            wait_for = coro.send(None)
            heapq.heappush(self._waiting, Task(wait_for, coro))

        while self._waiting:
            now = datetime.datetime.now()
            task = heapq.heappop(self._waiting)
            if now < task.waiting_until:
                delta = task.waiting_until - now
                time.sleep(delta.total_seconds())
                now = datetime.datetime.now()
            try:
                wait_until = task.coro.send(now)
                heapq.heappush(self._waiting, Task(wait_until, task.coro))
            except StopIteration:
                pass


@types.coroutine
def sleep(seconds):
    """Pause a coroutine for the specified number of seconds.

    Think of this as being like asyncio.sleep()/curio.sleep().
    """
    now = datetime.datetime.now()
    wait_until = now + datetime.timedelta(seconds=seconds)
    actual = yield wait_until
    return actual - now


async def countdown(label, length, *, delay=0):
    """Countdown a launch for `length` seconds, waiting `delay` seconds.

    This is what a user would typically write.
    """
    print(label, 'waiting', delay, 'seconds before starting countdown')
    delta = await sleep(delay)
    print(label, 'starting after waiting', delta)
    while length:
        print(label, 'T-minus', length)
        waited = await sleep(1)
        length -= 1

    print(label, 'lift-off!')


def main():
    """Start the event loop, counting down 3 separate launches.

    This is what a user would typically write.
    """
    loop = SleepingLoop(countdown('A', 5), countdown('B', 3, delay=2), countdown('C', 4, delay=1))
    start = datetime.datetime.now()
    loop.run_until_complete()
    print('Total elapsed time is', datetime.datetime.now() - start)


if __name__ == '__main__':
    main()