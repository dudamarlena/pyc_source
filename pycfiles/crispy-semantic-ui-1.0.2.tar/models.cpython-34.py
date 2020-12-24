# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alex/projects/showmore/venv3/lib/python3.4/site-packages/semantic_ui/models.py
# Compiled at: 2015-08-08 14:58:06
# Size of source mod 2**32: 113 bytes
from django import VERSION
if VERSION < (1, 7, 0):
    from semantic_ui.patch import patch_all
    patch_all()