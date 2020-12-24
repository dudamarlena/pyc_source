# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/templatetags/moneta.py
# Compiled at: 2018-01-20 04:55:34
# Size of source mod 2**32: 3091 bytes
from bootstrap3.templatetags.bootstrap3 import get_pagination_context
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
register = template.Library()

@register.filter
def extra_repo_urls(repo, request):
    return repo.get_model().extra_index_urls(request, repo)


@register.filter
def moneta_url(repo, view_name='index'):
    if repo.is_private:
        return 'repository:authb-%s:%s' % (repo.archive_type, view_name)
    else:
        return 'repository:%s:%s' % (repo.archive_type, view_name)


@register.filter
def checksum(element, value):
    if element.repository.is_private:
        return reverse('moneta:get_checksum', kwargs={'eid':element.id,  'value':value})
    else:
        return reverse('moneta:get_checksum_p', kwargs={'eid':element.id,  'value':value})


@register.filter
def direct_link(element):
    if element.repository.is_private:
        return reverse('moneta:get_file', kwargs={'eid':element.id,  'name':element.filename})
    else:
        return reverse('moneta:get_file_p', kwargs={'eid':element.id,  'name':element.filename})


@register.filter
def human_join(list_of_elements):
    if not list_of_elements:
        return ''
    else:
        if len(list_of_elements) == 1:
            return list_of_elements[0]
        result = _(', ').join([str(x) for x in list_of_elements[:-1]])
        result += _(' and ') + str(list_of_elements[(-1)])
        return result


@register.filter
def signature(signature_, element=None):
    if element is None:
        element = signature_.element
    if element.repository.is_private:
        return reverse('moneta:get_signature', kwargs={'eid':element.id,  'sid':signature_.id})
    else:
        return reverse('moneta:get_signature_p', kwargs={'eid':element.id,  'sid':signature_.id})


@register.filter
def auth_moneta_url(repo, view_name='index'):
    return 'repository:auth-%s:%s' % (repo.archive_type, view_name)


@register.inclusion_tag('bootstrap3/pagination.html')
def bootstrap_pagination_extra(page, search=None):
    """
    Render pagination for a page

    **Tag name**::

        bootstrap_pagination

    **Parameters**:

        :page:
        :kwargs:

    **usage**::

        {% bootstrap_pagination FIXTHIS %}

    **example**::

        {% bootstrap_pagination FIXTHIS %}
    """
    pagination_kwargs = {'extra':'search=%s' % search, 
     'page':page}
    return get_pagination_context(**pagination_kwargs)


class CurlNode(template.Node):

    def __init__(self, repo=None):
        super().__init__()
        self.repo_token = repo

    def render(self, context):
        if self.repo_token:
            if not context[self.repo_token].is_private:
                return mark_safe('curl')
        if context['df_remote_authenticated']:
            return mark_safe('curl --anyauth -u :')
        else:
            return mark_safe('curl --basic -u $MONETA_USER:$MONETA_PASSWORD')


@register.tag('curl')
def do_curl(parser, token):
    bits = list(token.split_contents())
    tagname = bits[0]
    repo = bits[1] if len(bits) > 1 else None
    return CurlNode(repo)