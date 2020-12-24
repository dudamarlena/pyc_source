# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/projects/showmore/venv3/lib/python3.4/site-packages/semantic_ui/models.py
# Compiled at: 2015-08-08 14:58:06
# Size of source mod 2**32: 113 bytes
from django import VERSION
if VERSION < (1, 7, 0):
    from semantic_ui.patch import patch_all
    patch_all()