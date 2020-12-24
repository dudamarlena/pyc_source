# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\files\WebFile.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 4801 bytes
from .BundleFile import BundleFile
from .File import File
from .SerializedFile import SerializedFile
from ..enums import FileType
from ..helpers import CompressionHelper, ImportHelper
from ..streams import EndianBinaryReader, EndianBinaryWriter

class WebFile(File):
    __doc__ = 'A package which can hold other WebFiles, Bundles and SerialiedFiles.\n    It may be compressed via gzip or brotli.\n\n    files -- list of all files in the WebFile\n    '

    def __init__(self, reader: EndianBinaryReader, environment=None):
        """Constructor Method
        """
        self.files = {}
        magic = reader.read_bytes(2)
        reader.Position = 0
        if magic == CompressionHelper.GZIP_MAGIC:
            self.compression = 'gzip'
            data = CompressionHelper.decompress_gzip(reader.bytes)
            reader = EndianBinaryReader(data, endian='<')
        else:
            reader.Position = 32
            magic = reader.read_bytes(6)
            reader.Position = 0
            if CompressionHelper.BROTLI_MAGIC == magic:
                self.compression = 'brotli'
                data = CompressionHelper.decompress_brotli(reader.bytes)
                reader = EndianBinaryReader(data, endian='<')
            else:
                self.compression = 'None'
                reader.endian = '<'
        signature = reader.read_string_to_null()
        if signature != 'UnityWebData1.0':
            return
        self.signature = signature
        head_length = reader.read_int()
        files = []
        while reader.Position < head_length:
            offset = reader.read_int()
            length = reader.read_int()
            path_length = reader.read_int()
            name = reader.read_bytes(path_length).decode('utf8')
            files.append((name, offset, length))

        for name, offset, length in files:
            reader.Position = offset
            data = reader.read(length)
            typ, item = ImportHelper.check_file_type(data)
            if typ == FileType.BundleFile:
                item = BundleFile(item, environment)
            else:
                if typ == FileType.WebFile:
                    item = WebFile(item, environment)
            if typ == FileType.AssetsFile:
                if name.endswith(('.resS', '.resource', '.config', '.xml', '.dat')):
                    environment.resources[name] = item
                else:
                    try:
                        item = SerializedFile(item, environment)
                        environment.assets[name] = item
                    except ValueError:
                        environment.resources[name] = item

            self.files[name] = item
            item.parent = self

    def save(self, files: dict=None, compression: str=None, signature: str='UnityWebData1.0') -> bytes:
        if not files:
            files = self.files
        if not compression:
            compression = self.compression
        files = {name:f.bytes if isinstance(f, EndianBinaryReader) else f.save() for name, f in files.items()}
        writer = EndianBinaryWriter(endian='<')
        writer.write_string_to_null(signature)
        offset = sum([
         writer.Position,
         sum(len(path.encode('utf8')) for path in files.keys()),
         12 * len(files),
         4])
        writer.write_int(offset)
        for name, data in files.items():
            writer.write_int(offset)
            length = len(data)
            writer.write_int(length)
            offset += length
            enc_path = name.encode('utf8')
            writer.write_int(len(enc_path))
            writer.write(enc_path)

        for data in files.values():
            writer.write(data)

        if compression == 'gzip':
            return CompressionHelper.compress_gzip(writer.bytes)
        else:
            if compression == 'brotli':
                return CompressionHelper.compress_brotli(writer.bytes)
            return writer.bytes