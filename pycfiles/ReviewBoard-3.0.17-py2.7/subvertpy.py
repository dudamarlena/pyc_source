# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/scmtools/svn/subvertpy.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import absolute_import, unicode_literals
import logging, os
from datetime import datetime
try:
    from subvertpy import AUTH_PARAM_DEFAULT_PASSWORD, AUTH_PARAM_DEFAULT_USERNAME, ra, SubversionException, __version__
    from subvertpy.client import Client as SVNClient, api_version, get_config
    has_svn_backend = __version__ >= (0, 9, 1)
except ImportError:
    has_svn_backend = False

from django.utils import six
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext as _
from reviewboard.scmtools.core import Revision, HEAD, PRE_CREATION
from reviewboard.scmtools.errors import FileNotFoundError, SCMError
from reviewboard.scmtools.svn import base, SVNTool
from reviewboard.scmtools.svn.utils import collapse_svn_keywords, has_expanded_svn_keywords
B = six.binary_type
DIFF_UNIFIED = [B(b'-u')]
SVN_KEYWORDS = B(b'svn:keywords')

class Client(base.Client):
    required_module = b'subvertpy'

    def __init__(self, config_dir, repopath, username=None, password=None):
        super(Client, self).__init__(config_dir, repopath, username, password)
        self.repopath = B(self.repopath)
        self.config_dir = B(config_dir)
        self._ssl_trust_prompt_cb = None
        auth_providers = [
         ra.get_simple_provider(),
         ra.get_username_provider()]
        if repopath.startswith(b'https:'):
            auth_providers += [
             ra.get_ssl_client_cert_file_provider(),
             ra.get_ssl_client_cert_pw_file_provider(),
             ra.get_ssl_server_trust_file_provider(),
             ra.get_ssl_server_trust_prompt_provider(self.ssl_trust_prompt)]
        self.auth = ra.Auth(auth_providers)
        self.username = None
        self.password = None
        if username:
            self.username = username
            self.auth.set_parameter(AUTH_PARAM_DEFAULT_USERNAME, B(self.username))
        if password:
            self.password = password
            self.auth.set_parameter(AUTH_PARAM_DEFAULT_PASSWORD, B(self.password))
        cfg = get_config(self.config_dir)
        self.client = SVNClient(cfg, auth=self.auth)
        return

    def set_ssl_server_trust_prompt(self, cb):
        self._ssl_trust_prompt_cb = cb

    def get_file(self, path, revision=HEAD):
        """Returns the contents of a given file at the given revision."""
        if not path:
            raise FileNotFoundError(path, revision)
        revnum = self._normalize_revision(revision)
        path = B(self.normalize_path(path))
        data = six.StringIO()
        try:
            self.client.cat(path, data, revnum)
        except SubversionException as e:
            raise FileNotFoundError(e)

        contents = data.getvalue()
        if has_expanded_svn_keywords(contents):
            keywords = self.get_keywords(path, revision)
            if keywords:
                contents = collapse_svn_keywords(contents, keywords)
        return contents

    def get_keywords(self, path, revision=HEAD):
        """Returns a list of SVN keywords for a given path."""
        revnum = self._normalize_revision(revision, negatives_allowed=False)
        path = self.normalize_path(path)
        return self.client.propget(SVN_KEYWORDS, path, None, revnum).get(path)

    def _normalize_revision(self, revision, negatives_allowed=True):
        if revision is None:
            return
        else:
            if revision == HEAD:
                return B(b'HEAD')
            if revision == PRE_CREATION:
                raise FileNotFoundError(b'', revision)
            elif isinstance(revision, Revision):
                revision = int(revision.name)
            elif isinstance(revision, (B,) + six.string_types):
                revision = int(revision)
            return revision

    @property
    def repository_info(self):
        """Returns metadata about the repository:

        * UUID
        * Root URL
        * URL
        """
        try:
            base = os.path.basename(self.repopath)
            info = self.client.info(self.repopath, b'HEAD')[base]
        except SubversionException as e:
            raise SVNTool.normalize_error(e)

        return {b'uuid': info.repos_uuid, 
           b'root_url': info.repos_root_url, 
           b'url': info.url}

    def ssl_trust_prompt(self, realm, failures, certinfo, may_save):
        """
        Callback for ``subvertpy.ra.get_ssl_server_trust_prompt_provider``.
        ``may_save`` indicates whether to save the cert info for
        subsequent requests.

        Calls ``callback_ssl_server_trust_prompt`` if it exists.

        :param certinfo: (hostname, fingerprint, valid_from, valid_until,
                          issuer_dname, ascii_cert)
        :return: (accepted_failures, may_save)
        """
        if self._ssl_trust_prompt_cb:
            trust_dict = {b'realm': realm, b'failures': failures, 
               b'hostname': certinfo[0], 
               b'finger_print': certinfo[1], 
               b'valid_from': certinfo[2], 
               b'valid_until': certinfo[3], 
               b'issuer_dname': certinfo[4]}
            return self._ssl_trust_prompt_cb(trust_dict)[1:]
        else:
            return
            return

    def accept_ssl_certificate(self, path, on_failure=None):
        """If the repository uses SSL, this method is used to determine whether
        the SSL certificate can be automatically accepted.

        If the cert cannot be accepted, the ``on_failure`` callback
        is executed.

        ``on_failure`` signature::

            void on_failure(e:Exception, path:str, cert:dict)
        """
        cert = {}

        def _accept_trust_prompt(realm, failures, certinfo, may_save):
            cert.update({b'realm': realm, 
               b'failures': failures, 
               b'hostname': certinfo[0], 
               b'finger_print': certinfo[1], 
               b'valid_from': certinfo[2], 
               b'valid_until': certinfo[3], 
               b'issuer_dname': certinfo[4]})
            if on_failure:
                return (0, False)
            else:
                del cert[b'failures']
                return (failures, True)

        auth = ra.Auth([
         ra.get_simple_provider(),
         ra.get_username_provider(),
         ra.get_ssl_client_cert_file_provider(),
         ra.get_ssl_client_cert_pw_file_provider(),
         ra.get_ssl_server_trust_file_provider(),
         ra.get_ssl_server_trust_prompt_provider(_accept_trust_prompt)])
        if self.username:
            auth.set_parameter(AUTH_PARAM_DEFAULT_USERNAME, B(self.username))
        if self.password:
            auth.set_parameter(AUTH_PARAM_DEFAULT_PASSWORD, B(self.password))
        cfg = get_config(self.config_dir)
        client = SVNClient(cfg, auth)
        try:
            info = client.info(path)
            logging.debug(b'SVN: Got repository information for %s: %s' % (
             path, info))
        except SubversionException as e:
            if on_failure:
                on_failure(e, path, cert)

        return cert

    def get_log(self, path, start=None, end=None, limit=None, discover_changed_paths=False, limit_to_path=False):
        """Returns log entries at the specified path.

        The log entries will appear ordered from most recent to least,
        with 'start' being the most recent commit in the range.

        If 'start' is not specified, then it will default to 'HEAD'. If
        'end' is not specified, it will default to '1'.

        To limit the commits to the given path, not factoring in history
        from any branch operations, set 'limit_to_path' to True.
        """

        def log_cb(changed_paths, revision, props, has_children):
            commit = {b'revision': six.text_type(revision)}
            if b'svn:date' in props:
                commit[b'date'] = datetime.strptime(props[b'svn:date'], b'%Y-%m-%dT%H:%M:%S.%fZ')
            if b'svn:author' in props:
                commit[b'author'] = props[b'svn:author']
            if b'svn:log' in props:
                commit[b'message'] = props[b'svn:log']
            commits.append(commit)

        if start is None:
            start = self.LOG_DEFAULT_START
        if end is None:
            end = self.LOG_DEFAULT_END
        commits = []
        self.client.log(log_cb, paths=B(self.normalize_path(path)), start_rev=self._normalize_revision(start), end_rev=self._normalize_revision(end), limit=limit, discover_changed_paths=discover_changed_paths, strict_node_history=limit_to_path)
        return commits

    def list_dir(self, path):
        """Lists the contents of the specified path.

        The result will be an ordered dictionary of contents, mapping
        filenames or directory names with a dictionary containing:

        * ``path``        - The full path of the file or directory.
        * ``created_rev`` - The revision where the file or directory was
                            created.
        """
        result = SortedDict()
        if api_version()[:2] >= (1, 5):
            depth = 2
        else:
            depth = 0
        norm_path = B(self.normalize_path(path)).rstrip(b'/')
        dirents = self.client.list(norm_path, None, depth)
        for name, dirent in six.iteritems(dirents):
            if name:
                result[six.text_type(name)] = {b'path': b'%s/%s' % (path.strip(b'/'), name), b'created_rev': six.text_type(dirent[b'created_rev'])}

        return result

    def diff(self, revision1, revision2, path=None):
        """Returns a diff between two revisions.

        The diff will contain the differences between the two revisions,
        and may optionally be limited to a specific path.

        The returned diff will be returned as a Unicode object.
        """
        if path:
            path = self.normalize_path(path)
        else:
            path = self.repopath
        out = None
        err = None
        try:
            try:
                out, err = self.client.diff(self._normalize_revision(revision1), self._normalize_revision(revision2), B(path), B(path), diffopts=DIFF_UNIFIED)
                diff = out.read()
            except Exception as e:
                logging.error(b'Failed to generate diff using subvertpy for revisions %s:%s for path %s: %s', revision1, revision2, path, e, exc_info=1)
                raise SCMError(_(b'Unable to get diff revisions %s through %s: %s') % (
                 revision1, revision2, e))

        finally:
            if out:
                out.close()
            if err:
                err.close()

        return diff