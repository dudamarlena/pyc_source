# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pylonsgenshi/decorators.py
# Compiled at: 2008-01-04 15:13:07
__doc__ = '\nGenshi related decorators ported from pylons.\n'
import os, pylons
from paste.util.multidict import UnicodeMultiDict
import formencode, formencode.variabledecode as variabledecode
from decorator import decorator
from pylons.decorators import determine_response_charset
from genshi.filters.html import HTMLFormFiller
from genshi.template.loader import TemplateLoader
import logging
log = logging.getLogger(__name__)
__docformat__ = 'restructuredtext en'

def validate(template=None, schema=None, validators=None, form=None, variable_decode=False, dict_char='.', list_char='-', state=None, post_only=True, on_get=False):
    """Validate input either for a FormEncode schema, or individual validators

    Given a form schema or dict of validators, validate will attempt to
    validate the schema or validator list.

    If validation was successful, the valid result dict will be saved
    as ``self.form_result``. Otherwise, the action will be re-run as if it was
    a GET, and the output will be filled by FormEncode's htmlfill to fill in
    the form field errors.

    ``template``
        Refers to the Genshi template to use in case errors need to be shown.
    ``schema``
        Refers to a FormEncode Schema object to use during validation.
    ``form``
        Method used to display the form, which will be used to get the
        HTML representation of the form for error filling.
    ``variable_decode``
        Boolean to indicate whether FormEncode's variable decode function
        should be run on the form input before validation.
    ``dict_char``
        Passed through to FormEncode. Toggles the form field naming
        scheme used to determine what is used to represent a dict. This
        option is only applicable when used with variable_decode=True.
    ``list_char``
        Passed through to FormEncode. Toggles the form field naming
        scheme used to determine what is used to represent a list. This
        option is only applicable when used with variable_decode=True.
    ``post_only``
        Boolean that indicates whether or not GET (query) variables should
        be included during validation.

        .. warning::
            ``post_only`` applies to *where* the arguments to be
            validated come from. It does *not* restrict the form to only
            working with post, merely only checking POST vars.
    ``state``
        Passed through to FormEncode for use in validators that utilize
        a state object.
    ``on_get``
        Whether to validate on GET requests. By default only POST requests
        are validated.

    Example:

    .. code-block:: python

        class SomeController(BaseController):

            def create(self, id):
                return render('myform.html')

            @validate(template='myform.html', schema=model.forms.myshema(),
                      form='create')
            def update(self, id):
                # Do something with self.form_result
                pass
    """
    log.debug('On PylonsGenshi validate decorator')

    def wrapper(func, self, *args, **kwargs):
        """Decorator Wrapper function"""
        request = pylons.request._current_obj()
        errors = {}
        if not on_get and request.environ['REQUEST_METHOD'] == 'GET':
            return func(self, *args, **kwargs)
        if post_only:
            params = request.POST
        else:
            params = request.params
        is_unicode_params = isinstance(params, UnicodeMultiDict)
        params = params.mixed()
        if variable_decode:
            log.debug('Running variable_decode on params:')
            decoded = variabledecode.variable_decode(params, dict_char, list_char)
            log.debug(decoded)
        else:
            decoded = params
        if schema:
            log.debug('Validating against a schema')
            try:
                self.form_result = schema.to_python(decoded, state)
            except formencode.Invalid, e:
                errors = e.unpack_errors(variable_decode, dict_char, list_char)

        if validators:
            log.debug('Validating against provided validators')
            if isinstance(validators, dict):
                if not hasattr(self, 'form_result'):
                    self.form_result = {}
                for (field, validator) in validators.iteritems():
                    try:
                        self.form_result[field] = validator.to_python(decoded.get(field), state)
                    except formencode.Invalid, error:
                        errors[field] = error

        if errors:
            log.debug('Errors found in validation, parsing form with htmlfill for errors')
            request.environ['REQUEST_METHOD'] = 'GET'
            pylons.c.form_errors = errors
            if not form:
                raise Exception('You MUST pass a form to display errors')
                return func(self, *args, **kwargs)
            request.environ['pylons.routes_dict']['action'] = form
            response = self._dispatch_call()
            log.debug(errors)
            pylons.c.errors = errors
            engine_dict = pylons.buffet._update_names({})
            loader = TemplateLoader(pylons.config['pylons.paths']['templates'])
            tpl = loader.load(template.replace('.', os.sep) + '.html')
            stream = tpl.generate(**engine_dict) | HTMLFormFiller(data=decoded)
            return stream.render()
        return func(self, *args, **kwargs)

    return decorator(wrapper)