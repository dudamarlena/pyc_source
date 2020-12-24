# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lib/chimera_cli/api.py
# Compiled at: 2019-12-26 07:34:51
# Size of source mod 2**32: 1240 bytes
from requests import post, get
from chimera_cli.configuration import configs
from json import load

class ClusterURLException(Exception):
    pass


class ChimeraException(Exception):
    pass


class chimera_rest_api:
    url = configs.clusterUrl
    url: str

    @staticmethod
    def create_channel(name: str, namespace: str, schema_path: str):
        try:
            with open(f".chimera/{schema_path}") as (f):
                schema = load(f)
        except:
            raise ChimeraException(f"Schema path invalid! - {e}")

        try:
            response = post(f"{url}/channel/{namespace}/{name}", json=schema)
        except Exception as e:
            try:
                raise ChimeraException(f"Unable to reach chimera cluster \n{e}")
            finally:
                e = None
                del e

        if response.status_code != 200:
            raise ChimeraException(f"Cluster response invalid! - {response.text()}")

    @staticmethod
    def delete_channel(name: str, namespace: str):
        try:
            response = post(f"{url}/delete/channel/{namespace}/{name}")
        except Exception as e:
            try:
                raise ChimeraException(f"Unable to reach chimera cluster \n{e}")
            finally:
                e = None
                del e

        if response.status_code != 200:
            raise ChimeraException(f"Cluster response invalid! - {response.text()}")