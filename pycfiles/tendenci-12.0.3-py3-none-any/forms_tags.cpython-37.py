# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/forms_builder/forms/templatetags/forms_tags.py
# Compiled at: 2020-02-26 14:49:27
# Size of source mod 2**32: 4489 bytes
from django.template import Library
from django.contrib.auth.models import AnonymousUser
from django.utils.safestring import mark_safe
from tendenci.apps.forms_builder.forms.forms import FormForForm
from tendenci.apps.forms_builder.forms.models import Form
register = Library()

@register.inclusion_tag('forms/options.html', takes_context=True)
def forms_options(context, user, form):
    context.update({'opt_object':form, 
     'user':user})
    return context


@register.inclusion_tag('forms/nav.html', takes_context=True)
def forms_nav(context, user, form=None):
    context.update({'nav_object':form, 
     'user':user})
    return context


@register.inclusion_tag('forms/search-form.html', takes_context=True)
def forms_search(context):
    return context


@register.inclusion_tag('forms/top_nav_items.html', takes_context=True)
def form_current_app(context, user, form=None):
    app_object = form
    if not (form and hasattr(form, 'pk')):
        app_object = None
    context.update({'app_object':app_object, 
     'user':user})
    return context


@register.inclusion_tag('forms/entry_options.html', takes_context=True)
def forms_entry_options(context, user, entry):
    context.update({'opt_object':entry, 
     'user':user})
    return context


@register.simple_tag(takes_context=True)
def embed_form(context, pk, *args, **kwargs):
    """
    Example:
        {% embed_form 123 [template] [gsize='compact'] %}
    """
    if len(args) > 0:
        template_name = args[0]
    else:
        template_name = 'forms/embed_form_new.html'
    form, = Form.objects.filter(pk=pk)[:1] or [None]
    if not form:
        return ''
    elif hasattr(form, 'object'):
        form_obj = form.object
    else:
        form_obj = form
    try:
        context['embed_form'] = form_obj
        context['embed_form_for_form'] = FormForForm(form_obj, AnonymousUser())
        if 'captcha' in context['embed_form_for_form'].fields:
            if 'gsize' in kwargs:
                if hasattr(context['embed_form_for_form'].fields['captcha'].widget, 'gtag_attrs'):
                    context['embed_form_for_form'].fields['captcha'].widget.gtag_attrs.update({'data-size': kwargs['gsize']})
        template = context.template.engine.get_template(template_name)
        output = '<div class="embed-form">%s</div>' % template.render(context=context)
        return mark_safe(output)
    except:
        return ''


@register.filter
def media_url(field):
    """
    example: field|media_url
    """
    from django.urls import reverse
    return reverse('form_files', args=[field.pk])