# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/flasik/decorators.py
# Compiled at: 2019-08-24 16:39:35
"""
decorators.py

Misc decorators

"""
import copy, inspect, blinker, functools, flask_cors
from .core import init_app as h_init_app, utc_now, apply_function_to_members
from flask import request, make_response, current_app, Response

def init_app(f):
    """
    Decorator for init_app
    As a convenience
    ie:
    def fn(app):
        pass
        
    before you would do: init_app(fn)
    
    with this decorator
    
    @init_app
    def fn(app):
        pass
        
    """
    return h_init_app(f)


def cors(*args, **kwargs):
    """
    A wrapper around flask-cors cross_origin, to also act on classes

    **An extra note about cors, a response must be available before the
    cors is applied. Dynamic return is applied after the fact, so use the
    decorators, json, xml, or return self.render() for txt/html
    ie:
    @cors()
    class Index(Flasik):
        def index(self):
            return self.render()

        @json
        def json(self):
            return {}

    class Index2(Flasik):
        def index(self):
            return self.render()

        @cors()
        @json
        def json(self):
            return {}

    :return:
    """

    def decorator(fn):
        cors_fn = flask_cors.cross_origin(automatic_options=True, *args, **kwargs)
        if inspect.isclass(fn):
            apply_function_to_members(fn, cors_fn)
        else:
            return cors_fn(fn)

    return decorator


def _cors(*args, **kwargs):
    """
    https://github.com/corydolphin/flask-cors/blob/master/flask_cors/decorator.py
    """
    _options = kwargs

    def decorator(f):
        if _options.get('automatic_options', True):
            f.required_methods = getattr(f, 'required_methods', set())
            f.required_methods.add('OPTIONS')
            f.provide_automatic_options = False

        def wrapped_function(*args, **kwargs):
            resp = f(*args, **kwargs)
            print f.required_methods
            if not isinstance(resp, Response):
                print (
                 'WOW', resp)
                resp = make_response(resp)
            options = flask_cors.core.get_cors_options(current_app, _options)
            flask_cors.core.set_cors_headers(resp, options)
            print ('R', resp, resp.headers)
            return resp

        return functools.update_wrapper(wrapped_function, f)

    return decorator


def headers(params={}):
    """This decorator adds the headers passed in to the response
    http://flask.pocoo.org/snippets/100/
    """

    def decorator(f):
        if inspect.isclass(f):
            h = headers(params)
            apply_function_to_members(f, h)
            return f

        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            resp = make_response(f(*args, **kwargs))
            h = resp.headers
            for header, value in params.items():
                h[header] = value

            return resp

        return decorated_function

    return decorator


def noindex(f):
    """This decorator passes X-Robots-Tag: noindex
    http://flask.pocoo.org/snippets/100/
    """
    return headers({'X-Robots-Tag': 'noindex'})(f)


__signals_namespace = blinker.Namespace()

def emit_signal(sender=None, namespace=None):
    """
    @emit_signal
    A decorator to mark a method or function as a signal emitter
    It will turn the function into a decorator that can be used to 
    receive signal with: $fn_name.pre.connect, $fn_name.post.connect 
    *pre will execute before running the function
    *post will run after running the function
    
    **observe is an alias to post.connect
    
    :param sender: string  to be the sender.
    If empty, it will use the function __module__+__fn_name,
    or method __module__+__class_name__+__fn_name__
    :param namespace: The namespace. If None, it will use the global namespace
    :return:

    """
    if not namespace:
        namespace = __signals_namespace

    def decorator(fn):
        fname = sender
        if not fname:
            fnargs = inspect.getargspec(fn).args
            fname = fn.__module__
            if 'self' in fnargs or 'cls' in fnargs:
                caller = inspect.currentframe().f_back
                fname += '_' + caller.f_code.co_name
            fname += '__' + fn.__name__
        fn.pre = namespace.signal('pre_%s' % fname)
        fn.post = namespace.signal('post_%s' % fname)
        fn.observe = fn.post.connect

        def send(action, *a, **kw):
            sig_name = '%s_%s' % (action, fname)
            result = kw.pop('result', None)
            kw.update(inspect.getcallargs(fn, *a, **kw))
            sendkw = {'kwargs': {k:v for k, v in kw.items() if k in kw.keys()}, 'sender': fn.__name__, 
               'emitter': kw.get('self', kw.get('cls', fn))}
            if action == 'post':
                namespace.signal(sig_name).send(result, **sendkw)
            else:
                namespace.signal(sig_name).send(**sendkw)
            return

        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            send('pre', *args, **kwargs)
            result = fn(*args, **kwargs)
            kwargs['result'] = result
            send('post', *args, **kwargs)
            return result

        return wrapper

    return decorator