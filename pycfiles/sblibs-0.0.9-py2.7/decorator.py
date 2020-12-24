# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sblibs/display/decorator.py
# Compiled at: 2017-09-18 18:37:05
"""
    The base class for creating new Decorators

    * Decorator: A base class for creating new decorators

"""
from __future__ import unicode_literals
from functools import wraps
from warnings import warn
from .base import DecoratorManager

class Decorator(DecoratorManager):
    """Decorator base class to keep easy creating more decorators

    triggers:
        self.start
        self.stop

    context_manager:
        self.__enter__
        self.__exit__

    Only this is in generall necessary to implement the class you are writing,
    like this:

    class Wired(Decorator):
        def __init__(self, user='Lain')
            self.user = user
        def start(self):
            self.login()

        def stop(self):
            self.logoff()

        def login(self):
            print('Welcome to the Wired, {user}!'.format(user=self.user))

        def logoff(self):
            print('Close this world, open the next!'.)

    And all the black magic is done for you behind the scenes. In theory,
    you can  use the decorator in these way:

    @Wired('lain')
    def foo():
        pass

    @Wired(argument='banana')
    def bar():
        pass

    @Wired
    def lain():
        pass

    @Wired()
    def death():
        pass

    And all are okay! As well, natively, you have support to use as
    context managers.

    So that you can handle that way:

    with Wired:
        print("Download the Knight files...")

    with Wired():
        print("Underlying bugs not anymore")

    with Wired("Lerax"):
        print("I'm exists?")

    with Wired(user="Lerax"):
        print("I don't have the real answer.")

    And all occurs be fine like you thinks this do.

    """
    instances = []

    @classmethod
    def __call__(cls, *args, **kwargs):
        instance = cls.recreate(*args, **kwargs)
        cls.instances.append(instance)
        if any(args) and callable(args[0]):
            return instance._over_wrapper(args[0])
        return instance

    def _over_wrapper(self, function):

        @wraps(function)
        def _wrapper(*args, **kargs):
            self.start()
            result = function(*args, **kargs)
            self.stop()
            return result

        return _wrapper

    @classmethod
    def default_arguments(cls):
        """Returns the available kwargs of the called class"""
        func = cls.__init__
        args = func.__code__.co_varnames
        defaults = func.__defaults__
        index = -len(defaults)
        return {k:v for k, v in zip(args[index:], defaults)}

    @classmethod
    def recreate(cls, *args, **kwargs):
        """Recreate the class based in your args, multiple uses"""
        cls.check_arguments(kwargs)
        first_is_callable = True if any(args) and callable(args[0]) else False
        signature = cls.default_arguments()
        allowed_arguments = {k:v for k, v in kwargs.items() if k in signature}
        if (any(allowed_arguments) or any(args)) and not first_is_callable:
            if any(args) and not first_is_callable:
                return cls(args[0], **allowed_arguments)
            if any(allowed_arguments):
                return cls(**allowed_arguments)
        if any(cls.instances):
            return cls.instances[(-1)]
        return cls()

    @classmethod
    def check_arguments(cls, passed):
        """Put warnings of arguments whose can't be handle by the class"""
        defaults = list(cls.default_arguments().keys())
        template = b'Pass arg {argument:!r} in {cname:!r}, can be a typo? Supported key arguments: {defaults}'
        fails = []
        for arg in passed:
            if arg not in defaults:
                warn(template.format(argument=arg, cname=cls.__name__, defaults=defaults))
                fails.append(arg)

        return any(fails)