# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/pungi_compose.py
# Compiled at: 2019-01-28 02:13:22
import os, requests, productmd.common

class PungiCompose(object):
    """Represents 3rd party Pungi Compose"""

    def __init__(self, variant_url):
        """
        Creates new PungiCompose.

        :param str metadata_url: URL to Pungi variant repository directory.
        """
        self.variant_url = variant_url.rstrip('/')
        self.variant_name = os.path.basename(self.variant_url)
        self.metadata_url = os.path.join(os.path.dirname(self.variant_url), 'metadata')

    def _fetch_json(self, url):
        """
        Fetches the json file represented by `url`.
        """
        r = requests.get(url)
        r.raise_for_status()
        return r.json()

    def get_rpms_data(self):
        """
        Returns the data describing the RPMs in the pungi compose.
        :rtype: dict.
        :return: Dictionary with RPMs data in following format:
            {
                "sigkeys": set() with sigkeys used in the compose.
                "arches": set() with all the arches used in the compose.
                "builds": {
                    koji-build-nvr1: set() with the RPMs NEVRAs,
                    koji-build-nvr2: ...,
                    ...
                }
            }
        """
        ret = {}
        ret['sigkeys'] = set()
        ret['arches'] = set()
        ret['builds'] = {}
        url = os.path.join(self.metadata_url, 'rpms.json')
        data = self._fetch_json(url)
        srpms_per_arch = data.get('payload', {}).get('rpms', {}).get(self.variant_name)
        if not srpms_per_arch:
            raise ValueError('The %s does not contain payload -> rpms -> %s section' % (
             url, self.variant_name))
        for arch, srpms in srpms_per_arch.items():
            ret['arches'].add(arch)
            for srpm_nevra, rpms in srpms.items():
                packages = set()
                for rpm_nevra, rpm_data in rpms.items():
                    packages.add(rpm_nevra)
                    ret['sigkeys'].add(rpm_data['sigkey'])

                srpm_nvr = ('{name}-{version}-{release}').format(**productmd.common.parse_nvra(srpm_nevra))
                ret['builds'][srpm_nvr] = packages

        return ret