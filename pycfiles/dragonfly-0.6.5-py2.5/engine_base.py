# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\engines\engine_base.py
# Compiled at: 2009-04-08 02:23:57
"""
Engine base class
============================================================================

"""
from ..log import get_log

class EngineBase(object):
    """ Base class for engine-specific back-ends. """
    _log = get_log('engine')
    _name = 'base'

    @classmethod
    def is_available(cls):
        """ Check whether this engine is available. """
        return False

    def __str__(self):
        return '%s()' % self.__class__.__name__

    @property
    def name(self):
        """ The human-readable name of this engine. """
        return self._name

    def load_grammar(self, grammar, *args, **kwargs):
        raise NotImplementedError('Engine %s not implemented.' % self)

    def update_list(self, lst, grammar):
        raise NotImplementedError('Engine %s not implemented.' % self)

    def register_recognition_observer(self, observer):
        self._recognition_observer_manager.register(observer)

    def unregister_recognition_observer(self, observer):
        self._recognition_observer_manager.unregister(observer)

    def enable_recognition_observers(self):
        self._recognition_observer_manager.enable()

    def disable_recognition_observers(self):
        self._recognition_observer_manager.disable()

    def mimic(self, words):
        """ Mimic a recognition of the given *words*. """
        raise NotImplementedError('Engine %s not implemented.' % self)

    def speak(self, text):
        """ Speak the given *text* using text-to-speech. """
        raise NotImplementedError('Engine %s not implemented.' % self)

    def _get_language(self):
        raise NotImplementedError('Engine %s not implemented.' % self)

    language = property(fget=lambda self: self._get_language(), doc='Current user language of the SR engine.')