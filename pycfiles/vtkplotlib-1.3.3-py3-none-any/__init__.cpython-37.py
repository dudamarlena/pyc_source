# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/bwoodsend/Windows_OS/Users/Brénainn/Documents/programming/WinPython-64bit-3.5.1.3/notebooks/vtkplotlib/vtkplotlib/data/__init__.py
# Compiled at: 2020-03-19 15:29:16
# Size of source mod 2**32: 1938 bytes
import sys
from pathlib2 import Path
import pkg_resources
if getattr(sys, 'frozen', False):
    DATA_FOLDER = Path(pkg_resources.resource_filename('vtkplotlib', '')).parent / 'vpl-data'
else:
    DATA_FOLDER = Path(pkg_resources.resource_filename('vtkplotlib', '')) / 'data'
ROOT = DATA_FOLDER.parent
MODELS_FOLDER = DATA_FOLDER / 'models'

def get_rabbit_stl():
    return str(MODELS_FOLDER / 'rabbit' / 'rabbit.stl')


ICONS_FOLDER = DATA_FOLDER / 'icons'
ICONS = {i.stem:str(i) for i in ICONS_FOLDER.glob('*.jpg')}

def assert_ok():
    assert ICONS_FOLDER.is_dir()
    assert MODELS_FOLDER.is_dir()
    assert Path(get_rabbit_stl()).exists()


if __name__ == '__main__':
    assert_ok()