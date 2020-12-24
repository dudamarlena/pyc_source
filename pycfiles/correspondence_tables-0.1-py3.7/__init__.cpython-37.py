# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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