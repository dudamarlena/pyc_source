# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/django-danceschool/currentmaster/django-danceschool/danceschool/core/mixins.py
# Compiled at: 2018-03-26 19:55:27
# Size of source mod 2**32: 13126 bytes
from django.contrib.auth.views import redirect_to_login
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ChoiceField, Media
from django.utils.translation import ugettext_lazy as _
from django.template.loader import get_template, render_to_string
from django.template import Template, Context
from django.template.exceptions import TemplateDoesNotExist
from braces.views import GroupRequiredMixin
from urllib.parse import quote
from six import string_types
import re
from .constants import getConstant
from .tasks import sendEmail
from .registries import plugin_templates_registry

class EmailRecipientMixin(object):

    def email_recipient(self, subject, content, **kwargs):
        """
        This method allows for direct emailing of an object's recipient(s)
        (default or manually specified), with both object-specific context
        provided using the get_email_context() method.  This is used, for example,
        to email an individual registrant or the recipient of an individual invoice.
        """
        email_kwargs = {}
        for list_arg in [
         'to', 'cc', 'bcc']:
            email_kwargs[list_arg] = kwargs.pop(list_arg, []) or []
            if isinstance(email_kwargs[list_arg], string_types):
                email_kwargs[list_arg] = [
                 email_kwargs[list_arg]]

        for none_arg in ['attachment_name', 'attachment']:
            email_kwargs[none_arg] = kwargs.pop(none_arg, None) or None

        if kwargs.pop('send_html', False) and kwargs.get('html_message'):
            email_kwargs['html_content'] = render_to_string('email/html_email_base.html', context={'html_content': kwargs.get('html_message'), 'subject': subject})
        email_kwargs['from_name'] = kwargs.pop('from_name', getConstant('email__defaultEmailName')) or getConstant('email__defaultEmailName')
        email_kwargs['from_address'] = kwargs.pop('from_name', getConstant('email__defaultEmailFrom')) or getConstant('email__defaultEmailFrom')
        default_recipients = self.get_default_recipients() or []
        if isinstance(default_recipients, string_types):
            default_recipients = [
             default_recipients]
        email_kwargs['bcc'] += default_recipients
        if not (email_kwargs['bcc'] or email_kwargs['cc'] or email_kwargs['to']):
            raise ValueError(_('Email must have a recipient.'))
        has_tags = re.search('\\{\\{.+\\}\\}', content)
        if not has_tags:
            t = Template(content)
            rendered_content = t.render(Context(kwargs))
            sendEmail(subject, rendered_content, **email_kwargs)
            return
        template_context = self.get_email_context() or {}
        template_context.update(kwargs)
        content = re.sub('\\{%\\s*((extends)|(load)|(debug)|(include)|(ssi))\\s+.*?\\s*%\\}', '', content)
        t = Template(content)
        rendered_content = t.render(Context(template_context))
        if email_kwargs.get('html_content'):
            html_content = re.sub('\\{%\\s*((extends)|(load)|(debug)|(include)|(ssi))\\s+.*?\\s*%\\}', '', email_kwargs.get('html_content'))
            t = Template(html_content)
            email_kwargs['html_content'] = t.render(Context(template_context))
        sendEmail(subject, rendered_content, **email_kwargs)

    def get_email_context(self, **kwargs):
        """
        This method can be overridden in classes that inherit from this mixin
        so that additional object-specific context is provided to the email
        template.  This should return a dictionary.  By default, only general
        financial context variables are added to the dictionary, and kwargs are
        just passed directly.

        Note also that it is in general not a good idea for security reasons
        to pass model instances in the context here, since these methods can be
        accessed by logged in users who use the SendEmailView.  So, In the default
        models of this app, the values of fields and properties are passed
        directly instead.
        """
        context = kwargs
        context.update({'currencyCode': getConstant('general__currencyCode'), 
         'currencySymbol': getConstant('general__currencySymbol'), 
         'businessName': getConstant('contact__businessName'), 
         'site_url': getConstant('email__linkProtocol') + '://' + Site.objects.get_current().domain})
        return context

    def get_default_recipients(self):
        """
        This method should be overridden in each class that inherits from this
        mixin, so that the email addresses to whom the email should be sent are
        included on the BCC line.  This should return a list.
        """
        return []


class FinancialContextMixin(object):
    __doc__ = '\n    This mixin just adds the currency code and symbol to the context\n    '

    def get_context_data(self, **kwargs):
        context = {'currencyCode': getConstant('general__currencyCode'), 
         'currencySymbol': getConstant('general__currencySymbol'), 
         'businessName': getConstant('contact__businessName')}
        context.update(kwargs)
        return super(FinancialContextMixin, self).get_context_data(**context)


class StaffMemberObjectMixin(object):
    __doc__ = "\n    For class-based views involving instructor info, this ensures that\n    the object being edited is always for the instructor's own information.\n    "

    def get_object(self, queryset=None):
        if hasattr(self.request.user, 'staffmember'):
            return self.request.user.staffmember
        else:
            return


class GroupRequiredByFieldMixin(GroupRequiredMixin):
    __doc__ = '\n    This subclass of the GroupRequiredMixin checks if a specified model field\n    identifies a group that is required.  If so, then require this group.  If\n    not, then no permissions are required.  This can be used for thing like survey\n    responses that are optionally restricted.\n    '
    group_required_field = ''

    def get_group_required(self):
        """ Get the group_required value from the object """
        this_object = self.model_object
        if hasattr(this_object, self.group_required_field) and hasattr(getattr(this_object, self.group_required_field), 'name'):
            return [getattr(this_object, self.group_required_field).name]
        return [
         '']

    def check_membership(self, groups):
        """ Allows for objects with no required groups """
        if not groups or groups == ['']:
            return True
        if self.request.user.is_superuser:
            return True
        user_groups = self.request.user.groups.values_list('name', flat=True)
        return set(groups).intersection(set(user_groups))

    def dispatch(self, request, *args, **kwargs):
        """
        This override of dispatch ensures that if no group is required, then
        the request still goes through without being logged in.
        """
        self.request = request
        in_group = False
        required_group = self.get_group_required()
        if not required_group or required_group == ['']:
            in_group = True
        else:
            if self.request.user.is_authenticated():
                in_group = self.check_membership(required_group)
            if not in_group:
                if self.raise_exception:
                    raise PermissionDenied
            else:
                return redirect_to_login(request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)


class AdminSuccessURLMixin(object):
    __doc__ = '\n    Many admin forms should redirect to return to the Page specified in the global settings.\n    This mixin is similar to the SuccessURLRedirectListMixin in django-braces.  If a\n    success_list_url is specified, it reverses that URL and returns the result.  But,\n    if a success_list_url is not specified, then it returns the default admin success form\n    Page as specified in settings.\n    '
    success_list_url = None

    def get_success_url(self):
        if self.success_list_url:
            return '%s?redirect_url=%s' % (reverse('submissionRedirect'), quote(self.success_list_url))
        else:
            return reverse('submissionRedirect')


class TemplateChoiceField(ChoiceField):

    def validate(self, value):
        """
        Check for empty values, and for an existing template, but do not check if
        this is one of the initial choices provided.
        """
        super(ChoiceField, self).validate(value)
        try:
            get_template(value)
        except TemplateDoesNotExist:
            raise ValidationError(_('%s is not a valid template.' % value))


class PluginTemplateMixin(object):
    __doc__ = '\n    This mixin is for plugin classes, to override the render_template with the one provided in the template field,\n    and to allow for selectable choices with the option to add a new (validated) choice.\n    '

    def render(self, context, instance, placeholder):
        """ Permits setting of the template in the plugin instance configuration """
        if instance and instance.template:
            self.render_template = instance.template
        return super(PluginTemplateMixin, self).render(context, instance, placeholder)

    def templateChoiceFormFactory(self, request, choices):

        class PluginTemplateChoiceForm(ModelForm):

            def __init__(self, *args, **kwargs):
                super(PluginTemplateChoiceForm, self).__init__(*args, **kwargs)
                self.request = request
                all_choices = choices
                if self.instance and self.instance.template not in [x[0] for x in choices]:
                    all_choices = [
                     (
                      self.instance.template, self.instance.template)] + all_choices
                if self.request and self.request.user.has_perm('core.choose_custom_plugin_template'):
                    self.fields['template'] = TemplateChoiceField(choices=all_choices)
                else:
                    self.fields['template'] = ChoiceField(choices=all_choices)

            def _media(self):
                """ Add Select2 custom behavior only if user has permissions to need it. """
                if self.request and self.request.user.has_perm('core.choose_custom_plugin_template'):
                    return Media(css={'all': ('select2/select2.min.css', )}, js=('select2/select2.min.js',
                                                                                 'js/select2_newtemplate.js'))
                return Media()

            media = property(_media)

        return PluginTemplateChoiceForm

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = self.templateChoiceFormFactory(request, self.get_template_choices())
        return super(PluginTemplateMixin, self).get_form(request, obj, **kwargs)

    def get_template_choices(self):
        if hasattr(self, 'template_choices') and self.template_choices:
            return self.template_choices
        registered = [x for x in plugin_templates_registry.values() if getattr(x, 'plugin', None) in [z.__name__ for z in self.__class__.__mro__]]
        if registered:
            return [(x.template_name, getattr(x, 'description', None) or x.template_name) for x in registered]
        if self.render_template:
            return [(self.render_template, self.render_template)]
        return []