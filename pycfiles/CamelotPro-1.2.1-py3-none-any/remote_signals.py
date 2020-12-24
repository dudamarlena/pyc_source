# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/remote_signals.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nClasses to connect the QT event loop with a messaging\nserver.  To enable multiple clients to push model updates\nto each other or messages for the users.\n\nAs a messaging server, Apache active MQ was tested in combination\nwith the stomp library (http://docs.codehaus.org/display/STOMP/Python)\n'
import logging, re
LOGGER = logging.getLogger('remote_signals')
from PyQt4 import QtCore

class SignalHandler(QtCore.QObject):
    """The signal handler connects multiple collection proxy classes to
    inform each other when they have changed an object.
    
    If the object is persistent (eg mapped by SQLAlchemy), the signal hanler
    can inform other signal handlers on the network of the change.
    
    A couple of the methods of this thread are protected by a QMutex through
    the synchronized decorator.  It appears that python/qt deadlocks when the
    entity_update_signal is connected to and emitted at the same time.  This
    can happen when the user closes a window that is still building up (the
    CollectionProxies are being constructed and they connect to the signal
    handler).
    
    These deadlock issues are resolved in recent PyQt, so comment out the 
    mutex stuff. (2011-08-12)
     """
    entity_update_signal = QtCore.pyqtSignal(object, object)
    entity_delete_signal = QtCore.pyqtSignal(object, object)
    entity_create_signal = QtCore.pyqtSignal(object, object)
    entity_update_pattern = '^/topic/Camelot.Entity.(?P<entity>.*).update$'

    def __init__(self):
        super(SignalHandler, self).__init__()
        self.update_expression = re.compile(self.entity_update_pattern)

    def connect_signals(self, obj):
        """Connect the SignalHandlers its signals to the slots of obj, while
        the mutex is locked"""
        self.entity_update_signal.connect(obj.handle_entity_update, QtCore.Qt.QueuedConnection)
        self.entity_delete_signal.connect(obj.handle_entity_delete, QtCore.Qt.QueuedConnection)
        self.entity_create_signal.connect(obj.handle_entity_create, QtCore.Qt.QueuedConnection)

    def send_entity_update(self, sender, entity, scope='local'):
        """Call this method to inform the whole application an entity has 
        changed"""
        self.sendEntityUpdate(sender, entity, scope)

    def sendEntityUpdate(self, sender, entity, scope='local'):
        """Call this method to inform the whole application an entity has 
        changed"""
        self.entity_update_signal.emit(sender, entity)

    def sendEntityDelete(self, sender, entity, scope='local'):
        """Call this method to inform the whole application an entity is 
        about to be deleted"""
        self.entity_delete_signal.emit(sender, entity)

    def sendEntityCreate(self, sender, entity, scope='local'):
        """Call this method to inform the whole application an entity 
        was created"""
        self.entity_create_signal.emit(sender, entity)


_signal_handler_ = []

def construct_signal_handler(*args, **kwargs):
    """Construct the singleton signal handler"""
    _signal_handler_.append(SignalHandler(*args, **kwargs))


def get_signal_handler():
    """Get the singleton signal handler"""
    if not len(_signal_handler_):
        construct_signal_handler()
    return _signal_handler_[(-1)]


def has_signal_handler():
    """Request if the singleton signal handler was constructed"""
    return len(_signal_handler_)