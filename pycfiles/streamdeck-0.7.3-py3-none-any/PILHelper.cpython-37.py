# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Dean\Documents\Python\python-elgato-streamdeck\src\StreamDeck\ImageHelpers\PILHelper.py
# Compiled at: 2020-04-11 03:07:55
# Size of source mod 2**32: 2190 bytes
import io

def create_image(deck, background='black'):
    """
    Creates a new PIL Image with the correct image dimensions for the given
    StreamDeck device's keys.

    .. seealso:: See :func:`~PILHelper.to_native_format` method for converting a
                 PIL image instance to the native image format of a given
                 StreamDeck device.

    :param StreamDeck deck: StreamDeck device to generate a compatible image for.
    :param str background: Background color to use, compatible with `PIL.Image.new()`.

    :rtype: PIL.Image
    :return: Created PIL image
    """
    from PIL import Image
    image_format = deck.key_image_format()
    return Image.new('RGB', image_format['size'], background)


def to_native_format(deck, image):
    """
    Converts a given PIL image to the native image format for a StreamDeck,
    suitable for passing to :func:`~StreamDeck.set_key_image`.

    .. seealso:: See :func:`~PILHelper.create_image` method for creating a PIL
                 image instance for a given StreamDeck device.

    :param StreamDeck deck: StreamDeck device to generate a compatible native image for.
    :param PIL.Image image: PIL Image to convert to the native StreamDeck image format

    :rtype: enumerable()
    :return: Image converted to the given StreamDeck's native format
    """
    from PIL import Image
    image_format = deck.key_image_format()
    if image_format['rotation']:
        image = image.rotate(image_format['rotation'])
    if image_format['flip'][0]:
        image = image.transpose(Image.FLIP_LEFT_RIGHT)
    if image_format['flip'][1]:
        image = image.transpose(Image.FLIP_TOP_BOTTOM)
    if image.size != image_format['size']:
        image.thumbnail(image_format['size'])
    compressed_image = io.BytesIO()
    image.save(compressed_image, (image_format['format']), quality=100)
    return compressed_image.getbuffer()