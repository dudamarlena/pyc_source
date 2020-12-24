# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/breno/Envs/djangoplus/lib/python3.6/site-packages/djangoplus/ui/components/select/widgets.py
# Compiled at: 2018-09-24 08:48:06
# Size of source mod 2**32: 13367 bytes
import os
from django.forms import widgets
from djangoplus.test import cache
from django.utils.safestring import mark_safe
from djangoplus.utils.metadata import get_metadata
from django.template.loader import render_to_string
from djangoplus.utils.serialization import dumps_qs_query
INIT_SCRIPT = '{html}\n<script>\n    $("#id_{name}").select2({{\n        allowClear: true,\n        language: \'pt-BR\',\n        {templates}\n        escapeMarkup: function (markup) {{ var links = markup==\'Nenhum resultado encontrado\'? \'<div>{links}</dev>\' : \'\'; return markup + links; }}}}).on(\'select2:unselecting\',\n        function() {{\n            $(this).data(\'unselecting\', true);}}).on(\n            \'select2:opening\',\n            function(e) {{\n                if ($(this).data(\'unselecting\')) {{\n                    $(this).removeData(\'unselecting\');\n                    e.preventDefault();\n                }}\n            }}\n        );\n    function load{function_name}(value){{\n        $(\'#id_{name}\').val(value);\n        $(\'#id_{name}\').trigger("change");\n    }}\n</script>'
AJAX_INIT_SCRIPT = '{html}\n<script>\n    window[\'qs_{name}\'] = {{ \'qs\' : \'{qs_dump}\' }}\n    $(\'#id_{name}\').select2({{\n        allowClear: true,\n        language: \'pt-BR\',\n        escapeMarkup: function (markup) {{ var links = markup==\'Nenhum resultado encontrado\'? \'<div>{links}</dev>\' : \'\'; return markup + links; }},\n        ajax: {{\n            delay: 500,\n            dataType: \'json\',\n            type: \'POST\',\n            url:\'/autocomplete/{app_label}/{model_name}/\',\n            data: function (params) {{return {{qs: window[\'qs_{name}\'], q:params.term}}}},\n            cache: true,\n            transport: function (params, success, failure) {{\n                if({minimum_input_length}==0 && $(\'#id_{name}\').prop(\'cache\')){{\n                    success($(\'#id_{name}\').prop(\'cache\'));\n                }} else {{\n                    var request = $.ajax(params);\n                    request.then(success);\n                    request.fail(failure);\n                    return request;\n                }}\n            }},\n            success: function(data){{\n                if({minimum_input_length}==0) $(\'#id_{name}\').prop(\'cache\', data);\n                var values = $(\'#id_{name}\').val();\n                $(\'#id_{name}\').append($(\'<option></option>\').attr("value", "").text(""));\n                for(var i=0; i<data.results.length; i++){{\n                    var option = $(\'<option></option>\').attr("value", data.results[i].id).text(data.results[i].text)\n                    $(\'#id_{name}\').append(option);\n                }}\n            }}\n        }},\n        minimumInputLength: {minimum_input_length},\n        templateResult: function (item) {{if (item.loading) return item.text; return item.html;}}\n        }}\n    );\n    $(\'#id_{name}\').on("select2:unselecting", function (e) {{\n        $(\'#id_{name}\').val(\'\').trigger("change");\n        e.preventDefault();\n    }});\n    function load{function_name}(value, text){{\n        var option = $(\'<option></option>\').attr("value", value).text(text).attr("selected", true);\n        $(\'#id_{name}\').append(option);\n    }}\n</script>\n'
RELOAD_SCRIPT = '\n<script>\n    function reload_{function_name}(){{\n        var pk = $(\'#id_{popup}{field_name}\').val()\n        if(!pk) pk = 0;\n        $.ajax({{url:"/reload_options/{app_label}/{model_name}/{value}/{lookup}/"+pk+"/{lazy}/", dataType:\'json\', success:function( data ) {{\n            if({lazy}){{\n                window[\'qs_{name}\'][\'qs\'] = data.qs;\n            }} else {{\n                $(\'#id_{name}\').select2(\'destroy\').empty().select2({{allowClear: true, data: data.results}});\n                $(\'#id_{name}\').val(\'{value}\'.split(\'_\'));\n            }}\n            $(\'#id_{name}\').trigger("change");\n        }}}});\n    }}\n    $(\'#id_{popup}{field_name}\').on(\'change\', function(e) {{\n        reload_{function_name}();\n    }});\n    reload_{function_name}();\n</script>\n'
ADD_LINK = '<a class="pull-right popup" style="padding:5px" href="javascript:" onclick="$(\\\'#id_{}\\\').select2(\\\'close\\\');popup(\\\'/add/{}/{}/?select=id_{}\\\');"><i class="fa fa-plus">\\</i>Adicionar {}</a>'

class SelectWidget(widgets.Select):

    class Media:
        css = {'all': ('/static/css/select2.min.css', )}
        js = ('/static/js/select2.min.js', '/static/js/i18n/pt-BR.js')

    def __init__(self, *args, **kwargs):
        (super(SelectWidget, self).__init__)(*args, **kwargs)
        self.lazy = False
        self.form_filters = []
        self.minimum_input_length = 3

    def render(self, name, value, attrs=None, renderer=None):
        if cache.HEADLESS:
            self.lazy = False
        else:
            attrs['class'] = 'form-control'
            if 'data-placeholder' not in self.attrs:
                attrs['data-placeholder'] = ' '
            else:
                queryset = None
                if self.lazy:
                    if hasattr(self.choices, 'queryset'):
                        queryset = self.choices.queryset
                        self.choices.queryset = self.choices.queryset.model.objects.filter(pk=(value or 0))
                model = None
                links = []
                templates = []
                if hasattr(self.choices, 'queryset'):
                    model = self.choices.queryset.model
                    models = model.__subclasses__() or [model]
                    if not self.lazy:
                        select_template = get_metadata(model, 'select_template')
                        select_display = get_metadata(model, 'select_display')
                        if select_template or select_display:
                            templates_var_name = name.replace('-', '_')
                            templates.append('templateResult: function (item) {{{}_templates = Array();'.format(templates_var_name))
                            if hasattr(self.choices.queryset.model, 'get_tree_index_field'):
                                tree_index_field = self.choices.queryset.model.get_tree_index_field()
                                if tree_index_field:
                                    self.choices.queryset = self.choices.queryset.order_by(tree_index_field.name)
                            for obj in self.choices.queryset:
                                obj_html = render_to_string(select_template or 'select_template.html', dict(obj=obj, select_display=select_display)) or str(obj)
                                templates.append("{}_templates[{}] = '{}';".format(templates_var_name, obj.pk, obj_html.replace('\n', '')))

                            templates.append('return {}_templates[item.id];}},'.format(templates_var_name))
                    if hasattr(self, 'user'):
                        for tmp in models:
                            class_name = tmp.__name__.lower()
                            app_label = get_metadata(tmp, 'app_label')
                            perm = '{}.add_{}'.format(app_label, class_name)
                            if self.user.has_perm(perm):
                                links.append(ADD_LINK.format(name, app_label, class_name, name, get_metadata(tmp, 'verbose_name')))

                html = super(SelectWidget, self).render(name, value, attrs)
                html = html.replace('---------', '')
                function_name = name.replace('-', '__')
                if model:
                    if self.lazy:
                        app_label = get_metadata(model, 'app_label')
                        model_name = model.__name__.lower()
                        qs_dump = dumps_qs_query(queryset)
                        html = AJAX_INIT_SCRIPT.format(html=html, name=name, function_name=function_name, qs_dump=qs_dump, app_label=app_label, model_name=model_name, links=(''.join(links)), minimum_input_length=(self.minimum_input_length))
                html = INIT_SCRIPT.format(html=html, name=name, function_name=function_name, links=(''.join(links)), templates=(''.join(templates)))
            if model:
                value = value or 0
                lazy = self.lazy and 1 or 0
                for field_name, lookup in self.form_filters:
                    if '-' in name:
                        field_name = '{}-{}'.format(name.split('-')[0], field_name)
                    app_label = get_metadata(model, 'app_label')
                    model_name = model.__name__.lower()
                    function_name = name.replace('-', '__')
                    popup = 'popup' in function_name and 'popup-' or ''
                    reload_script = RELOAD_SCRIPT.format(function_name=function_name,
                      field_name=field_name,
                      app_label=app_label,
                      model_name=model_name,
                      value=value,
                      lookup=lookup,
                      lazy=lazy,
                      name=name,
                      popup=popup)
                    html = '{} {}'.format(html, reload_script)

        return mark_safe(html)


class SelectMultipleWidget(widgets.SelectMultiple):

    class Media:
        css = {'all': ('/static/css/select2.min.css', )}
        js = ('/static/js/select2.min.js', '/static/js/i18n/pt-BR.js')

    def __init__(self, *args, **kwargs):
        (super(SelectMultipleWidget, self).__init__)(*args, **kwargs)
        self.lazy = False
        self.form_filters = []
        self.minimum_input_length = 3

    def render(self, name, value, attrs=None, renderer=None):
        if cache.HEADLESS:
            self.lazy = False
        else:
            attrs['class'] = 'form-control'
            attrs['data-placeholder'] = ' '
            queryset = None
            templates = []
            if hasattr(self.choices, 'queryset'):
                queryset = self.choices.queryset.all()
                if self.lazy:
                    self.choices.queryset = self.choices.queryset.model.objects.filter(pk__in=(value or []))
                else:
                    select_template = get_metadata(queryset.model, 'select_template')
                    select_display = get_metadata(queryset.model, 'select_display')
                    if select_template or select_display:
                        templates_var_name = name.replace('-', '_')
                        templates.append('templateResult: function (item) {{{}_templates = Array();'.format(templates_var_name))
                        if hasattr(self.choices.queryset.model, 'get_tree_index_field'):
                            tree_index_field = self.choices.queryset.model.get_tree_index_field()
                            if tree_index_field:
                                self.choices.queryset = self.choices.queryset.order_by(tree_index_field.name)
                        for obj in self.choices.queryset.all():
                            obj_html = render_to_string(select_template or 'select_template.html', dict(obj=obj, select_display=select_display)) or str(obj)
                            templates.append("{}_templates[{}] = '{}';".format(templates_var_name, obj.pk, obj_html.replace('\n', '')))

                        templates.append('return {}_templates[item.id];}},'.format(templates_var_name))
            html = super(SelectMultipleWidget, self).render(name, value, attrs)
            links = []
            if queryset:
                models = queryset.model.__subclasses__() or [queryset.model]
                if hasattr(self, 'user'):
                    for tmp in models:
                        class_name = tmp.__name__.lower()
                        app_label = get_metadata(tmp, 'app_label')
                        perm = '{}.add_{}'.format(app_label, class_name)
                        if self.user.has_perm(perm):
                            links.append(ADD_LINK.format(name, app_label, class_name, name, get_metadata(tmp, 'verbose_name')))

            else:
                function_name = name.replace('-', '__')
                if queryset.model:
                    if self.lazy:
                        app_label = get_metadata(queryset.model, 'app_label')
                        model_name = queryset.model.__name__.lower()
                        qs_dump = dumps_qs_query(queryset)
                        html = AJAX_INIT_SCRIPT.format(html=html, name=name, function_name=function_name, qs_dump=qs_dump, app_label=app_label, model_name=model_name, links=(''.join(links)), minimum_input_length=(self.minimum_input_length))
                html = INIT_SCRIPT.format(html=html, name=name, function_name=function_name, links=(''.join(links)), templates=(''.join(templates)))
            if queryset.model:
                l = []
                if value:
                    for pk in value:
                        l.append(str(pk))

                else:
                    l.append('0')
                lazy = self.lazy and 1 or 0
                for field_name, lookup in self.form_filters:
                    app_label = get_metadata(queryset.model, 'app_label')
                    model_name = queryset.model.__name__.lower()
                    value = '_'.join(l)
                    function_name = name.replace('-', '__')
                    popup = 'popup' in function_name and 'popup-' or ''
                    reload_script = RELOAD_SCRIPT.format(function_name=function_name, field_name=field_name, popup=popup, app_label=app_label,
                      model_name=model_name,
                      value=value,
                      lookup=lookup,
                      lazy=lazy,
                      name=name)
                    html = '{} {}'.format(html, reload_script)

        return mark_safe(html)


class NullBooleanSelect(widgets.NullBooleanSelect):

    class Media:
        css = {'all': ('/static/css/select2.min.css', )}
        js = ('/static/js/select2.min.js', '/static/js/i18n/pt-BR.js')

    def render(self, name, value, attrs=None, renderer=None):
        attrs['class'] = 'form-control'
        if 'data-placeholder' not in self.attrs:
            attrs['data-placeholder'] = ' '
        function_name = name.replace('-', '__')
        html = super(NullBooleanSelect, self).render(name, value, attrs)
        html = INIT_SCRIPT.format(html=html, name=name, function_name=function_name, templates='', links='')
        return mark_safe(html)