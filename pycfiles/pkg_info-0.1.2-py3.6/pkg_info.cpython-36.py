# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pkg_info.py
# Compiled at: 2018-03-30 14:20:38
# Size of source mod 2**32: 1285 bytes
import requests

class Package(object):

    def __init__(self, data: dict):
        info = data.get('info')
        self.raw_data = data
        self.name = info.get('name')
        self.license = info.get('license')
        self.summary = info.get('summary')
        self.description = info.get('description')
        self.version = info.get('version')
        self.keywords = info.get('keywords')
        self.homepage = info.get('homepage')
        self.url = info.get('package_url')
        self.maintainer = Maintainer(info.get('maintainer'), info.get('maintainer_email'))
        self.author = Maintainer(info.get('author'), info.get('author_email'))

    def __repr__(self):
        return f'<Package name:"{self.name}" version:"{self.version}">'


class Maintainer(object):

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


def _get_data(pkg_name: str) -> dict:
    url = f"https://pypi.python.org/pypi/{pkg_name}/json"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_pkg_info(pkg_name: str) -> Package:
    data = _get_data(pkg_name)
    if data is not None:
        return Package(data)