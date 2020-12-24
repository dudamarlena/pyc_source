# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dmsa/tests/output_all_ddl.py
# Compiled at: 2016-02-12 12:18:44
import os, sys, requests
from dmsa import ddl, __version__
from dmsa.utility import get_template_models, get_template_dialects
default_outpath = os.path.join(os.getcwd(), 'dmsa_%s_all_ddl.sql' % __version__)
outpath = sys.argv[1] if len(sys.argv) > 1 else default_outpath
baseurl = os.environ.get('DMSA_TEST_CONTAINER_URL', 'http://127.0.0.1:80/')
f = open(outpath, 'w')
for m in get_template_models(os.environ.get('DMSA_TEST_SERVICE') or 'http://data-models.origins.link/'):
    for v in m['versions']:
        for d in get_template_dialects():
            f.write((' ').join(['#', m['name'], v['name'], d['name'],
             'ddl\n\n']))
            f.write(requests.get(baseurl + '%s/%s/ddl/%s/' % (
             m['name'], v['name'], d['name'])).text)
            f.write((' ').join(['#', m['name'], v['name'], d['name'],
             'drop\n\n']))
            f.write(requests.get(baseurl + '%s/%s/drop/%s/' % (
             m['name'], v['name'], d['name'])).text)
            f.write((' ').join(['#', m['name'], v['name'], d['name'],
             'delete\n\n']))
            f.write(requests.get(baseurl + '%s/%s/delete/%s/' % (
             m['name'], v['name'], d['name'])).text)

        f.write((' ').join(['#', m['name'], v['name'], 'oracle',
         'logging\n\n']))
        f.write(requests.get(baseurl + '%s/%s/logging/oracle/' % (
         m['name'], v['name'])).text)
        f.write((' ').join(['#', m['name'], v['name'], 'oracle',
         'nologging\n\n']))
        f.write(requests.get(baseurl + '%s/%s/nologging/oracle/' % (
         m['name'], v['name'])).text)

f.close()