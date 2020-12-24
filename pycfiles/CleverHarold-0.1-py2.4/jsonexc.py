# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/harold/form/responder/jsonexc.py
# Compiled at: 2006-08-02 05:57:50
from inspect import getargspec
from harold.lib import keys, con_type, make_annotated, ValidationError
json_anno_template = '\ndef %(name)s%(signature)s:\n    %(docstring)r\n    return %(name)s.func_json_anno%(values)s\n'

def json(**attrs):
    """ returns decorator for making json exception handlers

    @param **attrs arbitrary keyword-value pairs to assign to the decorated function
    @return decorator function that wraps its original with JSON exception handling
    """
    content_type = 'content_type'
    exc_status = '500 Internal Server Error'
    if content_type not in attrs:
        attrs[content_type] = con_type.json

    def make_json_env(func, params, kwds):
        """ make_json_env(...) -> hack to locate the wsgi environ and munge it

        """
        (args, varargs, varkw, defaults) = getargspec(func)
        if keys.env in args:
            environ = params[args.index(keys.env)]
        else:
            environ = kwds.get(keys.env, {})
        environ[keys.content_type] = con_type.json
        environ[keys.response_status] = exc_status

    def json_deco(original):
        """ json_deco(original) -> replace original with a json-enabled copy

        """

        def json_anno(*varparams, **keyparams):
            """ json_anno(...) -> annotation which makes exceptions json-friendly

            original return values and execption values should be
            json-encoded elsewhere. (e.g., by the harold code
            publisher).
            """
            try:
                return original(*varparams, **keyparams)
            except (ValidationError,), exc:
                make_json_env(original, varparams, keyparams)
                return dict(errors=exc.args[0], values=exc.args[1])
            except (Exception,), exc:
                make_json_env(original, varparams, keyparams)
                return dict(errors=[str(exc)], values=[])

        replacement = make_annotated(original, json_anno_template)
        for (k, v) in attrs.items():
            setattr(replacement, k, v)

        replacement.func_json_anno = json_anno
        return replacement

    return json_deco