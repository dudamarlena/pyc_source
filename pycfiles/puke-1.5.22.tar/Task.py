# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: puke/Task.py
# Compiled at: 2011-12-05 13:53:13
import types, logging
from puke.Error import *
from puke.Console import *
from pydoc import help
from inspect import getcallargs
__tasks__ = {}

def addTask(task):
    console.debug('Registering task: %s' % task.name)
    __tasks__[task.name] = task


def hasDefault():
    if 'default' not in __tasks__:
        return False
    return True


def executeTask(name, *args):
    if name in __tasks__:
        console.header('-------------------------------------\n * Executing task: %s (%s) \n -------------------------------------' % (name, __tasks__[name].desc), 1)
        __tasks__[name](*args)
    else:
        raise PukeError('No such task: %s' % name)


def printHelp(name=''):
    if name in __tasks__:
        console.header('-------------------------------------\n * Help %s (%s) \n -------------------------------------' % (name, __tasks__[name].desc), 1)
        help(__tasks__[name].getFunc())
    else:
        raise PukeError('No such task: %s' % name)


def printTasks():
    for name in __tasks__:
        obj = __tasks__[name]
        if obj.desc:
            logging.info('%s: %s' % (name, obj.desc))
        else:
            logging.info('%s' % name)


class Task:
    """"""

    def __init__(self, func, desc=''):
        name = func.__name__
        self.__func = func
        self.name = name
        self.desc = desc
        self.fullname = '%s.%s' % (func.__module__, name)
        try:
            self.__doc__ = func.__doc__
        except AttributeError:
            pass

        addTask(self)

    def __call__(self, *args, **kw):
        try:
            getcallargs(self.__func, *args)
        except TypeError as e:
            printHelp(self.name)
            console.fail('%s' % e)
            raise

        retval = self.__func(*args)
        return retval

    def __repr__(self):
        return 'Task: ' + self.name

    def getFunc(self):
        return self.__func


def task(func):
    """ Specifies that this function is a task. """
    if isinstance(func, Task):
        return func
    else:
        if isinstance(func, types.FunctionType):
            return Task(func)

        def wrapper(finalfunc):
            return Task(finalfunc, func)

        return wrapper