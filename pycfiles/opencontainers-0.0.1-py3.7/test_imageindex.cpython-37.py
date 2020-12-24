# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/tests/test_imageindex.py
# Compiled at: 2019-11-05 17:55:50
# Size of source mod 2**32: 4805 bytes
from opencontainers.image.v1 import Index
import os, pytest
mediatype_invalid_pattern = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'invalid', 
   'size':7143, 
   'digest':'sha256:e692418e4cbaf90ca69d05a66403747baa33ee08806650b51fab815ad7fc331f', 
   'platform':{'architecture':'ppc64le', 
    'os':'linux'}}]}
manifest_invalid_string = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':'7682', 
   'digest':'sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270', 
   'platform':{'architecture':'amd64', 
    'os':'linux'}}]}
digest_missing = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':7682, 
   'platform':{'architecture':'amd64', 
    'os':'linux'}}]}
platform_arch_missing = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':7682, 
   'digest':'sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270', 
   'platform':{'os': 'linux'}}]}
invalid_manifest_mediatype = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'invalid', 
   'size':7682, 
   'digest':'sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270', 
   'platform':{'architecture':'amd64', 
    'os':'linux'}}]}
empty_manifest_mediatype = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'', 
   'size':7682, 
   'digest':'sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270', 
   'platform':{'architecture':'amd64', 
    'os':'linux'}}]}
index_with_optional = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':7143, 
   'digest':'sha256:e692418e4cbaf90ca69d05a66403747baa33ee08806650b51fab815ad7fc331f', 
   'platform':{'architecture':'ppc64le', 
    'os':'linux'}},
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':7682, 
   'digest':'sha256:5b0bcabd1ed22e9fb1310cf6c2dec7cdef19f0ad69efa1f392e94a4333501270', 
   'platform':{'architecture':'amd64', 
    'os':'linux'}}], 
 'annotations':{'com.example.key1':'value1', 
  'com.example.key2':'value2'}}
index_with_required = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/vnd.oci.image.manifest.v1+json', 
   'size':7143, 
   'digest':'sha256:e692418e4cbaf90ca69d05a66403747baa33ee08806650b51fab815ad7fc331f'}]}
index_with_custom = {'schemaVersion':2, 
 'manifests':[
  {'mediaType':'application/customized.manifest+json', 
   'size':7143, 
   'digest':'sha256:e692418e4cbaf90ca69d05a66403747baa33ee08806650b51fab815ad7fc331f', 
   'platform':{'architecture':'ppc64le', 
    'os':'linux'}}]}

def test_imageindex(tmp_path):
    """test creation of a simple sink plugin
    """
    index = Index()
    with pytest.raises(SystemExit):
        index.load(mediatype_invalid_pattern)
    with pytest.raises(SystemExit):
        index.load(manifest_invalid_string)
    with pytest.raises(SystemExit):
        index.load(digest_missing)
    with pytest.raises(SystemExit):
        index.load(platform_arch_missing)
    with pytest.raises(SystemExit):
        index.load(invalid_manifest_mediatype)
    with pytest.raises(SystemExit):
        index.load(empty_manifest_mediatype)
    index.load(index_with_optional)
    index.load(index_with_required)