# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/projects/templatetags/project_tags.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1620 bytes
from django.template import Library, TemplateSyntaxError
from tendenci.apps.projects.models import Project
from tendenci.apps.base.template_tags import ListNode, parse_tag_kwargs
register = Library()

class ListProjectsNode(ListNode):
    model = Project
    perms = 'projects.view_project'


@register.inclusion_tag('projects/top_nav_items.html', takes_context=True)
def project_current_app(context, user, project=None):
    context.update({'app_object':project, 
     'user':user})
    return context


@register.inclusion_tag('projects/nav.html', takes_context=True)
def project_nav(context, user, project=None):
    context.update({'nav_object':project, 
     'user':user})
    return context


@register.tag
def list_projects(parser, token):
    """
    Example:

    {% list_projects as projects_list [user=user limit=3 tags=bloop bleep q=searchterm] %}
    {% for project in projects %}
        {{ project.something }}
    {% endfor %}
    """
    args, kwargs = [], {}
    bits = token.split_contents()
    context_var = bits[2]
    if len(bits) < 3:
        message = "'%s' tag requires more than 2" % bits[0]
        raise TemplateSyntaxError(message)
    if bits[1] != 'as':
        message = "'%s' second argument must be 'as'" % bits[0]
        raise TemplateSyntaxError(message)
    kwargs = parse_tag_kwargs(bits)
    if 'order' not in kwargs:
        kwargs['order'] = '-create_dt'
    return ListProjectsNode(context_var, *args, **kwargs)


@register.inclusion_tag('projects/search-form.html', takes_context=True)
def project_search(context):
    return context