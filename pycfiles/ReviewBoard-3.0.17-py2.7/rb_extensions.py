# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/extensions/templatetags/rb_extensions.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import logging
from django import template
from django.template.loader import render_to_string
from reviewboard.extensions.hooks import CommentDetailDisplayHook, HeaderActionHook, HeaderDropdownActionHook, NavigationBarHook
from reviewboard.site.urlresolvers import local_site_reverse
register = template.Library()

def action_hooks(context, hook_cls, action_key=b'action', template_name=b'extensions/action.html'):
    """Displays all registered action hooks from the specified ActionHook."""
    html = []
    for hook in hook_cls.hooks:
        try:
            for actions in hook.get_actions(context):
                if actions:
                    context.push()
                    context[action_key] = actions
                    try:
                        html.append(render_to_string(template_name, context))
                    except Exception as e:
                        logging.error(b'Error when rendering template for action "%s" for hook %r in extension "%s": %s', action_key, hook, hook.extension.id, e, exc_info=1)

                    context.pop()

        except Exception as e:
            logging.error(b'Error when running get_actions() on hook %r in extension "%s": %s', hook, hook.extension.id, e, exc_info=1)

    return (b'').join(html)


@register.simple_tag(takes_context=True)
def navigation_bar_hooks(context):
    """Displays all registered navigation bar entries."""
    html = []
    for hook in NavigationBarHook.hooks:
        try:
            for nav_info in hook.get_entries(context):
                if nav_info:
                    url_name = nav_info.get(b'url_name', None)
                    if url_name:
                        nav_info[b'url'] = local_site_reverse(url_name, request=context.get(b'request'))
                    context.push()
                    context[b'entry'] = nav_info
                    html.append(render_to_string(b'extensions/navbar_entry.html', context))
                    context.pop()

        except Exception as e:
            extension = hook.extension
            logging.error(b'Error when running NavigationBarHook.get_entries function in extension: "%s": %s', extension.id, e, exc_info=1)

    return (b'').join(html)


@register.simple_tag(takes_context=True)
def header_action_hooks(context):
    """Displays all single-entry action hooks for the header bar."""
    return action_hooks(context, HeaderActionHook)


@register.simple_tag(takes_context=True)
def header_dropdown_action_hooks(context):
    """Displays all multi-entry action hooks for the header bar."""
    return action_hooks(context, HeaderDropdownActionHook, b'actions', b'extensions/header_action_dropdown.html')


@register.simple_tag(takes_context=True)
def comment_detail_display_hook(context, comment, render_mode):
    """Displays all additional detail from CommentDetailDisplayHooks."""
    assert render_mode in ('review', 'text-email', 'html-email')
    html = []
    for hook in CommentDetailDisplayHook.hooks:
        try:
            if render_mode == b'review':
                html.append(hook.render_review_comment_detail(comment))
            elif render_mode in ('text-email', 'html-email'):
                html.append(hook.render_email_comment_detail(comment, render_mode == b'html-email'))
        except Exception as e:
            extension = hook.extension
            logging.error(b'Error when running CommentDetailDisplayHook with render mode "%s" in extension: %s: %s', render_mode, extension.id, e, exc_info=1)

    return (b'').join(html)