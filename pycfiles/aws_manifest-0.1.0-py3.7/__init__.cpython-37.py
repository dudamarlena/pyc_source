# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/awsmanifest/__init__.py
# Compiled at: 2019-07-30 23:47:31
# Size of source mod 2**32: 2169 bytes
import json, os, requests
pkg_dir, _ = os.path.split(__file__)
local_policy_doc = f"{pkg_dir}/policies.js"
policies_url = 'https://awspolicygen.s3.amazonaws.com/js/policies.js'

def remote_manifest(url: str=policies_url) -> str:
    """
    Retrieve the latest manifest containing AWS services and actions
    """
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.text


def local_manifest(filename: str=local_policy_doc) -> str:
    """
    Retrieve the manifest bundled with the package
    """
    with open(local_policy_doc, 'r') as (f):
        return f.read()


def manifest(local: bool=False) -> dict:
    """
    Return a dictionary containing a mapping from amazon services
    to their actions
    """
    return AwsManifest(local).raw


class AwsManifest:
    __doc__ = '\n    A class for retrieving information about aws resources and their actions.\n\n    self.raw contains a dict with the full aws policy document\n    self.service_map contains a dict with aws resources and actions\n    '

    def __init__(self, local: bool=False):
        self.doc = local_manifest() if local else remote_manifest()
        idx = self.doc.find('{')
        self.raw = json.loads(self.doc[idx:])
        self.service_map = self.raw['serviceMap']

    def services(self) -> list:
        """
        Return a list containing the full names of aws services
        """
        return self.service_map.keys()

    def service_prefixes(self) -> list:
        """
        Return a list containing the prefix names for aws services
        """
        return [self.service_map[svc]['StringPrefix'] for svc in self.service_map.keys()]

    def actions(self, svc: str) -> list:
        """
        Return a list of actions for a given service.
        Full service names ("Amazon Ec2") or service prefixes ("ec2") are
        accepted.
        """
        for k, v in self.service_map.items():
            if svc == k or svc == v['StringPrefix']:
                return v['Actions']

        raise KeyError(svc)