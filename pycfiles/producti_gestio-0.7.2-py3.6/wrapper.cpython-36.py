# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/decorator/wrapper.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 4821 bytes
"""
producti_gestio.decorator.wrapper
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It defines a new class with decorator-magic-methods, that
will be called by the function that points to it.

The **user-defined** function, that's how we'll call the
function that will be passed as the **handler function**, will
be passed to a new Decorator instance with all of the user-passed parameters, that
we'll call **configuration**.

You can also use :class:`producti_gestio.handlers.handler` instead of this ``Decorator``.

This decorator is intended to be used when there's one **handler function**.
The function that is decorated using this class will become the **server-creator function** (calling it will create the server).

Here an example:

    .. code-block:: python

        import producti_gestio

        @producti_gestio.Decorator # Use the Decorator
        def my_server(**kwargs):
            print('Creating the server')

            def my_function(**kwargs):
                return {
                    'response_code': 200,
                    'response': {
                        'ok': True,
                        'message': 'Hello world!'
                    }
                }

            return my_function # Return the handler function

        my_server(allow_get=True) # Create and start the server instance

You can also use the :func:`producti_gestio.core.check` function to use ``Filters``.
"""
try:
    import _thread
    thread_activated = True
except ImportError:
    _thread = None
    thread_activated = False

from producti_gestio.exceptions import NotAFunction
from producti_gestio.server import Server
from typing import NewType
handler_function = NewType('Handler function', callable)

class Decorator:
    __doc__ = 'The Decorator class that\n    launch automatically the\n    server and uses the user-defined\n    function.\n\n    It has got just magic methods.\n    '
    server = None

    def __init__(self, call: handler_function):
        """
        It sets the server-creator function and creates the instance.
        Before setting the function, it checks if it is callable or not, and
        the response depends on that.

        Args:
            call (handler_function): The user-defined function

        Raises:
            NotAFunction: It throws a NotAFunction exception if the given parameter is not a function
        """
        global thread_activated
        self.thread_activated = thread_activated
        if callable(call):
            self.function = call
            return
        raise NotAFunction()

    def __repr__(self) -> str:
        """
        It returns a representation
        of the object.

        Returns:
            str: A representation of the object
        """
        return 'Decorator(' + repr(self.function) + ')'

    def __call__(self, **kwargs) -> bool:
        """
        It launches the server and
        sets the handler function.

        Args:
            kwargs:  The chosen configuration. See :mod:`producti_gestio.server.Server`.

        Returns:
            bool: True if all went well, False if not
        """
        self.server = Server(**kwargs)
        self.server.set_function(self.function())
        try:
            if not self.thread_activated:
                raise Exception()
            _thread.start_new_thread(self.server.run, ())
            return True
        except Exception as e:
            print(str(e))
            try:
                self.server.run()
                return True
            except Exception as error:
                print(str(error))
                return False