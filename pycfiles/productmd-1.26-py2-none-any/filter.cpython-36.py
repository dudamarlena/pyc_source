# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/filters/filter.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 5625 bytes
__doc__ = "\nproducti_gestio.filters.filter\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nThe Filter class is defined here, it is used\nto check the request using the filters.\n\nWhen :func:`producti_gestio.filters.filters.build` is triggered, a new ``Filter`` object\nis created.\nThis object is used to create the *special methods* (or dunder methods because of their ``__``) for\nPython operators (``__invert__`` for ``~``, ``__and__`` for ``and`` and ``&``, ``__or__`` for ``or`` and ``|``).\n\nIt could be useful when using ``Filters``.\nHere an example:\n\n.. code-block:: python\n\n    from producti_gestio import Server, Filters\n\n    my_server = Server(allow_get=True) # Create a server instance\n\n    @my_server.on_request(Filters.get & Filters.path('/something')) # It will filter the GET requests\n    def my_function(**kwargs):\n        return {\n            'response_code': 200, # The response code\n            'response': { # The response as a dictionary, it will be encoded in JSON\n                'ok': True\n            }\n        }\n\n    my_server.start() # Start the server using threads\n\n    while True:\n        pass\n"

class Filter:
    """Filter"""

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
    """InvertFilter"""

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
    """AndFilter"""

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
    """OrFilter"""

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