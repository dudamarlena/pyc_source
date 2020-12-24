# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superhero/tools.py
# Compiled at: 2015-05-05 00:01:33
from django import template
from django.contrib import messages
from django.contrib.admin import helpers
from django.shortcuts import render_to_response
from django.utils.translation import ugettext as _
import object_tools
from superhero.forms import ImportForm
from superhero.models import Superhero

class SuperheroImport(object_tools.ObjectTool):
    name = 'import'
    label = _('Import')
    help_text = _('Import a superhero bundle.')
    form_class = ImportForm

    def view(self, request, extra_context=None, process_form=True):
        form = extra_context['form']
        if form.is_valid() and process_form:
            superheroes = form.save()
            n = len(superheroes)
            if n == 1:
                message = _('The superhero bundle has been imported successfully.')
            else:
                message = _('%s superhero bundles have been imported successfully.' % n)
            messages.add_message(request, messages.SUCCESS, message)
        adminform = helpers.AdminForm(form, form.fieldsets, {})
        context = {'adminform': adminform}
        context.update(extra_context or {})
        context_instance = template.RequestContext(request)
        return render_to_response('admin/superhero/import_form.html', context, context_instance=context_instance)


object_tools.tools.register(SuperheroImport, Superhero)