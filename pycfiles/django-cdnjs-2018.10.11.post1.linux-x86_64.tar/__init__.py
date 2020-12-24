# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/cdnjs/__init__.py
# Compiled at: 2018-10-11 09:11:52
from __future__ import unicode_literals
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import os, json, requests
from cdnjs.settings import Settings

class RepositoryNotFoundException(Exception):
    """
    If requested repository is not found at cdnjs.com
    """
    pass


class FileNotFoundException(Exception):
    """
    If requested file is not found at cdnjs.com repository
    """
    pass


class InvalidFileException(Exception):
    """
    Internal library exceptions type
    """
    pass


class CDNJsObject(object):
    """
    CDNJs object
    """

    def __init__(self, name, version, default=None, files=None, keywords=None):
        """
        Init object
        :param name:
        :param version:
        :param str default:
        :param dict files:
        :param list keywords:
        """
        self.name = name
        self.version = version
        self.default = default.split(b'/')[(-1)]
        self.files = files or {}
        self.keywords = keywords or []

    def __str__(self):
        """
        :return str:
        """
        return (b'<{}/{}>').format(self.name, self.version)

    def __unicode__(self):
        """
        :return unicode:
        """
        return str(self)

    def __getitem__(self, item):
        """
        Returns file
        :param item:
        :return:
        """
        for name, obj in self.files.items():
            if name.endswith(item):
                return obj[(b'uri' if Settings.get(b'USE_LOCAL') else b'cdn')]

        raise FileNotFoundException((b'File {} was not found at {}').format(item, self.name))

    def __setitem__(self, key, value):
        """
        Adds file
        :param key:
        :param value:
        :return:
        """
        if b'uri' not in value or b'cdn' not in value:
            raise InvalidFileException((b'File {} that is trying to add is invalid').format(key))
        self.files[key] = value

    def __contains__(self, item):
        """
        Contains file
        :param item:
        :return:
        """
        for f in self.files.keys():
            if item in f:
                return True

    @property
    def dict(self):
        return {b'default': self.default, 
           b'files': self.files}

    @property
    def is_valid(self):
        """
        Is valid
        :return:
        """
        return len(self.files.keys()) > 0

    def matches(self, name, version=None):
        """
        Is matched to name with version
        :param name:
        :param version:
        :return:
        """
        if not any([ name in x for x in self.keywords ]) and name not in self.name:
            return False
        else:
            if version is not None and self.version != version:
                return False
            return True

    def download(self):
        """
        Downloads cdn repository to local storage
        :return:
        """
        storage_path = os.path.join(Settings.get(b'STATIC_ROOT'), self.name, self.version)
        if not os.path.exists(storage_path):
            os.makedirs(storage_path)
        for name, path_data in self.files.items():
            subdir = CDNJs.get_dir(path_data[b'cdn'], self.version)
            dir_path = os.path.join(storage_path, subdir)
            file_path = os.path.join(dir_path, name)
            file_uri = (b'{root}{name}/{version}/{subdir}{file}').format(root=Settings.get(b'STATIC_URL'), name=self.name, version=self.version, subdir=subdir + b'/' if subdir else b'', file=name)
            if not os.path.exists(file_path):
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                with open(file_path, b'w') as (f):
                    for c in requests.get(path_data[b'cdn']):
                        f.write(c)

                    f.close()
            self[name] = {b'cdn': path_data[b'cdn'], b'uri': file_uri}


class CDNJs(object):
    """
    CDNJs.com parser
    """
    API_URL = b'https://api.cdnjs.com/libraries{query}'
    FILE_CDN = b'https://cdnjs.cloudflare.com/ajax/libs/{name}/{version}/{file}'

    @staticmethod
    def get_dir(cdn, version):
        """
        Returns subdirectory
        :param cdn:
        :return:
        """
        filename = cdn.split(b'/')[(-1)]
        return cdn.split(version)[(-1)].replace(filename, b'').strip(b'/')

    def find(self, name, version=None):
        """
        Lads CDNJSObject
        :param name:
        :param version:
        :return CDNJsObject:
        """
        realname = self._find_hit(name)
        if realname is None:
            raise RepositoryNotFoundException((b'Repository {} was not found').format(name))
        return self._load_version(realname, version)

    def _find_hit(self, name):
        """
        Tries to find hits for selected repository
        :param str name:
        :return dict:
        """
        query = {b'search': name}
        response = json.loads(requests.get(self.API_URL.format(query=b'?' + urlencode(query))).text)[b'results'][0]
        return response[b'name']

    def _load_version(self, name, version=None):
        """
        Loads files for selected version
        :param name:
        :param version:
        :return CDNJsObject:
        """
        response = json.loads(requests.get(self.API_URL.format(query=(b'/{}').format(name))).text)
        version = version or response[b'version']
        obj = CDNJsObject(name=response[b'name'], version=version, default=response[b'filename'], keywords=response[b'keywords'])
        for assets in response[b'assets']:
            if assets[b'version'] == version:
                obj.files = self._parse_assets(response[b'name'], assets)

        if not obj.is_valid:
            return None
        else:
            return obj

    def _parse_assets(self, repository, assets):
        """
        Returns files
        :param repository:
        :param assets:
        :return:
        """
        result = {}
        for filename in assets[b'files']:
            result[self._file_name(filename)] = {b'cdn': self._file_cdn(repository, assets[b'version'], filename), 
               b'uri': None}

        return result

    def _file_cdn(self, repository, version, fname):
        """
        Returns file cdn
        :param repository:
        :param version:
        :param fname:
        :return:
        """
        return self.FILE_CDN.format(name=repository, version=version, file=fname)

    def _file_name(self, fname):
        """
        Returns clean filename
        :param fname:
        :return:
        """
        return fname.split(b'/')[(-1)]


class CDNStorage(object):
    """
    CDN Storage
    """
    DB_PATH = os.path.join(Settings.get(b'STATIC_ROOT'), b'cache.json')

    def __init__(self):
        self.database = list(self._load_db())
        self.storage = CDNJs()

    def get(self, repository, filename):
        """
        Returns CDN or URI
        :param repository:
        :param filename:
        :return:
        """
        name, ver = self.parse_name(repository)
        repo = None
        for r in self.database:
            if r.matches(name, ver):
                repo = r
                break

        if repo is None:
            repo = self.storage.find(name, ver)
        if repo is None:
            raise RepositoryNotFoundException((b'Repository {} was not found').find(repository))
        else:
            self.database.append(repo)
        if Settings.get(b'USE_LOCAL'):
            repo.download()
        self._save_db()
        return repo[(filename or repo.default)]

    def _load_db(self):
        """
        Loads cdns from db
        :return CDNJsObject:
        """
        if not os.path.exists(self.DB_PATH):
            return
        with open(self.DB_PATH, b'r') as (f):
            try:
                content = json.loads(f.read())
                for name, info in content.items():
                    for ver, data in info[b'releases'].items():
                        yield CDNJsObject(name=name, version=ver, default=data[b'default'], files=data[b'files'], keywords=info[b'keywords'])

            finally:
                f.close()

    def _save_db(self):
        """
        Saving cdns to db
        :return:
        """
        with open(self.DB_PATH, b'w') as (f):
            data = {}
            for cdn in self.database:
                if cdn.name not in data:
                    data[cdn.name] = {b'releases': {}, b'keywords': cdn.keywords}
                if cdn.version not in data[cdn.name][b'releases']:
                    data[cdn.name][b'releases'][cdn.version] = cdn.dict

            f.write(json.dumps(data, indent=2))

    @staticmethod
    def parse_name(repository_name):
        """
        Parses repository name and version
        :param repository_name:
        :return tuple(str, str):
        """
        pair = repository_name.split(b'/')
        return (pair[0], pair[1] if len(pair) > 1 else None)