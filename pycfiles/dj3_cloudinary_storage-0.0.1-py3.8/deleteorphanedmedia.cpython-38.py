# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/management/commands/deleteorphanedmedia.py
# Compiled at: 2020-03-01 07:43:02
# Size of source mod 2**32: 4743 bytes
from itertools import chain
import django.apps as apps
from django.core.management.base import BaseCommand
from django.db import models
from cloudinary_storage import app_settings
from cloudinary_storage.helpers import get_resources
from cloudinary_storage.storage import storages_per_type, RESOURCE_TYPES

class Command(BaseCommand):
    help = 'Removes all orphaned media files'
    TAG = app_settings.MEDIA_TAG

    def add_arguments(self, parser):
        parser.add_argument('--noinput', action='store_true', dest='no_input', help='Do not prompt the user for input of any kind.')

    def set_options(self, **options):
        self.no_input = options['no_input']

    def models(self):
        """
        Gets all registered models.
        """
        return apps.get_models()

    def model_file_fields(self, model):
        """
        Generator yielding all instances of FileField and its subclasses of a model.
        """
        for field in model._meta.fields:
            if isinstance(field, models.FileField):
                (yield field)

    def get_resource_types(self):
        """
        Returns set of resource types of FileFields of all registered models.
        Needed by Cloudinary as resource type is needed to browse or delete specific files.
        """
        resource_types = set()
        for model in self.models():
            for field in self.model_file_fields(model):
                resource_type = field.storage.RESOURCE_TYPE
                resource_types.add(resource_type)
            else:
                return resource_types

    def get_needful_files(self):
        """
        Returns set of media files associated with models.
        Those files won't be deleted.
        """
        needful_files = []
        for model in self.models():
            media_fields = []

        for field in self.model_file_fields(model):
            media_fields.append(field.name)
        else:
            if media_fields:
                exclude_options = {'':media_field for media_field in media_fields}
                model_uploaded_media = ((model.objects.exclude)(**exclude_options).values_list)(*media_fields)
                needful_files.extend(model_uploaded_media)
            return set(chain.from_iterable(needful_files))

    def get_exclude_paths(self):
        storage = storages_per_type[RESOURCE_TYPES['RAW']]
        paths = [storage._prepend_prefix(path) for path in app_settings.EXCLUDE_DELETE_ORPHANED_MEDIA_PATHS]
        return tuple(paths)

    def get_files_to_remove--- This code section failed: ---

 L.  75         0  BUILD_MAP_0           0 
                2  STORE_FAST               'files_to_remove'

 L.  76         4  LOAD_FAST                'self'
                6  LOAD_METHOD              get_needful_files
                8  CALL_METHOD_0         0  ''
               10  STORE_FAST               'needful_files'

 L.  77        12  LOAD_FAST                'self'
               14  LOAD_METHOD              get_uploaded_resources
               16  CALL_METHOD_0         0  ''
               18  GET_ITER         
               20  FOR_ITER             68  'to 68'
               22  UNPACK_SEQUENCE_2     2 
               24  STORE_FAST               'resources_type'
               26  STORE_FAST               'resources'

 L.  78        28  LOAD_FAST                'self'
               30  LOAD_METHOD              get_exclude_paths
               32  CALL_METHOD_0         0  ''
               34  STORE_DEREF              'exclude_paths'

 L.  79        36  LOAD_CLOSURE             'exclude_paths'
               38  BUILD_TUPLE_1         1 
               40  LOAD_SETCOMP             '<code_object <setcomp>>'
               42  LOAD_STR                 'Command.get_files_to_remove.<locals>.<setcomp>'
               44  MAKE_FUNCTION_8          'closure'
               46  LOAD_FAST                'resources'
               48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'resources'

 L.  80        54  LOAD_FAST                'resources'
               56  LOAD_FAST                'needful_files'
               58  BINARY_SUBTRACT  
               60  LOAD_FAST                'files_to_remove'
               62  LOAD_FAST                'resources_type'
               64  STORE_SUBSCR     
               66  JUMP_BACK            20  'to 20'

 L.  81        68  LOAD_FAST                'files_to_remove'
               70  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 40

    def get_uploaded_resources(self):
        for resources_type in self.get_resource_types():
            resources = get_resources(resources_type, self.TAG)
            (yield (resources_type, resources))

    def get_flattened_files_to_remove(self, files):
        result = set()
        for files_per_type in files.values():
            result = result | files_per_type
        else:
            return result

    def delete_orphaned_files(self, files):
        for resource_type, files_per_type in files.items():
            for file in files_per_type:
                self.get_file_storage(resource_type).delete(file)
                self.stdout.write('Deleted {}.'.format(file))

    def get_file_storage(self, resource_type):
        return storages_per_type[resource_type]

    def handle(self, *args, **options):
        (self.set_options)(**options)
        files_to_remove = self.get_files_to_remove()
        flattened_files_to_remove = self.get_flattened_files_to_remove(files_to_remove)
        length = len(flattened_files_to_remove)
        files_to_remove_str = '\n- '.join(flattened_files_to_remove)
        if not length:
            self.stdout.write('There is no file to delete.')
            return None
        else:
            self.stdout.write('{} files will be deleted:\n- {}'.format(length, files_to_remove_str))
            if self.no_input or input("If you are sure to delete them, please type 'yes': ") == 'yes':
                self.delete_orphaned_files(files_to_remove)
                self.stdout.write('{} files have been deleted successfully.'.format(length))
            else:
                self.stdout.write('As ordered, no file has been deleted.')