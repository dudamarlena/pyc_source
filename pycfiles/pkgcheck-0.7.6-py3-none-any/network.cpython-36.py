# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/network.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 10945 bytes
"""Various checks that require network support."""
import socket, traceback, urllib.request
from lxml import etree
from functools import partial
from itertools import chain
from pkgcore.fetch import fetchable
from .. import addons, base, results, sources
from . import NetworkCheck

class _UrlResult(results.FilteredVersionResult, results.Warning):
    __doc__ = 'Generic result for a URL with some type of failed status.'

    def __init__(self, attr, url, message, **kwargs):
        (super().__init__)(**kwargs)
        self.attr = attr
        self.url = url
        self.message = message

    @property
    def desc(self):
        return f"{self.attr}: {self.message}: {self.url}"


class DeadUrl(_UrlResult):
    __doc__ = 'Package with a dead URL of some type.'


class SSLCertificateError(_UrlResult):
    __doc__ = 'Package with https:// HOMEPAGE with an invalid SSL cert.'

    @property
    def desc(self):
        return f"{self.attr}: SSL cert error: {self.message}: {self.url}"


class _UpdatedUrlResult(results.FilteredVersionResult, results.Warning):
    __doc__ = 'Generic result for a URL that should be updated to an alternative.'
    message = None

    def __init__(self, attr, url, new_url, **kwargs):
        (super().__init__)(**kwargs)
        self.attr = attr
        self.url = url
        self.new_url = new_url

    @property
    def desc(self):
        msg = [self.attr]
        if self.message is not None:
            msg.append(self.message)
        msg.append(f"{self.url} -> {self.new_url}")
        return ': '.join(msg)


class RedirectedUrl(_UpdatedUrlResult):
    __doc__ = 'Package with a URL that permanently redirects to a different site.'
    message = 'permanently redirected'


class HttpsUrlAvailable(_UpdatedUrlResult):
    __doc__ = 'URL uses http:// when https:// is available.'
    message = 'HTTPS url available'


class _RequestException(Exception):
    __doc__ = 'Wrapper for requests exceptions.'

    def __init__(self, exc, msg=None):
        self.request_exc = exc
        self.msg = msg

    def __str__(self):
        if self.msg:
            return self.msg
        else:
            return str(self.request_exc)


class SSLError(_RequestException):
    __doc__ = 'Wrapper for requests SSLError exception.'


class RequestError(_RequestException):
    __doc__ = 'Wrapper for generic requests exception.'


class _UrlCheck(NetworkCheck):
    __doc__ = 'Generic URL verification check requiring network support.'
    known_results = frozenset([
     DeadUrl, RedirectedUrl, HttpsUrlAvailable, SSLCertificateError])

    def _http_check(self, attr, url, *, pkg):
        """Verify http:// and https:// URLs."""
        result = None
        try:
            r = self.session.head(url)
            redirected_url = None
            for response in r.history:
                if not response.is_permanent_redirect:
                    break
                redirected_url = response.headers['location']
                hsts = 'strict-transport-security' in response.headers

            if redirected_url:
                if redirected_url.startswith('https://'):
                    if url.startswith('http://'):
                        result = HttpsUrlAvailable(attr, url, redirected_url, pkg=pkg)
                elif redirected_url.startswith('http://'):
                    if hsts:
                        redirected_url = f"https://{redirected_url[7:]}"
                        result = RedirectedUrl(attr, url, redirected_url, pkg=pkg)
                else:
                    result = RedirectedUrl(attr, url, redirected_url, pkg=pkg)
        except SSLError as e:
            result = SSLCertificateError(attr, url, (str(e)), pkg=pkg)
        except RequestError as e:
            result = DeadUrl(attr, url, (str(e)), pkg=pkg)

        return result

    def _https_available_check(self, attr, url, *, future, orig_url, pkg):
        """Check if https:// alternatives exist for http:// URLs."""
        result = None
        try:
            r = self.session.head(url)
            redirected_url = None
            for response in r.history:
                if not response.is_permanent_redirect:
                    break
                redirected_url = response.headers['location']
                hsts = 'strict-transport-security' in response.headers

            if isinstance(future.result(), HttpsUrlAvailable) or redirected_url:
                if redirected_url.startswith('https://'):
                    result = HttpsUrlAvailable(attr, orig_url, redirected_url, pkg=pkg)
                elif redirected_url.startswith('http://'):
                    if hsts:
                        redirected_url = f"https://{redirected_url[7:]}"
                        result = HttpsUrlAvailable(attr, orig_url, redirected_url, pkg=pkg)
            else:
                result = HttpsUrlAvailable(attr, orig_url, url, pkg=pkg)
        except (RequestError, SSLError) as e:
            pass

        return result

    def _ftp_check(self, attr, url, *, pkg):
        """Verify ftp:// URLs with urllib."""
        result = None
        try:
            response = urllib.request.urlopen(url, timeout=(self.timeout))
        except urllib.error.URLError as e:
            result = DeadUrl(attr, url, (str(e.reason)), pkg=pkg)
        except socket.timeout as e:
            result = DeadUrl(attr, url, (str(e)), pkg=pkg)

        return result

    def task_done(self, results_q, pkg, future):
        """Determine the result of a given URL verification task."""
        exc = future.exception()
        if exc is not None:
            tb = traceback.format_exc()
            results_q.put((exc, tb))
            return
        result = future.result()
        if result is not None:
            if pkg is not None:
                data = result.attrs_to_pkg(result._attrs)
                data['pkg'] = pkg
                result = (result.__class__)(**data)
            results_q.put([result])

    def _get_urls(self, pkg):
        """Get URLs to verify for a given package."""
        raise NotImplementedError

    def _schedule_check(self, func, attr, url, executor, futures, results_q, **kwargs):
        """Schedule verification method to run in a separate thread against a given URL.

        Note that this tries to avoid hitting the network for the same URL
        twice using a mapping from requested URLs to future objects, adding
        result-checking callbacks to the futures of existing URLs.
        """
        future = futures.get(url)
        if future is None:
            future = (executor.submit)(func, attr, url, **kwargs)
            future.add_done_callback(partial(self.task_done, results_q, None))
            futures[url] = future
        else:
            future.add_done_callback(partial(self.task_done, results_q, kwargs['pkg']))

    def schedule(self, pkg, executor, futures, results_q):
        """Schedule verification methods to run in separate threads for all flagged URLs."""
        http_urls = []
        for attr, url in self._get_urls(pkg):
            if url.startswith('ftp://'):
                self._schedule_check((self._ftp_check),
                  attr, url, executor, futures, results_q, pkg=pkg)
            else:
                self._schedule_check((self._http_check),
                  attr, url, executor, futures, results_q, pkg=pkg)
                http_urls.append((attr, url))

        http_urls = tuple(http_urls)
        http_to_https_urls = ((attr, url, f"https://{url[7:]}") for attr, url in http_urls if url.startswith('http://'))
        for attr, orig_url, url in http_to_https_urls:
            future = futures[orig_url]
            self._schedule_check((self._https_available_check),
              attr, url, executor, futures, results_q, future=future,
              orig_url=orig_url,
              pkg=pkg)


class HomepageUrlCheck(_UrlCheck):
    __doc__ = 'Verify HOMEPAGE URLs.'

    def _get_urls(self, pkg):
        for url in pkg.homepage:
            yield ('HOMEPAGE', url)


class FetchablesUrlCheck(_UrlCheck):
    __doc__ = 'Verify SRC_URI URLs.'
    _filtering = False
    required_addons = (addons.UseAddon,)

    def __init__(self, *args, use_addon, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.fetch_filter = use_addon.get_filter('fetchables')

    def _get_urls(self, pkg):
        fetchables, _ = self.fetch_filter((
         fetchable,), pkg, pkg._get_attr['fetchables'](pkg,
          allow_missing_checksums=True, ignore_unknown_mirrors=True,
          skip_default_mirrors=True))
        for f in fetchables.keys():
            for url in f.uri:
                yield (
                 'SRC_URI', url)


class MetadataUrlCheck(_UrlCheck):
    __doc__ = 'Verify metadata.xml URLs.'
    scope = base.package_scope
    _source = sources.PackageRepoSource

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.protocols = ('http://', 'https://', 'ftp://')
        self.remote_map = {'bitbucket':'https://bitbucket.org/{project}', 
         'cpan':'https://metacpan.org/release/{project}', 
         'github':'https://github.com/{project}', 
         'gitlab':'https://gitlab.com/{project}', 
         'launchpad':'https://launchpad.net/{project}', 
         'pear':'https://pear.php.net/package/{project}', 
         'pypi':'https://pypi.org/project/{project}/', 
         'rubygems':'https://rubygems.org/gems/{project}', 
         'sourceforge':'https://sourceforge.net/projects/{project}/'}

    def _get_urls(self, pkg):
        try:
            tree = etree.parse(pkg._shared_pkg_data.metadata_xml._source)
        except etree.XMLSyntaxError:
            return
        else:
            for element in ('changelog', 'doc', 'bugs-to', 'remote-id'):
                for x in tree.xpath(f"//upstream/{element}"):
                    if x.text:
                        url = x.text
                        if element == 'remote-id':
                            try:
                                url = self.remote_map[x.attrib['type']].format(project=url)
                            except KeyError:
                                continue

                        if url.startswith(self.protocols):
                            yield (
                             f"metadata.xml: {element}", url)

    def schedule(self, pkgs, *args, **kwargs):
        (super().schedule)(pkgs[0], *args, **kwargs)