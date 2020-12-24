# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/altus/gitArchives/django/_instances/django-formfactory/formfactory/templatetags/formfactory_tags.py
# Compiled at: 2017-11-28 02:57:16
from django import template
from django.core.urlresolvers import reverse, resolve
from django.http import Http404
from formfactory import models
register = template.Library()

@register.tag()
def render_form(parser, token):
    """{% render_form <form_slug> %}"""
    tokens = token.split_contents()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError('{% render_form <form_slug>/<object> %}')
    return RenderFormNode(variable=tokens[1])


class RenderFormNode(template.Node):

    def __init__(self, variable):
        self.variable = template.Variable(variable)

    def render(self, context):
        try:
            variable = self.variable.resolve(context)
        except template.VariableDoesNotExist:
            variable = self.variable.var

        default_msg = 'No FormFactory Form matches the given query. %s' % self.variable
        if isinstance(variable, basestring):
            try:
                form = models.Form.objects.get(slug=variable)
            except models.Form.DoesNotExist:
                raise Http404(default_msg)

        elif isinstance(variable, models.Form):
            form = variable
        else:
            raise Http404(default_msg)
        url = form.absolute_url
        view, args, kwargs = resolve(url)
        request = context['request']
        original_method = request.method
        original_path = request.path
        original_info = request.path_info
        request.method = 'GET'
        request.path = url
        request.path_info = url
        kwargs['inclusion_tag'] = True
        result = view(request, *args, **kwargs)
        request.method = original_method
        request.path = original_path
        request.path_info = original_path
        result.render()
        html = result.rendered_content
        return html