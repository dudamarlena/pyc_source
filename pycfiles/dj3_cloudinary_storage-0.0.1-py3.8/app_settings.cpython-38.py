# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/app_settings.py
# Compiled at: 2020-03-05 09:53:49
# Size of source mod 2**32: 4455 bytes
import importlib, os, sys
from operator import itemgetter
import cloudinary
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.dispatch import receiver
from django.test.signals import setting_changed
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
user_settings = getattr(settings, 'CLOUDINARY_STORAGE', {})

def set_credentials--- This code section failed: ---

 L.  17         0  SETUP_FINALLY        22  'to 22'

 L.  18         2  LOAD_GLOBAL              itemgetter
                4  LOAD_STR                 'CLOUD_NAME'
                6  LOAD_STR                 'API_KEY'
                8  LOAD_STR                 'API_SECRET'
               10  CALL_FUNCTION_3       3  ''

 L.  19        12  LOAD_FAST                'user_settings'

 L.  18        14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'credentials'
               18  POP_BLOCK        
               20  JUMP_FORWARD        110  'to 110'
             22_0  COME_FROM_FINALLY     0  '0'

 L.  20        22  DUP_TOP          
               24  LOAD_GLOBAL              KeyError
               26  COMPARE_OP               exception-match
               28  POP_JUMP_IF_FALSE   108  'to 108'
               30  POP_TOP          
               32  POP_TOP          
               34  POP_TOP          

 L.  21        36  LOAD_GLOBAL              os
               38  LOAD_ATTR                environ
               40  LOAD_METHOD              get
               42  LOAD_STR                 'CLOUDINARY_URL'
               44  CALL_METHOD_1         1  ''
               46  POP_JUMP_IF_FALSE    54  'to 54'

 L.  22        48  POP_EXCEPT       
               50  LOAD_CONST               None
               52  RETURN_VALUE     
             54_0  COME_FROM            46  '46'

 L.  23        54  LOAD_GLOBAL              os
               56  LOAD_ATTR                environ
               58  LOAD_METHOD              get
               60  LOAD_STR                 'CLOUDINARY_CLOUD_NAME'
               62  CALL_METHOD_1         1  ''
               64  POP_JUMP_IF_FALSE    96  'to 96'
               66  LOAD_GLOBAL              os
               68  LOAD_ATTR                environ
               70  LOAD_METHOD              get

 L.  24        72  LOAD_STR                 'CLOUDINARY_API_KEY'

 L.  23        74  CALL_METHOD_1         1  ''
               76  POP_JUMP_IF_FALSE    96  'to 96'

 L.  24        78  LOAD_GLOBAL              os
               80  LOAD_ATTR                environ
               82  LOAD_METHOD              get

 L.  25        84  LOAD_STR                 'CLOUDINARY_API_SECRET'

 L.  24        86  CALL_METHOD_1         1  ''

 L.  23        88  POP_JUMP_IF_FALSE    96  'to 96'

 L.  26        90  POP_EXCEPT       
               92  LOAD_CONST               None
               94  RETURN_VALUE     
             96_0  COME_FROM            88  '88'
             96_1  COME_FROM            76  '76'
             96_2  COME_FROM            64  '64'

 L.  28        96  LOAD_GLOBAL              ImproperlyConfigured

 L.  29        98  LOAD_STR                 'In order to use cloudinary storage, you need to provide CLOUDINARY_STORAGE dictionary with CLOUD_NAME, API_SECRET and API_KEY in the settings or set CLOUDINARY_URL variable (or CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET variables).'

 L.  28       100  CALL_FUNCTION_1       1  ''
              102  RAISE_VARARGS_1       1  'exception instance'
              104  POP_EXCEPT       
              106  JUMP_FORWARD        138  'to 138'
            108_0  COME_FROM            28  '28'
              108  END_FINALLY      
            110_0  COME_FROM            20  '20'

 L.  35       110  LOAD_GLOBAL              cloudinary
              112  LOAD_ATTR                config

 L.  36       114  LOAD_FAST                'credentials'
              116  LOAD_CONST               0
              118  BINARY_SUBSCR    

 L.  37       120  LOAD_FAST                'credentials'
              122  LOAD_CONST               1
              124  BINARY_SUBSCR    

 L.  38       126  LOAD_FAST                'credentials'
              128  LOAD_CONST               2
              130  BINARY_SUBSCR    

 L.  35       132  LOAD_CONST               ('cloud_name', 'api_key', 'api_secret')
              134  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              136  POP_TOP          
            138_0  COME_FROM           106  '106'

Parse error at or near `LOAD_CONST' instruction at offset 50


set_credentials(user_settings)
cloudinary.config(secure=(user_settings.get('SECURE', True)))
MEDIA_TAG = user_settings.get('MEDIA_TAG', 'media')
INVALID_VIDEO_ERROR_MESSAGE = user_settings.get('INVALID_VIDEO_ERROR_MESSAGE', 'Please upload a valid video file.')
EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS = user_settings.get('EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS', ())
STATIC_TAG = user_settings.get('STATIC_TAG', 'static')
STATICFILES_MANIFEST_ROOT = user_settings.get('STATICFILES_MANIFEST_ROOT', os.path.join(BASE_DIR, 'manifest'))
STATIC_IMAGES_EXTENSIONS = user_settings.get('STATIC_IMAGES_EXTENSIONS', [
 'jpg',
 'jpe',
 'jpeg',
 'jpc',
 'jp2',
 'j2k',
 'wdp',
 'jxr',
 'hdp',
 'png',
 'gif',
 'webp',
 'bmp',
 'tif',
 'tiff',
 'ico'])
STATIC_VIDEOS_EXTENSIONS = user_settings.get('STATIC_VIDEOS_EXTENSIONS', [
 'mp4',
 'webm',
 'flv',
 'mov',
 'ogv',
 '3gp',
 '3g2',
 'wmv',
 'mpeg',
 'flv',
 'mkv',
 'avi'])
MAGIC_FILE_PATH = user_settings.get('MAGIC_FILE_PATH', 'magic')
PREFIX = user_settings.get('PREFIX', settings.MEDIA_URL)

@receiver(setting_changed)
def reload_settings(*args, **kwargs):
    setting_name, value = kwargs['setting'], kwargs['value']
    if setting_name in ('CLOUDINARY_STORAGE', 'MEDIA_URL'):
        value
        importlib.reload(sys.modules[__name__])