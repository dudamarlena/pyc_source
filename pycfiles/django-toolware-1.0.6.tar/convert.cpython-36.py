# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/4f/p6rdjlq11nz2jwrtdlm918l40000gn/T/pip-install-o463eux1/django-toolware/toolware/utils/convert.py
# Compiled at: 2018-06-21 10:53:48
# Size of source mod 2**32: 1068 bytes
import html2text, markdown

def html_to_text(content):
    """ Converts html content to plain text """
    text = None
    h2t = html2text.HTML2Text()
    h2t.ignore_links = False
    text = h2t.handle(content)
    return text


def md_to_html(content):
    """ Converts markdown content to HTML """
    html = markdown.markdown(content)
    return html


def md_to_text(content):
    """ Converts markdown content to text """
    text = None
    html = markdown.markdown(content)
    if html:
        text = html_to_text(content)
    return text


def parts_to_uri(base_uri, uri_parts):
    """
    Converts uri parts to valid uri.
    Example: /memebers, ['profile', 'view'] => /memembers/profile/view
    """
    uri = '/'.join(map(lambda x: str(x).rstrip('/'), [base_uri] + uri_parts))
    return uri


def domain_to_fqdn(domain, proto=None):
    """ returns a fully qualified app domain name """
    from .generic import get_site_proto
    proto = proto or get_site_proto()
    fdqn = '{proto}://{domain}'.format(proto=proto, domain=domain)
    return fdqn