# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/findwatt/client.py
# Compiled at: 2018-10-07 05:33:45
# Size of source mod 2**32: 1125 bytes
"""
Client for FindWAtt's API
"""
import io
from typing import Optional
from .uploads import Uploads
from .catalogs import Catalogs
from .datasets import Datasets

class Client:

    def __init__(self, api_key: str, api_url: str='https://api.findwatt.com/v1/'):
        self.api_key = api_key
        self.auth_header = f"Bearer {self.api_key}"
        self.api_url = api_url
        self.uploads = Uploads(api_key, api_url)
        self.catalogs = Catalogs(api_key, api_url)
        self.datasets = Datasets(api_key, api_url)

    def upload_file(self, file_path: str, catalog_id: Optional[str]=None, catalog_name: Optional[str]=None):
        return self.uploads.upload_file(file_path,
          catalog_id=catalog_id, catalog_name=catalog_name)

    def upload_fileobj(self, fileobj: io.BytesIO, file_name: str, catalog_id: Optional[str]=None, catalog_name: Optional[str]=None):
        return self.uploads.upload_fileobj(fileobj,
          file_name, catalog_id=catalog_id, catalog_name=catalog_name)