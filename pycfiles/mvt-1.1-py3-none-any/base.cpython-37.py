# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/ios/base.py
# Compiled at: 2020-02-21 13:21:48
# Size of source mod 2**32: 5187 bytes
import os, re, glob, json, logging
from ..utils import get_domain_from_url, get_toplevel_from_url
import simplejson as json
log = logging.getLogger(__name__)

class IOSExtraction(object):
    __doc__ = 'This class provides a base for all iOS extraction modules.'
    enabled = True

    def __init__(self, file_path=None, backup_id=None, base_folder=None, output_folder=None, domains=None, root=False):
        """Initialize module.
        :param file_path: Path to the module's database file, if there is any.
        :param backup_id: iTunes backup database file's ID.
        :param base_folder: Path to the base folder (backup or filesystem dump).
        :param output_folder: Folder where results will be stored.
        :param domains: List of domains to check against.
        """
        self.file_path = file_path
        self.backup_id = backup_id
        self.base_folder = base_folder
        self.output_folder = output_folder
        self.domains = domains
        self.root = root
        self.results = None

    def _find_database(self, backup_id=None, root_paths=[]):
        """Try to locate the module's database file from either an iTunes
        backup or a full filesystem dump.
        :param backup_id: iTunes backup database file's ID (or hash).
        """
        file_path = None
        if not self.file_path:
            if not self.backup_id:
                self.backup_id = backup_id
            else:
                if self.backup_id:
                    file_path = os.path.join(self.base_folder, self.backup_id[0:2], self.backup_id)
                file_path = file_path and os.path.exists(file_path) or None
                for root_path in root_paths:
                    for found_path in glob.glob(os.path.join(self.base_folder, root_path)):
                        if os.path.exists(found_path):
                            file_path = found_path
                            break
                        file_path = None

        elif file_path:
            self.file_path = file_path
        else:
            raise FileNotFoundError("Impossible to find the module's database file")

    def _check_domains(self, urls):
        """Check the provided list of (suspicious) domains against a list of URLs.
        :param urls: List of URLs to check
        """
        if not self.domains:
            return
        for url in urls:
            if type(url) == bytes:
                url = url.decode()
            try:
                domain = get_domain_from_url(url)
                top_level = get_toplevel_from_url(url)
            except:
                for suspicious in self.domains:
                    if suspicious.lower() in url:
                        log.warning('Maybe found a known suspicious domain: %s', url)

            else:
                for suspicious in self.domains:
                    if domain == suspicious:
                        log.warning('Found a known suspicious domain: %s', url)
                        return True
                        if top_level == suspicious:
                            log.warning('Found a sub-domain matching a suspicious top level: %s', url)
                            return True

    def run(self):
        """Run the main module procedure.
        """
        raise NotImpementedError

    def save_to_json(self):
        """Save the collected results to a json file.
        """
        if not self.results:
            return
        sub = re.sub('(.)([A-Z][a-z]+)', '\\1_\\2', self.__class__.__name__)
        file_name = '{}.json'.format(re.sub('([a-z0-9])([A-Z])', '\\1_\\2', sub).lower())
        json_path = os.path.join(self.output_folder, file_name)
        with open(json_path, 'w') as (handle):
            json.dump((self.results), handle, indent=4)