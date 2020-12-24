# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/commons/image.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 1420 bytes
from pyowm.commons.enums import ImageTypeEnum
from pyowm.commons.databoxes import ImageType

class Image:
    """Image"""

    def __init__(self, data, image_type=None):
        self.data = data
        if image_type is not None:
            assert isinstance(image_type, ImageType)
        self.image_type = image_type

    def persist(self, path_to_file):
        """
        Saves the image to disk on a file

        :param path_to_file: path to the target file
        :type path_to_file: str
        :return: `None`
        """
        with open(path_to_file, 'wb') as (f):
            f.write(self.data)

    @classmethod
    def load(cls, path_to_file):
        """
        Loads the image data from a file on disk and tries to guess the image MIME type

        :param path_to_file: path to the source file
        :type path_to_file: str
        :return: a `pyowm.image.Image` instance
        """
        import mimetypes
        mimetypes.init()
        mime = mimetypes.guess_type('file://%s' % path_to_file)[0]
        img_type = ImageTypeEnum.lookup_by_mime_type(mime)
        with open(path_to_file, 'rb') as (f):
            data = f.read()
        return Image(data, image_type=img_type)