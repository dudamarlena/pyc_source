# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.8/site-packages/MetaStalk/utils/heic_parse.py
# Compiled at: 2020-05-08 18:09:31
# Size of source mod 2**32: 746 bytes
"""heic_parse
---

Deals with heic and heif exif
"""
import io, exifread
try:
    import pyheif
    heic_enabled = True
except ImportError:
    heic_enabled = False
else:

    def check_heic():
        """check_heic
    ---

    Returns:
        [bool] -- Whether or not pyheif was imported
    """
        return heic_enabled


    def parse_heic(item: str) -> dict:
        """parse_heic
    ---
    The parses heic files
    """
        heif_file = pyheif.read_heif(item)
        if not heif_file.metadata:
            return {}
        for metadata in heif_file.metadata:
            if metadata['type'] == 'Exif':
                fstream = io.BytesIO(metadata['data'][6:])
                return exifread.process_file(fstream)
            return {}