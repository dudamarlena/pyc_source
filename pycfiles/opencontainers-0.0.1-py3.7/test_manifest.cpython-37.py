# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/tests/test_manifest.py
# Compiled at: 2019-11-06 10:20:41
# Size of source mod 2**32: 6080 bytes
from opencontainers.image.v1 import Manifest
import os, pytest
invalid_mediatype_pattern = {'schemaVersion':2, 
 'config':{'mediaType':'invalid', 
  'size':1470, 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':148, 
   'digest':'sha256:c57089565e894899735d458f0fd4bb17a0f1e0df8d72da392b85c9b35ee777cd'}]}
invalid_config_size_string = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':'1470', 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':148, 
   'digest':'sha256:c57089565e894899735d458f0fd4bb17a0f1e0df8d72da392b85c9b35ee777cd'}]}
invalid_layers_size_string = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':'675598', 
   'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}]}
valid_with_optional = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':675598, 
   'digest':'sha256:9d3dd9504c685a304985025df4ed0283e47ac9ffa9bd0326fddf4d59513f0827'},
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':156, 
   'digest':'sha256:2b689805fbd00b2db1df73fae47562faac1a626d5f61744bfe29946ecff5d73d'},
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':148, 
   'digest':'sha256:c57089565e894899735d458f0fd4bb17a0f1e0df8d72da392b85c9b35ee777cd'}], 
 'annotations':{'key1':'value1', 
  'key2':'value2'}}
valid_with_required = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':675598, 
   'digest':'sha256:9d3dd9504c685a304985025df4ed0283e47ac9ffa9bd0326fddf4d59513f0827'},
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':156, 
   'digest':'sha256:2b689805fbd00b2db1df73fae47562faac1a626d5f61744bfe29946ecff5d73d'},
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':148, 
   'digest':'sha256:c57089565e894899735d458f0fd4bb17a0f1e0df8d72da392b85c9b35ee777cd'}]}
invalid_empty_layers = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[]}
expected_bounds_pass = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256+b64:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':1470, 
   'digest':'sha256+foo-bar:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'},
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':1470, 
   'digest':'sha256.foo-bar:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}]}
expected_bounds_fail = {'schemaVersion':2, 
 'config':{'mediaType':'application/vnd.oci.image.config.v1+json', 
  'size':1470, 
  'digest':'sha256+b64:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}, 
 'layers':[
  {'mediaType':'application/vnd.oci.image.layer.v1.tar+gzip', 
   'size':1470, 
   'digest':'sha256+foo+-b:c86f7763873b6c0aae22d963bab59b4f5debbed6685761b5951584f6efb0633b'}]}

def test_manifests(tmp_path):
    """test creation of a simple sink plugin
    """
    manifest = Manifest()
    with pytest.raises(SystemExit):
        manifest.load(invalid_mediatype_pattern)
    with pytest.raises(SystemExit):
        manifest.load(invalid_config_size_string)
    with pytest.raises(SystemExit):
        manifest.load(invalid_layers_size_string)
    manifest.load(valid_with_optional)
    manifest.load(valid_with_required)
    with pytest.raises(SystemExit):
        manifest.load(invalid_empty_layers)
    manifest.load(expected_bounds_pass)
    with pytest.raises(SystemExit):
        manifest.load(expected_bounds_fail)