# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/util/mockedglobals.py
# Compiled at: 2015-11-06 23:45:35
import logging, mock
from salve.log import gen_handler
from salve.context import ExecutionContext
from .mockedio import MockedIO
from .context import clear_exec_context

class MockedGlobals(MockedIO):

    def __init__(self):
        MockedIO.__init__(self)
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        self.logger_patch = mock.patch('salve.logger', self.logger)
        self.action_logger_patches = [ mock.patch('salve.action.%s.logger' % loc, self.logger) for loc in [
         'backup.file', 'backup.directory',
         'copy.file', 'create.file',
         'copy.directory', 'create.directory',
         'modify.chmod', 'modify.chown',
         'modify.file_chmod', 'modify.file_chown',
         'modify.dir_chmod', 'modify.dir_chown']
                                     ]

    def setUp(self):
        self.logger.setLevel(logging.DEBUG)
        ExecutionContext().transition(ExecutionContext.phases.STARTUP, quiet=True)
        MockedIO.setUp(self)
        clear_exec_context()
        self.logger_patch.start()
        self.logger.addHandler(gen_handler(stream=self.stderr))
        for p in self.action_logger_patches:
            p.start()

    def tearDown(self):
        MockedIO.tearDown(self)
        self.logger_patch.stop()
        self.logger.handlers = []
        for p in self.action_logger_patches:
            p.stop()