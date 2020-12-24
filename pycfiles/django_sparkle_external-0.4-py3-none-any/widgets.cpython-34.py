# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/uranusjr/Documents/programming/python/django-sparkle-external/django-sparkle-external/sparkle/forms/widgets.py
# Compiled at: 2014-06-19 01:14:59
# Size of source mod 2**32: 325 bytes
from __future__ import unicode_literals
from django.template.loader import get_template
from ghostdown.forms.widgets import GhostdownInput

class PopupGhostdownInput(GhostdownInput):

    def get_template(self):
        return get_template('sparkle/includes/ghostdown_editor.html')