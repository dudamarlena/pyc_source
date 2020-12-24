# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/server/pyxrd_server.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 2793 bytes
import sys, os, logging
logger = logging.getLogger(__name__)
import multiprocessing

def _worker_initializer(pool_stop, debug, *args):
    if debug:
        if '-d' not in sys.argv:
            sys.argv.insert(1, '-d')
    else:
        if not debug:
            if '-d' in sys.argv:
                sys.argv.remove('-d')
        from pyxrd.data import settings
        settings.initialize()
        if settings.DEBUG:
            from pyxrd import stacktracer
            stacktracer.trace_start(('trace-worker-%s.html' % multiprocessing.current_process().name),
              interval=5,
              auto=True)
    logger.info('Worker process initialized, DEBUG=%s' % debug)


class PyXRDServer(object):
    pool = None
    pool_stop = None
    running = True

    def loopCondition(self):
        return self.running

    def __init__(self):
        from pyxrd.data import settings
        settings.initialize()
        logger.warning('Creating pool, DEBUG=%s' % settings.DEBUG)
        self.pool_stop = multiprocessing.Event()
        self.pool_stop.clear()
        maxtasksperchild = 10 if 'nt' == os.name else None
        self.pool = multiprocessing.Pool(initializer=_worker_initializer,
          maxtasksperchild=maxtasksperchild,
          initargs=(
         self.pool_stop,
         settings.DEBUG))
        settings.FINALIZERS.append(self.shutdown)

    def submit(self, func):
        """
            The callback 'func' will be submitted to a multiprocessing
            pool created by the server. The result object will be returned.
        """
        result = self.pool.apply_async(func)
        self._pyroDaemon.register(result)
        return result

    def submit_sync(self, func):
        """
            This will run the 'func' callback directly on the server process.
            Use this with care as it will block the server. 
            Can be used to pass in a full project refinement using the 
            pyxrd.calculations.run_refinement method.
        """
        result = func()
        self._pyroDaemon.register(result)
        return result

    def shutdown(self):
        """
            Shuts down the server.
        """
        logging.info('Closing multiprocessing pool ...')
        if self.pool is not None:
            self.pool_stop.set()
            self.pool.close()
            self.pool.join()
        self.running = False