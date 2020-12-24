# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ivi/agilent/hprtl.py
# Compiled at: 2014-04-16 18:42:56
"""

Python Interchangeable Virtual Instrument Library

Copyright (c) 2012-2014 Alex Forencich

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""
import io, struct, numpy as np

def parse_hprtl(rtl_file):
    """Convert HP Raster Transfer Language (RTL) to numpy array"""
    color = 1
    width = 0
    byte_width = 0
    height = 0
    compression = 0
    current_row = 0
    plane_cnt = 1
    current_plane = 0
    resolution = 1
    plane_data = None
    in_raster = False
    red = 0
    green = 0
    blue = 0
    color_list = [
     (255, 255, 255),
     (0, 0, 0)]
    if type(rtl_file) == str:
        rtlf = open(rtl_file, 'rb')
    else:
        rtlf = rtl_file
    while True:
        s = rtlf.read(1)
        if len(s) == 0:
            break
        if s[0] != 27:
            continue
        s = rtlf.read(1)
        if len(s) == 0:
            break
        if s[0] == ord('*'):
            cmd = rtlf.read(2)
            while True:
                if (cmd[(-1)] < ord('0') or cmd[(-1)] > ord('9')) and cmd[(-1)] != ord('-'):
                    break
                s = rtlf.read(1)
                if s[0] != 0:
                    cmd += s

            ca = cmd[0]
            cb = cmd[(-1)]
            if ca == ord('r') and (cb == ord('u') or cb == ord('U')):
                color = int(cmd[1:-1])
                if color == -4:
                    plane_cnt = 4
                    color_list = [
                     (255, 255, 255),
                     (127, 127, 127),
                     (0, 255, 255),
                     (0, 127, 127),
                     (255, 0, 255),
                     (127, 0, 127),
                     (0, 0, 255),
                     (0, 0, 127),
                     (255, 255, 0),
                     (127, 127, 0),
                     (0, 255, 0),
                     (0, 127, 0),
                     (255, 0, 0),
                     (127, 0, 0),
                     (63, 63, 63),
                     (0, 0, 0)]
                elif color == -3:
                    plane_cnt = 3
                    color_list = [
                     (255, 255, 255),
                     (0, 255, 255),
                     (255, 0, 255),
                     (0, 0, 255),
                     (255, 255, 0),
                     (0, 255, 0),
                     (255, 0, 0),
                     (0, 0, 0)]
                elif color == 1:
                    plane_cnt = 1
                    color_list = [
                     (255, 255, 255),
                     (0, 0, 0)]
                elif color == 3:
                    plane_cnt = 3
                    color_list = [
                     (0, 0, 0),
                     (255, 0, 0),
                     (0, 255, 0),
                     (255, 255, 0),
                     (0, 0, 255),
                     (255, 0, 255),
                     (0, 255, 255),
                     (255, 255, 255)]
                elif color == 4:
                    plane_cnt = 4
                    color_list = [
                     (0, 0, 0),
                     (0, 0, 0),
                     (127, 0, 0),
                     (255, 0, 0),
                     (0, 127, 0),
                     (0, 255, 0),
                     (127, 127, 0),
                     (255, 255, 0),
                     (0, 0, 127),
                     (0, 0, 255),
                     (127, 0, 127),
                     (255, 0, 255),
                     (0, 127, 127),
                     (0, 255, 255),
                     (127, 127, 127),
                     (255, 255, 255)]
                else:
                    raise Exception('Invalid color')
            elif ca == ord('r') and (cb == ord('a') or cb == ord('A')):
                if in_raster:
                    in_raster = False
                if height == 0:
                    in_raster = True
            elif ca == ord('r') and (cb == ord('c') or cb == ord('C')):
                in_raster = False
            elif ca == ord('r') and (cb == ord('b') or cb == ord('B')):
                pass
            elif ca == ord('r') and (cb == ord('s') or cb == ord('S')):
                width = int(cmd[1:-1])
                byte_width = int((width + 7) / 8)
            elif ca == ord('r') and (cb == ord('t') or cb == ord('T')):
                pass
            elif ca == ord('b') and (cb == ord('m') or cb == ord('M')):
                compression = int(cmd[1:-1])
            elif ca == ord('t') and (cb == ord('r') or cb == ord('R')):
                resolution = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('a') or cb == ord('A')):
                red = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('b') or cb == ord('B')):
                green = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('c') or cb == ord('C')):
                blue = int(cmd[1:-1])
            elif ca == ord('v') and (cb == ord('i') or cb == ord('I')):
                ind = int(cmd[1:-1])
                color_list[ind] = (red, green, blue)
            elif ca == ord('b') and (cb == ord('v') or cb == ord('V') or cb == ord('w') or cb == ord('W')):
                l = int(cmd[1:-1])
                d = rtlf.read(l)
                if not in_raster:
                    continue
                if width == 0:
                    width = l * 8
                if byte_width == 0:
                    byte_width = l
                if current_plane == 0:
                    if height == 0:
                        plane_data = np.zeros((10, byte_width, plane_cnt), dtype=np.uint8)
                    height += 1
                    if height >= plane_data.shape[0]:
                        plane_data = np.append(plane_data, np.zeros((10, byte_width, plane_cnt), dtype=np.uint8), 0)
                if compression == 0 or compression == 1:
                    x = 0
                    for b in d:
                        plane_data[(height - 1)][x][current_plane] = b
                        x += 1

                elif compression == 2:
                    k = 0
                    x = 0
                    while True:
                        if len(d) <= k:
                            break
                        h = d[k]
                        k += 1
                        if h == 128:
                            continue
                        if h < 128:
                            for j in range(h + 1):
                                b = d[k]
                                k += 1
                                plane_data[(height - 1)][x][current_plane] = b
                                x += 1

                        if h > 128:
                            b = d[k]
                            k += 1
                            for j in range(257 - h):
                                plane_data[(height - 1)][x][current_plane] = b
                                x += 1

                else:
                    raise Exception('Invalid compression')
                if plane_cnt > 0:
                    current_plane += 1
                    if current_plane == plane_cnt or cb == ord('w') or cb == ord('W'):
                        current_plane = 0

    plane_data = np.unpackbits(plane_data, axis=1)
    plane_data = plane_data[0:height, 0:width, :]
    plane_data = np.right_shift(np.packbits(plane_data, axis=2), 8 - plane_cnt)
    rgb_data = np.zeros((height, width, 3), dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            rgb_data[y][x] = color_list[plane_data[y][x][0]]

    plane_data = rgb_data
    return plane_data


def generate_bmp(img_data):
    """Generate a BMP format image from a numpy array"""
    bmp = io.BytesIO()
    width = img_data.shape[1]
    height = img_data.shape[0]
    if img_data.shape[2] == 1:
        bpp = 1
        color_table_entries = 2
    else:
        bpp = 24
        color_table_entries = 0
    row_size = int((bpp * width + 31) / 32) * 4
    image_size = row_size * height
    header_size = 54
    color_table_size = color_table_entries * 4
    image_offset = header_size + color_table_size
    file_size = image_offset + image_size
    bmp.write('BM')
    bmp.write(struct.pack('<L', file_size))
    bmp.write(struct.pack('<H', 0))
    bmp.write(struct.pack('<H', 0))
    bmp.write(struct.pack('<L', image_offset))
    bmp.write(struct.pack('<L', 40))
    bmp.write(struct.pack('<l', width))
    bmp.write(struct.pack('<l', height))
    bmp.write(struct.pack('<H', 1))
    bmp.write(struct.pack('<H', bpp))
    bmp.write(struct.pack('<L', 0))
    bmp.write(struct.pack('<L', image_size))
    bmp.write(struct.pack('<L', 1))
    bmp.write(struct.pack('<L', 1))
    bmp.write(struct.pack('<L', color_table_entries))
    bmp.write(struct.pack('<L', 0))
    if img_data.shape[2] == 1:
        bmp.write(struct.pack('<BBBx', 255, 255, 255))
        bmp.write(struct.pack('<BBBx', 0, 0, 0))
        plane_data = np.packbits(img_data, axis=1)
        for y in range(plane_data.shape[0] - 1, -1, -1):
            for x in range(plane_data.shape[1]):
                bmp.write(struct.pack('<B', plane_data[y][x][0]))

            if plane_data.shape[1] % 4 > 0:
                for x in range(4 - plane_data.shape[1] % 4):
                    bmp.write('\x00')

    else:
        for y in range(img_data.shape[0] - 1, -1, -1):
            for x in range(img_data.shape[1]):
                bmp.write(struct.pack('<BBB', img_data[y][x][2], img_data[y][x][1], img_data[y][x][0]))

            if img_data.shape[1] * 3 % 4 > 0:
                for x in range(4 - img_data.shape[1] * 3 % 4):
                    bmp.write('\x00')

    return bmp.getvalue()