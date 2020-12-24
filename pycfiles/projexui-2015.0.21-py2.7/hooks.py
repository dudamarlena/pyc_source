# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/projex/hooks.py
# Compiled at: 2016-07-03 23:28:12
__doc__ = "\nThe hooks module will provide an API to assigning multiple hooks to\nPython's internal exception and logging calls.  This will utilize the\nsys.excepthook method, and override the sys.stdout instance with a\nprinter wrapper while providing a queue based call to processing events.\n\nSimilar to the logging handling system, except works with the unknown\nexceptions and printed values as well.\n\n:usage      |>>> from projex import hooks\n            |>>> def email_error(cls, error, trace):\n            |...    error = hooks.formatExcept(cls, error, trace)\n            |...    notify.sendEmail('me@domain.com',\n            |...                     ['error@domain.com'],\n            |...                     'Error Occurred',\n            |...                     error)\n            |>>> from xqt import QtGui\n            |>>> def message_error(cls, error, trace):\n            |...    QtGui.QMessageBox.critical(None, 'Error', error)\n            |>>> # register exceptions\n            |>>> hooks.messageExcept(message_error)\n            |>>> hooks.registerExcept(email_error)\n"
import weakref, sys, traceback
_displayhooks = None
_excepthooks = None

class StreamHooks(object):
    """
    Basic class to wrap the sys stream system.
    """

    def __getattr__(self, key):
        try:
            return getattr(self.stream, key)
        except AttributeError:
            return getattr(sys.__stdout__, key)

    def __init__(self, stream):
        self.hooks = []
        self.stream = stream

    def write(self, text):
        new_hooks = []
        for hook_ref in self.hooks:
            hook = hook_ref()
            if hook:
                hook(text)
                new_hooks.append(hook_ref)

        self.hooks = new_hooks
        try:
            self.stream.write(text)
        except StandardError:
            pass


def displayhook(value):
    """
    Runs all of the registered display hook methods with the given value.
    Look at the sys.displayhook documentation for more information.
    
    :param      value | <variant>
    """
    global _displayhooks
    new_hooks = []
    for hook_ref in _displayhooks:
        hook = hook_ref()
        if hook:
            hook(value)
            new_hooks.append(hook_ref)

    _displayhooks = new_hooks
    sys.__displayhook__(value)


def excepthook(cls, error, trace):
    """
    Runs all of the registered exception hook methods with the given value.
    Look at the sys.excepthook documentation for more information.
    
    :param      cls     | <type>
                error   | <str>
                trace   | <traceback>
    """
    global _excepthooks
    new_hooks = []
    for hook_ref in _excepthooks:
        hook = hook_ref()
        if hook:
            hook(cls, error, trace)
            new_hooks.append(hook_ref)

    _excepthook = new_hooks
    sys.__excepthook__(cls, error, trace)


def formatExcept(cls, error, trace):
    """
    Formats the inputted class, error, and traceback information to the standard
    output commonly found in Python interpreters.
    
    :param      cls     | <type>
                error   | <str>
                trace   | <traceback>
    
    :return     <str>
    """
    clsname = cls.__name__ if cls else 'UnknownError'
    tb = 'Traceback (most recent call last):\n'
    tb += ('').join(traceback.format_tb(trace))
    tb += ('{0}: {1}').format(clsname, error)
    return tb


def registerDisplay(func):
    """
    Registers a function to the display hook queue to be called on hook.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    setup()
    ref = weakref.ref(func)
    if ref not in _displayhooks:
        _displayhooks.append(ref)


def registerExcept(func):
    """
    Registers a function to the except hook queue to be called on hook.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    setup()
    ref = weakref.ref(func)
    if ref not in _excepthooks:
        _excepthooks.append(ref)


def registerStdErr(func):
    """
    Registers a function to the print hook queue to be called on hook.
    This method will also override the current sys.stdout variable with a new
    <StreamHooks> instance.  This will preserve any current sys.stdout 
    overrides while providing a hookable class for linking multiple methods to.
    
    :param      func | <callable>
    """
    if not isinstance(sys.stderr, StreamHooks):
        sys.stderr = StreamHooks(sys.stderr)
    ref = weakref.ref(func)
    if ref not in sys.stderr.hooks:
        sys.stderr.hooks.append(ref)


def registerStdOut(func):
    """
    Registers a function to the print hook queue to be called on hook.
    This method will also override the current sys.stdout variable with a new
    <StreamHooks> instance.  This will preserve any current sys.stdout 
    overrides while providing a hookable class for linking multiple methods to.
    
    :param      func | <callable>
    """
    if not isinstance(sys.stdout, StreamHooks):
        sys.stdout = StreamHooks(sys.stdout)
    ref = weakref.ref(func)
    if ref not in sys.stdout.hooks:
        sys.stdout.hooks.append(ref)


def setup():
    """
    Initializes the hook queues for the sys module.  This method will
    automatically be called on the first registration for a hook to the system
    by either the registerDisplay or registerExcept functions.
    """
    global _displayhooks
    global _excepthooks
    if _displayhooks is not None:
        return
    else:
        _displayhooks = []
        _excepthooks = []
        if sys.displayhook != sys.__displayhook__:
            _displayhooks.append(weakref.ref(sys.displayhook))
        if sys.excepthook != sys.__excepthook__:
            _excepthooks.append(weakref.ref(sys.excepthook))
        sys.displayhook = displayhook
        sys.excepthook = excepthook
        return


def unregisterDisplay(func):
    """
    Un-registers a function from the display hook queue.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    try:
        _displayhooks.remove(weakref.ref(func))
    except ValueError:
        pass


def unregisterExcept(func):
    """
    Un-registers a function from the except hook queue.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    try:
        _excepthooks.remove(weakref.ref(func))
    except (AttributeError, ValueError):
        pass


def unregisterStdErr(func):
    """
    Un-registers a function from the print hook queue.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    try:
        sys.stderr.hooks.remove(weakref.ref(func))
    except (AttributeError, ValueError):
        pass


def unregisterStdOut(func):
    """
    Un-registers a function from the print hook queue.
    Look at the sys.displayhook documentation for more information.
    
    :param      func | <callable>
    """
    try:
        sys.stdout.hooks.remove(weakref.ref(func))
    except (AttributeError, ValueError):
        pass