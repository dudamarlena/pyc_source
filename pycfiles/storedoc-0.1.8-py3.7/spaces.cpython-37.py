# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/storedoc/spaces.py
# Compiled at: 2019-08-12 00:59:01
# Size of source mod 2**32: 465 bytes
from storedoc.s3 import S3Service

class DOService(S3Service):

    def __init__(self, region_name, endpoint_url, **credentials):
        endpoint_url = 'https://{}.digitaloceanspaces.com'.format(region_name)
        (super(DOService, self).__init__)(region_name, endpoint_url, **credentials)
        self.base_url = endpoint_url
        self.description = 'DigitalOcean Spaces are ideal for storing static, unstructureddata like audio, video, and images as well as large amounts of text'