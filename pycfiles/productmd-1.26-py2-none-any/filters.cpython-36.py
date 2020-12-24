# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/filters/filters.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 6240 bytes
__doc__ = "\nproducti_gestio.filters.filters\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nAll the filters are defined here using the\nFilters and the Filter class.\n\nYou can use filters by passing them as\nparameters in :func:`producti_gestio.server.server.Server.on_request`:\n\n.. code-block:: python\n\n    from producti_gestio import Server, Filter\n\n    my_server = Server(allow_get=True) # Create a server instance\n\n    @my_server.on_request(Filter.get) # It will filter the GET requests\n    def my_function(**kwargs):\n        return {\n            'response_code': 200, # The response code\n            'response': { # The response as a dictionary, it will be encoded in JSON\n                'ok': True\n            }\n        }\n\n    my_server.start() # Start the server using threads\n\n    while True:\n        pass\n\nYou can also use operators (``&``, ``|``, ``and``, ``or``, ``~``)!\n\nYou can check our repository for other examples_.\n\n.. _examples: https://github.com/pyTeens/producti-gestio/tree/master/examples\n"
import re
from .filter import Filter

def build(name: str, func: callable, **kwargs) -> Filter:
    """It builds a Filter class
    using a dictionary.

    It is used to create a Filter just giving
    a name and a function using :func:`type`.

    The provided function must have these parameters:

        * **_** - The object that is passed (useful when using a compiled function, see :func:`producti_gestio.filters.filters.Filters.regex`)
        * **kwargs** - A dictionary of all useful informations (the same is passed to the *handler function*)

    Here an example:

    .. code-block:: python

        from producti_gestio.filters.filters import build
        from producti_gestio import Server

        my_filter = build('My filter', lambda _, kwargs: bool(kwargs['path'] == '/my_path')) # If the path is '/my_path'
        my_server = Server(allow_get=True)

        @my_server.on_request(my_filter) # It uses our own filter
        def my_function(**kwargs):
            return {
                'response_code': 200, # The response code
                'response': {
                    'ok': True,
                    'path': kwargs['path']
                }
            }

        my_server.start() # Start the server using threads

        while True:
            pass

    Args:
      name(str): The name of the Filter.
      func(callable): A callable function that checks the request
      kwargs: A dictionary for other methods
      name: str:
      func: callable:
      **kwargs:

    Returns:
      Filter: A Filter-like object

    """
    d = {'__call__': func}
    d.update(kwargs)
    return type(name, (Filter,), d)()


class Filters:
    """Filters"""
    get: Filter = build('Get', lambda _, m: bool(str(m['request-type']) == 'GET'))
    post: Filter = build('Post', lambda _, m: bool(str(m['request-type']) == 'POST'))

    @staticmethod
    def regex(pattern: str, flags: int=0) -> Filter:
        """It filters requests with a path
        that match a given RegEx pattern.

        The ``Path`` always starts with ``/``!

        You can also give a flag (using :mod:`re`), here an example:

        .. code-block:: python

            import re
            from producti_gestio import Filters, Server

            my_server = Server(allow_get=True) # Create a server instance

            @my_server.on_request(Filters.regex('^/print', re.IGNORECASE)) # It filters all requests that start with print, case-insensitive
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The response code
                    'response': {
                        'ok': True,
                        'message': repr(kwargs['parameters'])
                    }
                }

            my_server.start() # Start the server using threads

            while True:
                pass

        Args:
          pattern(str): The RegEx pattern
          flags(int): The RegEx flags
          pattern: str:
          flags: int:  (Default value = 0)

        Returns:
          Filter: A Filter-like object

        """
        return build('Regex',
          (lambda _, m: bool(_.p.search(m['path'] or ''))), p=(re.compile(pattern, flags)))

    @staticmethod
    def path(given_path: str) -> Filter:
        """It filters requests using a path.

        The ``Path`` always starts with ``/``!

        Args:
          given_path(str): The path you'd like to check
          given_path: str:

        Returns:
          Filter: A Filter-like object

        """
        return build('Path',
          (lambda _, m: bool(m['path'] == _.p)), p=given_path)