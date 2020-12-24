# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/decorator/wrapper.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 4821 bytes
__doc__ = "\nproducti_gestio.decorator.wrapper\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt defines a new class with decorator-magic-methods, that\nwill be called by the function that points to it.\n\nThe **user-defined** function, that's how we'll call the\nfunction that will be passed as the **handler function**, will\nbe passed to a new Decorator instance with all of the user-passed parameters, that\nwe'll call **configuration**.\n\nYou can also use :class:`producti_gestio.handlers.handler` instead of this ``Decorator``.\n\nThis decorator is intended to be used when there's one **handler function**.\nThe function that is decorated using this class will become the **server-creator function** (calling it will create the server).\n\nHere an example:\n\n    .. code-block:: python\n\n        import producti_gestio\n\n        @producti_gestio.Decorator # Use the Decorator\n        def my_server(**kwargs):\n            print('Creating the server')\n\n            def my_function(**kwargs):\n                return {\n                    'response_code': 200,\n                    'response': {\n                        'ok': True,\n                        'message': 'Hello world!'\n                    }\n                }\n\n            return my_function # Return the handler function\n\n        my_server(allow_get=True) # Create and start the server instance\n\nYou can also use the :func:`producti_gestio.core.check` function to use ``Filters``.\n"
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
    """Decorator"""
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