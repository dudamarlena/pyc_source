# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_make_model_from_service.py
# Compiled at: 2016-02-12 12:18:44
from __future__ import unicode_literals
import os
from sqlalchemy import MetaData
from nose.tools import eq_
from dmsa import make_model_from_service
from dmsa.utility import get_template_models, get_model_json
SERVICE = os.environ.get(b'DMSA_TEST_SERVICE', b'http://data-models.origins.link/')

def test_model_creation():
    for m in get_template_models(SERVICE):
        for v in m[b'versions']:
            yield (
             check_model_creation, m[b'name'], v[b'name'], SERVICE)


def check_model_creation(model, model_version, service):
    model_json = get_model_json(model, model_version, service)
    metadata = MetaData()
    metadata = make_model_from_service(model, model_version, service, metadata)
    eq_(len(metadata.tables), len(model_json[b'tables']))