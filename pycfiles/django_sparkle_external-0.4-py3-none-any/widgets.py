# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/uranusjr.com/uranusjr.com/base/forms/widgets.py
# Compiled at: 2014-01-11 14:05:15
from __future__ import unicode_literals
from django.template.loader import get_template
from ghostdown.forms.widgets import GhostdownInput

class PopupGhostdownInput(GhostdownInput):

    def get_template(self):
        return get_template(b'base/includes/ghostdown_editor.html')