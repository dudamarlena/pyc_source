# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/deferred.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 13825 bytes
from __future__ import absolute_import, print_function
from future import standard_library
standard_library.install_aliases()
from builtins import map
from builtins import str
from builtins import range
from builtins import object
from collections import namedtuple
from contextlib import contextmanager
import dill, fcntl, logging, os, shutil, tempfile
from toil.lib.misc import mkdir_p
from toil.realtimeLogger import RealtimeLogger
from toil.resource import ModuleDescriptor
logger = logging.getLogger(__name__)

class DeferredFunction(namedtuple('DeferredFunction', 'function args kwargs name module')):
    __doc__ = "\n    >>> df = DeferredFunction.create(defaultdict, None, {'x':1}, y=2)\n    >>> df\n    DeferredFunction(defaultdict, ...)\n    >>> df.invoke() == defaultdict(None, x=1, y=2)\n    True\n    "

    @classmethod
    def create(cls, function, *args, **kwargs):
        """
        Capture the given callable and arguments as an instance of this class.

        :param callable function: The deferred action to take in the form of a function
        :param tuple args: Non-keyword arguments to the function
        :param dict kwargs: Keyword arguments to the function
        """
        return cls(*list(map(dill.dumps, (function, args, kwargs))), name=function.__name__, 
         module=ModuleDescriptor.forModule(function.__module__).globalize())

    def invoke(self):
        """
        Invoke the captured function with the captured arguments.
        """
        logger.debug('Running deferred function %s.', self)
        self.module.makeLoadable()
        function, args, kwargs = list(map(dill.loads, (self.function, self.args, self.kwargs)))
        return function(*args, **kwargs)

    def __str__(self):
        return '%s(%s, ...)' % (self.__class__.__name__, self.name)

    __repr__ = __str__


class DeferredFunctionManager(object):
    __doc__ = '\n    Implements a deferred function system. Each Toil worker will have an\n    instance of this class. When a job is executed, it will happen inside a\n    context manager from this class. If the job registers any "deferred"\n    functions, they will be executed when the context manager is exited.\n\n    If the Python process terminates before properly exiting the context\n    manager and running the deferred functions, and some other worker process\n    enters or exits the per-job context manager of this class at a later time,\n    or when the DeferredFunctionManager is shut down on the worker, the earlier\n    job\'s deferred functions will be picked up and run.\n\n    Note that deferred function cleanup is on a best-effort basis, and deferred\n    functions may end up getting executed multiple times.\n\n    Internally, deferred functions are serialized into files in the given\n    directory, which are locked by the owning process.\n\n    If that process dies, other processes can detect that the files are able to\n    be locked, and will take them over.\n    '
    STATE_DIR_STEM = 'deferred'
    PREFIX = 'func'
    WIP_SUFFIX = '.tmp'

    def __init__(self, stateDirBase):
        """
        Create a new DeferredFunctionManager, sharing state with other
        instances in other processes using the given shared state directory.

        Uses a fixed path under that directory for state files. Creates it if
        not present.

        Note that if the current umask lets other people create files in that
        new directory, we are going to execute their code!

        The created directory will be left behind, because we never know if
        another worker will come along later on this node.
        """
        self.stateDir = os.path.join(stateDirBase, self.STATE_DIR_STEM)
        mkdir_p(self.stateDir)
        self.stateFD, self.stateFileName = tempfile.mkstemp(dir=(self.stateDir), prefix=(self.PREFIX),
          suffix=(self.WIP_SUFFIX))
        try:
            fcntl.lockf(self.stateFD, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            raise RuntimeError('Could not lock deferred function state file %s: %s' % (self.stateFileName, str(e)))

        os.rename(self.stateFileName, self.stateFileName[:-len(self.WIP_SUFFIX)])
        self.stateFileName = self.stateFileName[:-len(self.WIP_SUFFIX)]
        self.stateFileOut = os.fdopen(self.stateFD, 'wb')
        self.stateFileIn = open(self.stateFileName, 'rb')
        logger.debug('Running for file %s' % self.stateFileName)

    def __del__(self):
        """
        Clean up our state on disk. We assume that the deferred functions we
        manage have all been executed, and none are currently recorded.
        """
        logger.debug('Deleting %s' % self.stateFileName)
        os.unlink(self.stateFileName)
        fcntl.lockf(self.stateFD, fcntl.LOCK_UN)

    @contextmanager
    def open(self):
        """
        Yields a single-argument function that allows for deferred functions of
        type :class:`toil.DeferredFunction` to be registered.  We use this
        design so deferred functions can be registered only inside this context
        manager.

        Not thread safe.
        """
        self._runOrphanedDeferredFunctions()
        try:

            def defer(deferredFunction):
                logger.debug('Deferring function %s' % repr(deferredFunction))
                dill.dump(deferredFunction, self.stateFileOut)
                self.stateFileOut.flush()

            logger.debug('Running job')
            yield defer
        finally:
            self._runOwnDeferredFunctions()
            self._runOrphanedDeferredFunctions()

    @classmethod
    def cleanupWorker(cls, stateDirBase):
        """
        Called by the batch system when it shuts down the node, after all
        workers are done, if the batch system supports worker cleanup. Checks
        once more for orphaned deferred functions and runs them.
        """
        logger.debug('Cleaning up deferred functions system')
        cleaner = cls(stateDirBase)
        cleaner._runOrphanedDeferredFunctions()
        del cleaner
        shutil.rmtree(os.path.join(stateDirBase, cls.STATE_DIR_STEM))

    def _runDeferredFunction(self, deferredFunction):
        """
        Run a deferred function (either our own or someone else's).

        Reports an error if it fails.
        """
        try:
            deferredFunction.invoke()
        except Exception as err:
            RealtimeLogger.error('Failed to run deferred function %s: %s', repr(deferredFunction), str(err))
        except:
            RealtimeLogger.error('Failed to run deferred function %s', repr(deferredFunction))

    def _runAllDeferredFunctions(self, fileObj):
        """
        Read and run deferred functions until EOF from the given open file.
        """
        try:
            while True:
                deferredFunction = dill.load(fileObj)
                logger.debug('Loaded deferred function %s' % repr(deferredFunction))
                self._runDeferredFunction(deferredFunction)

        except EOFError as e:
            logger.debug('Out of deferred functions!')

    def _runOwnDeferredFunctions(self):
        """
        Run all of the deferred functions that were registered.
        """
        logger.debug('Running own deferred functions')
        self.stateFileIn.seek(0)
        self._runAllDeferredFunctions(self.stateFileIn)
        self.stateFileIn.seek(0)
        self.stateFileOut.seek(0)
        self.stateFileOut.truncate()

    def _runOrphanedDeferredFunctions(self):
        """
        Scan for files that aren't locked by anybody and run all their deferred functions, then clean them up.
        """
        logger.debug('Running orphaned deferred functions')
        foundFiles = True
        while foundFiles:
            foundFiles = False
            for filename in os.listdir(self.stateDir):
                if filename.endswith(self.WIP_SUFFIX):
                    pass
                else:
                    if not filename.startswith(self.PREFIX):
                        pass
                    else:
                        fullFilename = os.path.join(self.stateDir, filename)
                        if fullFilename == self.stateFileName:
                            pass
                        else:
                            fd = None
                            try:
                                fd = os.open(fullFilename, os.O_RDWR)
                            except OSError:
                                continue

                            try:
                                fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                            except IOError:
                                continue

                            logger.debug('Locked file %s' % fullFilename)
                            foundFiles = True
                            fileObj = os.fdopen(fd, 'rb')
                            self._runAllDeferredFunctions(fileObj)
                            try:
                                os.unlink(fullFilename)
                            except OSError:
                                pass

                            fcntl.lockf(fd, fcntl.LOCK_UN)
                            fileObj.close()