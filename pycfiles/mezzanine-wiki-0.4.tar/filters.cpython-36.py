# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\landon\dropbox\documents\pycharmprojects\mezzanine-wiki\mezzanine_wiki\filters.py
# Compiled at: 2018-01-31 08:31:33
# Size of source mod 2**32: 589 bytes
from django.core.urlresolvers import reverse
from markdown import markdown
from mezzanine_wiki.mdx_wikilinks_extra import WikiLinkExtraExtension

def md_plain(content):
    """
    Renders content using markdown.
    """
    return markdown(content)


def md_wikilinks(content):
    """
    Renders content using markdown with wikilinks.
    Format: [[link|optional label]]
    """
    base_url = reverse('wiki_index')
    configs = {'base_url': base_url}
    wikilinks_extra = WikiLinkExtraExtension(configs=configs)
    return markdown(content, [wikilinks_extra])