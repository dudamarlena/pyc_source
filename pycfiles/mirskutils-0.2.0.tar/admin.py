# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./webapp/registration/admin.py
# Compiled at: 2014-06-01 18:18:49
from django.contrib import admin
from django.contrib import auth
from models import Individual

class IndividualCreationForm(auth.forms.UserCreationForm):

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            Individual.objects.get(username=username)
        except Individual.DoesNotExist:
            return username

        raise forms.ValidationError(self.error_messages['duplicate_username'])

    class Meta:
        model = Individual
        fields = ('username', )


class IndividualChangeForm(auth.forms.UserChangeForm):
    pass


class IndividualAdmin(auth.admin.UserAdmin):
    form = IndividualChangeForm
    add_form = IndividualCreationForm


admin.site.register(Individual, IndividualAdmin)