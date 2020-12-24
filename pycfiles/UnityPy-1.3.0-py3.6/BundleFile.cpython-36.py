# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\files\BundleFile.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 11291 bytes
from .File import File
from .SerializedFile import SerializedFile
from ..enums import FileType
from ..helpers import CompressionHelper, ImportHelper
from ..streams import EndianBinaryReader, EndianBinaryWriter

class BundleFile(File):
    format: int
    version_player: str
    version_engine: str

    def __init__(self, reader: EndianBinaryReader, environment=None):
        self.files = {}
        self.signature = reader.read_string_to_null()
        self.format = reader.read_int()
        self.version_player = reader.read_string_to_null()
        self.version_engine = reader.read_string_to_null()
        if self.format == 6:
            self.read_format_6(reader, self.signature != 'UnityFS')
        else:
            if self.signature in ('UnityWeb', 'UnityRaw', 'úúúúúúúú'):
                if self.format < 6:
                    bundle_size = reader.read_int()
                dummy2 = reader.read_short()
                offset = reader.read_short()
                if self.signature in ('UnityWeb', 'úúúúúúúú'):
                    dummy3 = reader.read_int()
                    lzma_chunks = reader.read_int()
                    reader.Position = reader.Position + (lzma_chunks - 1) * 8
                    lzma_size = reader.read_int()
                    stream_size = reader.read_int()
                    reader.Position = offset
                    lzma_buffer = reader.read_bytes(lzma_size)
                    data_reader = EndianBinaryReader(CompressionHelper.decompress_lzma(lzma_buffer))
                    self.get_assets_files(data_reader, 0)
                else:
                    if self.signature == 'UnityRaw':
                        reader.Position = offset
                        self.get_assets_files(reader, offset)
            else:
                raise ValueError(f"unknown combination of format ({self.format}) & signature ({self.signature})")
        for name, item in self.files.items():
            if name.endswith(('.resS', '.resource', '.config', '.xml', '.dat')):
                environment.resources[name] = item
            else:
                typ, _ = ImportHelper.check_file_type(item)
                if typ == FileType.AssetsFile:
                    item.Position = 0
                    sf = SerializedFile(item, environment, self)
                    sf.flag = item.flag
                    self.files[name] = sf
                    environment.assets[name] = sf
                else:
                    environment.resources[name] = item

    def get_assets_files(self, reader: EndianBinaryReader, offset):
        file_count = reader.read_int()
        files = [(reader.read_string_to_null(), reader.read_int(), reader.read_int()) for _ in range(file_count)]
        for name, f_offset, size in files:
            reader.Position = offset + f_offset
            self.files[name] = EndianBinaryReader(reader.read(size))

    def read_format_6(self, reader: EndianBinaryReader, padding):
        bundle_size = reader.read_long()
        compressed_size = reader.read_int()
        uncompressed_size = reader.read_int()
        flag = reader.read_int()
        if padding:
            reader.read_byte()
        else:
            if flag & 128 != 0:
                position = reader.Position
                reader.Position = reader.Length - compressed_size
                block_info_bytes = reader.read_bytes(compressed_size)
                reader.Position = position
            else:
                block_info_bytes = reader.read_bytes(compressed_size)
            switch = flag & 63
            if switch == 1:
                blocks_info_data = CompressionHelper.decompress_lzma(block_info_bytes)
            else:
                if switch in (2, 3):
                    blocks_info_data = CompressionHelper.decompress_lz4(block_info_bytes, uncompressed_size)
                else:
                    blocks_info_data = block_info_bytes
        blocks_info_reader = EndianBinaryReader(blocks_info_data)
        blocks_info_reader.Position = 16
        block_count = blocks_info_reader.read_int()
        block_infos = [BlockInfo(blocks_info_reader) for _ in range(block_count)]
        data = []
        for block_info in block_infos:
            switch = block_info.flag & 63
            if switch == 1:
                data.append(CompressionHelper.decompress_lzma(reader.read(block_info.compressed_size)))
            else:
                if switch in (2, 3):
                    data.append(CompressionHelper.decompress_lz4(reader.read(block_info.compressed_size), block_info.uncompressed_size))
                else:
                    data.append(reader.read(block_info.compressed_size))

        data_stream = EndianBinaryReader((b'').join(data))
        entry_info_count = blocks_info_reader.read_int()
        for _ in range(entry_info_count):
            offset = blocks_info_reader.read_long()
            size = blocks_info_reader.read_long()
            flag = blocks_info_reader.read_int()
            name = blocks_info_reader.read_string_to_null()
            data_stream.Position = offset
            item = EndianBinaryReader(data_stream.read(size))
            item.flag = flag
            self.files[name] = item

    def save(self):
        writer = EndianBinaryWriter()
        writer.write_string_to_null(self.signature)
        writer.write_int(self.format)
        writer.write_string_to_null(self.version_player)
        writer.write_string_to_null(self.version_engine)
        if self.format == 6:
            self.save_format_6(writer, self.signature != 'UnityFS')
        else:
            raise NotImplementedError('Not Implemented')
        return writer.bytes

    def save_format_6(self, writer: EndianBinaryWriter, padding=False):
        block_info_flag = 64
        data_flag = 64
        data_writer = EndianBinaryWriter()
        files = [(name, f.flag, data_writer.write_bytes(f.bytes if isinstance(f, EndianBinaryReader) else f.save())) for name, f in self.files.items()]
        file_data = data_writer.bytes
        data_writer.dispose()
        uncompressed_data_size = len(file_data)
        switch = data_flag & 63
        if switch == 1:
            file_data = CompressionHelper.compress_lzma(file_data)
        else:
            if switch in (2, 3):
                file_data = CompressionHelper.compress_lz4(file_data)
            else:
                if switch == 4:
                    raise NotImplementedError
                compressed_data_size = len(file_data)
                block_writer = EndianBinaryWriter(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
                block_writer.write_int(1)
                block_writer.write_u_int(uncompressed_data_size)
                block_writer.write_u_int(compressed_data_size)
                block_writer.write_short(data_flag)
                block_writer.write_int(len(files))
                offset = 0
                for f_name, f_flag, f_len in files:
                    block_writer.write_long(offset)
                    block_writer.write_long(f_len)
                    offset += f_len
                    block_writer.write_int(f_flag)
                    block_writer.write_string_to_null(f_name)

                block_data = block_writer.bytes
                block_writer.dispose()
                uncompressed_block_data_size = len(block_data)
                switch = block_info_flag & 63
                if switch == 1:
                    block_data = CompressionHelper.compress_lzma(block_data)
                else:
                    if switch in (2, 3):
                        block_data = CompressionHelper.compress_lz4(block_data)
                    elif switch == 4:
                        raise NotImplementedError
        compressed_block_data_size = len(block_data)
        writer.write_long(writer.Length + 8 + 4 + 4 + 4 + (1 if padding else 0) + compressed_block_data_size + compressed_data_size)
        writer.write_int(compressed_block_data_size)
        writer.write_int(uncompressed_block_data_size)
        writer.write_int(block_info_flag)
        if padding:
            writer.write_boolean(padding)
        else:
            if block_info_flag & 128 != 0:
                writer.write(file_data)
                writer.write(block_data)
            else:
                writer.write(block_data)
                writer.write(file_data)


class BlockInfo:
    compressed_size: int
    uncompressed_size: int
    flag: int

    def __init__(self, reader: EndianBinaryReader):
        self.uncompressed_size = reader.read_u_int()
        self.compressed_size = reader.read_u_int()
        self.flag = reader.read_short()