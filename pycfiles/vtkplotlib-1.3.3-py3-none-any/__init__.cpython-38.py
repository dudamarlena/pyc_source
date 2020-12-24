# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brénainn\documents\programming\winpython-64bit-3.5.1.3\notebooks\vtkplotlib\vtkplotlib\data\__init__.py
# Compiled at: 2020-04-02 16:27:39
# Size of source mod 2**32: 2020 bytes
import sys
from pathlib2 import Path
from vtkplotlib import __file__ as _init_path
if getattr(sys, 'frozen', False):
    DATA_FOLDER = Path(_init_path).parent.with_name('vpl-data')
else:
    DATA_FOLDER = Path(_init_path).with_name('data')
MODELS_FOLDER = DATA_FOLDER / 'models'

def get_rabbit_stl():
    return str(MODELS_FOLDER / 'rabbit' / 'rabbit.stl')


ICONS_FOLDER = DATA_FOLDER / 'icons'
ICONS = {str(i):i.stem for i in ICONS_FOLDER.glob('*.jpg')}

def assert_ok():
    assert ICONS_FOLDER.is_dir()
    assert MODELS_FOLDER.is_dir()
    assert Path(get_rabbit_stl()).exists()


if __name__ == '__main__':
    assert_ok()