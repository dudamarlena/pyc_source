# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/form/responder/formexc.py
# Compiled at: 2006-08-02 05:57:50
from paste.recursive import ForwardRequestException
from harold.lib import keys, make_annotated, ValidationError
form_anno_template = '\ndef %(name)s%(signature)s:\n    %(docstring)r\n    return %(name)s.func_form_anno%(values)s\n'

def redirect(**attrs):
    """ decorator to make callables act like form targets

    @param **attrs arbitrary keyword-value pairs to assign to the decorated function
    @return decorator function that wraps its original with form exception handling
    """

    def form_exceptions_deco(original):
        """ form_exceptions_deco(original) -> replace original with form-enabled copy

        @param original function to decorate
        @return replacement function that redirects when ValidationError is raised
        @exception Exception when function cannot determine redirect target
        """

        def form_anno(*varparams, **keyparams):
            """ form_anno(...) -> originals replacement proxies its calls here

            """
            try:
                return original(*varparams, **keyparams)
            except (ValidationError,), exc:
                try:
                    environ = keyparams[keys.env]
                    if not attrs.has_key('target'):
                        ref = scr = environ.get('SCRIPT_NAME', '')
                    else:
                        ref = attrs['target']
                    environ[keys.form_error] = dict(exc.args[0])
                    environ[keys.form_value] = dict(exc.args[1])
                    raise ForwardRequestException(ref)
                except (KeyError,):
                    raise
                else:
                    raise Exception('Exception with no where to go')

        replacement = make_annotated(original, form_anno_template)
        for (k, v) in attrs.items():
            setattr(replacement, k, v)

        replacement.func_form_anno = form_anno
        return replacement

    return form_exceptions_deco