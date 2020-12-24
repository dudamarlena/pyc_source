# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/management/commands/deleteredundantstatic.py
# Compiled at: 2020-03-01 07:43:02
# Size of source mod 2**32: 2228 bytes
from django.core.management import CommandError
from cloudinary_storage import app_settings
from cloudinary_storage.storage import StaticHashedCloudinaryStorage, RESOURCE_TYPES
from . import deleteorphanedmedia

class Command(deleteorphanedmedia.Command):
    help = 'Removes redundant static files'
    storage = StaticHashedCloudinaryStorage()
    TAG = app_settings.STATIC_TAG

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--keep-unhashed-files', action='store_true', dest='keep_unhashed_files', help='Keeps used unhashed files untouched. Without it all unhashed files will be always deleted.Use only when you run collectstatic with --upload-unhashed-files option.')

    def set_options(self, **options):
        (super(Command, self).set_options)(**options)
        self.keep_unhashed_files = options['keep_unhashed_files']

    def get_resource_types(self):
        """
        Overwritten as static files can be of any resource type.
        """
        return set(RESOURCE_TYPES.values())

    def get_file_storage(self, resource_type):
        return self.storage

    def get_exclude_paths(self):
        return ()

    def get_needful_files--- This code section failed: ---

 L.  41         0  LOAD_DEREF               'self'
                2  LOAD_ATTR                storage
                4  LOAD_METHOD              load_manifest
                6  CALL_METHOD_0         0  ''
                8  STORE_FAST               'manifest'

 L.  42        10  LOAD_DEREF               'self'
               12  LOAD_ATTR                keep_unhashed_files
               14  POP_JUMP_IF_FALSE    56  'to 56'

 L.  43        16  LOAD_GLOBAL              set
               18  LOAD_FAST                'manifest'
               20  LOAD_METHOD              keys
               22  CALL_METHOD_0         0  ''
               24  LOAD_FAST                'manifest'
               26  LOAD_METHOD              values
               28  CALL_METHOD_0         0  ''
               30  BINARY_OR        
               32  CALL_FUNCTION_1       1  ''
               34  STORE_FAST               'needful_files'

 L.  44        36  LOAD_CLOSURE             'self'
               38  BUILD_TUPLE_1         1 
               40  LOAD_SETCOMP             '<code_object <setcomp>>'
               42  LOAD_STR                 'Command.get_needful_files.<locals>.<setcomp>'
               44  MAKE_FUNCTION_8          'closure'
               46  LOAD_FAST                'needful_files'
               48  GET_ITER         
               50  CALL_FUNCTION_1       1  ''
               52  STORE_FAST               'needful_files'
               54  JUMP_FORWARD         68  'to 68'
             56_0  COME_FROM            14  '14'

 L.  46        56  LOAD_GLOBAL              set
               58  LOAD_FAST                'manifest'
               60  LOAD_METHOD              values
               62  CALL_METHOD_0         0  ''
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'needful_files'
             68_0  COME_FROM            54  '54'

 L.  47        68  LOAD_CLOSURE             'self'
               70  BUILD_TUPLE_1         1 
               72  LOAD_SETCOMP             '<code_object <setcomp>>'
               74  LOAD_STR                 'Command.get_needful_files.<locals>.<setcomp>'
               76  MAKE_FUNCTION_8          'closure'
               78  LOAD_FAST                'needful_files'
               80  GET_ITER         
               82  CALL_FUNCTION_1       1  ''
               84  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_SETCOMP' instruction at offset 40

    def process_file(self, file):
        return self.storage._remove_extension_for_non_raw_file(self.storage._prepend_prefix(file))

    def handle(self, *args, **options):
        if self.storage.read_manifest() is None:
            raise CommandError('Command requires staticfiles.json. Run collectstatic command first and try again.')
        (super(Command, self).handle)(*args, **options)