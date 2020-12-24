# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/markup.py
# Compiled at: 2007-10-25 12:41:27
from pprint import pprint
from gazest.lib.wikipage import WikiPage
from gazest.lib.wiki_util import *
from pylons import config
import gazest.lib.helpers as h
from gazest import model
import re, sha, wiki_macros, logging
log = logging.getLogger(__name__)
WIKI_LINK_PAT = re.compile('(\\[\\[.*?\\]\\])', re.UNICODE)
WIKI_LINK_INFO_PAT = re.compile('\\[\\[(.*?)(?:\\|(.*?))?\\]\\]', re.UNICODE)
PLACEHOLDER_PAT = re.compile('(\\[\\[\\[place_holder .+?\\]\\]\\])')
PLACEHOLDER_INFO_PAT = re.compile('\\[\\[\\[place_holder (.+?)\\]\\]\\]')
MACRO_PAT = re.compile('({{.+?}})')
MACRO_INFO_PAT = re.compile('{{(.+?)(?:\\s+(.+?))?}}')

def make_id(tag):
    return sha.new(tag.encode('utf-8')).hexdigest()


def expand_wiki_link(tag):
    (page, label) = WIKI_LINK_INFO_PAT.search(tag).groups()
    slug = normalize_page(page)
    url = h.url_for(controller='/wiki', action='view', slug=slug)
    classes = [
     'internal']
    if not model.Page.query.selectfirst_by(slug=slug):
        classes.append('broken')
    return '<a class="%s" href="%s">%s</a>' % ((' ').join(classes), url, label or page)


def make_placeholder(tag, stubs_h, expand_fun):
    """ Returns a placeholder macro tag for a non context specific tag
    and add it to stubs_h."""
    stub_id = make_id(tag)
    stub = '[[[place_holder %s]]]' % stub_id
    stubs_h[stub_id] = expand_fun(tag)
    return stub


def expand_placeholder(tag, stubs_h):
    stub_id = PLACEHOLDER_INFO_PAT.search(tag).group(1)
    return stubs_h[stub_id]


def expand_macro(page, tag):
    (name, args) = MACRO_INFO_PAT.search(tag).groups()
    try:
        (prefix, fname) = name.rsplit('.', 1)
        module = extra_macros[prefix]
    except ValueError:
        fname = name
        module = wiki_macros
    except KeyError:
        log.debug("No macro package called '%s'" % prefix)
        return ''

    if fname.startswith('_'):
        log.debug("Macros cannot be 'protected' functions. Requested name was: %s" % fname)
        return ''
    try:
        funct = getattr(module, fname)
    except AttributeError:
        log.debug('Invalid wiki macro: %s' % name)
        return ''

    return funct(page, args)


def replace_page_tags(body, pat, rep_fun):
    """ replace the tags in body matched by the compiled regexp pat
    what rep_fun(tag) returns."""
    frags = []
    prev_stop = 0
    for match in pat.finditer(body):
        frags.append(body[prev_stop:match.start()])
        prev_stop = match.end()
        tag = match.group()
        stub = rep_fun(tag)
        frags.append(stub)

    frags.append(body[prev_stop:])
    return ('').join(frags)


def render_page(body, slug=None):
    page = WikiPage(slug)
    if config['wiki_header']:
        body = '%s\n%s' % (config['wiki_header'], body)
    if config['wiki_footer']:
        body = '%s\n%s' % (body, config['wiki_footer'])
    stubs_h = {}

    def make_rep_fun(expand_fun):
        return lambda tag: make_placeholder(tag, stubs_h, expand_fun)

    body = replace_page_tags(body, WIKI_LINK_PAT, make_rep_fun(expand_wiki_link))
    body = replace_page_tags(body, MACRO_PAT, make_rep_fun(lambda tag: expand_macro(page, tag)))
    body = page.html_renderer(body)
    for processor in page.html_post_render_processors:
        body = processor(body)

    body = replace_page_tags(body, PLACEHOLDER_PAT, lambda tag: expand_placeholder(tag, stubs_h))
    for processor in page.html_post_expand_processors:
        body = processor(body)

    return (page, '<span class="wiki">%s</span>' % body)