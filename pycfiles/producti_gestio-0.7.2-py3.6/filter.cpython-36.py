# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/filters/filter.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 5625 bytes
"""
producti_gestio.filters.filter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The Filter class is defined here, it is used
to check the request using the filters.

When :func:`producti_gestio.filters.filters.build` is triggered, a new ``Filter`` object
is created.
This object is used to create the *special methods* (or dunder methods because of their ``__``) for
Python operators (``__invert__`` for ``~``, ``__and__`` for ``and`` and ``&``, ``__or__`` for ``or`` and ``|``).

It could be useful when using ``Filters``.
Here an example:

.. code-block:: python

    from producti_gestio import Server, Filters

    my_server = Server(allow_get=True) # Create a server instance

    @my_server.on_request(Filters.get & Filters.path('/something')) # It will filter the GET requests
    def my_function(**kwargs):
        return {
            'response_code': 200, # The response code
            'response': { # The response as a dictionary, it will be encoded in JSON
                'ok': True
            }
        }

    my_server.start() # Start the server using threads

    while True:
        pass
"""

class Filter:
    __doc__ = '\n    The Filter class is used\n    to check the given requests using\n    Filters.\n    '

    def __call__(self, args: dict):
        """
        It raises a NotImplementedError.

        Args:
            args (dict): The dictionary that will be used by filters

        Raises:
            NotImplementedError
        """
        raise NotImplementedError

    def __invert__(self) -> object:
        """
        It returns a InvertFilter object.

        Returns:
            InvertFilter: The InvertFilter object
        """
        return InvertFilter(self)

    def __and__(self, other: object) -> object:
        """
        It returns a AndFilter object.

        Args:
            other (Filter): The other filter you'd like to check

        Returns:
            AndFilter: The AndFilter object
        """
        return AndFilter(self, other)

    def __or__(self, other: object) -> object:
        """
        It returns a OrFilter object.

        Args:
            other (Filter): The other filter you'd like to check

        Returns:
            OrFilter: The OrFilter object
        """
        return OrFilter(self, other)


class InvertFilter(Filter):
    __doc__ = '\n    The InvertFilter is used to return an inverted filter\n    '

    def __init__(self, base: object):
        """
        It initializes the object.

        Args:
            base (object): The Filter that you'd like to check
        """
        self.base = base

    def __call__(self, args: dict) -> bool:
        """
        It returns the inverted result
        of a Filter.

        Args:
            args (dict): The dictionary that will be used by filters

        Returns:
            bool: The inverted result of the Filter
        """
        return not self.base(args)


class AndFilter(Filter):
    __doc__ = '\n    The AndFilter is used to\n    check two Filters and return\n    their result\n    '

    def __init__(self, base: object, other: object):
        """
        It initializes the object.

        Args:
            base (object): One of the Filters that you'd like to check
            other (object): The other Filter
        """
        self.base = base
        self.other = other

    def __call__(self, args: dict) -> bool:
        """
        It returns the result of
        two Filters.

        Args:
            args (dict): The dictionary that will be used by filters

        Returns:
            bool: True if all the Filters returned True, False if not
        """
        return self.base(args) and self.other(args)


class OrFilter(Filter):
    __doc__ = 'The OrFilter is used to\n    check two Filters and see if\n    one of them is True.\n    '

    def __init__(self, base: object, other: object):
        """
        It initializes the object.

        Args:
            base (object): One of the Filters that you'd like to check
            other (object): The other Filter
        """
        self.base = base
        self.other = other

    def __call__(self, args: dict) -> bool:
        """
        It returns the result of
        two Filters.

        Args:
            args (dict): The dictionary that will be used by filters

        Returns:
            bool: True if one of the Filters returned True, False if not
        """
        return self.base(args) or self.other(args)