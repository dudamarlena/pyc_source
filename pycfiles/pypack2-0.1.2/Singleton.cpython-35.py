# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/step/Workspace/pypack/singleton/pypack/singleton/Singleton.py
# Compiled at: 2018-01-13 12:06:57
# Size of source mod 2**32: 2429 bytes
__INSTANCES__ = {}

class Singleton:
    _Singleton__instances = {}

    def __init__(self, cls):
        if not isinstance(cls, type):
            raise TypeError('Only class can be decorated as Singleton')
        self._cls = cls

    def __call__(self, *arg, **kwarg):
        if self._cls not in self._Singleton__instances:
            self._Singleton__instances[self._cls] = self._cls(*arg, **kwarg)
        elif '__call__' in dir(self._Singleton__instances[self._cls]):
            self._Singleton__instances[self._cls](*arg, **kwarg)
        return self._Singleton__instances[self._cls]

    def get_instance(self):
        if isinstance(self, Singleton) and self._cls in list(self._Singleton__instances.keys()):
            return self._Singleton__instances[self._cls]

    @classmethod
    def clear(cls):
        __INSTANCES__ = {}
        Singleton._Singleton__instances = {}

    @classmethod
    def remove(cls, r):
        if r in cls.classes():
            del cls._Singleton__instances[r]

    @classmethod
    def pairs(cls):
        return cls.SingletonPairsIterator(cls._Singleton__instances)

    @classmethod
    def classes(cls):
        return cls.SingletonClassesIterator(list(cls._Singleton__instances.keys()))

    @classmethod
    def instances(cls):
        return cls.SingletonInstancesIterator(list(cls._Singleton__instances.values()))

    @classmethod
    def get(cls, g):
        if isinstance(g, Singleton) and g._cls in list(Singleton._Singleton__instances.keys()):
            return Singleton._Singleton__instances[g._cls]

    @classmethod
    def dump(cls):
        print('dump singleton')
        for e in cls.classes():
            print(e)

        print('--------------')

    class SingletonIterator:

        def __init__(self, l):
            self.l = l

        def __len__(self):
            return len(self.l)

        def __iter__(self):
            self.index = -1
            return self

        def __next__(self):
            self.index += 1
            if self.index >= len(self.l):
                raise StopIteration
            return self.l[self.index]

    class SingletonClassesIterator(SingletonIterator):

        def __contains__(self, e):
            if not isinstance(e, Singleton):
                return False
            for i in self:
                if i == e._cls:
                    return True

            return False

    class SingletonInstancesIterator(SingletonIterator):
        pass

    class SingletonPairsIterator(SingletonIterator):
        pass