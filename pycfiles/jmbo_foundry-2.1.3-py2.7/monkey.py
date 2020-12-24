# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/monkey.py
# Compiled at: 2015-04-30 10:11:23
"""Patch BaseCommentNode queryset method so comments are not constrained to
only one site. Our convention is that basic, smart and web site ids always fall
into a certain numerical range.  Use this fact to relax the query."""
from django.contrib.comments.templatetags.comments import BaseCommentNode
from django.utils.encoding import smart_unicode
from django.conf import settings

def BaseCommentNode_get_query_set(self, context):
    ctype, object_pk = self.get_target_ctype_pk(context)
    if not object_pk:
        return self.comment_model.objects.none()
    i = settings.SITE_ID / 10
    site_ids = range(i * 10 + 1, (i + 1) * 10)
    qs = self.comment_model.objects.filter(content_type=ctype, object_pk=smart_unicode(object_pk), site__pk__in=site_ids)
    field_names = [ f.name for f in self.comment_model._meta.fields ]
    if 'is_public' in field_names:
        qs = qs.filter(is_public=True)
    if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
        qs = qs.filter(is_removed=False)
    return qs


BaseCommentNode.get_query_set = BaseCommentNode_get_query_set
from django.db.models import Q
from django.db.models.aggregates import Max
from django.contrib.comments.templatetags.comments import CommentListNode

def CommentListNode_get_query_set(self, context):
    qs = super(CommentListNode, self).get_query_set(context)
    if context['request'].REQUEST.get('my_messages'):
        user = context['request'].user
        if user.is_authenticated():
            q1 = Q(user=user)
            q2 = Q(in_reply_to__user=user)
            qs = qs.filter(q1 | q2)
    setattr(context, 'foundry_last_comment_id', qs.aggregate(Max('id'))['id__max'] or 0)
    return qs


CommentListNode.get_query_set = CommentListNode_get_query_set
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import ErrorList

def errorlist_as_div(self):
    if not self:
        return ''
    return mark_safe('<div class="errorlist">%s</div>' % ('').join([ '<div class="error">%s</div>' % conditional_escape(force_unicode(e)) for e in self ]))


ErrorList.__unicode__ = errorlist_as_div
import re
from django.utils.functional import curry
from django.conf import settings
import photologue
from photologue.models import PhotoSize, ImageModel, size_method_map

class LayerAwareSizes(dict):

    def get(self, key):
        result = None
        layers = reversed(list(settings.LAYERS['layers']))
        for layer in layers:
            result = super(LayerAwareSizes, self).get(key + '_' + layer)
            if result is not None:
                break

        if result is None:
            result = super(LayerAwareSizes, self).get(key)
        return result


class PhotoSizeCache(object):
    __state = {'sizes': LayerAwareSizes()}

    def __init__(self):
        self.__dict__ = self.__state
        if not len(self.sizes):
            sizes = PhotoSize.objects.all()
            for size in sizes:
                self.sizes[size.name] = size

    def reset(self):
        self.sizes = LayerAwareSizes()


photologue.models.PhotoSizeCache = PhotoSizeCache

def init_size_method_map():
    global size_method_map
    for size in PhotoSizeCache().sizes.keys():
        size_method_map['get_%s_size' % size] = {'base_name': '_get_SIZE_size', 'size': size}
        size_method_map['get_%s_photosize' % size] = {'base_name': '_get_SIZE_photosize', 'size': size}
        size_method_map['get_%s_url' % size] = {'base_name': '_get_SIZE_url', 'size': size}
        size_method_map['get_%s_filename' % size] = {'base_name': '_get_SIZE_filename', 'size': size}
        layers = reversed(settings.LAYERS['layers'])
        layer_size = re.sub('_(%s)$' % ('|').join(layers), '', size)
        size_method_map['get_%s_size' % layer_size] = {'base_name': '_get_SIZE_size', 'size': layer_size}
        size_method_map['get_%s_photosize' % layer_size] = {'base_name': '_get_SIZE_photosize', 'size': layer_size}
        size_method_map['get_%s_url' % layer_size] = {'base_name': '_get_SIZE_url', 'size': layer_size}
        size_method_map['get_%s_filename' % layer_size] = {'base_name': '_get_SIZE_filename', 'size': layer_size}


photologue.models.init_size_method_map = init_size_method_map
from django.template.loader_tags import BlockNode, BLOCK_CONTEXT_KEY
from django.core.urlresolvers import resolve, Resolver404
from django.template.loader import render_to_string

def BlockNode_render(self, context):
    block_context = context.render_context.get(BLOCK_CONTEXT_KEY)
    context.push()
    if block_context is None:
        context['block'] = self
        result = self.nodelist.render(context)
    else:
        push = block = block_context.pop(self.name)
        if block is None:
            block = self
        block = BlockNode(block.name, block.nodelist)
        block.context = context
        context['block'] = block
        result = block.nodelist.render(context)
        if push is not None:
            block_context.push(self.name, push)
    context.pop()
    if self.name == 'content' and not hasattr(context['request'], '_foundry_blocknode_marker'):
        try:
            view_name = resolve(context['request'].META['PATH_INFO']).view_name
        except Resolver404:
            return result

        setattr(context['request'], '_foundry_blocknode_marker', 1)
        from foundry.models import Page, PageView
        pages = Page.permitted.filter(id__in=[ o.page.id for o in PageView.objects.filter(view_name=view_name) ])
        for page in pages:
            rows = page.row_set.filter(has_left_or_right_column=True)
            if rows.exists():
                html = render_to_string('foundry/inclusion_tags/rows.html', {'rows': [rows[0]], 'include_center_marker': 1}, context)
                return html.replace('_FOUNDRY_BLOCKNODE_PLACEHOLDER', result)

    return result


from django.template.defaulttags import CsrfTokenNode
from django.utils.safestring import mark_safe
from django.conf import settings

def CsrfTokenNode_render(self, context):
    csrf_token = context.get('csrf_token', None)
    if csrf_token:
        if csrf_token == 'NOTPROVIDED':
            return mark_safe('')
        else:
            return mark_safe("<input type='hidden' name='csrfmiddlewaretoken' value='%s' />" % csrf_token)

    else:
        from django.conf import settings
        if settings.DEBUG:
            import warnings
            warnings.warn('A {% csrf_token %} was used in a template, but the context did not provide the value.  This is usually caused by not using RequestContext.')
        return ''
    return


CsrfTokenNode.render = CsrfTokenNode_render
from django.contrib.sites.models import Site

def Site__unicode__(self):
    return self.name


def Site_title(self):
    return self.name.split('(')[0]


Site.__unicode__ = Site__unicode__
Site.title = Site_title
from pagination.templatetags import pagination_tags

def AutoPaginateNode_decorator(func):

    def new(self, context):
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        if not paginate_by:
            self.paginate_by = 100
        return func(self, context)

    return new


pagination_tags.AutoPaginateNode.render = AutoPaginateNode_decorator(pagination_tags.AutoPaginateNode.render)