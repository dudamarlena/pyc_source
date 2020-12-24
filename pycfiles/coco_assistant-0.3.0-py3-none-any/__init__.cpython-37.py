# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ashwin/Desktop/Projects/COCO-Assistant/coco_assistant/__init__.py
# Compiled at: 2019-09-20 04:47:50
# Size of source mod 2**32: 303 bytes
import os, pathlib
from .coco_assistant import COCO_Assistant
import coco_assistant
PACKAGE_ROOT = pathlib.Path(coco_assistant.__file__).resolve().parent
with open(os.path.join(PACKAGE_ROOT, 'VERSION')) as (version_file):
    __version__ = version_file.read().strip()