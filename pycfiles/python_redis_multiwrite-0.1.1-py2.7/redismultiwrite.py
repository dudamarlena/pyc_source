# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/redismultiwrite.py
# Compiled at: 2013-04-23 14:25:57
"""The redismultiwrite module provides a wrapper to the python redis client,
exposing functions that will mimic multi-master behavior by performing some
write operations to several extra specified hosts before returning.

"""
import logging, redis
from eventlet.greenpool import GreenPool, GreenPile
from eventlet import greenthread

class RedisMultiWriteError(redis.RedisError):
    """Base class for redismultiwrite errors."""
    pass


class TooManyRetries(redis.ConnectionError):
    """Exception thrown when an operation exceeds its allowed number of retries.
    
    """

    def __init__(self, exc, host):
        super(TooManyRetries, self).__init__(exc.message)
        self.host = host


class RedisMultiWrite(object):
    """Extends the functionality of the redis python client to perform some
    operations to a local redis instance as well as several remote instances
    for synchronization.
    
    """

    def __init__(self, local, remote=None, retries=3, log=None, pool_size=None, wait_for_remote=False):
        """Creates a new RedisMultiWrite object.

        :param local: A StrictRedis object representing a connection to the
                      local redis instance.
        :param remote: A list of StrictRedis objects representing connections to
                       remote redis instances. Default: empty list.
        :param retries: The number of times a write operation should be retried
                        on connection errors before failure. If this number is
                        exceeded, TooManyRetries is thrown with the error
                        message of the last attempt. Default: 3.
        :param log: The python-style log destination object. Defaults to the
                    standard destination of the `logging` module.
        :param pool_size: The size of the `GreenPool`. See the `eventlet`
                          library for details and default value.
        :param wait_for_remote: If False, a request will return as soon as the
                                local connection has handled it and the remote
                                connections will continue in the background.
                                If True, the request will only return once all
                                connections have completed.

        """
        self.local = local
        self.remote = remote or []
        self.retries = retries
        self.log = log or logging
        self.pool = GreenPool(pool_size) if pool_size else GreenPool()
        self.wait_for_remote = wait_for_remote

    def __getattr__(self, name):
        """Regular methods on this object will be redirected to the local redis
        object given in the constructor. Methods suffixed with `_everywhere`
        will be performed everywhere.

        :param name: The method name passed to the local instance.

        """
        if name.endswith('_everywhere'):
            name, everywhere = name.rsplit('_', 1)
            getattr(self.local, name)

            def intercept(*args):
                return self.run_everywhere(name, args)

            return intercept
        else:
            return getattr(self.local, name)

    def _wait_pile(self, pile):
        while True:
            try:
                pile.next()
            except StopIteration:
                break
            except TooManyRetries as e:
                self.log.error(e.message)
            except Exception:
                self.log.exception('Unhandled Exception')

    def _simple_exec(self, conn, command):
        op, args = command
        return getattr(conn, op)(*args)

    def _pipe_exec(self, conn, commands):
        pipe = conn.pipeline()
        for op, args in commands:
            getattr(pipe, op)(*args)

        return pipe.execute()

    def _run_all(self, executor, data):
        if not self.remote:
            return self._attempt(self.local, executor, data)
        pile = GreenPile(self.pool)
        ret = self.pool.spawn(self._attempt, self.local, executor, data)
        for server in self.remote:
            pile.spawn(self._attempt, server, executor, data)

        try:
            try:
                return ret.wait()
            except TooManyRetries as e:
                self.log.error(e.message)
                raise

        finally:
            if self.wait_for_remote:
                self._wait_pile(pile)
            else:
                self.pool.spawn(self._wait_pile, pile)

    def _attempt(self, conn, executor, data):
        try:
            host = conn.connection_pool.connection_kwargs['host']
        except (AttributeError, KeyError):
            host = '[Unknown]'

        last_connection_error = None
        for i in range(self.retries):
            try:
                return executor(conn, data)
            except redis.ConnectionError as e:
                self.log.warn('Connectivity issue with ' + host)
                last_connection_error = e
            except redis.RedisError as e:
                self.log.exception('Redis exception with ' + host)
                greenthread.sleep(0)
                raise e

        greenthread.sleep(0)
        raise TooManyRetries(last_connection_error, host)
        return

    def run_everywhere(self, command, args):
        """Runs the command with the given args on the local instance and all
        remote redis instances. This operation is not atomic. The return value
        and/or exception thrown will only come from the local instance, but the
        method will not return until all child operations are finished.

        :param command: The command to run, as it would be given as a method to
                        the python redis library, e.g. 'delete' or 'expire'.
        :param args: Tuple of arguments to pass in to the method.

        :returns: The return value from the local instance execution.
        :raises: TooManyRetries

        """
        return self._run_all(self._simple_exec, (command, args))

    def pipe_everywhere(self, zipped_commands):
        """Runs the pipe() function of the python redis library on the local
        instance and all remote redis instances. The operations are atomic to
        each instance, but the operation as a whole is non-atomic. The return
        value and/or exception thrown will only come from the local instance,
        but the method will not return until all child operations are finished.

        :param zipped_commands: List of tuples (command, args) to construct a
                                pipeline of commands with.

        :returns: The results of the pipe() on the local instance.
        :raises: TooManyRetries

        """
        return self._run_all(self._pipe_exec, zipped_commands)