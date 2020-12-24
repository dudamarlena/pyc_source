# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/luke/PycharmProjects/untitled1/NearBeach/forms.py
# Compiled at: 2020-04-05 05:09:39
# Size of source mod 2**32: 128150 bytes
from __future__ import unicode_literals
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib import auth
from django.forms import ModelForm, BaseModelFormSet
from django.forms.widgets import TextInput
from NearBeach.forms_special_fields import *
from tinymce import TinyMCE
from django_select2.forms import Select2MultipleWidget, ModelSelect2MultipleWidget, Select2Widget, ModelSelect2Widget, Select2TagWidget
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db import connection
import datetime
from django.core.exceptions import ObjectDoesNotExist
DISCOUNT_CHOICE = (('Percentage', 'Percentage'), ('Amount', 'Amount'))
NOTHING_CHOICE = (('', '-----'), )
OBJECT_CHOICES = (('Project', 'Project'), ('Task', 'Task'), ('Quote', 'Quote'), ('Opportunity', 'Opportunity'))
RATING_SCORE = ((1, '1 Star'), (2, '2 Star'), (3, '3 Star'), (4, '4 Star'), (5, '5 Star'))
RFC_IMPACT = ((3, 'High'), (2, 'Medium'), (1, 'Low'))
RFC_PRIORITY = ((4, 'Critical'), (3, 'High'), (2, 'Medium'), (1, 'Low'))
RFC_RISK = ((5, 'Very High'), (4, 'High'), (3, 'Moderate'), (2, 'Low'), (1, 'None'))
RFC_STATUS = ((1, 'Draft'), (2, 'Waiting for approval'), (3, 'Approved'), (4, 'Started'),
              (5, 'Finished'), (6, 'Rejected'))
RFC_TYPE = ((4, 'Emergency'), (3, 'High'), (2, 'Medium'), (1, 'Low'))
INCLUDE_CLOSED = {
 ('INCLUDE_CLOSED', 'Include Closed?')}
INCLUDE_DEACTIVATED = {
 ('INCLUDE_DEACTIVATED', 'Include Deactivated?')}
MAX_PICTURE_SIZE = 1024000

class about_user_form(ModelForm):
    about_user_text = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder': 'Give a good description about yourself'}),
      required=False)

    class Meta:
        model = about_user
        fields = {
         'about_user_text'}


class add_permission_set_to_group_form(forms.Form):

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id')
        (super(add_permission_set_to_group_form, self).__init__)(*args, **kwargs)
        permission_set_results = permission_set.objects.filter(is_deleted='FALSE').exclude(permission_set_id__in=(group_permission.objects.filter(is_deleted='FALSE',
          group_id=group_id).values('permission_set_id')))
        self.fields['add_permission_set'].queryset = permission_set_results

    add_permission_set = forms.ModelChoiceField(label='Permission Set Name',
      widget=Select2Widget(attrs={'class':'form-control', 
     'onchange':'permission_set_changed()'}),
      queryset=permission_set.objects.filter(is_deleted='FALSE'))


class add_user_to_group_form(forms.Form):

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id')
        (super(add_user_to_group_form, self).__init__)(*args, **kwargs)
        permission_set_results = permission_set.objects.filter(is_deleted='FALSE',
          permission_set_id__in=(group_permission.objects.filter(is_deleted='FALSE',
          group_id=group_id).values('permission_set_id')))
        self.fields['permission_set'].queryset = permission_set_results

    permission_set = forms.ModelChoiceField(queryset=(permission_set.objects.all()),
      widget=Select2Widget(attrs={'class':'form-control', 
     'onchange':'add_user_changed()'}))
    add_user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True),
      widget=Select2Widget(attrs={'class':'form-control', 
     'onchange':'add_user_changed()'}))


class assign_group_add_form(forms.Form):

    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        destination = kwargs.pop('destination', None)
        (super(assign_group_add_form, self).__init__)(*args, **kwargs)
        group_results = group.objects.all()
        if destination == 'project':
            group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
              project_id=location_id).exclude(group_id=None).values('group_id')))
        else:
            if destination == 'task':
                group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                  task_id=location_id).exclude(group_id=None).values('group_id')))
            else:
                if destination == 'requirement':
                    group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                      requirement_id=location_id).exclude(group_id=None).values('group_id')))
                else:
                    if destination == 'quote':
                        group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                          quote_id=location_id).exclude(group_id=None).values('group_id')))
                    else:
                        if destination == 'kanban_board':
                            group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                              kanban_board_id=location_id).exclude(group_id=None).values('group_id')))
                        else:
                            if destination == 'opportunity':
                                group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                  opportunity_id=location_id).exclude(group_id=None).values('group_id')))
                            else:
                                if destination == 'request_for_change':
                                    group_results = group_results.exclude(group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                      request_for_change_id=location_id).exclude(group_id=None).values('group_id')))
                                self.fields['add_group'].queryset = group_results

    add_group = forms.ModelChoiceField(queryset=(group.objects.all()),
      required=True,
      widget=forms.Select(attrs={'onchange':'add_group_change()', 
     'class':'form-control'}))


class assign_user_add_form(forms.Form):

    def __init__(self, *args, **kwargs):
        location_id = kwargs.pop('location_id')
        destination = kwargs.pop('destination', None)
        (super(assign_user_add_form, self).__init__)(*args, **kwargs)
        if destination == 'project':
            user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
              group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
              project_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
              project_id=location_id).exclude(assigned_user=None).values('assigned_user')))
        else:
            if destination == 'task':
                user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
                  group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                  task_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                  task_id=location_id).exclude(assigned_user=None).values('assigned_user')))
            else:
                if destination == 'requirement':
                    user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
                      group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                      requirement_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                      requirement_id=location_id).exclude(assigned_user=None).values('assigned_user')))
                else:
                    if destination == 'quote':
                        user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
                          group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                          quote_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                          quote_id=location_id).exclude(assigned_user=None).values('assigned_user')))
                    else:
                        if destination == 'kanban_board':
                            user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
                              group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                              kanban_board_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                              kanban_board_id=location_id).exclude(assigned_user=None).values('assigned_user')))
                        else:
                            if destination == 'opportunity':
                                user_results = User.objects.filter(id__in=(user_group.objects.filter(is_deleted='FALSE',
                                  group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                  opportunity_id=location_id).values('group_id'))).values('username'))).exclude(id__in=(object_assignment.objects.filter(is_deleted='FALSE',
                                  opportunity_id=location_id).exclude(assigned_user=None).values('assigned_user')))
                            else:
                                print('SOMETHING FUCKED UP!!!')
                                print('DESTINATION: ' + destination)
        self.fields['add_user'].queryset = user_results

    add_user = forms.ModelChoiceField(queryset=(User.objects.all()),
      required=True,
      widget=forms.Select(attrs={'onchange':'add_user_change()', 
     'class':'form-control'}))


class bug_client_form(ModelForm):
    bug_client_results = list_of_bug_client.objects.filter(is_deleted='FALSE')
    bug_client_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Bug Client Name', 
     'class':'form-control'}))
    list_of_bug_client = forms.ModelChoiceField(label='Bug Clients',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=bug_client_results,
      empty_label=None)
    bug_client_url = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Example: https://bugzilla.nearbeach.org', 
     'class':'form-control'}))

    class Meta:
        model = bug_client
        fields = {
         'bug_client_name',
         'list_of_bug_client',
         'bug_client_url'}


class bug_search_form(forms.Form):
    bug_client_results = bug_client.objects.filter(is_deleted='FALSE')
    list_of_bug_client = forms.ModelChoiceField(label='Bug Clients',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=bug_client_results,
      empty_label=None)
    search = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))


class campus_information_form(ModelForm):
    campus_nickname = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Campus Nickname i.e Melbourne', 
     'class':'form-control'}))
    campus_phone = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Campus Phone', 
     'type':'tel', 
     'class':'form-control', 
     'style':'display: none'}))
    campus_fax = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Campus Fax', 
     'type':'tel', 
     'class':'form-control', 
     'style':'display: none'}))
    campus_address1 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 1', 
     'class':'form-control'}))
    campus_address2 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 2', 
     'class':'form-control'}))
    campus_address3 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 3', 
     'class':'form-control'}))
    campus_suburb = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Suburb', 
     'class':'form-control'}))

    class Meta:
        model = campus
        fields = '__all__'
        exclude = [
         'campus_region_id',
         'campus_country_id',
         'organisation_id',
         'is_deleted',
         'change_user']


class campus_readonly_form(ModelForm):
    campus_nickname = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Campus Nickname i.e Melbourne', 
     'class':'form-control', 
     'readonly':True}))
    campus_phone = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Campus Phone', 
     'type':'tel', 
     'class':'form-control', 
     'readonly':True}))
    campus_fax = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Campus Fax', 
     'type':'tel', 
     'class':'form-control', 
     'readonly':True}))
    campus_address1 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 1', 
     'class':'form-control', 
     'readonly':True}))
    campus_address2 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 2', 
     'class':'form-control', 
     'readonly':True}))
    campus_address3 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 3', 
     'class':'form-control', 
     'readonly':True}))
    campus_suburb = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Suburb', 
     'class':'form-control', 
     'readonly':True}))

    class Meta:
        model = campus
        fields = '__all__'
        exclude = [
         'campus_region_id',
         'campus_country_id',
         'organisation_id',
         'is_deleted',
         'change_user']


class change_task_form(ModelForm):

    def __init__(self, *args, **kwargs):
        rfc_id = kwargs.pop('rfc_id')
        (super(change_task_form, self).__init__)(*args, **kwargs)
        user_results = User.objects.filter(is_active=True,
          id__in=(user_group.objects.filter(is_deleted='FALSE',
          group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id).values('group_id'))).values('username')))
        self.fields['change_task_assigned_user'].queryset = user_results
        self.fields['change_task_qa_user'].queryset = user_results

    change_task_title = forms.CharField(max_length=255,
      required=True,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    change_task_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control change_task_description'}))
    change_task_start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    change_task_end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    change_task_assigned_user = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))
    change_task_qa_user = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))
    change_task_required_by = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}),
      initial='Stakeholder(s)')

    class Meta:
        model = change_task
        fields = {
         'change_task_title',
         'change_task_description',
         'change_task_start_date',
         'change_task_end_date',
         'change_task_assigned_user',
         'change_task_qa_user',
         'change_task_required_by'}


class change_task_read_only_form(ModelForm):
    change_task_description = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control change_task_description'}))

    class Meta:
        model = change_task
        fields = {
         'change_task_description'}


class connect_form(forms.Form):
    customers = forms.ModelMultipleChoiceField(queryset=(customer.objects.filter(is_deleted='FALSE').order_by('customer_first_name', 'customer_last_name')),
      widget=(ConnectCustomerSelect()),
      required=False)
    organisations = forms.ModelMultipleChoiceField(queryset=(organisation.objects.filter(is_deleted='FALSE').order_by('organisation_name')),
      widget=(ConnectOrganisationSelect()),
      required=False)


class contact_history_readonly_form(ModelForm):

    def __init__(self, *args, **kwargs):
        contact_history_id = kwargs.pop('contact_history_id', None)
        (super(contact_history_readonly_form, self).__init__)(*args, **kwargs)
        self.fields['contact_history'].widget = TinyMCE(mce_attrs={'width':'100%', 
         'toolbar':False, 
         'menubar':False, 
         'readonly':1},
          attrs={'placeholder':'Requirement Scope', 
         'id':'id_contact_history' + str(contact_history_id)})

    contact_history = forms.CharField()
    submit_history = forms.CharField(widget=TextInput(attrs={'readonly':True, 
     'class':'form-control'}))

    class Meta:
        model = contact_history
        fields = {
         'contact_history'}


class cost_information_form(forms.Form):
    cost_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'width':'70%', 
     'placeholder':'Cost Description', 
     'onkeyup':'enable_disable_add_cost()', 
     'class':'form-control'}))
    cost_amount = forms.DecimalField(max_digits=19,
      decimal_places=2,
      required=False,
      widget=forms.TextInput(attrs={'width':'30%', 
     'placeholder':'$0.00', 
     'onkeyup':'enable_disable_add_cost()', 
     'class':'form-control'}))


class customer_campus_form(ModelForm):
    customer_phone = forms.CharField(max_length=11,
      required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer_fax = forms.CharField(max_length=11,
      required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = customer_campus
        fields = {
         'customer_phone',
         'customer_fax'}


class customer_information_form(ModelForm):
    customer_last_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    customer_title = forms.ModelChoiceField(queryset=(list_of_title.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    customer_email = forms.EmailField(max_length=255,
      widget=forms.EmailInput(attrs={'class': 'form-control'}))
    customer_first_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    update_profile_picture = forms.ImageField(required=False,
      widget=forms.FileInput(attrs={'size': MAX_PICTURE_SIZE}))

    class Meta:
        model = customer
        fields = '__all__'
        exclude = [
         'is_deleted',
         'organisation_id',
         'change_user']

    def clean_update_profile_picture(self):
        profile_picture = self.cleaned_data['update_profile_picture']
        try:
            picture_errors = ''
            main, sub = profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ('jpeg', 'gif', 'png')):
                picture_errors += 'Please use a JPEG, GIF or PNG image'
            if len(profile_picture) > MAX_PICTURE_SIZE:
                picture_errors += '\nPicture profile exceeds 1000kb'
            if not picture_errors == '':
                raise forms.ValidationError(picture_errors)
        except AttributeError:
            pass

        return profile_picture


class customer_readonly_form(ModelForm):
    customer_last_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'readonly':True}))
    customer_title = forms.ModelChoiceField(queryset=(list_of_title.objects.all()),
      widget=forms.Select(attrs={'class':'form-control', 
     'disabled':True}))
    customer_email = forms.EmailField(max_length=255,
      widget=forms.EmailInput(attrs={'class':'form-control', 
     'readonly':True}))
    customer_first_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'readonly':True}))
    customer_media = forms.CharField(widget=TinyMCE(attrs={}),
      required=False)

    class Meta:
        model = customer
        fields = '__all__'
        exclude = [
         'is_deleted',
         'organisation_id',
         'change_user']


class diagnostic_test_document_upload_form(forms.Form):
    document = forms.FileField(required=True)


class document_upload_form(ModelForm):
    document_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Document Description', 
     'class':'form-control'}))

    class Meta:
        model = document
        fields = {
         'document',
         'document_description'}


class document_url_form(ModelForm):
    document_url_location = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'https://documentlocation.com', 
     'style':'width: 100%;'}))
    document_description = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'placeholder': 'Document Description'}))

    class Meta:
        model = document
        fields = {
         'document_url_location',
         'document_description'}


class email_form(ModelForm):

    def __init__--- This code section failed: ---

 L.1015         0  LOAD_FAST                'kwargs'
                2  LOAD_METHOD              pop
                4  LOAD_STR                 'location_id'
                6  CALL_METHOD_1         1  '1 positional argument'
                8  STORE_FAST               'location_id'

 L.1016        10  LOAD_FAST                'kwargs'
               12  LOAD_METHOD              pop
               14  LOAD_STR                 'destination'
               16  LOAD_CONST               None
               18  CALL_METHOD_2         2  '2 positional arguments'
               20  STORE_FAST               'destination'

 L.1018        22  LOAD_GLOBAL              super
               24  LOAD_GLOBAL              email_form
               26  LOAD_FAST                'self'
               28  CALL_FUNCTION_2       2  '2 positional arguments'
               30  LOAD_ATTR                __init__
               32  LOAD_FAST                'args'
               34  LOAD_FAST                'kwargs'
               36  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               38  POP_TOP          

 L.1020        40  LOAD_FAST                'destination'
               42  LOAD_STR                 'organisation'
               44  COMPARE_OP               ==
               46  POP_JUMP_IF_FALSE    80  'to 80'

 L.1021        48  LOAD_GLOBAL              customer
               50  LOAD_ATTR                objects
               52  LOAD_ATTR                filter

 L.1022        54  LOAD_STR                 'FALSE'

 L.1023        56  LOAD_FAST                'location_id'
               58  LOAD_CONST               ('is_deleted', 'organisation_id')
               60  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               62  STORE_FAST               'customer_results'

 L.1025        64  LOAD_CONST               False
               66  LOAD_FAST                'self'
               68  LOAD_ATTR                fields
               70  LOAD_STR                 'to_email'
               72  BINARY_SUBSCR    
               74  STORE_ATTR               required
            76_78  JUMP_FORWARD        702  'to 702'
             80_0  COME_FROM            46  '46'

 L.1026        80  LOAD_FAST                'destination'
               82  LOAD_STR                 'customer'
               84  COMPARE_OP               ==
               86  POP_JUMP_IF_FALSE   154  'to 154'

 L.1027        88  LOAD_GLOBAL              customer
               90  LOAD_ATTR                objects
               92  LOAD_ATTR                filter

 L.1028        94  LOAD_STR                 'FALSE'

 L.1029        96  LOAD_GLOBAL              customer
               98  LOAD_ATTR                objects
              100  LOAD_ATTR                filter
              102  LOAD_FAST                'location_id'
              104  LOAD_CONST               ('customer_id',)
              106  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              108  LOAD_METHOD              values
              110  LOAD_STR                 'organisation_id'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  LOAD_CONST               ('is_deleted', 'organisation_id__in')
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  STORE_FAST               'customer_results'

 L.1033       120  LOAD_FAST                'customer_results'
              122  POP_JUMP_IF_TRUE    138  'to 138'

 L.1034       124  LOAD_GLOBAL              customer
              126  LOAD_ATTR                objects
              128  LOAD_ATTR                filter
              130  LOAD_FAST                'location_id'
              132  LOAD_CONST               ('customer_id',)
              134  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              136  STORE_FAST               'customer_results'
            138_0  COME_FROM           122  '122'

 L.1036       138  LOAD_CONST               True
              140  LOAD_FAST                'self'
              142  LOAD_ATTR                fields
              144  LOAD_STR                 'to_email'
              146  BINARY_SUBSCR    
              148  STORE_ATTR               required
          150_152  JUMP_FORWARD        702  'to 702'
            154_0  COME_FROM            86  '86'

 L.1037       154  LOAD_FAST                'destination'
              156  LOAD_STR                 'project'
              158  COMPARE_OP               ==
              160  POP_JUMP_IF_FALSE   234  'to 234'

 L.1042       162  LOAD_GLOBAL              project
              164  LOAD_ATTR                objects
              166  LOAD_ATTR                get
              168  LOAD_FAST                'location_id'
              170  LOAD_CONST               ('project_id',)
              172  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              174  STORE_FAST               'project_results'

 L.1043       176  LOAD_FAST                'project_results'
              178  LOAD_ATTR                organisation_id
              180  POP_JUMP_IF_FALSE   214  'to 214'

 L.1044       182  LOAD_GLOBAL              customer
              184  LOAD_ATTR                objects
              186  LOAD_ATTR                filter

 L.1045       188  LOAD_STR                 'FALSE'

 L.1046       190  LOAD_GLOBAL              project
              192  LOAD_ATTR                objects
              194  LOAD_ATTR                get
              196  LOAD_FAST                'location_id'
              198  LOAD_CONST               ('project_id',)
              200  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              202  LOAD_ATTR                organisation_id
              204  LOAD_ATTR                organisation_id
              206  LOAD_CONST               ('is_deleted', 'organisation_id')
              208  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              210  STORE_FAST               'customer_results'
              212  JUMP_FORWARD        702  'to 702'
            214_0  COME_FROM           180  '180'

 L.1049       214  LOAD_GLOBAL              customer
              216  LOAD_ATTR                objects
              218  LOAD_ATTR                filter

 L.1050       220  LOAD_FAST                'project_results'
              222  LOAD_ATTR                customer_id
              224  LOAD_CONST               ('customer_id',)
              226  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              228  STORE_FAST               'customer_results'
          230_232  JUMP_FORWARD        702  'to 702'
            234_0  COME_FROM           160  '160'

 L.1052       234  LOAD_FAST                'destination'
              236  LOAD_STR                 'task'
              238  COMPARE_OP               ==
          240_242  POP_JUMP_IF_FALSE   334  'to 334'

 L.1053       244  LOAD_GLOBAL              task
              246  LOAD_ATTR                objects
              248  LOAD_ATTR                get
              250  LOAD_FAST                'location_id'
              252  LOAD_CONST               ('task_id',)
              254  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              256  STORE_FAST               'task_results'

 L.1054       258  LOAD_FAST                'task_results'
              260  LOAD_ATTR                organisation_id
          262_264  POP_JUMP_IF_FALSE   298  'to 298'

 L.1055       266  LOAD_GLOBAL              customer
              268  LOAD_ATTR                objects
              270  LOAD_ATTR                filter

 L.1056       272  LOAD_STR                 'FALSE'

 L.1057       274  LOAD_GLOBAL              task
              276  LOAD_ATTR                objects
              278  LOAD_ATTR                get
              280  LOAD_FAST                'location_id'
              282  LOAD_CONST               ('task_id',)
              284  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              286  LOAD_ATTR                organisation_id
              288  LOAD_ATTR                organisation_id
              290  LOAD_CONST               ('is_deleted', 'organisation_id')
              292  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              294  STORE_FAST               'customer_results'
              296  JUMP_FORWARD        702  'to 702'
            298_0  COME_FROM           262  '262'

 L.1060       298  LOAD_GLOBAL              customer
              300  LOAD_ATTR                objects
              302  LOAD_ATTR                filter

 L.1061       304  LOAD_GLOBAL              task_customer
              306  LOAD_ATTR                objects
              308  LOAD_ATTR                filter

 L.1062       310  LOAD_STR                 'FALSE'

 L.1063       312  LOAD_FAST                'location_id'
              314  LOAD_CONST               ('is_deleted', 'task_id')
              316  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              318  LOAD_METHOD              values

 L.1064       320  LOAD_STR                 'customer_id'
              322  CALL_METHOD_1         1  '1 positional argument'
              324  LOAD_CONST               ('customer_id__in',)
              326  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              328  STORE_FAST               'customer_results'
          330_332  JUMP_FORWARD        702  'to 702'
            334_0  COME_FROM           240  '240'

 L.1066       334  LOAD_FAST                'destination'
              336  LOAD_STR                 'opportunity'
              338  COMPARE_OP               ==
          340_342  POP_JUMP_IF_FALSE   398  'to 398'

 L.1074       344  LOAD_GLOBAL              opportunity
              346  LOAD_ATTR                objects
              348  LOAD_ATTR                get
              350  LOAD_FAST                'location_id'
              352  LOAD_CONST               ('opportunity_id',)
              354  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              356  STORE_FAST               'opportunity_results'

 L.1075       358  LOAD_GLOBAL              customer
              360  LOAD_ATTR                objects
              362  LOAD_ATTR                filter

 L.1076       364  LOAD_STR                 'FALSE'

 L.1077       366  LOAD_GLOBAL              object_assignment
              368  LOAD_ATTR                objects
              370  LOAD_ATTR                filter

 L.1078       372  LOAD_STR                 'FALSE'

 L.1079       374  LOAD_CONST               False

 L.1080       376  LOAD_FAST                'location_id'
              378  LOAD_CONST               ('is_deleted', 'organisation_id__isnull', 'opportunity_id')
              380  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              382  LOAD_METHOD              values

 L.1081       384  LOAD_STR                 'organisation_id'
              386  CALL_METHOD_1         1  '1 positional argument'
              388  LOAD_CONST               ('is_deleted', 'organisation_id__in')
              390  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              392  STORE_FAST               'customer_results'
          394_396  JUMP_FORWARD        702  'to 702'
            398_0  COME_FROM           340  '340'

 L.1083       398  LOAD_FAST                'destination'
              400  LOAD_STR                 'quote'
              402  COMPARE_OP               ==
          404_406  POP_JUMP_IF_FALSE   698  'to 698'

 L.1094       408  LOAD_GLOBAL              quote
              410  LOAD_ATTR                objects
              412  LOAD_ATTR                get
              414  LOAD_FAST                'location_id'
              416  LOAD_CONST               ('quote_id',)
              418  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              420  STORE_FAST               'quote_results'

 L.1096       422  LOAD_FAST                'quote_results'
              424  LOAD_ATTR                project_id
          426_428  POP_JUMP_IF_FALSE   466  'to 466'

 L.1097       430  LOAD_GLOBAL              customer
              432  LOAD_ATTR                objects
              434  LOAD_ATTR                filter

 L.1098       436  LOAD_STR                 'FALSE'

 L.1099       438  LOAD_GLOBAL              project
              440  LOAD_ATTR                objects
              442  LOAD_ATTR                get
              444  LOAD_FAST                'quote_results'
              446  LOAD_ATTR                project_id
              448  LOAD_ATTR                project_id
              450  LOAD_CONST               ('project_id',)
              452  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              454  LOAD_ATTR                organisation_id
              456  LOAD_ATTR                organisation_id
              458  LOAD_CONST               ('is_deleted', 'organisation_id')
              460  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              462  STORE_FAST               'customer_results'
              464  JUMP_FORWARD        696  'to 696'
            466_0  COME_FROM           426  '426'

 L.1101       466  LOAD_FAST                'quote_results'
              468  LOAD_ATTR                task_id
          470_472  POP_JUMP_IF_FALSE   552  'to 552'

 L.1109       474  LOAD_FAST                'quote_results'
              476  LOAD_ATTR                task_id
              478  LOAD_ATTR                organisation_id
          480_482  POP_JUMP_IF_FALSE   520  'to 520'

 L.1110       484  LOAD_GLOBAL              customer
              486  LOAD_ATTR                objects
              488  LOAD_ATTR                filter

 L.1111       490  LOAD_STR                 'FALSE'

 L.1112       492  LOAD_GLOBAL              task
              494  LOAD_ATTR                objects
              496  LOAD_ATTR                get
              498  LOAD_FAST                'quote_results'
              500  LOAD_ATTR                task_id
              502  LOAD_ATTR                task_id
              504  LOAD_CONST               ('task_id',)
              506  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              508  LOAD_ATTR                organisation_id
              510  LOAD_ATTR                organisation_id
              512  LOAD_CONST               ('is_deleted', 'organisation_id')
              514  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              516  STORE_FAST               'customer_results'
              518  JUMP_FORWARD        550  'to 550'
            520_0  COME_FROM           480  '480'

 L.1115       520  LOAD_GLOBAL              customer
              522  LOAD_ATTR                objects
              524  LOAD_ATTR                filter

 L.1116       526  LOAD_STR                 'FALSE'

 L.1117       528  LOAD_GLOBAL              task_customer
              530  LOAD_ATTR                objects
              532  LOAD_ATTR                filter

 L.1118       534  LOAD_STR                 'FALSE'

 L.1119       536  LOAD_FAST                'quote_results'
              538  LOAD_ATTR                task_id_id
              540  LOAD_CONST               ('is_deleted', 'task_id')
              542  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              544  LOAD_CONST               ('is_deleted', 'customer_id__in')
              546  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              548  STORE_FAST               'customer_results'
            550_0  COME_FROM           518  '518'
              550  JUMP_FORWARD        696  'to 696'
            552_0  COME_FROM           470  '470'

 L.1122       552  LOAD_FAST                'quote_results'
              554  LOAD_ATTR                opportunity_id
          556_558  POP_JUMP_IF_FALSE   630  'to 630'

 L.1123       560  LOAD_GLOBAL              opportunity
              562  LOAD_ATTR                objects
              564  LOAD_ATTR                get

 L.1124       566  LOAD_FAST                'quote_results'
              568  LOAD_ATTR                opportunity_id
              570  LOAD_ATTR                opportunity_id
              572  LOAD_CONST               ('opportunity_id',)
              574  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              576  STORE_FAST               'opportunity_results'

 L.1126       578  LOAD_FAST                'opportunity_results'
              580  LOAD_ATTR                organisation_id
          582_584  POP_JUMP_IF_FALSE   608  'to 608'

 L.1127       586  LOAD_GLOBAL              customer
              588  LOAD_ATTR                objects
              590  LOAD_ATTR                filter

 L.1128       592  LOAD_STR                 'FALSE'

 L.1129       594  LOAD_FAST                'opportunity_results'
              596  LOAD_ATTR                organisation_id
              598  LOAD_ATTR                organisation_id
              600  LOAD_CONST               ('is_deleted', 'organisation_id')
              602  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              604  STORE_FAST               'customer_results'
              606  JUMP_FORWARD        628  'to 628'
            608_0  COME_FROM           582  '582'

 L.1132       608  LOAD_GLOBAL              customer
              610  LOAD_ATTR                objects
              612  LOAD_ATTR                filter

 L.1133       614  LOAD_STR                 'FALSE'

 L.1134       616  LOAD_FAST                'opportunity_results'
              618  LOAD_ATTR                customer_id
              620  LOAD_ATTR                customer_id
              622  LOAD_CONST               ('is_deleted', 'customer_id')
              624  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              626  STORE_FAST               'customer_results'
            628_0  COME_FROM           606  '606'
              628  JUMP_FORWARD        696  'to 696'
            630_0  COME_FROM           556  '556'

 L.1136       630  LOAD_FAST                'quote_results'
              632  LOAD_ATTR                customer_id
          634_636  POP_JUMP_IF_FALSE   660  'to 660'

 L.1137       638  LOAD_GLOBAL              customer
              640  LOAD_ATTR                objects
              642  LOAD_ATTR                filter

 L.1138       644  LOAD_STR                 'FALSE'

 L.1139       646  LOAD_FAST                'quote_results'
              648  LOAD_ATTR                customer_id
              650  LOAD_ATTR                customer_id
              652  LOAD_CONST               ('is_deleted', 'customer_id')
              654  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              656  STORE_FAST               'customer_results'
              658  JUMP_FORWARD        696  'to 696'
            660_0  COME_FROM           634  '634'

 L.1141       660  LOAD_FAST                'quote_results'
              662  LOAD_ATTR                organisation_id
          664_666  POP_JUMP_IF_FALSE   688  'to 688'

 L.1142       668  LOAD_GLOBAL              customer
              670  LOAD_ATTR                objects
              672  LOAD_ATTR                filter

 L.1143       674  LOAD_STR                 'FALSE'

 L.1144       676  LOAD_FAST                'quote_results'
              678  LOAD_ATTR                organisation_id
              680  LOAD_CONST               ('is_deleted', 'organisation_id')
            682_0  COME_FROM           212  '212'
              682  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              684  STORE_FAST               'customer_results'
              686  JUMP_FORWARD        696  'to 696'
            688_0  COME_FROM           664  '664'

 L.1147       688  LOAD_GLOBAL              print
              690  LOAD_STR                 'SOMETHING FUCKED UP!!!'
              692  CALL_FUNCTION_1       1  '1 positional argument'
              694  POP_TOP          
            696_0  COME_FROM           686  '686'
            696_1  COME_FROM           658  '658'
            696_2  COME_FROM           628  '628'
            696_3  COME_FROM           550  '550'
            696_4  COME_FROM           464  '464'
              696  JUMP_FORWARD        702  'to 702'
            698_0  COME_FROM           404  '404'

 L.1149       698  LOAD_STR                 ''
              700  STORE_FAST               'customer_results'
            702_0  COME_FROM           696  '696'
            702_1  COME_FROM           394  '394'
            702_2  COME_FROM           330  '330'
            702_3  COME_FROM           230  '230'
            702_4  COME_FROM           150  '150'
            702_5  COME_FROM            76  '76'

 L.1151       702  LOAD_FAST                'customer_results'
              704  LOAD_FAST                'self'
              706  LOAD_ATTR                fields
              708  LOAD_STR                 'to_email'
              710  BINARY_SUBSCR    
              712  STORE_ATTR               queryset

 L.1152       714  LOAD_FAST                'customer_results'
              716  LOAD_FAST                'self'
              718  LOAD_ATTR                fields
              720  LOAD_STR                 'cc_email'
              722  BINARY_SUBSCR    
              724  STORE_ATTR               queryset

 L.1153       726  LOAD_FAST                'customer_results'
              728  LOAD_FAST                'self'
              730  LOAD_ATTR                fields
              732  LOAD_STR                 'bcc_email'
              734  BINARY_SUBSCR    
              736  STORE_ATTR               queryset

Parse error at or near `COME_FROM' instruction at offset 682_0

    organisation_email = forms.EmailField(max_length=200,
      required=False,
      widget=forms.TextInput(attrs={'style':'display: none;', 
     'class':'form-control'}))
    to_email = forms.ModelMultipleChoiceField(queryset=(customer.objects.all()),
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 90%'}))
    cc_email = forms.ModelMultipleChoiceField(required=False,
      queryset=(customer.objects.all()),
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 90%'}))
    bcc_email = forms.ModelMultipleChoiceField(required=False,
      queryset=(customer.objects.all()),
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 90%'}))
    email_subject = forms.CharField(required=True,
      max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Email Subject', 
     'class':'form-control col-md-11'}))
    email_content = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Email content', 
     'class':'form-control'}))
    is_private = forms.BooleanField(required=False,
      widget=forms.CheckboxInput(attrs={}))
    email_quote = forms.BooleanField(required=False,
      widget=forms.CheckboxInput(attrs={}))
    quote_template_description = forms.ModelChoiceField(queryset=quote_template.objects.filter(is_deleted='FALSE'),
      empty_label=None,
      required=False,
      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = customer
        fields = {}


class email_information_form(ModelForm):
    email_subject = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control col-md-11'}))
    email_content = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'readonly':1},
      attrs={'placeholder':'Email content', 
     'class':'form-control'}))

    class Meta:
        model = email_content
        fields = {
         'email_subject',
         'email_content'}


class group_form(ModelForm):

    def __init__(self, *args, **kwargs):
        group_id = kwargs.pop('group_id')
        (super(group_form, self).__init__)(*args, **kwargs)
        group_results = group.objects.filter(is_deleted='FALSE').exclude(group_id=group_id)
        self.fields['parent_group'].queryset = group_results

    group_name = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'placeholder':'Group Name', 
     'class':'form-control'}))
    parent_group = forms.ModelChoiceField(queryset=(group.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}),
      required=False)

    class Meta:
        model = group
        fields = {
         'group_name',
         'parent_group'}


class information_customer_contact_history_form(forms.Form):
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')
    contact_type = forms.ModelChoiceField(label='Contact Type',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=contact_type_results,
      empty_label=None)
    contact_attachment = forms.FileField(required=False,
      widget=forms.FileInput(attrs={'onChange': 'enable_submit()'}))
    contact_history = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Opportunity Description', 
     'class':'form-control'}),
      required=False)
    contact_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'style':'width: 200px', 
     'class':'form-control'}))


class information_organisation_contact_history_form(forms.Form):
    contact_type_results = list_of_contact_type.objects.filter(is_deleted='FALSE')
    contact_type = forms.ModelChoiceField(label='Contact Type',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=contact_type_results,
      empty_label=None)
    contact_history = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Opportunity Description', 
     'class':'form-control'}),
      required=False)
    contact_attachment = forms.FileField(required=False,
      widget=forms.FileInput(attrs={'onChange': 'enable_submit()'}))
    contact_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'style':'width: 200px', 
     'class':'form-control'}))


class information_project_history_form(ModelForm):
    project_history = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder': 'Project Description'}))

    class Meta:
        model = project_history
        fields = {
         'project_history'}


class information_task_history_form(ModelForm):
    task_history = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder': 'Project Description'}))

    class Meta:
        model = task_history
        fields = {
         'task_history'}


class kanban_card_form(ModelForm):

    def __init__(self, *args, **kwargs):
        kanban_board_id = kwargs.pop('kanban_board_id')
        (super(kanban_card_form, self).__init__)(*args, **kwargs)
        self.fields['kanban_column'].queryset = kanban_column.objects.filter(kanban_board=kanban_board_id)
        self.fields['kanban_level'].queryset = kanban_level.objects.filter(kanban_board=kanban_board_id)

    kanban_card_comment = forms.CharField(required=False,
      widget=TextInput(attrs={'placeholder':'Card Comments', 
     'class':'form-control'}))
    kanban_card_text = forms.CharField(required=True,
      max_length=255,
      widget=TextInput(attrs={'placeholder':'Card Text', 
     'class':'form-control', 
     'onkeydown':'new_card_text_changed()', 
     'onchange':'new_card_text_changed()'}))
    kanban_column = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=0)
    kanban_level = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=0)

    class Meta:
        model = kanban_card
        fields = {
         'kanban_card_text',
         'kanban_column',
         'kanban_level'}


class kanban_board_form(forms.Form):
    group_results = group.objects.filter(is_deleted='FALSE')
    kanban_board_name = forms.CharField(max_length=255,
      widget=TextInput(attrs={'placeholder':'Board Name', 
     'class':'form-control'}))
    kanban_board_column = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Please place each new column on a new line. Each name will be truncated to 255 characters', 
     'class':'form-control'}),
      required=True)
    kanban_board_level = forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Please place each new level on a new line. Each name will be truncated to 255 characters', 
     'class':'form-control'}),
      required=True)
    select_groups = forms.ModelMultipleChoiceField(queryset=group_results,
      required=True,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 100%'}))


class kanban_edit_xy_name_form(forms.Form):
    kanban_xy_name = forms.CharField(max_length=50,
      widget=TextInput(attrs={'placeholder': 'Column/Level Name'}))


class kanban_properties_form(ModelForm):
    kanban_board_name = forms.CharField(max_length=255,
      widget=TextInput(attrs={'placeholder':'Board Name', 
     'class':'form-control'}),
      required=True)

    class Meta:
        model = kanban_board
        fields = {
         'kanban_board_name'}


class kanban_new_link_form(ModelForm):

    def __init__(self, *args, **kwargs):
        kanban_board_id = kwargs.pop('kanban_board_id')
        (super(kanban_new_link_form, self).__init__)(*args, **kwargs)
        self.fields['kanban_column'].queryset = kanban_column.objects.filter(kanban_board=kanban_board_id)
        self.fields['kanban_level'].queryset = kanban_level.objects.filter(kanban_board=kanban_board_id)
        self.fields['kanban_column'].empty_label = None
        self.fields['kanban_level'].empty_label = None

    kanban_column = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))
    kanban_level = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = kanban_card
        fields = {
         'kanban_column',
         'kanban_level'}


class kudos_form(ModelForm):
    kudos_rating = forms.ChoiceField(widget=forms.RadioSelect(attrs={'style': 'list-style: none;'}),
      choices=RATING_SCORE)
    improvement_note = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder': 'Improvement Note'}),
      required=False)
    liked_note = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder': 'Liked Note'}),
      required=False)
    project_description = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder': 'Project Description'}),
      required=False)

    class Meta:
        model = kudos
        fields = {
         'kudos_rating',
         'extra_kudos',
         'improvement_note',
         'liked_note'}


class kudos_read_only_form(ModelForm):
    improvement_note = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder': 'Improvement Note'}),
      required=False)
    liked_note = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder': 'Liked Note'}),
      required=False)
    project_description = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder': 'Project Description'}),
      required=False)

    class Meta:
        model = kudos
        fields = {
         'improvement_note',
         'liked_note'}


class list_of_tax_form(ModelForm):
    tax_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    tax_description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = list_of_tax
        fields = {
         'tax_amount',
         'tax_description'}


class login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 
     'class':'form-control', 
     'required':True, 
     'autofocus':True}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password', 
     'class':'form-control', 
     'required':True}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username:
            if password:
                user = authenticate(username=username, password=password)
                if user:
                    raise user.check_password(password) or forms.ValidationError('The login details are incorrect')
                elif not user.is_active:
                    raise forms.ValidationError('Please contact your system administrator. Your account has been disabled')
                try:
                    if (permission_set.objects.filter(permission_set_id=1).count() == 0 or user_group.objects.filter(username_id=(user.id), is_deleted='FALSE').count()) == 0:
                        raise forms.ValidationError('Please contact your system administrator. Your account has no group access')
                    else:
                        print('Currently the user has been setup with: ' + str(user_group.objects.filter(username_id=(user.id), is_deleted='FALSE').count()) + ' user group')
                except ObjectDoesNotExist:
                    print('First time setup ' + str(datetime.datetime.now()))

        return super(login_form, self).clean()


class my_profile_form(ModelForm):
    password1 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'type':'password', 
     'placeholder':'Password', 
     'onkeyup':'enable_submit()', 
     'autocomplete':'off', 
     'class':'form-control'}))
    password2 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'type':'password', 
     'placeholder':'Repeate Password', 
     'onkeyup':'enable_submit()', 
     'autocomplete':'off', 
     'class':'form-control'}))
    first_name = forms.CharField(max_length=100,
      widget=forms.TextInput(attrs={'placeholder':'First Name', 
     'class':'form-control'}))
    last_name = forms.CharField(max_length=100,
      widget=forms.TextInput(attrs={'placeholder':'Last Name', 
     'class':'form-control'}))
    email = forms.EmailField(max_length=100,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Email Address', 
     'class':'form-control'}))

    class Meta:
        model = User
        fields = {
         'first_name',
         'last_name',
         'email'}


class new_campus_form(forms.Form):
    campus_nickname = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Campus Nickname i.e Melbourne', 
     'class':'form-control'}))
    campus_address1 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 1', 
     'class':'form-control'}))
    campus_address2 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 2', 
     'class':'form-control'}))
    campus_address3 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Address 3', 
     'class':'form-control'}))
    campus_suburb = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Suburb', 
     'class':'form-control'}))
    country_and_region = forms.ModelChoiceField(required=False,
      queryset=list_of_country.objects.filter(is_deleted='FALSE'),
      empty_label='Please pick a Country/Region',
      widget=RegionSelect(attrs={'class':'form-control', 
     'tag':forms.HiddenInput(), 
     'style':'width: 100%'}))


class new_change_task_form(ModelForm):

    def __init__(self, *args, **kwargs):
        rfc_id = kwargs.pop('rfc_id')
        (super(new_change_task_form, self).__init__)(*args, **kwargs)
        user_results = User.objects.filter(is_active=True,
          id__in=(user_group.objects.filter(is_deleted='FALSE',
          group_id__in=(object_assignment.objects.filter(is_deleted='FALSE',
          request_for_change=rfc_id).values('group_id'))).values('username')))
        self.fields['change_task_assigned_user'].queryset = user_results
        self.fields['change_task_qa_user'].queryset = user_results

    change_task_title = forms.CharField(max_length=255,
      required=True,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    change_task_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control change_task_description'}))
    change_task_start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    change_task_end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    change_task_assigned_user = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))
    change_task_qa_user = forms.ModelChoiceField(queryset=None,
      widget=forms.Select(attrs={'class': 'form-control'}))
    change_task_required_by = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}),
      initial='Stakeholder(s)')

    class Meta:
        model = change_task
        fields = {
         'change_task_title',
         'change_task_description',
         'change_task_start_date',
         'change_task_end_date',
         'change_task_assigned_user',
         'change_task_qa_user',
         'change_task_required_by'}


class new_customer_form(forms.Form):
    titles_results = list_of_title.objects.all()
    organisations_results = organisation.objects.filter(is_deleted='FALSE')
    customer_title = forms.ModelChoiceField(label='Title',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=titles_results)
    customer_first_name = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'placeholder':'First Name', 
     'class':'form-control'}))
    customer_last_name = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'placeholder':'Last Name', 
     'class':'form-control'}))
    customer_email = forms.EmailField(max_length=200,
      widget=forms.TextInput(attrs={'placeholder':'customer@email.com', 
     'type':'email', 
     'class':'form-control'}))
    organisation_id = forms.ModelChoiceField(label='Organisation',
      widget=Select2Widget(attrs={'class': 'form-control'}),
      queryset=organisations_results,
      required=False)


class new_folder_form(forms.Form):
    folder_description = forms.CharField(max_length=255,
      required=True,
      widget=forms.TextInput(attrs={'placeholder':'Folder Description', 
     'class':'form-control'}))


class new_group_form(ModelForm):
    group_name = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'placeholder':'Group Name'}))
    parent_group = forms.ModelChoiceField(queryset=group.objects.filter(is_deleted='FALSE'),
      widget=forms.Select(attrs={'class': 'form-control'}),
      required=False)

    class Meta:
        model = group
        fields = {
         'group_name',
         'parent_group'}


class new_line_item_form(ModelForm):

    def __init__(self, *args, **kwargs):
        (super(new_line_item_form, self).__init__)(*args, **kwargs)
        product_and_service_results = product_and_service.objects.filter(is_deleted='FALSE')
        product_results = product_and_service_results.filter(product_or_service='Product')
        service_results = product_and_service_results.filter(product_or_service='Service')
        product_turple = ''
        service_turple = ''
        product_or_service_choices = ()
        print('TURPLE START')
        product_list = []
        for product in product_results:
            single_item = (product.product_id, product.product_name)
            product_list.append(single_item)

        service_list = []
        for service in service_results:
            single_item = (service.product_id, service.product_name)
            service_list.append(single_item)

        if not len(product_list) > 0:
            product_or_service_choices = service_list > 0 or (
             ('------', 'Please select a product or service'),
             (
              'Products', tuple(product_list)),
             (
              'Services', tuple(service_list)))
        else:
            if len(product_list) > 0:
                product_or_service_choices = (('------', 'Please select a product'),
                 (
                  'Products', tuple(product_list)))
            else:
                if len(service_list) > 0:
                    product_or_service_choices = (('------', 'Please select a service'),
                     (
                      'Services', tuple(service_list)))
                else:
                    product_or_service_choices = ('------', 'Please select a product or service')
        self.fields['product_and_service'].choices = product_or_service_choices

    product_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'value':'1', 
     'onkeyup':'update_total()', 
     'class':'form-control'}))
    product_price = forms.CharField(widget=forms.TextInput(attrs={'readonly':True, 
     'style':'background-color: aliceblue', 
     'class':'form-control'}))
    product_and_service = forms.ChoiceField(required=True,
      choices=(),
      widget=Select2Widget(attrs={'class': 'form-control'}))
    discount_amount = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'style':'background-color: aliceblue', 
     'step':'1', 
     'onkeyup':'update_total()', 
     'readonly':True, 
     'class':'form-control'}))
    discount_choice = forms.ChoiceField(choices=DISCOUNT_CHOICE,
      widget=forms.Select(attrs={'onchange':'discount_type_change()', 
     'class':'form-control'}))
    discount_percent = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'min':'0', 
     'max':'100', 
     'step':'5', 
     'onchange':'update_total()', 
     'class':'form-control'}))
    sales_price = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'step':'1', 
     'readonly':'true', 
     'style':'background-color: aliceblue', 
     'class':'form-control'}))
    tax_amount = forms.CharField(widget=forms.TextInput(attrs={'readonly':'true', 
     'width':'50px', 
     'value':'0', 
     'step':'1', 
     'style':'background-color: aliceblue', 
     'class':'form-control'}))
    tax = forms.ModelChoiceField(required=False,
      label='Organisations',
      queryset=list_of_tax.objects.filter(is_deleted='FALSE'),
      widget=forms.Select(attrs={'onChange':'update_total()', 
     'class':'form-control'}))
    total = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'readonly':True, 
     'width':'100px', 
     'value':'0', 
     'style':'background-color: aliceblue', 
     'class':'form-control'}))
    product_note = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Product Notes', 
     'class':'form-control'}))

    class Meta:
        model = quote_product_and_service
        fields = '__all__'
        exclude = {
         'quotes_products_and_services_id',
         'quote',
         'customer_id',
         'date_created',
         'date_modified',
         'user_id',
         'is_deleted',
         'change_user',
         'product_cost',
         'discount_percent',
         'product_and_service'}


class new_opportunity_form(ModelForm):
    opportunity_stage_results = list_of_opportunity_stage.objects.filter(is_deleted='FALSE')
    amount_type_results = list_of_amount_type.objects.filter(is_deleted='FALSE')
    groups_results = group.objects.filter(is_deleted='FALSE')
    user_results = auth.models.User.objects.all()
    currency_id = forms.ModelChoiceField(queryset=(list_of_currency.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    lead_source_id = forms.ModelChoiceField(queryset=(list_of_lead_source.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity_success_probability = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    opportunity_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_type_id = forms.ModelChoiceField(queryset=(list_of_amount_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Opportunity Name', 
     'class':'form-control'}))
    opportunity_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Opportunity Description', 
     'class':'form-control'}))
    opportunity_expected_close_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    amount_type_id = forms.ModelChoiceField(label='Amount Type',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=amount_type_results)
    select_groups = forms.ModelMultipleChoiceField(queryset=groups_results,
      required=False,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0'}))
    select_users = forms.ModelMultipleChoiceField(queryset=user_results,
      required=False,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0'}))

    class Meta:
        model = opportunity
        fields = '__all__'
        exclude = {
         'opportunity_stage_id',
         'date_created',
         'date_modified',
         'user_id',
         'is_deleted',
         'change_user'}


class new_organisation_form(forms.Form):
    organisation_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':"Organisation's Name", 
     'class':'form-control'}))
    organisation_website = forms.URLField(initial='https://',
      max_length=255,
      widget=forms.URLInput(attrs={'class':'form-control', 
     'placeholder':'https://organisation_website.com', 
     'onblur':'check_url()'}))
    organisation_email = forms.EmailField(max_length=255,
      widget=forms.EmailInput(attrs={'class':'form-control', 
     'placeholder':'organisation@email.com', 
     'type':'email'}))


class new_project_form(forms.Form):
    organisations_results = organisation.objects.filter(is_deleted='FALSE')
    group_results = group.objects.filter(is_deleted='FALSE')
    project_permission = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(attrs={'placeholder':'Select Groups to Assign to Project', 
     'class':'form-control', 
     'multiple tabindex':'0'}),
      required=True,
      queryset=group_results)
    project_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Project Name', 
     'class':'form-control'}))
    project_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Project Description', 
     'class':'form-control'}))
    organisation_id = forms.ModelChoiceField(label='Organisation',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=organisations_results,
      required=False)
    project_start_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    project_end_date = forms.DateTimeField(initial=(datetime.datetime.now() + datetime.timedelta(days=31)),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    project_story_point = forms.IntegerField(initial=1,
      min_value=1,
      max_value=100,
      widget=forms.NumberInput(attrs={'class':'form-control', 
     'onChange':'update_story_point()'}))

    class Meta:
        model = project
        fields = {
         'project_name',
         'project_description',
         'organisation_id',
         'project_start_date',
         'project_end_date'}


class new_quote_form(ModelForm):
    groups_results = group.objects.filter(is_deleted='FALSE')
    user_results = auth.models.User.objects.all()
    list_of_quote_stages = list_of_quote_stage.objects.filter(is_deleted='FALSE',
      is_invoice='FALSE')
    quote_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Quote Title', 
     'class':'form-control'}))
    quote_valid_till = forms.DateTimeField(initial=(datetime.datetime.now() + datetime.timedelta(days=31)),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    quote_stage_id = forms.ModelChoiceField(label='Quote Stage',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=list_of_quote_stages)
    quote_terms = forms.CharField(widget=TinyMCE(mce_attrs={'style': 'width: 100%'},
      attrs={'placeholder':'Quote Terms', 
     'class':'form-control'}))
    customer_notes = forms.CharField(widget=TinyMCE(mce_attrs={'style': 'width: 100%'},
      attrs={'placeholder':'Customer Notes', 
     'class':'form-control'}),
      required=False)
    select_groups = forms.ModelMultipleChoiceField(queryset=groups_results,
      required=True,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 100%'}))

    class Meta:
        model = quote
        fields = {
         'quote_title',
         'quote_stage_id',
         'quote_terms',
         'customer_notes',
         'quote_valid_till'}


class new_request_for_change_form(ModelForm):
    __doc__ = '\n    The request for change text has been truncated to rfc_ as the field names were too long.\n    '
    rfc_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_summary = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_type = forms.ChoiceField(choices=RFC_TYPE,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_implementation_start_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_end_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_release_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_version_number = forms.CharField(max_length=25,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'placeholder':'Version/Release Number'}),
      required=False)
    rfc_lead = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True),
      widget=Select2Widget(attrs={'class': 'form-control'}),
      required=True)
    rfc_priority = forms.ChoiceField(choices=RFC_PRIORITY,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_risk = forms.ChoiceField(choices=RFC_RISK,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_impact = forms.ChoiceField(choices=RFC_IMPACT,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_risk_and_impact_analysis = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_backout_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_test_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_permission = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(attrs={'placeholder':'Select Groups to Assign to Request for Change', 
     'class':'form-control', 
     'multiple tabindex':'0'}),
      required=True,
      queryset=group.objects.filter(is_deleted='FALSE'))

    class Meta:
        model = request_for_change
        exclude = [
         'change_user',
         'is_deleted',
         'rfc_status']


class new_requirement_item_form(ModelForm):
    requirement_item_status_results = list_of_requirement_item_status.objects.filter(is_deleted='FALSE')
    requirement_item_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Requirement Item Title', 
     'class':'form-control'}))
    requirement_item_scope = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))
    requirement_item_status = forms.ModelChoiceField(label='Quote Stage',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=requirement_item_status_results)
    requirement_item_type = forms.ModelChoiceField(queryset=(list_of_requirement_item_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement_item_story_point = forms.IntegerField(initial=1,
      min_value=1,
      max_value=100,
      widget=forms.NumberInput(attrs={'class':'form-control', 
     'onChange':'update_story_point()'}))

    class Meta:
        model = requirement_item
        fields = {
         'requirement_item_title',
         'requirement_item_scope',
         'requirement_item_type'}


class new_requirement_form(ModelForm):
    requirement_status_results = list_of_requirement_status.objects.filter(is_deleted='FALSE',
      requirement_status_is_closed='FALSE')
    groups_results = group.objects.filter(is_deleted='FALSE')
    organisation_results = organisation.objects.filter(is_deleted='FALSE')
    requirement_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Requirement Title', 
     'class':'form-control'}))
    requirement_scope = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))
    requirement_status = forms.ModelChoiceField(label='Quote Stage',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=requirement_status_results)
    requirement_permission = forms.ModelMultipleChoiceField(queryset=groups_results,
      required=True,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 100%'}))
    requirement_type = forms.ModelChoiceField(queryset=(list_of_requirement_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    organisation = forms.ModelChoiceField(queryset=organisation_results,
      widget=forms.Select(attrs={'class': 'form-control'}),
      required=False)

    class Meta:
        model = requirement
        fields = {
         'requirement_title',
         'requirement_scope',
         'requirement_type',
         'requirement_status'}


class new_tag_form(forms.Form):
    tag_name = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'class':'form-control col-md-10', 
     'placeholder':'Submit Tag', 
     'list':'tag_list'}))


class new_task_form(forms.Form):
    organisations_results = organisation.objects.filter(is_deleted='FALSE')
    group_results = group.objects.filter(is_deleted='FALSE')
    task_permission = forms.ModelMultipleChoiceField(widget=Select2MultipleWidget(attrs={'placeholder':'Select Groups to Assign to Project', 
     'class':'form-control', 
     'multiple tabindex':'0'}),
      required=True,
      queryset=group_results)
    task_short_description = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Task Short Description', 
     'class':'form-control'}))
    task_long_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Task Long Description', 
     'class':'form-control'}))
    organisation_id = forms.ModelChoiceField(label='Organisation',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=organisations_results,
      required=False)
    task_start_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    task_end_date = forms.DateTimeField(initial=(datetime.datetime.now() + datetime.timedelta(days=31)),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    task_story_point = forms.IntegerField(initial=1,
      min_value=1,
      max_value=100,
      widget=forms.NumberInput(attrs={'class':'form-control', 
     'onChange':'update_story_point()'}))


class new_timesheet_row(forms.Form):
    timesheet_description = forms.CharField(required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    timesheet_date = forms.DateField(required=True,
      initial=(datetime.datetime.now()),
      widget=forms.DateInput(attrs={'class': 'form-control'}))
    timesheet_start_time = forms.TimeField(required=True,
      widget=forms.TimeInput(attrs={'class': 'form-control'}))
    timesheet_end_time = forms.TimeField(required=True,
      widget=forms.TimeInput(attrs={'class': 'form-control'}))


class new_whiteboard_form(forms.Form):
    whiteboard_name = forms.CharField(max_length=255,
      required=True,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'placeholder':'Enter Whiteboard Name'}))


class opportunity_group_permission_form(forms.Form):

    def __init__(self, *args, **kwargs):
        group_results = kwargs.pop('group_results')
        (super(opportunity_group_permission_form, self).__init__)(*args, **kwargs)
        self.fields['group'].queryset = group_results

    group = forms.ModelChoiceField(required=True,
      queryset=group.objects.filter(is_deleted='BLANK'))


class opportunity_close_form(forms.Form):
    opportunity_close = forms.ModelChoiceField(queryset=list_of_opportunity_stage.objects.filter(is_deleted='FALSE',
      opportunity_closed='TRUE'),
      widget=forms.Select(attrs={'class': 'form-control'}))


class opportunity_information_form(ModelForm):
    groups_results = group.objects.filter(is_deleted='FALSE')
    user_results = auth.models.User.objects.all()
    opportunity_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    opportunity_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Opportunity Description', 
     'class':'form-control'}))
    opportunity_expected_close_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    next_step = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    select_groups = forms.ModelMultipleChoiceField(queryset=groups_results,
      required=False,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0'}))
    select_users = forms.ModelMultipleChoiceField(queryset=user_results,
      required=False,
      widget=Select2MultipleWidget(attrs={'placeholder':'Choose the users(s)', 
     'class':'form-control', 
     'multiple tabindex':'0', 
     'style':'width: 100%'}))
    currency_id = forms.ModelChoiceField(queryset=(list_of_currency.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity_amount = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    amount_type_id = forms.ModelChoiceField(queryset=(list_of_amount_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity_stage_id = forms.ModelChoiceField(queryset=(list_of_opportunity_stage.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity_success_probability = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = opportunity
        fields = '__all__'
        exclude = {
         'lead_source_id',
         'date_created',
         'date_modified',
         'user_id',
         'is_deleted',
         'change_user'}


class opportunity_readonly_form(forms.Form):
    opportunity_description = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder':'Opportunity Description', 
     'class':'form-control'}))


class organisation_information_form(ModelForm):
    organisation_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    organisation_website = forms.URLField(max_length=255,
      widget=forms.URLInput(attrs={'class': 'form-control'}))
    organisation_email = forms.EmailField(max_length=255,
      widget=forms.EmailInput(attrs={'class': 'form-control'}))
    update_profile_picture = forms.ImageField(required=False)
    document = forms.FileField(required=False)

    class Meta:
        model = organisation
        fields = {
         'organisation_name',
         'organisation_website',
         'organisation_email'}

    def clean_update_profile_picture(self):
        profile_picture = self.cleaned_data['update_profile_picture']
        try:
            picture_errors = ''
            main, sub = profile_picture.content_type.split('/')
            if not (main == 'image' and sub in ('jpeg', 'gif', 'png')):
                picture_errors += 'Please use a JPEG, GIF or PNG image'
            if len(profile_picture) > MAX_PICTURE_SIZE:
                picture_errors += '\nPicture profile exceeds 400kb'
            if not picture_errors == '':
                raise forms.ValidationError(picture_errors)
        except AttributeError:
            pass

        return profile_picture


class organisation_readonly_form(ModelForm):
    organisation_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'readonly':True}))
    organisation_website = forms.URLField(max_length=255,
      widget=forms.URLInput(attrs={'class':'form-control', 
     'readonly':True}))
    bug_fixing_field = forms.CharField(widget=TinyMCE(attrs={}))

    class Meta:
        model = organisation
        fields = {
         'organisation_name',
         'organisation_website'}


class opportunity_user_permission_form(forms.Form):

    def __init__(self, *args, **kwargs):
        user_results = kwargs.pop('user_results')
        (super(opportunity_user_permission_form, self).__init__)(*args, **kwargs)
        self.fields['user'].queryset = user_results

    user = forms.ModelChoiceField(required=True,
      queryset=User.objects.filter(username=None))


class permission_set_form(ModelForm):
    permission_set_name = forms.CharField(max_length=255,
      label='',
      widget=forms.TextInput(attrs={'placeholder':'Permission Set Name', 
     'class':'form-control'}))
    administration_assign_user_to_group = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    administration_create_group = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    administration_create_permission_set = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    administration_create_user = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    assign_campus_to_customer = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    associate_project_and_task = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    bug = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    bug_client = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    customer = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    email = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    invoice = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    invoice_product = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    kanban = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    kanban_card = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    opportunity = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    organisation = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    organisation_campus = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    project = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    quote = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    request_for_change = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement_link = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    tag = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    task = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    tax = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    template = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    whiteboard = forms.ChoiceField(choices=PERMISSION_LEVEL,
      widget=forms.Select(attrs={'class': 'form-control'}))
    contact_history = forms.ChoiceField(choices=PERMISSION_BOOLEAN,
      widget=forms.Select(attrs={'class': 'form-control'}))
    document = forms.ChoiceField(choices=PERMISSION_BOOLEAN,
      widget=forms.Select(attrs={'class': 'form-control'}))
    kanban_comment = forms.ChoiceField(choices=PERMISSION_BOOLEAN,
      widget=forms.Select(attrs={'class': 'form-control'}))
    project_history = forms.ChoiceField(choices=PERMISSION_BOOLEAN,
      widget=forms.Select(attrs={'class': 'form-control'}))
    task_history = forms.ChoiceField(choices=PERMISSION_BOOLEAN,
      widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = permission_set
        exclude = {
         'date_created',
         'date_modified',
         'change_user',
         'is_deleted'}


class product_and_service_form(ModelForm):
    product_or_service = forms.ChoiceField(choices=PRODUCT_OR_SERVICE,
      widget=forms.Select(attrs={'class': 'form-control'}))
    product_cost = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    product_price = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    product_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Product/Service Name', 
     'class':'form-control'}))
    product_part_number = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Product/Service Part Number', 
     'class':'form-control'}))
    product_description = forms.CharField(required=False,
      widget=forms.Textarea(attrs={'placeholder':'Product/Service Description', 
     'class':'form-control'}))

    class Meta:
        model = product_and_service
        fields = '__all__'
        exclude = {
         'is_deleted',
         'change_user'}


class project_history_readonly_form(ModelForm):

    def __init__(self, *args, **kwargs):
        project_history_id = kwargs.pop('project_history_id', None)
        (super(project_history_readonly_form, self).__init__)(*args, **kwargs)
        self.fields['project_history'].widget = TinyMCE(mce_attrs={'width':'100%', 
         'toolbar':False, 
         'menubar':False, 
         'readonly':1},
          attrs={'placeholder':'Requirement Scope', 
         'id':'id_project_history_' + str(project_history_id)})

    project_history = forms.CharField()
    submit_history = forms.CharField(widget=TextInput(attrs={'readonly':True, 
     'class':'form-control'}))

    class Meta:
        model = project_history
        fields = {
         'project_history'}


class project_information_form(ModelForm):
    __doc__ = '\n    Project information will need to abide by the stricked laws of the new\n    project datetime edits!!\n    '
    project_name = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    document = forms.FileField(required=False,
      widget=forms.FileInput(attrs={'onChange':'enable_submit()', 
     'class':'form-control'}))
    document_url_location = forms.URLField(required=False,
      widget=forms.TextInput(attrs={'placeholder':'https://example.com', 
     'onChange':'enable_submit()', 
     'class':'form-control'}))
    document_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'width':'100%', 
     'onkeyup':'enable_submit()', 
     'class':'form-control'}))
    folder_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'width':'100%', 
     'onkeyup':'enable_submit()', 
     'class':'form-control'}))
    project_description = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Please Enter your project description', 
     'class':'form-control'}))
    project_start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    project_end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = project
        fields = {
         'project_name',
         'project_description',
         'project_start_date',
         'project_end_date'}


class project_readonly_form(ModelForm):
    project_description = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))

    class Meta:
        model = project
        fields = {
         'project_description'}


class quote_information_form(ModelForm):

    def __init__(self, *args, **kwargs):
        quote_instance = kwargs.pop('quote_instance', None)
        (super(quote_information_form, self).__init__)(*args, **kwargs)
        if quote_instance.organisation_id:
            campus_results = campus.objects.filter(is_deleted='FALSE',
              organisation_id=(quote_instance.organisation_id))
        else:
            if quote_instance.customer_id:
                campus_results = campus.objects.filter(is_deleted='FALSE',
                  customer_id=(quote_instance.customer_id))
            else:
                campus_results = campus.objects.filter(pk=0)
        self.fields['quote_billing_address'].queryset = campus_results

    list_of_quote_stages = list_of_quote_stage.objects.filter(is_deleted='FALSE')
    quote_billing_address = forms.ModelChoiceField(required=False,
      queryset=(campus.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    quote_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Quote Title', 
     'class':'form-control'}))
    quote_valid_till = forms.DateTimeField(initial=(datetime.datetime.now() + datetime.timedelta(days=31)),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    quote_stage_id = forms.ModelChoiceField(label='Quote Stage',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=list_of_quote_stages)
    quote_terms = forms.CharField(widget=TinyMCE(mce_attrs={'style': 'width: 100%;'},
      attrs={'placeholder':'Quote Terms', 
     'class':'form-control'}))
    customer_notes = forms.CharField(widget=TinyMCE(mce_attrs={'style': 'width: 100%'},
      attrs={'placeholder':'Customer Notes', 
     'class':'form-control'}),
      required=False)
    hidden_select = forms.ChoiceField(required=False,
      choices=(),
      widget=Select2Widget(attrs={'class': 'form-control'}))

    class Meta:
        model = quote
        fields = {
         'quote_title',
         'quote_stage_id',
         'quote_terms',
         'customer_notes',
         'quote_valid_till'}


class quote_readonly_form(forms.Form):
    quote_terms = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))
    customer_notes = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))


class quote_template_form(ModelForm):
    quote_template_description = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Quote Template Description', 
     'class':'form-control'}))
    template_css = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    payment_terms = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    notes = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    page_layout = forms.ChoiceField(choices=PAGE_LAYOUT,
      widget=forms.Select(attrs={'class': 'form-control'}))
    margin_left = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    margin_right = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    margin_top = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    margin_bottom = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    margin_header = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    margin_footer = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    header = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Please Enter Template Header', 
     'class':'form-control'}))

    class Meta:
        model = quote_template
        exclude = {
         'date_created',
         'date_modified',
         'change_user',
         'is_deleted',
         'product_line',
         'service_line'}


class search_form(forms.Form):
    search_for = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Search', 
     'class':'form-control'}))


class request_for_change_form(ModelForm):
    __doc__ = '\n    The request for change text has been truncated to rfc_ as the field names were too long.\n    '
    rfc_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_summary = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_type = forms.ChoiceField(choices=RFC_TYPE,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_implementation_start_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_end_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_release_date = forms.DateTimeField(initial=(datetime.datetime.now()),
      widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
      required=True)
    rfc_version_number = forms.CharField(max_length=25,
      widget=forms.TextInput(attrs={'class':'form-control', 
     'placeholder':'Version/Release Number'}),
      required=False)
    rfc_lead = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True),
      widget=Select2Widget(attrs={'class': 'form-control'}),
      required=True)
    rfc_priority = forms.ChoiceField(choices=RFC_PRIORITY,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_risk = forms.ChoiceField(choices=RFC_RISK,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_impact = forms.ChoiceField(choices=RFC_IMPACT,
      required=True,
      widget=forms.Select(attrs={'class': 'form-control'}),
      initial=1)
    rfc_risk_and_impact_analysis = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_backout_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_test_plan = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'class': 'form-control'}),
      required=True)

    class Meta:
        model = request_for_change
        exclude = [
         'change_user',
         'is_deleted',
         'rfc_status']


class request_for_change_note_form(ModelForm):
    rfc_note = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 
     'style':'height: 80px;'}),
      required=False)

    class Meta:
        model = request_for_change_note
        fields = [
         'rfc_note']


class request_for_change_readonly_form(ModelForm):
    __doc__ = '\n    The request for change text has been truncated to rfc_ as the field names were too long.\n    '
    rfc_summary = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_risk_and_impact_analysis = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_implementation_plan = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_backout_plan = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control'}),
      required=True)
    rfc_test_plan = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'class': 'form-control'}),
      required=True)

    class Meta:
        model = request_for_change
        fields = [
         'rfc_summary',
         'rfc_risk_and_impact_analysis',
         'rfc_implementation_plan',
         'rfc_backout_plan',
         'rfc_test_plan']


class requirement_information_form(ModelForm):
    requirement_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    requirement_type = forms.ModelChoiceField(queryset=(list_of_requirement_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement_status = forms.ModelChoiceField(queryset=(list_of_requirement_status.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement_scope = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))

    class Meta:
        model = requirement
        exclude = [
         'change_user',
         'is_deleted',
         'requirement_story_point_min',
         'requirement_story_point_max']


class requirement_item_form(forms.ModelForm):
    requirement_item_status_results = list_of_requirement_item_status.objects.filter(is_deleted='FALSE')
    requirement_item_title = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'Requirement Item Title', 
     'class':'form-control'}))
    requirement_item_scope = forms.CharField(widget=TinyMCE(mce_attrs={'width': '100%'},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))
    requirement_item_status = forms.ModelChoiceField(label='Quote Stage',
      widget=forms.Select(attrs={'class': 'form-control'}),
      queryset=requirement_item_status_results)
    requirement_item_type = forms.ModelChoiceField(queryset=(list_of_requirement_item_type.objects.all()),
      widget=forms.Select(attrs={'class': 'form-control'}))
    requirement_id = forms.IntegerField(required=False)
    change_user = forms.IntegerField(required=False)

    class Meta:
        model = requirement_item
        exclude = [
         'requirement_idchange_user',
         'is_deleted',
         'ri_story_point_min',
         'ri_story_point_max']


class requirement_readonly_form(ModelForm):
    requirement_scope = forms.CharField(widget=TinyMCE(mce_attrs={'width':'100%', 
     'toolbar':False, 
     'menubar':False},
      attrs={'placeholder': 'Requirement Scope'}))

    class Meta:
        model = requirement
        fields = [
         'requirement_scope']


class search_customer_form(forms.Form):
    search_customer = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Search Customers', 
     'class':'form-control w-75'}))


class search_kanban_form(forms.Form):
    search_kanban = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Search Kanban Boards', 
     'class':'form-control w-75'}))


class search_organisation_form(forms.Form):
    search_organisation = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Search Organisations', 
     'class':'form-control w-75'}))


class search_template_form(forms.Form):
    search_templates = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Search Templates', 
     'class':'form-control w-75'}))


class search_user_form(forms.Form):
    search_users = forms.CharField(max_length=255,
      required=False)
    include_deactivated = forms.MultipleChoiceField(widget=(forms.CheckboxSelectMultiple),
      choices=INCLUDE_DEACTIVATED)


class task_history_readonly_form(ModelForm):

    def __init__(self, *args, **kwargs):
        task_history_id = kwargs.pop('task_history_id', None)
        (super(task_history_readonly_form, self).__init__)(*args, **kwargs)
        self.fields['task_history'].widget = TinyMCE(mce_attrs={'width':'100%', 
         'toolbar':False, 
         'menubar':False, 
         'readonly':1},
          attrs={'placeholder':'Requirement Scope', 
         'id':'id_task_history_' + str(task_history_id)})

    task_history = forms.CharField()
    submit_history = forms.CharField(widget=TextInput(attrs={'readonly':True, 
     'class':'form-control'}))

    class Meta:
        model = task_history
        fields = {
         'task_history'}


class task_information_form(ModelForm):
    task_short_description = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'class': 'form-control'}))
    document = forms.FileField(required=False,
      widget=forms.FileInput(attrs={'onChange':'enable_submit()', 
     'class':'form-control'}))
    document_url_location = forms.URLField(required=False,
      widget=forms.TextInput(attrs={'placeholder':'https://example.com', 
     'onChange':'enable_submit()', 
     'class':'form-control'}))
    document_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'width':'100%', 
     'onkeyup':'enable_submit()', 
     'class':'form-control'}))
    folder_description = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'width':'100%', 
     'onkeyup':'enable_submit()', 
     'class':'form-control'}))
    task_start_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))
    task_end_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control'}))

    class Meta:
        model = task
        fields = {
         'task_short_description',
         'task_long_description'}


class task_readonly_form(ModelForm):
    task_long_description = forms.CharField(widget=TinyMCE(mce_attrs={'toolbar':False, 
     'menubar':False, 
     'readonly':1},
      attrs={'placeholder':'Requirement Scope', 
     'class':'form-control'}))

    class Meta:
        model = task
        fields = {
         'task_long_description'}


class timeline_form(forms.Form):
    start_date = forms.DateField(widget=forms.DateInput(attrs={'onchange':'render_gantt_chart()', 
     'class':'form-control'}))
    end_date = forms.DateField(widget=forms.DateInput(attrs={'onchange':'render_gantt_chart()', 
     'class':'form-control'}))
    object_type = forms.ChoiceField(choices=OBJECT_CHOICES,
      widget=forms.Select(attrs={'onchange':'render_gantt_chart()', 
     'class':'form-control'}))


class to_do_form(ModelForm):
    to_do = forms.CharField(max_length=255,
      widget=forms.TextInput(attrs={'placeholder':'To do next?', 
     'class':'form-control'}))

    class Meta:
        model = to_do
        fields = {
         'to_do'}


class user_information_form(ModelForm):
    password1 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'type':'password', 
     'placeholder':'Password', 
     'onkeyup':'enable_submit()', 
     'autocomplete':'off', 
     'class':'form-control'}))
    password2 = forms.CharField(max_length=255,
      required=False,
      widget=forms.TextInput(attrs={'type':'password', 
     'placeholder':'Repeate Password', 
     'onkeyup':'enable_submit()', 
     'autocomplete':'off', 
     'class':'form-control'}))
    username = forms.CharField(max_length=50,
      widget=forms.TextInput(attrs={'placeholder':'Username', 
     'class':'form-control'}))
    first_name = forms.CharField(max_length=100,
      widget=forms.TextInput(attrs={'placeholder':'First Name', 
     'class':'form-control'}))
    last_name = forms.CharField(max_length=100,
      widget=forms.TextInput(attrs={'placeholder':'Last Name', 
     'class':'form-control'}))
    email = forms.EmailField(max_length=100,
      required=False,
      widget=forms.TextInput(attrs={'placeholder':'Email Address', 
     'class':'form-control'}))

    class Meta:
        model = User
        fields = {
         'username',
         'first_name',
         'last_name',
         'is_active',
         'is_superuser',
         'email'}


class user_want_form(ModelForm):
    want_choice_text = forms.CharField(max_length=50,
      required=True,
      widget=forms.TextInput(attrs={'placeholder':'Please input a want or do not want', 
     'class':'form-control'}))
    want_choice = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
      choices=WANT_CHOICE)
    want_skill = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
      choices=SKILL_CHOICE)

    class Meta:
        model = user_want
        fields = {
         'want_choice',
         'want_choice_text',
         'want_skill'}


class user_weblink_form(ModelForm):
    user_weblink_url = forms.URLField(widget=forms.URLInput(attrs={'placeholder':'https://nearbeach.org', 
     'class':'form-control'}))
    user_weblink_source = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}),
      choices=WEBSITE_SOURCE)

    class Meta:
        model = user_weblink
        fields = {
         'user_weblink_url',
         'user_weblink_source'}