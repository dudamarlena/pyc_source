# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/test_service.py
# Compiled at: 2016-02-12 12:18:44
import os
from nose.tools import eq_
from dmsa import service
from dmsa.utility import get_template_models
SERVICE = os.environ.get('DMSA_TEST_SERVICE', 'http://data-models.origins.link/')
app = service.build_app(SERVICE)
app.config['TESTING'] = True
test_app = app.test_client()
ENDPOINTS = [
 '/']
for m in get_template_models(SERVICE):
    ENDPOINTS.append('/%s/' % m['name'])
    for v in m['versions']:
        ENDPOINTS.append('/%s/%s/' % (m['name'], v['name']))
        ENDPOINTS.append('/%s/%s/erd/' % (m['name'], v['name']))
        ENDPOINTS.append('/%s/%s/ddl/sqlite/' % (
         m['name'], v['name']))
        ENDPOINTS.append('/%s/%s/drop/sqlite/' % (
         m['name'], v['name']))
        ENDPOINTS.append('/%s/%s/delete/sqlite/' % (
         m['name'], v['name']))
        for e in ['tables', 'indexes']:
            ENDPOINTS.append('/%s/%s/ddl/sqlite/%s/' % (
             m['name'], v['name'], e))
            ENDPOINTS.append('/%s/%s/drop/sqlite/%s/' % (
             m['name'], v['name'], e))

def test_endpoints():
    for endpoint in ENDPOINTS:
        yield (
         check_endpoint, endpoint)


def check_endpoint(endpoint):
    r = test_app.get(endpoint)
    if endpoint.endswith('/erd/'):
        eq_(r.status_code, 302)
        endpoint = r.location[r.location.find('/', 8):]
        r = test_app.get(endpoint)
        eq_(r.status_code, 200)
    else:
        eq_(r.status_code, 200)