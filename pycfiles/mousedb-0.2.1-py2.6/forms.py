# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mousedb/timed_mating/forms.py
# Compiled at: 2010-06-14 19:51:43
"""This package describes forms used by the Timed Mating app."""
from django import forms
from mousedb.timed_mating.models import PlugEvents

class BreedingPlugForm(forms.ModelForm):
    """This form is used to enter Plug Events from a specific breeding cage."""

    class Meta:
        model = PlugEvents
        exclude = ['Breeding']