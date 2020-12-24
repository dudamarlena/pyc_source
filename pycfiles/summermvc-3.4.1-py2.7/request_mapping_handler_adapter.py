# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/mvc/request_mapping_handler_adapter.py
# Compiled at: 2018-05-30 09:28:23
__all__ = [
 'RequestMappingHandlerAdapter']
__authors__ = ['Tim Chow']
import inspect, types
from .interface import HandlerAdapter
from ..decorator import *
from .exception import *
from .model_and_view import ModelAndView, Model

class RequestMappingHandlerAdapter(HandlerAdapter):

    def supports(self, handler):
        return is_request_mapping_present(handler.page_handler)

    def __build_args(self, handler, request, response, mv, matches):
        argspec = inspect.getargspec(handler)
        args = argspec.args
        defaults = {}
        if argspec.defaults:
            defaults = dict(zip(argspec.args[-1 * len(argspec.defaults):], argspec.defaults))
        bind_args = []
        for arg_name in args[1:]:
            if arg_name.startswith('arg_'):
                if len(arg_name) == 4:
                    raise InvalidArgumentError
                try:
                    bind_args.append(request.get_argument(arg_name[4:]))
                except MissingArgumentError:
                    if arg_name not in defaults:
                        raise
                    bind_args.append(defaults[arg_name])

                continue
            if arg_name.startswith('args_'):
                if len(arg_name) == 5:
                    raise InvalidArgumentError
                try:
                    bind_args.append(request.get_arguments(arg_name[5:]))
                except MissingArgumentError:
                    if arg_name not in defaults:
                        raise
                    bind_args.append(defaults[arg_name])

                continue
            if arg_name == 'request':
                bind_args.append(request)
                continue
            if arg_name == 'request_body':
                bind_args.append(request.body)
                continue
            if arg_name == 'response':
                bind_args.append(response)
                continue
            if arg_name == 'model_and_view':
                bind_args.append(mv)
                continue
            if arg_name == 'model':
                bind_args.append(mv.model)
                continue
            if arg_name.startswith('path_var_'):
                if len(arg_name) == 9:
                    raise InvalidArgumentError
                if arg_name[9:] in matches:
                    bind_args.append(matches[arg_name[9:]])
                elif arg_name in defaults:
                    bind_args.append(defaults[arg_name])
                else:
                    raise MissingArgumentError
                continue
            if arg_name.startswith('header_'):
                if len(arg_name) == 7:
                    raise InvalidArgumentError
                value = request.get_header_or_default(arg_name[7:], None)
                if value is not None:
                    bind_args.append(value)
                elif arg_name in defaults:
                    bind_args.append(defaults[arg_name])
                else:
                    raise MissingArgumentError
                continue
            if arg_name.startswith('cookie_'):
                if len(arg_name) == 7:
                    raise InvalidArgumentError
                value = request.get_cookie_or_default(arg_name[7:], None)
                if value is not None:
                    bind_args.append(value)
                elif arg_name in defaults:
                    bind_args.append(defaults[arg_name])
                else:
                    raise MissingArgumentError
                continue
            raise InvalidArgumentError('unsupported argument: %s' % arg_name)

        return tuple(bind_args)

    def handle(self, request, response, handler_execution_chain):
        mv = ModelAndView()
        handler = handler_execution_chain.handler
        exceptions = tuple(handler.exception_handlers.keys())
        try:
            result = handler_execution_chain.handle(request, response, mv, *self.__build_args(handler.page_handler, request, response, mv, handler.matches))
        except exceptions as ex:
            import traceback
            traceback.print_exc()
            for exception in exceptions:
                if isinstance(ex, exception):
                    exception_handler, matches = handler.exception_handlers[exception]
                    result = exception_handler(*self.__build_args(exception_handler, request, response, mv, matches))
                    break
            else:
                raise

        if response.get_header('Content-Type') is None:
            rm = get_request_mapping(handler.page_handler)
            if rm['produce'] is not None:
                response.add_header('Content-Type', rm['produce'])
        if isinstance(result, types.GeneratorType):
            return result
        else:
            if result is None:
                pass
            elif isinstance(result, Model):
                mv.model.merge(result)
            elif isinstance(result, ModelAndView):
                mv.merge(result)
            elif isinstance(result, basestring):
                mv.view = result
            else:
                raise InvalidReturnValueError
            return mv