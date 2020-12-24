# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/helpcenter/tests/dummy_classes.py
# Compiled at: 2016-09-30 00:56:02
from django import forms

class BlankForm(forms.Form):
    """A blank form for testing purposes."""

    def __init__(self, *args, **kwargs):
        """Consume arguments."""
        super(BlankForm, self).__init__()