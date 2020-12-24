# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/banner/templatetags/banner_inclusion_tags.py
# Compiled at: 2010-12-14 07:44:09
from django import template
from django.conf import settings
from django.core.urlresolvers import RegexURLResolver, Resolver404
from django.template import RequestContext
from django.utils.encoding import smart_str
from preferences import preferences
register = template.Library()

def resolve_pattern_name(resolver, path):
    tried = []
    match = resolver.regex.search(path)
    if match:
        new_path = path[match.end():]
        for pattern in resolver.url_patterns:
            try:
                sub_match = pattern.resolve(new_path)
            except Resolver404, e:
                sub_tried = e.args[0].get('tried')
                if sub_tried is not None:
                    tried.extend([ pattern.regex.pattern + '   ' + t for t in sub_tried ])
                else:
                    tried.append(pattern.regex.pattern)
            else:
                if sub_match:
                    sub_match_dict = dict([ (smart_str(k), v) for (k, v) in match.groupdict().items() ])
                    sub_match_dict.update(resolver.default_kwargs)
                    for (k, v) in sub_match[2].iteritems():
                        sub_match_dict[smart_str(k)] = v

                    try:
                        return pattern.name
                    except AttributeError:
                        return resolve_pattern_name(pattern, new_path)

                tried.append(pattern.regex.pattern)

        raise Resolver404, {'tried': tried, 'path': new_path}
    raise Resolver404, {'path': path}
    return


def resolve_banner(request, position):
    resolved_banner = None
    queryset = preferences.BannerPreferences.banneroption_set
    urlconf = getattr(request, 'urlconf', settings.ROOT_URLCONF)
    resolver = RegexURLResolver('^/', urlconf)
    url_name = resolve_pattern_name(resolver, request.path)
    queryset = queryset.filter(url_name__exact=url_name)
    queryset = queryset.filter(position__exact=position)
    if queryset:
        banner = queryset[0].banner
    path_filtered_queryset = queryset.filter(url=request.path)
    if path_filtered_queryset:
        for banner in path_filtered_queryset:
            bnr = banner.banner
            if bnr.is_permitted:
                reolved_banner = bnr
                break

    elif queryset:
        for banner in queryset:
            bnr = banner.banner
            if bnr.is_permitted:
                resolved_banner = bnr
                break

    if not resolved_banner:
        queryset = preferences.BannerPreferences.banneroption_set.filter(position__exact=position, is_default=True)
        for banner in queryset:
            bnr = banner.banner
            if bnr.is_permitted:
                resolved_banner = bnr
                break

    return resolved_banner.as_leaf_class() if resolved_banner else None


@register.inclusion_tag('banner/inclusion_tags/banner_wide_gizmo.html', takes_context=True)
def banner_wide_gizmo(context):
    context = RequestContext(context['request'], {'object': resolve_banner(context['request'], position=context['gizmo_slot_name'])})
    return context


@register.inclusion_tag('banner/inclusion_tags/banner_block_gizmo.html', takes_context=True)
def banner_block_gizmo(context):
    context = RequestContext(context['request'], {'object': resolve_banner(context['request'], position=context['gizmo_slot_name'])})
    return context