# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/backend/errata.py
# Compiled at: 2020-01-28 22:20:54
# Size of source mod 2**32: 6611 bytes
import os, threading, logging
from concurrent import futures
from six.moves.urllib import parse
from six.moves.xmlrpc_client import ServerProxy
from more_executors import Executors
from more_executors.futures import f_map, f_zip
from ..source import Source
from ..model import ErratumPushItem
LOG = logging.getLogger('pushsource')

class ErrataSource(Source):
    """ErrataSource"""

    def __init__(self, url, errata, target='cdn', koji_url=None, threads=4, timeout=14400):
        """Create a new source.

        Parameters:
            url (src)
                Base URL of Errata Tool, e.g. "http://errata.example.com",
                "https://errata.example.com:8123".

            errata (str, list[str])
                Advisory ID(s) to be used as push item source.
                If a single string is given, multiple IDs may be
                comma-separated.

            target (str)
                The target type used when querying Errata Tool.
                The target type may influence the content produced,
                depending on the Errata Tool settings.

                Valid values include at least: "cdn", "rhn", "ftp".

            koji_url (str)
                URL of the koji instance (XML-RPC endpoint) associated with this
                Errata Tool instance.

            threads (int)
                Number of threads used for concurrent queries to Errata Tool.

            timeout (int)
                Number of seconds after which an error is raised, if no progress is
                made during queries to Errata Tool.
        """
        self._url = url
        self._errata = errata
        self._target = target
        self._timeout = timeout
        self._tls = threading.local()
        self._executor = Executors.thread_pool(max_workers=threads).with_retry()

    @property
    def _errata_service_url(self):
        parsed = parse.urlparse(self._url)
        base = 'http://' + parsed.netloc
        return os.path.join(base, parsed.path, 'errata/errata_service')

    @property
    def _errata_service(self):
        if not hasattr(self._tls, 'errata_service'):
            url = self._errata_service_url
            LOG.debug('Creating XML-RPC client for Errata Tool: %s', url)
            self._tls.errata_service = ServerProxy(url)
        return self._tls.errata_service

    @property
    def _advisory_ids(self):
        return self._errata

    def _get_advisory_metadata(self, advisory_id):
        return self._errata_service.get_advisory_cdn_metadata(advisory_id)

    def _get_advisory_file_list(self, advisory_id):
        return self._errata_service.get_advisory_cdn_file_list(advisory_id)

    def _push_items_from_raw(self, metadata_and_file_list):
        metadata, file_list = metadata_and_file_list
        erratum = self._erratum_push_item_from_metadata(metadata)
        files = self._push_items_from_files(file_list)
        return [
         self._erratum_push_item_from_metadata(metadata)]

    def _erratum_push_item_from_metadata(self, metadata):
        kwargs = {}
        kwargs['name'] = metadata['id']
        kwargs['state'] = 'PENDING'
        for field in ('type', 'release', 'status', 'pushcount', 'reboot_suggested',
                      'rights', 'title', 'description', 'version', 'updated', 'issued',
                      'severity', 'summary', 'solution'):
            kwargs[field] = metadata[field]

        kwargs['from_'] = metadata['from']
        if metadata.get('cdn_repo'):
            kwargs['dest'] = metadata['cdn_repo']
        pulp_user_metadata = metadata.get('pulp_user_metadata') or 
        if pulp_user_metadata.get('content_types'):
            kwargs['content_types'] = pulp_user_metadata['content_types']
        return ErratumPushItem(**kwargs)

    def _push_items_from_files(self, file_list):
        LOG.warn('file list: %s', file_list)
        return []

    def __iter__(self):
        """Iterate over the push items contained within this source.
        """
        advisory_raw_fs = []
        for advisory_id in self._advisory_ids:
            metadata_f = self._executor.submit(self._get_advisory_metadata, advisory_id)
            filelist_f = self._executor.submit(self._get_advisory_file_list, advisory_id)
            advisory_raw_fs.append(f_zip(metadata_f, filelist_f))

        advisory_push_items_fs = [f_map(f, self._push_items_from_raw) for f in advisory_raw_fs]
        completed_fs = futures.as_completed(advisory_push_items_fs,
          timeout=(self._timeout))
        for f in completed_fs:
            for pushitem in f.result():
                yield pushitem


Source.register_backend('errata', ErrataSource)