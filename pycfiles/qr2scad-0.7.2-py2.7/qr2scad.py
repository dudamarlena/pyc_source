# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/qr2scad/qr2scad.py
# Compiled at: 2013-07-20 16:53:08
"""qr2scad - Convert QR code images to OpenSCAD
<http://github.com/l0b0/qr2scad>

Default syntax:

qr2scad < input_file

Description:

For each black pixel in the input, it will create a cube in the output.

The result can be used in an existing OpenSCAD file as follows:
1. Remove the QR code from a flat surface using the difference() function.
2. After printing, splash some removable paint or ink on the QR code holes.
3. Remove the residue around the holes with a piece of cloth, leaving the color
in the holes intact.

Examples:

qr2scad < example.png > example.scad
    Convert example.png to example.scad

<http://www.thingiverse.com/thing:4448>

Bugs: <https://github.com/l0b0/qr2scad/issues>
"""
from PIL import Image, ImageOps
from signal import signal, SIGPIPE, SIG_DFL
import sys
BLOCK_SIZE = 1
BLOCK_PADDING = 0.01
BLOCK_SIDE = BLOCK_SIZE - BLOCK_PADDING
PDP_SIDE = 7
signal(SIGPIPE, SIG_DFL)

def qr2scad(stream):
    """Convert black pixels to OpenSCAD cubes."""
    img = Image.open(stream)
    if img.mode != 'L':
        img = img.convert('L')
    img = ImageOps.invert(img)
    bbox = img.getbbox()
    img = img.crop(bbox)
    width, height = img.size
    assert width == height, 'The QR code should be a square, but we found it to be %(w)sx%(h)s' % {'w': width, 
       'h': height}
    qr_side = width
    qr_pixel_size = list(img.getdata()).index(0) / PDP_SIDE
    new_size = qr_side / qr_pixel_size
    img = img.resize((new_size, new_size))
    qr_side = new_size
    img_matrix = img.load()
    result = ''
    result += 'module qr_code() {\n'
    for row in range(qr_side):
        for column in range(qr_side):
            if img_matrix[(column, row)] != 0:
                result += '    translate([%(x)s, %(y)s, 0])' % {'x': BLOCK_SIZE * column - qr_side / 2, 
                   'y': -BLOCK_SIZE * row + qr_side / 2}
                result += ' cube([%(block_side)s, %(block_side)s, 1]);\n' % {'block_side': BLOCK_SIDE}

    result += '}\n'
    result += 'qr_code_size = %d;' % qr_side
    return result


def main(argv=None):
    print qr2scad(sys.stdin)


if __name__ == '__main__':
    sys.exit(main())