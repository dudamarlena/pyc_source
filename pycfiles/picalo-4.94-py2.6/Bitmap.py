# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/pyExcelerator/Bitmap.py
# Compiled at: 2008-03-17 12:58:02
__rev_id__ = '$Id: Bitmap.py,v 1.4 2005/07/20 07:24:11 rvk Exp $'
from BIFFRecords import BiffRecord
from struct import *

def _size_col(sheet, col):
    return sheet.col_width(col)


def _size_row(sheet, row):
    return sheet.row_height(row)


def _position_image(sheet, row_start, col_start, x1, y1, width, height):
    """Calculate the vertices that define the position of the image as required by
    the OBJ record.

             +------------+------------+
             |     A      |      B     |
       +-----+------------+------------+
       |     |(x1,y1)     |            |
       |  1  |(A1)._______|______      |
       |     |    |              |     |
       |     |    |              |     |
       +-----+----|    BITMAP    |-----+
       |     |    |              |     |
       |  2  |    |______________.     |
       |     |            |        (B2)|
       |     |            |     (x2,y2)|
       +---- +------------+------------+

    Example of a bitmap that covers some of the area from cell A1 to cell B2.

    Based on the width and height of the bitmap we need to calculate 8 vars:
        col_start, row_start, col_end, row_end, x1, y1, x2, y2.
    The width and height of the cells are also variable and have to be taken into
    account.
    The values of col_start and row_start are passed in from the calling
    function. The values of col_end and row_end are calculated by subtracting
    the width and height of the bitmap from the width and height of the
    underlying cells.
    The vertices are expressed as a percentage of the underlying cell width as
    follows (rhs values are in pixels):

           x1 = X / W *1024
           y1 = Y / H *256
           x2 = (X-1) / W *1024
           y2 = (Y-1) / H *256

           Where:  X is distance from the left side of the underlying cell
                   Y is distance from the top of the underlying cell
                   W is the width of the cell
                   H is the height of the cell

    Note: the SDK incorrectly states that the height should be expressed as a
    percentage of 1024.

    col_start  - Col containing upper left corner of object
    row_start  - Row containing top left corner of object
    x1  - Distance to left side of object
    y1  - Distance to top of object
    width  - Width of image frame
    height  - Height of image frame
    
    """
    while x1 >= _size_col(sheet, col_start):
        x1 -= _size_col(sheet, col_start)
        col_start += 1

    while y1 >= _size_row(sheet, row_start):
        y1 -= _size_row(sheet, row_start)
        row_start += 1

    row_end = row_start
    col_end = col_start
    width = width + x1 - 1
    height = height + y1 - 1
    while width >= _size_col(sheet, col_end):
        width -= _size_col(sheet, col_end)
        col_end += 1

    while height >= _size_row(sheet, row_end):
        height -= _size_row(sheet, row_end)
        row_end += 1

    if _size_col(sheet, col_start) == 0 or _size_col(sheet, col_end) == 0 or _size_row(sheet, row_start) == 0 or _size_row(sheet, row_end) == 0:
        return
    x1 = float(x1) / _size_col(sheet, col_start) * 1024
    y1 = float(y1) / _size_row(sheet, row_start) * 256
    x2 = float(width) / _size_col(sheet, col_end) * 1024
    y2 = float(height) / _size_row(sheet, row_end) * 256
    return (col_start, x1, row_start, y1, col_end, x2, row_end, y2)


class ObjBmpRecord(BiffRecord):
    _REC_ID = 93

    def __init__(self, row, col, sheet, im_data_bmp, x, y, scale_x, scale_y):
        width = im_data_bmp.width * scale_x
        height = im_data_bmp.height * scale_y
        (col_start, x1, row_start, y1, col_end, x2, row_end, y2) = _position_image(sheet, row, col, x, y, width, height)
        cObj = 1
        OT = 8
        id = 1
        grbit = 1556
        colL = col_start
        dxL = x1
        rwT = row_start
        dyT = y1
        colR = col_end
        dxR = x2
        rwB = row_end
        dyB = y2
        cbMacro = 0
        Reserved1 = 0
        Reserved2 = 0
        icvBack = 9
        icvFore = 9
        fls = 0
        fAuto = 0
        icv = 8
        lns = 255
        lnw = 1
        fAutoB = 0
        frs = 0
        cf = 9
        Reserved3 = 0
        cbPictFmla = 0
        Reserved4 = 0
        grbit2 = 1
        Reserved5 = 0
        data = pack('<L', cObj)
        data += pack('<H', OT)
        data += pack('<H', id)
        data += pack('<H', grbit)
        data += pack('<H', colL)
        data += pack('<H', dxL)
        data += pack('<H', rwT)
        data += pack('<H', dyT)
        data += pack('<H', colR)
        data += pack('<H', dxR)
        data += pack('<H', rwB)
        data += pack('<H', dyB)
        data += pack('<H', cbMacro)
        data += pack('<L', Reserved1)
        data += pack('<H', Reserved2)
        data += pack('<B', icvBack)
        data += pack('<B', icvFore)
        data += pack('<B', fls)
        data += pack('<B', fAuto)
        data += pack('<B', icv)
        data += pack('<B', lns)
        data += pack('<B', lnw)
        data += pack('<B', fAutoB)
        data += pack('<H', frs)
        data += pack('<L', cf)
        data += pack('<H', Reserved3)
        data += pack('<H', cbPictFmla)
        data += pack('<H', Reserved4)
        data += pack('<H', grbit2)
        data += pack('<L', Reserved5)
        self._rec_data = data


def _process_bitmap(bitmap):
    """Convert a 24 bit bitmap into the modified internal format used by Windows.
    This is described in BITMAPCOREHEADER and BITMAPCOREINFO structures in the
    MSDN library.

    """
    fh = file(bitmap, 'rb')
    try:
        data = fh.read()
    finally:
        fh.close()

    if len(data) <= 54:
        raise Exception("bitmap doesn't contain enough data.")
    if data[:2] != 'BM':
        raise Exception("bitmap doesn't appear to to be a valid bitmap image.")
    data = data[2:]
    size = unpack('<L', data[:4])[0]
    size -= 54
    size += 12
    data = data[4:]
    data = data[12:]
    (width, height) = unpack('<LL', data[:8])
    data = data[8:]
    if width > 65535:
        raise Exception('bitmap: largest image width supported is 65k.')
    if height > 65535:
        raise Exception('bitmap: largest image height supported is 65k.')
    (planes, bitcount) = unpack('<HH', data[:4])
    data = data[4:]
    if bitcount != 24:
        raise Exception("bitmap isn't a 24bit true color bitmap.")
    if planes != 1:
        raise Exception('bitmap: only 1 plane supported in bitmap image.')
    compression = unpack('<L', data[:4])[0]
    data = data[4:]
    if compression != 0:
        raise Exception('bitmap: compression not supported in bitmap image.')
    data = data[20:]
    header = pack('<LHHHH', 12, width, height, 1, 24)
    data = header + data
    return (width, height, size, data)


class ImDataBmpRecord(BiffRecord):
    _REC_ID = 127

    def __init__(self, filename):
        """Insert a 24bit bitmap image in a worksheet. The main record required is
        IMDATA but it must be proceeded by a OBJ record to define its position.

        """
        BiffRecord.__init__(self)
        (self.width, self.height, self.size, data) = _process_bitmap(filename)
        cf = 9
        env = 1
        lcb = self.size
        self._rec_data = pack('<HHL', cf, env, lcb) + data