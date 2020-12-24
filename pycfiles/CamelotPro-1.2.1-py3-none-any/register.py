# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot/view/register.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\nGlobal registry to register that an Python Object should\nbe scheduled for garbage collection, when a\nQObject is destroyed.\n\nThis is used to combine models and views, where\nthe model should be garbage collected once it has\nno views any more.  But as long as it has views, it\nshould be kept alive.\n'
import logging
from PyQt4 import QtCore
LOGGER = logging.getLogger('camelot.view.register')

class Register(QtCore.QObject):
    """The register that takes care of the dependencies.
    It monitors an object and when the monitored object
    is destroyed, its registered object is scheduled for
    collection.
    """

    def __init__(self):
        super(Register, self).__init__()
        self._key_name = 'monitor_key'
        self._max_monitor_key = 0
        self._registed_by_monitor_key = dict()

    def register(self, registered, monitored):
        """
        :param registered: the object that will be registered
        :param monitored: the object that will be monitored
        """
        if monitored.property(self._key_name).isValid():
            key, _success = monitored.property(self._key_name).toLongLong()
        else:
            self._max_monitor_key += 1
            key = self._max_monitor_key
            monitored.destroyed[QtCore.QObject].connect(self._monitored_object_destroyed)
        LOGGER.debug('monitor object with key %s' % key)
        self._registed_by_monitor_key[key] = registered
        monitored.setProperty(self._key_name, key)

    @QtCore.pyqtSlot(QtCore.QObject)
    def _monitored_object_destroyed(self, qobject):
        """slot to indicate a monitored object is destroyed"""
        key, _success = qobject.property(self._key_name).toLongLong()
        LOGGER.debug('object with key %s is destroyed' % key)
        del self._registed_by_monitor_key[key]


_global_register_ = None

def register(registered, monitored):
    """Global function to register an object and start monitoring
    the dependent object
    
    This function takes care of creating the global register as well.
    """
    global _global_register_
    if _global_register_ == None:
        _global_register_ = Register()
    _global_register_.register(registered, monitored)
    return


def dump_register(logger):
    """Method to see the currently monitored objects, for debugging
    purposes"""
    if _global_register_:
        for k, v in _global_register_._registed_by_monitor_key.items():
            logger.warn('%s : %s' % (k, v))