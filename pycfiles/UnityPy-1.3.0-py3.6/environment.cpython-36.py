# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\environment.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 4145 bytes
import io, os
from zipfile import ZipFile
from . import files
from .enums import FileType
from .helpers import ImportHelper

class Environment:
    files: dict
    resources: dict
    container: dict
    assets: dict
    path: str

    def __init__(self, *args):
        self.files = {}
        self.container = {}
        self.assets = {}
        self.resources = {}
        self.path = '.'
        if args:
            for arg in args:
                if isinstance(arg, str):
                    if os.path.isfile(arg):
                        if os.path.splitext(arg)[(-1)] in ('.apk', '.zip'):
                            self.load_zip_file(arg)
                        else:
                            self.path = os.path.dirname(arg)
                            self.load_file(arg)
                    elif os.path.isdir(arg):
                        self.path = arg
                        self.load_folder(arg)
                else:
                    self.path = None
                    self.load_file(data=arg)

        if len(self.files) == 1:
            self.file = list(self.files.values())[0]

    def load_files(self, files: list):
        """Loads all files (list) into the AssetsManager and merges .split files for common usage."""
        path = os.path.dirname(files[0])
        ImportHelper.merge_split_assets(path)
        to_read_file = ImportHelper.processing_split_files(files)
        self.load(to_read_file)

    def load_folder(self, path: str):
        """Loads all files in the given path and its subdirs into the AssetsManager."""
        ImportHelper.merge_split_assets(path, True)
        files = ImportHelper.list_all_files(path)
        to_read_file = ImportHelper.processing_split_files(files)
        self.load(to_read_file)

    def load(self, files: list):
        """Loads all files into the AssetsManager."""
        for f in files:
            self.load_file(f)

    def load_file(self, full_name: str='', data=None):
        typ, reader = ImportHelper.check_file_type(data if data else full_name)
        if not full_name:
            full_name = str(data[:256])
        if typ == FileType.AssetsFile:
            self.files[full_name] = files.SerializedFile(reader, self)
            self.assets[full_name] = self.files[full_name]
        else:
            if typ == FileType.BundleFile:
                self.files[full_name] = files.BundleFile(reader, self)
            else:
                if typ == FileType.WebFile:
                    self.files[full_name] = files.WebFile(reader, self)
                else:
                    if typ == FileType.ZIP:
                        self.load_zip_file(reader.stream)
                    elif typ == FileType.ResourceFile:
                        self.resources[os.path.basename(full_name)] = reader

    def load_zip_file(self, value):
        buffer = None
        if isinstance(value, str):
            if os.path.exists(value):
                buffer = open(value, 'rb')
        if isinstance(value, (bytes, bytearray)):
            buffer = ZipFile(io.BytesIO(value))
        else:
            if isinstance(value, (io.BufferedReader, io.BufferedIOBase)):
                buffer = value
        z = ZipFile(buffer)
        for path in z.namelist():
            self.load_file(path, z.open(path).read())

    @property
    def objects(self):

        def search(item):
            ret = []
            print(type(item))
            if not isinstance(item, Environment):
                if getattr(item, 'objects', None):
                    return [val for val in item.objects.values()]
            if getattr(item, 'files', None):
                for item in item.files.values():
                    ret.extend(search(item))

                return ret
            else:
                return ret

        return search(self)