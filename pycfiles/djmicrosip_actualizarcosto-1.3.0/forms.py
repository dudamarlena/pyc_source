# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\BitBucket\djmicrosip_apps\djmicrosip_actualizarcosto\djmicrosip_actualizarcosto\forms.py
# Compiled at: 2016-02-19 15:09:36
from .models import *
from django import forms
import autocomplete_light

class ArticuloForm(forms.ModelForm):

    class Meta:
        model = Articulo
        fields = ('costo_ultima_compra', )


class ArticuloSearchForm(forms.Form):
    articulo = forms.ModelChoiceField(queryset=Articulo.objects.all(), widget=autocomplete_light.ChoiceWidget('ArticuloAutocomplete'), required=False)
    clave = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Clave...'}), required=False)

    def __init__(self, *args, **kwargs):
        super(ArticuloSearchForm, self).__init__(*args, **kwargs)
        self.fields['articulo'].widget.attrs['class'] = 'form-control'
        self.fields['clave'].widget.attrs['class'] = 'form-control'