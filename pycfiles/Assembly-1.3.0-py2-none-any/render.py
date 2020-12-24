# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/render.py
# Compiled at: 2019-08-24 15:52:11
import copy, inspect, arrow, blinker, functools, flask_cors
from jinja2 import Markup
from dicttoxml import dicttoxml
from werkzeug.wrappers import BaseResponse
from .core import Flasik, init_app as h_init_app, apply_function_to_members, build_endpoint_route_name, set_view_attr, get_view_attr
from flask import Response, jsonify, request, current_app, url_for, make_response, g
import flask.json
from flask.json import dumps as flask_dumps

class _JSONEnc(flask.json.JSONEncoder):

    def default(self, o):
        if isinstance(o, arrow.Arrow):
            return o.for_json()
        else:
            return super(self.__class__, self).default(o)


def dumps(o, **kw):
    kw['cls'] = _JSONEnc
    return flask_dumps(o, **kw)


flask.json.dumps = dumps

def _normalize_response_tuple(tuple_):
    """
    Helper function to normalize view return values .
    It always returns (dict, status, headers). Missing values will be None.
    For example in such cases when tuple_ is
      (dict, status), (dict, headers), (dict, status, headers),
      (dict, headers, status)

    It assumes what status is int, so this construction will not work:
    (dict, None, headers) - it doesn't make sense because you just use
    (dict, headers) if you want to skip status.
    """
    v = tuple_ + (None, ) * (3 - len(tuple_))
    if isinstance(v[1], int):
        return v
    else:
        return (v[0], v[2], v[1])


__view_parsers = set()

def view_parser(f):
    """
    A simple decorator to to parse the data that will be rendered
    :param func:
    :return:
    """
    __view_parsers.add(f)
    return f


def _build_response(data, renderer=None):
    """
    Build a response using the renderer from the data
    :return:
    """
    if isinstance(data, Response) or isinstance(data, BaseResponse):
        return data
    if not renderer:
        raise AttributeError(' Renderer is required')
    if isinstance(data, dict) or data is None:
        data = {} if data is None else data
        for _ in __view_parsers:
            data = _(data)

        return make_response(renderer(data), 200, None)
    else:
        if isinstance(data, tuple):
            data, status, headers = _normalize_response_tuple(data)
            for _ in __view_parsers:
                data = _(data)

            return make_response(renderer(data or {}), status, headers)
        return data


json_renderer = lambda i, data: _build_response(data, jsonify)
xml_renderer = lambda i, data: _build_response(data, dicttoxml)

def json(func):
    """
    Decorator to render as JSON
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, json)
        return func
    else:

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, jsonify)

        return decorated_view


def xml(func):
    """
    Decorator to render as XML
    :param func:
    :return:
    """
    if inspect.isclass(func):
        apply_function_to_members(func, xml)
        return func
    else:

        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            data = func(*args, **kwargs)
            return _build_response(data, dicttoxml)

        return decorated_view


def jsonp(func):
    """Wraps JSONified output for JSONP requests.
    http://flask.pocoo.org/snippets/79/
    """

    @functools.wraps(func)
    def decorated_view(*args, **kwargs):
        callback = request.args.get('callback', None)
        if callback:
            data = str(func(*args, **kwargs))
            content = str(callback) + '(' + data + ')'
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
            return

    return decorated_view


def template(page=None, layout=None, **kwargs):
    """
    Decorator to change the view template and layout.

    It works on both Flasik class and view methods

    on class
        only $layout is applied, everything else will be passed to the kwargs
        Using as first argument, it will be the layout.

        :first arg or $layout: The layout to use for that view
        :param layout: The layout to use for that view
        :param kwargs:
            get pass to the TEMPLATE_CONTEXT

    ** on method that return a dict
        page or layout are optional

        :param page: The html page
        :param layout: The layout to use for that view

        :param kwargs:
            get pass to the view as k/V

    ** on other methods that return other type, it doesn't apply

    :return:
    """
    pkey = '_template_extends__'

    def decorator(f):
        if inspect.isclass(f):
            layout_ = layout or page
            extends = kwargs.pop('extends', None)
            if extends and hasattr(extends, pkey):
                items = getattr(extends, pkey).items()
                if 'layout' in items:
                    layout_ = items.pop('layout')
                for k, v in items:
                    kwargs.setdefault(k, v)

            if not layout_:
                layout_ = 'layout.html'
            kwargs.setdefault('brand_name', '')
            kwargs['layout'] = layout_
            setattr(f, pkey, kwargs)
            setattr(f, 'base_layout', kwargs.get('layout'))
            setattr(f, 'template_markup', 'html')
            return f
        else:

            @functools.wraps(f)
            def wrap(*args2, **kwargs2):
                response = f(*args2, **kwargs2)
                if isinstance(response, dict) or response is None:
                    response = response or {}
                    if page:
                        response.setdefault('_template', page)
                    if layout:
                        response.setdefault('_layout', layout)
                    for k, v in kwargs.items():
                        response.setdefault(k, v)

                return response

            return wrap
            return

    return decorator