# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\latihan_django\11agustus\djangoproj\form\views.py
# Compiled at: 2014-08-17 21:59:46
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .forms import ContactView
from django.contrib import messages

def contact(request):
    form = ContactView(request.POST or None)
    if form.is_valid():
        our_form = form.save(commit=False)
        our_form.save()
        messages.add_message(request, messages.INFO, 'Pesan anda sudah terkirim. Trims  :)')
        return HttpResponseRedirect('/')
    else:
        t = loader.get_template('contact.html')
        c = RequestContext(request, {'form': form})
        return HttpResponse(t.render(c))