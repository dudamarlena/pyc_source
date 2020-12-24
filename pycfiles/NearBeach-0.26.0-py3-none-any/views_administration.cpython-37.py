# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/views_administration.py
# Compiled at: 2020-02-08 00:57:55
# Size of source mod 2**32: 23672 bytes
from .forms import *
from .models import *
from .private_media import *
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum, Q, Min
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.urls import reverse
from .misc_functions import *
from .user_permissions import return_user_permission_level
import datetime, json, simplejson

@login_required(login_url='login', redirect_field_name='')
def list_of_taxes_deactivate(request, tax_id):
    if request.method == 'POST':
        tax_instance = list_of_tax.objects.get(tax_id=tax_id)
        if tax_instance.is_deleted == 'FALSE':
            tax_instance.is_deleted = 'TRUE'
        else:
            tax_instance.is_deleted = 'FALSE'
        tax_instance.save()
        t = loader.get_template('NearBeach/blank.html')
        c = {}
        return HttpResponse(t.render(c, request))
    return HttpResponseBadRequest('Sorry, can only be done through POST')


@login_required(login_url='login', redirect_field_name='')
def list_of_taxes_edit(request, tax_id):
    tax_result = list_of_tax.objects.get(pk=tax_id)
    if request.method == 'POST':
        form = list_of_tax_form(request.POST)
        if form.is_valid():
            tax_result.tax_amount = form.cleaned_data['tax_amount']
            tax_result.tax_description = form.cleaned_data['tax_description']
            tax_result.save()
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_edit.html')
    c = {'list_of_tax_form':list_of_tax_form(instance=tax_result), 
     'tax_id':tax_id}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def list_of_taxes_information(request):
    permission_results = return_user_permission_level(request, None, 'tax')
    if permission_results['tax'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_information.html')
    c = {'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def list_of_taxes_list(request):
    permission_results = return_user_permission_level(request, None, 'tax')
    if permission_results['tax'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    list_of_taxes_results = list_of_tax.objects.all().order_by('tax_amount')
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_list.html')
    c = {'list_of_taxes_results': list_of_taxes_results}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def list_of_taxes_new(request):
    if request.method == 'POST':
        form = list_of_tax_form(request.POST)
        if form.is_valid():
            tax_submit = list_of_tax(tax_amount=(form.cleaned_data['tax_amount']),
              tax_description=(form.cleaned_data['tax_description']),
              change_user=(request.user))
            tax_submit.save()
        else:
            print(form.errors)
    t = loader.get_template('NearBeach/list_of_taxes/list_of_taxes_new.html')
    c = {'list_of_tax_form': list_of_tax_form()}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def new_user(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_user')
    if permission_results['administration_create_user'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
        errors = ''
        if request.method == 'POST':
            if permission_results['administration_create_user'] == 4:
                form = user_information_form(request.POST)
                if form.is_valid():
                    form.save()
                    password1 = form.cleaned_data['password1']
                    password2 = form.cleaned_data['password2']
                    if not password1 == password2:
                        errors = '<li>PASSWORDS ARE NOT THE SAME<li>'
            else:
                if password1 == '':
                    password1 = User.objects.make_random_password()
                user_instance = User.objects.get(username=(form.cleaned_data['username']))
                user_instance.set_password(password1)
                user_instance.save()
                return HttpResponseRedirect(reverse('user_information', args={user_instance.id}))
    else:
        print(form.errors)
        errors = form.errors
    t = loader.get_template('NearBeach/new_user.html')
    c = {'user_information_form':user_information_form(request.POST or None), 
     'is_superuser':request.session['is_superuser'], 
     'errors':errors, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def product_and_service_discontinued(request, product_id):
    product_instance = product_and_service.objects.get(product_id=product_id)
    if product_instance.is_deleted == 'FALSE':
        product_instance.is_deleted = 'TRUE'
    else:
        product_instance.is_deleted = 'FALSE'
    product_instance.save()
    return HttpResponseRedirect(reverse(product_and_service_search))


@login_required(login_url='login', redirect_field_name='')
def product_and_service_edit(request, product_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
    if permission_results['administration_create_permission_set'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST' and permission_results['administration_create_permission_set'] > 2:
        form = product_and_service_form((request.POST), instance=product_and_service.objects.get(product_id=product_id))
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(product_and_service_search))
        print(form.errors)
    t = loader.get_template('NearBeach/product_and_service/product_and_service_edit.html')
    c = {'product_and_service_form':product_and_service_form(instance=product_and_service.objects.get(product_id=product_id)), 
     'product_id':product_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def product_and_service_new(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_permission_set')
    if permission_results['administration_create_permission_set'] < 2:
        return HttpResponseRedirect(reverse('permission_denied'))
    elif request.method == 'POST' and permission_results['administration_create_permission_set'] > 3:
        form = product_and_service_form(request.POST)
        if form.is_valid():
            submit_product = product_and_service(product_or_service=(form.cleaned_data['product_or_service']),
              product_name=(form.cleaned_data['product_name']),
              product_part_number=(form.cleaned_data['product_part_number']),
              product_cost=(form.cleaned_data['product_cost']),
              product_price=(form.cleaned_data['product_price']),
              product_description=(form.cleaned_data['product_description']),
              change_user=(request.user))
            submit_product.save()
            return HttpResponseRedirect(reverse(product_and_service_search))
        print(form.errors)
    t = loader.get_template('NearBeach/product_and_service/product_and_service_new.html')
    c = {'product_and_service_form':product_and_service_form(), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def product_and_service_search(request):
    permission_results = return_user_permission_level(request, None, 'invoice_product')
    if permission_results['invoice_product'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    product_results = product_and_service.objects.filter(product_or_service='Product')
    service_results = product_and_service.objects.filter(product_or_service='Service')
    t = loader.get_template('NearBeach/product_and_service/product_and_service_search.html')
    c = {'product_results':product_results, 
     'service_results':service_results, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def search_users(request):
    permission_results = return_user_permission_level(request, None, 'administration_create_users')
    if permission_results['administration_create_users'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
    else:
        filter_users = ''
        if request.method == 'POST':
            form = search_form(request.POST)
            if form.is_valid():
                search_for = form.cleaned_data['search_for']
                user_results = User.objects.filter(Q(is_active=True), Q(username__contains=search_for) | Q(first_name__contains=search_for) | Q(last_name__contains=search_for) | Q(email__contains=search_for))
            else:
                print(form.errors)
        else:
            user_results = User.objects.filter(is_active=True)
    t = loader.get_template('NearBeach/search_users.html')
    c = {'user_results':user_results, 
     'search_form':search_form(request.POST or None), 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration']}
    return HttpResponse(t.render(c, request))


@login_required(login_url='login', redirect_field_name='')
def user_information(request, user_id):
    permission_results = return_user_permission_level(request, None, 'administration_create_users')
    if permission_results['administration_create_users'] == 0:
        return HttpResponseRedirect(reverse('permission_denied'))
        errors = ''
        save_state = ''
        if request.method == 'POST' and permission_results['administration_create_users'] == 4:
            if user_id == '':
                form = user_information_form(request.POST)
    else:
        form = user_information_form((request.POST),
          instance=User.objects.get(id=user_id))
    if form.is_valid():
        form.save()
        save_state = 'User has been saved'
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if user_id == '':
            if not password1 == password1:
                errors = 'PASSWORDS ARE NOT THE SAME'
            else:
                if password1 == '':
                    password1 = User.objects.make_random_password()
                user_instance = User.objects.get(username=(form.cleaned_data['username']))
                user_instance.set_password(password1)
                user_instance.save()
                return HttpResponseRedirect(reverse('user_information', args={user_instance.id}))
        elif password1 == password2:
            if not password1 == '':
                user_instance = User.objects.get(id=user_id)
                user_instance.set_password(password1)
                user_instance.save()
            else:
                errors = 'PASSWORDS ARE NOT THE SAME'
        else:
            print(form.errors)
            errors = form.errors
    else:
        user_group_results = user_group.objects.filter(is_deleted='FALSE',
          username_id=user_id)
        if user_id == None:
            ui_form = user_information_form()
        else:
            ui_form = user_information_form(instance=User.objects.get(id=user_id))
    t = loader.get_template('NearBeach/user_information.html')
    c = {'user_group_results':user_group_results, 
     'user_information_form':ui_form, 
     'is_superuser':request.session['is_superuser'], 
     'errors':errors, 
     'user_id':user_id, 
     'new_item_permission':permission_results['new_item'], 
     'administration_permission':permission_results['administration'], 
     'save_state':save_state}
    return HttpResponse(t.render(c, request))