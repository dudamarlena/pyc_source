# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kyoukai/backends/uwsgi.py
# Compiled at: 2017-09-29 12:38:41
# Size of source mod 2**32: 5983 bytes
"""
A uWSGI adapter for Kyoukai.

This allows you to run Kyoukai with uWSGI as the web server. It translates the WSGI protocol into 
Kyoukai itself.
"""
import asyncio
try:
    import greenlet
except ImportError:
    raise RuntimeError('uwsgi must be configured with the greenlet and asyncio workers enabled for the uwsgi backend')

import functools
from asphalt.core import Context, ContainerComponent
from asphalt.core.component import component_types
from kyoukai.app import Kyoukai
from kyoukai.asphalt import KyoukaiBaseComponent
from werkzeug.wrappers import Request, Response

def uwsgi_entry_point(func):
    """
    Wraps a function as a uWSGI entry point.

    This will automatically switch greenlets and set the result on a Future instance.
    :param func: The function to wrap.
    """

    @functools.wraps(func)
    async def _uwsgi_entry_point(self, current_greenlet, future, *args, **kwargs):
        """
        uWSGI wrapper entry point.
        """
        try:
            try:
                result = await func(self, *args, **kwargs)
            except Exception as e:
                future.set_exception(e)
            else:
                future.set_result(result)
        finally:
            current_greenlet.switch()

    return _uwsgi_entry_point


class uWSGIAdapter(object):
    __doc__ = '\n    The main adapter.\n\n    To use uWSGI with Kyoukai, you must create an instance of this class with your app object, and \n    point uWSGI to the ``wsgi_application`` method.\n\n    .. code:: python\n\n        from kyoukai.backends.uwsgi import uWSGIAdapter\n        from myapp.app import kyk\n\n        adapter = uWSGIAdapter(kyk)\n\n    This adapter also supports using Asphalt .yml files.\n\n    .. code:: python\n\n        adapter = uWSGIAdapter.from_component(component, "config.yml")\n\n    Then, your app will be running under uWSGI.\n    '

    def __init__(self, app: Kyoukai, base_context: Context=None):
        """
        :param app: The application this class is running.
        """
        self.app = app
        self.app.finalize()
        self.base_context = base_context or Context()
        self.loop = None

    @classmethod
    def from_asphalt_config(cls, filename: str) -> 'uWSGIAdapter':
        """
        Produces a new uWSGIAdapter from an Asphalt config file.

        :param filename: The full path to the config file.
        """
        from ruamel import yaml
        with open(filename):
            config_data = yaml.load(filename)
        try:
            component_config = config_data.pop('component')
        except KeyError:
            raise LookupError('missing configuration key: component') from None
        else:
            component = (component_types.create_object)(**component_config)
        context = Context()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(component.start(context))
        for c in component.child_components:
            if isinstance(c, KyoukaiBaseComponent):
                break
        else:
            raise TypeError('Could not find KyoukaiComponent in component list')

        del component
        klass = cls(c.app, context)
        return klass

    @uwsgi_entry_point
    async def enter_kyoukai(self, request: Request) -> Response:
        """
        The main entry point to enter the app.

        This will be running inside the app greenlet.

        :param request: The request object to handle.
        :return: A response object to return.
        """
        result = await self.app.process_request(request, self.base_context)
        return result

    def run_application(self, environment: dict, start_response: callable):
        """
        Main entry point for the application.
        Called upon every request.

        :param environment: The WSGI environment for the application.
        :param start_response: A callable which is used by the Response.
        :return: A Werkzeug Response object.
        """
        if self.loop is None:
            self.loop = asyncio.get_event_loop()
        request = self.app.request_class(environment)
        fut = asyncio.Future(loop=(self.loop))
        g = greenlet.getcurrent()
        self.loop.create_task(self.enter_kyoukai(g, fut, request))
        g.parent.switch()
        result = fut.result()
        return result(environment, start_response)