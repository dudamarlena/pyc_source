# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/model_thread/no_thread_model_thread.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nCreated on Sep 12, 2009\n\n@author: tw55413\n'
import logging
logger = logging.getLogger('camelot.view.model_thread.no_thread_model_thread')
from PyQt4 import QtCore
from signal_slot_model_thread import AbstractModelThread, setup_model
from camelot.view.controls.exception import register_exception

class NoThreadModelThread(AbstractModelThread):

    def __init__(self, setup_thread=setup_model):
        super(NoThreadModelThread, self).__init__(setup_thread=setup_model)
        self.responses = []
        self.start()

    def start(self):
        try:
            self._setup_thread()
        except Exception as e:
            exc_info = register_exception(logger, 'Exception when setting up the NoThreadModelThread', e)
            self.setup_exception_signal.emit(exc_info)

    def post(self, request, response=None, exception=None, args=()):
        try:
            result = request(*args)
            response(result)
        except Exception as e:
            if exception:
                exception_info = register_exception(logger, 'Exception caught in model thread while executing %s' % request.__name__, e)
                exception(exception_info)

    def wait_on_work(self):
        app = QtCore.QCoreApplication.instance()
        i = 0
        while app.hasPendingEvents() and i < 10:
            app.processEvents()
            i += 1

    def isRunning(self):
        return True