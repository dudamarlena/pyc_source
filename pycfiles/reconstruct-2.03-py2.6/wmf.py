# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\formats\graphics\wmf.py
# Compiled at: 2010-05-01 15:45:14
"""
Windows Meta File
"""
from construct import *
wmf_record = Struct('records', ULInt32('size'), Enum(ULInt16('function'), Arc=2071, Chord=2096, Ellipse=1048, ExcludeClipRect=1045, FloodFill=1049, IntersectClipRect=1046, LineTo=531, MoveTo=532, OffsetClipRgn=544, OffsetViewportOrg=529, OffsetWindowOrg=527, PatBlt=1565, Pie=2074, RealizePalette=53, Rectangle=1051, ResizePalette=313, RestoreDC=295, RoundRect=1564, SaveDC=30, ScaleViewportExt=1042, ScaleWindowExt=1024, SetBkColor=513, SetBkMode=258, SetMapMode=259, SetMapperFlags=561, SetPixel=1055, SetPolyFillMode=262, SetROP2=260, SetStretchBltMode=263, SetTextAlign=302, SetTextCharacterExtra=264, SetTextColor=521, SetTextJustification=522, SetViewportExt=526, SetViewportOrg=525, SetWindowExt=524, SetWindowOrg=523, _default_=Pass), Array(lambda ctx: ctx.size - 3, ULInt16('params')))
wmf_placeable_header = Struct('placeable_header', Const(ULInt32('key'), 2596720087), ULInt16('handle'), SLInt16('left'), SLInt16('top'), SLInt16('right'), SLInt16('bottom'), ULInt16('units_per_inch'), Padding(4), ULInt16('checksum'))
wmf_file = Struct('wmf_file', Optional(wmf_placeable_header), Enum(ULInt16('type'), InMemory=0, File=1), Const(ULInt16('header_size'), 9), ULInt16('version'), ULInt32('size'), ULInt16('number_of_objects'), ULInt32('size_of_largest_record'), ULInt16('number_of_params'), GreedyRange(wmf_record))
if __name__ == '__main__':
    obj = wmf_file.parse_stream(open('../../test/wmf1.wmf', 'rb'))
    print obj