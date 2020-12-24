# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_internal/network/download.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 6260 bytes
"""Download files with progress indicators.
"""
import cgi, logging, mimetypes, os
from pip._vendor import requests
from pip._vendor.requests.models import CONTENT_CHUNK_SIZE
from pip._internal.models.index import PyPI
from pip._internal.network.cache import is_from_cache
from pip._internal.network.utils import response_chunks
from pip._internal.utils.misc import format_size, redact_auth_from_url, splitext
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.ui import DownloadProgressProvider
if MYPY_CHECK_RUNNING:
    from typing import Iterable, Optional
    from pip._vendor.requests.models import Response
    from pip._internal.models.link import Link
    from pip._internal.network.session import PipSession
logger = logging.getLogger(__name__)

def _get_http_response_size(resp):
    try:
        return int(resp.headers['content-length'])
    except (ValueError, KeyError, TypeError):
        return


def _prepare_download(resp, link, progress_bar):
    total_length = _get_http_response_size(resp)
    if link.netloc == PyPI.file_storage_domain:
        url = link.show_url
    else:
        url = link.url_without_fragment
    logged_url = redact_auth_from_url(url)
    if total_length:
        logged_url = '{} ({})'.format(logged_url, format_size(total_length))
    else:
        if is_from_cache(resp):
            logger.info('Using cached %s', logged_url)
        else:
            logger.info('Downloading %s', logged_url)
        if logger.getEffectiveLevel() > logging.INFO:
            show_progress = False
        else:
            if is_from_cache(resp):
                show_progress = False
            else:
                if not total_length:
                    show_progress = True
                else:
                    if total_length > 40000:
                        show_progress = True
                    else:
                        show_progress = False
        chunks = response_chunks(resp, CONTENT_CHUNK_SIZE)
        return show_progress or chunks
    return DownloadProgressProvider(progress_bar,
      max=total_length)(chunks)


def sanitize_content_filename(filename):
    """
    Sanitize the "filename" value from a Content-Disposition header.
    """
    return os.path.basename(filename)


def parse_content_disposition(content_disposition, default_filename):
    """
    Parse the "filename" value from a Content-Disposition header, and
    return the default filename if the result is empty.
    """
    _type, params = cgi.parse_header(content_disposition)
    filename = params.get('filename')
    if filename:
        filename = sanitize_content_filename(filename)
    return filename or default_filename


def _get_http_response_filename(resp, link):
    """Get an ideal filename from the given HTTP response, falling back to
    the link filename if not provided.
    """
    filename = link.filename
    content_disposition = resp.headers.get('content-disposition')
    if content_disposition:
        filename = parse_content_disposition(content_disposition, filename)
    ext = splitext(filename)[1]
    if not ext:
        ext = mimetypes.guess_extension(resp.headers.get('content-type', ''))
        if ext:
            filename += ext
    if not ext:
        if link.url != resp.url:
            ext = os.path.splitext(resp.url)[1]
            if ext:
                filename += ext
    return filename


def _http_get_download(session, link):
    target_url = link.url.split('#', 1)[0]
    resp = session.get(target_url,
      headers={'Accept-Encoding': 'identity'},
      stream=True)
    resp.raise_for_status()
    return resp


class Download(object):

    def __init__(self, response, filename, chunks):
        self.response = response
        self.filename = filename
        self.chunks = chunks


class Downloader(object):

    def __init__(self, session, progress_bar):
        self._session = session
        self._progress_bar = progress_bar

    def __call__(self, link):
        try:
            resp = _http_get_download(self._session, link)
        except requests.HTTPError as e:
            try:
                logger.critical('HTTP error %s while getting %s', e.response.status_code, link)
                raise
            finally:
                e = None
                del e

        return Download(resp, _get_http_response_filename(resp, link), _prepare_download(resp, link, self._progress_bar))