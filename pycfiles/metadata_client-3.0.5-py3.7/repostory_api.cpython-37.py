# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/metadata_client/apis/repostory_api.py
# Compiled at: 2017-06-27 18:09:39
# Size of source mod 2**32: 1256 bytes
"""RepositoryApi module class"""
import json
from common.base import Base

class RepositoryApi(Base):

    def create_repository_api(self, repository):
        api_url = self._RepositoryApi__get_api_url()
        return self.api_post(api_url, data=(json.dumps(repository)))

    def delete_repository_api(self, repository_id):
        api_url = self._RepositoryApi__get_api_url(repository_id)
        return self.api_delete(api_url)

    def update_repository_api(self, repository_id, repository):
        api_url = self._RepositoryApi__get_api_url(repository_id)
        return self.api_put(api_url, data=(json.dumps(repository)))

    def get_repository_by_id_api(self, repository_id):
        api_url = self._RepositoryApi__get_api_url(repository_id)
        return self.api_get(api_url, params={})

    def get_all_repositories_by_name_api(self, name):
        api_url = self._RepositoryApi__get_api_url()
        return self.api_get(api_url, params={'name': name})

    def get_all_repositories_by_identifier_api(self, identifier):
        api_url = self._RepositoryApi__get_api_url()
        return self.api_get(api_url, params={'identifier': identifier})

    def __get_api_url(self, api_specifics=''):
        model_name = 'repositories/'
        return self.get_api_url(model_name, api_specifics)