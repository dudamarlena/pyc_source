# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cellulose/observers.py
# Compiled at: 2007-06-07 19:22:59
__doc__ = "\ncellulose.observers\n\nThis is a simple method for observing changes happening inside a cellulose\nsystem from the outside.\n\nThis is basically how it works:\n    When an Observer is notified that one of its dependencies has changed, it\n    adds itself to an ObserverBank.\n\n    When the application is ready to handle changes, it calls the ObserverBank's\n    'flush' method, which causes all contained observers to verify changes.\n\nIf that doesn't make sense, read the code.  It might be clearer :)\n"
from cellulose.cells import DependantCell, get_dependant_stack
try:
    set
except NameError:
    from sets import Set as set

class ObserverBank(set):
    """
    Holds any observers that have possibly changed.
    """

    def flush(self, force=False):
        """
        Tell all held observers to check for changes now.

        Note that this is a possible location for an infinite loop.  If an
        observer changes one of its dependencies, it will again be added to the
        bank.
        """
        while len(self):
            if not force and get_dependant_stack()._call_stack:
                get_dependant_stack().call_when_empty.add(lambda : self.flush())
                return
            self.pop().check()


default_observer_bank = ObserverBank()

class Observer(DependantCell):
    """
    This class is rather limited in itself.  You might want to subclass it, or
    even replace it outright.
    """
    observer_bank = default_observer_bank

    def __init__(self, check_function, observer_bank=None):
        DependantCell.__init__(self)
        self.check_function = check_function
        if observer_bank is not None:
            self.observer_bank = observer_bank
        return

    def check(self):
        self._verify_possibly_changed_dependencies()
        if not self._dirty:
            return
        self.dependencies.clear()
        self.push()
        try:
            self.check_function()
        finally:
            self.pop()

        self._dirty = False

    def possibly_changed(self):
        self.observer_bank.add(self)


class SingleCellObserver(Observer):

    def __init__(self, observed_cell, observer_bank=None):
        Observer.__init__(self, lambda : None, observer_bank=observer_bank)
        observed_cell.register_dependant(self)
        self.change_callbacks = set()

    def check(self):
        self._verify_possibly_changed_dependencies()
        if not self._dirty:
            return
        for d in self.dependencies.values():
            d.unregister_dependant(self)

        self.dependencies = {}
        for callback in self.change_callbacks:
            callback()

        self._dirty = False