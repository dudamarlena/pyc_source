# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/api/net/scraper.py
# Compiled at: 2014-02-03 15:48:20
"""
URL scraping API.

This module contains utility functions to extract (scrape) URLs from data.
Currently only HTML and plain text data are supported.
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = [
 'extract',
 'extract_from_text',
 'extract_from_html',
 'is_link']
from .web_utils import parse_url, urldefrag, urljoin
from BeautifulSoup import BeautifulSoup
from warnings import warn
import re
from codecs import decode
from chardet import detect
_re_url_readable = re.compile('(?i)\\b((?:[a-z][\\w-]+:(?:/{1,3}|[a-z0-9%])|www\\d{0,3}[.]|[a-z0-9.\\-]+[.][a-z]{2,4}/)(?:[^\\s()<>]+|\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\))+(?:\\(([^\\s()<>]+|(\\([^\\s()<>]+\\)))*\\)|[^\\s`!()\\[\\]{};:\'".,<>?«»“”‘’]))', re.I)
_re_url_rfc = re.compile('\\\\<([^\\\\>]+\\\\:\\\\/\\\\/[^\\\\>]+)\\\\>', re.I)

def is_link(url, base_url):
    """
    Determines if an URL is a link to another resource.

    :param url: URL to test.
    :type url: str

    :param base_url: Base URL for the current document.
        Must not contain a fragment.
    :type base_url: str

    :returns: True if the URL points to another page or resource,
        False otherwise.
    :rtype: bool
    """
    try:
        parsed = parse_url(url, base_url)
        parsed.fragment = ''
        if parsed.url == base_url:
            return False
        return True
    except Exception:
        return False


def extract_from_text(text, base_url=None, only_links=True):
    """
    Extract URLs from text.

    Implementation notes:

    - Unicode URLs are currently not supported.

    :param text: Text.
    :type text: str

    :param base_url: Base URL for the current document.
        If not specified, relative URLs are ignored.
    :type base_url: str

    :param only_links: If True, only extract links to other resources.
        If False, extract all URLs.
    :type only_links: bool

    :returns: Extracted URLs.
    :rtype: set(str)
    """
    if not text:
        return set()
    if not isinstance(text, basestring):
        raise TypeError('Expected string, got %r instead' % type(text))
    result = set()
    add_result = result.add
    if base_url:
        base_url = urldefrag(base_url)[0]
    for regex in (_re_url_rfc, _re_url_readable):
        for url in regex.findall(text):
            url = url[0]
            try:
                url = str(url)
            except Exception:
                warn('Unicode URLs not yet supported: %r' % url)
                continue

            if base_url:
                try:
                    url = urljoin(base_url, url.strip())
                except Exception:
                    continue

                if only_links and not is_link(url, base_url=base_url):
                    continue
            else:
                try:
                    parsed = parse_url(url)
                    if not parsed.scheme or not parsed.netloc:
                        continue
                except Exception:
                    continue

            add_result(url)

    return result


def extract_forms_from_html(raw_html, base_url):
    """
    Extract forms info from HTML.

    :param raw_html: Raw HTML data.
    :type raw_html: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :returns: Extracted form info.
    :rtype: list((URL, METHOD, list({ "name" : PARAM_NAME, "value" : PARAM_VALUE, "type" : PARAM_TYPE})))
    """
    result = list()
    result_append = result.append
    base_url = urldefrag(base_url)[0]
    bs = BeautifulSoup(decode(raw_html, detect(raw_html)['encoding']))
    for form in bs.findAll('form'):
        target = form.get('action', None)
        method = form.get('method', 'POST').upper()
        if not target:
            continue
        try:
            target = str(target)
        except Exception:
            warn('Unicode URLs not yet supported: %r' % target)
            continue

        try:
            target = urljoin(base_url, target.strip())
        except Exception:
            continue

        form_params = []
        form_params_append = form_params.append
        for params in form.findAll('input'):
            if params.get('type') == 'submit':
                continue
            form_params_append({'name': params.get('name', 'NAME'), 
               'value': params.get('value', 'VALUE'), 
               'type': params.get('type', 'TYPE')})

        result_append((target, method, form_params))

    return result


def extract_from_html(raw_html, base_url, only_links=True):
    """
    Extract URLs from HTML.

    Implementation notes:

    - The current implementation is fault tolerant, meaning it will try
      to extract URLs even if the HTML is malformed and browsers wouldn't
      normally see those links. This may therefore result in some false
      positives.

    - HTML5 tags are supported, including tags not currently supported by
      any major browser.

    :param raw_html: Raw HTML data.
    :type raw_html: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :param only_links: If True, only extract links to other resources.
        If False, extract all URLs.
    :type only_links: bool

    :returns: Extracted URLs.
    :rtype: set(str)
    """
    result = set()
    add_result = result.add
    base_url = urldefrag(base_url)[0]
    bs = BeautifulSoup(decode(raw_html, detect(raw_html)['encoding']), convertEntities=BeautifulSoup.ALL_ENTITIES)
    href_tags = {
     'a', 'link', 'area'}
    src_tags = {'script', 'img', 'iframe', 'frame', 'embed', 'source', 'track'}
    param_names = {'movie', 'href', 'link', 'src', 'url', 'uri'}
    for tag in bs.findAll():
        name = tag.name.lower()
        url = None
        if name in href_tags:
            url = tag.get('href', None)
        elif name in src_tags:
            url = tag.get('src', None)
        elif name == 'param':
            name = tag.get('name', '').lower().strip()
            if name in param_names:
                url = tag.get('value', None)
        elif name == 'object':
            url = tag.get('data', None)
        elif name == 'applet':
            url = tag.get('code', None)
        elif name == 'meta':
            name = tag.get('name', '').lower().strip()
            if name == 'http-equiv':
                content = tag.get('content', '')
                p = content.find(';')
                if p >= 0:
                    url = content[p + 1:]
        elif name == 'base':
            url = tag.get('href', None)
            if url is not None:
                try:
                    url = str(url)
                except Exception:
                    warn('Unicode URLs not yet supported: %r' % url)
                    continue

                try:
                    base_url = urljoin(base_url, url.strip(), allow_fragments=False)
                except Exception:
                    continue

        if url is not None:
            try:
                url = str(url)
            except Exception:
                warn('Unicode URLs not yet supported: %r' % url)
                continue

            try:
                url = urljoin(base_url, url.strip())
            except Exception:
                continue

            if not only_links or is_link(url, base_url=base_url):
                add_result(url)

    return result


def extract(raw_data, content_type, base_url, only_links=True):
    """
    Extract URLs from raw data.

    Implementation notes:

    - Unicode URLs are currently not supported.

    - The current implementation is fault tolerant, meaning it will try
      to extract URLs even if the HTML is malformed and browsers wouldn't
      normally see those links. This may therefore result in some false
      positives.

    - HTML5 tags are supported, including tags not currently supported by
      any major browser.

    :param raw_data: Raw data.
    :type raw_data: str

    :param content_type: MIME content type.
    :type content_type: str

    :param base_url: Base URL for the current document.
    :type base_url: str

    :param only_links: If True, only extract links to other resources.
        If False, extract all URLs.
    :type only_links: bool

    :returns: Extracted URLs.
    :rtype: set(str)
    """
    content_type = content_type.strip().lower()
    if ';' in content_type:
        content_type = content_type[content_type.find(';'):].strip()
    if content_type == 'text/html':
        urls = extract_from_html(raw_data, base_url, only_links)
        urls.update(extract_from_text(raw_data, base_url, only_links))
        return urls
    if content_type.startswith('text/'):
        return extract_from_text(raw_data, base_url, only_links)
    return set()