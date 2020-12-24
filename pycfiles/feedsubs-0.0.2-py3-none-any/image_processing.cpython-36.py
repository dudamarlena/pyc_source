# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/reader/image_processing.py
# Compiled at: 2018-10-02 15:58:20
# Size of source mod 2**32: 1995 bytes
from io import BytesIO, SEEK_END
import attr
from PIL import Image
MAX_EDGE_PIXELS = 1024
QUALITY = 80
SUPPORTED_FORMATS = ('JPEG', 'PNG', 'GIF')
MAX_SIZE_IN_BYTES_AFTER_PROCESSING = 1048576
MIN_AREA_TRACKING_PIXEL = 10

@attr.s
class ImageProcessingResult:
    size_in_bytes: int = attr.ib()
    width: int = attr.ib()
    height: int = attr.ib()
    image_format: str = attr.ib()
    data: BytesIO = attr.ib()


class ImageProcessingError(Exception):
    pass


def process_image_data(data: bytes) -> ImageProcessingResult:
    try:
        image = Image.open(BytesIO(data))
    except OSError as e:
        raise ImageProcessingError('Cannot open image: {}'.format(e))

    with image:
        if image.format not in SUPPORTED_FORMATS:
            raise ImageProcessingError('Unsupported format {}'.format(image.format))
        else:
            width, height = image.size
            if width * height < MIN_AREA_TRACKING_PIXEL:
                raise ImageProcessingError('Tracking pixel')
            if image.format == 'GIF':
                data = BytesIO(data)
            else:
                try:
                    image.thumbnail((MAX_EDGE_PIXELS, MAX_EDGE_PIXELS))
                except OSError:
                    raise ImageProcessingError('Cannot resize image: {}'.format(e))

                width, height = image.size
                data = BytesIO()
                image.save(data, (image.format), quality=QUALITY, optimize=True,
                  progressive=True)
    size_in_bytes = data.seek(0, SEEK_END)
    data.seek(0)
    if size_in_bytes > MAX_SIZE_IN_BYTES_AFTER_PROCESSING:
        raise ImageProcessingError('Resulting file too big: {} bytes'.format(size_in_bytes))
    return ImageProcessingResult(size_in_bytes, width, height, image.format, data)