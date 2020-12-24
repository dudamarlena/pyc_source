# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/testmaker/middleware/testmaker.py
# Compiled at: 2008-08-03 20:43:08
from django.conf import settings
from django.test import Client
from django.test.utils import setup_test_environment
import re, logging
log = logging.getLogger('testmaker')
print 'Loaded Testmaker Middleware'

class TestMakerMiddleware(object):

    def process_request(self, request):
        if request.method == 'POST' and 'test_client_true' not in request.POST and not re.search('admin', request.path):
            post_str = "'" + request.path + "', {"
            for arg in request.POST:
                post_str += "'" + arg + "': '" + request.POST[arg] + "',"

            post_str += '}'
            log.info('r = c.post(' + post_str + ')')
        if request.method == 'GET' and 'test_client_true' not in request.GET and not re.search('admin', request.path):
            setup_test_environment()
            c = Client()
            get_str = "'%s', {" % request.path
            for arg in request.GET:
                get_str += "'%s': '%s'," % (arg, request.GET[arg])

            get_str += '}'
            log.info('\t\tr = c.get(%s)' % get_str)
            getdict = request.GET.copy()
            getdict['test_client_true'] = 'yes'
            r = c.get(request.path, getdict)
            try:
                log.info('\t\tself.assertEqual(r.status_code, %s)' % r.status_code)
                con = r.context[(-1)].dicts[(-1)]
                if con == {}:
                    con = r.context[(-1)].dicts[0]
                if 'MEDIA_URL' in con:
                    con = {}
                for var in con:
                    if not re.search('0x\\w+', unicode(con[var])):
                        log.info("\t\tself.assertEqual(unicode(r.context[-1]['%s']), '%s')" % (var, unicode(con[var])))

            except (KeyError, TypeError, IndexError), err:
                pass