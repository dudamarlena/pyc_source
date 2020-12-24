# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codebuild/output/src613133936/src/github.com/awslabs/aws-service-catalog-puppet/servicecatalog_puppet/asset_helpers.py
# Compiled at: 2020-05-13 08:59:18
# Size of source mod 2**32: 273 bytes
import os

def resolve_from_site_packages(what):
    return os.path.sep.join([
     os.path.dirname(os.path.abspath(__file__)),
     what])


def read_from_site_packages(what):
    return open(resolve_from_site_packages(what), 'r').read()