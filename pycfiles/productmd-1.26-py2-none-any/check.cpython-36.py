# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/producti_gestio/core/check.py
# Compiled at: 2018-05-24 14:59:02
# Size of source mod 2**32: 3695 bytes
__doc__ = '\nproducti_gestio.core.check\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nIt checks if a request is valid using\nFilters.\n'

def check(filters: object or None=None) -> callable:
    """This function is used
    to check if a request is valid
    using filters.

    It could be used only when the ``Server`` is using the
    ``function`` mode (alias *using decorator*, not ``handlers``).

    Here an example:

    .. code-block:: python

        from producti_gestio import Server, check, Decorator, Filters

        @producti_gestio.Decorator # Using this Decorator, the next function will become the server-creator function
        def my_server(**kwargs):
            print("Initializing the server")

            @producti_gestio.check(Filters.get) # Using this Decorator, the handler function will check for the requirements (using Filters)
            def my_function(**kwargs):
                return {
                    'response_code': 200, # The response code
                    'response': {
                        'ok': True,
                        'message': 'Hello world!'
                    }
                }

            return my_function

        my_server(allow_get=True) # Create and start the server instance using threads

        while True:
            pass

    Args:
      func(callable): The native handler function
      filters(Filter or None): A Filter object or a None type
      filters: object or None:  (Default value = None)

    Returns:
      callable: A callable object

    """

    def decorator(func):
        """This wrapped-function is
        used to define the function and then
        returns it to the decorator.

        Args:
          func(callable): The function
          func: callable:

        Returns:
          callable: The wrapped-function handler_func

        """

        def handler_func(**kwargs):
            """This wrapped-function in the
            wrapped-function is used to
            check the request using filters.

            Args:
              kwargs(dict): The arguments of the request
              **kwargs: dict:

            Returns:
              dict or bool: The result of the function if all went right, False if not

            """
            if filters:
                if filters(kwargs):
                    return func(**kwargs)
                else:
                    return False
            else:
                return func(**kwargs)

        return handler_func

    return decorator