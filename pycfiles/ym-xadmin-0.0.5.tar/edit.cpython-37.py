# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\python\hhwork\extra_apps\xadmin\views\edit.py
# Compiled at: 2019-04-17 23:57:58
# Size of source mod 2**32: 21021 bytes
from __future__ import absolute_import
import copy
from crispy_forms.utils import TEMPLATE_PACK
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied, FieldError
from django.db import models, transaction
from django.forms.models import modelform_factory, modelform_defines_fields
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.text import capfirst, get_text_list
from django.template import loader
import django.utils.translation as _
from xadmin import widgets
from xadmin.layout import FormHelper, Layout, Fieldset, TabHolder, Container, Column, Col, Field
from xadmin.util import unquote
from xadmin.views.detail import DetailAdminUtil
from .base import ModelAdminView, filter_hook, csrf_protect_m
FORMFIELD_FOR_DBFIELD_DEFAULTS = {models.DateTimeField: {'form_class':forms.SplitDateTimeField, 
                        'widget':widgets.AdminSplitDateTime}, 
 
 models.DateField: {'widget': widgets.AdminDateWidget}, 
 models.TimeField: {'widget': widgets.AdminTimeWidget}, 
 models.TextField: {'widget': widgets.AdminTextareaWidget}, 
 models.URLField: {'widget': widgets.AdminURLFieldWidget}, 
 models.IntegerField: {'widget': widgets.AdminIntegerFieldWidget}, 
 models.BigIntegerField: {'widget': widgets.AdminIntegerFieldWidget}, 
 models.CharField: {'widget': widgets.AdminTextInputWidget}, 
 models.IPAddressField: {'widget': widgets.AdminTextInputWidget}, 
 models.ImageField: {'widget': widgets.AdminFileWidget}, 
 models.FileField: {'widget': widgets.AdminFileWidget}, 
 models.ForeignKey: {'widget': widgets.AdminSelectWidget}, 
 models.OneToOneField: {'widget': widgets.AdminSelectWidget}, 
 models.ManyToManyField: {'widget': widgets.AdminSelectMultiple}}

class ReadOnlyField(Field):
    template = 'xadmin/layout/field_value.html'

    def __init__(self, *args, **kwargs):
        self.detail = kwargs.pop('detail')
        (super(ReadOnlyField, self).__init__)(*args, **kwargs)

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        html = ''
        for field in self.fields:
            result = self.detail.get_field_result(field)
            field = {'auto_id': field}
            html += loader.render_to_string(self.template, {'field':field,  'result':result})

        return html


class ModelFormAdminView(ModelAdminView):
    form = forms.ModelForm
    formfield_overrides = {}
    readonly_fields = ()
    style_fields = {}
    exclude = None
    relfield_style = None
    save_as = False
    save_on_top = False
    add_form_template = None
    change_form_template = None
    form_layout = None

    def __init__(self, request, *args, **kwargs):
        overrides = FORMFIELD_FOR_DBFIELD_DEFAULTS.copy()
        overrides.update(self.formfield_overrides)
        self.formfield_overrides = overrides
        (super(ModelFormAdminView, self).__init__)(request, *args, **kwargs)

    @filter_hook
    def formfield_for_dbfield(self, db_field, **kwargs):
        if isinstance(db_field, models.ManyToManyField):
            if not db_field.rel.through._meta.auto_created:
                return
        attrs = (self.get_field_attrs)(db_field, **kwargs)
        return (db_field.formfield)(**)

    @filter_hook
    def get_field_style(self, db_field, style, **kwargs):
        if style in ('radio', 'radio-inline'):
            if db_field.choices or isinstance(db_field, models.ForeignKey):
                attrs = {'widget': widgets.AdminRadioSelect(attrs={'inline': 'inline' if style == 'radio-inline' else ''})}
                if db_field.choices:
                    attrs['choices'] = db_field.get_choices(include_blank=(db_field.blank),
                      blank_choice=[
                     (
                      '', _('Null'))])
                return attrs
        if style in ('checkbox', 'checkbox-inline'):
            if isinstance(db_field, models.ManyToManyField):
                return {'widget':widgets.AdminCheckboxSelect(attrs={'inline': style == 'checkbox-inline'}), 
                 'help_text':None}

    @filter_hook
    def get_field_attrs(self, db_field, **kwargs):
        if db_field.name in self.style_fields:
            attrs = (self.get_field_style)(
             db_field, (self.style_fields[db_field.name]), **kwargs)
            if attrs:
                return attrs
        if hasattr(db_field, 'rel'):
            if db_field.rel:
                related_modeladmin = self.admin_site._registry.get(db_field.rel.to)
                if related_modeladmin:
                    if hasattr(related_modeladmin, 'relfield_style'):
                        attrs = (self.get_field_style)(
                         db_field, (related_modeladmin.relfield_style), **kwargs)
                        if attrs:
                            return attrs
        if db_field.choices:
            return {'widget': widgets.AdminSelectWidget}
        for klass in db_field.__class__.mro():
            if klass in self.formfield_overrides:
                return self.formfield_overrides[klass].copy()

        return {}

    @filter_hook
    def prepare_form(self):
        self.model_form = self.get_model_form()

    @filter_hook
    def instance_forms(self):
        self.form_obj = (self.model_form)(**self.get_form_datas())

    def setup_forms(self):
        helper = self.get_form_helper()
        if helper:
            self.form_obj.helper = helper

    @filter_hook
    def valid_forms(self):
        return self.form_obj.is_valid()

    @filter_hook
    def get_model_form--- This code section failed: ---

 L. 161         0  LOAD_FAST                'self'
                2  LOAD_ATTR                exclude
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_FALSE    16  'to 16'

 L. 162        10  BUILD_LIST_0          0 
               12  STORE_FAST               'exclude'
               14  JUMP_FORWARD         26  'to 26'
             16_0  COME_FROM             8  '8'

 L. 164        16  LOAD_GLOBAL              list
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                exclude
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  STORE_FAST               'exclude'
             26_0  COME_FROM            14  '14'

 L. 165        26  LOAD_FAST                'exclude'
               28  LOAD_METHOD              extend
               30  LOAD_FAST                'self'
               32  LOAD_METHOD              get_readonly_fields
               34  CALL_METHOD_0         0  '0 positional arguments'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_TOP          

 L. 166        40  LOAD_FAST                'self'
               42  LOAD_ATTR                exclude
               44  LOAD_CONST               None
               46  COMPARE_OP               is
               48  POP_JUMP_IF_FALSE    88  'to 88'
               50  LOAD_GLOBAL              hasattr
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                form
               56  LOAD_STR                 '_meta'
               58  CALL_FUNCTION_2       2  '2 positional arguments'
               60  POP_JUMP_IF_FALSE    88  'to 88'
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                form
               66  LOAD_ATTR                _meta
               68  LOAD_ATTR                exclude
               70  POP_JUMP_IF_FALSE    88  'to 88'

 L. 169        72  LOAD_FAST                'exclude'
               74  LOAD_METHOD              extend
               76  LOAD_FAST                'self'
               78  LOAD_ATTR                form
               80  LOAD_ATTR                _meta
               82  LOAD_ATTR                exclude
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_TOP          
             88_0  COME_FROM            70  '70'
             88_1  COME_FROM            60  '60'
             88_2  COME_FROM            48  '48'

 L. 172        88  LOAD_FAST                'exclude'
               90  JUMP_IF_TRUE_OR_POP    94  'to 94'
               92  LOAD_CONST               None
             94_0  COME_FROM            90  '90'
               94  STORE_FAST               'exclude'

 L. 174        96  LOAD_FAST                'self'
               98  LOAD_ATTR                form

 L. 175       100  LOAD_FAST                'self'
              102  LOAD_ATTR                fields
              104  POP_JUMP_IF_FALSE   116  'to 116'
              106  LOAD_GLOBAL              list
              108  LOAD_FAST                'self'
              110  LOAD_ATTR                fields
              112  CALL_FUNCTION_1       1  '1 positional argument'
              114  JUMP_IF_TRUE_OR_POP   118  'to 118'
            116_0  COME_FROM           104  '104'
              116  LOAD_CONST               None
            118_0  COME_FROM           114  '114'

 L. 176       118  LOAD_FAST                'exclude'

 L. 177       120  LOAD_FAST                'self'
              122  LOAD_ATTR                formfield_for_dbfield
              124  LOAD_CONST               ('form', 'fields', 'exclude', 'formfield_callback')
              126  BUILD_CONST_KEY_MAP_4     4 
              128  STORE_FAST               'defaults'

 L. 179       130  LOAD_FAST                'defaults'
              132  LOAD_METHOD              update
              134  LOAD_FAST                'kwargs'
              136  CALL_METHOD_1         1  '1 positional argument'
              138  POP_TOP          

 L. 181       140  LOAD_FAST                'defaults'
              142  LOAD_STR                 'fields'
              144  BINARY_SUBSCR    
              146  LOAD_CONST               None
              148  COMPARE_OP               is
              150  POP_JUMP_IF_FALSE   174  'to 174'
              152  LOAD_GLOBAL              modelform_defines_fields
              154  LOAD_FAST                'defaults'
              156  LOAD_STR                 'form'
              158  BINARY_SUBSCR    
              160  CALL_FUNCTION_1       1  '1 positional argument'
              162  POP_JUMP_IF_TRUE    174  'to 174'

 L. 182       164  LOAD_GLOBAL              forms
              166  LOAD_ATTR                ALL_FIELDS
              168  LOAD_FAST                'defaults'
              170  LOAD_STR                 'fields'
              172  STORE_SUBSCR     
            174_0  COME_FROM           162  '162'
            174_1  COME_FROM           150  '150'

 L. 184       174  LOAD_GLOBAL              modelform_factory
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                model
              180  BUILD_TUPLE_1         1 
              182  LOAD_FAST                'defaults'
              184  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              186  RETURN_VALUE     

 L. 188       188  DUP_TOP          
              190  LOAD_GLOBAL              FieldError
              192  COMPARE_OP               exception-match
          194_196  POP_JUMP_IF_FALSE   242  'to 242'
              198  POP_TOP          
              200  STORE_FAST               'e'
              202  POP_TOP          
              204  SETUP_FINALLY       230  'to 230'

 L. 189       206  LOAD_GLOBAL              FieldError
              208  LOAD_STR                 '%s. Check fields/fieldsets/exclude attributes of class %s.'

 L. 190       210  LOAD_FAST                'e'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                __class__
              216  LOAD_ATTR                __name__
              218  BUILD_TUPLE_2         2 
              220  BINARY_MODULO    
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  RAISE_VARARGS_1       1  'exception instance'
              226  POP_BLOCK        
              228  LOAD_CONST               None
            230_0  COME_FROM_FINALLY   204  '204'
              230  LOAD_CONST               None
              232  STORE_FAST               'e'
              234  DELETE_FAST              'e'
              236  END_FINALLY      
              238  POP_EXCEPT       
              240  JUMP_FORWARD        244  'to 244'
            242_0  COME_FROM           194  '194'
              242  END_FINALLY      
            244_0  COME_FROM           240  '240'

Parse error at or near `DUP_TOP' instruction at offset 188

    @filter_hook
    def get_form_layout(self):
        layout = copy.deepcopy(self.form_layout)
        arr = self.form_obj.fields.keys()
        if six.PY3:
            arr = [k for k in arr]
        fields = arr + list(self.get_readonly_fields())
        if layout is None:
            layout = Layout(Container(Col('full', Fieldset('', *fields, **{'css_class': 'unsort no_title'}),
              horizontal=True, span=12)))
        else:
            if type(layout) in (list, tuple):
                if len(layout) > 0:
                    if isinstance(layout[0], Column):
                        fs = layout
                    else:
                        if isinstance(layout[0], (Fieldset, TabHolder)):
                            fs = (
                             Col('full', *layout, **{'horizontal':True,  'span':12}),)
                        else:
                            fs = (
                             Col('full', Fieldset('', *layout, **{'css_class': 'unsort no_title'}), horizontal=True, span=12),)
                    layout = Layout(Container(*fs))
                    rendered_fields = [i[1] for i in layout.get_field_names()]
                    container = layout[0].fields
                    other_fieldset = Fieldset(_('Other Fields'), *[f for f in fields if f not in rendered_fields])
                    if len(other_fieldset.fields):
                        if len(container) and isinstance(container[0], Column):
                            container[0].fields.append(other_fieldset)
                        else:
                            container.append(other_fieldset)
            return layout

    @filter_hook
    def get_form_helper(self):
        helper = FormHelper()
        helper.form_tag = False
        helper.include_media = False
        helper.add_layout(self.get_form_layout())
        readonly_fields = self.get_readonly_fields()
        if readonly_fields:
            detail = self.get_model_view(DetailAdminUtil, self.model, self.form_obj.instance)
            for field in readonly_fields:
                helper[field].wrap(ReadOnlyField, detail=detail)

        return helper

    @filter_hook
    def get_readonly_fields(self):
        """
        Hook for specifying custom readonly fields.
        """
        return self.readonly_fields

    @filter_hook
    def save_forms(self):
        self.new_obj = self.form_obj.save(commit=False)

    @filter_hook
    def change_message(self):
        change_message = []
        if self.org_obj is None:
            change_message.append(_('Added.'))
        else:
            if self.form_obj.changed_data:
                change_message.append(_('Changed %s.') % get_text_list(self.form_obj.changed_data, _('and')))
        change_message = ' '.join(change_message)
        return change_message or _('No fields changed.')

    @filter_hook
    def save_models(self):
        self.new_obj.save()
        flag = self.org_obj is None and 'create' or 'change'
        self.log(flag, self.change_message(), self.new_obj)

    @filter_hook
    def save_related(self):
        self.form_obj.save_m2m()

    @csrf_protect_m
    @filter_hook
    def get(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()
        return self.get_response()

    @csrf_protect_m
    @transaction.atomic
    @filter_hook
    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()
        if self.valid_forms():
            self.save_forms()
            self.save_models()
            self.save_related()
            response = self.post_response()
            cls_str = str if six.PY3 else basestring
            if isinstance(response, cls_str):
                return HttpResponseRedirect(response)
            return response
        return self.get_response()

    @filter_hook
    def get_context(self):
        add = self.org_obj is None
        change = self.org_obj is not None
        new_context = {'form':self.form_obj, 
         'original':self.org_obj, 
         'show_delete':self.org_obj is not None, 
         'add':add, 
         'change':change, 
         'errors':self.get_error_list(), 
         'has_add_permission':self.has_add_permission(), 
         'has_view_permission':self.has_view_permission(), 
         'has_change_permission':self.has_change_permission(self.org_obj), 
         'has_delete_permission':self.has_delete_permission(self.org_obj), 
         'has_file_field':True, 
         'has_absolute_url':hasattr(self.model, 'get_absolute_url'), 
         'form_url':'', 
         'content_type_id':ContentType.objects.get_for_model(self.model).id, 
         'save_as':self.save_as, 
         'save_on_top':self.save_on_top}
        new_context.update({'onclick_attrib':'', 
         'show_delete_link':new_context['has_delete_permission'] and change or new_context['show_delete'], 
         'show_save_as_new':change and self.save_as, 
         'show_save_and_add_another':new_context['has_add_permission'] and not self.save_as or add, 
         'show_save_and_continue':new_context['has_change_permission'], 
         'show_save':True})
        if self.org_obj:
            if new_context['show_delete_link']:
                new_context['delete_url'] = self.model_admin_url('delete', self.org_obj.pk)
        context = super(ModelFormAdminView, self).get_context()
        context.update(new_context)
        return context

    @filter_hook
    def get_error_list(self):
        errors = forms.utils.ErrorList()
        if self.form_obj.is_bound:
            errors.extend(self.form_obj.errors.values())
        return errors

    @filter_hook
    def get_media(self):
        return super(ModelFormAdminView, self).get_media() + self.form_obj.media + self.vendor('xadmin.page.form.js', 'xadmin.form.css')


class CreateAdminView(ModelFormAdminView):

    def init_request(self, *args, **kwargs):
        self.org_obj = None
        if not self.has_add_permission():
            raise PermissionDenied
        self.prepare_form()

    @filter_hook
    def get_form_datas(self):
        if self.request_method == 'get':
            initial = dict(self.request.GET.items())
            for k in initial:
                try:
                    f = self.opts.get_field(k)
                except models.FieldDoesNotExist:
                    continue

                if isinstance(f, models.ManyToManyField):
                    initial[k] = initial[k].split(',')

            return {'initial': initial}
        return {'data':self.request.POST,  'files':self.request.FILES}

    @filter_hook
    def get_context(self):
        new_context = {'title': _('Add %s') % force_text(self.opts.verbose_name)}
        context = super(CreateAdminView, self).get_context()
        context.update(new_context)
        return context

    @filter_hook
    def get_breadcrumb(self):
        bcs = super(ModelFormAdminView, self).get_breadcrumb()
        item = {'title': _('Add %s') % force_text(self.opts.verbose_name)}
        if self.has_add_permission():
            item['url'] = self.model_admin_url('add')
        bcs.append(item)
        return bcs

    @filter_hook
    def get_response(self):
        context = self.get_context()
        context.update(self.kwargs or {})
        return TemplateResponse(self.request, self.add_form_template or self.get_template_list('views/model_form.html'), context)

    @filter_hook
    def post_response(self):
        """
        Determines the HttpResponse for the add_view stage.
        """
        request = self.request
        msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name':force_text(self.opts.verbose_name),  'obj':"<a class='alert-link' href='%s'>%s</a>" % (self.model_admin_url('change', self.new_obj._get_pk_val()), force_text(self.new_obj))}
        if '_continue' in request.POST:
            self.message_user(msg + ' ' + _('You may edit it again below.'), 'success')
            return self.model_admin_url('change', self.new_obj._get_pk_val())
        if '_addanother' in request.POST:
            self.message_user(msg + ' ' + _('You may add another %s below.') % force_text(self.opts.verbose_name), 'success')
            return request.path
        self.message_user(msg, 'success')
        if '_redirect' in request.POST:
            return request.POST['_redirect']
        if self.has_view_permission():
            return self.model_admin_url('changelist')
        return self.get_admin_url('index')


class UpdateAdminView(ModelFormAdminView):

    def init_request(self, object_id, *args, **kwargs):
        self.org_obj = self.get_object(unquote(object_id))
        if not self.has_change_permission(self.org_obj):
            raise PermissionDenied
        if self.org_obj is None:
            raise Http404(_('%(name)s object with primary key %(key)r does not exist.') % {'name':force_text(self.opts.verbose_name), 
             'key':escape(object_id)})
        self.prepare_form()

    @filter_hook
    def get_form_datas(self):
        params = {'instance': self.org_obj}
        if self.request_method == 'post':
            params.update({'data':self.request.POST, 
             'files':self.request.FILES})
        return params

    @filter_hook
    def get_context(self):
        new_context = {'title':_('Change %s') % force_text(self.org_obj), 
         'object_id':str(self.org_obj.pk)}
        context = super(UpdateAdminView, self).get_context()
        context.update(new_context)
        return context

    @filter_hook
    def get_breadcrumb(self):
        bcs = super(ModelFormAdminView, self).get_breadcrumb()
        item = {'title': force_text(self.org_obj)}
        if self.has_change_permission():
            item['url'] = self.model_admin_url('change', self.org_obj.pk)
        bcs.append(item)
        return bcs

    @filter_hook
    def get_response(self, *args, **kwargs):
        context = self.get_context()
        context.update(kwargs or {})
        return TemplateResponse(self.request, self.change_form_template or self.get_template_list('views/model_form.html'), context)

    def post(self, request, *args, **kwargs):
        if '_saveasnew' in self.request.POST:
            return self.get_model_view(CreateAdminView, self.model).post(request)
        return (super(UpdateAdminView, self).post)(request, *args, **kwargs)

    @filter_hook
    def post_response(self):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = self.new_obj._meta
        obj = self.new_obj
        request = self.request
        verbose_name = opts.verbose_name
        pk_value = obj._get_pk_val()
        msg = _('The %(name)s "%(obj)s" was changed successfully.') % {'name':force_text(verbose_name), 
         'obj':force_text(obj)}
        if '_continue' in request.POST:
            self.message_user(msg + ' ' + _('You may edit it again below.'), 'success')
            return request.path
        if '_addanother' in request.POST:
            self.message_user(msg + ' ' + _('You may add another %s below.') % force_text(verbose_name), 'success')
            return self.model_admin_url('add')
        self.message_user(msg, 'success')
        if '_redirect' in request.POST:
            return request.POST['_redirect']
        if self.has_view_permission():
            change_list_url = self.model_admin_url('changelist')
            if 'LIST_QUERY' in self.request.session:
                if self.request.session['LIST_QUERY'][0] == self.model_info:
                    change_list_url += '?' + self.request.session['LIST_QUERY'][1]
            return change_list_url
        return self.get_admin_url('index')


class ModelFormAdminUtil(ModelFormAdminView):

    def init_request(self, obj=None):
        self.org_obj = obj
        self.prepare_form()
        self.instance_forms()

    @filter_hook
    def get_form_datas(self):
        return {'instance': self.org_obj}