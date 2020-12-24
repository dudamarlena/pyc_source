# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/skylar/pinax/projects/testoster/apps/listings/forms.py
# Compiled at: 2009-08-16 07:26:56
from datetime import datetime
from django import forms
from listings.models import Listing

class ListingForm(forms.ModelForm):

    class Meta:
        model = Listing
        exclude = ('owner', 'state')