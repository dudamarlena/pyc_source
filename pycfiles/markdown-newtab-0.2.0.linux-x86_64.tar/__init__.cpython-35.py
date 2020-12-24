# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/markdown_newtab/__init__.py
# Compiled at: 2015-12-02 14:49:36
# Size of source mod 2**32: 2267 bytes
"""
New Tab Extension for Python-Markdown
=====================================

Modify the behavior of Links in Python-Markdown to open a in a new window. This
changes the HTML output to add target="_blank" to all generated links, except
ones which point to anchors on the existing page.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from markdown import Extension
from markdown.inlinepatterns import LinkPattern, ReferencePattern, AutolinkPattern, AutomailPattern, LINK_RE, REFERENCE_RE, SHORT_REF_RE, AUTOLINK_RE, AUTOMAIL_RE

class NewTabMixin(object):
    __doc__ = 'Common extension logic; mixed into the existing classes.'

    def handleMatch(self, match):
        """Handles a match on a pattern; used by existing implementation."""
        elem = super(NewTabMixin, self).handleMatch(match)
        if elem is not None and not elem.get('href').startswith('#'):
            elem.set('target', '_blank')
        return elem


class NewTabLinkPattern(NewTabMixin, LinkPattern):
    __doc__ = 'Links to URLs, e.g. [link](https://duck.co).'


class NewTabReferencePattern(NewTabMixin, ReferencePattern):
    __doc__ = 'Links to references, e.g. [link][1].'


class NewTabAutolinkPattern(NewTabMixin, AutolinkPattern):
    __doc__ = 'Autommatic links, e.g. <duck.co>.'


class NewTabAutomailPattern(NewTabMixin, AutomailPattern):
    __doc__ = 'Autommatic links, e.g. <address@example.com>.'


class NewTabExtension(Extension):
    __doc__ = 'Modifies HTML output to open links in a new tab.'

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = NewTabLinkPattern(LINK_RE, md)
        md.inlinePatterns['reference'] = NewTabReferencePattern(REFERENCE_RE, md)
        md.inlinePatterns['short_reference'] = NewTabReferencePattern(SHORT_REF_RE, md)
        md.inlinePatterns['autolink'] = NewTabAutolinkPattern(AUTOLINK_RE, md)
        md.inlinePatterns['automail'] = NewTabAutomailPattern(AUTOMAIL_RE, md)


def makeExtension(configs=None):
    """Loads the extension."""
    if configs is None:
        configs = {}
    return NewTabExtension(configs=configs)