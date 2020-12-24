# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simple_autocomplete/widgets.py
# Compiled at: 2017-09-18 04:36:14
import pickle
from django.forms.widgets import Select, SelectMultiple
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.core.urlresolvers import reverse
from django.conf import settings
from simple_autocomplete.monkey import _simple_autocomplete_queryset_cache
from simple_autocomplete.utils import get_search_fieldname, get_threshold_for_model

class AutoCompleteWidget(Select):
    input_type = 'autocomplete'
    url = None
    initial_display = None
    token = None
    model = None

    def __init__(self, url=None, initial_display=None, token=None, model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].

        initial_display: if url is provided then initial_display is the initial
        content of the autocomplete box, eg. "John Smith".

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        display = ''
        if self.url:
            url = self.url
            display = self.initial_display
        else:
            dc, dc, query = pickle.loads(_simple_autocomplete_queryset_cache[self.token])
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and queryset.count() < threshold:
                return super(AutoCompleteWidget, self).render(name, value, attrs)
        url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])
        if value:
            display = unicode(queryset.get(pk=value))
        html = '\n    <script type="text/javascript">\n    (function($) {\n\n    $(document).ready(function() {\n\n    $("#id_%(name)s_helper").autocomplete({\n        source: function(request, response){\n            $.ajax({\n                url: "%(url)s",\n                data: {q: request.term},\n                success: function(data) {\n                    if (data != \'CACHE_MISS\')\n                    {\n                        response($.map(data, function(item) {\n                            return {\n                                label: item[1],\n                                value: item[1],\n                                real_value: item[0]\n                            };\n                        }));\n                    }\n                },\n                dataType: "json"\n            });\n        },\n        select: function(event, ui) { $(\'#id_%(name)s\').val(ui.item.real_value); },\n        minLength: 3\n    });\n\n    });\n\n    })(django.jQuery);\n    </script>\n\n<input id="id_%(name)s_helper" type="text" value="%(display)s" />\n<a href="#" title="Clear" onclick="django.jQuery(\'#id_%(name)s_helper\').val(\'\'); django.jQuery(\'#id_%(name)s_helper\').focus(); django.jQuery(\'#id_%(name)s\').val(\'\'); return false;">x<small></small></a>\n<input name="%(name)s" id="id_%(name)s" type="hidden" value="%(value)s" />' % dict(name=name, url=url, display=display, value=value)
        return mark_safe(html)


class AutoCompleteMultipleWidget(SelectMultiple):
    input_type = 'autocomplete_multiple'
    url = None
    initial_display = None
    token = None
    model = None

    def __init__(self, url=None, initial_display=None, token=None, model=None, *args, **kwargs):
        """
        url: a custom URL that returns JSON with format [(value, label),(value,
        label),...].

        initial_display: if url is provided then initial_display is a
        dictionary containing the initial content of the autocomplete box, eg.
        {1:"John Smith", 2:"Sarah Connor"}. The key is the primary key of the
        referenced item.

        token: an identifier to retrieve a cached queryset. Used internally.

        model: the model that the queryset objects are instances of. Used
        internally.
        """
        self.url = url
        self.initial_display = initial_display
        self.token = token
        self.model = model
        super(AutoCompleteMultipleWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        display = ''
        if self.url:
            url = self.url
            display = self.initial_display
        else:
            dc, dc, query = pickle.loads(_simple_autocomplete_queryset_cache[self.token])
            queryset = QuerySet(model=self.model, query=query)
            threshold = get_threshold_for_model(self.model)
            if threshold and queryset.count() < threshold:
                return super(AutoCompleteMultipleWidget, self).render(name, value, attrs)
            url = reverse('simple_autocomplete:simple-autocomplete', args=[self.token])
            html = '\n    <script type="text/javascript">\n    (function($) {\n\n    $(document).ready(function() {\n\n    $("#id_%s_helper").autocomplete({\n        source: function(request, response) {\n            $.ajax({\n                url: "%s",\n                data: {q: request.term},\n                success: function(data) {\n                    if (data != \'CACHE_MISS\')\n                    {\n                        response($.map(data, function(item) {\n                            return {\n                                label: item[1],\n                                value: item[1],\n                                real_value: item[0]\n                            };\n                        }));\n                    }\n                },\n                dataType: "json"\n            });\n        },\n        select: function(event, ui) {\n            var name = \'%s\';\n            var parent = $(\'#id_\' + name).parent();\n            var target = $(\'div.autocomplete-placeholder\', parent);\n            target.append(\'<p><input name="\' + name + \'" value="\' + ui.item.real_value + \'" \'\n                + \'type="hidden" />\' + ui.item.value\n                + \' <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery(\'+"\'"+\'#id_%s_helper\'+"\'"+\').val(\' + "\'\'" + \'); django.jQuery(\'+"\'"+\'#id_%s_helper\'+"\'"+\').focus(); return false;">x<small></small></a></p>\');\n        },\n        close: function(event, ui) {\n            django.jQuery(\'#id_%s_helper\').val(\'\');\n        },\n        minLength: 3\n    });\n\n    });\n\n    })(django.jQuery);\n    </script>\n\n<input id="id_%s_helper" type="text" value="" />\n<input id="id_%s" type="hidden" value="" />\n<div class="autocomplete-placeholder">' % (name, url, name, name, name, name, name, name)
            for v in value:
                if v is None:
                    continue
                display = unicode(queryset.get(pk=v))
                html += '<p><input name="%s" type="hidden" value="%s" />\n%s <a href="#" title="Remove" onclick="django.jQuery(this).parent().remove(); django.jQuery(\'#id_%s_helper\').val(\'\'); django.jQuery(\'#id_%s_helper\').focus(); return false;">x<small></small></a></p>' % (name, v, display, name, name)

            html += '</div>'
            html += '<div style="display: inline-block; width: 104px;">&nbsp;</div>'
            return mark_safe(html)
        return