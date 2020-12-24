# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/quart_openapi/resource.py
# Compiled at: 2020-04-13 15:04:18
# Size of source mod 2**32: 3887 bytes
"""resource.py

Provide the Resource Base class to inherit from for using the class based route definitions
"""
import logging
from typing import Any, Callable, Dict, Tuple
from quart import request
from quart.typing import ResponseReturnValue
from quart.views import MethodView
from .typing import ExpectedDescList, ValidatorTypes
LOGGER = logging.getLogger('quart.serving')

def get_expect_args(expect: ExpectedDescList, default_content_type: str='application/json') -> Tuple[(ValidatorTypes, str, Dict[(str, Any)])]:
    """Normalize the different tuple sizes for the expect decorator

    :param expect: Either a validator, a tuple of size 1 containing a validator,
                   a tuple of the validator and content type or a tuple of the
                   validator, content_type and a dict of other properties to add
    :return: Regardless of how the expect decorator was used, returns a tuple containing
             the validator, the content type and any extra kwargs
    """
    content_type = default_content_type
    kwargs = {}
    if isinstance(expect, tuple):
        if len(expect) == 2:
            expect, content_type = expect
        else:
            if len(expect) == 3:
                expect, content_type, kwargs = expect
            else:
                expect = expect[0]
    return (
     expect, content_type, kwargs)


class Resource(MethodView):
    __doc__ = 'Inherit from this to create RESTful routes with openapi docs\n\n    A Resource subclass needs only to implement async functions corresponding to the HTTP\n    verbs you want to handle. Utilizing the decorators from :class:`Pint` you can set\n    the route, params, responses, and so on that will show up in the openapi documentation.\n\n    An example is,\n\n    .. code-block:: python\n\n          app = Pint(\'sample\')\n          @app.route(\'/<id>\')\n          class SimpleRoute(Resource):\n            async def get(self, id):\n              return f"ID is {id}"\n\n    That will enable a route \'/<id>\' which will return the string "ID is <id>" when called\n    by a GET request. If using :meth:`Pint.expect` to define the expected request body,\n    it will perform validation unless validate is set to false.\n    '

    async def dispatch_request(self, *args: Any, **kwargs: Any) -> ResponseReturnValue:
        """Can be overridden instead of creating verb functions

        This will be called with the request view_args, i.e. any url parameters
        """
        handler = getattr(self, request.method.lower(), None)
        if handler is None and request.method == 'HEAD' or request.method == 'OPTIONS':
            handler = getattr(self, 'get', None)
        await self.validate_payload(handler)
        return await handler(*args, **kwargs)

    async def validate_payload(self, func: Callable) -> bool:
        """This will perform validation

        Will check the api docs of the class as set by using the decorators in :class:`Pint`
        and if an expect was present without `validate` set to `False` or `None`, it will
        attempt to validate any request against the schema if json, or ensure the content_type
        matches at least.
        """
        if getattr(func, '__apidoc__', False) is not False:
            doc = func.__apidoc__
            validate = doc.get('validate', None)
            if validate:
                for expect in doc.get('expect', []):
                    validator, content_type, _ = get_expect_args(expect)
                    if content_type == 'application/json':
                        if request.is_json:
                            data = await request.get_json(force=True, cache=True)
                            return validator.validate(data)
                        elif content_type == request.mimetype:
                            return

                LOGGER.error("Request didn't pass any of the available validations")
                raise ValueError("request didn't pass validation")