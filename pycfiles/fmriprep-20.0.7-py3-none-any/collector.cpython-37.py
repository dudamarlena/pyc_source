# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/index/collector.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 21547 bytes
"""
The main purpose of this module is to expose LinkCollector.collect_links().
"""
import cgi, functools, itertools, logging, mimetypes, os, re
from collections import OrderedDict
from pip._vendor import html5lib, requests
from pip._vendor.distlib.compat import unescape
from pip._vendor.requests.exceptions import HTTPError, RetryError, SSLError
import pip._vendor.six.moves.urllib as urllib_parse
import pip._vendor.six.moves.urllib as urllib_request
from pip._internal.models.link import Link
from pip._internal.utils.filetypes import ARCHIVE_EXTENSIONS
from pip._internal.utils.misc import pairwise, redact_auth_from_url
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.urls import path_to_url, url_to_path
from pip._internal.vcs import is_url, vcs
if MYPY_CHECK_RUNNING:
    from typing import Callable, Iterable, List, MutableMapping, Optional, Protocol, Sequence, Tuple, TypeVar, Union
    import xml.etree.ElementTree
    from pip._vendor.requests import Response
    from pip._internal.models.search_scope import SearchScope
    from pip._internal.network.session import PipSession
    HTMLElement = xml.etree.ElementTree.Element
    ResponseHeaders = MutableMapping[(str, str)]
    F = TypeVar('F')

    class LruCache(Protocol):

        def __call__(self, maxsize=None):
            raise NotImplementedError


logger = logging.getLogger(__name__)

def noop_lru_cache(maxsize=None):

    def _wrapper(f):
        return f

    return _wrapper


_lru_cache = getattr(functools, 'lru_cache', noop_lru_cache)

def _match_vcs_scheme(url):
    """Look for VCS schemes in the URL.

    Returns the matched VCS scheme, or None if there's no match.
    """
    for scheme in vcs.schemes:
        if url.lower().startswith(scheme) and url[len(scheme)] in '+:':
            return scheme


def _is_url_like_archive(url):
    """Return whether the URL looks like an archive.
    """
    filename = Link(url).filename
    for bad_ext in ARCHIVE_EXTENSIONS:
        if filename.endswith(bad_ext):
            return True

    return False


class _NotHTML(Exception):

    def __init__(self, content_type, request_desc):
        super(_NotHTML, self).__init__(content_type, request_desc)
        self.content_type = content_type
        self.request_desc = request_desc


def _ensure_html_header(response):
    """Check the Content-Type header to ensure the response contains HTML.

    Raises `_NotHTML` if the content type is not text/html.
    """
    content_type = response.headers.get('Content-Type', '')
    if not content_type.lower().startswith('text/html'):
        raise _NotHTML(content_type, response.request.method)


class _NotHTTP(Exception):
    pass


def _ensure_html_response(url, session):
    """Send a HEAD request to the URL, and ensure the response contains HTML.

    Raises `_NotHTTP` if the URL is not available for a HEAD request, or
    `_NotHTML` if the content type is not text/html.
    """
    scheme, netloc, path, query, fragment = urllib_parse.urlsplit(url)
    if scheme not in {'https', 'http'}:
        raise _NotHTTP()
    resp = session.head(url, allow_redirects=True)
    resp.raise_for_status()
    _ensure_html_header(resp)


def _get_html_response(url, session):
    """Access an HTML page with GET, and return the response.

    This consists of three parts:

    1. If the URL looks suspiciously like an archive, send a HEAD first to
       check the Content-Type is HTML, to avoid downloading a large file.
       Raise `_NotHTTP` if the content type cannot be determined, or
       `_NotHTML` if it is not HTML.
    2. Actually perform the request. Raise HTTP exceptions on network failures.
    3. Check the Content-Type header to make sure we got HTML, and raise
       `_NotHTML` otherwise.
    """
    if _is_url_like_archive(url):
        _ensure_html_response(url, session=session)
    logger.debug('Getting page %s', redact_auth_from_url(url))
    resp = session.get(url,
      headers={'Accept':'text/html', 
     'Cache-Control':'max-age=0'})
    resp.raise_for_status()
    _ensure_html_header(resp)
    return resp


def _get_encoding_from_headers(headers):
    """Determine if we have any encoding information in our headers.
    """
    if headers:
        if 'Content-Type' in headers:
            content_type, params = cgi.parse_header(headers['Content-Type'])
            if 'charset' in params:
                return params['charset']


def _determine_base_url(document, page_url):
    """Determine the HTML document's base URL.

    This looks for a ``<base>`` tag in the HTML document. If present, its href
    attribute denotes the base URL of anchor tags in the document. If there is
    no such tag (or if it does not have a valid href attribute), the HTML
    file's URL is used as the base URL.

    :param document: An HTML document representation. The current
        implementation expects the result of ``html5lib.parse()``.
    :param page_url: The URL of the HTML document.
    """
    for base in document.findall('.//base'):
        href = base.get('href')
        if href is not None:
            return href

    return page_url


def _clean_url_path_part(part):
    """
    Clean a "part" of a URL path (i.e. after splitting on "@" characters).
    """
    return urllib_parse.quote(urllib_parse.unquote(part))


def _clean_file_url_path(part):
    """
    Clean the first part of a URL path that corresponds to a local
    filesystem path (i.e. the first part after splitting on "@" characters).
    """
    return urllib_request.pathname2url(urllib_request.url2pathname(part))


_reserved_chars_re = re.compile('(@|%2F)', re.IGNORECASE)

def _clean_url_path(path, is_local_path):
    """
    Clean the path portion of a URL.
    """
    if is_local_path:
        clean_func = _clean_file_url_path
    else:
        clean_func = _clean_url_path_part
    parts = _reserved_chars_re.split(path)
    cleaned_parts = []
    for to_clean, reserved in pairwise(itertools.chain(parts, [''])):
        cleaned_parts.append(clean_func(to_clean))
        cleaned_parts.append(reserved.upper())

    return ''.join(cleaned_parts)


def _clean_link(url):
    """
    Make sure a link is fully quoted.
    For example, if ' ' occurs in the URL, it will be replaced with "%20",
    and without double-quoting other characters.
    """
    result = urllib_parse.urlparse(url)
    is_local_path = not result.netloc
    path = _clean_url_path((result.path), is_local_path=is_local_path)
    return urllib_parse.urlunparse(result._replace(path=path))


def _create_link_from_element(anchor, page_url, base_url):
    """
    Convert an anchor element in a simple repository page to a Link.
    """
    href = anchor.get('href')
    if not href:
        return
    url = _clean_link(urllib_parse.urljoin(base_url, href))
    pyrequire = anchor.get('data-requires-python')
    pyrequire = unescape(pyrequire) if pyrequire else None
    yanked_reason = anchor.get('data-yanked')
    if yanked_reason:
        yanked_reason = unescape(yanked_reason)
    link = Link(url,
      comes_from=page_url,
      requires_python=pyrequire,
      yanked_reason=yanked_reason)
    return link


class CacheablePageContent(object):

    def __init__(self, page):
        assert page.cache_link_parsing
        self.page = page

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.page.url == other.page.url

    def __hash__(self):
        return hash(self.page.url)


def with_cached_html_pages(fn):
    """
    Given a function that parses an Iterable[Link] from an HTMLPage, cache the
    function's result (keyed by CacheablePageContent), unless the HTMLPage
    `page` has `page.cache_link_parsing == False`.
    """

    @_lru_cache(maxsize=None)
    def wrapper(cacheable_page):
        return list(fn(cacheable_page.page))

    @functools.wraps(fn)
    def wrapper_wrapper(page):
        if page.cache_link_parsing:
            return wrapper(CacheablePageContent(page))
        return list(fn(page))

    return wrapper_wrapper


@with_cached_html_pages
def parse_links(page):
    """
    Parse an HTML document, and yield its anchor elements as Link objects.
    """
    document = html5lib.parse((page.content),
      transport_encoding=(page.encoding),
      namespaceHTMLElements=False)
    url = page.url
    base_url = _determine_base_url(document, url)
    for anchor in document.findall('.//a'):
        link = _create_link_from_element(anchor,
          page_url=url,
          base_url=base_url)
        if link is None:
            continue
        yield link


class HTMLPage(object):
    __doc__ = 'Represents one page, along with its URL'

    def __init__(self, content, encoding, url, cache_link_parsing=True):
        """
        :param encoding: the encoding to decode the given content.
        :param url: the URL from which the HTML was downloaded.
        :param cache_link_parsing: whether links parsed from this page's url
                                   should be cached. PyPI index urls should
                                   have this set to False, for example.
        """
        self.content = content
        self.encoding = encoding
        self.url = url
        self.cache_link_parsing = cache_link_parsing

    def __str__(self):
        return redact_auth_from_url(self.url)


def _handle_get_page_fail(link, reason, meth=None):
    if meth is None:
        meth = logger.debug
    meth('Could not fetch URL %s: %s - skipping', link, reason)


def _make_html_page(response, cache_link_parsing=True):
    encoding = _get_encoding_from_headers(response.headers)
    return HTMLPage((response.content),
      encoding=encoding,
      url=(response.url),
      cache_link_parsing=cache_link_parsing)


def _get_html_page(link, session=None):
    if session is None:
        raise TypeError("_get_html_page() missing 1 required keyword argument: 'session'")
    else:
        url = link.url.split('#', 1)[0]
        vcs_scheme = _match_vcs_scheme(url)
        if vcs_scheme:
            logger.debug('Cannot look at %s URL %s', vcs_scheme, link)
            return
        scheme, _, path, _, _, _ = urllib_parse.urlparse(url)
        if scheme == 'file':
            if os.path.isdir(urllib_request.url2pathname(path)):
                if not url.endswith('/'):
                    url += '/'
                url = urllib_parse.urljoin(url, 'index.html')
                logger.debug(' file: URL is directory, getting %s', url)
        try:
            resp = _get_html_response(url, session=session)
        except _NotHTTP:
            logger.debug('Skipping page %s because it looks like an archive, and cannot be checked by HEAD.', link)
        except _NotHTML as exc:
            try:
                logger.debug('Skipping page %s because the %s request got Content-Type: %s', link, exc.request_desc, exc.content_type)
            finally:
                exc = None
                del exc

        except HTTPError as exc:
            try:
                _handle_get_page_fail(link, exc)
            finally:
                exc = None
                del exc

        except RetryError as exc:
            try:
                _handle_get_page_fail(link, exc)
            finally:
                exc = None
                del exc

        except SSLError as exc:
            try:
                reason = 'There was a problem confirming the ssl certificate: '
                reason += str(exc)
                _handle_get_page_fail(link, reason, meth=(logger.info))
            finally:
                exc = None
                del exc

        except requests.ConnectionError as exc:
            try:
                _handle_get_page_fail(link, 'connection error: {}'.format(exc))
            finally:
                exc = None
                del exc

        except requests.Timeout:
            _handle_get_page_fail(link, 'timed out')
        else:
            return _make_html_page(resp, cache_link_parsing=(link.cache_link_parsing))


def _remove_duplicate_links(links):
    """
    Return a list of links, with duplicates removed and ordering preserved.
    """
    return list(OrderedDict.fromkeys(links))


def group_locations--- This code section failed: ---

 L. 496         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'files'

 L. 497         4  BUILD_LIST_0          0 
                6  STORE_DEREF              'urls'

 L. 500         8  LOAD_CLOSURE             'files'
               10  LOAD_CLOSURE             'urls'
               12  BUILD_TUPLE_2         2 
               14  LOAD_CODE                <code_object sort_path>
               16  LOAD_STR                 'group_locations.<locals>.sort_path'
               18  MAKE_FUNCTION_8          'closure'
               20  STORE_FAST               'sort_path'

 L. 508        22  SETUP_LOOP          254  'to 254'
               24  LOAD_FAST                'locations'
               26  GET_ITER         
               28  FOR_ITER            252  'to 252'
               30  STORE_FAST               'url'

 L. 510        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              exists
               38  LOAD_FAST                'url'
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'is_local_path'

 L. 511        44  LOAD_FAST                'url'
               46  LOAD_METHOD              startswith
               48  LOAD_STR                 'file:'
               50  CALL_METHOD_1         1  '1 positional argument'
               52  STORE_FAST               'is_file_url'

 L. 513        54  LOAD_FAST                'is_local_path'
               56  POP_JUMP_IF_TRUE     62  'to 62'
               58  LOAD_FAST                'is_file_url'
               60  POP_JUMP_IF_FALSE   218  'to 218'
             62_0  COME_FROM            56  '56'

 L. 514        62  LOAD_FAST                'is_local_path'
               64  POP_JUMP_IF_FALSE    72  'to 72'

 L. 515        66  LOAD_FAST                'url'
               68  STORE_FAST               'path'
               70  JUMP_FORWARD         80  'to 80'
             72_0  COME_FROM            64  '64'

 L. 517        72  LOAD_GLOBAL              url_to_path
               74  LOAD_FAST                'url'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  STORE_FAST               'path'
             80_0  COME_FROM            70  '70'

 L. 518        80  LOAD_GLOBAL              os
               82  LOAD_ATTR                path
               84  LOAD_METHOD              isdir
               86  LOAD_FAST                'path'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  POP_JUMP_IF_FALSE   182  'to 182'

 L. 519        92  LOAD_FAST                'expand_dir'
               94  POP_JUMP_IF_FALSE   148  'to 148'

 L. 520        96  LOAD_GLOBAL              os
               98  LOAD_ATTR                path
              100  LOAD_METHOD              realpath
              102  LOAD_FAST                'path'
              104  CALL_METHOD_1         1  '1 positional argument'
              106  STORE_FAST               'path'

 L. 521       108  SETUP_LOOP          180  'to 180'
              110  LOAD_GLOBAL              os
              112  LOAD_METHOD              listdir
              114  LOAD_FAST                'path'
              116  CALL_METHOD_1         1  '1 positional argument'
              118  GET_ITER         
              120  FOR_ITER            144  'to 144'
              122  STORE_FAST               'item'

 L. 522       124  LOAD_FAST                'sort_path'
              126  LOAD_GLOBAL              os
              128  LOAD_ATTR                path
              130  LOAD_METHOD              join
              132  LOAD_FAST                'path'
              134  LOAD_FAST                'item'
              136  CALL_METHOD_2         2  '2 positional arguments'
              138  CALL_FUNCTION_1       1  '1 positional argument'
              140  POP_TOP          
              142  JUMP_BACK           120  'to 120'
              144  POP_BLOCK        
              146  JUMP_ABSOLUTE       216  'to 216'
            148_0  COME_FROM            94  '94'

 L. 523       148  LOAD_FAST                'is_file_url'
              150  POP_JUMP_IF_FALSE   164  'to 164'

 L. 524       152  LOAD_DEREF               'urls'
              154  LOAD_METHOD              append
              156  LOAD_FAST                'url'
              158  CALL_METHOD_1         1  '1 positional argument'
              160  POP_TOP          
              162  JUMP_ABSOLUTE       216  'to 216'
            164_0  COME_FROM           150  '150'

 L. 526       164  LOAD_GLOBAL              logger
              166  LOAD_METHOD              warning

 L. 527       168  LOAD_STR                 "Path '{0}' is ignored: it is a directory."
              170  LOAD_METHOD              format

 L. 528       172  LOAD_FAST                'path'
              174  CALL_METHOD_1         1  '1 positional argument'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  POP_TOP          
            180_0  COME_FROM_LOOP      108  '108'
              180  JUMP_ABSOLUTE       250  'to 250'
            182_0  COME_FROM            90  '90'

 L. 530       182  LOAD_GLOBAL              os
              184  LOAD_ATTR                path
              186  LOAD_METHOD              isfile
              188  LOAD_FAST                'path'
              190  CALL_METHOD_1         1  '1 positional argument'
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 531       194  LOAD_FAST                'sort_path'
              196  LOAD_FAST                'path'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  POP_TOP          
              202  JUMP_ABSOLUTE       250  'to 250'
            204_0  COME_FROM           192  '192'

 L. 533       204  LOAD_GLOBAL              logger
              206  LOAD_METHOD              warning

 L. 534       208  LOAD_STR                 "Url '%s' is ignored: it is neither a file nor a directory."

 L. 535       210  LOAD_FAST                'url'
              212  CALL_METHOD_2         2  '2 positional arguments'
              214  POP_TOP          
              216  JUMP_BACK            28  'to 28'
            218_0  COME_FROM            60  '60'

 L. 537       218  LOAD_GLOBAL              is_url
              220  LOAD_FAST                'url'
              222  CALL_FUNCTION_1       1  '1 positional argument'
              224  POP_JUMP_IF_FALSE   238  'to 238'

 L. 539       226  LOAD_DEREF               'urls'
              228  LOAD_METHOD              append
              230  LOAD_FAST                'url'
              232  CALL_METHOD_1         1  '1 positional argument'
              234  POP_TOP          
              236  JUMP_BACK            28  'to 28'
            238_0  COME_FROM           224  '224'

 L. 541       238  LOAD_GLOBAL              logger
              240  LOAD_METHOD              warning

 L. 542       242  LOAD_STR                 "Url '%s' is ignored. It is either a non-existing path or lacks a specific scheme."

 L. 543       244  LOAD_FAST                'url'
              246  CALL_METHOD_2         2  '2 positional arguments'
              248  POP_TOP          
              250  JUMP_BACK            28  'to 28'
              252  POP_BLOCK        
            254_0  COME_FROM_LOOP       22  '22'

 L. 546       254  LOAD_DEREF               'files'
              256  LOAD_DEREF               'urls'
              258  BUILD_TUPLE_2         2 
              260  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 180_0


class CollectedLinks(object):
    __doc__ = '\n    Encapsulates the return value of a call to LinkCollector.collect_links().\n\n    The return value includes both URLs to project pages containing package\n    links, as well as individual package Link objects collected from other\n    sources.\n\n    This info is stored separately as:\n\n    (1) links from the configured file locations,\n    (2) links from the configured find_links, and\n    (3) urls to HTML project pages, as described by the PEP 503 simple\n        repository API.\n    '

    def __init__(self, files, find_links, project_urls):
        """
        :param files: Links from file locations.
        :param find_links: Links from find_links.
        :param project_urls: URLs to HTML project pages, as described by
            the PEP 503 simple repository API.
        """
        self.files = files
        self.find_links = find_links
        self.project_urls = project_urls


class LinkCollector(object):
    __doc__ = "\n    Responsible for collecting Link objects from all configured locations,\n    making network requests as needed.\n\n    The class's main method is its collect_links() method.\n    "

    def __init__(self, session, search_scope):
        self.search_scope = search_scope
        self.session = session

    @property
    def find_links(self):
        return self.search_scope.find_links

    def fetch_page(self, location):
        """
        Fetch an HTML page containing package links.
        """
        return _get_html_page(location, session=(self.session))

    def collect_links(self, project_name):
        """Find all available links for the given project name.

        :return: All the Link objects (unfiltered), as a CollectedLinks object.
        """
        search_scope = self.search_scope
        index_locations = search_scope.get_index_urls_locations(project_name)
        index_file_loc, index_url_loc = group_locations(index_locations)
        fl_file_loc, fl_url_loc = group_locations((self.find_links),
          expand_dir=True)
        file_links = [Link(url) for url in itertools.chain(index_file_loc, fl_file_loc)]
        find_link_links = [Link(url, '-f') for url in self.find_links]
        url_locations = [link for link in itertools.chain((Link(url, cache_link_parsing=False) for url in index_url_loc), (Link(url) for url in fl_url_loc)) if self.session.is_secure_origin(link)]
        url_locations = _remove_duplicate_links(url_locations)
        lines = [
         '{} location(s) to search for versions of {}:'.format(len(url_locations), project_name)]
        for link in url_locations:
            lines.append('* {}'.format(link))

        logger.debug('\n'.join(lines))
        return CollectedLinks(files=file_links,
          find_links=find_link_links,
          project_urls=url_locations)