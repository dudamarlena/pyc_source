# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/Documents/Etudes/Doctorat/Australie/code/shwirl/extern/vispy/util/fonts/_quartz.py
# Compiled at: 2016-11-03 01:40:19
import numpy as np
from ctypes import byref, c_int32, c_byte
from ...ext.cocoapy import cf, ct, quartz, CFRange, CFSTR, CGGlyph, UniChar, kCTFontFamilyNameAttribute, kCTFontBoldTrait, kCTFontItalicTrait, kCTFontSymbolicTrait, kCTFontTraitsAttribute, kCTFontAttributeName, kCGImageAlphaPremultipliedLast, kCFNumberSInt32Type, ObjCClass
from ._vispy_fonts import _vispy_fonts, _get_vispy_font_filename
_font_dict = {}

def _load_vispy_font(face, bold, italic):
    fname = _get_vispy_font_filename(face, bold, italic)
    url = cf.CFURLCreateWithFileSystemPath(None, CFSTR(fname), 0, False)
    array = ct.CTFontManagerCreateFontDescriptorsFromURL(url)
    desc = cf.CFArrayGetValueAtIndex(array, 0)
    font = ct.CTFontCreateWithFontDescriptor(desc, 12.0, None)
    cf.CFRelease(array)
    cf.CFRelease(url)
    if not font:
        raise RuntimeError("Couldn't load font: %s" % face)
    key = '%s-%s-%s' % (face, bold, italic)
    _font_dict[key] = font
    return font


def _load_font(face, bold, italic):
    key = '%s-%s-%s' % (face, bold, italic)
    if key in _font_dict:
        return _font_dict[key]
    else:
        if face in _vispy_fonts:
            return _load_vispy_font(face, bold, italic)
        traits = 0
        traits |= kCTFontBoldTrait if bold else 0
        traits |= kCTFontItalicTrait if italic else 0
        args = [
         None, 0, cf.kCFTypeDictionaryKeyCallBacks,
         cf.kCFTypeDictionaryValueCallBacks]
        attributes = cf.CFDictionaryCreateMutable(*args)
        cfname = CFSTR(face)
        cf.CFDictionaryAddValue(attributes, kCTFontFamilyNameAttribute, cfname)
        cf.CFRelease(cfname)
        itraits = c_int32(traits)
        sym_traits = cf.CFNumberCreate(None, kCFNumberSInt32Type, byref(itraits))
        if sym_traits:
            args = [None, 0, cf.kCFTypeDictionaryKeyCallBacks,
             cf.kCFTypeDictionaryValueCallBacks]
            traits_dict = cf.CFDictionaryCreateMutable(*args)
            if traits_dict:
                cf.CFDictionaryAddValue(traits_dict, kCTFontSymbolicTrait, sym_traits)
                cf.CFDictionaryAddValue(attributes, kCTFontTraitsAttribute, traits_dict)
                cf.CFRelease(traits_dict)
            cf.CFRelease(sym_traits)
        desc = ct.CTFontDescriptorCreateWithAttributes(attributes)
        cf.CFRelease(attributes)
        font = ct.CTFontCreateWithFontDescriptor(desc, 12.0, None)
        if not font:
            raise RuntimeError("Couldn't load font: %s" % face)
        _font_dict[key] = font
        return font


def _load_glyph(f, char, glyphs_dict):
    font = _load_font(f['face'], f['bold'], f['italic'])
    args = [
     None, 0, cf.kCFTypeDictionaryKeyCallBacks,
     cf.kCFTypeDictionaryValueCallBacks]
    attributes = cf.CFDictionaryCreateMutable(*args)
    desc = ct.CTFontDescriptorCreateWithAttributes(attributes)
    cf.CFRelease(attributes)
    font = ct.CTFontCreateCopyWithAttributes(font, f['size'], None, desc)
    cf.CFRelease(desc)
    if not font:
        raise RuntimeError("Couldn't load font")
    args = [None, 1, cf.kCFTypeDictionaryKeyCallBacks,
     cf.kCFTypeDictionaryValueCallBacks]
    attributes = cf.CFDictionaryCreateMutable(*args)
    cf.CFDictionaryAddValue(attributes, kCTFontAttributeName, font)
    string = cf.CFAttributedStringCreate(None, CFSTR(char), attributes)
    line = ct.CTLineCreateWithAttributedString(string)
    cf.CFRelease(string)
    cf.CFRelease(attributes)
    chars = (UniChar * 1)(*map(ord, char))
    glyphs = (CGGlyph * 1)()
    ct.CTFontGetGlyphsForCharacters(font, chars, glyphs, 1)
    rect = ct.CTFontGetBoundingRectsForGlyphs(font, 0, glyphs, None, 1)
    advance = ct.CTFontGetAdvancesForGlyphs(font, 1, glyphs, None, 1)
    width = max(int(np.ceil(rect.size.width) + 1), 1)
    height = max(int(np.ceil(rect.size.height) + 1), 1)
    left = rect.origin.x
    baseline = -rect.origin.y
    top = height - baseline
    bits_per_component = 8
    bytes_per_row = 4 * width
    color_space = quartz.CGColorSpaceCreateDeviceRGB()
    args = [None, width, height, bits_per_component, bytes_per_row,
     color_space, kCGImageAlphaPremultipliedLast]
    bitmap = quartz.CGBitmapContextCreate(*args)
    quartz.CGContextSetShouldAntialias(bitmap, True)
    quartz.CGContextSetTextPosition(bitmap, -left, baseline)
    ct.CTLineDraw(line, bitmap)
    cf.CFRelease(line)
    image_ref = quartz.CGBitmapContextCreateImage(bitmap)
    assert quartz.CGImageGetBytesPerRow(image_ref) == bytes_per_row
    data_provider = quartz.CGImageGetDataProvider(image_ref)
    image_data = quartz.CGDataProviderCopyData(data_provider)
    buffer_size = cf.CFDataGetLength(image_data)
    assert buffer_size == width * height * 4
    buffer = (c_byte * buffer_size)()
    byte_range = CFRange(0, buffer_size)
    cf.CFDataGetBytes(image_data, byte_range, buffer)
    quartz.CGImageRelease(image_ref)
    quartz.CGDataProviderRelease(image_data)
    cf.CFRelease(bitmap)
    cf.CFRelease(color_space)
    bitmap = np.array(buffer, np.ubyte)
    bitmap.shape = (height, width, 4)
    bitmap = bitmap[:, :, 3].copy()
    glyph = dict(char=char, offset=(left, top), bitmap=bitmap, advance=advance, kerning={})
    glyphs_dict[char] = glyph
    for other_char, other_glyph in glyphs_dict.items():
        glyph['kerning'][other_char] = _get_k_p_a(font, other_char, char) - other_glyph['advance']
        other_glyph['kerning'][char] = _get_k_p_a(font, char, other_char) - glyph['advance']

    cf.CFRelease(font)
    return


def _get_k_p_a(font, left, right):
    """This actually calculates the kerning + advance"""
    chars = left + right
    args = [None, 1, cf.kCFTypeDictionaryKeyCallBacks,
     cf.kCFTypeDictionaryValueCallBacks]
    attributes = cf.CFDictionaryCreateMutable(*args)
    cf.CFDictionaryAddValue(attributes, kCTFontAttributeName, font)
    string = cf.CFAttributedStringCreate(None, CFSTR(chars), attributes)
    typesetter = ct.CTTypesetterCreateWithAttributedString(string)
    cf.CFRelease(string)
    cf.CFRelease(attributes)
    range = CFRange(0, 1)
    line = ct.CTTypesetterCreateLine(typesetter, range)
    offset = ct.CTLineGetOffsetForStringIndex(line, 1, None)
    cf.CFRelease(line)
    cf.CFRelease(typesetter)
    return offset


def _list_fonts():
    manager = ObjCClass('NSFontManager').sharedFontManager()
    avail = manager.availableFontFamilies()
    fonts = [ avail.objectAtIndex_(ii).UTF8String().decode('utf-8') for ii in range(avail.count())
            ]
    return fonts