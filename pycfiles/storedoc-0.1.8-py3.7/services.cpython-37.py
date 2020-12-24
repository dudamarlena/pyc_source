# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/storedoc/services.py
# Compiled at: 2019-08-12 00:59:01
# Size of source mod 2**32: 1130 bytes
from storedoc.local import LocalStorage
from storedoc.s3 import S3Service
from storedoc.spaces import DOService
SUPPORTED_SERVICES = {'local':{'service':LocalStorage, 
  'description':'Store locally'}, 
 's3':{'service':S3Service, 
  'description':'Amazon S3 or Amazon Simple Storage Service isa "simple storage service" offered by Amazon Web Services that provides object storage through a web service interface.'}, 
 'aws':{'service':S3Service, 
  'description':'Amazon S3 or Amazon Simple Storage Service isa "simple storage service" offered by Amazon Web Services that provides object storage through a web service interface.'}, 
 'spaces':{'service':DOService, 
  'description':'DigitalOcean Spaces are ideal for storing static, unstructureddata like audio, video, and images as well as large amounts of text'}, 
 'do':{'service':DOService, 
  'description':'DigitalOcean Spaces are ideal for storing static, unstructureddata like audio, video, and images as well as large amounts of text'}}