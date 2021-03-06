# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/payments/templatetags/payments_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 2196 bytes
from django.conf import settings
from django.template import Library
register = Library()

@register.inclusion_tag('payments/top_nav_items.html', takes_context=True)
def payment_current_app(context, payment=None):
    context.update({'app_object': payment})
    return context


@register.inclusion_tag('payments/nav.html', takes_context=True)
def payment_nav(context, payment=None):
    context.update({'nav_object': payment})
    return context


@register.inclusion_tag('payments/thankyou_display.html')
def payment_thankyou_display(request, payment):
    obj_header = None
    obj_display = None
    if not payment:
        obj = None
    else:
        obj = payment.invoice.get_object()
        if obj:
            if obj._meta.model_name == 'membershipset':
                obj, = obj.memberships()[:1] or [None]
        if obj:
            from django.template.loader import render_to_string
            from django.template import TemplateDoesNotExist
            app_label = obj._meta.app_label
            template_name = '%s/payment_thankyou_display.html' % app_label
            try:
                obj_display = render_to_string(template_name=template_name, context={'obj':obj,  'payment':payment},
                  request=request)
            except (TemplateDoesNotExist, IOError):
                pass

            template_name = '%s/payment_thankyou_header.html' % app_label
            try:
                obj_header = render_to_string(template_name=template_name, context={'obj':obj,  'payment':payment},
                  request=request)
            except (TemplateDoesNotExist, IOError):
                pass

    return {'request':request, 
     'payment':payment, 
     'obj':obj, 
     'obj_header':obj_header, 
     'obj_display':obj_display}


@register.inclusion_tag('payments/stripe/js_stripe_key.html', takes_context=True)
def set_stripe_key(context):
    context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
    return context