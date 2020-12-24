# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/private_media.py
# Compiled at: 2019-11-08 17:24:24
# Size of source mod 2**32: 7584 bytes
"""
The following code has been sourced from DJANGO-PRIVATE-MEDIA - https://github.com/RacingTadpole/django-private-media
which has been sourced from django-filer.

I have modified some of the code, however most of the recognition should be for both;
-- django-filer
-- django-private-media

I have placed this code into one file for convenience.
"""
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import Http404, HttpResponseNotModified, HttpResponse
from django.utils.http import http_date
from django.views.static import was_modified_since
import mimetypes, os, stat

class File_Storage(FileSystemStorage):

    def __init__(self, location=None, base_url=None):
        if location is None:
            location = settings.PRIVATE_MEDIA_ROOT
        if base_url is None:
            base_url = settings.PRIVATE_MEDIA_URL
        return super(File_Storage, self).__init__(location, base_url)


class Check_Permissions(object):

    def has_read_permission(self, request, path):
        user = request.user
        if not user.is_authenticated():
            return False
        return True
        return False


class NginxXAccelRedirectServer(object):

    def serve(self, request, path):
        response = HttpResponse()
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        response['X-Accel-Redirect'] = fullpath
        response['Content-Type'] = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return response


class ApacheXSendfileServer(object):

    def serve(self, request, path):
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        response = HttpResponse()
        response['X-Sendfile'] = fullpath
        response['Content-Type'] = mimetypes.guess_type(path)[0] or 'application/octet-stream'
        return response


class DefaultServer(object):
    __doc__ = '\n    Serve static files from the local filesystem through django.\n    This is a bad idea for most situations other than testing.\n\n    This will only work for files that can be accessed in the local filesystem.\n    '

    def serve(self, request, path):
        fullpath = os.path.join(settings.PRIVATE_MEDIA_ROOT, path)
        if not os.path.exists(fullpath):
            raise Http404('"{0}" does not exist'.format(fullpath))
        else:
            statobj = os.stat(fullpath)
            content_type = mimetypes.guess_type(fullpath)[0] or 'application/octet-stream'
            return was_modified_since(request.META.get('HTTP_IF_MODIFIED_SINCE'), statobj[stat.ST_MTIME], statobj[stat.ST_SIZE]) or HttpResponseNotModified(content_type=content_type)
        response = HttpResponse((open(fullpath, 'rb').read()), content_type=content_type)
        response['Last-Modified'] = http_date(statobj[stat.ST_MTIME])
        return response


from importlib import import_module

def get_class(import_path=None):
    """
    Largely based on django.core.files.storage's get_storage_class
    """
    from django.core.exceptions import ImproperlyConfigured
    if import_path is None:
        raise ImproperlyConfigured('No class path specified.')
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("%s isn't a module." % import_path)

    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        try:
            raise ImproperlyConfigured('Error importing module %s: "%s"' % (module, e))
        finally:
            e = None
            del e

    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" class.' % (module, classname))


if settings.DEBUG == True:
    server = DefaultServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
else:
    server = ApacheXSendfileServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
if hasattr(settings, 'PRIVATE_MEDIA_PERMISSIONS'):
    permissions = (get_class(settings.PRIVATE_MEDIA_PERMISSIONS))(**getattr(settings, 'PRIVATE_MEDIA_PERMISSIONS_OPTIONS', {}))
else:
    permissions = Check_Permissions()