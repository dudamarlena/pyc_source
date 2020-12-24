# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/dispatcher_application.py
# Compiled at: 2018-06-03 12:39:11
__all__ = [
 'DispatcherApplication',
 'BasePackageDispatcherApplication',
 'FilePathDispatcherApplication']
__authors__ = ['Tim Chow']
import re, types
from .wsgi import *
from .model_and_view import *
from .interface import *
from .exception import *
from .json_view_resolver import JsonViewResolver
from .request_mapping_handler_mapping import *
from .request_mapping_handler_adapter import *
from .handler_execution_chain import *
from .constrant import HTTPStatus
from ..application_context import *
from .dispatcher_application_configurer import *

class DispatcherApplication(object):

    def __init__(self, application_context):
        self._ctx = application_context
        self._handler_mappings = []
        self._handler_adapters = []
        self._view_resolver = JsonViewResolver()
        self._handler_interceptors = []
        for name, bean in self._ctx.iter_beans():
            obj = self._ctx.get_bean(name)
            if issubclass(bean.cls, HandlerMapping):
                self._handler_mappings.append(obj)
            if issubclass(bean.cls, HandlerAdapter):
                self._handler_adapters.append(obj)
            if issubclass(bean.cls, ViewResolver):
                self._view_resolver = obj
            if issubclass(bean.cls, HandlerInterceptor):
                self._handler_interceptors.append(obj)

        self._default_handler_mapping = RequestMappingHandlerMapping()
        self._default_handler_adapter = RequestMappingHandlerAdapter()
        self._configurer = DefaultDispatcherApplicationConfigurer()

    @property
    def application_context(self):
        return self._ctx

    @property
    def handler_mappings(self):
        return self._handler_mappings

    @property
    def handler_adapters(self):
        return self._handler_adapters

    @property
    def view_resolver(self):
        return self._view_resolver

    @property
    def handler_interceptors(self):
        return self._handler_interceptors

    @property
    def configurer(self):
        return self._configurer

    @configurer.setter
    def configurer(self, configurer):
        self._configurer = configurer

    def get_handler(self, request):
        for hm in self.handler_mappings:
            handler = hm.get_handler(request)
            if handler is not None:
                return handler

        return self._default_handler_mapping.get_handler(request)

    def get_adpater(self, handler):
        for ha in self.handler_adapters:
            if ha.supports(handler):
                return ha

        if self._default_handler_adapter.supports(handler):
            return self._default_handler_adapter
        else:
            return

    def get_interceptors(self, uri):
        interceptors = []
        for hi in self.handler_interceptors:
            if re.match(hi.path_pattern(), uri):
                interceptors.append(hi)

        return sorted(interceptors, key=lambda hi: hi.get_order(), reverse=True)

    def __do_dispatch(self, request, response):
        handler = self.get_handler(request)
        if handler is None:
            raise NoHandlerFoundError
        adapter = self.get_adpater(handler)
        if adapter is None:
            raise NoAdapterFoundError
        interceptors = self.get_interceptors(request.uri)
        hec = HandlerExecutionChain(handler, interceptors)
        return adapter.handle(request, response, hec)

    def __render(self, mv, status_code):
        view_object = self.view_resolver.get_view(mv.view, status_code)
        response_body = view_object.render(mv.model)
        return (response_body, view_object.get_content_type())

    def __call__(self, enviroment, start_response):
        request = Request(enviroment, self.application_context)
        response = Response(request)
        mv = ModelAndView()
        try:
            for redirect_count in range(self.configurer.max_redirect_count):
                result = self.__do_dispatch(request, response)
                if response.internal_redirect_to is not None:
                    request.uri = response.internal_redirect_to
                    response.clear()
                    continue
                if response.status_code in [HTTPStatus.MovedPermanently,
                 HTTPStatus.MovedTemporarily]:
                    response.remove_headers('Content-Length', 'Transfer-Encoding')
                    start_response(response.get_headline(), response.get_headers())
                    request.close()
                    response.close()
                    return ['']
                if isinstance(result, types.GeneratorType):
                    response.remove_headers('Content-Length')
                    start_response(response.get_headline(), response.get_headers())
                    request.close()
                    response.close()
                    return result
                mv.merge(result)
                break
            else:
                raise MaxRedirectCountReached('internal redirect count: %d' % redirect_count)

        except (NoHandlerFoundError, NoAdapterFoundError):
            response.set_status(HTTPStatus.NotFound)
            mv.model.add_attribute('info', 'no handler or adapter found')
        except:
            import traceback
            traceback.print_exc()
            response.set_status(HTTPStatus.InternalError)
            mv.model.add_attribute('traceback', traceback.format_exc())

        body, content_type = self.__render(mv, response.status_code)
        response.add_header('Content-Length', str(len(body)))
        if content_type is not None:
            response.add_header('Content-Type', content_type)
        start_response(response.get_headline(), response.get_headers())
        request.close()
        response.close()
        return [
         body]


class BasePackageDispatcherApplication(DispatcherApplication):

    def __init__(self, *packages):
        DispatcherApplication.__init__(self, BasePackageApplicationContext(*packages))


class FilePathDispatcherApplication(DispatcherApplication):

    def __init__(self, *paths):
        DispatcherApplication.__init__(self, FilePathApplicationContext(*paths))