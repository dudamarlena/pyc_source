# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/jmbo-foundry/foundry/templatetags/foundry_tags.py
# Compiled at: 2015-09-03 08:53:47
import types, hashlib, cPickle, re
from BeautifulSoup import BeautifulSoup
from django import template
from django.core.cache import cache
from django.core.urlresolvers import reverse, resolve, NoReverseMatch, get_script_prefix
from django.template.loader import render_to_string
from django.http import HttpResponse, Http404
from django.template.response import TemplateResponse
from django.core.paginator import Paginator, InvalidPage
from django.contrib.sites.models import get_current_site
from django.conf import settings
from pagination.templatetags.pagination_tags import DEFAULT_PAGINATION, DEFAULT_ORPHANS, INVALID_PAGE_RAISES_404
from foundry.models import Menu, Navbar, Listing, Page, Member
from foundry.templatetags.listing_styles import LISTING_MAP
register = template.Library()

@register.filter(name='as_list')
def as_list(value, coerce=None):
    li = value.split()
    if coerce == 'int':
        li = [ int(l) for l in li ]
    return li


@register.filter(name='join_titles')
def join_titles(value, delimiter=', '):
    return delimiter.join([ v.title for v in value ])


@register.tag
def menu(parser, token):
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('menu tag requires argument slug')

    return MenuNode(slug)


class MenuNode(template.Node):

    def __init__(self, slug):
        self.slug = template.Variable(slug)

    def render(self, context, as_tile=False):
        slug = self.slug.resolve(context)
        try:
            obj = Menu.permitted.get(slug=slug)
        except Menu.DoesNotExist:
            return ''

        object_list = []
        for o in obj.menulinkposition_set.select_related().all().order_by('position'):
            if o.condition_expression_result(context['request']):
                o.link.name = o.name
                o.link.class_name = o.class_name
                object_list.append(o.link)

        extra = {'object': obj, 'object_list': object_list}
        return render_to_string('foundry/inclusion_tags/menu.html', extra, context)


@register.tag
def navbar(parser, token):
    try:
        tag_name, slug = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('navbar tag requires argument slug')

    return NavbarNode(slug)


class NavbarNode(template.Node):

    def __init__(self, slug):
        self.slug = template.Variable(slug)

    def render(self, context, as_tile=False):
        slug = self.slug.resolve(context)
        try:
            obj = Navbar.permitted.get(slug=slug)
        except Navbar.DoesNotExist:
            return ''

        extra = {'object': obj}
        object_list = []
        active_link = None
        for o in obj.navbarlinkposition_set.select_related().all().order_by('position'):
            if o.condition_expression_result(context['request']):
                o.link.name = o.name
                o.link.class_name = o.class_name
                object_list.append(o.link)
                if not active_link and o.link.is_active(context['request']):
                    active_link = o.link

        extra['object_list'] = object_list
        extra['active_link'] = active_link
        return render_to_string('foundry/inclusion_tags/navbar.html', extra, context)


@register.tag
def listing(parser, token):
    tokens = token.split_contents()
    length = len(tokens)
    if length < 2:
        raise template.TemplateSyntaxError('listing tag require at least argument slug or queryset')
    slug_or_queryset = tokens[1]
    kwargs = {}
    for token in tokens[2:]:
        k, v = token.split('=')
        kwargs[k] = v

    return ListingNode(slug_or_queryset, **kwargs)


class ListingNode(template.Node):

    def __init__(self, slug_or_queryset, **kwargs):
        self.slug_or_queryset = template.Variable(slug_or_queryset)
        self.kwargs = kwargs

    def render(self, context, as_tile=False):
        slug_or_queryset = self.slug_or_queryset.resolve(context)
        if isinstance(slug_or_queryset, types.UnicodeType):
            try:
                obj = Listing.permitted.get(slug=slug_or_queryset)
            except Listing.DoesNotExist:
                return ''

        else:

            class ListingProxy:
                """Helper class emulating Listing API so AbstractBaseStyle
                works. Essentially a record class."""

                def __init__(self, queryset, **kwargs):
                    self.queryset = lambda x: queryset
                    self.items_per_page = 0
                    for k, v in kwargs.items():
                        setattr(self, k, v)

                    if not hasattr(self, 'id'):
                        setattr(self, 'id', None)
                    return

            di = {}
            for k, v in self.kwargs.items():
                di[k] = template.Variable(v).resolve(context)

            obj = ListingProxy(slug_or_queryset, **di)
        return LISTING_MAP[obj.style](obj).render(context, as_tile=as_tile)


@register.tag
def rows(parser, token):
    try:
        tag_name, block_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('rows tag requires argument block_name')

    return RowsNode(block_name)


class RowsNode(template.Node):

    def __init__(self, block_name):
        self.block_name = template.Variable(block_name)

    def render(self, context):
        request = context['request']
        if hasattr(request, '_foundry_suppress_rows_tag'):
            return
        else:
            block_name = self.block_name.resolve(context)
            empty_marker = None
            key = 'foundry-rbbn-%s' % settings.SITE_ID
            cached = cache.get(key, empty_marker)
            if cached is None:
                pages = Page.permitted.filter(is_homepage=True)
                if pages:
                    rows_by_block_name = pages[0].rows_by_block_name
                else:
                    rows_by_block_name = []
                cache.set(key, cPickle.dumps(rows_by_block_name), settings.FOUNDRY.get('layout_cache_time', 60))
            else:
                rows_by_block_name = cPickle.loads(cached)
            if rows_by_block_name:
                rows = rows_by_block_name.get(block_name, [])
                if rows:
                    return render_to_string('foundry/inclusion_tags/rows.html', {'rows': rows}, context)
            return render_to_string('foundry/inclusion_tags/%s.html' % block_name, {}, context)


@register.tag
def tile(parser, token):
    try:
        tag_name, tile = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tile tag requires argument tile')

    return TileNode(tile)


class TileNode(template.Node):

    def __init__(self, tile):
        self.tile = template.Variable(tile)

    def render(self, context):
        tile = self.tile.resolve(context)
        request = context['request']
        if not tile.condition_expression_result(request):
            return ''
        if tile.view_name:
            try:
                url = reverse(tile.view_name)
            except NoReverseMatch:
                return 'No reverse match for %s' % tile.view_name

            view, args, kwargs = resolve(url)
            setattr(request, '_foundry_suppress_rows_tag', 1)
            setattr(request, 'render_only_content_block', True)
            html = ''
            result = view(request, *args, **kwargs)
            if isinstance(result, TemplateResponse):
                result.render()
                html = result.rendered_content
            else:
                if isinstance(result, HttpResponse):
                    html = result.content
                if hasattr(request, '_foundry_suppress_rows_tag'):
                    delattr(request, '_foundry_suppress_rows_tag')
                if hasattr(request, 'render_only_content_block'):
                    delattr(request, 'render_only_content_block')
                soup = BeautifulSoup(html)
                content = soup.find('div', id='content')
                if content:
                    return content.renderContents()
            return html
        if tile.target:
            node = globals().get('%sNode' % tile.target.__class__.__name__)
            try:
                return node('"' + tile.target.slug + '"').render(context, as_tile=True)
            except:
                if settings.DEBUG:
                    raise
                return 'A render error has occurred'


@register.tag
def tile_url(parser, token):
    """Return the Url for a given view. Very similar to the {% url %} template tag,
    but can accept a variable as first parameter."""
    try:
        tag_name, tile = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('tile_url tag requires argument tile')

    return TileUrlNode(tile)


class TileUrlNode(template.Node):

    def __init__(self, tile):
        self.tile = template.Variable(tile)

    def render(self, context):
        tile = self.tile.resolve(context)
        if tile.view_name:
            try:
                return reverse(tile.view_name)
            except NoReverseMatch:
                return ''

        if tile.target:
            url = reverse('listing-detail', args=[tile.target.slug])
            return url


@register.tag
def get_listing_queryset(parser, token):
    """{% get_listing_queryset [slug] as [varname] %}"""
    try:
        tag_name, slug, dc, as_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_listing_queryset tag has syntax {% get_listing_items [slug] as [varname] %}')

    return ListingQuerysetNode(slug, as_var)


class ListingQuerysetNode(template.Node):

    def __init__(self, slug, as_var):
        self.slug = template.Variable(slug)
        self.as_var = template.Variable(as_var)

    def render(self, context):
        slug = self.slug.resolve(context)
        as_var = self.as_var.resolve(context)
        try:
            obj = Listing.permitted.get(slug=slug)
            context[as_var] = obj.queryset(context['request'])
        except Listing.DoesNotExist:
            obj = None
            context[as_var] = None

        return ''


def do_autopaginate(parser, token):
    """
    Splits the arguments to the autopaginate tag and formats them correctly.
    """
    split = token.split_contents()
    as_index = None
    context_var = None
    for i, bit in enumerate(split):
        if bit == 'as':
            as_index = i
            break

    if as_index is not None:
        try:
            context_var = split[(as_index + 1)]
        except IndexError:
            raise template.TemplateSyntaxError('Context variable assignment ' + 'must take the form of {%% %r object.example_set.all ... as ' + 'context_var_name %%}' % split[0])

        del split[as_index:as_index + 2]
    if len(split) == 2:
        return AutoPaginateNode(split[1])
    else:
        if len(split) == 3:
            return AutoPaginateNode(split[1], paginate_by=split[2], context_var=context_var)
        if len(split) == 4:
            return AutoPaginateNode(split[1], paginate_by=split[2], page_number=split[3], context_var=context_var)
        if len(split) == 5:
            try:
                orphans = int(split[4])
            except ValueError:
                raise template.TemplateSyntaxError('Got %s, but expected integer.' % split[4])

            return AutoPaginateNode(split[1], paginate_by=split[2], page_number=split[3], orphans=orphans, context_var=context_var)
        raise template.TemplateSyntaxError('%r tag takes one required ' + 'argument and one optional argument' % split[0])
        return


class AutoPaginateNode(template.Node):

    def __init__(self, queryset_var, paginate_by=DEFAULT_PAGINATION, page_number=0, orphans=DEFAULT_ORPHANS, context_var=None):
        self.queryset_var = template.Variable(queryset_var)
        if isinstance(paginate_by, int):
            self.paginate_by = paginate_by
        else:
            self.paginate_by = template.Variable(paginate_by)
        if isinstance(page_number, int):
            self.page_number = page_number
        else:
            self.page_number = template.Variable(page_number)
        self.orphans = orphans
        self.context_var = context_var

    def render(self, context):
        key = self.queryset_var.var
        value = self.queryset_var.resolve(context)
        if isinstance(self.paginate_by, int):
            paginate_by = self.paginate_by
        else:
            paginate_by = self.paginate_by.resolve(context)
        if isinstance(self.page_number, int):
            page_number = self.page_number
        else:
            page_number = self.page_number.resolve(context)
        paginator = Paginator(value, paginate_by, self.orphans)
        p = context['request'].page
        if 'page' not in context['request'].GET:
            if page_number == -1:
                p = paginator.num_pages
        try:
            page_obj = paginator.page(p)
        except InvalidPage:
            if INVALID_PAGE_RAISES_404:
                raise Http404('Invalid page requested.  If DEBUG were set to ' + 'False, an HTTP 404 page would have been shown instead.')
            context[key] = []
            context['invalid_page'] = True
            return ''

        if self.context_var is not None:
            context[self.context_var] = page_obj.object_list
        else:
            context[key] = page_obj.object_list
        context['paginator'] = paginator
        context['page_obj'] = page_obj
        return ''


register.tag('autopaginate', do_autopaginate)

@register.tag('foundrycache')
def do_foundrycache(parser, token):
    nodelist = parser.parse(('endfoundrycache', ))
    parser.delete_first_token()
    tokens = token.contents.split()
    if len(tokens) < 2:
        raise template.TemplateSyntaxError('foundry_cache tag requires an argument that is an instance of a subclass of CachingMixin')
    return FoundryCacheNode(nodelist, tokens[1])


class FoundryCacheNode(template.Node):

    def __init__(self, nodelist, obj):
        self.nodelist = nodelist
        self.obj = template.Variable(obj)

    def render(self, context):
        """Based on Django's default cache template tag"""
        obj = self.obj.resolve(context)
        if obj.enable_caching:
            request = context['request']
            user = getattr(request, 'user', None)
            k = ''
            if obj.cache_type == 'anonymous_only':
                if getattr(user, 'is_authenticated', lambda : False)():
                    return self.nodelist.render(context)
                k = 'anon'
            elif obj.cache_type == 'anonymous_and_authenticated':
                k = getattr(user, 'is_anonymous', lambda : True)() and 'anon' or 'auth'
            elif obj.cache_type == 'per_user':
                k = getattr(user, 'username', 'anon')
            vary_on = [obj.id, k, get_current_site(request).id, request.META.get('QUERY_STRING', '')]
            args = hashlib.md5((':').join([ str(v) for v in vary_on if v ]))
            cache_key = 'template.foundrycache.%s.%s' % (getattr(obj, 'klass', obj.__class__).__name__, args.hexdigest())
            value = cache.get(cache_key)
            if value is None:
                value = self.nodelist.render(context)
                cache.set(cache_key, value, obj.cache_timeout)
            return value
        return self.nodelist.render(context)


@register.tag
def get_can_report_comment(parser, token):
    """{% get_can_report_comment [comment] as [varname] %}"""
    try:
        tag_name, comment, dc, as_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('get_can_report_comment tag has syntax {% get_can_report_comment [comment] as [varname] %}')

    return CanReportCommentNode(comment, as_var)


class CanReportCommentNode(template.Node):

    def __init__(self, comment, as_var):
        self.comment = template.Variable(comment)
        self.as_var = template.Variable(as_var)

    def render(self, context):
        comment = self.comment.resolve(context)
        as_var = self.as_var.resolve(context)
        request = context['request']
        user = getattr(request, 'user', None)
        result = False
        if getattr(user, 'is_authenticated', lambda : False)():
            key = 'comment_report_%s' % comment.id
            result = key not in request.COOKIES
        context[as_var] = result
        return ''


@register.tag
def render_view(parser, token):
    """{% render_view view_name %}"""
    tokens = token.split_contents()
    if len(tokens) != 2:
        raise template.TemplateSyntaxError('render_view view_name %}')
    return RenderViewNode(tokens[1])


class RenderViewNode(template.Node):

    def __init__(self, view_name):
        self.view_name = template.Variable(view_name)

    def render(self, context):
        view_name = self.view_name.resolve(context)
        url = reverse(view_name)
        url = re.sub('^%s' % get_script_prefix().rstrip('/'), '', url)
        view, args, kwargs = resolve(url)
        request = context['request']
        old = getattr(request, 'render_only_content_block', False)
        setattr(request, 'render_only_content_block', True)
        result = view(request, *args, **kwargs)
        setattr(request, 'render_only_content_block', old)
        if isinstance(result, TemplateResponse):
            result.render()
            html = result.rendered_content
        elif isinstance(result, HttpResponse):
            html = result.content
        return html