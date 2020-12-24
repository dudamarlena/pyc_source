# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/char2image/char2image.py
# Compiled at: 2017-01-17 22:59:46
# Size of source mod 2**32: 1520 bytes
import sys, numpy, PIL.Image, PIL.ImageDraw, PIL.ImageFont
__all__ = [
 'char_to_image',
 'char_to_image_dict',
 'chars_to_images',
 'filename_to_font']
FOREGROUND_COLOR = 255
BACKGROUND_COLOR = 0

def char_to_image(char, font, *, size):
    empty_image = PIL.Image.new('L', size, color=BACKGROUND_COLOR)
    try:
        image = empty_image.copy()
        PIL.ImageDraw.Draw(image).text((0, 0), char, font=font, fill=FOREGROUND_COLOR)
        return numpy.array(image, dtype=numpy.uint8)
    except UnicodeEncodeError:
        print('Could not render the unicode character \\u{:04X}'.format(ord(char)), file=sys.stderr)
        return


def char_to_image_dict(chars, font):
    size = tuple(map(max, zip(*[font.getsize(char) for char in chars])))
    pairs = {char:char_to_image(char, font, size=size) for char in chars}
    return {char:image.tolist() for char, image in pairs.items() if image is not None and (image != BACKGROUND_COLOR).any() if image is not None and (image != BACKGROUND_COLOR).any()}


def chars_to_images(chars, font, unknown_char='�'):
    char_to_image = char_to_image_dict(set(chars), font)
    return [char_to_image[char] if char in char_to_image else char_to_image[unknown_char] for char in chars]


def filename_to_font(filename, size):
    return PIL.ImageFont.truetype(filename, size=size)