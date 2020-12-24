# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/storage.py
# Compiled at: 2020-03-01 07:43:02
# Size of source mod 2**32: 12777 bytes
import errno, json, os
from urllib.parse import unquote, urlsplit, urlunsplit
import cloudinary, cloudinary.api, cloudinary.uploader, requests
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import HashedFilesMixin, ManifestFilesMixin
from django.core.files.base import ContentFile, File
from django.core.files.storage import Storage, FileSystemStorage
from django.core.files.uploadedfile import UploadedFile
from django.utils.deconstruct import deconstructible
from . import app_settings
from .helpers import get_resources_by_path
RESOURCE_TYPES = {'IMAGE':'image', 
 'RAW':'raw', 
 'VIDEO':'video'}

@deconstructible
class MediaCloudinaryStorage(Storage):
    RESOURCE_TYPE = RESOURCE_TYPES['IMAGE']
    TAG = app_settings.MEDIA_TAG

    def __init__(self, tag=None, resource_type=None):
        if tag is not None:
            self.TAG = tag
        if resource_type is not None:
            self.RESOURCE_TYPE = resource_type

    def _get_resource_type(self, name):
        """
        Implemented to allow different resource types per file name
        within one storage class.
        """
        return self.RESOURCE_TYPE

    def _open(self, name, mode='rb'):
        url = self._get_url(name)
        response = requests.get(url)
        if response.status_code == 404:
            raise IOError
        response.raise_for_status()
        file = ContentFile(response.content)
        file.name = name
        file.mode = mode
        return file

    def _upload(self, name, content):
        options = {'use_filename':True, 
         'resource_type':self._get_resource_type(name),  'tags':self.TAG}
        folder = os.path.dirname(name)
        if folder:
            options['folder'] = folder
        return (cloudinary.uploader.upload)(content, **options)

    def _save(self, name, content):
        name = self._normalise_name(name)
        name = self._prepend_prefix(name)
        content = UploadedFile(content, name)
        response = self._upload(name, content)
        return response['public_id']

    def delete(self, name):
        response = cloudinary.uploader.destroy(name, invalidate=True, resource_type=(self._get_resource_type(name)))
        return response['result'] == 'ok'

    def _get_url(self, name):
        name = self._prepend_prefix(name)
        cloudinary_resource = cloudinary.CloudinaryResource(name, default_resource_type=(self._get_resource_type(name)))
        return cloudinary_resource.url

    def url(self, name):
        return self._get_url(name)

    def exists(self, name):
        url = self._get_url(name)
        response = requests.head(url)
        if response.status_code == 404:
            return False
        response.raise_for_status()
        return True

    def size(self, name):
        url = self._get_url(name)
        response = requests.head(url)
        if response.status_code == 200:
            return int(response.headers['content-length'])
        return

    def get_available_name(self, name, max_length=None):
        if max_length is None:
            return name
        return name[:max_length]

    def _normalize_path(self, path):
        if path != '':
            if not path.endswith('/'):
                path += '/'
        return path

    def _get_prefix(self):
        return app_settings.PREFIX

    def _prepend_prefix(self, name):
        prefix = self._get_prefix().lstrip('/')
        prefix = self._normalize_path(prefix)
        if not name.startswith(prefix):
            name = prefix + name
        return name

    def listdir(self, path):
        path = self._normalize_path(path)
        resources = get_resources_by_path(self.RESOURCE_TYPE, self.TAG, path)
        directories = set()
        files = []
        for resource in resources:
            resource_tail = resource.replace(path, '', 1)
            if '/' in resource_tail:
                directory = resource_tail.split('/', 1)[0]
                directories.add(directory)
            else:
                files.append(resource_tail)
        else:
            return (
             list(directories), files)

    def _normalise_name(self, name):
        return name.replace('\\', '/')


class RawMediaCloudinaryStorage(MediaCloudinaryStorage):
    RESOURCE_TYPE = RESOURCE_TYPES['RAW']


class VideoMediaCloudinaryStorage(MediaCloudinaryStorage):
    RESOURCE_TYPE = RESOURCE_TYPES['VIDEO']


storages_per_type = {RESOURCE_TYPES['IMAGE']: MediaCloudinaryStorage(), 
 RESOURCE_TYPES['RAW']: RawMediaCloudinaryStorage(), 
 RESOURCE_TYPES['VIDEO']: VideoMediaCloudinaryStorage()}

class StaticCloudinaryStorage(MediaCloudinaryStorage):
    __doc__ = '\n    Base storage for staticfiles kept in Cloudinary.\n    Uploads only unhashed files, so it is highly unrecommended to use it directly,\n    because static files are cached both by Cloudinary CDN and browsers\n    and changing files could become problematic.\n    '
    RESOURCE_TYPE = RESOURCE_TYPES['RAW']
    TAG = app_settings.STATIC_TAG

    def _get_resource_type(self, name):
        """
        Implemented as static files can be of different resource types.
        Because web developers are the people who control those files, we can distinguish them
        simply by looking at their extensions, we don't need any content based validation.
        """
        extension = self._get_file_extension(name)
        if extension is None:
            return self.RESOURCE_TYPE
        if extension in app_settings.STATIC_IMAGES_EXTENSIONS:
            return RESOURCE_TYPES['IMAGE']
        if extension in app_settings.STATIC_VIDEOS_EXTENSIONS:
            return RESOURCE_TYPES['VIDEO']
        return self.RESOURCE_TYPE

    @staticmethod
    def _get_file_extension(name):
        substrings = name.split('.')
        if len(substrings) == 1:
            return
        return substrings[(-1)].lower()

    def url(self, name):
        if settings.DEBUG:
            return settings.STATIC_URL + name
        return super(StaticCloudinaryStorage, self).url(name)

    def _upload(self, name, content):
        resource_type = self._get_resource_type(name)
        name = self._remove_extension_for_non_raw_file(name)
        return cloudinary.uploader.upload(content, public_id=name, resource_type=resource_type, invalidate=True,
          tags=(self.TAG))

    def _remove_extension_for_non_raw_file(self, name):
        """
        Implemented as image and video files' Cloudinary public id
        shouldn't contain file extensions, otherwise Cloudinary url
        would contain doubled extension - Cloudinary adds extension to url
        to allow file conversion to arbitrary file, like png to jpg.
        """
        file_resource_type = self._get_resource_type(name)
        if file_resource_type is None or file_resource_type == self.RESOURCE_TYPE:
            return name
        extension = self._get_file_extension(name)
        return name[:-len(extension) - 1]

    file_hash = HashedFilesMixin.file_hash
    clean_name = HashedFilesMixin.clean_name

    def _exists_with_etag(self, name, content):
        """
        Checks whether a file with a name and a content is already uploaded to Cloudinary.
        Uses ETAG header and MD5 hash for the content comparison.
        """
        url = self._get_url(name)
        response = requests.head(url)
        if response.status_code == 404:
            return False
        etag = response.headers['ETAG'].split('"')[1]
        hash = self.file_hash(name, content)
        return etag.startswith(hash)

    def _save(self, name, content):
        name = self.clean_name(name)
        if not self._exists_with_etag(name, content):
            content.seek(0)
            super(StaticCloudinaryStorage, self)._save(name, content)
        return self._prepend_prefix(name)

    def _get_prefix(self):
        return settings.STATIC_URL

    def listdir(self, path):
        """
        Not implemented as static assets can be of different resource types
        in contrast to media storages, which are specialized per given resource type.
        That's why we cannot use parent's class listdir.
        This method could be implemented in the future if there is a demand for it.
        """
        raise NotImplementedError()

    def stored_name(self, name):
        """
        Implemented to standardize interface
        for StaticCloudinaryStorage and StaticHashedCloudinaryStorage
        """
        return self._prepend_prefix(name)


class ManifestCloudinaryStorage(FileSystemStorage):
    __doc__ = '\n    Storage for manifest file which will keep map of hashed paths.\n    Subclasses FileSystemStorage, so the manifest file is kept locally.\n    It is highly recommended to keep the manifest in your version control system,\n    then you are guaranteed the manifest will be used in all production environment,\n    including Heroku and AWS Elastic Beanstalk.\n    '

    def __init__(self, location=None, base_url=None, *args, **kwargs):
        location = app_settings.STATICFILES_MANIFEST_ROOT if location is None else location
        (super(ManifestCloudinaryStorage, self).__init__)(location, base_url, *args, **kwargs)


class HashCloudinaryMixin(object):

    def __init__(self, *args, **kwargs):
        self.manifest_storage = ManifestCloudinaryStorage()
        (super(HashCloudinaryMixin, self).__init__)(*args, **kwargs)

    def hashed_name(self, name, content=None, filename=None):
        parsed_name = urlsplit(unquote(name))
        clean_name = parsed_name.path.strip()
        opened = False
        if content is None:
            absolute_path = finders.find(clean_name)
            try:
                content = open(absolute_path, 'rb')
            except (IOError, OSError) as e:
                try:
                    if e.errno == errno.ENOENT:
                        raise ValueError("The file '%s' could not be found with %r." % (clean_name, self))
                    else:
                        raise
                finally:
                    e = None
                    del e

            else:
                content = File(content)
                opened = True
        try:
            file_hash = self.file_hash(clean_name, content)
        finally:
            if opened:
                content.close()

        path, filename = os.path.split(clean_name)
        root, ext = os.path.splitext(filename)
        if file_hash is not None:
            file_hash = '.%s' % file_hash
        hashed_name = os.path.join(path, '%s%s%s' % (root, file_hash, ext))
        unparsed_name = list(parsed_name)
        unparsed_name[2] = hashed_name
        if '?#' in name:
            if not unparsed_name[3]:
                unparsed_name[2] += '?'
        return urlunsplit(unparsed_name)

    def post_process(self, paths, dry_run=False, **options):
        original_exists = self.exists
        self.exists = lambda name: False
        for response in (super(HashCloudinaryMixin, self).post_process)(paths, dry_run, **options):
            (yield response)
        else:
            self.exists = original_exists

    def read_manifest--- This code section failed: ---

 L. 318         0  SETUP_FINALLY        56  'to 56'

 L. 319         2  LOAD_FAST                'self'
                4  LOAD_ATTR                manifest_storage
                6  LOAD_METHOD              open
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                manifest_name
               12  CALL_METHOD_1         1  ''
               14  SETUP_WITH           46  'to 46'
               16  STORE_FAST               'manifest'

 L. 320        18  LOAD_FAST                'manifest'
               20  LOAD_METHOD              read
               22  CALL_METHOD_0         0  ''
               24  LOAD_METHOD              decode
               26  LOAD_STR                 'utf-8'
               28  CALL_METHOD_1         1  ''
               30  POP_BLOCK        
               32  ROT_TWO          
               34  BEGIN_FINALLY    
               36  WITH_CLEANUP_START
               38  WITH_CLEANUP_FINISH
               40  POP_FINALLY           0  ''
               42  POP_BLOCK        
               44  RETURN_VALUE     
             46_0  COME_FROM_WITH       14  '14'
               46  WITH_CLEANUP_START
               48  WITH_CLEANUP_FINISH
               50  END_FINALLY      
               52  POP_BLOCK        
               54  JUMP_FORWARD         78  'to 78'
             56_0  COME_FROM_FINALLY     0  '0'

 L. 321        56  DUP_TOP          
               58  LOAD_GLOBAL              IOError
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE    76  'to 76'
               64  POP_TOP          
               66  POP_TOP          
               68  POP_TOP          

 L. 322        70  POP_EXCEPT       
               72  LOAD_CONST               None
               74  RETURN_VALUE     
             76_0  COME_FROM            62  '62'
               76  END_FINALLY      
             78_0  COME_FROM            54  '54'

Parse error at or near `ROT_TWO' instruction at offset 32

    def add_unix_path_keys_to_paths(self, paths):
        for path in paths.copy():
            if '\\' in path:
                clean_path = self.clean_name(path)
                paths[clean_path] = paths[path]

    def save_manifest(self):
        payload = {'paths':self.hashed_files, 
         'version':self.manifest_version}
        if os.name == 'nt':
            paths = payload['paths']
            self.add_unix_path_keys_to_paths(paths)
        if self.manifest_storage.exists(self.manifest_name):
            self.manifest_storage.delete(self.manifest_name)
        contents = json.dumps(payload).encode('utf-8')
        self.manifest_storage._save(self.manifest_name, ContentFile(contents))

    stored_name = HashedFilesMixin.stored_name


class StaticHashedCloudinaryStorage(HashCloudinaryMixin, ManifestFilesMixin, StaticCloudinaryStorage):
    pass