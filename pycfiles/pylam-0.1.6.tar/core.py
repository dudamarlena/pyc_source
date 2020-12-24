# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/PyLAF/core.py
# Compiled at: 2011-04-22 21:09:56
import utils.core, weakref, inspect, threading

def kw(**kwargs):
    return kwargs


def args(*args, **kwargs):
    return (args, kwargs)


def cb2str(callback):
    return '(%s.%s)' % (callback.weakref_obj(), callback.method_name)


def cwl(wrappers):
    string = '['
    for wrapper in wrappers:
        string = string + ' %s' % cb2str(wrapper)

    string = string + ' ]'
    return string


def isPort(obj):
    return utils.isfamily(obj, Port)


def get_child(ins, id):
    id = id.split('.')
    obj = ins
    for name in id:
        obj = obj.children[name]

    return obj


def get_port(ins, id):
    idl = id.split('.')
    id, name = idl[0], idl[(-1)]
    for o in idl[1:-1]:
        id = id + '.' + o

    return getattr(get_child(ins, id), name)


(EVENT_SET, EVENT_GET) = range(2)
HISTORY_CALLBACK = []

class CallWrapper:

    def __init__(self, method):
        self.weakref_obj = None
        self.method_name = None
        self.function = None
        try:
            method.__self__
        except AttributeError:
            self.function = method
        else:
            obj, name = method.__self__, method.__name__
            self.weakref_obj = weakref.ref(obj)
            self.method_name = name

        return

    def ismethod(self):
        return not self.weakref_obj == None and self.function == None

    def isfunction(self):
        return self.weakref_obj == None and not self.function == None

    def isalive(self):
        if self.ismethod():
            try:
                o = self.weakref_obj()
            except TypeError:
                return False
            else:
                try:
                    getattr(o, self.method_name)
                except AttributeError:
                    return False

        else:
            if self.isfunction():
                return True
            else:
                return False
        return True

    def __call__(self, *args, **kwargs):
        if self.isalive():
            if self.ismethod():
                o, name = self.weakref_obj(), self.method_name
                return getattr(o, name).__call__(*args, **kwargs)
            if self.isfunction():
                return self.function(*args, **kwargs)

    def __eq__(self, other):
        try:
            o, q = self.weakref_obj(), other.weakref_obj()
        except TypeError:
            return False

        return o == q and self.method_name == other.method_name and self.function == other.function


class Scheduler:
    __metaclass__ = utils.core.Singleton

    def __init__(self):
        self.threads = weakref.WeakKeyDictionary()
        self.trace = False

    def add(self, thread):
        self.threads[thread] = Schedule()

    def get(self, thread):
        return self.threads[thread]


class Schedule:

    def __init__(self):
        self.queue = None
        self.ignore = []
        self.fixed = []
        return

    def flush(self):
        callbacks = []
        for callback in self.queue:
            if not callbacks.count(callback):
                callbacks.append(callback)

        self.queue = []
        for callback in callbacks:
            if not self.ignore.count(callback):
                if Scheduler().trace:
                    print 'Call:(%s.%s)' % (callback.weakref_obj(), callback.method_name)
                self.ignore.append(callback)
                callback.__call__()

        if not len(self.queue) == 0:
            self.flush()


class Root:
    __metaclass__ = utils.core.Singleton

    def __init__(self):
        self.children = {}
        self.queue = None
        self.ignore = []
        self.fixed = []
        self.depth = 0
        self.trace = False
        return

    def destroy(self):
        for c in self.children.values():
            c.destroy()

    def flush(self):
        callbacks = []
        for callback in self.queue:
            if not callbacks.count(callback):
                callbacks.append(callback)

        self.queue = []
        for callback in callbacks:
            if not self.ignore.count(callback):
                if self.trace:
                    print 'Call:(%s.%s)' % (callback.weakref_obj(), callback.method_name)
                self.ignore.append(callback)
                callback.__call__()

        if not len(self.queue) == 0:
            self.depth += 1
            self.flush()
            self.depth -= 1


class Port(utils.core.Observer):

    def update(self, event, *args):
        if event == EVENT_GET:
            return
        callbacks = list(self._callbacks)
        for callback in callbacks:
            if not callback.isalive():
                self._callbacks.remove(callback)
                continue
            callback.__call__()

    def __init__(self, *args, **kw):
        if utils.isfamily(args[0], Port):
            s = Storage(args[0].storage.value)
            utils.core.Observer.__init__(self, s)
        else:
            s = Storage(*args, **kw)
            utils.core.Observer.__init__(self, s)
        self._callbacks = []
        self._iscaller = False

    def bind(self, method):
        self._callbacks.append(CallWrapper(method))
        return self

    def unbind(self, method):
        self._callbacks.remove(CallWrapper(method))

    def unbind_all(self):
        callbacks = list(self._callbacks)
        for callback in callbacks:
            self._callbacks.remove(callback)

    def passive(self):
        self._deposit = self._callbacks
        self._callbacks = []

    def disable(self, target=None):
        callbacks = self._callbacks
        self._deposit = self._callbacks
        self._callbacks = []
        for callback in callbacks:
            if not callback.weakref_obj() == target and not target == None:
                self._callbacks.append(callback)

        return

    def active(self):
        try:
            self._deposit
        except AttributeError:
            return
        else:
            for callback in self._callbacks:
                self._deposit.append(callback)

        self._callbacks = self._deposit
        del self._deposit

    enable = active

    def isoutput(self, klass):
        family = inspect.getmro(klass)
        for c in family:
            name = repr(c).split()[1]
            if name == 'PyLAF.core.Output' or name == 'core.Output':
                return True

        return False

    def link(self, *ports, **kw):
        for port in ports:
            port.subject.observers.cleanup()

        outputs = []
        for obj in self.subject.observers.tolist():
            if self.isoutput(obj.__class__):
                outputs.append(obj)

        for port in ports:
            for obj in port.subject.observers.tolist():
                if self.isoutput(obj.__class__):
                    outputs.append(obj)

        if len(outputs) > 1:
            raise ValueError('too many Output was linked')

        def _kw(set=False):
            return set

        set = _kw(**kw)
        for port in ports:
            if set:
                port.set(self.subject.value)
            for obj in port.subject.observers.tolist():
                obj.register(self.subject)

        return self

    def revlink(self, port, **kw):
        port.link(self, **kw)

    def unlink(self):
        self.unregister()
        self.register(Storage(None))
        return

    def set(self, *args, **kw):
        try:
            self._set_called
        except AttributeError:
            self._set_called = None
            self.subject.set(*args, **kw)
            del self._set_called

        return

    def set_now(self, *args, **kwargs):
        self._setnow_called = None
        schedule = Scheduler().get(threading.currentThread())
        escape = (schedule.queue, schedule.ignore, schedule.fixed)
        schedule.queue = None
        schedule.ignore = list(schedule.ignore)
        schedule.fixed = list(schedule.fixed)
        if schedule.fixed.count(self.subject):
            schedule.fixed.remove(self.subject)
        self.set(*args, **kwargs)
        (schedule.queue, schedule.ignore, schedule.fixed) = escape
        del self._setnow_called
        return

    def get(self):
        return self.subject.get()


class Parm(Port):

    def update(self, event, *args):
        if event == EVENT_GET:
            return
        callbacks = list(self._callbacks)
        for callback in callbacks:
            if not callback.isalive():
                self._callbacks.remove(callback)
                continue
            try:
                self._setnow_called
            except AttributeError:
                schedule = Scheduler().get(threading.currentThread())
                if not schedule.queue.count(callback):
                    schedule.queue.append(callback)
            else:
                callback.__call__()


class Output(Port):

    def update(self, event, *args):
        if event == EVENT_SET:
            return
        schedule = Scheduler().get(threading.currentThread())
        if schedule.fixed.count(self.subject):
            return
        callbacks = list(self._callbacks)
        for callback in callbacks:
            if not callback.isalive():
                self._callbacks.remove(callback)
                continue
            if not schedule.ignore.count(callback):
                if Scheduler().trace:
                    self.print_callback(callback)
                schedule.ignore.append(callback)
                callback.__call__()

        if Scheduler().trace:
            self.print_queue()

    def print_callback(self, callback):
        print 'Get:(%s.%s)' % (callback.weakref_obj(), callback.method_name),

    def print_queue(self):
        schedule = Scheduler().get(threading.currentThread())
        if schedule.queue == None:
            return
        else:
            callbacks = []
            for callback in schedule.queue:
                if not callbacks.count(callback):
                    callbacks.append(callback)

            for callback in schedule.ignore:
                if callbacks.count(callback):
                    callbacks.remove(callback)

            print 'Queue:', cwl(callbacks),
            return


class Storage(utils.core.Subject):
    u"""
    複数のPortクラスで同期する任意のリテラルを格納する実体クラス
    メンバ変数による参照禁止
    """

    def __init__(self, *args, **kw):
        utils.core.Subject.__init__(self)
        self._set(*args, **kw)

    def _set(self, *args, **kw):
        if args and kw:
            args = tuple([ utils.core.itemcopy(item) for item in args ])
            temp = {}
            for key in kw:
                temp[key] = utils.core.itemcopy(kw[key])

            kw = temp
            self.value = (args, kw)
        elif args:
            if len(args) == 1:
                self.value = utils.core.itemcopy(args[0])
            else:
                self.value = tuple([ utils.core.itemcopy(item) for item in args ])
        elif kw:
            temp = {}
            for key in kw:
                temp[key] = utils.core.itemcopy(kw[key])

            self.value = temp

    def set(self, *args, **kw):
        thread = threading.currentThread()
        if not Scheduler().threads.has_key(thread):
            Scheduler().add(thread)
        schedule = Scheduler().get(thread)
        if not schedule.fixed.count(self):
            schedule.fixed.append(self)
            self._set(*args, **kw)
        if schedule.queue == None:
            schedule.queue = []
            self.notify(EVENT_SET)
            schedule.flush()
            schedule.queue = None
            schedule.ignore = []
            schedule.fixed = []
        else:
            self.notify(EVENT_SET)
        return

    def get(self):
        u"""格納しているオブジェクトまたはリテラルを返す"""
        self.notify(EVENT_GET)
        return self.value


class Component:
    u"""
    PyLAF.Rootを基盤とするPyLAFコンポーネント
    メンバ変数による参照禁止
    """

    def __init__(self, master=None, name=None):
        self.children = {}
        if master == None:
            self.master = Root()
        else:
            self.master = master
        if name == None:
            self._name = repr(id(self))
        else:
            self._name = name
        self._assign_to_master()
        return

    def _assign_to_master(self):
        if self.master.children.has_key(self._name):
            self.master.children[self._name].destroy()
        self.master.children[self._name] = self

    def _remove_from_master(self):
        if self.master.children.has_key(self._name):
            del self.master.children[self._name]

    def destroy(self):
        """ Destroy this and all descendants nodes."""
        for c in self.children.values():
            c.destroy()

        self._remove_from_master()

    def set(self, **kwargs):
        for key in kwargs:
            getattr(self, key).set(kwargs[key])

    def component(self, path=None):
        if path == None:
            return self
        else:
            ids = path.split('.')
            child = self
            for id in ids:
                if child.children.has_key(id):
                    child = child.children[id]
                else:
                    return

            return child

    def port(self, path=None):
        if path == None:
            return self
        else:
            name = path.split('.')[(-1)]
            path = path[:-(len(name) + 1)]
            if len(path) == 0:
                component = self
            else:
                component = self.component(path)
            if component == None:
                return
            try:
                return getattr(component, name)
            except AttributeError:
                return

            return

    child = component


if __name__ == '__main__':

    class Child(Component):
        pass


    class MyComponent(Component):

        def __init__(self, master):
            Component.__init__(self, master)
            self.port = Port(0).bind(self.callback)
            c = Child(self, name='child')
            print c

        def callback(self):
            print self.port.get(), self.children['child']


    c = MyComponent(Root())
    print c.port.get()
    c.port.set('aa', xaxis='aa')
    c.port.set(xaxis='aa')
    c.port.set('1 aa')
    c.port.unbind(c.callback)
    c.port.set('aa', xaxis='aa')
    c = weakref.ref(c)
    print c
    c().destroy()
    print c