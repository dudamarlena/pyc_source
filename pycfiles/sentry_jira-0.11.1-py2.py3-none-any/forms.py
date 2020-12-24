# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/getsentry/sentry-jira/sentry_jira/forms.py
# Compiled at: 2016-06-02 14:44:05
from __future__ import absolute_import
import logging
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms
from .jira import JIRAClient, JIRAError
log = logging.getLogger(__name__)

class JIRAFormUtils(object):

    @staticmethod
    def make_choices(x):
        if x:
            return [ (y['id'], y['name'] if 'name' in y else y['value']) for y in x ]
        return []


class JIRAOptionsForm(forms.Form):
    instance_url = forms.CharField(label=_('JIRA Instance URL'), widget=forms.TextInput(attrs={'class': 'span6', 'placeholder': 'e.g. "https://jira.atlassian.com"'}), help_text=_('It must be visible to the Sentry server'), required=True)
    username = forms.CharField(label=_('Username'), widget=forms.TextInput(attrs={'class': 'span6'}), help_text=_('Ensure the JIRA user has admin perm. on the project'), required=True)
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput(attrs={'class': 'span6'}), required=False)
    default_project = forms.ChoiceField(label=_('Linked Project'))
    ignored_fields = forms.CharField(label=_('Ignored Fields'), widget=forms.Textarea(attrs={'class': 'span11', 'placeholder': 'e.g. "components, security, customfield_10006"'}), help_text=_("Comma-separated list of properties that you don't want to show in the form"), required=False)
    default_priority = forms.ChoiceField(label=_('Default Priority'), required=False)
    default_issue_type = forms.ChoiceField(label=_('Default Issue Type'), required=False)
    auto_create = forms.BooleanField(label=_('Auto create JIRA tickets'), help_text=_('Automatically create a JIRA ticket for EVERY new issue'), required=False)

    def __init__(self, data=None, *args, **kwargs):
        super(JIRAOptionsForm, self).__init__(data=data, *args, **kwargs)
        initial = kwargs.get('initial') or {}
        for key, value in self.data.items():
            initial[key.lstrip(self.prefix or '')] = value

        has_credentials = all(initial.get(k) for k in ('instance_url', 'username',
                                                       'password'))
        project_safe = False
        can_auto_create = False
        has_auto_create = 'auto_create' in initial
        if has_credentials:
            jira = JIRAClient(initial['instance_url'], initial['username'], initial['password'])
            try:
                projects_response = jira.get_projects_list()
            except JIRAError as e:
                if e.status_code == 401:
                    has_credentials = False
            else:
                projects = projects_response.json
                if projects:
                    project_choices = [ (p.get('key'), '%s (%s)' % (p.get('name'), p.get('key'))) for p in projects ]
                    project_safe = True
                    can_auto_create = True
                    self.fields['default_project'].choices = project_choices
        if project_safe and has_auto_create:
            try:
                priorities_response = jira.get_priorities()
            except JIRAError as e:
                if e.status_code == 401:
                    has_credentials = False

            priorities = priorities_response.json
            if priorities:
                priority_choices = [ (p.get('id'), '%s' % p.get('name')) for p in priorities ]
                self.fields['default_priority'].choices = priority_choices
            default_project = initial.get('default_project')
            if default_project:
                try:
                    meta = jira.get_create_meta_for_project(default_project)
                except JIRAError as e:
                    if e.status_code == 401:
                        has_credentials = False
                    can_auto_create = False
                else:
                    if meta:
                        self.fields['default_issue_type'].choices = JIRAFormUtils.make_choices(meta['issuetypes'])
                    else:
                        can_auto_create = False
        if not has_credentials:
            self.fields['password'].required = True
        else:
            self.fields['password'].help_text = _('Only enter a new password if you wish to update the stored value')
        if not project_safe:
            del self.fields['default_project']
            del self.fields['default_issue_type']
            del self.fields['default_priority']
            del self.fields['ignored_fields']
        if not can_auto_create:
            del self.fields['auto_create']

    def clean_password(self):
        """
        Don't complain if the field is empty and a password is already stored,
        no one wants to type a pw in each time they want to change it.
        """
        pw = self.cleaned_data.get('password')
        if pw:
            return pw
        else:
            old_pw = self.initial.get('password')
            if not old_pw:
                raise ValidationError('A Password is Required')
            return old_pw

    def clean_instance_url(self):
        """
        Strip forward slashes off any url passed through the form.
        """
        url = self.cleaned_data.get('instance_url')
        if url and url[-1:] == '/':
            return url[:-1]
        else:
            return url

    def clean_auto_create(self):
        cd = self.cleaned_data
        if not cd.get('auto_create'):
            return False
        if not (cd.get('default_priority') and cd.get('default_issue_type')):
            raise ValidationError('Default priority and issue type must be configured.')
        return cd['auto_create']

    def clean(self):
        """
        try and build a JIRAClient and make a random call to make sure the
        configuration is right.
        """
        cd = self.cleaned_data
        missing_fields = False
        if not cd.get('instance_url'):
            self.errors['instance_url'] = [
             'Instance URL is required']
            missing_fields = True
        if not cd.get('username'):
            self.errors['username'] = [
             'Username is required']
            missing_fields = True
        if missing_fields:
            raise ValidationError('Missing Fields')
        if cd.get('password'):
            jira = JIRAClient(cd['instance_url'], cd['username'], cd['password'])
            try:
                sut_response = jira.get_priorities()
            except JIRAError as e:
                if e.status_code == 403 or e.status_code == 401:
                    self.errors['username'] = [
                     'Username might be incorrect']
                    self.errors['password'] = ['Password might be incorrect']
                    raise ValidationError('Unable to connect to JIRA: %s, if you have tried and failed multiple times you may have to enter a CAPTCHA in JIRA to re-enable API logins.' % e.status_code)
                else:
                    logging.exception(e)
                    raise ValidationError('Unable to connect to JIRA: the remote server returned an unhandled %s status  code' % e.status_code)

            if not sut_response.json:
                raise ValidationError('Unable to connect to JIRA: the response did not contain valid JSON, did you enter the correct instance URL?')
        return cd


CUSTOM_FIELD_TYPES = {'select': 'com.atlassian.jira.plugin.system.customfieldtypes:select', 
   'textarea': 'com.atlassian.jira.plugin.system.customfieldtypes:textarea', 
   'multiuserpicker': 'com.atlassian.jira.plugin.system.customfieldtypes:multiuserpicker'}

class JIRAIssueForm(forms.Form):
    project = forms.CharField(widget=forms.HiddenInput())
    issuetype = forms.ChoiceField(label='Issue Type', help_text='Changing the issue type will refresh the page with the required form fields.', required=True)
    summary = forms.CharField(label=_('Issue Summary'), widget=forms.TextInput(attrs={'class': 'span6'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'span6'}))

    def __init__(self, *args, **kwargs):
        self.ignored_fields = set((kwargs.pop('ignored_fields') or '').split(','))
        initial = kwargs.get('initial')
        jira_client = kwargs.pop('jira_client')
        project_key = kwargs.pop('project_key')
        priorities = jira_client.get_priorities().json
        versions = jira_client.get_versions(project_key).json
        meta = jira_client.get_create_meta(project_key).json
        if not meta or not priorities:
            super(JIRAIssueForm, self).__init__(*args, **kwargs)
            self.errors['__all__'] = [
             'Error communicating with JIRA, Please check your configuration.']
            return
        else:
            if len(meta['projects']) == 0:
                super(JIRAIssueForm, self).__init__(*args, **kwargs)
                self.errors['__all__'] = [
                 ('Error in JIRA configuration, no projects found for user %s.').format(jira_client.username)]
                return
            project = meta['projects'][0]
            issue_types = project['issuetypes']
            self.issue_type = initial.get('issuetype')
            if self.issue_type:
                matching_type = [ t for t in issue_types if t['id'] == self.issue_type ]
                self.issue_type = matching_type[0] if len(matching_type) > 0 else None
            if not self.issue_type:
                self.issue_type = issue_types[0]
            kwargs['initial'] = initial
            super(JIRAIssueForm, self).__init__(*args, **kwargs)
            self.fields['project'].initial = project['id']
            self.fields['issuetype'].choices = JIRAFormUtils.make_choices(issue_types)
            anti_gravity = {'priority': -150, 'fixVersions': -125, 
               'components': -100, 
               'security': -50}
            dynamic_fields = self.issue_type.get('fields').keys()
            dynamic_fields.sort(key=lambda f: anti_gravity.get(f) or 0)
            for field in dynamic_fields:
                if field in self.fields.keys() or field in [ x.strip() for x in self.ignored_fields ]:
                    continue
                mb_field = self.build_dynamic_field(self.issue_type['fields'][field])
                if mb_field:
                    self.fields[field] = mb_field

            if 'priority' in self.fields.keys():
                self.fields['priority'].choices = JIRAFormUtils.make_choices(priorities)
            if 'fixVersions' in self.fields.keys():
                self.fields['fixVersions'].choices = JIRAFormUtils.make_choices(versions)
            return

    def clean_description(self):
        """
        Turn code blocks that are in the stack trace into JIRA code blocks.
        """
        desc = self.cleaned_data['description']
        return desc.replace('```', '{code}')

    def clean(self):
        """
        The form clean method needs to take advantage of the loaded issue type
        fields and meta info so it can determine the format that the datatypes
        should render as.
        """
        very_clean = self.cleaned_data
        if not very_clean.get('issuetype'):
            raise ValidationError('Issue Type is required. Check your plugin configuration.')
        fs = self.issue_type['fields']
        for field in fs.keys():
            f = fs[field]
            if field in ('description', 'summary'):
                continue
            if field in very_clean.keys():
                v = very_clean.get(field)
                if v:
                    schema = f['schema']
                    if schema.get('type') == 'string' and not schema.get('custom') == CUSTOM_FIELD_TYPES['select']:
                        continue
                    if schema['type'] == 'user' or schema.get('item') == 'user':
                        v = {'name': v}
                    elif schema.get('custom') == CUSTOM_FIELD_TYPES.get('multiuserpicker'):
                        v = [{'name': v}]
                    elif schema['type'] == 'array' and schema.get('item') != 'string':
                        v = [ {'id': vx} for vx in v ]
                    elif schema.get('custom') == CUSTOM_FIELD_TYPES.get('textarea'):
                        v = v
                    elif schema.get('type') != 'string' or schema.get('item') != 'string' or schema.get('custom') == CUSTOM_FIELD_TYPES.get('select'):
                        v = {'id': v}
                    very_clean[field] = v
                else:
                    very_clean.pop(field, None)

        if not (isinstance(very_clean['issuetype'], dict) and 'id' in very_clean['issuetype']):
            very_clean['issuetype'] = {'id': very_clean['issuetype']}
        return very_clean

    def build_dynamic_field(self, field_meta):
        """
        Builds a field based on JIRA's meta field information
        """
        schema = field_meta['schema']
        fieldtype = forms.CharField
        fkwargs = {'label': field_meta['name'], 
           'required': field_meta['required'], 
           'widget': forms.TextInput(attrs={'class': 'span6'})}
        if schema['type'] in ('securitylevel', 'priority') or schema.get('custom') == CUSTOM_FIELD_TYPES.get('select'):
            fieldtype = forms.ChoiceField
            fkwargs['choices'] = JIRAFormUtils.make_choices(field_meta.get('allowedValues'))
            fkwargs['widget'] = forms.Select()
        else:
            if schema.get('items') == 'user' or schema['type'] == 'user':
                fkwargs['widget'] = forms.TextInput(attrs={'class': 'user-selector', 
                   'data-autocomplete': field_meta.get('autoCompleteUrl')})
            elif schema['type'] in ('timetracking', ):
                return None
            if schema.get('items') in ('worklog', 'attachment'):
                return None
        if schema['type'] == 'array' and schema['items'] != 'string':
            fieldtype = forms.MultipleChoiceField
            fkwargs['choices'] = JIRAFormUtils.make_choices(field_meta.get('allowedValues'))
            fkwargs['widget'] = forms.SelectMultiple()
        if schema.get('custom'):
            if schema['custom'] == CUSTOM_FIELD_TYPES.get('textarea'):
                fkwargs['widget'] = forms.Textarea(attrs={'class': 'span6'})
        return fieldtype(**fkwargs)