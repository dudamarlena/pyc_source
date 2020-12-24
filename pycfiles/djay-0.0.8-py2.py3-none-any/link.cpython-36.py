# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/models/link.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 6553 bytes
import posixpath, re
from pip._vendor.six.moves.urllib import parse as urllib_parse
from pip._internal.utils.misc import WHEEL_EXTENSION, path_to_url, redact_password_from_url, split_auth_from_netloc, splitext
from pip._internal.utils.models import KeyBasedCompareMixin
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, Text, Tuple, Union
    from pip._internal.index import HTMLPage
    from pip._internal.utils.hashes import Hashes

class Link(KeyBasedCompareMixin):
    __doc__ = "Represents a parsed link from a Package Index's simple URL\n    "

    def __init__(self, url, comes_from=None, requires_python=None, yanked_reason=None):
        """
        :param url: url of the resource pointed to (href of the link)
        :param comes_from: instance of HTMLPage where the link was found,
            or string.
        :param requires_python: String containing the `Requires-Python`
            metadata field, specified in PEP 345. This may be specified by
            a data-requires-python attribute in the HTML link tag, as
            described in PEP 503.
        :param yanked_reason: the reason the file has been yanked, if the
            file has been yanked, or None if the file hasn't been yanked.
            This is the value of the "data-yanked" attribute, if present, in
            a simple repository HTML link. If the file has been yanked but
            no reason was provided, this should be the empty string. See
            PEP 592 for more information and the specification.
        """
        if url.startswith('\\\\'):
            url = path_to_url(url)
        self._parsed_url = urllib_parse.urlsplit(url)
        self._url = url
        self.comes_from = comes_from
        self.requires_python = requires_python if requires_python else None
        self.yanked_reason = yanked_reason
        super(Link, self).__init__(key=url, defining_class=Link)

    def __str__(self):
        if self.requires_python:
            rp = ' (requires-python:%s)' % self.requires_python
        else:
            rp = ''
        if self.comes_from:
            return '%s (from %s)%s' % (redact_password_from_url(self._url),
             self.comes_from, rp)
        else:
            return redact_password_from_url(str(self._url))

    def __repr__(self):
        return '<Link %s>' % self

    @property
    def url(self):
        return self._url

    @property
    def filename(self):
        path = self.path.rstrip('/')
        name = posixpath.basename(path)
        if not name:
            netloc, user_pass = split_auth_from_netloc(self.netloc)
            return netloc
        else:
            name = urllib_parse.unquote(name)
            assert name, 'URL %r produced no filename' % self._url
            return name

    @property
    def scheme(self):
        return self._parsed_url.scheme

    @property
    def netloc(self):
        """
        This can contain auth information.
        """
        return self._parsed_url.netloc

    @property
    def path(self):
        return urllib_parse.unquote(self._parsed_url.path)

    def splitext(self):
        return splitext(posixpath.basename(self.path.rstrip('/')))

    @property
    def ext(self):
        return self.splitext()[1]

    @property
    def url_without_fragment(self):
        scheme, netloc, path, query, fragment = self._parsed_url
        return urllib_parse.urlunsplit((scheme, netloc, path, query, None))

    _egg_fragment_re = re.compile('[#&]egg=([^&]*)')

    @property
    def egg_fragment(self):
        match = self._egg_fragment_re.search(self._url)
        if not match:
            return
        else:
            return match.group(1)

    _subdirectory_fragment_re = re.compile('[#&]subdirectory=([^&]*)')

    @property
    def subdirectory_fragment(self):
        match = self._subdirectory_fragment_re.search(self._url)
        if not match:
            return
        else:
            return match.group(1)

    _hash_re = re.compile('(sha1|sha224|sha384|sha256|sha512|md5)=([a-f0-9]+)')

    @property
    def hash(self):
        match = self._hash_re.search(self._url)
        if match:
            return match.group(2)

    @property
    def hash_name(self):
        match = self._hash_re.search(self._url)
        if match:
            return match.group(1)

    @property
    def show_url(self):
        return posixpath.basename(self._url.split('#', 1)[0].split('?', 1)[0])

    @property
    def is_wheel(self):
        return self.ext == WHEEL_EXTENSION

    @property
    def is_artifact(self):
        """
        Determines if this points to an actual artifact (e.g. a tarball) or if
        it points to an "abstract" thing like a path or a VCS location.
        """
        from pip._internal.vcs import vcs
        if self.scheme in vcs.all_schemes:
            return False
        else:
            return True

    @property
    def is_yanked(self):
        return self.yanked_reason is not None

    @property
    def has_hash(self):
        return self.hash_name is not None

    def is_hash_allowed(self, hashes):
        """
        Return True if the link has a hash and it is allowed.
        """
        if hashes is None or not self.has_hash:
            return False
        else:
            if not self.hash_name is not None:
                raise AssertionError
            elif not self.hash is not None:
                raise AssertionError
            return hashes.is_hash_allowed((self.hash_name), hex_digest=(self.hash))