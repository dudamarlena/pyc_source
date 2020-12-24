# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\UnityPy\classes\Texture2D.py
# Compiled at: 2020-03-30 16:40:06
# Size of source mod 2**32: 5270 bytes
from .Texture import Texture
from ..enums import TextureFormat
from ..export import Texture2DConverter
from ..helpers.ResourceReader import get_resource_data
from ..streams import EndianBinaryWriter

class Texture2D(Texture):

    @property
    def image(self):
        return Texture2DConverter.get_image_from_texture2d(self)

    @image.setter
    def image(self, img):
        writer = EndianBinaryWriter()
        for pix in img.getdata():
            for val in pix:
                writer.write_u_byte(val)

        self.image_data = writer.bytes
        self.m_TextureFormat = TextureFormat.RGBA32 if len(pix) == 4 else TextureFormat.RGB24

    def __init__(self, reader):
        super().__init__(reader=reader)
        version = self.version
        self.m_Width = reader.read_int()
        self.m_Height = reader.read_int()
        self.m_CompleteImageSize = reader.read_int()
        self.m_TextureFormat = TextureFormat(reader.read_int())
        if version[0] < 5 or version[0] == 5 and version[1] < 2:
            self.m_MipMap = reader.read_boolean()
        else:
            self.m_MipCount = reader.read_int()
        self.m_IsReadable = reader.read_boolean()
        self.m_ReadAllowed = reader.read_boolean()
        reader.align_stream()
        if version[0] > 2018 or version[0] == 2018 and version[1] >= 2:
            self.m_StreamingMipmapsPriority = reader.read_int()
        self.m_ImageCount = reader.read_int()
        self.m_TextureDimension = reader.read_int()
        self.m_TextureSettings = GLTextureSettings(reader)
        if version[0] >= 3:
            self.m_LightmapFormat = reader.read_int()
        if version[0] > 3 or version[0] == 3 and version[1] >= 5:
            self.m_ColorSpace = reader.read_int()
        else:
            image_data_size = reader.read_int()
            self.image_data = b''
            if image_data_size == 0:
                if version[0] == 5 and version[1] >= 3 or version[0] > 5:
                    m_StreamData = StreamingInfo(reader)
                    self.image_data = get_resource_data(m_StreamData.path, self.assets_file, m_StreamData.offset, m_StreamData.size)
            self.image_data = reader.read_bytes(image_data_size)

    def save(self, writer=None):
        if writer == None:
            writer = EndianBinaryWriter()
        else:
            version = self.version
            writer.write_int(self.m_Width)
            writer.write_int(self.m_Height)
            writer.write_int(self.m_CompleteImageSize)
            writer.write_int(int(self.m_TextureFormat))
            if version[0] < 5 or version[0] == 5 and version[1] < 2:
                writer.write_boolean(self.m_MipMap)
            else:
                writer.write_int(self.m_MipCount)
            writer.write_boolean(self.m_IsReadable)
            writer.write_boolean(self.m_ReadAllowed)
            writer.align_stream()
            if version[0] > 2018 or version[0] == 2018 and version[1] >= 2:
                writer.write_int(self.m_StreamingMipmapsPriority)
            writer.write_int(self.m_ImageCount)
            writer.write_int(self.m_TextureDimension)
            self.m_TextureSettings.save(writer, version)
            if version[0] >= 3:
                writer.write_int(self.m_LightmapFormat)
            if version[0] > 3 or version[0] == 3 and version[1] >= 5:
                writer.write_int(self.m_ColorSpace)
        writer.write_int(len(self.image_data))
        writer.write_bytes(self.image_data)


class StreamingInfo:
    offset: int = 0
    size: int = 0
    path: str = ''

    def __init__(self, reader):
        self.offset = reader.read_u_int()
        self.size = reader.read_u_int()
        self.path = reader.read_aligned_string()


class GLTextureSettings:

    def __init__(self, reader):
        version = reader.version
        self.m_FilterMode = reader.read_int()
        self.m_Aniso = reader.read_int()
        self.m_MipBias = reader.read_float()
        if version[0] >= 2017:
            self.m_WrapMode = reader.read_int()
            self.m_WrapV = reader.read_int()
            self.m_WrapW = reader.read_int()
        else:
            self.m_WrapMode = reader.read_int()

    def save(self, writer, version):
        writer.write_int(self.self.m_FilterMode)
        writer.write_int(self.self.m_Aniso)
        writer.write_float(self.self.m_MipBias)
        if version[0] >= 2017:
            writer.write_int(self.self.m_WrapMode)
            writer.write_int(self.self.m_WrapV)
            writer.write_int(self.self.m_WrapW)
        else:
            writer.write_int(self.self.m_WrapMode)