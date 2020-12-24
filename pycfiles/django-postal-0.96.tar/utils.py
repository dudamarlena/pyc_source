# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mick/src/django-postal/src/postal/utils.py
# Compiled at: 2015-03-03 03:42:01
"""
Code imported and optimized from django-piston 0.2.3rc1
"""
from django import get_version as django_version
from django.http import HttpResponse

def format_error(error):
    return 'Postal (Django %s) crash report:\n\n%s' % (
     django_version(), error)


class RcFactory(object):
    """
    Status codes.
    """
    CODES = dict(ALL_OK=('OK', 200), CREATED=('Created', 201), DELETED=('', 204), BAD_REQUEST=('Bad Request',
                                                                                               400), FORBIDDEN=('Forbidden',
                                                                                                                401), NOT_FOUND=('Not Found',
                                                                                                                                 404), DUPLICATE_ENTRY=('Conflict/Duplicate',
                                                                                                                                                        409), NOT_HERE=('Gone',
                                                                                                                                                                        410), INTERNAL_ERROR=('Internal Error',
                                                                                                                                                                                              500), NOT_IMPLEMENTED=('Not Implemented',
                                                                                                                                                                                                                     501), THROTTLED=('Throttled',
                                                                                                                                                                                                                                      503))

    def __getattr__(self, attr):
        """
        Returns a fresh `HttpResponse` when getting 
        an "attribute". This is backwards compatible
        with 0.2, which is important.
        """
        try:
            r, c = self.CODES.get(attr)
        except TypeError:
            raise AttributeError(attr)

        class HttpResponseWrapper(HttpResponse):
            """
            Wrap HttpResponse and make sure that the internal _is_string 
            flag is updated when the _set_content method (via the content 
            property) is called
            """

            def _set_content(self, content):
                """
                Set the _container and _is_string properties based on the 
                type of the value parameter. This logic is in the construtor
                for HttpResponse, but doesn't get repeated when setting 
                HttpResponse.content although this bug report (feature request)
                suggests that it should: http://code.djangoproject.com/ticket/9403 
                """
                if not isinstance(content, basestring) and hasattr(content, '__iter__'):
                    self._container = content
                    self._is_string = False
                else:
                    self._container = [
                     content]
                    self._is_string = True

            content = property(HttpResponse._get_content, _set_content)

        return HttpResponseWrapper(r, content_type='text/plain', status=c)


rc = RcFactory()

class FormValidationError(Exception):

    def __init__(self, form):
        self.form = form


class HttpStatusCode(Exception):

    def __init__(self, response):
        self.response = response


def coerce_put_post(request):
    """
    Django doesn't particularly understand REST.
    In case we send data over PUT, Django won't
    actually look at the data and load it. We need
    to twist its arm here.

    The try/except abominiation here is due to a bug
    in mod_python. This should fix it.
    """
    if request.method == 'PUT':
        if hasattr(request, '_post'):
            del request._post
            del request._files
        try:
            request.method = 'POST'
            request._load_post_and_files()
            request.method = 'PUT'
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'

        request.PUT = request.POST


class MimerDataException(Exception):
    """
    Raised if the content_type and data don't match
    """
    pass


class Mimer(object):
    TYPES = dict()

    def __init__(self, request):
        self.request = request

    def is_multipart(self):
        content_type = self.content_type()
        if content_type is not None:
            return content_type.lstrip().startswith('multipart')
        else:
            return False

    def loader_for_type(self, ctype):
        """
        Gets a function ref to deserialize content
        for a certain mimetype.
        """
        for loadee, mimes in Mimer.TYPES.iteritems():
            for mime in mimes:
                if ctype.startswith(mime):
                    return loadee

    def content_type(self):
        """
        Returns the content type of the request in all cases where it is
        different than a submitted form - application/x-www-form-urlencoded
        """
        type_formencoded = 'application/x-www-form-urlencoded'
        ctype = self.request.META.get('CONTENT_TYPE', type_formencoded)
        if type_formencoded in ctype:
            return None
        else:
            return ctype

    def translate(self):
        """
        Will look at the `Content-type` sent by the client, and maybe
        deserialize the contents into the format they sent. This will
        work for JSON, YAML, XML and Pickle. Since the data is not just
        key-value (and maybe just a list), the data will be placed on
        `request.data` instead, and the handler will have to read from
        there.

        It will also set `request.content_type` so the handler has an easy
        way to tell what's going on. `request.content_type` will always be
        None for form-encoded and/or multipart form data (what your browser sends.)
        """
        ctype = self.content_type()
        self.request.content_type = ctype
        if not self.is_multipart() and ctype:
            loadee = self.loader_for_type(ctype)
            if loadee:
                try:
                    self.request.data = loadee(self.request.raw_post_data)
                    self.request.POST = self.request.PUT = dict()
                except (TypeError, ValueError):
                    raise MimerDataException

            else:
                self.request.data = None
        return self.request

    @classmethod
    def register(cls, loadee, types):
        cls.TYPES[loadee] = types

    @classmethod
    def unregister(cls, loadee):
        return cls.TYPES.pop(loadee)


def translate_mime(request):
    request = Mimer(request).translate()