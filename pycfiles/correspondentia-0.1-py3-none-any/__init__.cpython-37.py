# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\correspondence_tables\__init__.py
# Compiled at: 2020-01-19 13:33:24
# Size of source mod 2**32: 362 bytes
__all__ = ('generate_usepa_to_chemspyder_correspondence', )
__version__ = (0, 1)
from pathlib import Path
data_dir = Path(__file__).parent / 'data'
from .usepa_to_chemspyder import generate_usepa_to_chemspyder_correspondence

def generate_all(base_dir):
    print('hello bonsai')