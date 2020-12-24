# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mark/django_avem_theme/avem_theme/functions/sanitize.py
# Compiled at: 2019-11-08 15:35:12
# Size of source mod 2**32: 2771 bytes
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.conf import settings
DEFAULT_NOSCR_ALLOWED_TAGS = 'strong:title b i em:title p:title h1:title h2:title h3:title h4:title h5:title div:title span:title ol ul li:title a:href:title:rel img:src:alt:title dl td:title dd:titletable:cellspacing:cellpadding thead tbody th tr td:title:colspan:rowspan br'

def sanitize_html(text, add_nofollow=False, allowed_tags=getattr(settings, 'NOSCR_ALLOWED_TAGS', DEFAULT_NOSCR_ALLOWED_TAGS)):
    """
                Cleans an html string:

                * remove any not-whitelisted tags
                        - remove any potentially malicious tags or attributes
                        - remove any invalid tags that may break layout
                * esca[e any <, > and & from remaining text (by bs4); this prevents
                        > >> <<script>script> alert("Haha, I hacked your page."); </</script>script>            * optionally add nofollow attributes to foreign anchors
                * removes comments
                :comment * optionally replace some tags with others:

                :arg text: Input html.
                :arg allowed_tags: Argument should be in form 'tag2:attr1:attr2 tag2:attr1 tag3', where tags are allowed HTML
                        tags, and attrs are the allowed attributes for that tag.
                :return: Sanitized html.

                This is based on https://djangosnippets.org/snippets/1655/
        """
    try:
        from bs4 import BeautifulSoup, Comment, NavigableString
    except ImportError:
        raise ImportError('to use sanitize_html() and |noscr, you need to install beautifulsoup4')

    is_relative = lambda url: not bool(urlparse(url).netloc)
    allowed_tags = [tag.split(':') for tag in allowed_tags.split()]
    allowed_tags = {tag[0]:tag[1:] for tag in allowed_tags}
    soup = BeautifulSoup(text)
    for comment in soup.findAll(text=(lambda text: isinstance(text, Comment))):
        comment.extract()

    for tag in soup.find_all(recursive=True):
        if tag.name not in allowed_tags:
            tag.hidden = True
        else:
            tag.attrs = {attr:val for attr, val in tag.attrs.items() if attr in allowed_tags[tag.name]}
        if add_nofollow and tag.name == 'a' and 'href' in tag.attrs:
            tag.attrs['rel'] = is_relative(tag.attrs['href']) or (tag.attrs['rel'] if 'rel' in tag.attrs else []) + ['nofollow']

    return soup.renderContents().decode('utf8')