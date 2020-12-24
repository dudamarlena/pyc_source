# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/pipeline.py
# Compiled at: 2019-09-30 09:28:30
# Size of source mod 2**32: 1825 bytes
from .base import Base

class Pipeline(Base):

    def __init__(self, api):
        super(Pipeline, self).__init__(api)
        self.api = api

    def get_pipeline_by_id(self, pipeline_id, brief=False, rdepends=False, resolve=None):
        if type(pipeline_id) == list:
            pipeline_id = ','.join([str(m) for m in pipeline_id])
        params = dict(brief=brief,
          rdepends=rdepends,
          resolve=(resolve or []))
        endpoint = '/pipelines/{}'.format(pipeline_id)
        return self.api.GET(endpoint, params=params)

    def create_pipeline(self, pipeline, update_if_exists=False):
        params = dict(update_if_exists=update_if_exists)
        endpoint = '/pipelines'
        return self.api.POST(endpoint, json=pipeline, params=params)

    def update_pipeline(self, pipeline_id, pipeline):
        endpoint = '/pipelines/{}'.format(pipeline_id)
        return self.api.PUT(endpoint, json=pipeline)

    def upload_pipeline_json(self, pipelines, strict=False):
        params = dict(strict=strict)
        endpoint = '/pipelines/json'
        return self.api.POST(endpoint, json=pipelines, params=params)

    def list_pipelines(self, detail=False, rdepends=False, resolve=None, limit=100, page=0):
        params = dict(detail=detail,
          rdepends=rdepends,
          resolve=(resolve or []),
          limit=limit,
          page=page)
        endpoint = '/pipelines'
        return self.api.GET(endpoint, params=params)

    def delete_pipeline_by_id(self, pipeline_id):
        if type(pipeline_id) == list:
            pipeline_id = ','.join([str(m) for m in pipeline_id])
        endpoint = '/pipelines/{}'.format(pipeline_id)
        return self.api.DELETE(endpoint)