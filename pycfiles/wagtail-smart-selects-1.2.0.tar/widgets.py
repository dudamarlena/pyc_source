# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rmartins/Desenvolvimento/Django/Apps/wagtaildemo/smart_selects/widgets.py
# Compiled at: 2016-01-06 11:55:57
import locale, django
from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.core.urlresolvers import reverse
from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from django.utils.html import escape
import json
from smart_selects.utils import unicode_sorter, sort_results
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model

if django.VERSION >= (1, 2, 0) and getattr(settings, 'USE_DJANGO_JQUERY', True):
    USE_DJANGO_JQUERY = True
else:
    USE_DJANGO_JQUERY = False
    JQUERY_URL = getattr(settings, 'JQUERY_URL', 'http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js')
URL_PREFIX = getattr(settings, 'SMART_SELECTS_URL_PREFIX', '')

class ChainedSelect(Select):

    def __init__(self, to_app_name, to_model_name, chained_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, show_all, auto_choose, manager=None, view_name=None, *args, **kwargs):
        self.to_app_name = to_app_name
        self.to_model_name = to_model_name
        self.chained_field = chained_field
        self.chained_model_field = chained_model_field
        self.show_all = show_all
        self.auto_choose = auto_choose
        self.manager = manager
        self.view_name = view_name
        self.foreign_key_app_name = foreign_key_app_name
        self.foreign_key_model_name = foreign_key_model_name
        self.foreign_key_field_name = foreign_key_field_name
        super(Select, self).__init__(*args, **kwargs)

    class Media:
        extra = '' if settings.DEBUG else '.min'
        js = []
        js = js + [static('smart-selects/admin/js/chainedfk.js')]

    def render(self, name, value, attrs=None, choices=()):
        if len(name.split('-')) > 1:
            chained_field = ('-').join(name.split('-')[:-1] + [self.chained_field])
        else:
            chained_field = self.chained_field
        if not self.view_name:
            if self.show_all:
                view_name = 'chained_filter_all'
            else:
                view_name = 'chained_filter'
        else:
            view_name = self.view_name
        kwargs = {'app': self.to_app_name, 'model': self.to_model_name, 
           'field': self.chained_model_field, 
           'foreign_key_app_name': self.foreign_key_app_name, 
           'foreign_key_model_name': self.foreign_key_model_name, 
           'foreign_key_field_name': self.foreign_key_field_name, 
           'value': '1'}
        if self.manager is not None:
            kwargs.update({'manager': self.manager})
        url = URL_PREFIX + ('/').join(reverse(view_name, kwargs=kwargs).split('/')[:-2])
        if self.auto_choose:
            auto_choose = 'true'
        else:
            auto_choose = 'false'
        iterator = iter(self.choices)
        if hasattr(iterator, '__next__'):
            empty_label = iterator.__next__()[1]
        else:
            empty_label = iterator.next()[1]
        js = '\n        <script type="text/javascript">\n        (function($) {\n            var chainfield = "#id_%(chainfield)s";\n            var url = "%(url)s";\n            var id = "#%(id)s";\n            var value = %(value)s;\n            var auto_choose = %(auto_choose)s;\n            var empty_label = "%(empty_label)s";\n\n            $(document).ready(function() {\n                chainedfk.init(chainfield, url, id, value, empty_label, auto_choose);\n            });\n        })(jQuery || django.jQuery);\n        </script>\n\n        '
        js = js % {'chainfield': chained_field, 'url': url, 
           'id': attrs['id'], 
           'value': 'undefined' if value is None else value, 
           'auto_choose': auto_choose, 
           'empty_label': escape(empty_label)}
        final_choices = []
        if value:
            available_choices = self._get_available_choices(self.queryset, value)
            for choice in available_choices:
                final_choices.append((choice.pk, force_text(choice)))

        if len(final_choices) > 1:
            final_choices = [
             (
              '', empty_label)] + final_choices
        if self.show_all:
            final_choices.append(('', empty_label))
            self.choices = list(self.choices)
            self.choices.sort(key=lambda x: unicode_sorter(x[1]))
            for ch in self.choices:
                if ch not in final_choices:
                    final_choices.append(ch)

        self.choices = ()
        final_attrs = self.build_attrs(attrs, name=name)
        if 'class' in final_attrs:
            final_attrs['class'] += ' chained'
        else:
            final_attrs['class'] = 'chained'
        output = super(ChainedSelect, self).render(name, value, final_attrs, choices=final_choices)
        output += js
        return mark_safe(output)

    def _get_available_choices(self, queryset, value):
        """
        get possible choices for selection
        """
        item = queryset.filter(pk=value).first()
        if item:
            try:
                pk = getattr(item, self.chained_model_field + '_id')
                filter = {self.chained_model_field: pk}
            except AttributeError:
                try:
                    pks = getattr(item, self.chained_model_field).all().values_list('pk', flat=True)
                    filter = {self.chained_model_field + '__in': pks}
                except AttributeError:
                    try:
                        pks = getattr(item, self.chained_model_field + '_set').all().values_list('pk', flat=True)
                        filter = {self.chained_model_field + '__in': pks}
                    except:
                        filter = {}

            filtered = list(get_model(self.to_app_name, self.to_model_name).objects.filter(**filter).distinct())
            sort_results(filtered)
        else:
            filtered = []
        return filtered


class ChainedSelectMultiple(SelectMultiple):

    def __init__(self, to_app_name, to_model_name, chain_field, chained_model_field, foreign_key_app_name, foreign_key_model_name, foreign_key_field_name, auto_choose, manager=None, *args, **kwargs):
        self.to_app_name = to_app_name
        self.to_model_name = to_model_name
        self.chain_field = chain_field
        self.chained_model_field = chained_model_field
        self.auto_choose = auto_choose
        self.manager = manager
        self.foreign_key_app_name = foreign_key_app_name
        self.foreign_key_model_name = foreign_key_model_name
        self.foreign_key_field_name = foreign_key_field_name
        super(SelectMultiple, self).__init__(*args, **kwargs)

    class Media:
        extra = '' if settings.DEBUG else '.min'
        js = [
         'jquery%s.js' % extra,
         'jquery.init.js']
        if USE_DJANGO_JQUERY:
            js = [ static('admin/js/%s' % url) for url in js ]
        elif JQUERY_URL:
            js = [
             JQUERY_URL]
        js = js + [static('smart-selects/admin/js/chainedm2m.js')]

    def render(self, name, value, attrs=None, choices=()):
        if len(name.split('-')) > 1:
            chain_field = ('-').join(name.split('-')[:-1] + [self.chain_field])
        else:
            chain_field = self.chain_field
        view_name = 'chained_filter'
        kwargs = {'app': self.to_app_name, 
           'model': self.to_model_name, 
           'field': self.chained_model_field, 
           'foreign_key_app_name': self.foreign_key_app_name, 
           'foreign_key_model_name': self.foreign_key_model_name, 
           'foreign_key_field_name': self.foreign_key_field_name, 
           'value': '1'}
        if self.manager is not None:
            kwargs.update({'manager': self.manager})
        url = URL_PREFIX + ('/').join(reverse(view_name, kwargs=kwargs).split('/')[:-2])
        if self.auto_choose:
            auto_choose = 'true'
        else:
            auto_choose = 'false'
        js = '\n        <script type="text/javascript">\n        (function($) {\n\n        var chainfield = "#id_%(chainfield)s";\n        var url = "%(url)s";\n        var id = "#%(id)s";\n        var value = %(value)s;\n        var auto_choose = %(auto_choose)s;\n\n        $(document).ready(function() {\n            chainedm2m.init(chainfield, url, id, value, auto_choose);\n        });\n        })(jQuery || django.jQuery);\n        </script>\n\n        '
        js = js % {'chainfield': chain_field, 'url': url, 
           'id': attrs['id'], 
           'value': json.dumps(value), 
           'auto_choose': auto_choose}
        final_choices = []
        self.choices = ()
        final_attrs = self.build_attrs(attrs, name=name)
        if 'class' in final_attrs:
            final_attrs['class'] += ' chained'
        else:
            final_attrs['class'] = 'chained'
        output = super(ChainedSelectMultiple, self).render(name, value, final_attrs, choices=final_choices)
        output += js
        return mark_safe(output)