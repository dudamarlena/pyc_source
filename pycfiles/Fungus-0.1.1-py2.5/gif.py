# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/image/codecs/gif.py
# Compiled at: 2009-02-07 06:48:49
"""Read GIF control data.

http://www.w3.org/Graphics/GIF/spec-gif89a.txt
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: gif.py 1938 2008-03-21 11:47:05Z Alex.Holkner $'
import struct
from pyglet.image.codecs import ImageDecodeException

class GIFStream(object):

    def __init__(self):
        self.images = []


class GIFImage(object):
    delay = None


class GraphicsScope(object):
    delay = None


LABEL_EXTENSION_INTRODUCER = 33
LABEL_GRAPHIC_CONTROL_EXTENSION = 249
LABEL_IMAGE_DESCRIPTOR = 44
LABEL_TRAILER = 59

def unpack(format, file):
    size = struct.calcsize(format)
    data = file.read(size)
    if len(data) < size:
        raise ImageDecodeException('Unexpected EOF')
    return struct.unpack(format, data)


def read_byte(file):
    data = file.read(1)
    if not len(data):
        raise ImageDecodeException('Unexpected EOF')
    return ord(data)


def read(file):
    """Read a GIF file stream.

    :rtype: GIFStream
    """
    signature = file.read(3)
    version = file.read(3)
    if signature != 'GIF':
        raise ImageDecodeException('Not a GIF stream')
    stream = GIFStream()
    (logical_screen_width, logical_screen_height, fields, background_color_index, pixel_aspect_ratio) = unpack('HHBBB', file)
    global_color_table_flag = fields & 128
    global_color_table_size = fields & 7
    if global_color_table_flag:
        global_color_table = file.read(6 << global_color_table_size)
    graphics_scope = GraphicsScope()
    block_type = read_byte(file)
    while block_type != LABEL_TRAILER:
        if block_type == LABEL_IMAGE_DESCRIPTOR:
            read_table_based_image(file, stream, graphics_scope)
            graphics_scope = GraphicsScope()
        elif block_type == LABEL_EXTENSION_INTRODUCER:
            extension_block_type = read_byte(file)
            if extension_block_type == LABEL_GRAPHIC_CONTROL_EXTENSION:
                read_graphic_control_extension(file, stream, graphics_scope)
            else:
                skip_data_sub_blocks(file)
        else:
            print block_type
        block_type = read_byte(file)

    return stream


def skip_data_sub_blocks(file):
    block_size = read_byte(file)
    while block_size != 0:
        data = file.read(block_size)
        block_size = read_byte(file)


def read_table_based_image(file, stream, graphics_scope):
    gif_image = GIFImage()
    stream.images.append(gif_image)
    gif_image.delay = graphics_scope.delay
    (image_left_position, image_top_position, image_width, image_height, fields) = unpack('HHHHB', file)
    local_color_table_flag = fields & 128
    local_color_table_size = fields & 7
    if local_color_table_flag:
        local_color_table = file.read(6 << local_color_table_size)
    lzw_code_size = file.read(1)
    skip_data_sub_blocks(file)


def read_graphic_control_extension(file, stream, graphics_scope):
    (block_size, fields, delay_time, transparent_color_index, terminator) = unpack('BBHBB', file)
    if block_size != 4:
        raise ImageFormatException('Incorrect block size')
    if delay_time:
        if delay_time <= 1:
            delay_time = 10
        graphics_scope.delay = float(delay_time) / 100