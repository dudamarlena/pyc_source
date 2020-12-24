# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/mass_post_office/management/signal_receivers.py
# Compiled at: 2015-03-06 05:08:58
try:
    from south.signals import post_migrate
    from django.template.loader import find_template
    from django.dispatch import receiver
    from post_office import models as post_office_models
    from ..settings import EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED
    DEFAULT_TEMPLATE_NAMES = [
     'post_office/canceled_subscription',
     'post_office/unsubscribe_page']

    @receiver(post_migrate, dispatch_uid='mass_post_office_models_post_migrate')
    def create_default_templates(sender, app, **kwargs):
        if app != 'post_office':
            return
        try:
            find_template('hello')
        except Exception:
            pass

        from django.template.loader import template_source_loaders
        for template_name in DEFAULT_TEMPLATE_NAMES:
            if template_name in EMAIL_TEMPLATES_SHOULD_BE_OVERRIDED:
                continue
            if post_office_models.EmailTemplate.objects.filter(name=template_name).exists():
                continue
            data = {'html_content': '', 'content': '', 'subject': ''}
            for loader in template_source_loaders:
                for key in data:
                    try:
                        data[key] = loader.load_template_source('%s_%s_default.txt' % (template_name, key))[0]
                    except Exception:
                        pass

            for key in data:
                if not data[key] and key != 'html_content':
                    template_full_name = '%s_%s_default.txt' % (template_name, key)
                    raise ValueError('Cant load template %s' % template_full_name)

            post_office_models.EmailTemplate.objects.create(name=template_name, **data)


except ImportError:
    pass