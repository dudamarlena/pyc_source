# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/a_sync/examples.py
# Compiled at: 2016-12-23 16:13:40
# Size of source mod 2**32: 3254 bytes
"""Example Use."""
import asyncio, time, a_sync

def examples() -> None:
    """Run examples."""

    def hello(name: str, seconds: int) -> str:
        """
        Hello.

        Prints 'hello <name>', waits for <seconds> seconds, and then
        prints 'bye <name>' and returns the name.

        Args:
            name - the name to say hello to.
            seconds - the seconds to wait to say bye.

        Returns:
            name - the given name.
        """
        print('hello {}'.format(name))
        time.sleep(seconds)
        print('bye {}'.format(name))
        return name

    def async_hello(name: str, seconds: int) -> str:
        """
        Hello.

        Prints 'hello <name>', waits for <seconds> seconds, and then
        prints 'bye <name>' and returns the name.

        Args:
            name - the name to say hello to.
            seconds - the seconds to wait to say bye.

        Returns:
            name - the given name.
        """
        print('hello {}'.format(name))
        await asyncio.sleep(seconds)
        print('bye {}'.format(name))
        return name

    background_thread = a_sync.queue_background_thread(hello, 'background-joe', 20)
    parallel_1 = a_sync.Parallel()
    parallel_1.schedule(hello, 'joe', 5)
    parallel_1.schedule(hello, 'sam', 3)
    parallel_1.schedule(async_hello, 'bob', 1)
    parallel_2 = a_sync.Parallel()
    parallel_2.schedule(async_hello, 'jill', 4)
    parallel_2.schedule(async_hello, 'jane', 2)
    parallel_2.schedule(hello, 'mary', 1)
    serial_1 = a_sync.Serial()
    serial_1.schedule(parallel_1.run)
    serial_1.schedule(parallel_2.block)
    parallel_3 = a_sync.Parallel()
    parallel_3.schedule(async_hello, 'joseph', 5)
    parallel_3.schedule(hello, 'joey', 3)
    parallel_3.schedule(async_hello, 'jo', 1)
    parallel_4 = a_sync.Parallel()
    parallel_4.schedule(hello, 'alex', 4)
    parallel_4.schedule(async_hello, 'alexandria', 2)
    parallel_4.schedule(hello, 'alexandra', 1)
    serial_2 = a_sync.Serial()
    serial_2.schedule(parallel_3.run)
    serial_2.schedule(parallel_4.block)
    final_parallel = a_sync.Parallel()
    final_parallel.schedule(serial_1.block)
    final_parallel.schedule(serial_2.run)
    final_parallel.block()
    background_thread.result()


if __name__ == '__main__':
    examples()