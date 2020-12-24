# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gerardo/Projects/nlp_model_gen/nlp_model_gen/utils/classUtills.py
# Compiled at: 2019-06-14 18:07:58
# Size of source mod 2**32: 1802 bytes
from abc import ABC

class Singleton(type):
    __doc__ = '\n    Implementación de Singleton\n    '

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = (super().__call__)(*args, **kwargs)
        return cls._instance


class Observable:
    __doc__ = '\n    Implementación de observable\n    '

    def __init__(self):
        self._Observable__observers = list([])

    def add_observer(self, observer):
        """
        Agrega un observador
        """
        self._Observable__observers.append(observer)

    def notify(self, data):
        """
        Notifica a los observadores un evento.

        :data: [Any] - Datos a notificar al observer
        """
        for observer in self._Observable__observers:
            observer.update(data)


class Observer(ABC):
    __doc__ = '\n    Implementación de observer (clase abstracta)\n    '

    def __init__(self):
        pass

    def update(self, data):
        pass


class ObservableSingleton(metaclass=Singleton):
    __doc__ = '\n    Implementación de observable combinado con singleton\n    '

    def __init__(self):
        self._ObservableSingleton__observers = list([])

    def add_observer(self, observer):
        """
        Agrega un observador
        """
        self._ObservableSingleton__observers.append(observer)

    def notify(self, data):
        """
        Notifica a los observadores un evento.

        :data: [Any] - Datos a notificar al observer
        """
        for observer in self._ObservableSingleton__observers:
            observer.update(data)


class ObserverSingleton(metaclass=Singleton):
    __doc__ = '\n    Implementación de observer combinado con singleton\n    '

    def __init__(self):
        pass

    def update(self, data):
        pass