# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/private_media.py
# Compiled at: 2020-05-03 01:13:24
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

def get_class--- This code section failed: ---

 L. 192         0  LOAD_CONST               0
                2  LOAD_CONST               ('ImproperlyConfigured',)
                4  IMPORT_NAME_ATTR         django.core.exceptions
                6  IMPORT_FROM              ImproperlyConfigured
                8  STORE_FAST               'ImproperlyConfigured'
               10  POP_TOP          

 L. 193        12  LOAD_FAST                'import_path'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    28  'to 28'

 L. 194        20  LOAD_FAST                'ImproperlyConfigured'
               22  LOAD_STR                 'No class path specified.'
               24  CALL_FUNCTION_1       1  ''
               26  RAISE_VARARGS_1       1  'exception instance'
             28_0  COME_FROM            18  '18'

 L. 195        28  SETUP_FINALLY        44  'to 44'

 L. 196        30  LOAD_FAST                'import_path'
               32  LOAD_METHOD              rindex
               34  LOAD_STR                 '.'
               36  CALL_METHOD_1         1  ''
               38  STORE_FAST               'dot'
               40  POP_BLOCK        
               42  JUMP_FORWARD         76  'to 76'
             44_0  COME_FROM_FINALLY    28  '28'

 L. 197        44  DUP_TOP          
               46  LOAD_GLOBAL              ValueError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    74  'to 74'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 198        58  LOAD_FAST                'ImproperlyConfigured'
               60  LOAD_STR                 "%s isn't a module."
               62  LOAD_FAST                'import_path'
               64  BINARY_MODULO    
               66  CALL_FUNCTION_1       1  ''
               68  RAISE_VARARGS_1       1  'exception instance'
               70  POP_EXCEPT       
               72  JUMP_FORWARD         76  'to 76'
             74_0  COME_FROM            50  '50'
               74  END_FINALLY      
             76_0  COME_FROM            72  '72'
             76_1  COME_FROM            42  '42'

 L. 199        76  LOAD_FAST                'import_path'
               78  LOAD_CONST               None
               80  LOAD_FAST                'dot'
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  LOAD_FAST                'import_path'
               88  LOAD_FAST                'dot'
               90  LOAD_CONST               1
               92  BINARY_ADD       
               94  LOAD_CONST               None
               96  BUILD_SLICE_2         2 
               98  BINARY_SUBSCR    
              100  ROT_TWO          
              102  STORE_FAST               'module'
              104  STORE_FAST               'classname'

 L. 200       106  SETUP_FINALLY       120  'to 120'

 L. 201       108  LOAD_GLOBAL              import_module
              110  LOAD_FAST                'module'
              112  CALL_FUNCTION_1       1  ''
              114  STORE_FAST               'mod'
              116  POP_BLOCK        
              118  JUMP_FORWARD        170  'to 170'
            120_0  COME_FROM_FINALLY   106  '106'

 L. 202       120  DUP_TOP          
              122  LOAD_GLOBAL              ImportError
              124  COMPARE_OP               exception-match
              126  POP_JUMP_IF_FALSE   168  'to 168'
              128  POP_TOP          
              130  STORE_FAST               'e'
              132  POP_TOP          
              134  SETUP_FINALLY       156  'to 156'

 L. 203       136  LOAD_FAST                'ImproperlyConfigured'
              138  LOAD_STR                 'Error importing module %s: "%s"'
              140  LOAD_FAST                'module'
              142  LOAD_FAST                'e'
              144  BUILD_TUPLE_2         2 
              146  BINARY_MODULO    
              148  CALL_FUNCTION_1       1  ''
              150  RAISE_VARARGS_1       1  'exception instance'
              152  POP_BLOCK        
              154  BEGIN_FINALLY    
            156_0  COME_FROM_FINALLY   134  '134'
              156  LOAD_CONST               None
              158  STORE_FAST               'e'
              160  DELETE_FAST              'e'
              162  END_FINALLY      
              164  POP_EXCEPT       
              166  JUMP_FORWARD        170  'to 170'
            168_0  COME_FROM           126  '126'
              168  END_FINALLY      
            170_0  COME_FROM           166  '166'
            170_1  COME_FROM           118  '118'

 L. 204       170  SETUP_FINALLY       184  'to 184'

 L. 205       172  LOAD_GLOBAL              getattr
              174  LOAD_FAST                'mod'
              176  LOAD_FAST                'classname'
              178  CALL_FUNCTION_2       2  ''
              180  POP_BLOCK        
              182  RETURN_VALUE     
            184_0  COME_FROM_FINALLY   170  '170'

 L. 206       184  DUP_TOP          
              186  LOAD_GLOBAL              AttributeError
              188  COMPARE_OP               exception-match
              190  POP_JUMP_IF_FALSE   218  'to 218'
              192  POP_TOP          
              194  POP_TOP          
              196  POP_TOP          

 L. 207       198  LOAD_FAST                'ImproperlyConfigured'
              200  LOAD_STR                 'Module "%s" does not define a "%s" class.'
              202  LOAD_FAST                'module'
              204  LOAD_FAST                'classname'
              206  BUILD_TUPLE_2         2 
              208  BINARY_MODULO    
              210  CALL_FUNCTION_1       1  ''
              212  RAISE_VARARGS_1       1  'exception instance'
              214  POP_EXCEPT       
              216  JUMP_FORWARD        220  'to 220'
            218_0  COME_FROM           190  '190'
              218  END_FINALLY      
            220_0  COME_FROM           216  '216'

Parse error at or near `POP_TOP' instruction at offset 194


if settings.DEBUG == True:
    server = DefaultServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
else:
    server = ApacheXSendfileServer(**getattr(settings, 'PRIVATE_MEDIA_SERVER_OPTIONS', {}))
if hasattr(settings, 'PRIVATE_MEDIA_PERMISSIONS'):
    permissions = (get_class(settings.PRIVATE_MEDIA_PERMISSIONS))(**getattr(settings, 'PRIVATE_MEDIA_PERMISSIONS_OPTIONS', {}))
else:
    permissions = Check_Permissions()