# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled/NearBeach/views_organisation_information.py
# Compiled at: 2020-05-03 01:13:24
# Size of source mod 2**32: 6130 bytes
"""
VIEWS - project information
~~~~~~~~~~~~~~~~~~~~~~~~~~~
This views python file will store all the required classes/functions for the AJAX
components of the PROJECT INFORMATION MODULES. This is to help keep the VIEWS
file clean from AJAX (spray and wipe).
"""
from django.contrib.auth.decorators import login_required
from .models import *
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader
from NearBeach.forms import *
from .models import *
from .misc_functions import *
from .user_permissions import return_user_permission_level
from django.urls import reverse
import simplejson

@login_required(login_url='login', redirect_field_name='')
def information_organisation_contact_history(request, organisation_id):
    permission_results = return_user_permission_level(request, None, ['organisation', 'contact_history'])
    if permission_results['organisation'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
        if request.method == 'POST' and permission_results['organisation'] > 1:
            print('Request is post')
            form = information_organisation_contact_history_form(request.POST, request.FILES)
            if form.is_valid():
                current_user = request.user
                contact_history_notes = form.cleaned_data['contact_history']
                if not contact_history_notes == '':
                    contact_type = form.cleaned_data['contact_type']
                    contact_date = form.cleaned_data['contact_date']
                    if request.FILES == None:
                        print('No files uploaded in contacts')
                    else:
                        contact_attachment = request.FILES.get('contact_attachment')
                        if contact_attachment:
                            print('There was a document')
                            documents_save = document(document_description=contact_attachment,
                              document=contact_attachment,
                              change_user=(request.user))
                            documents_save.save()
                            document_permissions_save = document_permission(document_key=documents_save,
                              organisation_id=organisation.objects.get(organisation_id=organisation_id),
                              change_user=(request.user))
                            document_permissions_save.save()
                        else:
                            print('There was no document?')
                    submit_history = contact_history(organisation_id=organisation.objects.get(organisation_id=organisation_id),
                      contact_type=contact_type,
                      contact_date=contact_date,
                      contact_history=contact_history_notes,
                      user_id=current_user,
                      change_user=(request.user))
                    if contact_attachment:
                        submit_history.document_key = documents_save
                    submit_history.save()
    else:
        print(form.errors)
    contact_history_results = contact_history.objects.filter(organisation_id=organisation.objects.get(organisation_id=organisation_id))
    contact_date = datetime.datetime.now()
    t = loader.get_template('NearBeach/organisation_information/organisation_contact_history.html')
    c = {'contact_history_form':information_organisation_contact_history_form(), 
     'contact_history_results':contact_history_results, 
     'organisation_permissions':permission_results['organisation'], 
     'contact_history_permission':permission_results['contact_history'], 
     'PRIVATE_MEDIA_URL':settings.PRIVATE_MEDIA_URL, 
     'contact_year':contact_date.year, 
     'contact_month':contact_date.month, 
     'contact_day':contact_date.day, 
     'contact_hour':contact_date.hour, 
     'contact_minute':int(contact_date.minute / 5) * 5}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def information_organisation_documents_upload(request, organisation_id):
    if request.method == 'POST':
        if request.FILES == None:
            return HttpResponseBadRequest('File needs to be uploaded')
        file = request.FILES['file']
        filename = str(file)
        file_size = file.size
        print('File name: ' + filename + '\nFile Size: ' + str(file_size))
        organisation_instance = organisation.objects.get(organisation_id=organisation_id)
        document_save = document(document_description=filename,
          document=file,
          change_user=(request.user))
        document_save.save()
        document_permissions_save = document_permission(document_key=document_save,
          organisation_id=organisation_instance,
          change_user=(request.user))
        document_permissions_save.save()
        result = []
        result.append({'name':filename, 
         'size':file_size, 
         'url':'', 
         'thumbnail_url':'', 
         'delete_url':'/', 
         'delete_type':'POST'})
        response_data = simplejson.dumps(result)
        return HttpResponse(response_data, content_type='application/json')
    return HttpResponseBadRequest('Only POST accepted')