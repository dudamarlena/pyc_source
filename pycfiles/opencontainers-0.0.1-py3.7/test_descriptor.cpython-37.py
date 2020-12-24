# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/tests/test_descriptor.py
# Compiled at: 2019-11-06 10:24:34
# Size of source mod 2**32: 9632 bytes
from opencontainers.image.v1 import Descriptor
import os, pytest

def test_descriptor(tmp_path):
    """test creation of opencontiners Descriptor
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