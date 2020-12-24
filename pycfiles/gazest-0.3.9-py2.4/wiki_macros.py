# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/wiki_macros.py
# Compiled at: 2007-10-16 06:04:23
import gazest.lib.helpers as h
from gazest.lib import wiki_util
import re

def duplicate(page, text):
    return '%s %s' % (text, text)


def edit_self(page, label):
    """ Return a link to edit the current page. """
    url = h.url_for(controller='/wiki', action='edit_form', slug=wiki_util.normalize_slug(page.slug))
    return '<a href="%s">%s</a>' % (url, label or 'edit')


def title(page, title):
    """ Override the title infered from the slug. """
    page.title = title
    return ''


def rel_nofollow(page, arg):
    """ Mark all external links with ``rel="nofollow"`` """
    A_PAT = re.compile('(<a\\s.*?>)', re.UNICODE | re.DOTALL)

    def rep(match):
        tag = match.group(0)
        if tag.find('nofollow') != -1:
            return tag
        else:
            return tag[:-1] + ' rel="nofollow">'

    def fix_tags(body):
        return re.sub(A_PAT, rep, body)

    page.html_post_render_processors.append(fix_tags)
    return ''