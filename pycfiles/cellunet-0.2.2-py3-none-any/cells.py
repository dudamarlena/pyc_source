# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cellulose/cells.py
# Compiled at: 2007-06-08 12:55:49
__doc__ = '\ncellulose.cells\nCopyright 2006 by Matthew Marshall <matthew@matthewmarshall.org>\n\nThis module contains the core functionality of cellulose.\n\nThis stuff should be documented pretty well in the docs subdirectory of the\ncellulose distribution.\n\n'
import threading, weakref, warnings
try:
    set
except NameError:
    from sets import Set as set

class CyclicDependencyError(Exception):
    pass


class CellCallStack(object):
    """
    A stack of DependantCell subclasses that are currently discovering
    dependencies.  (eg, ComputedCell cells push themselves onto the stack while
    their value is being calculated, and when other cells are accessed they
    register themselves as a dependency of the cell on top of the stack.)

    Note that to prevent a dependency from being discovered, push None onto the
    stack while they are being accessed.

    Don't instance this class directly (unless you know what you're doing.)
    Instead, call cellulose.get_dependant_stack().
    """

    def __init__(self):
        self._call_stack = []
        self.call_when_empty = set()

    def push(self, cell):
        """
        Pushes a cell onto the stack to discover dependencies.

        In general, you'll want to use DependantCell.push() instead.  (It just
        calls this method with itself, but it looks clearer.)

        If you want to access a cell without it being reported as a dependency
        of whatever is on the stack, you can push None.  Just be sure to pop
        it back off when you're done!  (Use a try/finally.)
        """
        if cell is not None and cell in self._call_stack:
            raise CyclicDependencyError
        self._call_stack.append(cell)
        return

    def pop(self, cell):
        """
        Pops a cell off the stack.

        (Just as with push, you'll probably want to use DependantCell.pop()
        instead.)

        This method requires that you explicitly state what you expect to pop.
        This is to help catch bugs with cells not being popped when they should,
        causing dependencies to be directed to the wrong dependants.
        """
        popped = self._call_stack.pop()
        if popped is not cell:
            warnings.warn('Popped %r, expected %r' % (popped, cell), stacklevel=2)
            if cell in self._call_stack:
                while popped != cell:
                    popped = self._call_stack.pop()

        while len(self._call_stack) == 0 and self.call_when_empty:
            self.call_when_empty.pop()()

        return popped

    def __contains__(self, cell):
        return cell in self._call_stack

    def _get_current(self):
        if self._call_stack:
            return self._call_stack[(-1)]
        else:
            return
        return

    current = property(_get_current)


_dependant_stacks = {}

def get_dependant_stack(thread=None):
    if thread is None:
        thread = threading.currentThread()
    if not _dependant_stacks.has_key(thread):
        _dependant_stacks[thread] = CellCallStack()
    return _dependant_stacks[thread]


class DependencyCell(object):
    """
    This class provides the functionality of a cell that can be used as a
    dependency of others.  It is not meant to be instanced, but subclassed.
    """

    def __init__(self):
        self.dependants = {}

    def register_dependant(self, dependant):
        if dependant is None:
            return
        id_ = id(dependant)
        if id_ not in self.dependants:
            self.dependants[id_] = weakref.ref(dependant, lambda _: self.unregister_dependant(id_))
        dependant.register_dependency(self)
        return

    def depended(self):
        """
        Called whenever data is retrieved from us, and we need to be made a
        dependency of the cell on the stack.
        """
        stack = get_dependant_stack()
        if stack.current is not None:
            self.register_dependant(stack.current)
        return

    def unregister_dependant(self, dependant):
        """
        Called by a dependant when it no longer wants to be notified of changes.

        This function is also called when a dependant is garbage collected, in
        which case only the id is passed.

        This should always be called for unregistering a dependant instead of
        altering self.dependants directly.  That way, subclasses can use this
        as a hook.
        """
        try:
            if isinstance(dependant, (int, long)):
                del self.dependants[dependant]
            else:
                del self.dependants[id(dependant)]
        except KeyError:
            pass

    def changed(self):
        """
        This function should be called when this cell is known to have changed
        and the depenants need to be notified.

        Ideally, ``changed`` should only be called when the cell is known,
        without any doubt, to have changed.  If there is only a possibility of
        change, ``possibly_changed`` should be called instead.
        """
        for wr in self.dependants.values():
            dep = wr()
            if dep is not None:
                dep.dependency_changed(self)

        return

    def possibly_changed(self):
        """
        This function should be called when this cell *might* have changed.
        """
        for wr in self.dependants.values():
            dep = wr()
            if dep is not None:
                dep.dependency_possibly_changed(self)

        return

    def verify_changed(self):
        """
        Called when a dependant is verifying if a possibly changed dependency
        has actually changed.

        Returns None, but calls self.changed() if it has changed.

        This method should be implemented by any cell that calls the
        self.possibly_changed() method.

        It is reasonable for an implementation of this method to 'lie'.  For
        example, if calculating the respective value is very expensive, but
        taking a 99% accurate guess at if it has changed is cheap, giving a
        false negative (or positive) should be acceptable.  This is especially
        true if the dependant cell often changes its dependencies.  (Note: None
        of the cell classes included in cellulose lie in this method.)
        """
        raise NotImplementedError


class DependantCell(object):
    """
    A cell that can discover dependencies, (ie inputs,)  and be alerted of
    changes in those dependencies.

    Note that this class does not have an associated value.  (Opposed to a
    ComputedCell.)  This allows for more flexibility in the system.

    This class is not meant to be instanced, but subclassed.
    """

    def __init__(self):
        self.dependencies = {}
        self._possibly_changed_dependencies = {}
        self._dirty = True
        self._incomming_notification_lock = threading.Lock()

    def register_dependency(self, dependency):
        self.dependencies[id(dependency)] = dependency

    def dependency_changed(self, dependency=None):
        """
        Called by a dependency when it knows for certain that it has changed.

        This method can also be used if, for some reason, the cached value needs
        to be expired manually.

        The single argument, ``dependency``, should be the changed dependency,
        privided that the dependency is a Cell.
        """
        self._incomming_notification_lock.acquire()
        try:
            if dependency is not None and id(dependency) not in self.dependencies:
                dependency.unregister_dependant(self)
                return
            if self._dirty:
                return
            self._possibly_changed_dependencies = {}
            self._dirty = True
        finally:
            self._incomming_notification_lock.release()

        self.possibly_changed()
        return

    def dependency_possibly_changed(self, dependency):
        """
        Called by a dependency to alert us that it might have changed, (but is
        putting off verifying it.)
        """
        self._incomming_notification_lock.acquire()
        try:
            if id(dependency) not in self.dependencies:
                dependency.unregister_dependant(self)
                return
            if self._dirty:
                return
            alert = not self._possibly_changed_dependencies
            self._possibly_changed_dependencies[id(dependency)] = dependency
        finally:
            self._incomming_notification_lock.release()

        if alert:
            self.possibly_changed()

    def _verify_possibly_changed_dependencies(self):
        while self._possibly_changed_dependencies:
            try:
                (id_, d) = self._possibly_changed_dependencies.popitem()
            except KeyError:
                break

            d.verify_changed()

    def push(self):
        """
        Begins dependency discovery for this cell.
        """
        get_dependant_stack().push(self)

    def pop(self):
        """
        Ends dependency discover for this cell.

        Note that this should be called once for every call to push().  Be sure
        to wrap anything that happens in-between in a try/finally block.
        """
        get_dependant_stack().pop(self)

    def _get_dirty(self):
        self._verify_possibly_changed_dependencies()
        return self._dirty

    dirty = property(_get_dirty, doc='\n    Authoritatively determines if this cell is dirty or not.  (This may involve\n    calculating any possibly changed dependencies.)\n    ')

    def _get_possibly_dirty(self):
        return bool(self._dirty or self._possibly_changed_dependencies)

    possibly_dirty = property(_get_possibly_dirty, doc='\n    This is like ``dirty`` except for that no calculations will be performed.\n    A false positive may be given, but never a false negative.\n    ')


class InputCell(DependencyCell):
    """
    InputCell

    A cell that has its value explicitly assigned.
    """

    def __init__(self, value=None):
        DependencyCell.__init__(self)
        self._value = None
        self._dirty = False
        self._lock = threading.Lock()
        return

    def get(self):
        """
        Returns the value that was set.

        In general, I recommend using the 'value' property instead.  To me,
        using 'get' makes me feel like I should be using a dictionary, while
        'value' reminds me that it's a cell.  (Python isn't Java, after all.)
        """
        self.depended()
        return self._value

    def set(self, value):
        """
        Sets the value for this cell.

        As mentioned in the docstring for ``get``, it is recommended to use
        the property ``value`` instead of ``set`` directly.
        """
        self._lock.acquire()
        try:
            old = self._value
            self._value = value
            if value != old:
                self.changed()
        finally:
            self._lock.release()

    value = property(get, set)

    def verify_changed(self):
        get_dependant_stack().push(None)
        try:
            self.get()
        finally:
            get_dependant_stack().pop(None)

        return


class ComputedCell(DependencyCell, DependantCell):
    """
    ComputedCell

    A cell that gets it's value by calling a function.

    While it is not (currently) enforced, it is highly recommended that the
    function used to calculate the value does not have any side-effects.  There
    is no guarantee when the function will be called, if it is called at all.

    If you need to do something in response to a ComputedCell changing, do it
    in a separate cell.  (such as the ones provided in cellulose.observers.)
    """

    def __init__(self, function=None):
        DependencyCell.__init__(self)
        DependantCell.__init__(self)
        self._value = None
        self._function = function
        self._get_lock = threading.Lock()
        return

    def get(self):
        if not self._get_lock.acquire(False):
            if self in get_dependant_stack():
                raise CyclicDependencyError
            else:
                self._get_lock.acquire()
        self._incomming_notification_lock.acquire()
        held = True
        try:
            old_value = self._value
            while self.possibly_dirty:
                self._incomming_notification_lock.release()
                held = False
                if self.dirty:
                    self.dependencies.clear()
                    self._dirty = False
                    self._possibly_changed_dependencies = {}
                    self.push()
                    try:
                        self._value = self.run_function()
                    finally:
                        self.pop()

                self._incomming_notification_lock.acquire()
                held = True

            if old_value != self._value:
                self.changed()
            self.depended()
        finally:
            if held:
                self._incomming_notification_lock.release()
            self._get_lock.release()

        return self._value

    value = property(get)

    def verify_changed(self):
        get_dependant_stack().push(None)
        try:
            self.get()
        finally:
            get_dependant_stack().pop(None)

        return

    def set_function(self, new):
        old = self._function
        self._function = new
        if new is not old:
            self.dependency_changed()

    function = property(lambda self: self._function, set_function)

    def run_function(self):
        """
        This is mainly a hook for subclasses that want to wrap the calling of
        the function.
        """
        return self.function()