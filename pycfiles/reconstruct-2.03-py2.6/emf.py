# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\reconstruct\formats\graphics\emf.py
# Compiled at: 2010-05-01 15:45:14
"""
Enhanced Meta File
"""
from construct import *
record_type = Enum(ULInt32('record_type'), ABORTPATH=68, ANGLEARC=41, ARC=45, ARCTO=55, BEGINPATH=59, BITBLT=76, CHORD=46, CLOSEFIGURE=61, CREATEBRUSHINDIRECT=39, CREATEDIBPATTERNBRUSHPT=94, CREATEMONOBRUSH=93, CREATEPALETTE=49, CREATEPEN=38, DELETEOBJECT=40, ELLIPSE=42, ENDPATH=60, EOF=14, EXCLUDECLIPRECT=29, EXTCREATEFONTINDIRECTW=82, EXTCREATEPEN=95, EXTFLOODFILL=53, EXTSELECTCLIPRGN=75, EXTTEXTOUTA=83, EXTTEXTOUTW=84, FILLPATH=62, FILLRGN=71, FLATTENPATH=65, FRAMERGN=72, GDICOMMENT=70, HEADER=1, INTERSECTCLIPRECT=30, INVERTRGN=73, LINETO=54, MASKBLT=78, MODIFYWORLDTRANSFORM=36, MOVETOEX=27, OFFSETCLIPRGN=26, PAINTRGN=74, PIE=47, PLGBLT=79, POLYBEZIER=2, POLYBEZIER16=85, POLYBEZIERTO=5, POLYBEZIERTO16=88, POLYDRAW=56, POLYDRAW16=92, POLYGON=3, POLYGON16=86, POLYLINE=4, POLYLINE16=87, POLYLINETO=6, POLYLINETO16=89, POLYPOLYGON=8, POLYPOLYGON16=91, POLYPOLYLINE=7, POLYPOLYLINE16=90, POLYTEXTOUTA=96, POLYTEXTOUTW=97, REALIZEPALETTE=52, RECTANGLE=43, RESIZEPALETTE=51, RESTOREDC=34, ROUNDRECT=44, SAVEDC=33, SCALEVIEWPORTEXTEX=31, SCALEWINDOWEXTEX=32, SELECTCLIPPATH=67, SELECTOBJECT=37, SELECTPALETTE=48, SETARCDIRECTION=57, SETBKCOLOR=25, SETBKMODE=18, SETBRUSHORGEX=13, SETCOLORADJUSTMENT=23, SETDIBITSTODEVICE=80, SETMAPMODE=17, SETMAPPERFLAGS=16, SETMETARGN=28, SETMITERLIMIT=58, SETPALETTEENTRIES=50, SETPIXELV=15, SETPOLYFILLMODE=19, SETROP2=20, SETSTRETCHBLTMODE=21, SETTEXTALIGN=22, SETTEXTCOLOR=24, SETVIEWPORTEXTEX=11, SETVIEWPORTORGEX=12, SETWINDOWEXTEX=9, SETWINDOWORGEX=10, SETWORLDTRANSFORM=35, STRETCHBLT=77, STRETCHDIBITS=81, STROKEANDFILLPATH=63, STROKEPATH=64, WIDENPATH=66, _default_=Pass)
generic_record = Struct('records', record_type, ULInt32('record_size'), Union('params', Field('raw', lambda ctx: ctx._.record_size - 8), Array(lambda ctx: (ctx._.record_size - 8) // 4, ULInt32('params'))))
header_record = Struct('header_record', Const(record_type, 'HEADER'), ULInt32('record_size'), SLInt32('bounds_left'), SLInt32('bounds_right'), SLInt32('bounds_top'), SLInt32('bounds_bottom'), SLInt32('frame_left'), SLInt32('frame_right'), SLInt32('frame_top'), SLInt32('frame_bottom'), Const(ULInt32('signature'), 1179469088), ULInt32('version'), ULInt32('size'), ULInt32('num_of_records'), ULInt16('num_of_handles'), Padding(2), ULInt32('description_size'), ULInt32('description_offset'), ULInt32('num_of_palette_entries'), SLInt32('device_width_pixels'), SLInt32('device_height_pixels'), SLInt32('device_width_mm'), SLInt32('device_height_mm'), Pointer(lambda ctx: ctx.description_offset, StringAdapter(Array(lambda ctx: ctx.description_size, Field('description', 2)))), Padding(lambda ctx: ctx.record_size - 88))
emf_file = Struct('emf_file', header_record, Array(lambda ctx: ctx.header_record.num_of_records - 1, generic_record))
if __name__ == '__main__':
    obj = emf_file.parse_stream(open('../../test/emf1.emf', 'rb'))
    print obj