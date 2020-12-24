# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ashwin/Desktop/Projects/COCO-Assistant/coco_assistant/__init__.py
# Compiled at: 2019-09-20 04:47:50
# Size of source mod 2**32: 303 bytes
import os, pathlib
from .coco_assistant import COCO_Assistant
import coco_assistant
PACKAGE_ROOT = pathlib.Path(coco_assistant.__file__).resolve().parent
with open(os.path.join(PACKAGE_ROOT, 'VERSION')) as (version_file):
    __version__ = version_file.read().strip()